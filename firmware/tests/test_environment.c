#include "ap_environment.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
static void near(double a,double b) { assert(fabs(a-b)<1e-8); }
static void sht_vector(uint16_t t,uint16_t h,uint8_t d[6]) {
    d[0]=(uint8_t)(t>>8); d[1]=(uint8_t)t; d[2]=ap_sht_crc(d);
    d[3]=(uint8_t)(h>>8); d[4]=(uint8_t)h; d[5]=ap_sht_crc(d+3);
}
typedef struct { unsigned calls,delay_ms,fail_at; int never_ready,bad_id,overflow; } fake;
static void delay(void *ctx,unsigned ms) { ((fake*)ctx)->delay_ms+=ms; }
static int transfer(void *ctx,uint8_t addr,const uint8_t *tx,size_t nt,uint8_t *rx,size_t nr) {
    fake *f=ctx;
    if (++f->calls==f->fail_at) return -1;
    if (addr==0x44) {
        if(nt) { assert(nt==1 && (tx[0]==0xfd || tx[0]==0x89) && nr==0); }
        else { assert(nr==6); const uint8_t v[]={0xbe,0xef,0x92,0xbe,0xef,0x92}; memcpy(rx,v,6); }
    } else {
        assert(addr==0x45 || addr==0x40);
        if (!nr) {
            assert(nt==3);
            if(addr==0x45) assert(tx[0]==1 && tx[1]==0xca && tx[2]==0x10);
            else assert((tx[0]==0 && tx[1]==0 && tx[2]==0x10) ||
                        (tx[0]==1 && tx[1]==0x7b && tx[2]==0x68));
            return 0;
        }
        assert(nt==1); memset(rx,0,nr);
        if(tx[0]==0x7e || tx[0]==0x3e) { rx[0]=0x54; rx[1]=f->bad_id?0:0x49; }
        else if(tx[0]==0x7f) { rx[0]=0x30; rx[1]=1; }
        else if(tx[0]==0x3f) { rx[0]=0x22; rx[1]=0x81; }
        else if(addr==0x45 && tx[0]==1) { rx[0]=0xc8|(f->overflow?1:0); rx[1]=f->never_ready?0x10:0x90; }
        else if(addr==0x45 && tx[0]==0) { rx[0]=0x34; rx[1]=0x56; }
        else if(tx[0]==0) { rx[1]=0x10; }
        else if(tx[0]==0x0b) { rx[1]=f->never_ready?0:2; }
        else if(tx[0]==5) { assert(nr==3); rx[0]=0x1e; } /* 24 V */
        else if(tx[0]==4) { assert(nr==3); rx[0]=0x4b; } /* 24 mV at ADCRANGE=1 */
        else if(tx[0]==6) { rx[0]=0x0c; rx[1]=0x80; } /* 25 C */
        else assert(0);
    }
    return 0;
}
int main(void) {
    const uint8_t manufacturer_vector[]={0xbe,0xef};
    assert(ap_sht_crc(manufacturer_vector)==0x92);
    uint8_t data[6]; ap_sht_reading sht={123,456};
    sht_vector(0,0,data); assert(ap_sht_decode(data,&sht)==AP_SENSOR_OK);
    near(sht.temperature_c,-45); near(sht.humidity_percent,0);
    sht_vector(65535,65535,data); assert(ap_sht_decode(data,&sht)==AP_SENSOR_OK);
    near(sht.temperature_c,130); near(sht.humidity_percent,100);
    sht_vector(0xbeef,0xbeef,data);
    for(unsigned bit=0;bit<48;bit++) {
        data[bit/8]^=(uint8_t)(1U<<(bit%8)); sht=(ap_sht_reading){123,456};
        assert(ap_sht_decode(data,&sht)==AP_SENSOR_CRC);
        near(sht.temperature_c,123); near(sht.humidity_percent,456);
        data[bit/8]^=(uint8_t)(1U<<(bit%8));
    }
    /* Independent TI table 8-9 vectors, including equivalent ranges. */
    const uint16_t words[]={0x0001,0x0fff,0x3456,0x789a,0x8800,0x9400,0xa200,0xb100,0xb001,0xbfff};
    const double expected[]={0.01,40.95,88.8,2818.56,5242.88,5242.88,5242.88,5242.88,20.48,83865.6};
    double lux=0;
    for(unsigned i=0;i<10;i++) { assert(ap_opt_decode(words[i],0xc890,&lux)==AP_SENSOR_OK); near(lux,expected[i]); }
    lux=-1; assert(ap_opt_decode(0,0xc810,&lux)==AP_SENSOR_TIMEOUT); near(lux,-1);
    assert(ap_opt_decode(0,0xc990,&lux)==AP_SENSOR_RANGE); near(lux,-1);
    assert(ap_opt_decode(0xc000,0xc890,&lux)==AP_SENSOR_RANGE); near(lux,-1);
    assert(ap_opt_decode(0,0xc894,&lux)==AP_SENSOR_ARGUMENT);
    const uint8_t bus[]={0x1e,0,0}, shunt[]={0x4b,0,0}, die[]={0x0c,0x80};
    ap_ina_reading ina={0};
    assert(ap_ina_decode(bus,shunt,die,0.008,&ina)==AP_SENSOR_OK);
    near(ina.bus_v,24); near(ina.shunt_v,0.024); near(ina.current_a,3);
    near(ina.calculated_power_w,72); near(ina.die_c,25);
    const uint8_t neg[]={0xb5,0,0}, cold[]={0xf3,0x80};
    assert(ap_ina_decode(bus,neg,cold,0.008,&ina)==AP_SENSOR_OK);
    near(ina.current_a,-3); near(ina.calculated_power_w,-72); near(ina.die_c,-25);
    const uint8_t min[]={0x80,0,0}, max[]={0x7f,0xff,0xf0};
    assert(ap_ina_decode(bus,min,die,0.008,&ina)==AP_SENSOR_OK); near(ina.current_a,-5.12);
    assert(ap_ina_decode(bus,max,die,0.008,&ina)==AP_SENSOR_OK); near(ina.current_a,5.119990234375);
    assert(ap_ina_decode(bus,shunt,die,0,&ina)==AP_SENSOR_ARGUMENT);
    assert(ap_ina_decode(bus,shunt,die,NAN,&ina)==AP_SENSOR_ARGUMENT);
    assert(ap_ina_decode(bus,shunt,die,INFINITY,&ina)==AP_SENSOR_ARGUMENT);
    fake f={0}; ap_bus b={&f,transfer,delay}; uint32_t serial=0;
    assert(ap_sht_serial(&b,&serial)==AP_SENSOR_OK); assert(serial==0xbeefbeef);
    f=(fake){0}; assert(ap_sht_measure(&b,&sht)==AP_SENSOR_OK); assert(f.delay_ms==10);
    for(unsigned i=1;i<=2;i++) { f=(fake){.fail_at=i}; assert(ap_sht_measure(&b,&sht)==AP_SENSOR_IO); }
    f=(fake){0}; assert(ap_opt_measure(&b,&lux)==AP_SENSOR_OK); near(lux,88.8); assert(f.calls==5);
    for(unsigned i=1;i<=5;i++) { f=(fake){.fail_at=i}; lux=-1; assert(ap_opt_measure(&b,&lux)==AP_SENSOR_IO); near(lux,-1); }
    f=(fake){.never_ready=1}; assert(ap_opt_measure(&b,&lux)==AP_SENSOR_TIMEOUT); assert(f.delay_ms==2000);
    f=(fake){.bad_id=1}; assert(ap_opt_measure(&b,&lux)==AP_SENSOR_ID);
    f=(fake){.overflow=1}; assert(ap_opt_measure(&b,&lux)==AP_SENSOR_RANGE);
    f=(fake){0}; assert(ap_ina_measure(&b,0x40,0.008,&ina)==AP_SENSOR_OK); assert(f.calls==9); near(ina.current_a,3);
    for(unsigned i=1;i<=9;i++) { f=(fake){.fail_at=i}; ina.bus_v=-1; assert(ap_ina_measure(&b,0x40,0.008,&ina)==AP_SENSOR_IO); near(ina.bus_v,-1); }
    f=(fake){.never_ready=1}; assert(ap_ina_measure(&b,0x40,0.008,&ina)==AP_SENSOR_TIMEOUT); assert(f.delay_ms==25);
    f=(fake){.bad_id=1}; assert(ap_ina_measure(&b,0x40,0.008,&ina)==AP_SENSOR_ID);
    assert(ap_sht_measure(NULL,&sht)==AP_SENSOR_ARGUMENT);
    assert(ap_opt_measure(&b,NULL)==AP_SENSOR_ARGUMENT);
    assert(ap_ina_measure(&b,0x20,0.008,&ina)==AP_SENSOR_ARGUMENT);
    puts("PASS: datasheet vectors, 48 single-bit CRC corruptions, signed ADC endpoints, 16 transport failures, identity, overflow and bounded timeouts");
}
