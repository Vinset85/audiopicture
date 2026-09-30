# AudioPicture V2.2 — front target-holder to rear-frame structural integration Rev.H

Status: **NO_SECOND_FRONT_RING / LOCAL_PC_CF_CANTILEVER_TABS_SELECTED / DML_COMPLIANT_RING_SEPARATE / NOMINAL_LOAD_PATH_DEFINED**

## 1. Purpose
Resolve the structural attachment of the eight fixed magnetic target holders without adding a second continuous rigid ring around the DML.

## 2. Existing authoritative architecture
The repository already defines:
- a continuous rear PC-CF outer structural ring, nominal projected width 10 mm;
- a mechanically distinct DML support/hard-stop ring;
- a continuous compliant PORON perimeter interface for the DML;
- no hard structural shortcut through the DML compliant mount.

Therefore a new continuous fixed front perimeter ring is rejected as unnecessary and potentially harmful.

## 3. Selected architecture
Each magnetic target cassette becomes a local **front cantilever tab/node** tied to the existing PC-CF outer structural ring.

There are eight independent local nodes.

The nodes:
- project forward from legal outer-ring material;
- terminate at the Rev.G target-holder rear shelf;
- remain outside the DML hard XY projection;
- do not connect to the DML support ring;
- do not cross the PORON compliant path;
- do not form a continuous front ring.

## 4. Load path
Front-frame retention load path:
removable ASA carrier
-> S-04-02-N magnet
-> 7x7x1 steel target
-> Rev.G three-sided target cassette
-> local PC-CF cantilever tab
-> existing PC-CF outer structural ring
-> existing rear structural load paths / cleat nodes.

The DML and PORON are not in this magnetic retention load path.

## 5. Local tab seed
Diagnostic local tab:
- material: PC-CF, consistent with rear structural frame;
- tangential width: 10 mm seed;
- radial/perimeter-side attachment width: governed by legal outer ring;
- local web thickness seed: 2.4 mm;
- two triangular side gussets seed: 2.4 mm;
- root fillet target: >=1.5 mm;
- holder-end local pad sized to the 8.9 mm tangential cassette envelope.

These are FEA/process seeds, not released dimensions.

## 6. Z architecture
Rev.G holder rear extent:
<=Z6.3 mm diagnostic.

Existing generic rear PC-CF band:
Z27..35 mm where legal.

A straight 20+ mm unsupported front post is not accepted.

Instead the local tab is generated as a **shallow perimeter-side wall/web integrated with the enclosure side/perimeter structural section**, using the existing outer-ring radial section as the support.

The exact Z transition is controlled by the real rear-frame/shell section and shall be clipped by electronics/RF/service keep-outs.

This document defines topology, not a fictitious free-standing post.

## 7. DML exclusion
DML hard projection:
X10..310 / Y10..390.

For all tab/holder material in Z3.3..9.3:
- intersection with DML hard volume shall be exactly 0 mm3.

No tab may touch the DML edge.

No tab may replace or locally crush the PORON perimeter support.

## 8. DML compliant mount relationship
The DML mount remains:
- continuous compliant perimeter behavior;
- nominal PORON width 6 mm;
- 2.0 mm uncompressed thickness seed;
- 15..25% installed compression target;
- 20% nominal.

Magnetic target tabs are structurally downstream/outboard and mechanically separate.

No magnetic retention load is credited to foam.

## 9. Eight-node independence
The eight target tabs are local nodes, not one continuous front rail.

Benefits:
- avoids creating a second rigid acoustic boundary;
- allows individual RF/radar suppression or tangential relocation;
- limits structure-borne coupling;
- supports tolerance correction per station;
- permits local FEA optimization.

## 10. Tab station mapping
Use current centers:
M1D (70,394)
M2D (250,394)
M3D (70,6)
M4D (250,6)
M5D (6,135)
M6D (6,275)
M7D (314,135)
M8D (314,315).

Each tab grows only toward the nearest product perimeter.

No inward tab growth across the DML boundary is permitted.

