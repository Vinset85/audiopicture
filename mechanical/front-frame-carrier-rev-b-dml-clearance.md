# AudioPicture V2.2 Rev.B — front carrier DML-clearance redesign

Status: **MAGNET_STATIONS_MOVED_TO_PERIMETER / D_SHAPED_PADS_DEFINED / DML_HARD_OVERLAP_REMOVED_BY_CONSTRUCTION / REAL_KERNEL_REGEN_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic station geometry after the integrated DMU detected overlap between 12 mm circular pads and the projected DML perimeter.

The DML remains unchanged.

## 2. Authoritative product geometry
Product:
320 x 400 mm.

DML projected hard rectangle:
X=10..310
Y=10..390.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

## 3. Rev.B magnet centers
Top:
M1B=(70,388)
M2B=(250,388)

Bottom:
M3B=(70,12)
M4B=(250,12)

Left:
M5B=(12,135)
M6B=(12,275)

Right:
M7B=(308,135)
M8B=(308,315).

## 4. Why circular pads are rejected
A circular pad around these centers still extends across the DML hard boundary.

Therefore the pad is no longer defined by a complete circle.

Use a perimeter-biased D-shaped/local rectangular-round pad with the DML-facing side clipped to the DML hard boundary plus assembly clearance.

## 5. Hard DML clearance
Define:
G_PAD_DML = **0.5 mm nominal seed**.

No rigid magnetic-station carrier material may cross into:
- top: Y < 390.5 for top station pad extension toward DML;
- bottom: Y > 9.5 for bottom station pad extension toward DML;
- left: X > 9.5 for left station pad extension toward DML;
- right: X < 310.5 for right station pad extension toward DML.

Because the magnet centers themselves lie close to/inside the DML projected edge, this exposes a critical issue:
a centered Ø6 mm magnet cannot remain entirely outside the DML hard projection at the current centers.

## 6. Center correction
The Rev.B center seeds from the master audit are therefore insufficient for a Ø6 mm magnet plus 0.5 mm DML clearance.

Minimum magnet-center location for a 3.0 mm radius magnet and 0.5 mm clearance:

Top:
Y >= 390 + 3.0 + 0.5 = **393.5 mm**

Bottom:
Y <= 10 - 3.0 - 0.5 = **6.5 mm**

Left:
X <= **6.5 mm**

Right:
X >= **313.5 mm**.

These locations are incompatible or extremely tight with the 0.8 mm carrier outer boundary and practical capture wall for some edges.

Therefore the original architecture "magnet fully outside DML projection" is not feasible with Ø6 mm magnets inside a ~10 mm perimeter without further interface redesign.

## 7. Correct architecture
Do not require the complete magnet to lie outside the DML XY projection.

Instead distinguish:
- DML structural projected rectangle;
- DML active moving surface;
- front carrier seating/perimeter land;
- Z-separated magnetic hardware.

A projected XY overlap is acceptable only if sufficient Z separation exists and the magnet/pad cannot mechanically contact or preload the DML.

The hard requirement is **3D non-intersection + dynamic clearance**, not zero 2D projection overlap.

This corrects the overly conservative Rev.B 2D rule.

## 8. 3D station strategy
Keep Rev.B centers as packaging seeds.

Use D-shaped pads biased toward the product perimeter.

DML-facing pad edge is minimized.

Global Z placement shall keep:
- rigid pad rear face in front of DML front plane;
- dynamic clearance to DML >=2.0 mm hard minimum under tolerance.

The magnet pocket is oriented so magnetic circuit closes toward a product-side perimeter target without contacting the DML.

## 9. Z envelope
Fabric outer:
Z0.

DML front:
Z3.3.

The carrier/magnet station must remain entirely within a legal front-perimeter Z envelope.

For any station that overlaps DML in XY:
Z_PAD_REAR <= **1.3 mm** would be required to preserve 2.0 mm hard clearance to DML front.

This is incompatible with a 2 mm-thick magnet if stacked purely behind the visible front plane.

Therefore a flat axial Ø6x2 magnet directly over the DML projection cannot satisfy the current 2.0 mm clearance.

## 10. Architecture consequence
A major correction is required before regenerating the carrier solid.

Preferred solutions in order:

### B1 — move magnets into true perimeter outside DML projection
Use smaller magnets and/or narrower capture geometry in the 10 mm border.

### B2 — relocate magnetic circuit behind a non-DML perimeter ledge
Create a stepped side/perimeter magnetic interface outside the DML moving panel.

### B3 — use thin rectangular magnets along product perimeter
This may exploit the long narrow border more efficiently than Ø6 discs.

### B4 — reduce DML projected size
Rejected baseline because it changes acoustic architecture.

## 11. Preferred next design
Adopt **thin rectangular perimeter magnets** rather than force the Ø6x2 disc into the 10 mm border.

Target magnet envelope:
- radial/inboard dimension <=4 mm class;
- tangential length 8..15 mm;
- thickness 1..2 mm.

This gives room for:
- outer carrier wall;
- magnet;
- capture wall;
- DML clearance.

The existing S-06-02-N remains a force-characterization reference but is no longer the preferred packaging geometry.

## 12. Retention target unchanged
Total assembled retention:
20..30 N.

Station count:
6/8/10 parametric.

With rectangular magnets, per-station force target remains based on assembled measured circuit, not catalogue free pull.

## 13. CAD release decision
Do **not** regenerate a misleading Rev.B B-rep with Ø6 disc pockets.

The integrated DMU has disproven that packaging choice under the required DML clearance.

This is an intentional engineering stop.

## 14. Automatic checks
C431 DML remains 300 x 380.
C432 Rev.B station centers recorded.
C433 circular 12 mm pad rejected.
C434 zero-2D-overlap rule identified as overconservative.
C435 actual requirement defined as 3D non-intersection plus dynamic clearance.
C436 Ø6x2 flat magnet over DML projection fails front Z clearance.
C437 DML reduction rejected baseline.
C438 smaller/narrower perimeter magnetic geometry required.
C439 thin rectangular magnet architecture preferred.
C440 total retention target remains 20..30 N.
C441 station count remains 6/8/10 parametric.
C442 S-06-02-N retained only as force/reference candidate.
C443 no false B-rep generated after geometry contradiction.
C444 exact rectangular magnet search required.
C445 next carrier kernel generation waits for viable magnet envelope.

## 15. State
The Rev.B DMU refinement exposed that the issue is not merely pad shape.

A 6 mm diameter x 2 mm thick disc cannot be cleanly packaged in the available front perimeter while preserving the current 2.0 mm DML dynamic clearance if it overlaps the DML projection.

Therefore:
**disc magnet packaging is withdrawn as preferred front-carrier architecture**.

Next action:
select a thin rectangular magnet whose inboard dimension is <=4 mm class, then regenerate the carrier.

Status:
**DML_CLEARANCE_CONTRADICTION_FOUND / 6X2_DISC_PACKAGING_WITHDRAWN / THIN_RECTANGULAR_PERIMETER_MAGNET_REQUIRED / C01_TO_C445**.
