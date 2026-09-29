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


## 13. First XY placement solve — vertical 220 x 70 rectangle

A geometry-first placement screen was performed against the current Candidate-B exciter keep-outs (R=30 mm), product envelope 320 x 400 mm and nominal 220 x 70 mm MAIN rectangle.

### Result
A full 220 x 70 mm vertical rectangle is geometrically feasible only in restricted side corridors if a strict no-overlap rule is applied to the entire PCB outline. This is unnecessarily conservative because low-profile PCB regions may coexist in XY with an exciter provided the Z-stack clears.

Therefore the production placement problem shall use **height-aware 3D collision**, not a blanket 2D board-vs-exciter exclusion.

### Baseline placement strategy
Use the MAIN long axis vertical and place it in a central-to-left or central-to-right corridor selected by component zoning, with:
- H4 PVDD pocket entirely outside all R30 exciter projections;
- H3/H4 PoE/connector volumes outside exciter projections unless exact Z proves clearance;
- H0/H1/H2 logic allowed under projected exciter XY only after exact Z clearance;
- board edge >=8 mm from structural/cosmetic outer perimeter where connector/boss geometry does not require otherwise;
- no board region inside the DML compliant-mount land.

### Board-origin parameter
Do not freeze BOARD_X/BOARD_Y from 2D screening alone. Shared CAD shall optimize BOARD_X/Y/Z simultaneously with component-side orientation.

### Notch decision
No MAIN notch is justified yet.

A notch is permitted only if the exact 3D placement cannot simultaneously provide:
1. H4 capacitor pocket clearance;
2. Ag53024/connector clearance;
3. ESP32 antenna keep-out;
4. daughterboard FPC service paths;
5. assembly/removal path.

Status: **MAIN_RECTANGULAR_OUTLINE_RETAINED_FOR_3D_PLACEMENT / HEIGHT_AWARE_COLLISION_SOLVE_REQUIRED**.


## 14. MAIN Z-stack baseline — component side toward DML

The preferred first 3D configuration is:

**rear shell -> PCB solder side -> PCB -> component side -> DML cavity**

This uses the inter-exciter cavity for component height while keeping the rear shell side comparatively flat and serviceable.

### Product Z reference
Use the master product datum with Z=0 at the visible front and Z increasing toward the wall.

Working stack for collision studies:
- front fabric/cosmetic allowance: approximately Z=0..2 mm;
- DML A1 structural stack: approximately Z=2..8 mm;
- exciter bodies project rearward from approximately Z=8 to Z=28.5 mm using the legacy 20.5 mm reference;
- maintain >=2 mm nominal clearance beyond the exciter body where a rigid object lies directly behind it.

### MAIN board plane seed
Use an initial PCB component-side reference plane near **Z=34 mm**, with components projecting toward decreasing Z (toward the DML).

Assuming approximately 1.6 mm PCB thickness, the solder side/rear face lies near Z=35.6 mm before local solder/lead allowances, leaving roughly 4.4 mm to the 40 mm external limit for rear shell, standoffs and tolerance. This is a CAD seed only.

### Height-aware consequence
At PCB component plane Z=34 mm:
- an H1 5 mm component reaches approximately Z=29 mm;
- an H2 10 mm component reaches approximately Z=24 mm;
- the H4 capacitor envelope of 19 mm reaches approximately Z=15 mm.

Therefore:
- H0/H1 regions can potentially sit behind an exciter projection if exact body geometry and >=2 mm clearance are satisfied;
- H2 generally conflicts with the legacy exciter depth where projected XY overlaps;
- H3/H4 must be placed in inter-exciter free volumes.

With the conservative legacy exciter rear body ending near Z=28.5 mm, a 5 mm component ending at Z=29 mm provides only about 0.5 mm nominal separation and is **not acceptable**. Thus H1-under-exciter is not automatically released at BOARD_Z=34 mm.

### Clearance target
Require >=2.0 mm nominal rigid-body clearance between exciter envelope and any PCB/component/frame object, before print/assembly tolerance stack.

To place a 5 mm component directly behind a legacy exciter would require moving the component-side PCB plane farther rearward than approximately Z=35.5 mm, which is incompatible with the current rear-shell budget. Consequently only lower-profile H0/low-H1 parts may ultimately occupy direct exciter-overlap regions.

### PCB plane optimization window
Shared CAD shall sweep the PCB component plane approximately Z=33..35 mm, constrained by:
- rear shell thickness;
- standoff/boss geometry;
- solder-side protrusions;
- connector THT tails;
- assembly tolerance;
- wall-mount features.

