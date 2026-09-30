# AudioPicture V2.2 — executed frame-aware master promotion Rev.BM

Status: **FRAME_AWARE_MASTER_EXECUTED_PASS / ZERO_COARSE_PC_CF_SHADOW / REV_AD_REV_V_COORDINATES_SUPERSEDED / LABYRINTH_GATE_OPEN**

## Actual CadQuery execution
Rev.BK was executed with CadQuery 2.8 / OpenCASCADE.

Results:
- valid B-rep: true;
- connected solids: 1;
- vent count: 22;
- bounding box: 320 x 400 x 4.4 mm for the shell/return/seat assembly;
- global Z extent: 35.6..40.0 mm;
- maximum seat-to-edge-return overlap: 0 mm3;
- maximum vent reclosure after seat integration: 0 mm3;
- pre-seat volume: 280134.121 mm3;
- final volume: 280982.351 mm3.

Real R1.5 capsule areas:
- inlet: 1416.823 mm2;
- outlet: 1330.686 mm2.

## Post-build projected PC-CF audit
The 22 relocated vents were re-audited at 0.25 mm raster resolution against the documented Rev.C PC-CF projection.

A 1.0 mm cardinal clearance seed was also screened.

Result for every IL/IR/UL/UR slot:
- projected PC-CF overlap = 0;
- 1.0 mm clearance-screen violation = 0.

This is a geometric coarse-mask result, not a manufacturing tolerance or CFD result.

## Promotion
Rev.BK is promoted as the preferred current rear-shell vent master.

The vent coordinates in Rev.AD and Rev.V are superseded for current shell geometry.

Those revisions remain historical evidence for the development path and area derivation.

## Consequence
The prior structural shadowing problem is removed at the coarse projected-geometry level without cutting the PC-CF structural ring.

The acoustic/thermal labyrinth design gate is now open.

The labyrinth must:
- preserve the new vent coordinates;
- avoid reducing the controlling throat below justified limits;
- provide two direction changes where packaging permits;
- avoid DML acoustic short-circuit;
- remain clear of retention seats, frame, electronics, RF/radar and service paths;
- be validated by CFD later.

## Open items
- exact RF/radar masks;
- service connector exact sweep;
- harness swept volumes;
- ASA dimensional/warpage qualification;
- CFD;
- final baffle pressure-loss validation.

## Checks
C1283 Rev.BK actually executed.
C1284 valid B-rep confirmed.
C1285 one connected solid confirmed.
C1286 22 open vents confirmed.
C1287 seat-return overlap zero.
C1288 vent reclosure zero.
C1289 Zmax 40.0 mm.
C1290 inlet real area 1416.823 mm2.
C1291 outlet real area 1330.686 mm2.
C1292 post-build projected-frame audit executed.
C1293 all 22 projected overlaps zero.
C1294 all 22 pass 1.0 mm coarse clearance screen.
C1295 1.0 mm screen not treated as production tolerance.
C1296 Rev.BK promoted.
C1297 Rev.AD/Rev.V vent coordinates superseded.
C1298 PC-CF ring remains uncut.
C1299 labyrinth design gate opened.
C1300 CFD remains authoritative for thermal flow.

Status:
**REAR_SHELL_REV_BM / EXECUTED_ONE_SOLID / 22_FRAME_CLEAR_VENTS / REV_BK_PROMOTED / LABYRINTH_NEXT / C01_TO_C1300**.
