# AudioPicture V2.2 Rev.B — keep-out-driven rear structural frame

Status: **KEEP_OUT_DRIVEN_FRAME_TOPOLOGY_DEFINED / 70N_FEA_AND_SHARED_CAD_RELEASE_GATE**

## 1. Purpose
Define the load-bearing PC-CF rear frame after the first complete DMU packing pass.

The frame is generated around:
- DML perimeter;
- four EX25FHE2-4 columns;
- MAIN-P;
- MAIN-C;
- VOICE;
- RADAR;
- ENV;
- ESP32 RF keep-out;
- radar RF cone;
- passive thermal chimney;
- Ethernet tunnel;
- cable/FPC corridors;
- upper wall cleats;
- lower supports;
- connection/service exit.

The frame is not a full rear plate.

## 2. Structural load path
Primary load path:
**DML/product mass -> PC-CF perimeter/frame -> upper M4 mount nodes -> aluminum cleats -> wall**

Secondary load paths:
- lower pads resist rotation/wall-normal motion;
- anti-lift prevents upward disengagement;
- local carriers support PCBs without becoming primary DML supports.

The DML compliant perimeter is not a structural shortcut.

## 3. Material
Baseline:
**PC-CF structural frame**

Initial printable geometry:
- general wall: 2.4 mm;
- primary rib: 2.8 mm seed;
- local mount rib/gusset: 3.0..3.6 mm seed;
- minimum root fillet: 1.5 mm general;
- mount-node root fillet: >=2.0 mm.

Final thicknesses are FEA/process outputs.

## 4. Outer structural ring
Create a closed PC-CF perimeter ring inside the cosmetic ASA shell.

Projected ring width seed:
**10 mm nominal**

Local range:
- 8 mm where packaging is tight;
- 12..16 mm around mount/load nodes.

The ring shall remain continuous around connection/service cutouts using local bridges/gussets.

Do not rely on ASA rear shell to close the primary structural load path.

## 5. DML support ring
Inside the structural ring create the DML support/hard-stop geometry.

Requirements:
- PORON compliant perimeter remains continuous;
- hard stop controls maximum compression;
- hidden safety capture does not hard-preload DML;
- frame does not bridge directly onto active panel surface.

This ring remains mechanically distinct from electronics carriers.

## 6. Upper cleat nodes
Two independent upper structural islands tie into the outer ring.

LEFT mount node seed:
- X approximately 30..75 mm
- Y approximately 350..382 mm

RIGHT mount node seed:
- X approximately 245..290 mm
- Y approximately 350..382 mm

Each supports:
- one ~50 mm class aluminum cleat;
- two M4 x 0.7 fasteners;
- two M4 heat-set inserts.

Boss seed:
- OD >=11 mm;
- engagement depth >=7 mm where Z allows;
- root fillet >=2 mm;
- each boss tied into at least two ribs/gussets.

Exact Y placement shall avoid MAIN-C connector/service volumes and ESP32 RF keep-out.

## 7. Primary vertical rails
Use two discontinuous-but-load-connected vertical structural rails rather than one central full-height spine.

### LEFT STRUCTURAL RAIL
Seed corridor:
- X approximately 25..45 mm where free.

Functions:
- connect left upper mount node to lower perimeter;
- support left shell;
- bypass L1 using perimeter path.

### RIGHT STRUCTURAL RAIL
Seed corridor:
- X approximately 300-side inner perimeter, shifted inward only where RF allows.

Functions:
- connect right mount node to lower perimeter;
- support right shell.

The right rail shall not enter:
- radar forward RF cone;
- ENV room-air chamber;
- ESP32 antenna keep-out.

## 8. Central load bridges
Because exciter columns and electronics prevent full straight rails, use local diagonal/curved bridges.

Preferred topology:
- upper left mount -> upper perimeter -> left rail;
- upper right mount -> upper perimeter -> right rail;
- local inward gussets around MAIN-C edges;
- mid-height bridges routed between L2/R1 exclusion regions;
- lower bridges routed around MAIN-P/VOICE/service zones.

No bridge may cross an exciter column.

## 9. MAIN-C carrier
MAIN-C carrier is attached to frame at multiple local standoffs.

Requirements:
- support 150 x 55 board;
- avoid Ag53024 top clearance;
- avoid RJ45 plug/latch/service sweep;
- avoid ESP32 RF zone;
- preserve upper exhaust.

Use 3 or 4 local mounting points rather than a continuous shelf.

No full-width carrier plate.

## 10. MAIN-P carrier
MAIN-P carrier:
- supports 115 x 45 board;
- keeps horizontal 470 uF retention cradle;
- provides thermal/open-air access;
- supports JCP/JCS strain relief;
- does not obstruct speaker harness exits.

Use local standoffs and short rails.

Do not create a closed thermal box around MAIN-P.

## 11. VOICE carrier interface
VOICE remains vibration isolated.

Frame provides only isolated carrier anchor islands.

Between frame and VOICE carrier use compliant isolation elements.

No rigid continuous PC-CF bridge directly beneath microphone array.

The carrier must not become a DML hard stop.

## 12. RADAR carrier interface
Radar forward region uses non-conductive unfilled polymer where required.

PC-CF frame terminates outside the RF cone.

Radar carrier may attach to frame from rear/side using geometry that does not project into forward cone.

## 13. ENV carrier interface
ENV carrier is thermally isolated from the structural frame.

