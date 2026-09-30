# AudioPicture V2.2 — simplified CFD solid/fluid CAD Rev.CL

Status: **CFD_SOLID_OBSTRUCTION_PREPROCESSOR_DEFINED / INTERNAL_AIR_SEED_DEFINED / VENT_CONNECTED_UNIFIED_FLUID_BOOLEAN_OPEN / NO_CFD_RESULT**

## Purpose
Create a solver-oriented CAD preprocessor without claiming a thermal solution.

Rev.CK defines:
- coarse internal-air seed;
- coarse Rev.C PC-CF obstruction;
- MAIN-P obstruction/source seed;
- MAIN-C obstruction/source seed;
- D1 external-air seed and nominal wall plane.

## Coordinate authority
Product:
- X=0..320 mm;
- Y=0..400 mm;
- Z=0..40 mm.

MAIN-P coarse CFD board:
- X=105..220;
- Y=112..157;
- Z=18.0..19.6.

MAIN-C coarse CFD board:
- X=85..235;
- Y=315..370;
- Z=17.0..18.6.

The PCB Z bands follow the reconciled master global Z map.

## PC-CF
Use the current coarse Rev.C structural-frame boolean as an obstruction for the first solver-preparation model.

This is not a substitute for the exact final frame STEP.

## Internal-air seed
Rev.CK uses Z=10..37.8 as a deliberately simplified internal cavity seed.

Z=10 is not asserted to be the physical DML/front air boundary. The exact front/DML/exciter obstruction geometry must replace this seed before final component-temperature CFD.

The purpose of this first body is to test boolean robustness and source/obstruction registration.

## External domain
D1 seed:
- X=-100..420;
- Y=-100..600;
- front extent to Z=-100;
- wall plane at Z=44;
- nominal product-to-wall gap=4 mm.

D1 remains subject to the D1/D2 domain-independence gate.

## Required execution gates
Rev.CK must be actually executed before promotion.

Record:
- internal-air B-rep validity;
- number of internal-air solids;
- frame/MAIN-P overlap;
- frame/MAIN-C overlap;
- external-air validity;
- STEP export.

Any board/frame overlap is a geometry-model inconsistency and must be reconciled rather than ignored.

## Critical open boolean
The external domain in Rev.CK subtracts a coarse product bounding block.

Therefore it intentionally does not yet create a single vent-connected fluid body through the 22 real shell openings.

Next gate:
1. import/use the promoted shell vent geometry;
2. create the real interior/exterior air union through all vent capsules;
3. include the 4 mm rear wall gap;
4. verify inlet-to-outlet fluid connectivity;
5. label lower inlet and upper outlet faces for solver boundary reporting.

Do not claim a CFD-ready unified fluid domain until that boolean is executed.

## Heat sources
Rev.CJ source allocations apply:
- 5 W: MAIN-P 3.5 / MAIN-C 1.5 W;
- 8 W: MAIN-P 6.0 / MAIN-C 2.0 W;
- 10 W: MAIN-P 8.0 / MAIN-C 2.0 W.

These remain board-level model allocations.

## Checks
C1471 solver-oriented CAD preprocessor Rev.CK defined.
C1472 product coordinate system retained.
C1473 MAIN-P coarse CFD obstruction registered.
C1474 MAIN-C coarse CFD obstruction registered.
C1475 master board Z bands used.
C1476 coarse Rev.C PC-CF obstruction included.
C1477 internal-air Z10 boundary explicitly classified as simplification.
C1478 D1 external-domain geometry encoded.
C1479 wall plane Z44 / nominal gap4 encoded.
C1480 external product bounding-block subtraction is not vent connectivity.
C1481 real 22-vent unified fluid boolean remains mandatory.
C1482 inlet/outlet face labeling remains mandatory.
C1483 no CFD result claimed.

Status:
**THERMAL_REV_CL / CFD_PREPROCESSOR_REV_CK / EXECUTION_NEXT / UNIFIED_FLUID_BOOLEAN_OPEN / C01_TO_C1483**.
