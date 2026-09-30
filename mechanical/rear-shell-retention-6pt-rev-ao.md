# AudioPicture V2.2 — six-point rear-shell retention topology Rev.AO

Status: **6PT_RETENTION_TOPOLOGY_SCREEN_PASS / TWO_DEDICATED_TOP_PC_CF_TABS_REQUIRED / FASTENER_AND_LOCAL_FEA_OPEN**

## Why the original 8-point seed is not frozen
Executed Rev.AM screening showed that a blind nearest-legal search can force undesirable migrations:
- original T1 seed can move about 55 mm;
- central bottom B2 can move about 21.4 mm because of service/anti-lift competition.

Those migrations are rejected as a design basis.

The original eight-point seed therefore remains historical/parametric, not release geometry.

## Selected six-point topology
Packaging centers:
- TOP_L = (145,383)
- TOP_R = (175,383)
- SIDE_L = (12,200)
- SIDE_R = (308,200)
- BOT_L = (80,17)
- BOT_R = (240,17)

A 5 mm radius packaging envelope was screened around every center.

Result:
zero intersections with the documented vent, service, anti-lift, cleat, MAIN-C and coarse ESP32 RF exclusions used by Rev.AN.

Minimum center-to-center node spacing:
30 mm.

## Structural attachment concept
SIDE_L, SIDE_R, BOT_L and BOT_R:
use legal regions of the existing PC-CF perimeter ring, subject to exact B-rep and final boss/fastener geometry.

TOP_L and TOP_R:
require dedicated local PC-CF tabs extending inward from the top structural ring.

Initial tab seed boxes:
- TAB_TOP_L X139..151 / Y378..390
- TAB_TOP_R X169..181 / Y378..390

The tab seeds screen clear of:
- upper vent banks;
- cleat islands;
- MAIN-C;
- coarse ESP32 RF mask.

They overlap the top-ring Y388..398 region by 2 mm, giving a deliberate fuse path in the next PC-CF B-rep gate.

## Fastener status
No fastener MPN is selected here.

Not frozen:
- screw diameter;
- thread;
- insert type;
- boss OD;
- counterbore/countersink;
- ASA local seat geometry.

The 5 mm radius envelope is only a packaging screen.

## Required next gate
Create the actual PC-CF frame with the two top tabs fused to the existing Rev.C frame, then verify:
1. one connected B-rep;
2. tab-to-ring overlap/fusion;
3. zero hard-keepout intersections;
4. no loss of upper vent opening;
5. no RF-mask intrusion;
6. local load-case readiness for shell retention;
7. mass delta.

Only after that gate should a fastener/insert family be selected.

## Checks
C1076 Rev.AM screen executed.
C1077 undesirable T1 large migration identified.
C1078 undesirable central-bottom migration identified.
C1079 eight-point seed not frozen.
C1080 six-point topology selected.
C1081 TOP_L center 145/383.
C1082 TOP_R center 175/383.
C1083 SIDE_L center 12/200.
C1084 SIDE_R center 308/200.
C1085 BOT_L center 80/17.
C1086 BOT_R center 240/17.
C1087 six node r5 packaging envelopes clear documented exclusions.
C1088 minimum node spacing 30 mm.
C1089 two dedicated top PC-CF tabs required.
C1090 top-left tab seed 139..151/378..390.
C1091 top-right tab seed 169..181/378..390.
C1092 tab seeds clear upper vents.
C1093 tab seeds clear cleat islands.
C1094 tab seeds clear MAIN-C.
C1095 tab seeds clear coarse ESP32 RF mask.
C1096 top tabs deliberately overlap structural top ring for fusion.
C1097 side/bottom nodes use existing perimeter-ring regions.
C1098 fastener MPN remains open.
C1099 5 mm radius is packaging screen, not boss release dimension.
C1100 actual PC-CF tab B-rep and local structural gate required next.

Status:
**REAR_SHELL_RETENTION_REV_AO / SIX_POINTS / 2_TOP_TABS_PLUS_2_SIDE_PLUS_2_BOTTOM / PACKAGING_PASS / PC_CF_BREP_NEXT / C01_TO_C1100**.
