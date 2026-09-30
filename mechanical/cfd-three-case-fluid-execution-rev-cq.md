# AudioPicture V2.2 — three-case exact-shell fluid execution Rev.CQ

Status: **CFD0_CFD08_CFD10_EXACT_FLUID_KERNEL_PASS / THREE_CONNECTED_FLUID_DOMAINS / MESHING_CANDIDATES / NO_CFD_SOLUTION**

## Execution
Rev.CO was actually executed with CadQuery 2.8 / OpenCASCADE.

### CFD0 — no labyrinth baffles
- fluid B-rep valid: true;
- connected fluid solids: 1;
- shell solids: 1;
- all 22 vent probes open: true;
- minimum vent-probe air volume: 306.978317 mm3;
- fluid volume: 3,907,713.649424 mm3.

### CFD08 — U15 / H0.8
- fluid B-rep valid: true;
- connected fluid solids: 1;
- shell solids: 1;
- all 22 vent probes open: true;
- minimum vent-probe air volume: 306.978317 mm3;
- fluid volume: 3,907,222.129424 mm3.

### CFD10 — U15 / H1.0
- fluid B-rep valid: true;
- connected fluid solids: 1;
- shell solids: 1;
- all 22 vent probes open: true;
- minimum vent-probe air volume: 306.978317 mm3;
- fluid volume: 3,907,099.249424 mm3.

STEP export succeeded for all three fluid domains during execution.

## Volume deltas
Relative to CFD0:
- CFD08 removes 491.52 mm3 of fluid volume;
- CFD10 removes 614.40 mm3 of fluid volume.

CFD10 relative to CFD08 removes a further 122.88 mm3.

These differences are geometric displacement by the modeled baffles. They are not pressure-loss or airflow results.

## Promotion
The three Rev.CO domains are promoted to **meshing candidates for the controlled labyrinth comparison** because each case satisfies:
- valid fluid B-rep;
- one connected fluid solid;
- one shell solid;
- 22/22 vent probes open;
- successful STEP export.

## Remaining limitations
This promotion is not final production thermal-DMU qualification.

Still open:
- exact DML and exciter obstruction solids;
- exact final PC-CF frame STEP instead of coarse Rev.C abstraction;
- exact PCB/component geometry for local temperature work;
- external D1/D2 room-domain meshing;
- buoyancy solver setup;
- radiation/material assumptions;
- mesh-independence study;
- domain-independence study;
- CFD solution and convergence;
- prototype correlation.

The current front/internal boundary at Z10 remains a simplification.

## Solver order
Recommended first numerical discriminator:
1. CFD0 / CFD08 / CFD10;
2. identical 8 W total heat allocation;
3. 30 C ambient;
4. 4 mm wall gap;
5. identical natural-convection boundary conditions;
6. identical mesh policy.

Only after the first stable comparison should the 5 W, 10 W/35 C and 3/5 mm wall-gap sensitivity cases be expanded.

## Checks
C1518 Rev.CO actually executed with CadQuery/OpenCASCADE.
C1519 CFD0 fluid B-rep valid.
C1520 CFD0 one connected fluid solid.
C1521 CFD0 22/22 vent probes open.
C1522 CFD08 fluid B-rep valid.
C1523 CFD08 one connected fluid solid.
C1524 CFD08 22/22 vent probes open.
C1525 CFD10 fluid B-rep valid.
C1526 CFD10 one connected fluid solid.
C1527 CFD10 22/22 vent probes open.
C1528 all three shell bodies are one solid.
C1529 all three STEP fluid exports succeeded.
C1530 CFD0 fluid volume 3907713.649424mm3.
C1531 CFD08 fluid volume 3907222.129424mm3.
C1532 CFD10 fluid volume 3907099.249424mm3.
C1533 CFD08 geometric fluid displacement vs CFD0 491.52mm3.
C1534 CFD10 geometric fluid displacement vs CFD0 614.40mm3.
C1535 three cases promoted as controlled-comparison meshing candidates.
C1536 first solver discriminator defined as 8W/30C/4mm.
C1537 no airflow, pressure or temperature result claimed.

Status:
**THERMAL_REV_CQ / THREE_CASE_FLUID_KERNEL_PASS / MESHING_CANDIDATES / FIRST_SOLVER_CASE_8W_30C_4MM / C01_TO_C1537**.
