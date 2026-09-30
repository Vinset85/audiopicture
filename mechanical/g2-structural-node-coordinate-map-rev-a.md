# AudioPicture V2.2 Rev.A — G2 structural node coordinate map

Status: **G2_STRUCTURAL_NODE_SEEDS_FROZEN / CLEAT_HOLE_PITCH_PARAMETRIC / FEA_SOLID_GENERATION_READY**

## 1. Coordinate convention
Product coordinates:
- origin front lower-left;
- +X right;
- +Y up;
- +Z toward wall.

All structural node coordinates below are projected XY center coordinates. Z is derived from the local rear-frame section and mount-interface stack.

## 2. Upper cleat reference centers
Freeze symmetric cleat center seeds:
- CLEAT_L_C = (52.5, 366.0) mm
- CLEAT_R_C = (267.5, 366.0) mm

These lie inside the previously reserved cleat regions and maintain symmetry about X=160 mm.

Cleat nominal length remains 50 mm class.

## 3. M4 boss parametrization
Do not freeze commercial cleat hole pitch before exact cleat drawing/part selection.

Define:
- CLEAT_HOLE_PITCH = P_CLEAT
- seed P_CLEAT = 30 mm
- allowed design sweep initially 26..36 mm.

Boss centers are generated symmetrically about each cleat center along X.

LEFT:
- UL1 = (52.5 - P_CLEAT/2, 366.0)
- UL2 = (52.5 + P_CLEAT/2, 366.0)

At 30 mm seed:
- UL1 = (37.5, 366.0)
- UL2 = (67.5, 366.0)

RIGHT:
- UR1 = (267.5 - P_CLEAT/2, 366.0)
- UR2 = (267.5 + P_CLEAT/2, 366.0)

At 30 mm seed:
- UR1 = (252.5, 366.0)
- UR2 = (282.5, 366.0)

Boss:
- M4 x 0.7
- OD 11 mm seed
- OD sweep 11/12/13 mm
- engagement >=7 mm where Z permits
- root fillet >=2 mm.

## 4. Cleat load-spreader islands
Each two-boss pair sits on a local PC-CF island.

Seed projected island:
- length X = P_CLEAT + 24 mm
- height Y = 28 mm.

At P_CLEAT=30:
- island length approximately 54 mm.

LEFT island seed:
- X25.5..79.5
- Y352..380

RIGHT island seed:
- X240.5..294.5
- Y352..380.

Clip to legal outer-ring/product keep-outs in CAD rather than expanding outside the frame.

## 5. Boss load paths
Each boss requires two local load directions:
A. outward/perimeter path;
B. inward/diagonal gusset path.

No boss may depend on a single narrow neck.

Seed gusset centerline directions:
- UL1: left/down + inward/down
- UL2: upper/perimeter + inward/down
- UR1: upper/perimeter + inward/down
- UR2: right/down + inward/down.

Exact curves avoid MAIN-C and RF/service keep-outs.

## 6. Lower wall-support centers
Freeze initial symmetric lower support seeds:
- LOWER_PAD_L = (45, 28) mm
- LOWER_PAD_R = (275, 28) mm

Rationale:
- far outside the central service recess X100..220;
- away from VOICE X119..201;
- left pad below/left of L1;
- right pad outside ENV X252..294 in Y, but exact ENV air-chamber sweep must be checked;
- maximize anti-rocking baseline.

Nominal wall gap:
- 4 mm.

Pad projected seed:
- 18 x 12 mm.

Compliant contact layer:
- 1..2 mm class, exact material open.

## 7. Lower-pad structural connection
LOWER_PAD_L connects to lower/left outer ring.
LOWER_PAD_R connects to lower/right outer ring.

Pads are not credited as primary vertical load anchors.

FEA:
- wall-normal contact;
- limited/no vertical friction credit in baseline;
- reaction recorded separately.

## 8. Anti-lift node
Freeze initial anti-lift center:
- ANTILIFT_C = (160, 18) mm.

This is centered below the service recess and avoids placing anti-lift on either RF-sensitive side.

However, service recess occupies X100..220/Y20..48.

Therefore anti-lift mechanism must engage from below and tie structurally into a reinforced bridge beneath/around the recess, without blocking cable exit.

Seed anti-lift structural node:
- center X160
- local Y12..24 region
- M4 x 0.7.

Load:
- 50 N upward.

Service access must remain possible after wall installation.

## 9. Anti-lift reinforcement
Create a shallow U-shaped load path around the central lower opening:
- left leg ties toward X~95;
- right leg ties toward X~225;
- lower cross-member remains outside/under the service opening;
- upper opening remains clear for cables/air.

Do not create a solid horizontal wall.

Use open-web ribs and inlet perforation/opening continuity.

## 10. Left rail waypoint seeds
Because L1 blocks a straight rail, define centerline waypoints:
- LL0 = (34, 352)
- LL1 = (30, 235)
- LL2 = (27, 125)
- LL3 = (24, 112)
- LL4 = (24, 45)
- LL5 = (45, 28)

The rail remains perimeter-side of L1 X37..99/Y50..110.

These are spline/polyline control seeds, not final wall surfaces.

## 11. Right rail waypoint seeds
ENV reaches X294 and R2 reaches X285.

Use outer-perimeter-biased route:
- RR0 = (286, 352)
- RR1 = (300, 300)
- RR2 = (303, 225)
- RR3 = (305, 155)
- RR4 = (306, 75)
- RR5 = (300, 62)
- RR6 = (296, 30)
- RR7 = (275, 28)

