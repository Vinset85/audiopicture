# AudioPicture V2.2 Rev.A — recessed connection bay

Status: **LOWER_LEFT_CONNECTION_BAY_BASELINE_DEFINED / CONNECTOR_EXACT_CAD_AND_CABLE_BEND_RELEASE_GATE**

## 1. Purpose
Define one recessed service/connection bay for:
- Ethernet;
- external 24 V DC;
- USB-C service/recovery.

The bay shall preserve:
- 320 x 400 x 40 mm product envelope;
- wall-mounted cable access;
- passive lower intake;
- VOICE board;
- ENV chamber;
- exciter exclusion columns;
- wall-mount structure.

## 2. Placement decision
Place the connection bay in the **lower-left / lower-center rear edge region**.

Avoid lower-right because:
- ENV PCB and SHT45 room-air chamber occupy the lower-right region;
- radar/right-side FPC corridor is reserved;
- environmental sensing must remain isolated from cable/connector thermal disturbance.

Avoid the extreme left L1 exciter projection.

Initial product-space bay seed:
- **X = 100..220 mm**
- **Y = 20..48 mm**
- rear-access/service volume toward Z rear shell.

Nominal projected bay:
**120 x 28 mm**

This sits below MAIN-P (Y112..157), below its electronics and between the lower exciter constraints.

Exact connector positions are solved inside this bay.

## 3. Relationship to VOICE
VOICE PCB:
- X119..201
- Y20..102
- Z12..13.6.

The bay overlaps VOICE in XY, therefore it shall not be a full-depth rectangular cavity.

Architecture:
- VOICE occupies front Z;
- connector bay occupies rear Z;
- a controlled structural/service separation remains between them.

This is intentional 2.5D stacking.

No bay fastener or connector body may contact the VOICE isolation carrier.

## 4. Bay Z volume
Initial rear service cavity:
**Z approximately 22..40 mm**

VOICE remains forward around Z12..14 mm.

This leaves a nominal intermediate separation for:
- carrier;
- FPC;
- acoustic isolation;
- shell geometry.

Exact connector bodies may locally extend forward of Z22 only after collision validation.

## 5. Ethernet
Ethernet is the primary always-accessible connector.

RJ45 orientation:
- plug insertion from bottom/rear recess;
- cable turns downward then parallel to wall/product plane.

Do not point the installed cable directly into the wall.

Initial RJ45 local region:
- bay left/center portion.

Create:
- RJ45_BODY;
- RJ45_PLUG;
- RJ45_BOOT;
- ETH_BEND_CORRIDOR.

Target support:
- ordinary flexible Cat5e/Cat6 patch cable;
- no proprietary Ethernet lead required.

A slim or right-angle plug may be recommended but not required unless final CAD proves standard boots impossible.

## 6. External 24 V
External 24 V is the second normal-use connector.

Current PCB connector candidate:
- Molex Micro-Fit 3.0 43650-0200 PCB header;
- mating 43645-0200 housing family.

Place adjacent to Ethernet with clear tactile/keying separation.

The user must not be able to confuse Ethernet and DC connectors physically.

Create:
- J2_BODY;
- J2_MATED_HOUSING;
- J2_WIRE_BEND_CORRIDOR.

Cable exits downward/sideways, parallel to wall.

Provide enclosure strain relief independent of PCB solder joints.

## 7. USB-C service
USB-C is not expected to remain connected during normal wall operation.

Place deeper inside the recess or behind a small service aperture.

Requirements:
- standard USB-C plug can be inserted;
- recovery/service possible without opening the product;
- plug may protrude beyond normal installed wall envelope temporarily during service.

Do not compromise IP/dust behavior more than the already vented product architecture.

## 8. Connector order
Initial left-to-right seed viewed from rear/bottom:
1. Ethernet
2. 24 V DC
3. USB-C service

Final order may change after MAIN-C/MAIN-P harness routing.

Keep USB away from high-current DC wiring where practical.

## 9. Cross-board connection issue
Ethernet and USB belong to MAIN-C.
24 V belongs to MAIN-P.

