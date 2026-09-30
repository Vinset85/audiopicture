# AudioPicture V2.2 — U15 H1.0 executed baseline and height sweep Rev.BZ

Status: **U15_H1P0_EXECUTED_PASS / EXACT_COORDINATE_LOS_PASS / XY_TOPOLOGY_BASELINE / HEIGHT_SWEEP_ACTIVE**

## Rev.BW execution
Rev.BW was executed with CadQuery 2.8 / OpenCASCADE.

Results:
- valid B-rep;
- one connected ASA shell solid;
- eight alternating-gate baffles;
- H = 1.0 mm;
- upper end opening = 15 mm;
- lower end opening = 24 mm;
- zero nominal Rev.C PC-CF intersection;
- zero vent reclosure;
- nominal under-rib clearance to frame plane = 1.8 mm;
- product Zmax = 40.0 mm;
- STEP/STL export generated.

## Exact-coordinate LOS recheck
The Rev.BW gate rectangles were rechecked using the same exact U15 coordinates.

Sampled straight source-to-cavity paths:
- lower left: 0;
- upper left: 0;
- right side is mirrored.

Therefore the XY alternating-gate topology is accepted as the current baseline.

This does not prove acoustic attenuation or thermal flow.

## Height sweep
With XY topology fixed, Rev.BY evaluates H:
- 0.8 mm;
- 1.0 mm;
- 1.2 mm;
- 1.4 mm.

Nominal shell/frame gap remains 2.8 mm.

Nominal under-rib bypass:
- H0.8 -> 2.0 mm;
- H1.0 -> 1.8 mm;
- H1.2 -> 1.6 mm;
- H1.4 -> 1.4 mm.

A separate engineering gap sensitivity of 2.0 / 2.4 / 2.8 / 3.2 mm is recorded only to show robustness. It is not a manufacturing tolerance declaration.

## Current decision
Do not freeze H yet.

H=1.0 is the executed baseline because it has already passed the kernel and LOS gates.

Selection of production H requires:
- measured shell/frame gap and warpage evidence;
- minimum acceptable no-contact margin;
- CFD pressure-loss/natural-convection comparison;
- acoustic vent-radiation prototype test.

## Checks
C1373 Rev.BW actually executed.
C1374 one connected solid confirmed.
C1375 eight alternating gates confirmed.
C1376 zero PC-CF nominal intersection.
C1377 zero vent reclosure.
C1378 nominal under-rib clearance 1.8mm at H1.0.
C1379 Zmax 40.0mm.
C1380 STEP/STL generated.
C1381 exact U15 coordinate LOS rechecked.
C1382 lower sampled straight paths zero.
C1383 upper sampled straight paths zero.
C1384 XY topology accepted as current baseline.
C1385 acoustic attenuation not proven.
C1386 thermal flow not proven.
C1387 Rev.BY height sweep 0.8..1.4 defined.
C1388 engineering gap sensitivity 2.0..3.2 defined.
C1389 gap sensitivity is not production tolerance.
C1390 H1.0 retained as executed baseline only.
C1391 production H remains open pending physical/CFD/acoustic evidence.

Status:
**LABYRINTH_REV_BZ / U15_XY_BASELINE / H1P0_EXECUTED / HEIGHT_SWEEP_ACTIVE / C01_TO_C1391**.