The route stays near the outer perimeter and must be clipped against shell clearance.

Exact radar RF cone subtraction remains authoritative.

## 12. Mid open-web bridge seeds
Avoid a single horizontal rib.

Bridge network seed:

B1:
- from left rail near (30,235)
- toward central lower-L2 region around (155,230).

B2:
- from central region around (155,230)
- toward right rail around (300,225).

Because R1 occupies X175..237/Y238..298, B2 remains at/below its lower edge.

B3:
- diagonal from central region around (155,230)
- toward MAIN-P-side lower structural region around (205,165), clipped around MAIN-P and R2.

These are load-path seeds only; hard keep-outs subtract final geometry.

## 13. Lower open-web bridge seeds
Use perimeter-led split bridges:

LB1:
- left lower ring near (24,45)
- toward service-left jamb near (95,55).

LB2:
- service-right jamb near (225,55)
- toward right lower ring near (296,60).

No structural member crosses the service opening X100..220/Y20..48 as a solid wall.

Anti-lift U-path is separate and perforated/open.

## 14. Rib section seeds
Primary side rail:
- web thickness 2.8 mm
- local rib depth determined by available Z;
- seed structural depth 8 mm where packaging allows.

Open-web bridges:
- web thickness 2.8 mm
- seed depth 6 mm.

Cleat gussets:
- 3.2 mm web
- seed depth 8..10 mm where Z permits.

Lower service reinforcement:
- 2.8 mm web
- seed depth 6..8 mm.

All depths are measured in local Z structural extent and are clipped by component/service keep-outs.

## 15. Section optimization sweeps
For FEA:
- rail web: 2.4 / 2.8 / 3.2 mm
- bridge web: 2.4 / 2.8 / 3.2 mm
- gusset web: 3.0 / 3.2 / 3.6 mm
- rail depth: 6 / 8 / 10 mm
- bridge depth: 5 / 6 / 8 mm
- mount fillet: 2 / 3 / 4 mm.

Do not globally thicken all members in one step.

## 16. Z rules
No structural primitive may exceed:
- product rear envelope Z40;
- rear-shell inner allowance;
- exact component keep-outs.

Exciter columns remain no-rib zones to approximately Z35.

Mount nodes may use deeper local Z only where no PCB/service/RF conflict exists.

## 17. FEA load application nodes
Named interfaces:
- BC_CLEAT_L_UL1
- BC_CLEAT_L_UL2
- BC_CLEAT_R_UR1
- BC_CLEAT_R_UR2
- CONTACT_LOWER_PAD_L
- CONTACT_LOWER_PAD_R
- BC_ANTILIFT

This permits independent LC2 left/right single-cleat analysis.

## 18. Tolerance seeds
Before process capability data:
- printed frame XY dimensional tolerance seed +/-0.30 mm local;
- critical boss position seed +/-0.20 mm after calibrated process;
- insert bore/feature compensated by print coupon;
- shell-to-frame clearance seed 0.4..0.6 mm where non-precision cosmetic fit;
- rigid component static clearance target >=1.0 mm where feasible.

These are CAD/process seeds, not released manufacturing tolerances.

## 19. Collision observations
At current coarse geometry:
- UL1/UL2 remain outside MAIN-C X85..235;
- UR1/UR2 remain to the right of MAIN-C X235, but right cleat island approaches C3/ESP32 RF region and must be RF-clipped;
- lower pads are outside central service recess;
- left rail waypoint route avoids L1 by staying X<=~30 through its Y band;
- right rail route uses X~300+ through ENV/R2 bands and therefore relies on the outer perimeter strip;
- anti-lift centered at X160 requires a shaped U-path around the service recess rather than a solid boss bridge.

## 20. Automatic checks
C136 cleat centers symmetric about X160.
C137 boss pitch parameter changes without topology failure.
C138 all four M4 boss circles stay inside legal reinforced islands.
C139 left boss pair clears MAIN-C.
C140 right boss pair clears MAIN-C and RF keep-out after clipping.
C141 lower pads clear service recess.
C142 left lower pad clears L1 hard keep-out.
C143 right lower pad does not obstruct ENV room-air path.
C144 anti-lift service path remains accessible.
C145 anti-lift reinforcement preserves cable exit.
C146 left rail remains perimeter-side of L1.
C147 right rail remains outside R2 and radar RF keep-out.
C148 bridge B1/B2/B3 survive keep-out subtraction as connected load paths.
C149 lower bridges preserve effective inlet.
C150 rib section sweep remains inside 40 mm product envelope.
C151 each cleat boss has two local load paths.
C152 FEA named interfaces generated.
C153 tolerance offsets do not create exciter collision.
C154 exact cleat hole pitch can replace seed parametrically.
C155 no lower support is credited as primary vertical anchor.

## 21. G2 state
Node coordinates: **SEED FROZEN**
Cleat hole pitch: **PARAMETRIC, 30 mm seed**
Boss OD: **11 mm seed**
Lower supports: **(45,28) and (275,28)**
Anti-lift: **X160 lower-center architecture**
Side-rail waypoint topology: **DEFINED**
Bridge centerline topology: **DEFINED**
Section sweeps: **DEFINED**

Next release action is to generate the watertight PC-CF frame solid from these primitives and run geometry/connectivity/mass checks before structural FEA.

Status: **G2_NODE_MAP_READY / 4X_M4_BOSSES / LOWER_PADS_230MM_SPAN / CENTRAL_ANTILIFT_U_PATH / C01_TO_C155**.
