# AudioPicture V2.2 Rev.B — DML-clear magnetic front carrier

Status: **MAGNET_CENTER_REV_B_REJECTED_BY_GEOMETRIC_PROOF / PERIMETER_MAGNET_ARCHITECTURE_REQUIRES_SMALLER_TARGET_OR_REAR_INTERFACE**

## 1. Purpose
Resolve the front-carrier magnet-pad overlap found by the integrated DMU.

## 2. Hard geometry
Product:
320 x 400 mm.

Front carrier projected boundary:
X=0.8..319.2
Y=0.8..399.2.

DML projected boundary:
X=10..310
Y=10..390.

Available projected border between DML and carrier outer boundary:
- left: 9.2 mm
- right: 9.2 mm
- bottom: 9.2 mm
- top: 9.2 mm.

## 3. Existing magnet pocket
Candidate A magnet:
6.0 mm diameter.

Pocket seed:
6.6 mm diameter.

Required mechanical capture material around pocket cannot be zero.

A circular 12 mm station pad requires 6 mm radial half-width.

## 4. Rev.B center test
Proposed Rev.B centers:
M1B/M2B Y=388
M3B/M4B Y=12
M5B/M6B X=12
M7B/M8B X=308.

These centers are still inside the DML projected boundary:
- top centers are 2 mm below Y390;
- bottom centers are 2 mm above Y10;
- left centers are 2 mm right of X10;
- right centers are 2 mm left of X310.

Therefore moving from 14 to 12 mm or 386 to 388 mm does not solve the fundamental overlap.

## 5. D-shaped pad test
A D-shaped pad can remove pad material on the DML-facing side.

However the magnet pocket itself is centered at the station.

For a 6.6 mm pocket:
radius = 3.3 mm.

At a top center Y=388:
pocket extends to Y384.7..391.3.

Therefore 5.3 mm of the pocket radial span lies inside the DML projection below Y390.

Equivalent conflicts exist on all four edges.

Conclusion:
**D-shaping the outer pad alone cannot make the pocket DML-clear.**

## 6. Minimum center location for DML-clear pocket
For a 6.6 mm pocket to remain fully outside DML projection with zero additional clearance:

Top:
center Y >= 390 + 3.3 = **393.3 mm**

Bottom:
center Y <= 10 - 3.3 = **6.7 mm**

Left:
center X <= 10 - 3.3 = **6.7 mm**

Right:
center X >= 310 + 3.3 = **313.3 mm**.

These are the mathematical minimums before adding structural material around the pocket.

## 7. Structural capture requirement
If minimum material between pocket and DML-facing pad edge is 1.2 mm seed:

required center offset from DML edge:
3.3 + 1.2 = **4.5 mm**.

Thus:
Top Y >=394.5
Bottom Y <=5.5
Left X <=5.5
Right X >=314.5.

## 8. Carrier outer-boundary check
Carrier outer boundary:
top 399.2
bottom 0.8
left 0.8
right 319.2.

At center Y394.5, available material to outer edge:
399.2 - 394.5 = 4.7 mm.

A 6.6 mm pocket requires 3.3 mm radius, leaving only:
1.4 mm outer material.

This is geometrically possible but tight.

Same on all edges.

Therefore a true perimeter-only pocket is feasible only as a narrow local boss with approximately:
- 1.2 mm DML-side material;
- 1.4 mm outer-side material.

This is too sensitive to print tolerance/warp for immediate production freeze.

## 9. Revised legal center seed
For CAD investigation only:

Top:
M1C=(70,394.5)
M2C=(250,394.5)

Bottom:
M3C=(70,5.5)
M4C=(250,5.5)

Left:
M5C=(5.5,135)
M6C=(5.5,275)

Right:
M7C=(314.5,135)
M8C=(314.5,315).

These centers are legal for a 6.6 mm pocket with approximately 1.2 mm DML-side wall and 1.4 mm outer-side wall in nominal geometry.

## 10. Risk classification
The MxC layout is:
**GEOMETRICALLY_FEASIBLE / PROCESS_MARGIN_TIGHT**.

