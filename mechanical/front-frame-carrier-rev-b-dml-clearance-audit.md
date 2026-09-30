# AudioPicture V2.2 Rev.B — front carrier magnetic-station DML clearance audit

Status: **DML_EDGE_PACKAGING_CONFLICT_CONFIRMED / 6MM_MAGNET_CANNOT_FIT_FLAT_IN_10MM_BORDER_WITH_REQUIRED_LANDS / MAGNET_ARCHITECTURE_RELOCATION_REQUIRED**

## 1. Purpose
Re-evaluate the proposed Rev.B perimeter-biased/D-shaped magnetic stations against the real product and DML projected geometry before generating another CAD solid.

This is a dimensional feasibility gate.

## 2. Governing XY geometry
Product:
X=0..320
Y=0..400 mm.

DML:
X=10..310
Y=10..390 mm.

Therefore the nominal geometric border between DML projection and product edge is only:
**10 mm per side**.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

Usable carrier border from DML edge to carrier outer edge is therefore approximately:
**9.2 mm**.

## 3. Candidate magnet
Packaging reference:
S-06-02-N class
diameter 6.0 mm.

Pocket seed:
diameter 6.6 mm.

A 6.6 mm pocket has radial extent:
**3.3 mm**.

## 4. Minimum material lands
A printable/robust pocket cannot terminate exactly at the carrier outer edge or DML-facing edge.

Use first-order minimum material land:
- outer-edge land >=1.5 mm seed;
- DML-facing structural/safety land >=1.0 mm seed.

Required transverse width for a flat circular pocket:
1.5 + 6.6 + 1.0 =
**9.1 mm**.

Available:
~9.2 mm.

This leaves only:
**~0.1 mm nominal geometric margin** before print tolerance, warp, assembly tolerance, DML edge motion and fabric wrap/bonding requirements.

Therefore a flat circular pocket is not production-robust.

## 5. Additional DML clearance
The DML is compliant and its perimeter mount uses foam.

A magnetic hard feature should not be dimensioned to nominal tangency with the DML projection.

Introduce hard-feature-to-DML projected clearance seed:
**>=1.0 mm**, with exact dynamic clearance to be validated.

This changes the required width to approximately:
1.5 + 6.6 + 1.0 hard land + 1.0 DML clearance =
**10.1 mm**.

This exceeds the available ~9.2 mm carrier border.

## 6. Rev.B center test
Proposed side centers:
X=12 or X=308.

For a 6.6 mm pocket:
left pocket extends X=8.7..15.3.
DML begins X=10.

Therefore it overlaps DML projection by:
**5.3 mm**.

Right pocket is symmetric.

Top/bottom centers similarly overlap the DML projection.

Moving the center outward far enough to clear DML pushes the pocket too close to or beyond the carrier/product edge once robust outer land is included.

## 7. D-shaped pad limitation
Changing only the external pad from circular to D-shaped does not solve the fundamental problem.

The magnet/pocket itself remains 6.6 mm diameter.

A D-shaped support can remove polymer on the DML-facing side, but cannot remove the magnet volume.

Therefore:
**D-shaped pad alone is rejected as the solution.**

## 8. Smaller magnet option
A smaller magnet could fit the border, but would introduce:
- new force model;
- smaller mechanical capture;
- higher tolerance sensitivity;
- potentially more stations.

This remains an optimization option, not preferred baseline.

Do not downsize magnet solely to preserve the previous station concept.

## 9. Preferred architecture change
Move the magnetic circuit away from the flat front border.

Preferred:
**rearward/perimeter-return magnetic interface**.

Concept:
- front carrier develops a shallow perimeter return/tab toward +Z outside the active DML edge;
- magnet axis and/or target interface is placed on the side/rear perimeter structure where XY overlap with DML is avoided;
- discrete steel targets attach to legal PC-CF/ASA perimeter nodes;
- magnetic retention still pulls the front frame onto its seating plane;
- X/Y location remains handled by LOC_A/LOC_B.

