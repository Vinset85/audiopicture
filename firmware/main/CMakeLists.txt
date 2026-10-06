idf_component_register(SRCS "app_main.c" "ap_network.c" INCLUDE_DIRS "."
 REQUIRES environment power_governor esp_driver_gpio esp_driver_i2c esp_driver_spi
 esp_eth esp_netif esp_event esp_wifi esp_http_server nvs_flash esp_timer json app_update)
