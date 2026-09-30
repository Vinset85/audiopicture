# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnetic stations

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_OVERLAP_REMOVED_BY_CONSTRUCTION / REAL_BREP_REGENERATION_GATE**

## 1. Purpose
Correct the Rev.A circular magnet-pad/DML projected overlap found by the integrated master DMU.

The DML remains unchanged.

The magnetic station geometry moves toward the product perimeter and uses clipped/D-shaped support pads.

## 2. Authoritative global geometry
Product:
320 x 400 mm.

DML hard projected rectangle:
X=10..310
Y=10..390.

Front carrier projected outer boundary:
X=0.8..319.2
Y=0.8..399.2.

Carrier ring:
10 mm nominal.

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

These centers are packaging seeds, not permission for circular pads to cross the DML boundary.

## 4. DML-facing hard clipping planes
Top stations:
all rigid station-pad material must remain at Y>=390, except the magnet pocket itself only if an explicit DML Z-clearance solve proves legal.

Bottom:
pad rigid material Y<=10.

Left:
pad rigid material X<=10.

Right:
pad rigid material X>=310.

Baseline Rev.B chooses the stronger rule:
**no station support-pad material inside the DML projected hard rectangle.**

## 5. D-shaped pad concept
Each station uses a perimeter-side lobe connected to the carrier ring.

Nominal lobe envelope:
- tangential length 14 mm;
- perimeter-normal depth 8 mm maximum;
- local total thickness 3.2 mm;
- root fillet >=1.5 mm.

The DML-facing side is clipped flush to the DML projected boundary.

The lobe is therefore D/segment-shaped rather than a 12 mm full circle.

## 6. Critical magnet-pocket feasibility
A 6.6 mm diameter pocket has radius 3.3 mm.

At top center Y=388, a symmetric pocket reaches Y391.3 and crosses the DML boundary Y390.

Likewise:
- bottom Y12 reaches Y8.7..15.3;
- left X12 reaches X8.7..15.3;
- right X308 reaches X304.7..311.3.

Therefore merely clipping the support pad is insufficient if the magnet itself remains centered at the Rev.B seed.

This is a second-order collision discovered analytically.

## 7. Rev.C-ready corrected centerline
To keep the complete 6.6 mm pocket outside DML projection with a minimum 0.5 mm geometric margin:

required center distance from DML edge:
3.3 + 0.5 = 3.8 mm.

Corrected centers:

Top:
M1C=(70,393.8)
M2C=(250,393.8)

Bottom:
M3C=(70,6.2)
M4C=(250,6.2)

Left:
M5C=(6.2,135)
M6C=(6.2,275)

Right:
M7C=(313.8,135)
M8C=(313.8,315).

## 8. Carrier-edge feasibility
Carrier boundary:
0.8..319.2 / 0.8..399.2.

For M1C/M2C:
pocket outer edge Y=397.1 <399.2.

Bottom:
outer edge Y=2.9 >0.8.

Left:
outer edge X=2.9 >0.8.

Right:
outer edge X=317.1 <319.2.

Thus a bare 6.6 mm pocket envelope fits between the DML hard boundary and carrier outer boundary.

Available outer-side material:
approximately 2.1 mm from pocket edge to carrier outer boundary.

This is tight but potentially printable with a locally shaped lobe.

## 9. Structural wall around magnet
A conventional full 1.5..2 mm radial wall around the complete pocket does not fit in the 9.2 mm carrier-to-DML perimeter strip.

Therefore Rev.B/Rev.C station must use one of:
A. open/rear retention cap integrated with perimeter edge;
B. tangentially elongated lobe with reduced outer radial wall;
C. smaller magnet candidate;
D. product-side magnet and thin steel target in front carrier.

Preferred next solve:
compare A and D before freezing.

## 10. Architecture implication
The previous assumption "magnet in front carrier" is no longer automatically optimal.

The 9.2 mm usable perimeter strip is the governing dimension.

A thin steel target can be easier to package in the front carrier than a 2 mm thick magnet pocket.

Therefore evaluate:
**product-side magnet + front-carrier steel target** as a serious preferred architecture.

This also moves magnet mass/rear thickening away from the removable fabric carrier.

