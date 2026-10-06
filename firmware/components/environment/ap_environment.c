#include "ap_environment.h"
#include <math.h>
#include <stdbool.h>
static uint16_t be16(const uint8_t *p) { return ((uint16_t)p[0] << 8) | p[1]; }
static uint32_t be24(const uint8_t *p) { return ((uint32_t)p[0]<<16) | ((uint32_t)p[1]<<8) | p[2]; }
static bool valid_bus(const ap_bus *b) { return b && b->transfer && b->delay; }
uint8_t ap_sht_crc(const uint8_t data[2]) {
    uint8_t crc = 0xff;
    for (unsigned i=0; i<2; ++i) {
        crc ^= data[i];
        for (unsigned bit=0; bit<8; ++bit)
            crc = (uint8_t)((crc & 0x80) ? (crc << 1) ^ 0x31 : crc << 1);
    }
    return crc;
}
static ap_sensor_result sht_read(const ap_bus *b, uint8_t cmd, uint8_t data[6]) {
    if (!valid_bus(b)) return AP_SENSOR_ARGUMENT;
    if (b->transfer(b->context, 0x44, &cmd, 1, NULL, 0)) return AP_SENSOR_IO;
    b->delay(b->context, 10); /* high-repeatability max 8.3 ms; no clock stretching */
    if (b->transfer(b->context, 0x44, NULL, 0, data, 6)) return AP_SENSOR_IO;
    if (ap_sht_crc(data)!=data[2] || ap_sht_crc(data+3)!=data[5]) return AP_SENSOR_CRC;
    return AP_SENSOR_OK;
}
ap_sensor_result ap_sht_decode(const uint8_t data[6], ap_sht_reading *out) {
    if (!data || !out) return AP_SENSOR_ARGUMENT;
    if (ap_sht_crc(data)!=data[2] || ap_sht_crc(data+3)!=data[5]) return AP_SENSOR_CRC;
    ap_sht_reading r={-45.0+175.0*be16(data)/65535.0, -6.0+125.0*be16(data+3)/65535.0};
    r.humidity_percent=fmax(0.0, fmin(100.0, r.humidity_percent));
    *out=r; return AP_SENSOR_OK;
}
ap_sensor_result ap_sht_measure(const ap_bus *b, ap_sht_reading *out) {
    if (!out) return AP_SENSOR_ARGUMENT;
    uint8_t data[6]; ap_sensor_result r=sht_read(b, 0xfd, data);
    return r == AP_SENSOR_OK ? ap_sht_decode(data, out) : r;
}
ap_sensor_result ap_sht_serial(const ap_bus *b, uint32_t *out) {
    if (!out) return AP_SENSOR_ARGUMENT;
    uint8_t data[6]; ap_sensor_result r=sht_read(b, 0x89, data);
    if (r == AP_SENSOR_OK) *out=((uint32_t)be16(data)<<16)|be16(data+3);
    return r;
}
static int read_reg(const ap_bus *b, uint8_t addr, uint8_t reg, uint8_t *data, size_t n) {
    return b->transfer(b->context, addr, &reg, 1, data, n);
}
static int write16(const ap_bus *b, uint8_t addr, uint8_t reg, uint16_t value) {
    const uint8_t data[]={reg, (uint8_t)(value>>8), (uint8_t)value};
    return b->transfer(b->context, addr, data, 3, NULL, 0);
}
ap_sensor_result ap_opt_decode(uint16_t result, uint16_t config, double *lux) {
    if (!lux) return AP_SENSOR_ARGUMENT;
    if (!(config & 0x80)) return AP_SENSOR_TIMEOUT;
    if ((config & 0x100) || (result>>12)>11) return AP_SENSOR_RANGE;
    /* ME=0 is required, otherwise the exponent is masked. */
    if (config & 0x04) return AP_SENSOR_ARGUMENT;
    *lux=0.01*(1U<<(result>>12))*(result&0xfff); return AP_SENSOR_OK;
}
ap_sensor_result ap_opt_measure(const ap_bus *b, double *lux) {
    if (!valid_bus(b) || !lux) return AP_SENSOR_ARGUMENT;
    uint8_t data[2];
    if (read_reg(b,0x45,0x7e,data,2)) return AP_SENSOR_IO;
    if (be16(data)!=0x5449) return AP_SENSOR_ID;
    if (read_reg(b,0x45,0x7f,data,2)) return AP_SENSOR_IO;
    if (be16(data)!=0x3001) return AP_SENSOR_ID;
    /* Automatic range, 800-ms single shot, exponent unmasked. */
    if (write16(b,0x45,1,0xca10)) return AP_SENSOR_IO;
    for (unsigned i=0; i<100; ++i) {
        b->delay(b->context,20);
        if (read_reg(b,0x45,1,data,2)) return AP_SENSOR_IO;
        uint16_t cfg=be16(data);
        if (!(cfg&0x80)) continue;
        if (read_reg(b,0x45,0,data,2)) return AP_SENSOR_IO;
        return ap_opt_decode(be16(data),cfg,lux);
    }
    return AP_SENSOR_TIMEOUT;
}
ap_sensor_result ap_ina_decode(const uint8_t bus[3], const uint8_t shunt[3],
    const uint8_t die[2], double shunt_ohm, ap_ina_reading *out) {
    if (!bus || !shunt || !die || !out || !isfinite(shunt_ohm) || shunt_ohm<=0.0)
        return AP_SENSOR_ARGUMENT;
    uint32_t raw=be24(shunt)>>4;
    int32_t signed_shunt=(int32_t)raw-((raw&0x80000)?0x100000:0);
    int32_t td=(int32_t)be16(die)-((be16(die)&0x8000)?0x10000:0);
    ap_ina_reading r={0};
    r.bus_v=(be24(bus)>>4)*0.0001953125;
    r.shunt_v=signed_shunt*0.000000078125;
    r.die_c=td*0.0078125;
    r.current_a=r.shunt_v/shunt_ohm;
    r.calculated_power_w=r.bus_v*r.current_a;
    if (r.bus_v>85.0 || !isfinite(r.current_a) || !isfinite(r.calculated_power_w))
        return AP_SENSOR_RANGE;
    *out=r; return AP_SENSOR_OK;
}
ap_sensor_result ap_ina_measure(const ap_bus *b, uint8_t addr, double shunt_ohm,
                               ap_ina_reading *out) {
    if (!valid_bus(b) || !out || addr<0x40 || addr>0x4f ||
        !isfinite(shunt_ohm) || shunt_ohm<=0) return AP_SENSOR_ARGUMENT;
    uint8_t data[2], bus[3], shunt[3], die[2];
    if (read_reg(b,addr,0x3e,data,2)) return AP_SENSOR_IO;
    if (be16(data)!=0x5449) return AP_SENSOR_ID;
    if (read_reg(b,addr,0x3f,data,2)) return AP_SENSOR_IO;
    if ((be16(data)>>4)!=0x228) return AP_SENSOR_ID;
    if (write16(b,addr,0,0x0010)) return AP_SENSOR_IO; /* ADCRANGE=1, temp comp off */
    if (read_reg(b,addr,0,data,2)) return AP_SENSOR_IO;
    if (be16(data)!=0x0010) return AP_SENSOR_IO;
    /* Triggered Vbus/Vshunt/T, 1052 us each, no averaging; coherent frozen result. */
    if (write16(b,addr,1,0x7b68)) return AP_SENSOR_IO;
    for (unsigned i=0; i<25; ++i) {
        b->delay(b->context,1);
        if (read_reg(b,addr,0x0b,data,2)) return AP_SENSOR_IO;
        if (!(be16(data)&2)) continue;
        if (read_reg(b,addr,5,bus,3) || read_reg(b,addr,4,shunt,3) || read_reg(b,addr,6,die,2))
            return AP_SENSOR_IO;
        return ap_ina_decode(bus,shunt,die,shunt_ohm,out);
    }
    return AP_SENSOR_TIMEOUT;
}
