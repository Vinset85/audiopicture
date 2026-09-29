# AudioPicture V2.2 Rev.A — MAIN PCB mechanical height map

Status: **MAIN_HEIGHT_ZONING_BASELINE_DEFINED / FULL_PLACEMENT_AND_STEP_COLLISION_SOLVE_OPEN**

## 1. Purpose
Define mechanical placement classes for PCB-A MAIN before native KiCad placement and before the enclosure frame is frozen.

Nominal board target remains approximately 220 x 70 mm. This document does not freeze the exact board outline.

## 2. Height datum
Component height is measured from the PCB component-side surface.

Classes:
- H0: <=2.0 mm
- H1: >2.0 to 5.0 mm
- H2: >5.0 to 10.0 mm
- H3: >10.0 to 15.0 mm
- H4: >15.0 mm

Collision CAD shall use exact maximum/seated dimensions rather than class boundaries.

## 3. Audio power zone
### Four output inductors
Candidate: Coilcraft XAL7050-103MEC.
Class: H1/H2 boundary by exact manufacturer body dimension; reserve a 5.5 mm conservative CAD height until STEP cross-check.
Placement rule:
- group near TAS5825M outputs;
- preserve BTL symmetry/current-loop discipline;
- keep clear of exciter rear cylinders;
- do not place directly beside VOICE interconnect zone if avoidable.

### PVDD bulk
Candidate: Panasonic EEU-FR1V471B.
Class: H4.
Electrical can body commonly listed as 10 x 16 mm; collision envelope shall use 17.5 mm seated maximum until exact lead-form drawing is reconciled.
Placement rule:
- dedicated tall-component pocket;
- no exciter overlap;
- no rear-frame rib above can;
- service/assembly clearance in addition to seated height.

## 4. Tall-component pocket
Create one explicit H4 pocket in the MAIN placement plan for the PVDD bulk capacitor.

Initial mechanical envelope from PCB surface:
- XY: >=12 x 12 mm local no-collision box around nominal 10 mm can;
- Z: >=19 mm reserved including seated-height and assembly tolerance.

This pocket shall be placed in an exciter-free corridor and must not determine the global product thickness.

If exact CAD shows insufficient Z, preferred remedies in order are:
1. move the capacitor in XY;
2. locally notch/route rear structural rib;
3. reshape MAIN outline;
4. evaluate electrically equivalent distributed bulk capacitance.
Do not reduce DML/exciter safety clearance first.

## 5. Functional height zones
Partition MAIN into these placement zones:

A. AUDIO / PVDD
- TAS5825M
- 4 x XAL7050-103
- LC capacitors
- 470 uF bulk
- speaker harness egress
- local PVDD ceramics

B. POWER CONVERSION
- input protection / source selection
- INA228/shunt
- TPSM63603
- TPS62823
- local capacitors

C. POE / ETHERNET
- Ag53024
- W5500
- 25 MHz crystal
- Ethernet magnetics
- RJ45 interface

D. MCU / RF
- ESP32-S3-WROOM-1-N16R8
- antenna keep-out
- USB data routing adjacency as required

E. SERVICE / CONNECTORS
- 24 V input
- USB-C
- FPC daughterboard connectors
- test/recovery interfaces

## 6. Exciter-overlap rule
Projected XY overlap with an exciter keep-out is forbidden for:
- H4 components;
- H3 components unless exact Z-stack proves clearance;
- connector mating/service volumes;
- rigid frame posts/ribs.

H0/H1/H2 overlap is not automatically allowed: it still requires exact Z-stack and DML motion clearance.

## 7. Board-outline strategy
Start with 220 x 70 mm rectangle for placement studies.

Permit:
- edge notches around exciter cylinders;
- local narrowing;
- connector tabs;
- mounting ears outside sensitive current/RF zones.

Reject a complex outline unless it produces a real collision/service benefit.

## 8. Preferred orientation
Maintain long-axis vertical as first enclosure configuration.

Orient the board so:
- connection/service edge approaches rear connection bay;
- AUDIO zone has short flexible paths to LEFT/RIGHT exciter harnesses;
- ESP32 antenna faces an RF-clean non-metallic enclosure region;
- POE/Ethernet high-current/noisy area is separated from VOICE;
- H4 capacitor occupies a known free pocket.

Exact X/Y is solved in shared CAD.

## 9. PCB mounting plane
The MAIN mounting Z shall be chosen from actual component-side orientation and rear-shell geometry.

Do not assume a centered PCB plane. It may be advantageous to place components into the deeper DML-side void in exciter-free corridors while keeping solder-side clearance to the rear shell.

Any such orientation must preserve serviceability and electrical creepage/clearance.

## 10. Thermal map coupling
Height map and thermal map are coupled.

Hot zones:
- TAS5825M / output filter;
- PoE module;
- 5 V converter;
- input protection path under load.

Keep the H4 electrolytic away from avoidable hot spots; lifetime analysis shall use local capacitor ambient/hot-spot temperature, not room temperature.

## 11. Native KiCad placement gate
Before detailed native PCB placement:
1. import exact board-critical footprints;
2. attach verified/derived 3D envelopes;
3. place H4/H3 components first;
4. reserve antenna/RF/service keep-outs;
5. then place power/audio loops;
6. run board-vs-enclosure interference;
7. only then optimize low-profile logic placement.

## 12. Immediate CAD implications
The MAIN is not yet proven to fit as an unmodified 220 x 70 mm rectangle.

However, the selected audio inductor is low enough that the 470 uF capacitor is currently the dominant known audio-zone Z feature. A single controlled H4 pocket is therefore preferable to increasing the entire electronics cavity depth.

Status: **MAIN_HEIGHT_ZONING_BASELINE_DEFINED / FULL_PLACEMENT_AND_STEP_COLLISION_SOLVE_OPEN**.
