# AudioPicture V2.2 — complete ventilated rear-shell kernel Rev.AF

Status: **22_VENT_KERNEL_EXECUTED_PASS / NOMINAL_VENTILATED_MASTER / SERVICE_RETENTION_BAFFLES_OPEN**

## Executed CAD
Source: mechanical/cad/generate_rear_shell_ventilated_rev_ae.py

The combined rear-panel kernel was executed with CadQuery/OpenCASCADE after integrating the executed upper Rev.V/Z layout and lower Rev.AD layout.

## Kernel result
- external XY: 320 x 400 mm
- thickness: 2.2 mm
- global Z: 37.8..40.0 mm
- connected solids: 1
- valid B-rep: PASS
- total vents: 22
- upper outlets: 10
- lower inlets: 12
- all vents use real R1.5 capsule ends
- upper minimum nominal web: 4.0 mm
- lower minimum nominal web: 4.0 mm
- all documented gate-obstacle intersections: 0 mm3

## Real geometric opening
Upper:
- 1330.6858 mm2 gross
- 1064.5487 mm2 preliminary effective seed at 0.80
- preferred seed threshold 1000 mm2: PASS

Lower:
- 1416.8230 mm2 gross
- 1062.6173 mm2 preliminary effective seed at 0.75
- preferred seed threshold 900 mm2: PASS

Total real geometric vent opening:
2747.5088 mm2.

The 0.80/0.75 factors remain reduced-order CAD sizing assumptions, not CFD results.

## Volume consistency
Nominal solid plate:
320 x 400 x 2.2 = 281600 mm3.

Analytic ventilated volume:
281600 - (2747.5088 x 2.2) = approximately 275555.48 mm3.

The executed kernel volume agrees with the analytic subtraction within numerical precision.

## Export
Execution produced:
- AP22_REAR_SHELL_VENTILATED_REV_AE.step
- AP22_REAR_SHELL_VENTILATED_REV_AE.stl

The parametric source remains the authoritative reproducible artifact.

## Interpretation
This is now the preferred nominal **ventilated rear-panel master kernel**.

It is not yet the complete production rear shell.

Still to add/resolve:
1. rear-shell perimeter/edge form;
2. service recess/tunnel geometry;
3. shell-to-PC-CF retention interfaces;
4. inlet/outlet internal baffles/labyrinth;
5. anti-warp/anti-drum ribs where legal;
6. exact cable/harness swept-volume audit;
7. exact RF/radar audit;
8. CFD;
9. industrial-FDM ASA process/flatness qualification.

No later feature may reduce the verified vent area or violate the 4 mm nominal vent webs without explicit revalidation.

## Checks
C1003 upper and lower executed layouts combined.
C1004 complete kernel executed.
C1005 B-rep valid.
C1006 connected solid count 1.
C1007 22 total vents.
C1008 10 upper outlets.
C1009 12 lower inlets.
C1010 all vent ends R1.5.
C1011 upper minimum nominal web 4.0 mm.
C1012 lower minimum nominal web 4.0 mm.
C1013 documented upper obstacle intersections zero.
C1014 documented lower expanded-keepout intersections zero.
C1015 upper real gross area 1330.6858 mm2.
C1016 upper 0.80 seed 1064.5487 mm2.
C1017 lower real gross area 1416.8230 mm2.
C1018 lower 0.75 seed 1062.6173 mm2.
C1019 total real geometric vent opening 2747.5088 mm2.
C1020 analytic/kernel volume consistency PASS.
C1021 STEP export generated.
C1022 STL export generated.
C1023 CFD remains OPEN.
C1024 physical ASA qualification remains OPEN.
C1025 service/retention/baffles remain OPEN.
C1026 this kernel is nominal ventilated master, not production release.

Status:
**REAR_SHELL_REV_AF_NOMINAL_VENTILATED_MASTER / 320X400X2P2 / 22_R1P5_VENTS / 4MM_MIN_WEBS / STEP_STL_EXPORT_VERIFIED / C01_TO_C1026**.
