# AudioPicture V2.2 Rev.A — 40 mm Z-stack closure

Status: **40MM_ARCHITECTURE_CONDITIONALLY_VIABLE / SHARED_CAD_STEP_COLLISION_AND_REAR_SKIN_CLOSURE_REQUIRED**

## 1. Objective
Determine whether the current architecture can physically remain within the product target:

- width: 320 mm
- height: 400 mm
- maximum total depth: 40 mm

The analysis uses the successor EX25FHE2-4 mechanical envelope, not the legacy DAEX25FHE-4.

## 2. Product Z datum
Use the existing master convention:
- Z=0 at front cosmetic/acoustic surface;
- positive Z toward wall/rear.

Target:
- Z <= 40 mm everywhere.

## 3. Front stack
Current baseline:
- printed acoustic fabric/front treatment: approximately Z=0..2 mm;
- DML structural stack: approximately 6 mm.

Therefore the rear face of the DML is approximately:
- **Z = 8 mm**.

Exact fabric/adhesive thickness remains a tolerance item.

## 4. Successor exciter columns
EX25FHE2-4 manufacturer drawing anchor:
- rearward depth approximately 25.5 +/-0.5 mm.

With mounting plane at approximately Z=8 mm:
- nominal rear extremity = Z 33.5 mm;
- drawing high-depth tolerance = Z 34.0 mm.

Add a minimum engineering non-contact allowance:
- 1.0 mm minimum local static clearance target.

Required clear rear volume at each exciter column therefore reaches approximately:
- **Z = 35.0 mm**.

This leaves only approximately:
- **5 mm to the 40 mm external rear plane**.

Conclusion:
**the four successor-exciter columns are full-depth exclusion columns.**

No MAIN PCB, daughterboard, bulk capacitor, structural cross-beam, wall-mount plate, insert, screw head or cable bundle may occupy these columns behind the exciters unless exact STEP geometry proves a dedicated recess/path.

## 5. Rear skin consequence
At exciter projections, the remaining 5 mm must accommodate:
- local air/assembly clearance;
- rear shell thickness;
- dimensional tolerance/warpage.

Initial rear-skin target in these regions:
- approximately 2.0..2.4 mm printed polymer;
- no thick structural rib directly behind the exciter.

This leaves approximately 2.6..3.0 mm nominal residual allowance from a 35 mm cleared exciter envelope to the 40 mm external plane.

This is tight but not geometrically impossible.

## 6. MAIN-P Z-stack
MAIN-P occupies an XY region clear of the four exciter columns:
- 115 x 45 mm;
- product X=105..220 mm;
- product Y=112..157 mm.

PCB stack target:
- PCB thickness: 1.6 mm nominal.

Board Z placement must be solved independently from the exciter mounting plane because it occupies free XY.

### Normal components
Most MAIN-P components are low-profile and can occupy a shallow electronics cavity.

### XAL7050
Body height:
- approximately 5.0 mm.

Reserve:
- 5.5 mm CAD envelope until STEP closure.

### EEU-FR1V471B bulk capacitor
Nominal:
- approximately 10 mm diameter x 16 mm body height.

Existing mechanical pocket:
- 12 x 12 x 19 mm.

This is the dominant MAIN-P component height.

Do not mount the 19 mm bulk pocket on a PCB plane that would place its top beyond the 40 mm rear envelope.

Preferred solution:
- orient component side toward the front/DML-side cavity where free XY permits;
- locally recess/step the carrier/frame around the capacitor;
- retain service/lead-form allowance.

A 19 mm component envelope plus 1.6 mm PCB can fit inside the available product depth in free XY, but only after exact board Z and rear-frame section are co-solved.

## 7. MAIN-C Z-stack
MAIN-C:
- 150 x 55 mm;
- product X=85..235 mm;
- product Y=315..370 mm.

Dominant known height:
- Ag53024 approximately 14 mm class;
- connector mating/service envelopes may exceed IC heights.

The upper-band board is free from exciter columns in the current coarse map.

