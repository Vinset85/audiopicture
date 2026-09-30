# AudioPicture V2.2 Rev.B — front carrier magnetic interface correction

Status: **D_SHAPED_COPLANAR_PAD_REJECTED / PERIMETER_BRIDGE_MAGNET_INTERFACE_SELECTED / DML_NOTCH_REJECTED**

## 1. Purpose
Resolve the Rev.A magnetic-pad overlap discovered by the integrated DMU.

## 2. Governing geometry
Product: 320 x 400 mm.
DML projection: X10..310, Y10..390.
Available pure perimeter strip outside DML: only 10 mm nominal per edge.

Magnet Candidate A: diameter 6.0 mm.
Process pocket seed: diameter 6.6 mm.

A robust printed pocket also requires polymer wall/capture material around the 6.6 mm bore.

## 3. Finding
A conventional 12 mm circular pad centered at the Rev.B seeds:
top Y388, bottom Y12, left X12, right X308
still overlaps the DML projected rectangle.

A simple D-shaped pad does not by itself solve the fundamental issue if the 6.6 mm magnet pocket remains coplanar with the DML edge: the available 10 mm perimeter strip is too small to provide comfortable symmetric pocket wall/capture and a hard DML clearance simultaneously.

Therefore the previous statement that a D-shaped pad alone would solve the collision is withdrawn.

## 4. Rejected solution
Do not notch, drill or trim the active DML panel to accommodate front-frame magnets.

DML acoustic/structural geometry remains authoritative.

## 5. Selected architecture
Use a **perimeter bridge magnetic interface**.

The front carrier remains thin at the fabric/DML plane.

At each magnetic station:
- a narrow ASA perimeter bridge runs outward/rearward around the DML edge;
- the magnet pocket is positioned in a legal volume outside the DML projected hard column;
- the mating steel target is attached to a legal PC-CF/rear-frame perimeter node;
- the magnetic circuit closes across a controlled local gap;
- no magnet pocket sits directly over the DML panel.

This converts the problem from a coplanar XY pad into a 3D perimeter-edge interface.

## 6. Local coordinate concept
For each edge define:
DML_EDGE = 10 mm from product outer boundary.

Carrier bridge occupies the product perimeter band and turns rearward only outside the DML hard projection.

Magnet center shall satisfy a CAD-derived condition:
its full pocket/capture envelope does not intersect the extruded DML hard volume.

No fixed center is production-frozen until this 3D boolean condition passes.

## 7. Seed station tangential coordinates
Tangential coordinates remain useful:
Top: X70, X250.
Bottom: X70, X250.
Left: Y135, Y275.
Right: Y135, Y315.

The normal-to-edge coordinate becomes solver/CAD-derived rather than fixed at 12/308/388.

## 8. Pocket envelope
Candidate A pocket:
6.6 mm process seed.

Minimum surrounding polymer seed:
>=1.5 mm locally where mechanically loaded, subject to print qualification.

Resulting minimum structural width class:
~9.6 mm before asymmetric capture details.

This explains why the 10 mm perimeter strip is marginal for a coplanar pocket and supports the 3D bridge solution.

## 9. Bridge geometry
Seed:
- tangential width 12..16 mm;
- wall 1.8..2.2 mm;
- rearward leg sized by global Z collision solve;
- root radius >=1.5 mm;
- no sharp inside corner.

The bridge is local, not a continuous deep perimeter wall.

## 10. Global Z rule
The bridge may extend rearward only where:
- it clears DML edge/compliant mount;
- it clears exciter columns;
- it does not reduce the governing EX25 rear clearance;
- it does not block microphone/radar/optical paths.

The magnet pocket Z is selected from legal perimeter free volume, not from the active DML plane.

## 11. Target architecture
Discrete low-carbon steel target at matching perimeter structural node.

No continuous steel ring.

Target:
- mechanically trapped or positively retained;
- outside radar/ESP32 RF keep-outs;
- does not bridge compliant DML mounting interface.

## 12. Retention target
Unchanged:
20..30 N total assembled normal retention.

Eight stations remain baseline.

Actual station force is tuned with:
- magnetic gap;
- target thickness/area;
- bridge compliance;
- pocket/target alignment.

## 13. Peel
Lower center peel recess remains.

Bottom magnetic bridges at tangential X70 and X250 preserve progressive release around X160.

## 14. Structural behavior
Magnetic removal load flows:
front carrier perimeter -> local bridge -> magnet -> target -> PC-CF perimeter node.

It does not flow through:
- DML;
- DML foam mount;
- sensor PCB;
- radar board.

## 15. CAD implementation sequence
1. import/extrude DML hard volume.
2. generate front perimeter carrier.
3. generate legal perimeter bridge candidate at each tangential station.
4. place magnet pocket in bridge.
5. boolean-check pocket/capture envelope vs DML hard volume.
6. check RF/sensor masks.
7. check removal sweep.
8. optimize normal-to-edge and Z coordinates.
9. regenerate one-solid carrier.
10. export Rev.B DMU STEP.

## 16. Automatic checks
C431 DML projection treated as hard volume for magnet pockets.
C432 coplanar 12 mm circular pad rejected.
C433 D-shaped-only coplanar fix rejected.
C434 no DML notch allowed.
C435 magnet pocket full envelope outside DML hard volume.
C436 local bridge connects carrier to magnet pocket.
C437 bridge root radius >=1.5 mm seed.
C438 bridge does not enter exciter hard column.
C439 bridge does not consume EX25 rear-clearance envelope.
C440 target attaches to structural perimeter node.
C441 target does not bridge DML compliant mount.
C442 no continuous steel ring.
C443 radar RF mask rejects magnetic hardware.
C444 ESP32 RF mask rejects magnetic hardware.
C445 tangential station coordinates retained.
C446 normal-to-edge coordinate CAD-derived.
C447 magnet Z CAD-derived.
C448 total retention target remains 20..30 N.
C449 peel recess remains between bottom stations.
C450 removal load bypasses DML.

## 17. State
The integrated DMU correctly invalidated the simple coplanar pad concept.

Selected correction:
**3D perimeter bridge magnetic interface**.

Tangential seeds:
- top/bottom X70, X250;
- left Y135, Y275;
- right Y135, Y315.

Normal and Z positions:
**CAD-derived from hard-volume boolean clearance**.

Status:
**COPLANAR_MAGNET_PAD_REJECTED / 3D_PERIMETER_BRIDGE_SELECTED / DML_UNMODIFIED / C01_TO_C450 / REV_B_KERNEL_GENERATION_NEXT**.
