# AudioPicture V2.2 Rev.A — daughterboard envelopes and placement map

Status: **VOICE_RADAR_ENV_COARSE_ENVELOPES_AND_PLACEMENT_SEEDS_DEFINED / NATIVE_PCB_AND_EXACT_STEP_COLLISION_GATE**

## 1. Purpose
Replace the undefined VOICE, RADAR and ENV placement regions in the master DMU with concrete first-order PCB outlines and product coordinates.

These are packaging seeds for native PCB layout and shared CAD. They are not production-frozen board outlines.

## 2. Hard exclusions
All daughterboards shall:
- remain inside the 20 mm protected product perimeter unless an explicitly required sensing aperture dictates otherwise;
- avoid the four EX25FHE2-4 exclusion columns;
- avoid MAIN-P and MAIN-C;
- preserve cable bend/service volume;
- remain within Z=40 mm;
- preserve DML acoustic perimeter sealing.

## 3. VOICE PCB-B

### Functional constraint
Four IM72D128 microphones use the existing SQ66 geometry:
- microphone centers at approximately +/-33.3 mm from array center in X/Y;
- square diagonal arrangement equivalent to a 66.6 mm center-to-center span on each axis.

A PCB carrying all four microphones therefore cannot be a very small central module.

### PCB outline seed
Set first packaging outline:
**82 x 82 mm**

This allows:
- four microphone positions;
- XVF3800;
- QSPI;
- 0.9 V / 1.8 V rails;
- oscillator;
- FPC;
- edge/mechanical margin.

### Product placement seed
VOICE PCB center:
**(160, 60) mm**

Envelope:
- X = 119..201 mm
- Y = 20..102 mm

This clears the coarse L1 exciter box X37..99/Y50..110 and the R2 box X223..285/Y88..148.

It remains inside the 20 mm protected perimeter with the lower edge at Y=20 mm.

### Microphone coordinates
Relative to board center:
- M1 = (-33.3, -33.3)
- M2 = (+33.3, -33.3)
- M3 = (+33.3, +33.3)
- M4 = (-33.3, +33.3)

Product microphone centers:
- M1 = (126.7, 26.7)
- M2 = (193.3, 26.7)
- M3 = (193.3, 93.3)
- M4 = (126.7, 93.3)

All microphone ports require dedicated front acoustic channels through fabric without a hard bridge to the DML.

### Mechanical isolation
VOICE PCB shall use an isolated carrier with compliant mounts.

Do not clamp VOICE PCB directly to the vibrating DML panel.

The carrier may reference the rear structural frame but shall include vibration isolation and shall not become a hard DML support.

## 4. RADAR PCB-C

### Functional constraint
BGT60TR13C integrated antenna requires a controlled forward RF volume at 60 GHz.

### PCB outline seed
Set:
**38 x 32 mm**

This is a packaging allocation, not a native-layout release outline.

### Product placement seed
Center:
**(268, 200) mm**

Envelope:
- X = 249..287 mm
- Y = 184..216 mm

This clears:
- R2 coarse box ending Y=148;
- R1 coarse box beginning Y=238;
- MAIN-P ending X=220;
- MAIN-C beginning Y=315.

### RF cone
Create a forward RF keep-out originating from the antenna face toward the front fabric.

Initial CAD screening cone:
- half-angle: **45 degrees**
- forward path from radar antenna to front exterior;
- no metal;
- no PC-CF;
- no copper plane/PCB in front;
- no wall-mount hardware.

The 45-degree value is a conservative packaging seed, not a statement of final antenna beamwidth.

Final RF keep-out shall be replaced by antenna/radome EM simulation and Infineon layout/radome guidance.

### Local material
Forward carrier/radome region:
- unfilled non-conductive polymer;
- no carbon-filled filament in RF cone.

## 5. ENV PCB-D

### Functional constraint
SHT45 needs representative room air and OPT3004 needs a front optical path.