Therefore the Ag53024 height is compatible in principle with 40 mm total depth, but:
- its exact STEP;
- RJ45 geometry;
- USB-C access;
- Micro-Fit mating volume;
- rear shell;
- frame beam;
must be solved together.

## 8. Daughterboards
VOICE, RADAR and ENV shall not be stacked directly behind exciter columns.

VOICE:
- preserve mechanical vibration isolation;
- no rigid bridge to DML.

RADAR:
- forward RF cone must remain free of carbon-filled polymer, metal and dense electronics.

ENV:
- preserve passive air chamber and thermal isolation.

The daughterboards use otherwise unused XY cavities rather than a second full-area electronics layer.

## 9. Rear structural frame update
The previous generic rear-frame concept remains valid only with explicit exciter tunnels.

Required topology:
- perimeter frame;
- local electronics carriers;
- bridges routed around the four full-depth exciter columns;
- no full-width rear deck;
- no transverse beam directly behind an exciter;
- local thin rear skin over exciter columns.

The frame shall use the MAIN-P and MAIN-C board edges as packaging boundaries, not cross through their tall-component service volumes.

## 10. Wall-mount consequence
The wall-mount interface cannot be treated as an unconstrained rear plate.

Avoid:
- full-area metal backing plate;
- fastener heads directly behind exciters;
- metal in ESP32 antenna forward/rear RF-sensitive region;
- metal/carbon structure in radar cone.

Use discrete structural load paths into perimeter/rear-frame nodes.

Exact wall-mount hardware remains a critical Z-stack release gate.

## 11. Worst-case depth classes

### Exciter column
Approximate:
- front treatment: 2 mm
- DML: 6 mm
- EX25FHE2-4 high tolerance: 26 mm
- clearance: 1 mm
= **35 mm**

Remaining to external rear plane:
= **5 mm**

### MAIN-P bulk region
Not additive to exciter depth because it is in different XY.

A 19 mm capacitor pocket + PCB + carrier can fit within a 40 mm local free-XY cavity if board plane is placed appropriately.

### MAIN-C Ag53024 region
Likewise independent of exciter Z. A ~14 mm module body is not by itself a 40 mm blocker.

## 12. Key conclusion
The correct packaging model is **2.5D**, not a single additive Z stack.

It is incorrect to calculate:
DML + exciter + PCB + capacitor + rear frame.

Those objects occupy different XY regions.

The actual limiting local column is currently the EX25FHE2-4:
- approximately 35 mm including front stack and 1 mm clearance;
- approximately 5 mm remains for rear-skin/tolerance.

Therefore:
**40 mm total product depth remains architecturally viable.**

But the margin at the exciter columns is small enough that the 40 mm target cannot be production-frozen until exact STEP-based shared CAD and print-tolerance analysis are complete.

## 13. CAD collision rules
Master CAD shall automatically fail if:
1. any object intersects the exact EX25FHE2-4 STEP envelopes;
2. rear skin enters the minimum exciter clearance;
3. any PCB/tall component exceeds Z=40 minus rear-skin allowance;
4. frame beams enter exciter columns;
5. wall-mount hardware enters exciter columns;
6. cables violate bend/terminal service volumes;
7. bulk capacitor pocket intersects DML/frame;
8. Ag53024/RJ45/USB mating volume exceeds rear envelope;
9. radar/ESP32 RF keep-outs are violated.

## 14. Release gates
1. import EX25FHE2-4 exact manufacturer STEP/drawing geometry;
2. freeze front fabric + adhesive thickness;
3. freeze PCB Z planes;
4. import Ag53024, RJ45, USB-C, Micro-Fit and bulk exact CAD;
5. define rear-skin local thickness map;
6. define wall-mount hardware;
7. run tolerance stack including print warpage;
8. run automatic collision solve;
9. validate structural frame FEA with exciter tunnels;
10. confirm no local point exceeds 40 mm.

Status: **EXCITER_COLUMN_Z35MM_CLASS / ~5MM_REAR_ALLOWANCE / 40MM_CONDITIONALLY_VIABLE**.
