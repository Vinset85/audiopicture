#include "power_governor.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
/* TEST FIXTURE VALUES ONLY: not measured/calibrated production settings. */
static ap_governor_config cfg(void){return (ap_governor_config){
 .voltage_min=20,.voltage_max=25.3,.power_error_w=.2,.power_error_fraction=.02,
 .poe_soft_w=18,.poe_hard_w=21,.poe_emergency_w=22.5,.ext_soft_a=2.7,.ext_hard_a=2.9,
 .attack_db_s=100,.recovery_db_s=3,.max_attenuation_db=60,
 .poe_transition_attenuation_db=20,.monitor_fallback_attenuation_db=40,
 .power_hysteresis_w=1,.current_hysteresis_a=.1,.sample_timeout_ms=20,.stable_dwell_ms=100};}
static ap_governor_input sample(uint32_t now,ap_source s,double p){return (ap_governor_input){
 .source=s,.type2_verified=true,.rail_5v_good=true,.rail_3v3_good=true,.monitor_valid=true,
 .now_ms=now,.sample_time_ms=now,.bus_voltage=24,.bus_current=p/24,.source_power_w=p};}
int main(void){
 ap_governor g;ap_governor_config c=cfg();assert(ap_governor_init(&g,&c));assert(g.amp_pdn_asserted);
 for(uint32_t t=0;t<=21000;t+=5){ap_governor_input i=sample(t,AP_SOURCE_EXT24,10);ap_governor_step(&g,&i);if(t<100)assert(g.amp_pdn_asserted);}
 assert(g.state==AP_EXT_PERFORMANCE&&g.attenuation_db==0&&!g.amp_pdn_asserted);
 ap_governor_input i=sample(21005,AP_SOURCE_POE,10);ap_governor_step(&g,&i);assert(g.amp_pdn_asserted&&g.attenuation_db>=20);
 for(uint32_t t=21010;t<=21110;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}
 assert(!g.amp_pdn_asserted);
 i=sample(21115,AP_SOURCE_POE,22.5);ap_governor_step(&g,&i);assert(g.amp_pdn_asserted&&g.state==AP_DERATE_POWER);
 i=sample(21120,AP_SOURCE_POE,10);i.amp_hard_fault=true;ap_governor_step(&g,&i);assert(g.state==AP_FAULT_LATCH&&g.amp_pdn_asserted);
 for(uint32_t t=21125;t<=21300;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);assert(g.amp_pdn_asserted&&g.state==AP_FAULT_LATCH);}
 i.reset_fault=true;i.now_ms=i.sample_time_ms=21305;ap_governor_step(&g,&i);assert(g.state==AP_RECOVERY&&!g.amp_pdn_asserted);
 i=sample(21310,AP_SOURCE_POE,10);i.monitor_valid=false;ap_governor_step(&g,&i);assert(g.amp_pdn_asserted&&g.measurement_fault);
 c.fallback_calibrated=true;assert(ap_governor_init(&g,&c));i=sample(0,AP_SOURCE_POE,10);i.monitor_valid=false;ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 for(uint32_t t=5;t<=110;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}
 i=sample(115,AP_SOURCE_POE,10);i.monitor_valid=false;ap_governor_step(&g,&i);assert(!g.amp_pdn_asserted&&g.attenuation_db>=40);
 i=sample(5,AP_SOURCE_POE,10);i.type2_verified=false;ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 /* Exhaustive invalid-input combinations, including IEEE NaN/Inf and stale/future timestamps. */
 const double values[]={-1,0,24,NAN,INFINITY};
 for(unsigned k=0;k<5;k++)for(unsigned flags=0;flags<64;flags++){
  assert(ap_governor_init(&g,&c));i=sample(100,AP_SOURCE_POE,10);i.bus_voltage=values[k];
  i.rail_5v_good=flags&1;i.rail_3v3_good=flags&2;i.type2_verified=flags&4;i.monitor_valid=flags&8;
  i.amp_hard_fault=flags&16;i.thermal_critical=flags&32;ap_governor_step(&g,&i);
  if(k!=2||!i.rail_5v_good||!i.rail_3v3_good||!i.type2_verified||i.amp_hard_fault||i.thermal_critical)assert(g.amp_pdn_asserted);
 }
 assert(ap_governor_init(&g,&c));i=sample(10,AP_SOURCE_POE,10);i.sample_time_ms=11;ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 /* Unsigned time wrap remains valid, but cannot bypass stable-source dwell. */
 assert(ap_governor_init(&g,&c));for(uint32_t dt=0;dt<=110;dt+=5){i=sample((UINT32_MAX-50)+dt,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}assert(!g.amp_pdn_asserted);
 c.poe_emergency_w=23;assert(!ap_governor_init(&g,&c));ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 c=cfg();c.attack_db_s=NAN;assert(!ap_governor_init(&g,&c));
 /* Loss of the scheduler/input re-arms the stable-source dwell. */
 c=cfg();assert(ap_governor_init(&g,&c));for(unsigned t=0;t<=110;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}assert(!g.amp_pdn_asserted);
 ap_governor_step(&g,NULL);assert(g.amp_pdn_asserted);
 i=sample(115,AP_SOURCE_POE,10);ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 for(unsigned t=120;t<=220;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}assert(!g.amp_pdn_asserted);
 i=sample(1000,AP_SOURCE_POE,10);ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 /* A calibrated monitor fallback never bypasses a reported over-budget sample. */
 c.fallback_calibrated=true;assert(ap_governor_init(&g,&c));for(unsigned t=0;t<=110;t+=5){i=sample(t,AP_SOURCE_POE,10);ap_governor_step(&g,&i);}
 i=sample(115,AP_SOURCE_POE,23);i.monitor_valid=false;ap_governor_step(&g,&i);assert(g.amp_pdn_asserted);
 c.max_attenuation_db=NAN;assert(!ap_governor_init(&g,&c));assert(isfinite(g.attenuation_db)&&g.amp_pdn_asserted);
 /* Deterministic event sequence tests state invariants while actually exercising enabled output. */
 c=cfg();assert(ap_governor_init(&g,&c));uint32_t rng=0x53024582u;unsigned enabled=0;
 for(uint32_t n=0;n<200000;n++){
  rng=1664525u*rng+1013904223u;unsigned event=(rng>>16)%100;
  i=sample(n*5,AP_SOURCE_POE,10);i.reset_fault=true;
  switch(event){case 0:i.rail_5v_good=false;break;case 1:i.rail_3v3_good=false;break;case 2:i.type2_verified=false;break;case 3:i.monitor_valid=false;break;case 4:i.amp_hard_fault=true;break;case 5:i.thermal_critical=true;break;case 6:i.source=AP_SOURCE_NONE;break;case 7:i.source_power_w=23;i.bus_current=23.0/24;break;case 8:i.sample_time_ms-=100;break;case 9:i.bus_voltage=NAN;break;case 10:i.thermal_warning=true;break;default:break;}
  ap_governor_step(&g,&i);
  assert(isfinite(g.attenuation_db)&&g.attenuation_db>=0&&g.attenuation_db<=c.max_attenuation_db);
  if(event<=9)assert(g.amp_pdn_asserted);
  if(!g.amp_pdn_asserted)enabled++;
 }
 assert(enabled>100);printf("PASS: 200000 deterministic events, %u enabled samples with safety invariants\n",enabled);
 puts("PASS: governor transitions, source loss, 22.5 W boundary, fault latch, stale/invalid monitor, 320 input combinations, timer wrap, config rejection");
}