## 11. Target-in-carrier option
Front carrier contains discrete steel target:
- 8..10 mm tangential dimension;
- 5..7 mm perimeter-normal dimension;
- 0.5..0.8 mm thickness seed;
- mechanically trapped.

Product-side magnet:
- mounted on rigid non-RF perimeter structure;
- force tuned through front carrier/polymer gap.

Benefits:
- thinner removable carrier;
- easier DML clearance;
- less front-carrier warp;
- magnets remain with product during front removal.

Risk:
- steel target still must stay outside RF keep-outs;
- local target geometry must fit perimeter strip.

## 12. D-shaped target seed
Use target lobe:
- tangential length 10 mm;
- normal width <=6.5 mm;
- thickness 0.6 mm seed.

Target inner edge remains outside DML hard rectangle.

Carrier local pocket/recess:
0.7..0.9 mm class including adhesive/capture allowance.

This is much easier than a 3.2 mm magnet boss.

## 13. Force model consequence
Moving magnet to product side changes G_MAG stack.

New effective magnetic path may include:
- magnet coating;
- local air gap;
- product-side retention skin;
- front carrier polymer;
- target coating.

Force must be remeasured/recomputed.

20..30 N total target remains unchanged.

## 14. Peel behavior
Magnet-on-product / steel-on-front does not alter sequential peel principle.

Lower peel recess remains centered X160.

M3/M4 target stations remain far from center peel initiation.

## 15. Mass consequence
Front removable assembly loses most magnet mass and thick bosses.

Eight Candidate-A magnets:
3.44 g move to fixed product side.

Steel targets add only local small mass.

Front carrier mass may reduce relative to Rev.A real B-rep.

## 16. Rev.B CAD generation rule
Do not regenerate the Rev.A carrier with merely shifted circular bosses.

Generate two CAD variants:

V1:
front-carrier magnets using corrected M*C centers and edge-integrated retention lobes.

V2:
front-carrier thin steel targets using corrected M*C perimeter zones, magnets fixed product-side.

Compare:
- solid validity;
- DML clearance;
- minimum printable wall;
- carrier mass;
- peel behavior;
- serviceability;
- RF legality.

## 17. Automatic checks
C431 DML hard projected rectangle explicit.
C432 Rev.B centers tested against full magnet pocket radius.
C433 support-pad-only clipping identified as insufficient.
C434 full 6.6 mm pocket collision at M*B analytically detected.
C435 corrected M*C centers maintain >=0.5 mm DML projected margin.
C436 M*C pockets remain inside carrier outer boundary.
C437 outer-side residual material recorded.
C438 conventional symmetric thick magnet boss flagged as packaging-tight.
C439 DML remains unmodified.
C440 magnet-on-product architecture admitted for comparison.
C441 target-in-carrier thickness seed <=0.8 mm.
C442 target D-shaped perimeter-normal width <=6.5 mm seed.
C443 front carrier magnetic hardware remains outside DML hard projection.
C444 total retention target remains 20..30 N.
C445 peel recess architecture preserved.
C446 V1 and V2 real CAD variants required.
C447 real B-rep solid validity required for both.
C448 RF keep-outs remain authoritative over station coordinates.
C449 final magnet/target architecture selected only after force and packaging comparison.
C450 no circular 12 mm Rev.A pad may be reused as production geometry.

## 18. State
Important result:
The first Rev.B center shift alone was not sufficient.

A full 6.6 mm magnet pocket at the Rev.B centers still crosses the DML hard projected boundary.

Corrected geometric centers:
- top Y393.8
- bottom Y6.2
- left X6.2
- right X313.8.

This fits the magnet envelope, but leaves only about 2.1 mm outer-side material to the carrier boundary.

Therefore the architecture is now explicitly comparing:
V1 edge-integrated magnet pockets;
V2 product-side magnets + thin front-carrier steel targets.

Status:
**REV_B_ANALYTICAL_COLLISION_CAUGHT / REV_C_CENTERLINES_DEFINED / MAGNET_ON_PRODUCT_OPTION_PROMOTED / C01_TO_C450 / DUAL_CAD_VARIANT_NEXT**.