It shall not be production-frozen without:
- real ASA print tolerance data;
- magnet-pocket coupon;
- edge-strength test;
- peel-cycle test.

## 11. Preferred architecture review
Three alternatives remain.

A. Edge pocket, current 6 x 2 magnet:
- feasible;
- tight wall;
- easiest architecture.

B. Smaller magnet:
- increases polymer wall/process margin;
- requires new magnetic-force characterization;
- may be preferred if 8 stations still meet 20..30 N.

C. Magnet/target moved to a rearward structural interface:
- removes front DML overlap issue;
- may increase mechanical complexity and removal-path coupling.

## 12. Recommended next branch
Do not alter DML.

Do not pretend MxB solved the collision.

Generate MxC edge-pocket CAD as a feasibility body, but in parallel evaluate a smaller 5 mm-class magnet because the additional 0.5..0.8 mm radial polymer margin is valuable at the product perimeter.

## 13. Front carrier Rev.B topology
Base ring remains:
- 318.4 x 398.4 mm;
- 10 mm nominal width;
- 1.8 mm nominal thickness.

Magnet stations become edge bosses rather than symmetric 12 mm circular pads.

Boss is clipped by:
- carrier outer boundary;
- DML hard-clearance boundary;
- local minimum-wall rules.

## 14. Edge-boss construction
For each station:
1. create local rectangular/rounded edge boss;
2. subtract magnet pocket;
3. preserve DML-side wall >=1.2 mm seed;
4. preserve outer wall >=1.2 mm seed;
5. preserve tangential end wall >=1.5 mm;
6. merge with perimeter ring;
7. validate one-solid result.

## 15. Pocket depth
Candidate A 6 x 2:
- pocket depth process seed 2.15..2.25 mm;
- local boss Z thickness 3.2 mm seed.

Front floor:
~0.9..1.0 mm nominal if 3.2 mm local thickness and 2.2 mm pocket.

This floor contributes to magnetic gap and force tuning.

## 16. DML clearance
Hard rule:
no magnet pocket solid/void envelope may cross into DML hard projected region.

A separate service clearance may later increase this requirement beyond zero projected overlap.

## 17. Global Z
Carrier remains perimeter-only.

Local edge bosses occupy front perimeter and do not alter the central fabric-DML gap.

The master global Z stack remains:
- fabric Z0..0.5;
- air gap to Z3.3;
- DML Z3.3..9.3.

## 18. Automatic checks
C431 Rev.B MxB centers analytically tested.
C432 MxB centers fail DML-clear pocket rule.
C433 D-shaped pad alone proven insufficient.
C434 6.6 mm pocket radius recorded as 3.3 mm.
C435 zero-clearance legal center equations defined.
C436 1.2 mm DML-side wall rule applied.
C437 MxC center set defined.
C438 MxC nominal DML-side wall >=1.2 mm.
C439 MxC nominal outer-side wall >=1.2 mm.
C440 MxC classified process-margin tight.
C441 DML modification rejected.
C442 edge-boss topology defined.
C443 tangential wall >=1.5 mm seed.
C444 boss merges with perimeter ring.
C445 local Z thickness 3.2 mm seed.
C446 pocket depth sweep 2.15..2.25 mm.
C447 front pocket floor approximately 0.9..1.0 mm.
C448 central fabric-DML gap unchanged.
C449 smaller magnet branch retained.
C450 production freeze requires print/pocket/peel qualification.

## 19. State
The previous Rev.B station relocation was not sufficient.

Corrected legal seed:
M1C (70,394.5)
M2C (250,394.5)
M3C (70,5.5)
M4C (250,5.5)
M5C (5.5,135)
M6C (5.5,275)
M7C (314.5,135)
M8C (314.5,315).

Status:
**REV_B_MAGNET_GEOMETRY_CORRECTED / EDGE_POCKET_FEASIBLE_BUT_TIGHT / DML_UNCHANGED / C01_TO_C450 / SMALLER_MAGNET_COMPARISON_NEXT**.
