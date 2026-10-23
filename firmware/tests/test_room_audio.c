#include "ap_clock.h"
#include "ap_dsp.h"
#include "ap_room.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#define FS 48000.0
static const double PI = 3.14159265358979323846;

typedef struct { double re, im; } cpx;
static cpx response(const ap_biquad *bq, double f) {
    double w=2*PI*f/FS;
    double nr=bq->b0+bq->b1*cos(w)+bq->b2*cos(2*w), ni=-(bq->b1*sin(w)+bq->b2*sin(2*w));
    double dr=1+bq->a1*cos(w)+bq->a2*cos(2*w), di=-(bq->a1*sin(w)+bq->a2*sin(2*w));
    double d=dr*dr+di*di;
    return (cpx){(nr*dr+ni*di)/d,(ni*dr-nr*di)/d};
}
static cpx mul(cpx a, cpx b) { return (cpx){a.re*b.re-a.im*b.im,a.re*b.im+a.im*b.re}; }
static double mag_db(cpx a) { return 10*log10(a.re*a.re+a.im*a.im); }

static ap_twoway_config flat(void) {
    ap_twoway_config c; ap_twoway_default_config(&c);
    c.eq_count=0; c.tweeter_pad_db=0; c.trim_db=0;
    return c;
}

/* Steady-state RMS of woofer+tweeter for a sine on the selected input channels. */
static double sine_gain(ap_twoway *dsp, double f, double left, double right) {
    static float in[2*48000], w[48000], t[48000];
    for(int n=0;n<48000;n++) {
        float s=(float)sin(2*PI*f*n/FS);
        in[2*n]=(float)left*s; in[2*n+1]=(float)right*s;
    }
    ap_twoway_process(dsp,in,w,t,48000);
    double acc=0;
    for(int n=24000;n<48000;n++) acc+=(double)(w[n]+t[n])*(w[n]+t[n]);
    return sqrt(2*acc/24000);
}

static void test_design(void) {
    ap_biquad bq;
    assert(!ap_biquad_design(NULL,AP_BIQUAD_LOWPASS,FS,1000,0.7,0));
    assert(!ap_biquad_design(&bq,AP_BIQUAD_LOWPASS,FS,30000,0.7,0));
    assert(!ap_biquad_design(&bq,AP_BIQUAD_LOWPASS,FS,1000,0.01,0));
    assert(!ap_biquad_design(&bq,AP_BIQUAD_PEAKING,FS,1000,1,NAN));
    assert(!ap_biquad_design(&bq,(ap_biquad_kind)99,FS,1000,1,0));
    assert(ap_biquad_design(&bq,AP_BIQUAD_PEAKING,FS,66.91,1.1577,6.0));
    assert(fabs(ap_biquad_response_db(&bq,FS,66.91)-6.0)<0.02);
    assert(fabs(ap_biquad_response_db(&bq,FS,5000))<0.01);
}

static void test_lr4_sum(void) {
    ap_twoway dsp; ap_twoway_config c=flat();
    assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    double worst=0;
    for(int k=0;k<=400;k++) {
        double f=200*pow(100.0,k/400.0);
        cpx lp=mul(response(&dsp.woofer[0],f),response(&dsp.woofer[1],f));
        cpx hp=mul(response(&dsp.tweeter[0],f),response(&dsp.tweeter[1],f));
        double e=fabs(mag_db((cpx){lp.re+hp.re,lp.im+hp.im}));
        if(e>worst) worst=e;
    }
    assert(worst<0.01);
    cpx lp=mul(response(&dsp.woofer[0],3000),response(&dsp.woofer[1],3000));
    cpx hp=mul(response(&dsp.tweeter[0],3000),response(&dsp.tweeter[1],3000));
    assert(fabs(mag_db(lp)+6.02)<0.05 && fabs(mag_db(hp)+6.02)<0.05);
    cpx s0=mul(response(&dsp.subsonic[0],45),response(&dsp.subsonic[1],45));
    assert(fabs(mag_db(s0)+3.01)<0.05);
    printf("LR4 acoustic-sum magnitude error 200 Hz..20 kHz: %.4f dB\n",worst);
}

static void test_runtime(void) {
    static ap_twoway dsp; ap_twoway_config c=flat();
    const double freqs[]={200,1000,3000,8000};
    for(int i=0;i<4;i++) {
        assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
        double g=sine_gain(&dsp,freqs[i],1,1);
        assert(fabs(20*log10(g))<0.05);
    }
    c.role=AP_ROLE_LEFT; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    assert(fabs(sine_gain(&dsp,1000,1,0)-1)<0.01);
    assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK && sine_gain(&dsp,1000,0,1)<1e-6);
    c.role=AP_ROLE_RIGHT; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    assert(fabs(sine_gain(&dsp,1000,0,1)-1)<0.01);
    c.role=AP_ROLE_SOLO; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    assert(fabs(sine_gain(&dsp,1000,1,0)-0.5)<0.01);
    c.role=AP_ROLE_FILL; c.trim_db=-6.0206; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    assert(fabs(sine_gain(&dsp,1000,1,1)-0.5)<0.01);

    ap_twoway_config d; ap_twoway_default_config(&d);
    assert(ap_twoway_init(&dsp,&d)==AP_DSP_OK);
    double low=20*log10(sine_gain(&dsp,66.91,1,1)), mid=20*log10(sine_gain(&dsp,1000,1,1));
    assert(fabs(low-mid-5.9)<0.5);
}

