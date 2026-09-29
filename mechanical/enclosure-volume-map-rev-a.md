# AudioPicture V2.2 Rev.A — Enclosure volume map and 40 mm depth budget

Status: **VOLUME_ARCHITECTURE_BASELINE_FROZEN / COMPONENT_HEIGHT_AND_SHARED_CAD_COLLISION_GATE**

## 1. Product datum
Maximum external envelope:
- width X = 320 mm;
- height Y = 400 mm;
- depth Z = 40 mm.

DML active-panel datum:
- 300 x 380 mm;
- centered nominally inside the product envelope;
- DML local origin is 10 mm from the product left and lower edges when centered.

Candidate-B exciter centers converted to product coordinates:
- L1 = (68,80) mm;
- L2 = (114,196) mm;
- R1 = (206,268) mm;
- R2 = (254,118) mm.

These are nominal FEA/CAD seed coordinates, not production drill dimensions.

## 2. Z-stack baseline
Allocate depth from front to rear as follows:

Z0..2 mm:
- printed acoustic fabric and front cosmetic/support allowance.

Z2..8 mm:
- nominal A1 DML structural sandwich, approximately 6 mm.

Z8..29 mm:
- rear exciter volumes; legacy DAEX25FHE-4 reference height approximately 20.5 mm from mounting surface;
- retain >=2 mm local clearance to the rear shell or internal structures where possible.

Z29..40 mm:
- only local low-profile structure/electronics may occupy regions not intersecting exciter keep-outs;
- rear shell, manufacturing tolerance and wall-mount/interface geometry consume part of this band.

This stack demonstrates that no full-area rear electronics deck is allowed behind the DML. Electronics must be distributed in XY around the exciter cylinders and controlled keep-outs.

## 3. Exciter keep-out cylinders
For early CAD use conservative rear keep-outs centered at Candidate-B coordinates:
- radial keep-out: >=30 mm from center until successor-exciter CAD is frozen;
- Z keep-out: from rear DML skin to at least 23 mm behind the panel;
- add harness/terminal egress volume separately.

No PCB, rigid frame rib, radar module, microphone carrier or connector body may intersect these volumes.

## 4. MAIN PCB placement baseline
Target PCB-A MAIN size remains approximately 220 x 70 mm.

Preferred orientation:
- long axis vertical;
- locate along the rear central/side corridor that avoids all four exciter cylinders;
- Ethernet/PoE and 24 V connector end shall face the rear connection bay;
- amplifier/output-filter zone shall minimize harness length to the four exciters;
- ESP32 antenna region requires a non-metallic/no-copper enclosure clearance and shall not be buried behind PoE magnetics or large conductive masses.

A single 220 x 70 rectangular board shall not be considered mechanically frozen until actual component-height zoning proves collision-free. Board-outline notches or a modest outline reduction are permitted before PCB freeze if they materially improve clearance.

## 5. VOICE PCB volume
PCB-B VOICE shall be mounted to the rear structural frame on its own isolation system.

Requirements:
- no shared DML clamp posts;
- no overlap with exciter keep-outs;
- microphone acoustic ports require controlled front acoustic paths through the fabric/front construction;
- carrier location should minimize DML structural acceleration;
- FPC service loop shall not touch the active panel.

The SQ66 microphone geometry controls the local board footprint and must be preserved.

## 6. RADAR PCB volume
PCB-C RADAR shall sit behind a dedicated non-conductive forward RF window/volume.

Requirements:
- no GFRP/carbon/metal fastener assumptions inside the RF cone without EM validation;
- avoid exciter magnet/metal mass in the forward/near-field keep-out;
- avoid MAIN ground planes and PoE magnetics behind/adjacent where the RF model identifies sensitivity;
- keep the front fabric/radome stack locally controlled.

Final radar coordinates require shared RF CAD/EM analysis.

## 7. ENV PCB volume
PCB-D ENV occupies a lower/side passive-air chamber:
- thermally isolated from MAIN, amplifier, PoE and DC/DC;
- hidden micro-air channels to room air;
- SHT45 not in direct stagnant contact with warm rear-shell air;
- OPT3004 has a matte-black optical tunnel toward the fabric;
- ENV chamber shall not become a DML brace.

## 8. Rear connection bay
Provide a recessed/controlled rear-side bay for:
- shielded RJ45;
- locking 24 V input;
- USB-C service/recovery.

Cable plugs and bend radii count toward installation clearance even if they are outside the 40 mm product body.

The bay shall not compromise the DML compliant perimeter or create a hard structural bridge into the active panel.

## 9. Frame architecture
Use a rear structural perimeter/spine system rather than a full rigid plate immediately behind the DML.

Frame functions:
- react wall-mount loads;
- define PORON compression hard stops;
- carry PCB-A/B/C/D;
- provide safety capture for the DML;
- keep electronics away from moving-panel zones.

Ribs shall be routed around exciter keep-outs and shall not touch the active panel.

## 10. Preliminary XY zoning
Preferred functional zones, subject to CAD collision solve:
- lower/rear connection zone: RJ45, 24 V, USB-C;
- vertical electronics corridor: MAIN;
- acoustically quiet isolated zone: VOICE;
- RF-clear upper/side zone: RADAR;
- lower/side ventilated edge: ENV;
- central distributed zones: exciter keep-outs and flexible speaker harness.

Do not stack VOICE directly over the TAS5825M/output-filter region.

## 11. Thermal consequence
The 40 mm sealed/shallow architecture means natural convection is weak. Thermal design shall rely on:
- spreading heat into PCB copper and rear structural/shell area where appropriate;
- separation of SHT45 from heat sources;
- no fan;
- preserving air gaps around PoE/DC-DC/amplifier hot components;
- thermal simulation with external 24 V worst-case audio profile.

No ventilation opening may violate acoustic-fabric aesthetics, radar performance or environmental-sensor measurement integrity.

## 12. CAD collision gates
Before mechanical freeze import exact STEP/3D envelopes for:
- selected exciter revision;
- RJ45 + Ethernet transformer;
- Ag53024;
- 24 V connector;
- USB-C;
- tallest inductors/electrolytics;
- MAIN FPC connectors;
- VOICE/RADAR/ENV boards.

Run interference checks with:
- nominal geometry;
- component-height tolerance;
- PCB placement tolerance;
- DML motion/service clearance;
- enclosure print tolerance.

## 13. Release rule
The product may remain 40 mm maximum only if exact 3D component envelopes prove all collision/service/thermal clearances. If a conflict exists, first optimize XY zoning/PCB outline/component placement; do not reduce DML-to-rear clearance below safe motion/tolerance limits merely to preserve an arbitrary PCB location.
