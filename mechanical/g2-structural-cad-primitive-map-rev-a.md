# AudioPicture V2.2 Rev.A — G2 structural CAD primitive map

Status: **G2_PARAMETRIC_PRIMITIVES_DEFINED / KEEP_OUT_DRIVEN_BOOLEAN_BUILD_READY / FEA_SOLID_PENDING**

## 1. Objective
Translate the Rev.B rear-frame topology into dimensioned CAD primitives. All dimensions are seeds subject to exact STEP collision and FEA optimization.

## 2. Structural datum
PC-CF frame occupies only rear-cavity regions permitted by DML, PCB, RF, airflow, service and exciter keep-outs.

Baseline structural thickness parameters:
- wall 2.4 mm
- primary rib 2.8 mm
- mount rib 3.2 mm
- general root fillet >=1.5 mm
- mount root fillet >=2.0 mm
- outer ring nominal width 10 mm.

## 3. Outer ring primitive
Create closed rounded rectangular ring:
- external projected boundary follows inner product structural perimeter;
- nominal ring width 10 mm;
- local width allowed 8..16 mm;
- shell clearance is a separate parameter.

Primitive name:
FRAME_OUTER_RING_RAW

Boolean subtract all service/RF/exciter hard keep-outs only after load-node additions, then restore load continuity with explicit bridges.

## 4. Upper mount islands
LEFT_CLEAT_ISLAND:
- seed X 25..80
- seed Y 344..388
- local reinforcement thickness/depth determined by available Z.

RIGHT_CLEAT_ISLAND:
- seed X 240..295
- seed Y 344..388.

Each island contains two M4 boss primitives.

Boss seed:
- OD 11 mm
- local OD sweep 11/12/13 mm
- engagement >=7 mm where Z allows
- root fillet >=2 mm.

Boss centers remain parametric until exact cleat-hole pitch is frozen.

## 5. Side load rails
LEFT_RAIL_RAW:
- nominal projected corridor X 24..46
- segmented around service/geometry constraints
- ties left cleat island to lower outer ring.

RIGHT_RAIL_RAW:
- nominal projected corridor X 294..310
- locally shift inward only if radar/ENV/RF keep-outs permit
- ties right cleat island to lower outer ring.

Rails are ribbed/open sections, not solid bars.

## 6. Upper bridge
Create an upper structural bridge around MAIN-C without covering its rear service area.

Preferred topology:
- outer top ring carries left-right global load;
- local gussets descend beside MAIN-C;
- no full shelf over MAIN-C.

MAIN-C projected box:
X85..235 Y315..370.

Required clear volumes:
- RJ45 plug/latch at lower C1;
- Ag53024 rear-top clearance;
- ESP32 antenna region;
- upper thermal outlet.

## 7. Mid bridges
Exciter keep-outs:
- L2 X83..145 Y166..226
- R1 X175..237 Y238..298.

Use central free corridor between their projected edges.

MID_BRIDGE_A seed:
- connects left structural network toward central zone below/around L2;
- does not cross L2.

MID_BRIDGE_B seed:
- connects central zone toward right structural network below/around R1;
- does not cross R1.

No continuous horizontal bridge is allowed across the chimney.

Prefer diagonal/open-web geometry.

## 8. Lower structural bridge
Lower obstacles:
- L1 X37..99 Y50..110
- R2 X223..285 Y88..148
- VOICE X119..201 Y20..102
- service recess X100..220 Y20..48
- ENV X252..294 Y35..59.

LOWER_BRIDGE_RAW shall use perimeter continuity plus local arches/gussets rather than a straight full-width beam.

Critical rule:
the lower airflow inlet remains open and >=600 mm2 effective with cables installed.

## 9. MAIN-C carrier primitives
Use 3 or 4 isolated standoff islands.

No continuous shelf.

Each standoff:
- local pad;
- screw/retention boss;
- root gusset into nearest structural rail/ring.

Placement is driven by final PCB mounting holes.

Do not place standoffs:
- inside ESP32 antenna keep-out;
- under RJ45 latch sweep;
- above/below Ag53024 service volume where removal is blocked.

## 10. MAIN-P carrier primitives
Use local standoffs/short rails only.

Reserve:
- horizontal 470 uF cradle;
- XAL7050/output area airflow;
- JCP/JCS bend volume;
- speaker harness exits.

No closed tray beneath/above MAIN-P.

## 11. VOICE carrier anchor primitives
Create 3 or 4 small structural anchor islands around VOICE carrier perimeter.

They terminate before compliant isolation elements.

No rigid PC-CF cross-member runs beneath the four-microphone square.

## 12. RADAR frame truncation
Create RADAR_RF_KO before right-side frame boolean.

