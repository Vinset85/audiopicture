#ifndef AP_CLOCK_H
#define AP_CLOCK_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
/* Follower-side estimate of the room master clock from four-timestamp exchanges
 * (t1 local send, t2 master receive, t3 master send, t4 local receive; microseconds).
 * The lowest-delay eighth of the window (never fewer than four) is fitted for offset and drift. */
#define AP_CLOCK_WINDOW 64u
#define AP_CLOCK_MIN_SAMPLES 16u
#define AP_CLOCK_MIN_FIT 4u
#define AP_CLOCK_MAX_DRIFT_PPM 500.0
#define AP_CLOCK_MAX_PATH_US 1000000
typedef struct { int64_t t1, t2, t3, t4; } ap_clock_exchange;
typedef struct { int64_t local_us; double offset_us, delay_us; } ap_clock_sample;
typedef struct {
    ap_clock_sample window[AP_CLOCK_WINDOW];
    size_t count, next;
    double lock_us;
    int64_t ref_local_us;
    double offset_us, drift, residual_us;
    bool locked;
} ap_clock;
/* lock_us: residual RMS required for lock; Rev.D uses 25 us per unit inside a stereo pair. */
void ap_clock_init(ap_clock *, double lock_us);
/* Rejects inconsistent timestamps, negative path delay and paths above AP_CLOCK_MAX_PATH_US. */
bool ap_clock_add(ap_clock *, const ap_clock_exchange *);
/* False until locked. */
bool ap_clock_to_master(const ap_clock *, int64_t local_us, int64_t *master_us);
#endif
