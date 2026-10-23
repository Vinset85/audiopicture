#ifndef AP_ROOM_H
#define AP_ROOM_H
#include "ap_dsp.h"
/* Rev.D room plan, written by Home Assistant. A lone unit is SOLO. Two units are LEFT+RIGHT
 * or two FILL. Three or more may hold one LEFT+RIGHT pair; every other unit is FILL. */
#define AP_ROOM_MAX_MEMBERS 8u
#define AP_ROOM_MAX_DELAY_US 50000u
#define AP_ROOM_MIN_TRIM_DB (-30.0)
typedef struct {
    uint8_t uuid[16];
    ap_role role;
    uint32_t delay_us;
    double trim_db;
    uint16_t firmware_major;
} ap_room_member;
typedef struct {
    uint32_t group_id;
    size_t count;
    ap_room_member members[AP_ROOM_MAX_MEMBERS];
} ap_room_plan;
typedef enum {
    AP_ROOM_OK, AP_ROOM_ARGUMENT, AP_ROOM_EMPTY, AP_ROOM_TOO_MANY, AP_ROOM_DUPLICATE,
    AP_ROOM_ROLE, AP_ROOM_SOLO_IN_GROUP, AP_ROOM_LONE_NOT_SOLO, AP_ROOM_PAIR_INCOMPLETE,
    AP_ROOM_FIRMWARE_MISMATCH, AP_ROOM_DELAY, AP_ROOM_TRIM, AP_ROOM_NOT_MEMBER
} ap_room_result;
ap_room_result ap_room_validate(const ap_room_plan *);
/* Validates, then writes this unit's role, delay and trim into cfg. cfg is untouched on error. */
ap_room_result ap_room_apply(const ap_room_plan *, const uint8_t uuid[16], ap_twoway_config *cfg);
#endif
