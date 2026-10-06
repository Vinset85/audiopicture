#include "ap_network.h"
#include <string.h>
#include "esp_check.h"
#include "esp_eth.h"
#include "esp_eth_mac_spi.h"
#include "esp_eth_netif_glue.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_mac.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "mdns.h"
#include "nvs.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
static const char *TAG="ap_network";
static bool wifi_configured;
static esp_err_t ethernet_start(const char *hostname) {
    spi_bus_config_t spi={.mosi_io_num=11,.miso_io_num=13,.sclk_io_num=12,
        .quadwp_io_num=-1,.quadhd_io_num=-1};
    ESP_RETURN_ON_ERROR(spi_bus_initialize(SPI2_HOST,&spi,SPI_DMA_CH_AUTO),TAG,"SPI initialization");
    esp_err_t err=gpio_install_isr_service(0);
    if(err!=ESP_OK && err!=ESP_ERR_INVALID_STATE) return err;
    spi_device_interface_config_t dev={.mode=0,.clock_speed_hz=10*1000*1000,
        .spics_io_num=10,.queue_size=20};
    eth_w5500_config_t w=ETH_W5500_DEFAULT_CONFIG(SPI2_HOST,&dev); w.int_gpio_num=9;
    eth_mac_config_t mc=ETH_MAC_DEFAULT_CONFIG();
    eth_phy_config_t pc=ETH_PHY_DEFAULT_CONFIG(); pc.phy_addr=1; pc.reset_gpio_num=8;
    esp_eth_mac_t *mac=esp_eth_mac_new_w5500(&w,&mc);
    esp_eth_phy_t *phy=esp_eth_phy_new_w5500(&pc);
    if(!mac || !phy) return ESP_ERR_NO_MEM;
    esp_eth_config_t config=ETH_DEFAULT_CONFIG(mac,phy); esp_eth_handle_t eth=NULL;
    err=esp_eth_driver_install(&config,&eth);
    if(err!=ESP_OK) { mac->del(mac); phy->del(phy); return err; }
    uint8_t address[6]; ESP_RETURN_ON_ERROR(esp_read_mac(address,ESP_MAC_ETH),TAG,"factory MAC read");
    ESP_RETURN_ON_ERROR(esp_eth_ioctl(eth,ETH_CMD_S_MAC_ADDR,address),TAG,"Ethernet MAC");
    esp_netif_inherent_config_t base=ESP_NETIF_INHERENT_DEFAULT_ETH(); base.route_prio=100;
    esp_netif_config_t nc={.base=&base,.stack=ESP_NETIF_NETSTACK_DEFAULT_ETH};
    esp_netif_t *net=esp_netif_new(&nc);
    if(!net) return ESP_ERR_NO_MEM;
    ESP_RETURN_ON_ERROR(esp_netif_set_hostname(net,hostname),TAG,"hostname");
    esp_eth_netif_glue_handle_t glue=esp_eth_new_netif_glue(eth);
    if(!glue) return ESP_ERR_NO_MEM;
    ESP_RETURN_ON_ERROR(esp_netif_attach(net,glue),TAG,"attach");
    return esp_eth_start(eth);
}
static void wifi_event(void *arg,esp_event_base_t base,int32_t id,void *data) {
    (void)arg; (void)data;
    if(base==WIFI_EVENT && (id==WIFI_EVENT_STA_START || id==WIFI_EVENT_STA_DISCONNECTED)) {
        /* Retries occur in the background task, never recursively in this event. */
        ESP_LOGI(TAG,"Wi-Fi awaiting connection");
    }
}
static void retry_wifi(void *arg) {
    (void)arg;
    for(;;) {
        wifi_ap_record_t ap;
        if(wifi_configured && esp_wifi_sta_get_ap_info(&ap)!=ESP_OK) esp_wifi_connect();
        vTaskDelay(pdMS_TO_TICKS(10000));
    }
}
static esp_err_t wifi_start(const char *hostname) {
    nvs_handle_t h;
    if(nvs_open("network",NVS_READONLY,&h)!=ESP_OK) return ESP_ERR_NOT_FOUND;
    char ssid[33]={0},password[65]={0}; size_t sn=sizeof(ssid),pn=sizeof(password);
    esp_err_t err=nvs_get_str(h,"ssid",ssid,&sn);
    if(err==ESP_OK) err=nvs_get_str(h,"password",password,&pn);
    nvs_close(h); if(err!=ESP_OK || !ssid[0]) return ESP_ERR_NOT_FOUND;
    esp_netif_t *net=esp_netif_create_default_wifi_sta();
    if(!net) return ESP_ERR_NO_MEM;
    ESP_RETURN_ON_ERROR(esp_netif_set_hostname(net,hostname),TAG,"Wi-Fi hostname");
    wifi_init_config_t init=WIFI_INIT_CONFIG_DEFAULT();
    ESP_RETURN_ON_ERROR(esp_wifi_init(&init),TAG,"Wi-Fi init");
    ESP_RETURN_ON_ERROR(esp_wifi_set_storage(WIFI_STORAGE_RAM),TAG,"Wi-Fi storage");
    wifi_config_t cfg={0}; memcpy(cfg.sta.ssid,ssid,strlen(ssid));
    memcpy(cfg.sta.password,password,strlen(password));
    cfg.sta.threshold.authmode=WIFI_AUTH_WPA2_PSK; cfg.sta.pmf_cfg.capable=true;
    ESP_RETURN_ON_ERROR(esp_event_handler_register(WIFI_EVENT,ESP_EVENT_ANY_ID,wifi_event,NULL),TAG,"Wi-Fi handler");
    ESP_RETURN_ON_ERROR(esp_wifi_set_mode(WIFI_MODE_STA),TAG,"Wi-Fi mode");
    ESP_RETURN_ON_ERROR(esp_wifi_set_config(WIFI_IF_STA,&cfg),TAG,"Wi-Fi config");
    memset(password,0,sizeof(password)); memset(&cfg,0,sizeof(cfg));
    ESP_RETURN_ON_ERROR(esp_wifi_start(),TAG,"Wi-Fi start");
    wifi_configured=true;
    return xTaskCreate(retry_wifi,"wifi_retry",3072,NULL,3,NULL)==pdPASS?ESP_OK:ESP_ERR_NO_MEM;
}
void ap_network_start(const char *hostname,const char *uuid) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_err_t eth=ethernet_start(hostname),wifi=wifi_start(hostname);
    ESP_LOGI(TAG,"Ethernet initialization: %s; Wi-Fi initialization: %s",esp_err_to_name(eth),esp_err_to_name(wifi));
    ESP_ERROR_CHECK(mdns_init()); ESP_ERROR_CHECK(mdns_hostname_set(hostname));
    ESP_ERROR_CHECK(mdns_instance_name_set("AudioPicture"));
    mdns_txt_item_t txt[]={{"uuid",uuid},{"model","OS-PF320-V22"},{"api","1"},{"stage","diagnostic"}};
    ESP_ERROR_CHECK(mdns_service_add(NULL,"_audiopicture","_tcp",80,txt,4));
}