This uses Z/perimeter geometry rather than attempting to fit the full magnetic circuit inside a 9.2 mm flat border.

## 10. Candidate architectures
### P1 — perimeter return, axial normal attraction
Front carrier has local rearward ears outside DML projection.
Magnet remains approximately front-normal.
Target is recessed into rear/perimeter support.

Advantages:
- preserves simple magnet-to-steel circuit;
- retains existing 6 x 2 mm candidate;
- force direction remains favorable.

### P2 — sidewall shear/angled magnetic capture
Magnet acts through side/perimeter geometry.

Advantages:
- frees front border.

Disadvantages:
- force/removal behavior harder to predict;
- shear/friction sensitivity.

### P3 — smaller flat magnets
Retain flat-border concept with smaller diameter.

Advantages:
- simplest front geometry.

Disadvantages:
- component reselection and more stations likely.

Preferred order:
**P1 > P3 > P2**.

## 11. P1 dimensional seed
Use local perimeter-return ears centered near previous station Y/X coordinates but outside DML projection.

Return-ear Z band:
approximately **Z=1.0..6.5 mm** local/global-compatible subject to DML/front stack.

Critical rule:
the ear remains outside DML X/Y projection plus hard clearance.

Magnet pocket may then occupy Z depth without consuming DML-facing XY width.

Exact return geometry requires integration with:
- fabric wrap;
- DML perimeter foam;
- front carrier seating;
- rear structural perimeter;
- shell assembly/removal path.

## 12. Fabric bonding consequence
Perimeter-return ears must not break the continuous fabric wrap/bonding land.

Therefore:
- fabric bonding land remains front/perimeter continuous;
- magnetic ears originate behind the bonding land;
- adhesive and fabric never become structural magnet-retention members.

## 13. Removal consequence
P1 preserves sequential peel.

Magnetic stations should release as the front carrier rotates locally away from its seating plane.

No hook geometry may trap the front frame after magnetic force is overcome.

## 14. RF policy
All previous exclusions remain:
- no magnetic station in radar keep-out;
- no steel in radar keep-out;
- no magnetic station in ESP32 RF keep-out;
- no continuous steel ring.

Relocating rearward does not waive RF constraints.

## 15. CAD decision
Do **not** generate a Rev.B solid with D-shaped flat pads because the magnet volume itself still collides with the DML projected region.

Generate next:
**FRONT_CARRIER_REV_C_PERIMETER_RETURN**.

This avoids creating a geometrically valid but physically incorrect B-rep.

## 16. Automatic checks
C431 product-to-DML nominal border =10 mm.
C432 carrier usable border approximately 9.2 mm.
C433 6.6 mm pocket radial extent =3.3 mm.
C434 robust outer land included.
C435 DML-facing land included.
C436 DML hard clearance included.
C437 flat 6.6 mm pocket packaging fails robust-width criterion.
C438 Rev.B side center pocket overlap calculated.
C439 top/bottom equivalent conflict recognized.
C440 D-shaped external pad alone rejected.
C441 DML notch remains rejected baseline.
C442 magnet downsizing remains optional, not automatic.
C443 perimeter-return architecture selected preferred.
C444 existing 6 x 2 mm magnet may be retained in P1.
C445 fabric bonding land remains continuous.
C446 magnetic ears originate behind fabric land.
C447 removal remains peel-compatible.
C448 RF exclusions remain authoritative after relocation.
C449 no Rev.B B-rep generated from invalid flat-pad premise.
C450 Rev.C perimeter-return CAD is next geometry gate.

## 17. State
The integrated dimensional check disproves the previous assumption that a 6 mm-class magnet can be robustly packaged flat in the front carrier's nominal 10 mm border.

The correct engineering action is to change the magnetic interface topology rather than hide the conflict.

Status:
**FLAT_MAGNET_BORDER_CONCEPT_REJECTED / D_SHAPED_PAD_INSUFFICIENT / PERIMETER_RETURN_REV_C_SELECTED / C01_TO_C450**.
