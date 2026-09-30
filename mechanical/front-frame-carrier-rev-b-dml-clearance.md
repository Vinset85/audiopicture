# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **REV_B_MAGNET_STATION_GEOMETRY_DEFINED / DML_PROJECTED_OVERLAP_REMOVED_BY_PERIMETER_CLIPPED_PADS / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A magnetic-station warning found by the integrated master DMU.

The active DML projected rectangle is:
- X = 10..310 mm
- Y = 10..390 mm.

Rev.A circular 12 mm station pads crossed this projected boundary.

Rev.B moves the centers outward and clips each pad on the DML-facing side.

## 2. Rev.B magnet centers
Top:
- M1B = (70,388)
- M2B = (250,388)

Bottom:
- M3B = (70,12)
- M4B = (250,12)

Left:
- M5B = (12,135)
- M6B = (12,275)

Right:
- M7B = (308,135)
- M8B = (308,315).

## 3. Important geometric consequence
A 6.6 mm diameter magnet pocket has radius 3.3 mm.

At a center only 2 mm outside the DML projected edge, the pocket itself would still cross the DML projection if its axis remained coplanar with the DML edge.

Therefore merely clipping the 12 mm reinforcement pad is insufficient.

The pocket/magnet envelope must also remain outside the DML hard-clearance projection.

## 4. Minimum legal center offset
For a circular pocket radius 3.3 mm and a desired geometric margin M:

center offset from DML edge >= 3.3 + M.

Using M=0.7 mm seed:
required center offset >=4.0 mm.

Therefore the Rev.B 2 mm-outward centers are not production-legal for a strict no-overlap rule.

## 5. Rev.C-compatible corrected seed
Adopt corrected center offset 5 mm outside DML edge where product perimeter allows.

Top DML edge Y=390:
center Y=395.

Bottom DML edge Y=10:
center Y=5.

Left DML edge X=10:
center X=5.

Right DML edge X=310:
center X=315.

Corrected centers:
- M1C = (70,395)
- M2C = (250,395)
- M3C = (70,5)
- M4C = (250,5)
- M5C = (5,135)
- M6C = (5,275)
- M7C = (315,135)
- M8C = (315,315).

## 6. Product-edge feasibility
Product boundary:
X0..320, Y0..400.

For 6.6 mm pocket radius 3.3 mm at center coordinate 5 mm:
nearest product edge clearance:
5 - 3.3 = **1.7 mm**.

For center coordinate 315:
320 - (315+3.3) = **1.7 mm**.

For top Y395:
400 - (395+3.3) = **1.7 mm**.

Thus the pocket fits inside the product projected envelope with 1.7 mm geometric edge material before outer cosmetic details.

## 7. Carrier outer boundary issue
The Rev.A carrier outer boundary is inset to X/Y=0.8..319.2/399.2.

At center coordinate 5 mm, pocket outer edge is 1.7 mm from product edge and 0.9 mm from carrier nominal outer edge.

That is insufficient structural wall for a simple circular through/rear pocket.

Therefore Rev.B/Rev.C magnetic stations require local perimeter ears or a smaller magnet architecture.

## 8. Preferred solution
Do not create fragile 0.9 mm outer walls.

Preferred design change:
use a smaller magnet candidate class for perimeter stations OR locally extend/thicken the hidden rear carrier geometry while preserving visible outer dimensions.

Candidate design space:
- 5 mm diameter magnet;
- 1.5..2.0 mm thickness;
- discrete steel target;
- controlled magnetic gap.

With a 5.4 mm process pocket radius 2.7 mm at center offset 4.0 mm:
- DML margin ~1.3 mm;
- product-edge remaining ~1.3 mm at a 4 mm center;
- carrier-wall geometry remains tight but more manageable with asymmetric rear capture.

## 9. Architectural decision
The current 6 x 2 mm magnet remains a force-reference candidate but is **withdrawn as the default packaging reference** for the front carrier perimeter.

Reason:
DML extends to within 10 mm of product edge and strict no-overlap plus mechanical capture makes the 6.6 mm pocket unnecessarily packaging-critical.

The front frame should not force a DML modification.

## 10. New magnet packaging requirement
Target nominal magnet diameter:
**<=5.0 mm preferred**

Pocket outer diameter:
**<=5.5 mm target**

Magnet thickness:
1.5..2.0 mm class.

Assembled force target remains:
20..30 N total.

This may require:
- stronger grade;
- thinner gap;
- larger/more efficient steel target;
- 10 stations instead of 8 if necessary.

## 11. Station count trade
8 stations remain preferred for simplicity.

10 stations are now a valid fallback if <=5 mm magnets cannot deliver a smooth 20..30 N assembled retention curve.

Do not increase magnet diameter back into DML keep-out merely to preserve 8 stations.

## 12. D-shaped pad geometry
Regardless of magnet size, reinforcement pads are perimeter-biased D-shapes.

For each station:
- flat/clipped face toward DML;
- rounded/full material toward product perimeter;
- pocket center remains fully outside DML hard projection;
- minimum material around pocket is process/strength qualified.

## 13. Structural load path
Magnetic normal load:
front fabric/carrier -> local magnet capture -> local perimeter pad -> ASA perimeter ring.

It must not load:
- DML;
- DML compliant foam;
- microphone carrier;
- radar PCB.

## 14. CAD release consequence
Do not regenerate a Rev.B B-rep with the 6.6 mm pockets at the 2 mm-outward centers because it would encode a known geometric defect.

Next kernel generation shall use:
- <=5 mm selected magnet envelope, or
- an explicitly proven alternate capture architecture.

## 15. Automatic checks
C431 Rev.A 12 mm circular pad overlap is retired.
C432 Rev.B 2 mm center offset evaluated.
C433 6.6 mm pocket at 2 mm offset fails strict DML no-overlap.
C434 minimum pocket/DML margin formula documented.
C435 5 mm-outside corrected center seed defined.
C436 6.6 mm pocket fits product envelope at corrected centers.
C437 6.6 mm pocket leaves insufficient carrier outer wall in simple architecture.
C438 6 x 2 mm magnet withdrawn as default packaging reference.
C439 <=5.0 mm magnet diameter preferred.
C440 <=5.5 mm pocket OD target.
C441 D-shaped perimeter-biased pad required.
C442 pocket itself, not only reinforcement pad, must clear DML.
C443 DML modification prohibited baseline.
C444 8 stations preferred.
C445 10 stations allowed if smaller magnets require it.
C446 total assembled retention remains 20..30 N.
C447 magnetic load path terminates in ASA perimeter ring.
C448 no magnetic load into DML foam.
C449 real kernel regeneration waits for smaller magnet selection.
C450 known-defect Rev.B 6.6 mm B-rep shall not be generated.

## 16. State
The attempted Rev.B geometry review exposed a deeper packaging constraint before kernel generation:

**the magnet pocket itself must clear the DML, not merely its reinforcement pad.**

Therefore the 6 x 2 mm reference magnet is no longer the default packaging choice.

Next action:
select and verify a real <=5 mm magnet candidate, calculate its magnetic-circuit force range, then generate the corrected carrier B-rep.

Status:
**MAGNET_POCKET_VS_DML_CONSTRAINT_RESOLVED / 6MM_DEFAULT_WITHDRAWN / <=5MM_REAL_COMPONENT_SELECTION_NEXT / C01_TO_C450**.
