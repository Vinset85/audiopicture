#include "ap_clock.h"
#include <math.h>
#include <string.h>

void ap_clock_init(ap_clock *c, double lock_us) {
    if(!c) return;
    memset(c,0,sizeof(*c));
    c->lock_us=isfinite(lock_us) && lock_us>0?lock_us:0;
}

static void fit(ap_clock *c) {
    size_t n=c->count, order[AP_CLOCK_WINDOW];
    for(size_t i=0;i<n;i++) order[i]=i;
    for(size_t i=1;i<n;i++)
        for(size_t j=i;j>0 && c->window[order[j]].delay_us<c->window[order[j-1]].delay_us;j--) {
            size_t t=order[j]; order[j]=order[j-1]; order[j-1]=t;
        }
    size_t use=n/8;
    if(use<AP_CLOCK_MIN_FIT) use=n<AP_CLOCK_MIN_FIT?n:AP_CLOCK_MIN_FIT;
    int64_t ref=c->window[(c->next+AP_CLOCK_WINDOW-1)%AP_CLOCK_WINDOW].local_us;
    double sx=0,sy=0,sxx=0,sxy=0;
    for(size_t k=0;k<use;k++) {
        const ap_clock_sample *s=&c->window[order[k]];
        double x=(double)(s->local_us-ref);
        sx+=x; sy+=s->offset_us; sxx+=x*x; sxy+=x*s->offset_us;
    }
    double den=use*sxx-sx*sx, slope=use>1 && fabs(den)>1e-9?(use*sxy-sx*sy)/den:0;
    double intercept=(sy-slope*sx)/use, ss=0;
    for(size_t k=0;k<use;k++) {
        const ap_clock_sample *s=&c->window[order[k]];
        double e=s->offset_us-(intercept+slope*(double)(s->local_us-ref));
        ss+=e*e;
    }
    c->ref_local_us=ref; c->offset_us=intercept; c->drift=slope; c->residual_us=sqrt(ss/use);
    c->locked=n>=AP_CLOCK_MIN_SAMPLES && c->lock_us>0 && c->residual_us<=c->lock_us
        && fabs(slope)*1e6<=AP_CLOCK_MAX_DRIFT_PPM;
}

bool ap_clock_add(ap_clock *c, const ap_clock_exchange *e) {
    if(!c || !e || e->t4<e->t1 || e->t3<e->t2) return false;
    int64_t round_trip=e->t4-e->t1, hold=e->t3-e->t2;
    if(hold>round_trip || round_trip-hold>AP_CLOCK_MAX_PATH_US) return false;
    if(c->count && e->t1<c->window[(c->next+AP_CLOCK_WINDOW-1)%AP_CLOCK_WINDOW].local_us) return false;
    c->window[c->next]=(ap_clock_sample){
        e->t1+round_trip/2,
        ((double)(e->t2-e->t1)+(double)(e->t3-e->t4))/2,
        (double)(round_trip-hold)};
    c->next=(c->next+1)%AP_CLOCK_WINDOW;
    if(c->count<AP_CLOCK_WINDOW) c->count++;
    fit(c);
    return true;
}

bool ap_clock_to_master(const ap_clock *c, int64_t local_us, int64_t *master_us) {
    if(!c || !master_us || !c->locked) return false;
    double dt=(double)(local_us-c->ref_local_us);
    *master_us=local_us+(int64_t)llround(c->offset_us+c->drift*dt);
    return true;
}
