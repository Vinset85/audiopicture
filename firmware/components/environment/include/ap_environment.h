#ifndef AP_ENVIRONMENT_H
#define AP_ENVIRONMENT_H
#include <stddef.h>
#include <stdint.h>
/* Transport returns zero only after every requested byte has transferred. */
typedef int (*ap_i2c_transfer)(void *, uint8_t, const uint8_t *, size_t, uint8_t *, size_t);
typedef void (*ap_delay_ms)(void *, unsigned);
typedef struct { void *context; ap_i2c_transfer transfer; ap_delay_ms delay; } ap_bus;
typedef enum { AP_SENSOR_OK, AP_SENSOR_ARGUMENT, AP_SENSOR_IO, AP_SENSOR_CRC,
               AP_SENSOR_ID, AP_SENSOR_TIMEOUT, AP_SENSOR_RANGE,
               AP_SENSOR_CONFIG } ap_sensor_result;
typedef struct { double temperature_c, humidity_percent; } ap_sht_reading;
typedef struct { double bus_v, shunt_v, current_a, calculated_power_w, die_c; } ap_ina_reading;
uint8_t ap_sht_crc(const uint8_t data[2]);
ap_sensor_result ap_sht_decode(const uint8_t data[6], ap_sht_reading *out);
ap_sensor_result ap_sht_measure(const ap_bus *, ap_sht_reading *out);
ap_sensor_result ap_sht_serial(const ap_bus *, uint32_t *out);
ap_sensor_result ap_opt_decode(uint16_t result, uint16_t config, double *lux);
ap_sensor_result ap_opt_measure(const ap_bus *, double *lux);
/* Caller must supply the strapped address and nominal or measured shunt value.
 * Current/power are calculated from raw Vshunt/Vbus, not calibrated power registers.
 * This single-shot diagnostic driver is not the real-time amplifier governor loop. */
ap_sensor_result ap_ina_decode(const uint8_t bus[3], const uint8_t shunt[3],
    const uint8_t die[2], double shunt_ohm, ap_ina_reading *out);
ap_sensor_result ap_ina_measure(const ap_bus *, uint8_t address,
                               double shunt_ohm, ap_ina_reading *out);
#endif
