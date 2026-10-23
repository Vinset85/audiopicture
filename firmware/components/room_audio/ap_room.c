#include "ap_room.h"
#include <math.h>
#include <string.h>

ap_room_result ap_room_validate(const ap_room_plan *plan) {
    if(!plan) return AP_ROOM_ARGUMENT;
    if(plan->count==0) return AP_ROOM_EMPTY;
    if(plan->count>AP_ROOM_MAX_MEMBERS) return AP_ROOM_TOO_MANY;
    size_t left=0,right=0,solo=0;
    for(size_t i=0;i<plan->count;i++) {
        const ap_room_member *m=&plan->members[i];
        for(size_t j=0;j<i;j++)
            if(!memcmp(m->uuid,plan->members[j].uuid,sizeof(m->uuid))) return AP_ROOM_DUPLICATE;
        switch(m->role) {
        case AP_ROLE_SOLO: solo++; break;
        case AP_ROLE_LEFT: left++; break;
        case AP_ROLE_RIGHT: right++; break;
        case AP_ROLE_FILL: break;
        default: return AP_ROOM_ROLE;
        }
        if(m->firmware_major!=plan->members[0].firmware_major) return AP_ROOM_FIRMWARE_MISMATCH;
        if(m->delay_us>AP_ROOM_MAX_DELAY_US) return AP_ROOM_DELAY;
        if(!isfinite(m->trim_db) || m->trim_db>0 || m->trim_db<AP_ROOM_MIN_TRIM_DB) return AP_ROOM_TRIM;
    }
    if(plan->count==1) return solo==1?AP_ROOM_OK:AP_ROOM_LONE_NOT_SOLO;
    if(solo) return AP_ROOM_SOLO_IN_GROUP;
    if(left!=right || left>1) return AP_ROOM_PAIR_INCOMPLETE;
    return AP_ROOM_OK;
}

ap_room_result ap_room_apply(const ap_room_plan *plan, const uint8_t uuid[16], ap_twoway_config *cfg) {
    if(!uuid || !cfg) return AP_ROOM_ARGUMENT;
    ap_room_result r=ap_room_validate(plan); if(r!=AP_ROOM_OK) return r;
    for(size_t i=0;i<plan->count;i++) {
        const ap_room_member *m=&plan->members[i];
        if(memcmp(m->uuid,uuid,sizeof(m->uuid))) continue;
        double samples=floor(m->delay_us*cfg->sample_rate_hz/1e6+0.5);
        if(!(samples>=0) || samples>AP_DSP_MAX_DELAY_SAMPLES) return AP_ROOM_DELAY;
        cfg->role=m->role;
        cfg->delay_samples=(uint32_t)samples;
        cfg->trim_db=m->trim_db;
        return AP_ROOM_OK;
    }
    return AP_ROOM_NOT_MEMBER;
}