All PC-CF geometry intersecting the forward radar RF keep-out is removed.

Restore structural continuity around the cone using rear/side route only.

Never restore material through the RF cone during automatic healing.

## 13. ENV thermal break
ENV supports use narrow necks/minimal section.

Do not directly connect SHT45 chamber wall to a broad PC-CF thermal mass.

ENV support is not a primary structural bridge.

## 14. Lower service reinforcement
Service recess:
X100..220 Y20..48 rear region.

Create:
- left jamb;
- right jamb;
- upper arch/bridge;
- corner radii;
- local gussets into outer ring.

No sharp rectangular notch.

The service reinforcement shall not become a wall across the lower inlet.

## 15. Lower supports
Create two wall support pad nodes on structurally continuous regions near lower left/right perimeter.

Nominal stand-off:
4 mm.

Exact pad centers are solved after lower inlet/service geometry.

Pads are secondary supports and are not credited as nominal vertical-load anchors.

## 16. Anti-lift node
Create one reinforced PC-CF node in lower region, independent of ASA shell.

Load contract:
50 N upward.

The anti-lift feature shall tie into outer ring plus at least one local rib/gusset.

## 17. Boolean build order
1. create master datums;
2. create FRAME_OUTER_RING_RAW;
3. create cleat islands/boss raw solids;
4. create side rails;
5. create mid/lower bridge raw solids;
6. fuse structural raw solids;
7. subtract EX25FHE2 keep-outs;
8. subtract PCB/service removal keep-outs;
9. subtract ESP32/RADAR RF keep-outs;
10. subtract airflow hard corridors;
11. subtract Ethernet/service sweeps;
12. inspect connectivity;
13. add only explicit legal restoration bridges;
14. add carrier islands;
15. add lower supports/anti-lift;
16. apply gussets;
17. apply fillets last;
18. run geometry validation;
19. compute mass;
20. export FEA solid.

## 18. Connectivity assertions
After all booleans:
- one connected primary PC-CF structural body is preferred;
- both upper cleat islands connect to outer ring;
- each cleat has >=2 independent local rib/gusset paths;
- anti-lift connects to primary frame;
- no bridge enters an exciter keep-out;
- no bridge crosses radar RF cone;
- no bridge creates a full-width airflow barrier.

## 19. Material/process
Baseline material remains Prusament PC Blend Carbon Fiber or qualified equivalent.

Manufacturer documentation supports:
- carbon-fiber-filled PC Blend;
- high dimensional stability;
- high temperature resistance up to approximately 114 C;
- hardened nozzle requirement.

These manufacturer claims do not replace coupon-derived orthotropic FEA properties.

## 20. G2 dimensional audit
With current G1 boxes:
- left rail X24..46 touches/approaches L1 X37..99 in Y50..110, therefore the rail must route on outer-perimeter side of L1 or locally narrow/offset;
- right rail X294..310 is outside R2 max X285 and ENV max X294, giving only boundary-class clearance near ENV;
- MAIN-C leaves outer-ring paths on both sides;
- central region between L2 max X145 and R1 min X175 provides approximately 30 mm projected X corridor where their Y ranges overlap only partially;
- lower region is dominated by VOICE/service opening, so load continuity must remain perimeter-led rather than a central lower spine.

This confirms the dual-side/perimeter topology and rejects a naive straight central spine.

## 21. New automatic checks
C121 primary PC-CF body connectivity valid.
C122 left rail routes legally around L1.
C123 right rail clears ENV thermal chamber.
C124 both cleat islands connect through two local load paths.
C125 no bridge intersects any EX25FHE2 keep-out.
C126 no structural restoration enters radar RF keep-out.
C127 MAIN-C rear service volumes remain open.
C128 MAIN-P thermal surfaces remain open.
C129 lower service reinforcement preserves inlet area.
C130 anti-lift node connects to primary PC-CF body.
C131 structural fillets do not grow into hard keep-outs.
C132 frame mass computed before FEA.
C133 FEA export is watertight/manifold.
C134 structural body stays within product Z envelope.
C135 no full-width rib blocks bottom-to-top chimney.

## 22. G2 release gate
G2-PRIMITIVES: **PASS when generated from this map**
G2-COLLISION: requires exact manufacturer solids
G2-FEA: requires watertight solid and coupon sensitivity model
G2-RELEASE: requires final FEA/CFD/RF/service passes.

Status: **OUTER_RING_10MM / LEFT_RIGHT_RAILS / OPEN_WEB_BRIDGES / M4_BOSS_11MM_SEED / C01_TO_C135 / CENTRAL_SPINE_REJECTED**.
