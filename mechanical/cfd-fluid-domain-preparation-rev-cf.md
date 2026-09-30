# AudioPicture V2.2 — CFD fluid-domain preparation Rev.CF

Status: **CFD_CANDIDATE_GEOMETRIES_QUALIFIED / FLUID_DOMAIN_SEEDS_DEFINED / SOLVER_RUN_OPEN**

## Rev.CC actual execution
The H0.8 U15 alternating-gate shell was executed with CadQuery 2.8 / OpenCASCADE.

Results:
- valid B-rep: true;
- connected solids: 1;
- baffle count: 8;
- H=0.8 mm;
- upper opening=15 mm;
- lower opening=24 mm;
- nominal under-rib clearance to PC-CF rear plane=2.0 mm;
- PC-CF intersection=0 mm3;
- maximum vent reclosure=0 mm3;
- Zmax=40.0 mm;
- STEP/STL export generated.

H0.8 and H1.0 are now qualified to the same coarse geometric/kernel level.

## CFD cases
CFD-0: Rev.BK/BM, no baffles.
CFD-08: Rev.CC, U15/H0.8.
CFD-10: Rev.BW, U15/H1.0.

## Fluid-domain coordinate convention
Use the existing product coordinates:
- product X 0..320 mm;
- product Y 0..400 mm;
- product Z 0..40 mm;
- rear wall lies beyond product rear at nominal 4 mm wall gap.

The CFD fluid region is a separate volume and shall not be confused with the shell solid.

## External-domain seeds
D1:
- lateral margin 100 mm each side;
- below product 100 mm;
- above product 200 mm;
- front clearance 100 mm;
- rear wall gap 4 mm.

D2:
- lateral margin 160 mm each side;
- below product 160 mm;
- above product 300 mm;
- front clearance 160 mm;
- rear wall gap 4 mm.

D1/D2 are numerical-domain seeds only.

A domain-independence comparison is mandatory before release use.

## Fluid subtraction
The solver fluid volume must subtract every solid body actually represented in the thermal model.

At minimum this includes the rear shell and labyrinth geometry for the selected case.

For system-temperature prediction it must also represent/subtract the appropriate PC-CF frame, DML/exciters, PCB/component abstractions and other major blockage bodies consistently across all three cases.

Do not use a shell-only fluid model to claim final Pi/TPA temperatures.

## Boundary policy
For the natural-convection comparison:
- gravity vector fixed for wall-mounted portrait orientation;
- same ambient temperature;
- same external pressure/far-field treatment;
- same rear wall condition;
- same 4 mm nominal wall gap;
- same radiation model choice;
- same heat loads;
- same material properties;
- same numerical convergence criteria.

## Domain-independence gate
Compare D1 and D2 for at least the baseline CFD-10 or the thermally worst candidate identified by the first run.

If mass flow and key component temperatures remain materially domain-sensitive, enlarge the domain again.

No numerical acceptance percentage is invented before solver behavior is known.

## Mesh gate
Local refinement must resolve:
- 3 mm vent width;
- R1.5 capsule ends;
- 1.2 mm gate thickness;
- 0.8/1.0 mm gate height;
- nominal 2.0/1.8 mm under-rib gaps;
- 4 mm rear wall gap.

Mesh convergence must be demonstrated separately from domain independence.

## Checks
C1422 Rev.CC H0.8 actually executed.
C1423 Rev.CC valid B-rep.
C1424 Rev.CC one connected solid.
C1425 Rev.CC zero PC-CF intersection.
C1426 Rev.CC zero vent reclosure.
C1427 Rev.CC nominal under-rib clearance 2.0mm.
C1428 Rev.CC Zmax 40.0mm.
C1429 H0.8/H1.0 now same-level geometry qualified.
C1430 CFD fluid domain treated separately from solid geometry.
C1431 D1 external-domain seed defined.
C1432 D2 larger external-domain seed defined.
C1433 nominal rear wall gap remains 4mm.
C1434 domain-independence study mandatory.
C1435 solid blockage consistency required across CFD cases.
C1436 shell-only model prohibited for final component-temperature claims.
C1437 mesh convergence separate from domain independence.
C1438 no CFD result claimed.

Status:
**THERMAL_REV_CF / H0P8_H1P0_GEOMETRY_QUALIFIED / CFD_DOMAIN_SEEDS_D1_D2 / SOLVER_OPEN / C01_TO_C1438**.
