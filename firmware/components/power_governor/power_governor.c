#include "power_governor.h"
#include <math.h>
#include <string.h>
static double maxd(double a,double b){return a>b?a:b;}
static double mind(double a,double b){return a<b?a:b;}
static bool finite_config(const ap_governor_config *c){
 const double v[]={c->voltage_min,c->voltage_max,c->power_error_w,c->power_error_fraction,
 c->poe_soft_w,c->poe_hard_w,c->poe_emergency_w,c->ext_soft_a,c->ext_hard_a,
 c->attack_db_s,c->recovery_db_s,c->max_attenuation_db,c->poe_transition_attenuation_db,
 c->monitor_fallback_attenuation_db,c->power_hysteresis_w,c->current_hysteresis_a};
 for(unsigned i=0;i<sizeof(v)/sizeof(v[0]);++i)if(!isfinite(v[i])||v[i]<0)return false;
 return true;
}
bool ap_governor_init(ap_governor *g,const ap_governor_config *c){
 if(!g)return false;
 memset(g,0,sizeof(*g));g->amp_pdn_asserted=true;g->state=AP_BOOT_SAFE;
 if(!c)return false;
 g->cfg=*c;
 g->config_valid=finite_config(c)&&c->voltage_min>0&&c->voltage_max>c->voltage_min
 &&c->poe_soft_w<c->poe_hard_w&&c->poe_hard_w<c->poe_emergency_w
 &&c->poe_emergency_w<=22.5 /* authoritative application continuous budget */
 &&c->power_error_fraction<1&&c->power_error_w<c->poe_soft_w
 &&c->ext_soft_a<c->ext_hard_a&&c->ext_hard_a<3.0
 &&c->attack_db_s>0&&c->recovery_db_s>0&&c->max_attenuation_db>0
 &&c->poe_transition_attenuation_db<=c->max_attenuation_db
 &&c->monitor_fallback_attenuation_db<=c->max_attenuation_db
 &&c->power_hysteresis_w<c->poe_soft_w&&c->current_hysteresis_a<c->ext_soft_a
 &&c->sample_timeout_ms>0&&c->sample_timeout_ms<0x80000000u
 &&c->stable_dwell_ms>0&&c->stable_dwell_ms<0x80000000u;
 if(g->config_valid)g->attenuation_db=c->max_attenuation_db;
 return g->config_valid;
}
void ap_governor_step(ap_governor *g,const ap_governor_input *i){
 if(!g)return;
 if(!i){g->amp_pdn_asserted=true;g->stable_tracking=false;g->measurement_fault=true;return;}
 bool was_running=!g->amp_pdn_asserted&&g->stable_tracking;
 g->amp_pdn_asserted=true;
 if(!g->config_valid)return;
 const ap_governor_config *c=&g->cfg;
 uint32_t elapsed=g->initialized?(uint32_t)(i->now_ms-g->last_ms):0;
 g->last_ms=i->now_ms;g->initialized=true;
 /* A clock reversal/long scheduler stall must not create a gain step. */
 double dt=elapsed<=c->sample_timeout_ms?elapsed/1000.0:0;
 if(elapsed>c->sample_timeout_ms){g->stable_tracking=false;was_running=false;}
 bool source_ok=i->source==AP_SOURCE_EXT24||(i->source==AP_SOURCE_POE&&i->type2_verified);
 bool rails_ok=i->rail_5v_good&&i->rail_3v3_good;
 bool changed=i->source!=g->source;
 if(changed){
  g->source=i->source;g->stable_tracking=false;
  g->attenuation_db=maxd(g->attenuation_db,c->poe_transition_attenuation_db);
  g->power_limited=false;
 }
 bool values=isfinite(i->bus_voltage)&&isfinite(i->bus_current)&&isfinite(i->source_power_w)
   &&i->bus_current>=0&&i->source_power_w>=0;
 bool voltage_ok=values&&i->bus_voltage>=c->voltage_min&&i->bus_voltage<=c->voltage_max;
 bool fresh=(uint32_t)(i->now_ms-i->sample_time_ms)<=c->sample_timeout_ms;
 bool consistent=values&&fabs(i->bus_voltage*i->bus_current-i->source_power_w)
   <=c->power_error_w+c->power_error_fraction*fabs(i->source_power_w);
 bool measurement=i->monitor_valid&&fresh&&voltage_ok&&consistent;
 g->measurement_fault=!measurement;
 if(i->amp_hard_fault||i->thermal_critical){g->state=AP_FAULT_LATCH;g->stable_tracking=false;}
 if(!source_ok||!rails_ok||!measurement){
  g->stable_tracking=false;
  /* Verified fallback is restricted to monitor loss with still-valid rail/voltage evidence. */
  bool fallback=!i->monitor_valid&&fresh&&voltage_ok&&consistent&&source_ok&&rails_ok
    &&c->fallback_calibrated&&was_running&&!changed&&g->state!=AP_FAULT_LATCH
    &&!i->thermal_warning
    &&(i->source==AP_SOURCE_POE?i->source_power_w<c->poe_emergency_w:i->bus_current<c->ext_hard_a);
  if(fallback){g->attenuation_db=maxd(g->attenuation_db,c->monitor_fallback_attenuation_db);
   g->state=AP_DERATE_POWER;g->amp_pdn_asserted=false;}
  else if(g->state!=AP_FAULT_LATCH)g->state=AP_BOOT_SAFE;
  return;
 }
 if(!g->stable_tracking){g->stable_since_ms=i->now_ms;g->stable_tracking=true;}
 bool stable=(uint32_t)(i->now_ms-g->stable_since_ms)>=c->stable_dwell_ms;
 if(g->state==AP_FAULT_LATCH){
  if(!(i->reset_fault&&stable&&!i->amp_hard_fault&&!i->thermal_critical))return;
  g->attenuation_db=c->max_attenuation_db;g->state=AP_RECOVERY;
 }
 if(!stable){g->state=AP_RECOVERY;return;}
 bool poe=i->source==AP_SOURCE_POE;
 bool emergency=poe?i->source_power_w>=c->poe_emergency_w:i->bus_current>=c->ext_hard_a;
 bool hard=poe&&i->source_power_w>=c->poe_hard_w;
 bool excess=poe?i->source_power_w>=c->poe_soft_w:i->bus_current>=c->ext_soft_a;
 bool below=poe?i->source_power_w<c->poe_soft_w-c->power_hysteresis_w
                  :i->bus_current<c->ext_soft_a-c->current_hysteresis_a;
 if(emergency){g->attenuation_db=c->max_attenuation_db;g->power_limited=true;
  g->state=AP_DERATE_POWER;return;}
 if(hard)g->attenuation_db=maxd(g->attenuation_db,c->poe_transition_attenuation_db);
 if(excess||i->thermal_warning){
  g->power_limited=excess;g->attenuation_db=mind(c->max_attenuation_db,g->attenuation_db+c->attack_db_s*dt);
  g->state=i->thermal_warning?AP_DERATE_THERMAL:AP_DERATE_POWER;
 }else if(below){
  g->power_limited=false;g->attenuation_db=maxd(0,g->attenuation_db-c->recovery_db_s*dt);
  g->state=g->attenuation_db>0?AP_RECOVERY:(poe?AP_POE_ECO:AP_EXT_PERFORMANCE);
 }else if(g->power_limited){g->state=AP_DERATE_POWER;}
 g->amp_pdn_asserted=false;
}
