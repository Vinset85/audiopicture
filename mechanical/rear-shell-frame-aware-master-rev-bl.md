# AudioPicture V2.2 — frame-aware rear-shell master gate Rev.BL

Status: **FRAME_AWARE_MASTER_SOURCE_FROZEN / 22_RELOCATED_VENTS / SEGMENTED_RETURNS / SIX_SEATS / EXECUTION_AND_SHADOW_AUDIT_REQUIRED**

## Master definition
Rev.BK replaces the vent coordinates in the prior rear-shell master while retaining:
- 320 x 400 x 2.2 mm rear panel;
- global rear shell Z37.8..40;
- segmented ASA edge returns Z35.6..37.8;
- six D10 x 1.8 mm ASA retention seats;
- 22 real R1.5 capsule vents.

## Relocated inlet
12 vertical 3 x 40 R1.5 slots.

Left:
X17..20 and X24..27 at:
- Y14..54
- Y62..102
- Y110..150

Right is mirrored about X160.

## Relocated outlet
10 horizontal 3 x 45 R1.5 slots.

Left:
X17..62 at:
- Y315..318
- Y322..325
- Y329..332
- Y336..339
- Y343..346

Right:
X258..303 at the same Y levels.

## Area preservation
Real capsule area targets remain:
- inlet 1416.823 mm2;
- outlet 1330.686 mm2.

No area is credited from the service opening.

## Required executable gate
Rev.BK shall only supersede the prior vent master after actual CadQuery execution confirms:
- valid B-rep;
- one connected solid;
- 22 open vents;
- zero seat-to-return overlap;
- zero vent reclosure;
- product Z <= 40 mm;
- STEP and STL export.

A post-build projected PC-CF audit shall also confirm no reintroduced shadowing at the agreed coarse clearance basis.

## Supersession rule
Rev.AD / Rev.V remain historical geometry references until both executable conditions above pass.

After pass:
- Rev.BK becomes the preferred rear-shell vent master;
- Rev.AD / Rev.V are superseded for current shell coordinates;
- acoustic labyrinth design may begin.

## Open items
- service connector opening exact sweep;
- exact RF/radar release;
- cable/harness swept volumes;
- ASA process qualification;
- CFD;
- final labyrinth geometry.

## Checks
C1271 frame-aware full-shell source created.
C1272 22 relocated real capsule vents integrated.
C1273 segmented edge returns retained.
C1274 six ASA retention seats retained.
C1275 global Z map retained.
C1276 inlet real area target retained.
C1277 outlet real area target retained.
C1278 service opening not credited.
C1279 executable B-rep gate mandatory.
C1280 post-build projected-frame audit mandatory.
C1281 old vent coordinates not yet superseded until execution.
C1282 labyrinth remains gated on executable pass.

Status:
**REAR_SHELL_REV_BL / FRAME_AWARE_MASTER_SOURCE / EXECUTION_GATE_PENDING / C01_TO_C1282**.