Do not move 24 V protection onto MAIN-C merely to simplify the bay.

Instead use:
- board-edge placement if mechanically reachable; or
- a short qualified internal pigtail/remote panel connector only if electrical/current/protection architecture remains correct.

Preferred: keep the primary 24 V input/protection path electrically short and avoid unnecessary internal connector stages.

This remains a layout gate.

## 10. Passive cooling inlet
The connection bay shall not consume the complete lower-air inlet.

Current inlet seed:
**600 mm2 free area**.

Partition lower rear edge into:
- connection bay;
- separate inlet slot groups.

No cable bundle may cover more than a defined fraction of inlet area.

Initial CAD rule:
**>=600 mm2 unobstructed effective inlet area after cables are installed.**

Therefore geometric slot area will likely need to exceed 600 mm2 to account for cable obstruction/grills.

## 11. Acoustic isolation
Bay is entirely behind the sealed DML acoustic perimeter.

No direct opening from bay to front fabric volume.

Any VOICE acoustic channel crossing nearby remains independently sealed/isolated.

## 12. Structural rules
Do not cut the lower PC-CF perimeter into an unsupported long beam.

Use:
- bay-edge local frame rails;
- radiused corners;
- bridge/gusset around opening;
- no sharp rectangular stress raisers.

Connection bay shall be included in:
- wall-mount frame FEA;
- torsion case;
- lower support reaction case.

## 13. Rear-shell geometry
Use a recessed pocket/lip so installed connectors and first cable bend remain inside the wall-facing silhouette as much as possible.

The bay cover is optional; baseline is open/recessed because product is already ventilated.

If a cover is added:
- tool-less or captive;
- cannot pinch cables;
- does not block cooling inlet.

## 14. Human factors
Emboss/mold labels into rear/bottom shell:
- ETH
- 24V
- USB/SERVICE

Labels need not be visible from front.

24 V connector shall be mechanically keyed.

Provide finger/tool access sufficient to release RJ45 latch without removing rear shell.

## 15. Cable management
Add two non-structural routing clips/channels:
- Ethernet;
- 24 V.

They guide cables toward common downward exit but maintain separation.

Do not use adhesive-only cable retention as the primary strain relief.

## 16. DMU checks
Add:
C29 bay does not intersect VOICE PCB/carrier.
C30 bay does not intersect L1/R2 exciter columns.
C31 standard RJ45 latch can be operated.
C32 Ethernet boot/bend fits installed.
C33 24 V mating housing can be inserted/removed.
C34 24 V strain relief does not load PCB header.
C35 USB-C plug insertion path valid.
C36 installed cables leave >=600 mm2 effective cooling inlet.
C37 bay opening does not break DML acoustic seal.
C38 bay cutout passes lower-frame structural FEA.
C39 cables do not obstruct SHT45 chamber.
C40 cables do not enter radar RF cone.

## 17. CAD parameters
- CONNECTION_BAY_X0 = 100 mm
- CONNECTION_BAY_X1 = 220 mm
- CONNECTION_BAY_Y0 = 20 mm
- CONNECTION_BAY_Y1 = 48 mm
- CONNECTION_BAY_REAR_Z0_SEED = 22 mm
- CONNECTION_BAY_Z1 = 40 mm
- CONNECTION_BAY_PROJECTED = 120 x 28 mm
- CONNECTOR_ORDER_SEED = ETH / 24V / USB
- EFFECTIVE_INLET_AFTER_CABLES_MIN = 600 mm2

## 18. Release gates
1. exact RJ45 body/plug/boot CAD;
2. exact J2 Micro-Fit mated CAD;
3. exact USB4085 + plug CAD;
4. decide direct-board vs short internal connector strategy;
5. exact VOICE carrier Z envelope;
6. cable bend sweeps;
7. inlet CFD with cables installed;
8. lower-frame FEA with bay cutout;
9. serviceability simulation;
10. freeze shell recess geometry.

Status: **CONNECTION_BAY_120X28_LOWER_LEFT_CENTER / REAR_Z22_TO_40 / VOICE_FRONT_Z_STACK_SHARED_XY**.
