# AudioPicture V2.2 — CFD thermal-source model Rev.CH

Status: **THERMAL_SOURCE_CONTRACT_RECONCILED / SYSTEM_HEAT_SWEEP_AUTHORITATIVE / COMPONENT_DOUBLE_COUNTING_PROHIBITED / CFD_SOLVER_OPEN**

## Source reconciliation
Existing project thermal/power documents were reviewed before assigning CFD heat sources.

The enclosure-level thermal contract already defines total internal heat sweeps:
- 3 W;
- 5 W;
- 8 W;
- 10 W.

The 10 W case is explicitly adverse/stress and is not claimed as nominal operation.

These total-heat cases remain the primary authority for the first enclosure CFD comparison.

## Component-level anchors

### TAS5825M
Existing thermal contract:
- 60 W total audio output extreme sine bound;
- simple 90% efficiency bound;
- approximately 66.7 W DC input;
- approximately 6.7 W amplifier-stage loss.

Use 6.7 W only as the documented extreme continuous-sine stage-loss bound. It is not the normal product dissipation.

### TPSM63603
Existing documented operating point:
- 24 V input;
- 5 V / 2.5 A output = 12.5 W;
- approximately 91% published efficiency;
- approximately 1.24 W conversion loss.

Use only when the simulated 5 V load corresponds to that operating point or when explicitly treated as a sensitivity case.

### MAIN-C / VOICE / RADAR / ENV
The system power budget contains electrical load allocations:
- MAIN-C 1.40 W;
- VOICE 0.80 W;
- RADAR 0.20 W normal / 0.45 W stress;
- ENV 0.02 W;
- housekeeping 0.08 W.

These are not automatically equivalent to heat deposited at the named PCB/component region.

Do not use them as local CFD heat sources without rail/conversion closure.

### Ag53024
Project documents explicitly require the exact efficiency-versus-load curve.

Q_POE_AG53024 therefore remains OPEN.

### Raspberry Pi 5
No project-specific Pi 5 heat-source value was established in the reviewed thermal/power contracts.

Q_RPI5 remains OPEN rather than assigning a generic wattage.

## Double-counting rule
Two valid CFD source modes are permitted.

Mode A — enclosure heat sweep:
- distribute a defined total 3/5/8/10 W among simplified source regions according to an explicitly documented scenario;
- sum of all active sources must equal the selected system heat case.

Mode B — component-resolved:
- use calculated/measured component losses;
- aggregate MAIN-P/MAIN-C source is reduced by the component losses already represented.

Never apply a 5/8/10 W aggregate source and then add TAS5825M/TPSM63603 losses on top.

## First CFD matrix retained
From the existing CFD domain contract:
1. 5 W / 30 C / 4 mm wall gap;
2. 8 W / 30 C / 4 mm;
3. 10 W / 35 C / 4 mm;
4. 8 W / 35 C / 3 mm;
5. 8 W / 35 C / 5 mm.

For labyrinth selection, run the same matrix on CFD-0 / CFD-08 / CFD-10 where computational cost permits.

At minimum, the initial discriminator should use the same thermal case across all three geometries.

## Geometry/source regions
Retain the existing named regions:
- Q_MAIN_P;
- Q_MAIN_C;
- Q_TAS5825M;
- Q_TPSM63603;
- Q_POE_AG53024;
- Q_W5500;
- Q_ESP32;
- Q_VOICE;
- Q_RADAR.

Fluid domains retain:
- AIR_ROOM_LOWER;
- AIR_INLET;
- AIR_REAR_CAVITY;
- AIR_CHIMNEY_MAIN;
- AIR_BYPASS_LEFT;
- AIR_BYPASS_RIGHT;
- AIR_OUTLET;
- AIR_WALL_GAP;
- AIR_SHT45_CHAMBER.

## What is still missing before component-resolved temperature claims
- project-specific Raspberry Pi 5 loss/operating scenario;
- Ag53024 efficiency/load loss;
- actual 5 V and 3.3 V rail loads;
- TAS5825M ECO/PERFORMANCE loss profiles beyond the extreme bound;
- XAL7050 copper/core loss;
- PCB conduction/spreader abstractions;
- emissivity assumptions;
- detailed component/package thermal models.

Therefore the first CFD can compare enclosure/labyrinth airflow using the total heat sweep, but shall not claim final silicon junction temperatures.

## Checks
C1439 existing thermal/power contracts reviewed.
C1440 3/5/8/10W system heat sweep retained.
C1441 10W identified as adverse/stress.
C1442 TAS5825M 6.7W extreme loss bound retained with scope.
C1443 TPSM63603 1.24W documented operating-point loss retained with scope.
C1444 MAIN-C 1.40W treated as electrical allocation, not automatic heat.
C1445 VOICE 0.80W treated as electrical allocation, not automatic heat.
C1446 RADAR allocations not automatically converted to local heat.
C1447 Ag53024 local loss remains open.
C1448 project-specific Raspberry Pi 5 heat remains open.
C1449 component/aggregate double counting prohibited.
C1450 enclosure heat-sweep mode defined.
C1451 component-resolved mode defined.
C1452 existing 5-case CFD matrix retained.
C1453 same thermal case required across labyrinth geometry comparison.
C1454 named heat-source regions retained.
C1455 named fluid subdomains retained.
C1456 first CFD cannot claim final silicon junction temperatures.

Status:
**THERMAL_REV_CH / SYSTEM_SWEEP_3_5_8_10W / SOURCE_ACCOUNTING_CONTROLLED / COMPONENT_LOSSES_PARTIAL / CFD_SOLVER_OPEN / C01_TO_C1456**.
