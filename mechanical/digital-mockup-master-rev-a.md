# AudioPicture V2.2 Rev.A — master digital mock-up

Status: **MASTER_DMU_NUMERIC_BASELINE_FROZEN / DAUGHTERBOARD_EXACT_ENVELOPES_AND_STEP_IMPORTS_OPEN**

## 1. Purpose
Create one authoritative packaging map for the complete 320 x 400 x 40 mm product.

This document does not replace native CAD. It defines the coordinates, envelopes, exclusion volumes and automated checks that the master CAD must implement.

## 2. Coordinate system
Origin P0:
- external front-view lower-left corner.

Axes:
- X: left -> right;
- Y: bottom -> top;
- Z: front -> wall/rear.

External product envelope:
- X = 0..320 mm
- Y = 0..400 mm
- Z = 0..40 mm

No production object may exceed this envelope unless an explicitly excluded wall-side installation part is defined separately.

## 3. Protected perimeter
Conservative electronics packaging perimeter:
**20 mm from all product edges**

Baseline no-PCB-body zone:
- X <20
- X >300
- Y <20
- Y >380

Exceptions require explicit mechanical/interface justification.

## 4. DML
Active structural panel:
- X = 10..310
- Y = 10..390
- Z approximately 2..8 mm

Dimensions:
- 300 x 380 mm
- structural stack approximately 6 mm

Front acoustic/cosmetic treatment:
- Z approximately 0..2 mm

DML perimeter acoustic boundary:
**SEALED**

## 5. EX25FHE2-4 placement
Candidate B product coordinates, center positions:

- L1 = (68, 80)
- L2 = (114, 196)
- R1 = (206, 268)
- R2 = (254, 118)

Candidate B remains subject to full FEA/acoustic comparison.

### Coarse XY exclusion boxes
Until exact STEP is imported, use 62 x 60 mm conservative boxes:

L1:
- X 37..99
- Y 50..110

L2:
- X 83..145
- Y 166..226

R1:
- X 175..237
- Y 238..298

R2:
- X 223..285
- Y 88..148

### Z exclusion
Mounting/rear DML plane approximately Z=8 mm.

EX25FHE2-4 drawing-depth high tolerance:
- rear extremity approximately Z=34 mm.

Engineering clearance:
- no rigid object before approximately Z=35 mm in the exact exciter projection.

Treat each exciter projection as a full-depth electronics/structure exclusion column until exact STEP collision solving.

## 6. MAIN-P
Board seed:
- width X = 115 mm
- height Y = 45 mm

Product placement:
- X = 105..220
- Y = 112..157

Functional zones:
- P1: local X 0..30
- P2: local X 30..65
- P3: local X 65..115

Dominant tall pocket:
- 470 uF capacitor pocket approximately local X 58..70, local Y 28..40
- envelope 12 x 12 x 19 mm.

Board Z plane:
**OPEN PARAMETER**

CAD must solve it jointly with component-side orientation, frame and rear skin.

MAIN-P shall not intersect exact exciter envelopes.

## 7. MAIN-C
Board seed:
- 150 x 55 mm

Product placement:
- X = 85..235
- Y = 315..370

Functional zones:
- C1 local X 0..55: Ethernet/PoE input domain
- C2 local X 55..105: Ag53024 output/W5500/service
- C3 local X 105..150: ESP32/RF/daughterboard interfaces

Board Z plane:
**OPEN PARAMETER**

Exact Ag53024, RJ45, USB-C and FPC service envelopes remain STEP/drawing import gates.

## 8. MAIN-C RF clean region
ESP32 antenna is toward the right/outward end of MAIN-C.

Create a parametric keep-out volume:
**RF_ESP32_KEEP_OUT**

It shall include:
- no metal wall-mount part;
- no PC-CF in prohibited near-field volume;
- no dense cable bundle;
- no Ag53024/magnetics/RJ45 shield intrusion.

Exact dimensions shall come from ESP32 module integration guidance and final antenna orientation.

Do not replace this parameter with an arbitrary fixed box before layout orientation is frozen.

## 9. RADAR region
Create:
**RADAR_BOARD_ENVELOPE**
**RADAR_FORWARD_RF_CONE**

Requirements:
- behind front fabric;
- no metal/carbon-filled polymer in forward RF path;
- away from massive PCB/cleat/exciter structures;
- electrically connected by the defined 12-pin FPC interface.

Exact board XY/Z envelope remains open pending native PCB placement.

The master CAD shall refuse release while RADAR_BOARD_ENVELOPE is undefined.

## 10. VOICE region
Create:
**VOICE_BOARD_ENVELOPE**
**VOICE_MIC_APERTURE_PATTERN**

Requirements:
- SQ66 four-mic geometry;
- mechanically isolated carrier;
- no rigid structural bridge to vibrating DML;
- front acoustic path through fabric;
- cable service volume;
- no collision with exciter columns.

Exact PCB envelope remains open.

The microphone acoustic ports shall have dedicated front-path keep-outs independent of electronics airflow.

## 11. ENV region
Create:
**ENV_BOARD_ENVELOPE**
**SHT45_AIR_CHAMBER**
**OPT3004_OPTICAL_PATH**

Requirements:
- side/lower environmental chamber;
- separate from main electronics chimney;
- hidden room-air micro-openings;
- SHT45 thermally isolated from PC-CF/hot PCB paths;
- OPT3004 front optical path through fabric;
- no exciter-column collision.

