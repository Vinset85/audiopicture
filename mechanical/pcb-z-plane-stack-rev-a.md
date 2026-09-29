# AudioPicture V2.2 Rev.A — PCB Z-plane and component-side architecture

Status: **ALL_FIVE_PCB_Z_PLANE_SEEDS_DEFINED / 40MM_COARSE_3D_PACKING_PASS / EXACT_STEP_COLLISION_GATE**

## 1. Purpose
Extend the master digital mock-up from XY packing to first-order 3D packaging.

Coordinate convention:
- Z=0 front cosmetic surface;
- positive Z toward rear/wall;
- external rear plane Z=40 mm.

Known front stack:
- acoustic/cosmetic layer approximately Z=0..2 mm;
- DML approximately Z=2..8 mm.

All electronics must remain behind the DML or in dedicated non-interfering cavities.

## 2. General PCB convention
Nominal PCB thickness:
**1.6 mm**

For packaging, define:
- FRONT SIDE = side facing DML/front;
- REAR SIDE = side facing rear shell/wall.

Where practical, tall components are placed on only one side to simplify carriers and service clearances.

Do not allow component bodies to contact the DML.

## 3. MAIN-P

### Nominal board plane
Set PCB laminate:
**Z = 18.0..19.6 mm**

Nominal board center plane:
**Z = 18.8 mm**

### Component orientation
Dominant/tall power components:
**REAR SIDE**

Rationale:
- free XY region permits use of rear cavity;
- isolates hot power components from DML;
- improves coupling to rear convection chimney.

### Tallest known envelope
470 uF capacitor CAD pocket:
**19 mm rearward from board-side reference envelope**

A literal 19 mm body placed entirely rearward from Z=19.6 would exceed Z=38.6 before rear-shell/service allowance.

Therefore the bulk capacitor cannot use the generic board-plane rule without local treatment.

Freeze architecture:
**C_BULK_LOCAL_RECESS_REQUIRED**

Options allowed in detailed CAD:
A. capacitor mounted front-side into a dedicated free-XY pocket;
B. locally lowered PCB/carrier plane;
C. qualified horizontal/low-profile mechanical mounting if electrically/manufacturing acceptable.

Preferred first solve:
**front-side bulk capacitor pocket**, because the MAIN-P XY region is not behind an exciter.

With board front surface near Z=18.0, a 19 mm frontward envelope would approach Z=-1 and is impossible if measured literally from body base.

Therefore exact capacitor lead/body geometry must be solved rather than using a symmetric 19 mm box.

Conclusion:
MAIN-P generic board plane is viable for normal components, but the radial 470 uF capacitor remains a local Z-stack blocker requiring exact oriented CAD.

Do not declare MAIN-P final Z pass until that component is solved.

## 4. MAIN-P revised capacitor strategy
Preferred production packaging direction:
**radial capacitor axis parallel to PCB plane (horizontal lay-down)** using controlled mechanical retention if manufacturer lead-form rules permit.

Required CAD reserve for laid-down EEU-FR1V471B:
- body length class ~16 mm;
- body diameter class ~10 mm;
- lead/service/retention envelope.

Initial laid-down local box:
**20 x 12 x 12 mm class**

This converts the previous 19 mm vertical H4 problem into approximately 12 mm Z class.

Exact lead bend radius and body clearance require manufacturer drawing/process validation.

If horizontal mounting is rejected by reliability/manufacturing review, MAIN-P board Z must be locally re-optimized.

## 5. MAIN-C

### Nominal board plane
PCB laminate:
**Z = 17.0..18.6 mm**

Center:
**Z = 17.8 mm**

### Component orientation
Most tall connector/PoE components:
**REAR SIDE**

Expected available rear component height before a 2.0 mm shell at Z=40:
- 40 - 2 - 18.6 = **19.4 mm**

This is compatible in first order with the ~14 mm-class Ag53024 body and typical low-profile logic.

RJ45 and mating/service geometry remain exact-CAD gates.

ESP32 antenna area shall remain free of rear conductive/PC-CF obstruction.

## 6. VOICE PCB-B

### Nominal board plane
PCB laminate:
**Z = 12.0..13.6 mm**

Center:
**Z = 12.8 mm**

### Orientation
Microphones:
**FRONT SIDE**, acoustic ports toward controlled front acoustic channels.

XVF3800/regulators/QSPI/FPC:
prefer **REAR SIDE** where routing permits.

### Front clearance
DML rear plane is approximately Z=8 mm.

PCB front surface at Z=12 mm gives:
**~4 mm nominal separation**

The microphone-port acoustic channel/carrier shall bridge acoustically, not structurally, toward the front fabric.

No rigid microphone body contact with DML.

VOICE carrier isolation hardware must fit around this plane.

## 7. RADAR PCB-C

### Nominal board plane
PCB laminate:
**Z = 11.0..12.6 mm**

Center:
**Z = 11.8 mm**

### Orientation
BGT60TR13C antenna face:
**FRONT SIDE**

Forward path toward fabric must be RF clean.

Other support components:
rear side where useful.

DML geometry in front of the radar location must not place conductive/carbon material in the RF path. The final local front/radome architecture may require a dedicated non-DML sensing window/edge path depending on EM simulation.