### PCB outline seed
Set:
**42 x 24 mm**

### Product placement seed
Center:
**(273, 47) mm**

Envelope:
- X = 252..294 mm
- Y = 35..59 mm

This:
- stays inside protected perimeter;
- clears R2 coarse exciter box which begins at Y=88;
- remains away from MAIN-P;
- is near lower/right external room-air access.

### SHT45 chamber
Create a side/lower micro-air chamber adjacent to ENV PCB.

Requirements:
- separate from main thermal chimney;
- hidden micro-openings to room;
- no direct hot-air exhaust from MAIN-P;
- thermally weak connection to PC-CF structural members.

### OPT3004
Provide a front optical tunnel through the fabric.

The optical tunnel shall not double as the main ENV ventilation opening.

Fabric attenuation/calibration remains required.

## 6. Coarse XY collision screen

### VOICE vs exciters
VOICE X119..201 / Y20..102.

- L1 X37..99: separated in X by 20 mm.
- R2 X223..285: separated in X by 22 mm.
- L2/R1 separated in Y.

PASS coarse rectangular screen.

### RADAR vs exciters
RADAR X249..287 / Y184..216.

- R2 ends Y148: 36 mm vertical separation.
- R1 begins Y238: 22 mm vertical separation.

PASS coarse rectangular screen.

### ENV vs exciters
ENV X252..294 / Y35..59.

R2 begins Y88: 29 mm vertical separation.

PASS coarse rectangular screen.

### Boards vs MAIN
VOICE Y20..102 vs MAIN-P Y112..157:
- 10 mm board-edge separation.

RADAR X249..287 vs MAIN-P ending X220:
- 29 mm separation.

ENV separated from MAIN-P in both X/Y.

All daughterboards are separated from MAIN-C Y315..370.

PASS coarse board-body screen.

## 7. Cable routing seeds
VOICE:
- route FPC upward/right or centrally toward MAIN-C while avoiding MAIN-P and R2/R1 columns.

RADAR:
- route FPC upward along right-side free corridor toward MAIN-C.

ENV:
- route FPC upward along right perimeter corridor;
- keep away from radar RF cone.

All routes require exact FPC bend-volume solving.

## 8. Z placement
Do not stack any daughterboard behind an exciter.

Initial architecture:
- daughterboards occupy free XY cavities;
- component sides and carrier Z planes shall be optimized after native layouts;
- microphone acoustic ports and radar antenna face require controlled front-facing paths.

No final Z coordinate is frozen in this document.

## 9. DMU parameter updates
Replace undefined board-envelope placeholders with:

VOICE_BOARD:
- X 119..201
- Y 20..102
- outline 82 x 82 mm

RADAR_BOARD:
- X 249..287
- Y 184..216
- outline 38 x 32 mm

ENV_BOARD:
- X 252..294
- Y 35..59
- outline 42 x 24 mm

Keep Z as open parameters.

## 10. Native PCB implications
VOICE:
- native layout must preserve exact SQ66 microphone centers and port geometry;
- if 82 x 82 cannot route cleanly, board may grow inward/upward only after DMU collision check.

RADAR:
- RF layout rules dominate compactness;
- do not shrink below what Infineon antenna/layout constraints permit merely to preserve this seed.

ENV:
- thermal isolation and optical/air openings dominate outline optimization.

## 11. Release gates
1. native PCB placement for each daughterboard;
2. exact component 3D envelopes;
3. board-edge connector/FPC orientation;
4. carrier geometry;
5. vibration isolation model for VOICE;
6. radar radome/EM model;
7. ENV CFD thermal-bias model;
8. exact FPC swept volumes;
9. full C01..C20 DMU collision run;
10. freeze daughterboard Z planes.

Status: **VOICE_82x82_CENTER_160_60 / RADAR_38x32_CENTER_268_200 / ENV_42x24_CENTER_273_47 / COARSE_XY_PASS**.
