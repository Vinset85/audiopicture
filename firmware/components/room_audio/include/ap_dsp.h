#ifndef AP_DSP_H
#define AP_DSP_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
/* Dual-output chain (Rev.E DML: EX_LF + EX_WB; still named woofer/tweeter in the API).
 * Role select, delay, subsonic, EQ, trim, LR4 split, pad. Defaults from ap_model_curve_rev_e.h.
 * Gains never exceed AP_DSP_MAX_BOOST_DB; panel limits have authority over bass. */
typedef struct { float b0, b1, b2, a1, a2, z1, z2; } ap_biquad;
typedef enum { AP_BIQUAD_LOWPASS, AP_BIQUAD_HIGHPASS, AP_BIQUAD_PEAKING } ap_biquad_kind;
bool ap_biquad_design(ap_biquad *, ap_biquad_kind, double fs, double f0, double q, double gain_db);
float ap_biquad_process(ap_biquad *, float x);
double ap_biquad_response_db(const ap_biquad *, double fs, double f);

typedef enum { AP_ROLE_SOLO, AP_ROLE_LEFT, AP_ROLE_RIGHT, AP_ROLE_FILL } ap_role;
#define AP_DSP_MAX_EQ 8u
#define AP_DSP_MAX_DELAY_SAMPLES 2400u
#define AP_DSP_MAX_BOOST_DB 6.0
typedef struct { double hz, q, gain_db; } ap_eq_band;
typedef struct {
    double sample_rate_hz, crossover_hz, subsonic_hz;
    double tweeter_pad_db, trim_db;
    uint32_t delay_samples;
    ap_role role;
    size_t eq_count;
    ap_eq_band eq[AP_DSP_MAX_EQ];
} ap_twoway_config;
typedef struct {
    ap_twoway_config cfg;
    ap_biquad subsonic[2], eq[AP_DSP_MAX_EQ], woofer[2], tweeter[2];
    float trim, tweeter_gain;
    float delay[AP_DSP_MAX_DELAY_SAMPLES + 1];
    uint32_t head;
    bool ready;
} ap_twoway;
typedef enum {
    AP_DSP_OK, AP_DSP_ARGUMENT, AP_DSP_RATE, AP_DSP_CROSSOVER, AP_DSP_SUBSONIC,
    AP_DSP_PAD, AP_DSP_TRIM, AP_DSP_DELAY, AP_DSP_ROLE, AP_DSP_EQ, AP_DSP_BOOST
} ap_dsp_result;
/* Rev.D box-model starting curve. Not a factory measurement. */
void ap_twoway_default_config(ap_twoway_config *);
/* On any error the chain is left not ready and outputs silence. */
ap_dsp_result ap_twoway_init(ap_twoway *, const ap_twoway_config *);
/* stereo: interleaved L,R. Non-finite input samples are replaced by silence. */
void ap_twoway_process(ap_twoway *, const float *stereo, float *woofer, float *tweeter, size_t frames);
#endif
