#include "ap_status.h"
static ap_sensor_result check_registers(const ap_bus *b) {
    const uint8_t regs[2]={3,2}, expected[2]={0xff,0};
    for (unsigned i=0;i<2;i++) {
        uint8_t value=0;
        if (b->transfer(b->context,0x20,&regs[i],1,&value,1)) return AP_SENSOR_IO;
        if (value!=expected[i]) return AP_SENSOR_CONFIG;
    }
    return AP_SENSOR_OK;
}
ap_sensor_result ap_status_configure(const ap_bus *b) {
    if (!b || !b->transfer) return AP_SENSOR_ARGUMENT;
    /* First make every pin an input; never write the output-port register. */
    const uint8_t writes[2][2]={{3,0xff},{2,0}};
    for (unsigned i=0;i<2;i++)
        if (b->transfer(b->context,0x20,writes[i],2,NULL,0)) return AP_SENSOR_IO;
    return check_registers(b);
}
ap_sensor_result ap_status_read(const ap_bus *b,uint8_t *raw) {
    if (!b || !b->transfer || !raw) return AP_SENSOR_ARGUMENT;
    ap_sensor_result r=check_registers(b);
    if (r!=AP_SENSOR_OK) return r;
    const uint8_t reg=0; uint8_t value;
    if (b->transfer(b->context,0x20,&reg,1,&value,1)) return AP_SENSOR_IO;
    *raw=value;
    return AP_SENSOR_OK;
}