Use minimal cross-section support and low-conductance interface where practical.

SHT45 chamber remains coupled to room air, not frame temperature.

## 14. Thermal chimney
Frame topology shall create a vertical open-flow network.

Rules:
- no full-width horizontal rib;
- bridges use local openings;
- harness clips stay at sides;
- upper exhaust path remains open;
- lower inlet remains >=600 mm2 effective after installed cables.

Primary chimney corridor shall remain connected bottom-to-top.

## 15. Ethernet tunnel
The Ethernet cable route is not a structural rail.

Frame provides:
- local guide clips;
- radiused pass-throughs;
- anti-rattle support.

Do not close the route into a stiff full-length conduit that blocks convection.

RJ45 plug/latch swept volume is a hard keep-out.

## 16. Lower service opening
Connection/service recess cuts the lower rear shell/frame region.

Compensate structurally with:
- radiused opening corners;
- side rails;
- upper local bridge;
- gussets into outer ring.

No sharp internal corners.

The lower opening is explicitly included in torsion and wall-normal FEA.

## 17. Lower supports
Two lower wall-contact/support pads tie into outer structural ring.

They:
- stabilize product against wall;
- set nominal wall gap;
- provide anti-rocking support;
- are not the primary vertical load path.

Nominal wall stand-off:
**4 mm CFD seed**

Pads use compliant contact layer where needed.

## 18. Anti-lift
Hidden M4 anti-lift feature ties into a reinforced lower structural node.

It shall withstand the frozen **50 N upward** FEA load case.

Do not attach anti-lift only to ASA shell.

## 19. Rear shell relationship
ASA shell:
- cosmetic;
- airflow shaping;
- cable recess;
- dust/labyrinth features.

PC-CF:
- structural.

Use local snap/screw interfaces that permit differential thermal/print tolerance without forcing shell warpage into DML.

## 20. Exciter rear zones
For each EX25FHE2-4:
- no PC-CF rib in exact projection;
- no rear-shell thickening into Z clearance;
- no harness clip above rear cap;
- maintain >=1 mm rigid static clearance target after tolerance stack where feasible.

These remain four structural holes in the frame topology.

## 21. FEA model
Use the existing wall-mount FEA contract.

Mandatory load cases:
- LC1 70 N symmetric vertical;
- LC2 70 N single upper cleat, left and right;
- LC3 50 N wall-normal pull;
- LC4 30 N corner/torsion;
- LC5 100 N installation seating;
- LC6 50 N anti-lift upward;
- LC7 print warp/assembly preload.

Include:
- connection/service opening;
- PCB carrier cutouts;
- exciter holes;
- upper mount bosses;
- lower support nodes.

## 22. FEA optimization variables
Optimize in this order:
1. fillet radius;
2. local gusset;
3. local rib depth;
4. print orientation/toolpath strategy;
5. boss material;
6. bridge position;
7. global ring width/thickness last.

Do not solve a local stress concentration by globally thickening the frame unless required.

## 23. Print architecture
Frame may be:
A. one-piece PC-CF print if machine envelope/process permits; or
B. mechanically joined structural subframes.

One-piece is preferred for first structural model.

If segmented:
- joints become explicit FEA/contact/fastener interfaces;
- adhesive-only structural joints are not baseline.

## 24. Mass target
Existing frame budget:
~220 g nominal.

Rev.B structural target:
**<=250 g before inserts/metal cleats**

If FEA drives above 250 g:
- topology must be reviewed before accepting mass increase.

## 25. DMU checks
Add:
C65 outer structural ring continuous.
C66 no frame enters exciter columns.
C67 left cleat node has two independent rib/gusset load paths.
C68 right cleat node has two independent rib/gusset load paths.
C69 MAIN-C carrier does not block exhaust/RJ45 service.
C70 MAIN-P carrier does not enclose thermal source.
C71 VOICE carrier remains compliant-isolated.
C72 radar cone contains no PC-CF.
C73 ENV chamber has no high-conductance frame bridge.
C74 chimney connected bottom-to-top.
C75 Ethernet tunnel remains serviceable.
C76 lower service cutout has radiused structural reinforcement.
C77 anti-lift attaches to PC-CF load node.
C78 lower supports set 4 mm nominal wall gap.
C79 rear shell not credited as sole structural path.
C80 frame mass <=250 g target.

## 26. CAD generation order
1. instantiate external product envelope;
2. import DML and exact exciter keep-outs;
3. import all PCB envelopes;
4. import RF/airflow/service keep-outs;
5. generate outer structural ring;
6. create upper cleat islands;
7. create left/right vertical load rails;
8. route bridges around keep-outs;
9. create PCB carrier islands;
10. create lower service reinforcement;
11. add lower supports/anti-lift;
12. fillet/gusset;
13. run C01..C80;
14. mesh FEA;
15. optimize locally.

## 27. Release gates
- exact EX25FHE2 STEP;
- exact PCB/component solids;
- exact cleat coordinates;
- PC-CF coupon-derived orthotropic properties;
- shared CAD collision pass;
- FEA convergence;
- LC1..LC7 margins;
- thermal CFD;
- vibration/acoustic coupling check;
- print-process qualification.

Status: **CLOSED_OUTER_RING / DUAL_SIDE_LOAD_RAILS / LOCAL_BRIDGES / NO_FULL_REAR_DECK / FRAME_MASS_TARGET_LE_250G**.