Exact board envelope remains open.

## 12. Wall mount
Two upper cleats:
- 6061-T6 candidate
- approximately 50 x 22 x 2.5 mm each
- hook engagement seed 6 mm
- two M4 fasteners per cleat.

Initial placement regions:
LEFT_UPPER_CLEAT_REGION:
- X approximately 25..75 mm

RIGHT_UPPER_CLEAT_REGION:
- X approximately 245..295 mm

Y/Z remain dependent on MAIN-C service and RF keep-outs.

Two lower support regions:
- lower-left perimeter;
- lower-right perimeter.

Anti-lift:
- M4 captive feature;
- underside accessible;
- outside exciter columns.

## 13. Rear structural frame
Create a parametric PC-CF structure with:
- closed outer structural perimeter;
- DML support/hard-stop perimeter;
- local PCB carriers;
- mount-node gussets;
- local transverse/vertical bridges.

Hard rule:
**no frame member enters exact exciter clearance columns.**

No full-area rear deck.

Initial structural wall/rib:
- 2.4 mm baseline;
- primary ribs 2.4..3.0 mm;
- local mount geometry per wall-mount hardware contract.

## 14. Rear shell
ASA unfilled.

Baseline:
- local rear skin 2.0..2.4 mm behind exciter projections;
- thicker/ribbed only where Z permits;
- not credited as primary structural member.

Rear skin must not enter the exciter Z=35 mm engineering-clearance envelope.

## 15. Airflow geometry
Wall gap CFD seed:
- 4 mm nominal
- sweep 3/4/5 mm.

Inlet:
- 600 mm2 free-area seed.

Outlet:
- 750 mm2 free-area seed.

Create:
- MAIN_VERTICAL_CHIMNEY
- LOWER_INLET_VOLUME
- UPPER_OUTLET_VOLUME

No PCB/FPC/frame feature may fully block the main vertical chimney.

## 16. Cable/service envelopes
Create separate swept/service volumes for:
- JCP 230 mm harness;
- JCS 220 mm FPC;
- VOICE FPC;
- RADAR FPC;
- ENV FPC;
- speaker harness;
- Ethernet cable;
- external 24 V cable;
- USB-C service cable.

A cable path is not considered valid merely because its centerline fits. Minimum bend and connector mating/service volumes must also fit.

## 17. Product mass model
Current nominal:
- approximately 1.55 kg.

Production design target:
- <=1.70 kg nominal.

Master CAD shall calculate:
- total mass;
- X/Y/Z center of gravity;
- mass by subsystem.

Any >20 g geometry/material change triggers mass-budget review.
Any >50 g asymmetric change triggers CG review.

## 18. Automated collision checks
The master CAD/automation shall fail release if any of the following occurs:

C01 external envelope exceeds 320 x 400 x 40.
C02 PCB/component intersects exact exciter geometry.
C03 structural frame enters exciter clearance.
C04 rear shell enters exciter minimum clearance.
C05 wall-mount hardware enters exciter column.
C06 MAIN-P intersects protected perimeter or exciter volume.
C07 MAIN-C intersects protected perimeter or exciter volume.
C08 ESP32 RF keep-out violated.
C09 radar RF cone violated.
C10 microphone acoustic path obstructed.
C11 SHT45 chamber opens into main hot plume beyond defined coupling.
C12 OPT3004 optical path obstructed.
C13 DML front/rear acoustic seal broken.
C14 main convection chimney fully blocked.
C15 cable bend/service volume invalid.
C16 RJ45/24V/USB service access invalid.
C17 cleat/anti-lift service access invalid.
C18 front frame removal path invalid.
C19 PCB removal path invalid.
C20 any production component uses a placeholder envelope.

## 19. Current coarse collision result
Using the existing coarse exciter boxes:
- MAIN-P X105..220 / Y112..157 clears L1, L2, R1 and R2.
- MAIN-C X85..235 / Y315..370 clears all four exciter boxes.
- both boards remain inside the 20 mm protected product perimeter.

Therefore the current two-board architecture passes the **coarse XY packing screen**.

This is not a STEP-level collision pass.

## 20. Open geometric blockers
Before shared CAD can be called release-grade:
1. exact EX25FHE2-4 STEP;
2. exact Ag53024 envelope/STEP;
3. RJ45 and Ethernet magnetics exact geometry;
4. USB4085 STEP;
5. Micro-Fit/JCP mated and cable envelope;
6. Hirose FPC mated/bend service volumes;
7. exact VOICE PCB outline;
8. exact RADAR PCB outline and RF cone;
9. exact ENV PCB outline/chamber;
10. PCB Z planes;
11. wall-cleat Y/Z coordinates;
12. rear-frame actual topology;
13. wall-side installation-envelope interpretation.

## 21. Release sequence
A. import exact manufacturer geometry;
B. assign all component/PCB envelopes;
C. solve PCB Z planes;
D. solve daughterboard placement;
E. generate rear-frame topology around keep-outs;
F. generate rear shell;
G. generate airflow passages;
H. run collision/service checks C01..C20;
I. calculate mass/CG;
J. export geometry to structural/thermal/acoustic/RF solvers.

Status: **TWO_BOARD_COARSE_PACKING_PASS / FULL_PRODUCT_DMU_BASELINE_DEFINED / EXACT_STEP_AND_DAUGHTERBOARD_PLACEMENT_GATE**.