Do not freeze Z=34 mm until exact rear-shell and connector models are imported.

### Through-hole consequence
RJ45, Micro-Fit, USB retention tabs and other THT features require local rear/solder-side clearance. These may force local shell recesses or connector-edge placement independent of the general board plane.

### H4 capacitor orientation
The 470 uF capacitor shall remain vertical to the PCB for the baseline. Do not bend/lay it horizontally merely to solve Z unless vibration, lead stress, assembly and electrical-loop implications are requalified.

At the Z=34 mm seed its 19 mm conservative envelope occupies to approximately Z=15 mm, so it requires a clean inter-exciter column through that depth.

### Mechanical conclusion
The preferred architecture is retained:
- MAIN near rear shell;
- components facing DML;
- tall components placed between exciter volumes;
- low-profile logic may use limited overlap regions;
- rear shell may use local boss/recess geometry rather than moving the whole board forward.

Status: **MAIN_COMPONENT_SIDE_TOWARD_DML_BASELINE / BOARD_Z_33_TO_35MM_COLLISION_SWEEP_REQUIRED**.


## 15. Combined XYZ placement seed

Combining the 220 x 70 mm vertical MAIN target, Candidate-B exciter centers, R=30 mm preliminary keep-outs and the Z=33..35 mm board-plane window yields the following first shared-CAD seed:

- **BOARD_X = 125 mm**
- **BOARD_Y = 90 mm**
- **BOARD_W = 70 mm**
- **BOARD_H = 220 mm**
- **BOARD_Z_COMPONENT_PLANE = 34 mm**
- long axis vertical;
- component side faces the DML.

This places the nominal PCB rectangle at:
- X = 125..195 mm;
- Y = 90..310 mm.

### Why this seed
The central corridor keeps the board away from the product outer perimeter and connection-frame edges while distributing projected exciter intersections mainly toward board corners/edges rather than consuming the full board width.

The rectangle is not collision-free in 2D and is not intended to be. Its purpose is to create usable height-zoned regions:
- central inter-exciter column for H3/H4;
- edge/corner overlap regions reserved for H0/very-low-H1 only;
- upper/lower service regions adjustable toward the final connection bay.

### H4 placement region
Reserve the PVDD 470 uF capacitor near the board centerline and select its exact Y only after exact exciter-body and Ag53024 envelopes are imported.

The H4 pocket must satisfy:
- >=30 mm radial projected separation from every exciter center for the conservative first CAD pass;
- >=2 mm rigid-body Z clearance after exact geometry;
- no rear-frame rib overhead;
- thermal separation from avoidable PoE/DC-DC heat.

### BOARD_Z
Retain Z=34 mm as the nominal seed and sweep 33..35 mm.

Z=35 mm is mechanically attractive on the component side but leaves less rear-shell/solder-side budget.
Z=33 mm increases rear-shell margin but sharply reduces allowed component height under exciter projections.

The final optimum therefore depends on exact rear-shell thickness and THT lead/connector geometry.

### Board-outline decision
The 220 x 70 rectangular outline remains preferred for the next CAD iteration. No evidence yet justifies a notch.

### Required next solve
The next placement pass shall use exact/derived 3D envelopes for:
- legacy and successor exciters;
- Ag53024;
- 470 uF capacitor;
- XAL7050;
- RJ45/magnetics;
- Micro-Fit 24 V;
- USB-C;
and shall optimize component placement and board position together.

Status: **MAIN_XYZ_SEED_DEFINED_X125_Y90_Z34 / EXACT_3D_COMPONENT_COLLISION_OPTIMIZATION_REQUIRED**.


## 16. Successor-exciter collision re-solve

The EX25FHE2-4 manufacturer drawing supersedes the legacy depth assumption for production packaging studies.

Use for coarse collision:
- outer framed footprint approximately 58.3 x 56 mm;
- depth 25.5 +/-0.5 mm from its mounting reference;
- coarse XY exclusion rectangle expanded to 62 x 60 mm for first-pass tolerance/wiring;
- no useful electronics volume assumed directly behind the exciter.

### Effect on previous X125/Y90/Z34 seed
The previous MAIN seed is **withdrawn as a production placement candidate**.

Reason: at the current Candidate-B centers, a 70 x 220 vertical board in the central region intersects successor-exciter full-depth exclusion volumes. Moving the board plane rearward cannot recover adequate room within the 40 mm product envelope once PCB thickness, rear shell, solder-side features and assembly tolerance are included.

