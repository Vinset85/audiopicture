# AudioPicture V2.2 — ASA shell retention seats Rev.AS

Status: **SIX_LOCAL_ASA_SEATS_PACKAGING_PASS / NO_HOLES / NO_CLAMP_STACK_CLAIM / MASTER_INTEGRATION_NEXT**

## Purpose
Provide local shell-side reinforcement at the six Rev.AO retention nodes without prematurely selecting a screw or threaded insert.

## Executed Rev.AR seed
Six circular ASA seats:
- diameter: 10 mm seed;
- inward protrusion from shell inner plane: 1.8 mm seed;
- global Z: 36.0..37.8 mm.

Centers:
- TOP_L (145,383)
- TOP_R (175,383)
- SIDE_L (12,200)
- SIDE_R (308,200)
- BOT_L (80,17)
- BOT_R (240,17)

## Result
- valid B-rep: PASS;
- one connected panel+seat solid;
- six seats;
- vent intersections: zero;
- service-region intersection: zero;
- conservative anti-lift intersection: zero;
- rear product limit Z40 preserved;
- added ASA volume approximately 848.2 mm3.

With the coarse PC-CF frame ending at Z35:
seat front Z36 leaves a nominal 1.0 mm separation.

That 1.0 mm is a packaging seed only.
It is not a released manufacturing tolerance and is not the final clamped stack.

## Design intent
The seat creates local reinforcement/land for the future removable fastener interface.

It does not yet define:
- hole diameter;
- counterbore/countersink;
- screw head;
- washer;
- insert;
- compression limiter;
- compliant washer;
- clamp preload.

Broad hard contact between shell and PC-CF remains undesirable.

## Next gate
Fuse the six seats into the Rev.AJ vent+segmented-edge master and verify:
- one solid;
- all 22 vents unchanged;
- no service/anti-lift collision;
- no unintended seat/edge-return bridge that broadens shell/frame contact;
- Z<=40.

Only then proceed to fastener family selection.

## Checks
C1119 six ASA seat seed defined.
C1120 seat diameter 10 mm seed.
C1121 seat protrusion 1.8 mm seed.
C1122 seat Z36.0..37.8.
C1123 six seats fused to panel kernel.
C1124 B-rep valid.
C1125 one connected solid.
C1126 vent intersections zero.
C1127 service intersection zero.
C1128 anti-lift intersection zero.
C1129 added ASA volume ~848.2 mm3.
C1130 nominal coarse PC-CF separation 1.0 mm.
C1131 1.0 mm explicitly not production tolerance.
C1132 no fastener hole frozen.
C1133 no insert frozen.
C1134 no preload/compression stack claimed.
C1135 full master integration required next.

Status:
**ASA_RETENTION_SEATS_REV_AS / 6X_D10_H1P8_SEED / Z36_TO37P8 / PACKAGING_PASS / FULL_MASTER_NEXT / C01_TO_C1135**.
