# AudioPicture V2.2 — Rev.CK execution and vent-connected fluid audit Rev.CN

Status: **REV_CK_KERNEL_PASS / BOARD_FRAME_REGISTRATION_PASS / VENT_CONNECTIVITY_MODEL_DEFINED / EXACT_SHELL_SUBTRACTION_AND_EXECUTION_OPEN / NO_CFD_RESULT**

## Rev.CK execution
Rev.CK was executed with CadQuery 2.8 / OpenCASCADE.

Recorded gates:
- internal-air B-rep valid;
- external-air seed valid;
- MAIN-P versus coarse Rev.C frame intersection = 0 mm3;
- MAIN-C versus coarse Rev.C frame intersection = 0 mm3;
- nominal wall plane Z=44 mm;
- nominal wall gap=4 mm;
- STEP exports generated.

Therefore the coarse board/frame registration is internally consistent at this gate.

## Rev.CM
Rev.CM defines the first vent-connected fluid connectivity audit.

It uses the promoted 22 frame-aware vent coordinates:
- 12 lower inlet capsules;
- 10 upper outlet capsules.

Each capsule is extended geometrically from the internal cavity through the rear-shell region into the nominal 4 mm rear wall plenum.

The audit checks:
- every vent channel intersects internal air;
- every vent channel intersects rear plenum;
- the resulting union is a valid B-rep;
- connected-solid count.

## Important limitation
Rev.CM is a topology/connectivity model.

It does not yet subtract the exact Rev.BK/Rev.CC/Rev.BW shell+baffle solid from a common external room volume.

Therefore a one-solid result in Rev.CM would demonstrate geometric connectivity of the intended channels, not final solver-ready fluid-domain correctness.

## Next exact boolean
For each CFD geometry:
- CFD-0 Rev.BK/BM;
- CFD-08 Rev.CC;
- CFD-10 Rev.BW;

construct:
1. common room + rear-wall-gap air volume;
2. exact product internal cavity seed;
3. subtract the corresponding exact shell solid;
4. subtract PC-CF and board obstructions;
5. retain actual 22 vent passages;
6. verify a connected lower-inlet to upper-outlet path;
7. export named fluid volume.

The exact baffle solid must differ only between CFD-08 and CFD-10.

## Checks
C1484 Rev.CK actually executed.
C1485 Rev.CK internal-air B-rep valid.
C1486 Rev.CK external-air seed valid.
C1487 MAIN-P/coarse-frame overlap zero.
C1488 MAIN-C/coarse-frame overlap zero.
C1489 nominal wall plane Z44 confirmed.
C1490 nominal wall gap4 confirmed.
C1491 Rev.CK STEP exports generated.
C1492 coarse board/frame registration passes.
C1493 Rev.CM vent-connected audit defined.
C1494 all 22 promoted vent coordinates used.
C1495 per-vent internal/rear-plenum connectivity check defined.
C1496 exact shell subtraction remains mandatory.
C1497 exact CFD-0/08/10 fluid exports remain open.
C1498 no CFD result claimed.

Status:
**THERMAL_REV_CN / CK_EXECUTED_PASS / CM_CONNECTIVITY_AUDIT / EXACT_THREE_CASE_FLUID_BOOLEAN_NEXT / C01_TO_C1498**.
