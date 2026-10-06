#include "ap_status.h"
#include <assert.h>
#include <stdio.h>
typedef struct { unsigned calls, fail_at, writes; uint8_t config, polarity, raw; } mock;
static int xfer(void *ctx,uint8_t addr,const uint8_t *tx,size_t nt,uint8_t *rx,size_t nr) {
    mock *m=ctx; assert(addr==0x20 && tx);
    if (++m->calls==m->fail_at) return -1;
    if (nt==2) {
        assert(nr==0 && rx==NULL);
        /* A future accidental output-register write is a test failure. */
        assert((tx[0]==3 && tx[1]==0xff) || (tx[0]==2 && tx[1]==0));
        if(tx[0]==3) m->config=tx[1]; else m->polarity=tx[1];
        m->writes++;
    } else {
        assert(nt==1 && nr==1 && rx);
        switch(tx[0]) {
            case 0: *rx=m->raw; break;
            case 2: *rx=m->polarity; break;
            case 3: *rx=m->config; break;
            default: assert(0);
        }
    }
    return 0;
}
int main(void) {
    mock m={0}; ap_bus b={&m,xfer,NULL}; uint8_t out=0xa5;
    assert(ap_status_configure(NULL)==AP_SENSOR_ARGUMENT);
    assert(ap_status_read(NULL,&out)==AP_SENSOR_ARGUMENT);
    assert(ap_status_read(&b,NULL)==AP_SENSOR_ARGUMENT);
    ap_bus absent={0}; assert(ap_status_configure(&absent)==AP_SENSOR_ARGUMENT);
    assert(ap_status_read(&absent,&out)==AP_SENSOR_ARGUMENT);
    assert(ap_status_configure(&b)==AP_SENSOR_OK && m.writes==2);
    for(unsigned i=0;i<256;i++) {
        m=(mock){.config=0xff,.raw=(uint8_t)i};
        assert(ap_status_read(&b,&out)==AP_SENSOR_OK && out==i && m.writes==0);
    }
    for(unsigned i=0;i<256;i++) {
        m=(mock){.config=(uint8_t)i}; out=0xa5;
        if(i!=255) { assert(ap_status_read(&b,&out)==AP_SENSOR_CONFIG); assert(out==0xa5); }
        m=(mock){.config=0xff,.polarity=(uint8_t)i}; out=0xa5;
        if(i!=0) { assert(ap_status_read(&b,&out)==AP_SENSOR_CONFIG); assert(out==0xa5); }
    }
    for(unsigned i=1;i<=4;i++) {
        m=(mock){.fail_at=i}; assert(ap_status_configure(&b)==AP_SENSOR_IO);
    }
    for(unsigned i=1;i<=3;i++) {
        m=(mock){.config=0xff,.fail_at=i}; out=0xa5;
        assert(ap_status_read(&b,&out)==AP_SENSOR_IO && out==0xa5);
    }
    puts("PASS: 256 raw patterns, 510 invalid register configurations, 7 transport faults, input-only writes; no hardware/source qualification claimed");
}