static void test_delay_and_faults(void) {
    static ap_twoway dsp; ap_twoway_config c=flat();
    c.delay_samples=480; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    static float in[2*2048], w[2048], t[2048];
    memset(in,0,sizeof(in)); in[0]=in[1]=1;
    ap_twoway_process(&dsp,in,w,t,2048);
    int first=-1;
    for(int n=0;n<2048 && first<0;n++) if(fabsf(w[n])+fabsf(t[n])>1e-9f) first=n;
    assert(first==480);

    assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    for(int n=0;n<2048;n++) { in[2*n]=n%3?NAN:INFINITY; in[2*n+1]=-INFINITY; }
    ap_twoway_process(&dsp,in,w,t,2048);
    for(int n=0;n<2048;n++) assert(w[n]==0 && t[n]==0);

    ap_twoway_config bad;
    bad=c; bad.sample_rate_hz=96000; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_RATE);
    for(int n=0;n<4;n++) { w[n]=t[n]=1; }
    ap_twoway_process(&dsp,in,w,t,4);
    assert(w[0]==0 && t[3]==0);
    bad=c; bad.crossover_hz=800; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_CROSSOVER);
    bad=c; bad.subsonic_hz=10; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_SUBSONIC);
    bad=c; bad.tweeter_pad_db=1; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_PAD);
    bad=c; bad.trim_db=0.5; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_TRIM);
    bad=c; bad.trim_db=NAN; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_TRIM);
    bad=c; bad.delay_samples=AP_DSP_MAX_DELAY_SAMPLES+1; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_DELAY);
    bad=c; bad.role=(ap_role)7; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_ROLE);
    bad=c; bad.eq_count=AP_DSP_MAX_EQ+1; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_EQ);
    bad=c; bad.eq_count=1; bad.eq[0]=(ap_eq_band){70,1,6.5}; assert(ap_twoway_init(&dsp,&bad)==AP_DSP_EQ);
    bad=c; bad.eq_count=2; bad.eq[0]=(ap_eq_band){70,1,5}; bad.eq[1]=(ap_eq_band){72,1,5};
    assert(ap_twoway_init(&dsp,&bad)==AP_DSP_BOOST && !dsp.ready);
    assert(ap_twoway_init(&dsp,NULL)==AP_DSP_ARGUMENT && !dsp.ready);
    assert(ap_twoway_init(NULL,&c)==AP_DSP_ARGUMENT);
}

static ap_room_member member(uint8_t id, ap_role role) {
    ap_room_member m; memset(&m,0,sizeof(m));
    m.uuid[0]=id; m.role=role; m.firmware_major=1;
    return m;
}

static void test_room(void) {
    ap_room_plan p; memset(&p,0,sizeof(p));
    assert(ap_room_validate(NULL)==AP_ROOM_ARGUMENT);
    assert(ap_room_validate(&p)==AP_ROOM_EMPTY);
    p.count=1; p.members[0]=member(1,AP_ROLE_SOLO); assert(ap_room_validate(&p)==AP_ROOM_OK);
    p.members[0].role=AP_ROLE_LEFT; assert(ap_room_validate(&p)==AP_ROOM_LONE_NOT_SOLO);
    p.count=2; p.members[0]=member(1,AP_ROLE_LEFT); p.members[1]=member(2,AP_ROLE_RIGHT);
    assert(ap_room_validate(&p)==AP_ROOM_OK);
    p.members[1].role=AP_ROLE_LEFT; assert(ap_room_validate(&p)==AP_ROOM_PAIR_INCOMPLETE);
    p.members[1].role=AP_ROLE_FILL; assert(ap_room_validate(&p)==AP_ROOM_PAIR_INCOMPLETE);
    p.members[0].role=AP_ROLE_FILL; assert(ap_room_validate(&p)==AP_ROOM_OK);
    p.members[1].role=AP_ROLE_SOLO; assert(ap_room_validate(&p)==AP_ROOM_SOLO_IN_GROUP);
    p.members[1]=member(1,AP_ROLE_FILL); assert(ap_room_validate(&p)==AP_ROOM_DUPLICATE);
    p.members[1]=member(2,AP_ROLE_FILL); p.members[1].firmware_major=2;
    assert(ap_room_validate(&p)==AP_ROOM_FIRMWARE_MISMATCH);
    p.members[1]=member(2,(ap_role)9); assert(ap_room_validate(&p)==AP_ROOM_ROLE);
    p.count=4;
    p.members[0]=member(1,AP_ROLE_LEFT); p.members[1]=member(2,AP_ROLE_RIGHT);
    p.members[2]=member(3,AP_ROLE_FILL); p.members[3]=member(4,AP_ROLE_FILL);
    p.members[3].delay_us=12500; p.members[3].trim_db=-4;
    assert(ap_room_validate(&p)==AP_ROOM_OK);
    p.members[2].role=AP_ROLE_LEFT; assert(ap_room_validate(&p)==AP_ROOM_PAIR_INCOMPLETE);
    p.members[2].role=AP_ROLE_FILL;
    p.members[3].delay_us=AP_ROOM_MAX_DELAY_US+1; assert(ap_room_validate(&p)==AP_ROOM_DELAY);
    p.members[3].delay_us=12500; p.members[3].trim_db=0.1; assert(ap_room_validate(&p)==AP_ROOM_TRIM);
    p.members[3].trim_db=-31; assert(ap_room_validate(&p)==AP_ROOM_TRIM);
    p.members[3].trim_db=-4;
    p.count=AP_ROOM_MAX_MEMBERS+1; assert(ap_room_validate(&p)==AP_ROOM_TOO_MANY);
    p.count=4;

    ap_twoway_config c; ap_twoway_default_config(&c);
    uint8_t me[16]={0}; me[0]=4;
    assert(ap_room_apply(&p,me,&c)==AP_ROOM_OK);
    assert(c.role==AP_ROLE_FILL && c.delay_samples==600 && c.trim_db==-4);
    ap_twoway dsp; assert(ap_twoway_init(&dsp,&c)==AP_DSP_OK);
    me[0]=9; ap_twoway_config before=c;
    assert(ap_room_apply(&p,me,&c)==AP_ROOM_NOT_MEMBER && !memcmp(&before,&c,sizeof(c)));
    p.members[1].role=AP_ROLE_FILL; me[0]=1;
    assert(ap_room_apply(&p,me,&c)==AP_ROOM_PAIR_INCOMPLETE && !memcmp(&before,&c,sizeof(c)));
}

