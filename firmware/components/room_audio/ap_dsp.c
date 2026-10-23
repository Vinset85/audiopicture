#include "ap_dsp.h"
#include <math.h>
#include <string.h>
#include "ap_model_curve_rev_d.h"

static const double PI = 3.14159265358979323846;
static const double BUTTERWORTH4_Q[2] = {0.5411961, 1.3065630};
static const double BUTTERWORTH2_Q = 0.70710678118654752;

bool ap_biquad_design(ap_biquad *bq, ap_biquad_kind kind, double fs, double f0, double q, double gain_db) {
    if(!bq || !isfinite(fs) || !isfinite(f0) || !isfinite(q) || !isfinite(gain_db)) return false;
    if(fs<=0 || f0<=0 || f0>=0.45*fs || q<0.1 || q>20 || fabs(gain_db)>24) return false;
    double w0=2*PI*f0/fs, cw=cos(w0), alpha=sin(w0)/(2*q), b0,b1,b2,a0,a1,a2;
    switch(kind) {
    case AP_BIQUAD_LOWPASS:
        b0=(1-cw)/2; b1=1-cw; b2=(1-cw)/2; a0=1+alpha; a1=-2*cw; a2=1-alpha; break;
    case AP_BIQUAD_HIGHPASS:
        b0=(1+cw)/2; b1=-(1+cw); b2=(1+cw)/2; a0=1+alpha; a1=-2*cw; a2=1-alpha; break;
    case AP_BIQUAD_PEAKING: {
        double amp=pow(10.0,gain_db/40.0);
        b0=1+alpha*amp; b1=-2*cw; b2=1-alpha*amp; a0=1+alpha/amp; a1=-2*cw; a2=1-alpha/amp; break;
    }
    default: return false;
    }
    *bq=(ap_biquad){(float)(b0/a0),(float)(b1/a0),(float)(b2/a0),(float)(a1/a0),(float)(a2/a0),0,0};
    return true;
}

float ap_biquad_process(ap_biquad *bq, float x) {
    float y=bq->b0*x+bq->z1;
    bq->z1=bq->b1*x-bq->a1*y+bq->z2;
    bq->z2=bq->b2*x-bq->a2*y;
    return y;
}

double ap_biquad_response_db(const ap_biquad *bq, double fs, double f) {
    double w=2*PI*f/fs, c1=cos(w), s1=-sin(w), c2=cos(2*w), s2=-sin(2*w);
    double nr=bq->b0+bq->b1*c1+bq->b2*c2, ni=bq->b1*s1+bq->b2*s2;
    double dr=1+bq->a1*c1+bq->a2*c2, di=bq->a1*s1+bq->a2*s2;
    return 10*log10((nr*nr+ni*ni)/(dr*dr+di*di));
}

void ap_twoway_default_config(ap_twoway_config *cfg) {
    if(!cfg) return;
    memset(cfg,0,sizeof(*cfg));
    cfg->sample_rate_hz=AP_MODEL_SAMPLE_RATE_HZ;
    cfg->crossover_hz=AP_MODEL_CROSSOVER_HZ;
    cfg->subsonic_hz=AP_MODEL_SUBSONIC_HZ;
    cfg->tweeter_pad_db=AP_MODEL_TWEETER_PAD_DB;
    cfg->role=AP_ROLE_SOLO;
    cfg->eq_count=AP_MODEL_EQ_COUNT;
    for(size_t i=0;i<AP_MODEL_EQ_COUNT;i++)
        cfg->eq[i]=(ap_eq_band){ap_model_eq_rev_d[i].hz,ap_model_eq_rev_d[i].q,ap_model_eq_rev_d[i].gain_db};
}

static ap_dsp_result check(const ap_twoway_config *c) {
    if(c->sample_rate_hz!=44100.0 && c->sample_rate_hz!=48000.0) return AP_DSP_RATE;
    if(!isfinite(c->crossover_hz) || c->crossover_hz<1500 || c->crossover_hz>5000) return AP_DSP_CROSSOVER;
    if(!isfinite(c->subsonic_hz) || c->subsonic_hz<20 || c->subsonic_hz>80) return AP_DSP_SUBSONIC;
    if(!isfinite(c->tweeter_pad_db) || c->tweeter_pad_db<-20 || c->tweeter_pad_db>0) return AP_DSP_PAD;
    if(!isfinite(c->trim_db) || c->trim_db<-30 || c->trim_db>0) return AP_DSP_TRIM;
    if(c->delay_samples>AP_DSP_MAX_DELAY_SAMPLES) return AP_DSP_DELAY;
    if(c->role!=AP_ROLE_SOLO && c->role!=AP_ROLE_LEFT && c->role!=AP_ROLE_RIGHT && c->role!=AP_ROLE_FILL)
        return AP_DSP_ROLE;
    if(c->eq_count>AP_DSP_MAX_EQ) return AP_DSP_EQ;
    for(size_t i=0;i<c->eq_count;i++) {
        const ap_eq_band *e=&c->eq[i];
        if(!isfinite(e->gain_db) || e->gain_db>AP_DSP_MAX_BOOST_DB || e->gain_db<-15) return AP_DSP_EQ;
    }
    return AP_DSP_OK;
}

