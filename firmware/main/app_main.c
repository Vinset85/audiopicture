#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include "ap_environment.h"
#include "ap_status.h"
#include "ap_network.h"
#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "esp_app_desc.h"
#include "esp_http_server.h"
#include "esp_log.h"
#include "esp_random.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "cJSON.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
static const char *TAG="audiopicture";
static char device_uuid[37];
static i2c_master_dev_handle_t devices[4];
static SemaphoreHandle_t lock;
static struct {
    ap_sht_reading sht; ap_ina_reading ina; double lux;
    ap_sensor_result sht_error,opt_error,ina_error;
    int64_t sht_time,opt_time,ina_time;
    uint8_t power_status_raw;
    ap_sensor_result status_error;
    int64_t status_time;
} snapshot;
static void set_output(int pin,int level) {
    /* Preload the output latch before enabling the driver. External bias is still
     * required during ROM boot/reset, before any application instruction runs. */
    ESP_ERROR_CHECK(gpio_set_level(pin,level));
    ESP_ERROR_CHECK(gpio_set_direction(pin,GPIO_MODE_OUTPUT));
}
static void safe_outputs(void) {
    const int low[]={2,21,16,42,8,38};
    for(unsigned i=0;i<sizeof(low)/sizeof(low[0]);i++) set_output(low[i],0);
    set_output(10,1); set_output(14,1); set_output(40,0);
    const int input[]={1,9,15,39,41};
    for(unsigned i=0;i<sizeof(input)/sizeof(input[0]);i++)
        ESP_ERROR_CHECK(gpio_set_direction(input[i],GPIO_MODE_INPUT));
}
static esp_err_t identity_init(void) {
    /* Never erase identity or calibration automatically on an NVS error. */
    esp_err_t err=nvs_flash_init(); if(err!=ESP_OK) return err;
    nvs_handle_t h; err=nvs_open("identity",NVS_READWRITE,&h); if(err!=ESP_OK) return err;
    size_t size=sizeof(device_uuid); err=nvs_get_str(h,"uuid",device_uuid,&size);
    if(err==ESP_ERR_NVS_NOT_FOUND) {
        uint8_t u[16]; esp_fill_random(u,sizeof(u)); u[6]=(u[6]&15)|0x40; u[8]=(u[8]&63)|0x80;
        snprintf(device_uuid,sizeof(device_uuid),"%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",
          u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],u[10],u[11],u[12],u[13],u[14],u[15]);
        err=nvs_set_str(h,"uuid",device_uuid); if(err==ESP_OK) err=nvs_commit(h);
    }
    nvs_close(h);
    if(err==ESP_OK && strlen(device_uuid)!=36) return ESP_ERR_INVALID_STATE;
    return err;
}
static int transfer(void *ctx,uint8_t address,const uint8_t *tx,size_t nt,uint8_t *rx,size_t nr) {
    (void)ctx; int i=address==0x44?0:address==0x45?1:address==0x40?2:address==0x20?3:-1;
    if(i<0 || !devices[i]) return -1;
    if(nt && nr) return i2c_master_transmit_receive(devices[i],tx,nt,rx,nr,100);
    if(nt) return i2c_master_transmit(devices[i],tx,nt,100);
    return i2c_master_receive(devices[i],rx,nr,100);
}
static void delay(void *ctx,unsigned ms) { (void)ctx; vTaskDelay(pdMS_TO_TICKS(ms)+1); }
static esp_err_t bus_init(void) {
    i2c_master_bus_config_t cfg={.i2c_port=I2C_NUM_0,.sda_io_num=17,.scl_io_num=18,
        .clk_source=I2C_CLK_SRC_DEFAULT,.glitch_ignore_cnt=7,.flags.enable_internal_pullup=false};
    i2c_master_bus_handle_t bus; esp_err_t err=i2c_new_master_bus(&cfg,&bus);
    if(err!=ESP_OK) return err;
    const uint8_t addresses[]={0x44,0x45,0x40,0x20};
    for(unsigned i=0;i<4;i++) {
        i2c_device_config_t dev={.dev_addr_length=I2C_ADDR_BIT_LEN_7,.device_address=addresses[i],.scl_speed_hz=100000};
        err=i2c_master_bus_add_device(bus,&dev,&devices[i]); if(err!=ESP_OK) return err;
    }
    return ESP_OK;
}
static void sensors(void *arg) {
    (void)arg; ap_bus bus={NULL,transfer,delay}; bool status_ready=false;
    for(;;) {
        ap_sht_reading sht; ap_ina_reading ina; double lux;
        ap_sensor_result se=ap_sht_measure(&bus,&sht); int64_t st=esp_timer_get_time()/1000;
        ap_sensor_result oe=ap_opt_measure(&bus,&lux); int64_t ot=esp_timer_get_time()/1000;
        ap_sensor_result ie=ap_ina_measure(&bus,0x40,0.008,&ina); int64_t it=esp_timer_get_time()/1000;
        /* Raw diagnostic status only: neither PHY type detection nor these
         * bits establish a qualified source power budget. Audio stays off. */
        uint8_t raw=0;
        ap_sensor_result pe=status_ready?AP_SENSOR_OK:ap_status_configure(&bus);
        if(pe==AP_SENSOR_OK) pe=ap_status_read(&bus,&raw);
        status_ready=pe==AP_SENSOR_OK;
        int64_t pt=esp_timer_get_time()/1000;
        xSemaphoreTake(lock,portMAX_DELAY);
        snapshot.sht_error=se; snapshot.opt_error=oe; snapshot.ina_error=ie;
        snapshot.status_error=pe;
        if(se==AP_SENSOR_OK) { snapshot.sht=sht; snapshot.sht_time=st; }
        if(oe==AP_SENSOR_OK) { snapshot.lux=lux; snapshot.opt_time=ot; }
        if(ie==AP_SENSOR_OK) { snapshot.ina=ina; snapshot.ina_time=it; }
        if(pe==AP_SENSOR_OK) { snapshot.power_status_raw=raw; snapshot.status_time=pt; }
        xSemaphoreGive(lock);
        vTaskDelay(pdMS_TO_TICKS(30000));
    }
}
static esp_err_t reply(httpd_req_t *req,cJSON *root) {
    if(!root) return httpd_resp_send_err(req,HTTPD_500_INTERNAL_SERVER_ERROR,"memory");
    char *body=cJSON_PrintUnformatted(root); cJSON_Delete(root);
    if(!body) return httpd_resp_send_err(req,HTTPD_500_INTERNAL_SERVER_ERROR,"memory");
    httpd_resp_set_type(req,"application/json"); httpd_resp_set_hdr(req,"Cache-Control","no-store");
    esp_err_t err=httpd_resp_send(req,body,HTTPD_RESP_USE_STRLEN); cJSON_free(body); return err;
}
static esp_err_t info(httpd_req_t *req) {
    cJSON *root=cJSON_CreateObject(); if(!root) return reply(req,NULL);
    cJSON_AddNumberToObject(root,"api_version",1);
    cJSON_AddStringToObject(root,"uuid",device_uuid);
    cJSON_AddStringToObject(root,"model","OS-PF320-V22");
    cJSON_AddStringToObject(root,"firmware",esp_app_get_description()->version);
    cJSON_AddStringToObject(root,"stage","diagnostic");
    cJSON_AddBoolToObject(root,"commissioned",false);
    cJSON *cap=cJSON_AddObjectToObject(root,"capabilities");
    cJSON_AddBoolToObject(cap,"environment",true); cJSON_AddBoolToObject(cap,"power_diagnostics",true);
    cJSON_AddBoolToObject(cap,"audio",false); cJSON_AddBoolToObject(cap,"radar",false);
    cJSON_AddBoolToObject(cap,"voice",false); cJSON_AddBoolToObject(cap,"ota",false);
    return reply(req,root);
}
static void metric(cJSON *root,const char *key,double value,bool valid) {
    if(valid) cJSON_AddNumberToObject(root,key,value); else cJSON_AddNullToObject(root,key);
}
static esp_err_t status(httpd_req_t *req) {
    int64_t now=esp_timer_get_time()/1000;
    cJSON *root=cJSON_CreateObject(); if(!root) return reply(req,NULL);
    cJSON_AddNumberToObject(root,"api_version",1); cJSON_AddStringToObject(root,"uuid",device_uuid);
    cJSON_AddNumberToObject(root,"uptime_ms",(double)now);
    cJSON_AddBoolToObject(root,"amplifier_enabled",false); cJSON_AddBoolToObject(root,"microphones_enabled",false);
    cJSON_AddStringToObject(root,"inhibit_reason","hardware_and_calibration_unqualified");
    xSemaphoreTake(lock,portMAX_DELAY);
    bool s=snapshot.sht_error==AP_SENSOR_OK && now-snapshot.sht_time<=90000;
    bool o=snapshot.opt_error==AP_SENSOR_OK && now-snapshot.opt_time<=90000;
    bool i=snapshot.ina_error==AP_SENSOR_OK && now-snapshot.ina_time<=90000;
    bool p=snapshot.status_error==AP_SENSOR_OK && now-snapshot.status_time<=90000;
    metric(root,"temperature_raw_c",snapshot.sht.temperature_c,s);
    metric(root,"humidity_raw_percent",snapshot.sht.humidity_percent,s);
    metric(root,"illuminance_raw_lux",snapshot.lux,o);
    metric(root,"bus_voltage_v",snapshot.ina.bus_v,i);
    metric(root,"current_nominal_shunt_a",snapshot.ina.current_a,i);
    metric(root,"power_calculated_w",snapshot.ina.calculated_power_w,i);
    metric(root,"monitor_die_c",snapshot.ina.die_c,i);
    metric(root,"power_status_raw",snapshot.power_status_raw,p);
    cJSON_AddBoolToObject(root,"type2_verified",false);
    cJSON *errors=cJSON_AddObjectToObject(root,"sensor_errors");
    cJSON_AddNumberToObject(errors,"sht45",snapshot.sht_error);
    cJSON_AddNumberToObject(errors,"opt3004",snapshot.opt_error);
    cJSON_AddNumberToObject(errors,"ina228",snapshot.ina_error);
    cJSON_AddNumberToObject(errors,"status_expander",snapshot.status_error);
    xSemaphoreGive(lock); return reply(req,root);
}
void app_main(void) {
    safe_outputs();
    ESP_ERROR_CHECK(identity_init());
    lock=xSemaphoreCreateMutex(); if(!lock) abort();
    snapshot.sht_error=snapshot.opt_error=snapshot.ina_error=AP_SENSOR_TIMEOUT;
    snapshot.status_error=AP_SENSOR_TIMEOUT;
    char hostname[32]; snprintf(hostname,sizeof(hostname),"audiopicture-%.8s",device_uuid);
    ap_network_start(hostname,device_uuid);
    esp_err_t err=bus_init();
    if(err==ESP_OK) {
        if(xTaskCreate(sensors,"ap_sensors",4096,NULL,4,NULL)!=pdPASS) abort();
    } else ESP_LOGE(TAG,"I2C unavailable: %s",esp_err_to_name(err));
    httpd_config_t hc=HTTPD_DEFAULT_CONFIG(); hc.stack_size=6144; httpd_handle_t server;
    ESP_ERROR_CHECK(httpd_start(&server,&hc));
    const httpd_uri_t routes[]={{.uri="/api/v1/info",.method=HTTP_GET,.handler=info},
                               {.uri="/api/v1/status",.method=HTTP_GET,.handler=status}};
    for(unsigned i=0;i<2;i++) ESP_ERROR_CHECK(httpd_register_uri_handler(server,&routes[i]));
    ESP_LOGI(TAG,"Diagnostic firmware ready; audio, microphones and radar remain off");
}