### New placement rule
Treat each successor exciter as a full-depth exclusion column from the DML rear surface to the rear-shell electronics zone.

No PCB substrate, component, rigid frame rib or connector service volume may cross those columns in the baseline CAD model.

Only flexible harness may cross locally, subject to abrasion and motion clearance.

### Consequence for MAIN outline
The simple 70 x 220 rectangular MAIN is no longer the preferred architecture.

The next CAD solve shall compare:
A. a notched/slender MAIN that routes around the four exciter columns;
B. two electrically connected MAIN sub-boards, separating power/audio from MCU/Ethernet/service;
C. a shorter MAIN placed entirely in a single exciter-free corridor.

Do not increase product depth beyond 40 mm before these planar packaging options are exhausted.

### Preferred direction
Option A remains first to test because it preserves one PCB and avoids additional board-to-board connectors. However, a highly constricted neck is rejected if it compromises:
- return-current continuity;
- power copper width;
- PCB stiffness;
- assembly panelization;
- EMC partitioning.

Option B becomes preferred if a one-board outline requires narrow necks or awkward high-current routing.

### 40 mm feasibility
The successor exciter does **not** by itself disprove the 40 mm product target. It removes the previous behind-exciter electronics assumption and makes XY packing the dominant problem.

Status: **OLD_MAIN_X125_Y90_Z34_SEED_WITHDRAWN / FULL_DEPTH_EXCITER_COLUMNS_ACTIVE / PLANAR_MAIN_REPACK_REQUIRED**.


## 17. Candidate-B free-space map with EX25FHE2-4 columns

Using Candidate-B product coordinates:
- L1 = (68,80) mm
- L2 = (114,196) mm
- R1 = (206,268) mm
- R2 = (254,118) mm

and the coarse successor-exciter exclusion box 62 x 60 mm centered on each point, the first-pass blocked rectangles are:

- L1: X 37..99, Y 50..110
- L2: X 83..145, Y 166..226
- R1: X 175..237, Y 238..298
- R2: X 223..285, Y 88..148

These are conservative packaging rectangles, not final exciter geometry.

### Free-space observations

The four columns do not form a continuous wall across the 320 mm product width. Large connected free space remains around and between them.

Important corridors include:

1. **central vertical meander corridor**
   Free space exists through the central product region, but its lateral position changes with Y because L2 and R1 occupy opposite sides. A rigid 70 mm-wide straight vertical PCB is inefficient here.

2. **left-side corridor**
   The region toward X<~35 mm is continuously clear of the coarse exciter boxes, but is too close to the product/DML perimeter to host the complete MAIN after frame, mount and connector margins.

3. **right-side corridor**
   Similarly, X>~287 mm is clear but too narrow for the complete electronics system.

4. **central horizontal bands**
   Useful full-width bands exist between the staggered exciters. These favor a shorter/wider PCB or multiple boards more than the previous long 70 x 220 board.

### Architecture conclusion
A single highly notched vertical MAIN would need to weave between L1/L2/R1/R2. That is mechanically possible in principle but unattractive for:
- continuous ground planes;
- high-current 24 V/PVDD routing;
- audio BTL return/current geometry;
- PCB stiffness;
- panelization and assembly;
- predictable EMC.

Therefore **Option B becomes the preferred packaging architecture**:

**MAIN-P — POWER / AUDIO / ETHERNET-POE power front end**
and
**MAIN-C — CONTROL / MCU / Ethernet logic / USB / daughterboard interfaces**

The exact functional split remains to be optimized so W5500/magnetics/RJ45 placement does not create unnecessary inter-board high-speed routing.

### Inter-board rule
Avoid sending analog Class-D power loops or raw Ethernet MDI pairs across the board-to-board link.

Preferred inter-board signals are:
- regulated power rails as justified;
- SPI or other controlled digital interfaces;
- I2C;
- GPIO/interrupt/reset;
- I2S audio clocks/data;
- housekeeping/status.

### Next optimization
Evaluate two-board rectangles in the connected free-space bands and decide which board owns:
- RJ45 + magnetics + W5500;
- Ag53024;
- 24 V source selection;
- TAS5825M and output filter;
- ESP32-S3;
- USB-C;
- FPC daughterboard interfaces.

Status: **TWO_BOARD_MAIN_ARCHITECTURE_PREFERRED / FUNCTIONAL_SPLIT_AND_RECTANGLE_PACKING_OPEN**.