ap_dsp_result ap_twoway_init(ap_twoway *dsp, const ap_twoway_config *cfg) {
    if(!dsp) return AP_DSP_ARGUMENT;
    memset(dsp,0,sizeof(*dsp));
    if(!cfg) return AP_DSP_ARGUMENT;
    ap_dsp_result r=check(cfg); if(r!=AP_DSP_OK) return r;
    double fs=cfg->sample_rate_hz;
    for(int i=0;i<2;i++) {
        if(!ap_biquad_design(&dsp->subsonic[i],AP_BIQUAD_HIGHPASS,fs,cfg->subsonic_hz,BUTTERWORTH4_Q[i],0))
            return AP_DSP_SUBSONIC;
        if(!ap_biquad_design(&dsp->woofer[i],AP_BIQUAD_LOWPASS,fs,cfg->crossover_hz,BUTTERWORTH2_Q,0) ||
           !ap_biquad_design(&dsp->tweeter[i],AP_BIQUAD_HIGHPASS,fs,cfg->crossover_hz,BUTTERWORTH2_Q,0))
            return AP_DSP_CROSSOVER;
    }
    for(size_t i=0;i<cfg->eq_count;i++)
        if(!ap_biquad_design(&dsp->eq[i],AP_BIQUAD_PEAKING,fs,cfg->eq[i].hz,cfg->eq[i].q,cfg->eq[i].gain_db))
            return AP_DSP_EQ;
    /* Overlapping bands must not sum past the boost ceiling anywhere in the audio band. */
    for(int k=0;k<=480;k++) {
        double f=20*pow(1000.0,k/480.0), total=0;
        for(size_t i=0;i<cfg->eq_count;i++) total+=ap_biquad_response_db(&dsp->eq[i],fs,f);
        if(total>AP_DSP_MAX_BOOST_DB+0.01) { memset(dsp,0,sizeof(*dsp)); return AP_DSP_BOOST; }
    }
    dsp->cfg=*cfg;
    dsp->trim=(float)pow(10.0,cfg->trim_db/20.0);
    dsp->tweeter_gain=(float)pow(10.0,cfg->tweeter_pad_db/20.0);
    dsp->ready=true;
    return AP_DSP_OK;
}

static float select_input(ap_role role, float l, float r) {
    if(!isfinite(l)) l=0;
    if(!isfinite(r)) r=0;
    switch(role) {
    case AP_ROLE_LEFT: return l;
    case AP_ROLE_RIGHT: return r;
    default: return 0.5f*(l+r);
    }
}

void ap_twoway_process(ap_twoway *dsp, const float *stereo, float *woofer, float *tweeter, size_t frames) {
    if(!woofer || !tweeter) return;
    if(!dsp || !dsp->ready || !stereo) {
        for(size_t n=0;n<frames;n++) woofer[n]=tweeter[n]=0;
        return;
    }
    const uint32_t size=AP_DSP_MAX_DELAY_SAMPLES+1;
    for(size_t n=0;n<frames;n++) {
        dsp->delay[dsp->head]=select_input(dsp->cfg.role,stereo[2*n],stereo[2*n+1]);
        float x=dsp->delay[(dsp->head+size-dsp->cfg.delay_samples)%size];
        dsp->head=(dsp->head+1)%size;
        x=ap_biquad_process(&dsp->subsonic[1],ap_biquad_process(&dsp->subsonic[0],x));
        for(size_t i=0;i<dsp->cfg.eq_count;i++) x=ap_biquad_process(&dsp->eq[i],x);
        x*=dsp->trim;
        woofer[n]=ap_biquad_process(&dsp->woofer[1],ap_biquad_process(&dsp->woofer[0],x));
        tweeter[n]=dsp->tweeter_gain*ap_biquad_process(&dsp->tweeter[1],ap_biquad_process(&dsp->tweeter[0],x));
    }
}