static uint64_t rng=0x9e3779b97f4a7c15ull;
static double uniform(void) {
    rng^=rng<<13; rng^=rng>>7; rng^=rng<<17;
    return (double)(rng>>11)/9007199254740992.0;
}

static void test_clock(void) {
    ap_clock c; ap_clock_init(&c,25);
    int64_t out;
    assert(!ap_clock_add(&c,&(ap_clock_exchange){100,50,40,200}));
    assert(!ap_clock_add(&c,&(ap_clock_exchange){100,50,60,90}));
    assert(!ap_clock_add(&c,&(ap_clock_exchange){0,0,0,AP_CLOCK_MAX_PATH_US+1}));
    assert(!ap_clock_add(&c,&(ap_clock_exchange){0,0,500,100}));
    assert(!ap_clock_to_master(&c,0,&out));

    const double ppm=50e-6, offset=1234567.0;
    double worst=0;
    int64_t local=10000000;
    for(int i=0;i<200;i++) {
        double up=300+1500*pow(uniform(),3), down=300+1500*pow(uniform(),3), hold=80;
        int64_t t1=local;
        double m2=(t1+up)*(1+ppm)+offset;
        int64_t t2=(int64_t)llround(m2), t3=(int64_t)llround(m2+hold);
        int64_t t4=(int64_t)llround(t1+up+hold/(1+ppm)+down);
        assert(ap_clock_add(&c,&(ap_clock_exchange){t1,t2,t3,t4}));
        if(i==(int)AP_CLOCK_MIN_SAMPLES-2) assert(!c.locked && !ap_clock_to_master(&c,t4,&out));
        if(i>=(int)AP_CLOCK_WINDOW) {
            assert(c.locked);
            int64_t probe=t4+250000;
            assert(ap_clock_to_master(&c,probe,&out));
            double e=fabs((double)out-(probe*(1+ppm)+offset));
            if(e>worst) worst=e;
        }
        assert(!ap_clock_add(&c,&(ap_clock_exchange){t1-1,t2,t3,t4}));
        local=t4+1000000;
    }
    assert(worst<25);
    assert(fabs(c.drift-ppm)<5e-6);
    printf("clock: worst master-time error %.1f us at +250 ms, drift %.2f ppm\n",worst,c.drift*1e6);

    ap_clock noisy; ap_clock_init(&noisy,25); local=0;
    for(int i=0;i<(int)AP_CLOCK_WINDOW;i++) {
        double up=300+(i%2?40000:0), down=300+(i%2?0:40000);
        int64_t t1=local, t2=(int64_t)(t1+up), t3=t2+80, t4=(int64_t)(t3+down);
        assert(ap_clock_add(&noisy,&(ap_clock_exchange){t1,t2,t3,t4}));
        local=t4+1000000;
    }
    assert(!noisy.locked);
}

int main(void) {
    test_design();
    test_lr4_sum();
    test_runtime();
    test_delay_and_faults();
    test_room();
    test_clock();
    puts("PASS: biquad design, LR4 sum, role routing, model EQ, delay, fail-closed config, room plan, clock lock");
}
