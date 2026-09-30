# AudioPicture V2.2 — vent connectivity execution and exact-shell fluid gate Rev.CP

Status: **REV_CM_EXECUTED_PASS / 22_OF_22_CONNECTIVITY_PASS / THREE_CASE_EXACT_SHELL_BOOLEAN_DEFINED / EXECUTION_REQUIRED / NO_CFD_RESULT**

## Rev.CM actual execution
Rev.CM was executed with CadQuery 2.8 / OpenCASCADE.

Results:
- fluid B-rep valid;
- connected fluid solids = 1;
- vent count = 22;
- all 22 vents intersect internal cavity;
- all 22 vents intersect rear plenum;
- exported connected-fluid STEP.

Therefore the intended frame-aware vent network is topologically connected in the audit model.

This is not a CFD solution.

## Rev.CO exact-shell gate
Rev.CO builds the three CFD geometry cases with a common fluid seed and common obstructions.

Cases:
- CFD0: promoted frame-aware shell, no baffles;
- CFD08: U15 alternating gates, H0.8;
- CFD10: U15 alternating gates, H1.0.

Common:
- same 22 vent capsules;
- same segmented returns;
- same six retention seats;
- same coarse PC-CF frame;
- same MAIN-P/MAIN-C obstruction seeds;
- same internal cavity seed;
- same rear plenum to Z44.

Only labyrinth baffle height/topology state changes as intended.

## Exact boolean method
A continuous air seed spans Z10..44.

For each case subtract:
1. exact reconstructed shell solid for that case;
2. coarse PC-CF frame;
3. MAIN-P;
4. MAIN-C.

A correct result should retain one connected fluid body through the actual shell vent openings.

Rev.CO also probes every vent after subtraction.

## Promotion criteria
For each CFD0/08/10:
- valid B-rep;
- one connected fluid solid;
- shell is one solid;
- all 22 vent probes retain air;
- STEP export succeeds.

Failure in any case blocks CFD meshing promotion.

## Scope limitation
The front/internal cavity boundary remains the Z10 simplification.

The exact DML/exciter bodies and exact final PC-CF frame are still required before final system-temperature release CFD.

Thus passing Rev.CO qualifies a consistent labyrinth-comparison fluid geometry, not the final production thermal digital twin.

## Checks
C1499 Rev.CM actually executed.
C1500 Rev.CM fluid B-rep valid.
C1501 Rev.CM one connected fluid solid.
C1502 all 22 vents touch internal cavity.
C1503 all 22 vents touch rear plenum.
C1504 Rev.CM connected-fluid STEP generated.
C1505 vent topology connectivity passes.
C1506 Rev.CO three-case exact-shell boolean defined.
C1507 common fluid seed Z10..44 defined.
C1508 common frame and board obstructions retained.
C1509 CFD0 no-baffle case defined.
C1510 CFD08 H0.8 case defined.
C1511 CFD10 H1.0 case defined.
C1512 per-vent post-subtraction probes defined.
C1513 one-solid criterion required per case.
C1514 STEP export required per case.
C1515 Z10 front cavity simplification remains open.
C1516 exact DML/exciter/final-frame model remains release gate.
C1517 no CFD result claimed.

Status:
**THERMAL_REV_CP / CM_CONNECTIVITY_PASS / CO_EXACT_SHELL_BOOLEAN_EXECUTION_NEXT / C01_TO_C1517**.