This is a critical release gate.

## 8. ENV PCB-D

### Nominal board plane
PCB laminate:
**Z = 12.0..13.6 mm**

Center:
**Z = 12.8 mm**

### Orientation
OPT3004:
front side toward optical tunnel.

SHT45:
side/front arrangement coupled to its isolated micro-air chamber.

Other passives/FPC:
rear side.

The ENV board shall not be used as a structural wall between the main chimney and environmental chamber.

## 9. Rear shell
Nominal local inner rear boundary for generic electronics:
- external Z=40 mm;
- shell thickness 2.0..2.4 mm;
- inner shell surface approximately Z=37.6..38.0 mm.

Maintain assembly clearance between tallest rear-side component and inner shell.

Initial generic minimum:
**1.0 mm static clearance**
unless connector/service geometry requires more.

Thus preferred generic rear-side component envelope limit:
approximately **Z <=36.6..37.0 mm**.

## 10. Coarse Z checks

### MAIN-C
Rear-side allowance from PCB rear surface 18.6 to generic component limit 36.6:
**~18 mm**

First-order PASS for Ag53024 ~14 mm class.
Exact RJ45/service: OPEN.

### VOICE
Rear-side allowance from 13.6 to 36.6:
**~23 mm**
PASS coarse.

Front gap to DML:
~4 mm.
PASS coarse, isolation/acoustic carrier open.

### RADAR
Rear-side allowance from 12.6 to 36.6:
**~24 mm**
PASS coarse.
Forward RF path remains critical.

### ENV
Rear-side allowance from 13.6 to 36.6:
**~23 mm**
PASS coarse.

### MAIN-P
Normal rear-side components:
allowance from 19.6 to 36.6:
**~17 mm**
PASS for XAL7050 and normal power components.

470 uF vertical radial pocket:
**does not automatically pass**.
Horizontal lay-down/local mechanical solution required.

## 11. Exciter-column relationship
No PCB occupies the coarse XY exciter columns.

Therefore the Z=35 mm exciter clearance requirement does not directly stack with the PCB/component Z planes.

This remains the key 2.5D packaging principle.

## 12. Cable Z corridor
Create a general FPC/low-voltage cable corridor:
**Z approximately 14..18 mm**
where XY permits.

Power/speaker harnesses may use deeper rear corridors.

Do not route cable across:
- exciter rear caps;
- radar RF cone;
- microphone acoustic channels;
- rear-shell contact points.

## 13. Carrier planes
Initial carrier strategy:
- VOICE isolated carrier around Z~11..14 mm;
- RADAR non-conductive carrier around Z~10..13 mm;
- ENV thermally isolated carrier around Z~11..14 mm;
- MAIN-C/P rigid structural carriers tied to PC-CF frame.

Exact carrier thickness is part of shared CAD.

## 14. Thermal implications
MAIN-P tall/hot components face rear chimney.
MAIN-C PoE/connectivity components face rear chimney.

VOICE/RADAR/ENV low-power boards sit closer to the front to preserve rear airflow volume and sensing paths.

No board shall bridge the full rear chimney width.

## 15. 40 mm coarse 3D verdict
Current first-order result:

- EX25FHE2-4 columns: PASS conditionally, ~5 mm rear allowance.
- MAIN-C: PASS coarse.
- VOICE: PASS coarse.
- RADAR: PASS coarse, RF-front architecture open.
- ENV: PASS coarse.
- MAIN-P normal components: PASS coarse.
- MAIN-P 470 uF radial capacitor: **LOCAL PACKAGING ACTION REQUIRED**.

Therefore the product architecture remains compatible with 40 mm, but full 3D packaging is not released until the bulk capacitor and exact connector/STEP envelopes are solved.

## 16. CAD parameters
- MAIN_P_PCB_Z0 = 18.0 mm
- MAIN_P_PCB_Z1 = 19.6 mm
- MAIN_C_PCB_Z0 = 17.0 mm
- MAIN_C_PCB_Z1 = 18.6 mm
- VOICE_PCB_Z0 = 12.0 mm
- VOICE_PCB_Z1 = 13.6 mm
- RADAR_PCB_Z0 = 11.0 mm
- RADAR_PCB_Z1 = 12.6 mm
- ENV_PCB_Z0 = 12.0 mm
- ENV_PCB_Z1 = 13.6 mm
- GENERIC_REAR_COMPONENT_LIMIT = 36.6 mm
- GENERIC_REAR_CLEARANCE_MIN = 1.0 mm

## 17. Immediate packaging blockers
Priority:
1. solve EEU-FR1V471B orientation/retention;
2. import exact Ag53024;
3. import RJ45 and mating cable envelope;
4. import Micro-Fit/FPC connector service envelopes;
5. freeze radar front RF/radome path;
6. design VOICE isolation carrier;
7. freeze carrier thicknesses;
8. rerun full C01..C20 DMU.

Status: **PCB_Z_SEEDS_MAINP_18 / MAINC_17 / VOICE_12 / RADAR_11 / ENV_12 / BULK_CAP_LOCAL_ACTION_REQUIRED**.
