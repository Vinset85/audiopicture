#ifndef AP_STATUS_H
#define AP_STATUS_H
#include "ap_environment.h"
/* TCA9534 @ 0x20, A2/A1/A0 grounded, diagnostic inputs only.
 * No chip-ID register exists. Register verification is not device identity,
 * electrical source qualification, or permission to enable the amplifier. */
ap_sensor_result ap_status_configure(const ap_bus *);
ap_sensor_result ap_status_read(const ap_bus *, uint8_t *raw);
#endif