## 11. ESP32 consequence
M1D is the closest top magnetic node to the frozen MAIN-C/ESP32 left-edge RF region.

The existing 15 mm antenna enclosure mask remains authoritative.

M1D tab must be boolean-clipped/suppressed if the exact antenna mask intersects it.

Current result remains:
**COARSE COMPATIBLE / EXACT RF BOOLEAN OPEN**.

## 12. Radar consequence
No exact radar EM hard mask is available.

Therefore M7D/M8D or any other affected tab may not be production-frozen.

Tab topology is intentionally local so a conflicting station can be:
- shifted tangentially;
- reduced;
- suppressed;
- replaced by a validated alternate station,
without redesigning a continuous ring.

## 13. Structural verification
Do not claim strength from geometry alone.

Local target-tab FEA shall include at minimum:
- outward/front-normal pull at target;
- peel-biased eccentric load;
- tangential/shear load;
- installation snap load;
- combined tolerance eccentricity.

Use coupon-derived PC-CF properties and print orientation.

The full rear frame still follows its existing LC1..LC7 contract.

## 14. Magnetic load seed for FEA
Until physical magnetic coupon data exists, use conservative local structural seed cases, not predicted magnetic performance:
- 5 N normal per target node;
- 2 N tangential per target node;
- 10 N local installation/service proof seed.

These are structural design loads only.

They are not magnetic-force predictions and do not alter the 20..30 N complete-frame measured retention requirement.

## 15. Failure criteria
Local tab must not:
- contact DML under load;
- permanently deform enough to alter G_EFF outside magnetic tolerance;
- release steel target;
- crack at root;
- transmit hard clamp load into DML support;
- enter RF/EM hard masks.

Allowable stress/strain and displacement limits remain dependent on qualified PC-CF material/process data.

## 16. CAD generation rule
The Rev.H diagnostic generator shall create local tab envelope seeds only.

It shall check:
- station count 8;
- DML hard-volume intersection 0;
- local node remains perimeter-biased;
- no continuous front ring is created.

Final union to the real rear-frame B-rep requires the transformed shared rear-frame solid and exact side-section geometry.

## 17. Automatic checks
C571 existing PC-CF outer structural ring recognized as authoritative fixed load path.
C572 second continuous front structural ring rejected.
C573 DML compliant support ring remains mechanically distinct.
C574 eight local PC-CF front cantilever nodes selected.
C575 magnetic retention load path excludes DML/PORON.
C576 tab tangential width seed 10 mm.
C577 tab web thickness seed 2.4 mm.
C578 tab gusset thickness seed 2.4 mm.
C579 tab root fillet target >=1.5 mm.
C580 no free-standing 20+ mm straight post accepted.
C581 tab transition must use real perimeter structural section.
C582 all tab material at DML Z band must have zero DML hard-volume intersection.
C583 no tab locally crushes PORON.
C584 eight tabs remain independent.
C585 each tab grows toward nearest product perimeter.
C586 M1D exact ESP32 RF boolean remains open.
C587 radar exact EM boolean remains open.
C588 local tabs may be shifted/suppressed independently for RF/EM.
C589 5 N normal/node structural FEA seed defined.
C590 2 N tangential/node structural FEA seed defined.
C591 10 N local installation/service proof seed defined.
C592 structural seed loads explicitly not magnetic predictions.
C593 physical complete-frame retention target remains 20..30 N.
C594 local FEA must check DML contact and G_EFF displacement.
C595 final union requires real transformed rear-frame/perimeter section.

## 18. State
A separate fixed front perimeter frame is not added.

The correct integration is:
**eight local PC-CF target-holder cantilever tabs tied into the existing rear outer structural ring/perimeter section while the DML compliant ring remains independent.**

Status:
**NO_SECOND_FRONT_RING / 8X_LOCAL_PC_CF_TARGET_TABS / DML_PORON_LOAD_PATH_SEPARATE / C01_TO_C595 / REAL_REAR_FRAME_UNION_AND_LOCAL_FEA_NEXT**.
