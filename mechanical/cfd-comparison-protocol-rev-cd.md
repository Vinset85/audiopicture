# AudioPicture V2.2 — CFD comparison protocol Rev.CD

Status: **CFD_GEOMETRY_MATRIX_DEFINED / NO_CFD_RESULT_CLAIMED / H0P8_KERNEL_REQUIRED / H1P0_AVAILABLE**

## Objective
Compare the thermal-flow penalty of the acoustic labyrinth while holding the rear-shell vent topology constant.

## Geometry matrix
Case CFD-0 — reference:
- promoted Rev.BK/BM frame-aware rear shell;
- no labyrinth baffles;
- same 22 vent capsules.

Case CFD-08:
- U15 alternating-gate topology;
- H=0.8 mm;
- source Rev.CC;
- same 22 vents and retention architecture.

Case CFD-10:
- executed Rev.BW;
- U15 alternating-gate topology;
- H=1.0 mm;
- same 22 vents and retention architecture.

Do not compare against superseded Rev.AD/Rev.V vent coordinates.

## Common model requirements
Use identical:
- product orientation;
- external wall spacing;
- gravity vector;
- ambient temperature;
- air material model;
- radiation treatment;
- heat-source powers and locations;
- PCB/component thermal abstractions;
- wall/shell/frame material properties;
- external computational domain;
- mesh strategy and convergence criteria.

The only intended geometry variable between CFD-08 and CFD-10 is baffle height.

## Boundary-condition policy
Do not impose arbitrary inlet/outlet mass flow for the natural-convection release comparison.

The preferred release study is buoyancy-driven natural convection with openings connected to the same external pressure environment.

A forced-flow auxiliary study may be used for resistance characterization, but must be reported separately.

## Minimum outputs
For each case record:
- total inlet mass flow;
- total outlet mass flow;
- pressure difference across lower and upper labyrinth regions;
- peak and area-weighted vent velocity;
- recirculation/dead-zone observations;
- TPA3255 temperature metric;
- Raspberry Pi 5 temperature metric;
- internal air temperature metric;
- mesh count and convergence evidence.

## Comparison metrics
Report CFD-08 and CFD-10 relative to CFD-0 for:
- mass-flow change;
- component-temperature change;
- pressure-loss change.

No acceptance threshold is invented here. Release thresholds require system thermal requirements or measured prototype correlation.

## Mesh requirements
Refine:
- 3 mm vent capsules;
- 1.2 mm baffle thickness;
- 0.8/1.0 mm baffle heights;
- 1.8/2.0 mm nominal under-rib gaps;
- narrow gate openings;
- near-wall boundary layers as supported by the selected solver/model.

Perform at least one mesh-independence comparison before using results for release.

## Acoustic separation
CFD does not validate acoustic attenuation.

Use the same CFD-selected geometries in an acoustic prototype comparison so thermal and acoustic tradeoffs refer to identical parts.

## Checks
C1406 three-case CFD matrix defined.
C1407 CFD-0 is Rev.BK/BM no-baffle reference.
C1408 CFD-08 is U15 H0.8.
C1409 CFD-10 is executed U15 H1.0.
C1410 22 vent coordinates held constant.
C1411 natural convection is preferred release model.
C1412 arbitrary imposed mass flow rejected for release comparison.
C1413 forced-flow resistance study allowed only as auxiliary.
C1414 common thermal loads required.
C1415 common ambient/domain/gravity required.
C1416 mesh refinement around vents/baffles/gaps required.
C1417 mesh-independence evidence required.
C1418 mass-flow/pressure/temperature outputs defined.
C1419 no acceptance threshold invented.
C1420 acoustic validation remains separate.
C1421 no CFD result claimed.

Status:
**THERMAL_REV_CD / CFD0_CFD08_CFD10 / CONTROLLED_GEOMETRY_COMPARISON / SOLVER_RUN_OPEN / C01_TO_C1421**.
