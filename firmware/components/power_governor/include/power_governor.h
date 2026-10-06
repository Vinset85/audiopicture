#ifndef AUDIOPICTURE_POWER_GOVERNOR_H
#define AUDIOPICTURE_POWER_GOVERNOR_H
#include <stdbool.h>
#include <stdint.h>
typedef enum { AP_SOURCE_NONE, AP_SOURCE_POE, AP_SOURCE_EXT24 } ap_source;
typedef enum { AP_BOOT_SAFE, AP_POE_ECO, AP_EXT_PERFORMANCE, AP_DERATE_POWER,
               AP_DERATE_THERMAL, AP_FAULT_LATCH, AP_RECOVERY } ap_state;
/* All parameters are calibration inputs. No production defaults are implied. */
typedef struct {
 double voltage_min, voltage_max, power_error_w, power_error_fraction;
 double poe_soft_w, poe_hard_w, poe_emergency_w;
 double ext_soft_a, ext_hard_a;
 double attack_db_s, recovery_db_s, max_attenuation_db;
 double poe_transition_attenuation_db, monitor_fallback_attenuation_db;
 double power_hysteresis_w, current_hysteresis_a;
 uint32_t sample_timeout_ms, stable_dwell_ms;
 bool fallback_calibrated;
} ap_governor_config;
typedef struct {
 ap_source source;
 bool type2_verified, rail_5v_good, rail_3v3_good, monitor_valid;
 bool amp_hard_fault, thermal_warning, thermal_critical, reset_fault;
 uint32_t now_ms, sample_time_ms;
 double bus_voltage, bus_current, source_power_w;
} ap_governor_input;
typedef struct {
 ap_governor_config cfg;
 ap_state state;
 ap_source source;
 uint32_t last_ms, stable_since_ms;
 double attenuation_db;
 bool initialized, config_valid, stable_tracking, power_limited;
 bool amp_pdn_asserted, measurement_fault;
} ap_governor;
bool ap_governor_init(ap_governor *, const ap_governor_config *);
void ap_governor_step(ap_governor *, const ap_governor_input *);
#endif
