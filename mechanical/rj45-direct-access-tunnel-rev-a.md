# AudioPicture V2.2 Rev.A — RJ45 direct-access tunnel

Status: **RJ45_DIRECT_TO_MAIN_C_ARCHITECTURE_FROZEN / DOWNWARD_CABLE_TUNNEL_BASELINE / EXACT_JACK_PLUG_CAD_GATE**

## 1. Decision
Keep the Ethernet RJ45 electrically and mechanically on MAIN-C.

Do not use:
- a remote passive RJ45 daughterboard;
- a long internal raw-MDI harness;
- a proprietary Ethernet extension.

The external Ethernet plug mates directly with the MAIN-C RJ45.

The enclosure provides a passive cable-access tunnel from the jack to the lower/rear cable exit.

## 2. MAIN-C geometry
MAIN-C:
- X=85..235 mm
- Y=315..370 mm
- PCB Z=17.0..18.6 mm.

C1 Ethernet/PoE region:
- local X=0..55 mm;
- product X=85..140 mm.

Preferred RJ45 location:
**lower edge of C1**, approximately product X=95..125 mm, near Y=315 mm.

Preferred mating direction:
**downward in product Y**.

This allows the plug/cable to travel toward the lower product edge without crossing the ESP32 RF region on the right.

## 3. Why downward
Rejected baseline directions:

### Rearward
A plug inserted toward the wall consumes wall gap/depth and conflicts with the 40 mm shallow installation.

### Rightward
Moves plug/cable toward ESP32 RF-clean region and upper/right electronics.

### Leftward
Approaches structural perimeter and upper-left mount region and gives poor route to lower cable exit.

### Upward
Approaches upper cleats/outlet and traps cable at top.

Preferred:
**downward**, parallel to product plane.

## 4. Cable tunnel
Create:
**ETH_DIRECT_TUNNEL**

Seed center corridor:
- X approximately 95..130 mm;
- from Y approximately 315 mm downward toward lower cable exit;
- Z in rear service layer, nominally approximately 22..36 mm where geometry permits.

The tunnel is not a sealed tube.

It is a guided open/recessed corridor using clips, ribs and shell geometry.

## 5. Exciter avoidance
The downward path encounters the L2/L1 side of the product if routed as a straight line.

Therefore it shall not remain at one X coordinate for the full height.

Use staged path:
1. depart RJ45 downward;
2. shift toward central corridor above L2;
3. descend between left/right exciter exclusions;
4. shift toward lower connection/cable exit region below MAIN-P/VOICE constraints.

Exact swept spline/polyline shall be solved in CAD.

No cable or plug boot may enter:
- L2 exclusion X83..145/Y166..226;
- L1 exclusion X37..99/Y50..110;
- MAIN-P body X105..220/Y112..157.

## 6. Preferred macro route
Initial routing waypoints, centerline seeds:
- P0 RJ45 exit: approximately (110,315)
- P1: approximately (155,300)
- P2: approximately (155,235)
- P3: approximately (160,165)
- P4: approximately (105,105)
- P5 lower cable exit: approximately (105,45)

These are routing seeds only.

They intentionally use the central free corridors around the coarse exciter boxes.

CAD shall replace them with smooth bend-compatible geometry.

## 7. Cable construction assumption
Target ordinary flexible Cat5e/Cat6 patch cable.

Do not freeze a universal minimum bend radius because cable OD and construction vary.

CAD shall model at least:
- representative slim patch cable;
- representative conventional molded-boot patch cable.

Product compatibility statement shall ultimately be based on the validated cable envelope.

## 8. RJ45 latch access
The user/installer must be able to release the latch.

Provide one of:
- finger-access slot if geometry permits;
- guided narrow tool-access feature;
- latch-facing orientation into accessible recess.

Do not create a connector that can be inserted but not removed after wall mounting.

## 9. Tunnel structure
Tunnel side rails may be ASA/PC-CF where allowed.

Do not:
- create a full-width horizontal wall;
- block chimney;
- place conductive material in ESP32/radar RF keep-outs.

Use local cable clips rather than continuous closed conduit.

## 10. Thermal relationship
Ethernet cable may pass through the rear cavity but shall stay outside the central highest-velocity chimney core where possible.

Cable routing shall not reduce effective lower inlet below 600 mm2.

CFD includes installed Ethernet and 24 V cables.

## 11. Connection-bay update
The previous lower connection bay is reinterpreted as:
**LOWER CABLE EXIT / SERVICE RECESS**, not a requirement that every electrical connector physically resides there.

Ethernet:
- connector remains MAIN-C;
- cable traverses internal rear tunnel;
- cable exits at lower recess.

24 V:
- may use short internal harness from lower recess to MAIN-P if required.

USB:
- preferably direct service tunnel to MAIN-C; exact service aperture may be separate.

This avoids unnecessary signal extensions.

## 12. Wall mounting
The Ethernet cable tunnel must remain serviceable with product on wall where practical.

Installation sequence baseline:
1. connect Ethernet/24 V in rear recess/tunnel access;
2. route cables into clips;
3. seat product onto upper cleats;
4. verify lower cable exit is not pinched;
5. engage anti-lift.

Alternative pre-connect-before-hang procedure is acceptable if removal remains straightforward.

## 13. Rear-shell cable exit
Lower exit shall:
- face downward/rearward;
- have radiused edges;
- provide cable strain/bend support;
- avoid SHT45 chamber;
- preserve inlet free area;
- prevent cable pinch against wall.

No sharp 90-degree cable turn.

## 14. EMI
Because RJ45 remains adjacent to magnetics on MAIN-C:
- MDI routing stays local;
- shield/ground strategy remains local;
- external cable is post-connector, as intended.

This is preferred over a remote jack.

Keep the external cable route away from:
- VOICE microphone electronics;
- speaker BTL harness;
- radar RF cone;
- ESP32 antenna.

## 15. DMU checks
Add:
C55 RJ45 plug mates directly to MAIN-C without remote MDI.
C56 plug insertion swept volume clears frame/shell.
C57 latch can be released.
C58 Ethernet cable swept volume clears all exciter columns.
C59 cable clears MAIN-P and VOICE carrier.
C60 cable route does not enter ESP32 keep-out.
C61 cable route does not enter radar RF cone.
C62 cable does not obstruct >20 percent local chimney section.
C63 lower exit preserves >=600 mm2 effective inlet.
C64 wall installation does not pinch Ethernet cable.

## 16. CAD parameters
- RJ45_LOCATION_SEED = MAIN_C_C1_LOWER_EDGE
- RJ45_PRODUCT_X_SEED = 110 mm
- RJ45_PRODUCT_Y_SEED = 315 mm
- RJ45_MATING_DIRECTION = DOWNWARD_Y
- ETH_TUNNEL_Z_SEED = 22..36 mm
- ETH_REMOTE_MDI = PROHIBITED_BASELINE
- LOWER_CONNECTION_BAY_ROLE = CABLE_EXIT_SERVICE_RECESS

## 17. Release gates
1. exact TE 2-1734264-1 STEP/drawing;
2. exact jack mating direction from footprint/CAD;
3. standard plug + molded boot solid;
4. representative cable bend model;
5. solve route against exact EX25FHE2 STEP;
6. solve latch access;
7. solve wall-install sequence;
8. CFD with cable installed;
9. structural check of tunnel rails;
10. update MAIN-C native PCB connector placement.

Status: **RJ45_ON_MAIN_C / DOWNWARD_DIRECT_MATING / PASSIVE_REAR_CABLE_TUNNEL / LOWER_RECESS_AS_CABLE_EXIT**.
