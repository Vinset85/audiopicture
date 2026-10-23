/* Auto-intent: Rev.E provisional DML factory starting curve.
 * NOT A MEASUREMENT. Replace after first-article vibrometry + 1 m sweep.
 * Channel A = EX_LF (LowFreq), channel B = EX_WB (wideband). */
#ifndef AP_MODEL_CURVE_REV_E_H
#define AP_MODEL_CURVE_REV_E_H
#define AP_MODEL_SAMPLE_RATE_HZ 48000.0
#define AP_MODEL_CROSSOVER_HZ 450.0
#define AP_MODEL_SUBSONIC_HZ 35.0
#define AP_MODEL_TWEETER_PAD_DB (0.0)
#define AP_MODEL_EQ_COUNT 2u
/* Mild modal seeds: refine from evidence/rev-e after FEA/measure. */
static const struct { double hz, q, gain_db; } ap_model_eq_rev_e[] = {
    {55.0, 1.20, 4.50},
    {180.0, 2.50, -2.00},
};
#endif
