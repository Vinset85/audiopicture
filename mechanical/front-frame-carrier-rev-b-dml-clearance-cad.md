# AudioPicture V2.2 Rev.B — front carrier DML-clearance CAD

Status: **REV_B_MAGNET_STATIONS_PERIMETER_BIASED / DML_FACING_PAD_CLIPPED / ONE_BODY_TARGET / GLOBAL_Z_INTEGRATION_READY**

## 1. Purpose
Resolve the Rev.A front-carrier warning where nominal 12 mm circular magnet pads extended into the DML projected perimeter.

Rev.B preserves:
- removable fabric carrier;
- eight magnetic stations;
- 20..30 N assembled retention target;
- hidden peel removal;
- unfilled ASA;
- 318.4 x 398.4 mm carrier;
- 10 mm nominal perimeter ring;
- 1.8 mm base thickness.

## 2. Authoritative DML projection
DML:
X=10..310 mm
Y=10..390 mm.

No local magnet-station thickening may protrude into the DML hard projected region.

The normal thin carrier perimeter is a separate front-interface feature and is not interpreted as an exciter/electronics rear-volume intrusion.

## 3. Rev.B magnet centers
Top:
- M1B=(70,388)
- M2B=(250,388)

Bottom:
- M3B=(70,12)
- M4B=(250,12)

Left:
- M5B=(12,135)
- M6B=(12,275)

Right:
- M7B=(308,135)
- M8B=(308,315).

## 4. Pad topology
Rev.A circular 12 mm pad:
**withdrawn as production baseline**.

Rev.B uses perimeter-biased clipped pads.

Each station starts from a 12 mm class local reinforcement but the DML-facing side is clipped by the DML hard projection plus clearance.

Resulting topology is D-shaped/asymmetric.

## 5. DML-facing limits
Top stations:
rear-thickened pad material must remain at Y>=390 mm where it would otherwise intrude behind DML.

Bottom:
rear-thickened pad material must remain at Y<=10 mm.

Left:
rear-thickened pad material must remain at X<=10 mm.

Right:
rear-thickened pad material must remain at X>=310 mm.

Because the product/carrier boundary is close to these values, the pad is not a simple full 12 mm disc.

## 6. Magnet pocket implication
A 6 mm diameter magnet centered only 2 mm from the DML edge cannot itself remain entirely outside the DML projection.

Therefore the Rev.B coordinate seed alone is insufficient if the complete magnet body is treated as a rearward DML keep-out object.

This exposes a second-order conflict:
- M center at Y388 with radius 3 mm extends to Y385;
- DML begins below Y390.

Equivalent conflicts exist at all four edges.

## 7. Corrected magnet center requirement
To keep a 6 mm magnet fully outside DML projection with 0.5 mm geometric clearance:

Top center:
Y >= 393.5 mm.

Bottom:
Y <= 6.5 mm.

Left:
X <= 6.5 mm.

Right:
X >= 313.5 mm.

Carrier projected boundary:
X0.8..319.2
Y0.8..399.2.

These positions are geometrically possible in the outer carrier band.

## 8. Rev.C-ready center seed
Use a 4.0 mm centerline from the outer carrier edge class:

Top:
M1C=(70,395)
M2C=(250,395)

Bottom:
M3C=(70,5)
M4C=(250,5)

Left:
M5C=(5,135)
M6C=(5,275)

Right:
M7C=(315,135)
M8C=(315,315).

These centers keep a 6 mm magnet outside the DML projection with approximately 2 mm nominal edge separation.

## 9. Edge containment
For 6.6 mm pocket diameter, radius 3.3 mm.

At center 5 mm:
outermost pocket edge=1.7 mm.

Carrier starts at 0.8 mm.

Remaining carrier material to projected edge:
~0.9 mm before local outer-shape optimization.

This is too thin for a robust simple circular pocket wall.

Therefore local carrier edge must be thickened/reshaped or center moved slightly inward while reducing pocket wall strategy.

## 10. Packaging trade
There is a narrow radial design window:
- move outward -> DML clearance improves but outer pocket wall thins;
- move inward -> pocket wall improves but magnet enters DML projection.

A conventional radial 6.6 mm bore inside a 10 mm flat ring is marginal.

Preferred solution:
**tangential magnet pocket integrated into a locally widened perimeter ear**.

The ear expands locally along the outer product edge, not toward DML.

## 11. Local perimeter ear
At each magnet station:
- locally widen carrier structural region tangentially;
- retain product outer boundary;
- use material along perimeter direction for stiffness;
- use thin closed outer wall >=1.2 mm target;
- DML-facing rear thickening clipped outside hard DML projection.

Pocket axis remains Z.

The visible front silhouette does not change.

## 12. Candidate magnet size review
S-06-02-N 6x2 mm remains feasible but mechanically tight in the 10 mm ring.

Before production freeze evaluate a smaller-diameter magnet class if:
- assembled 20..30 N can still be achieved;
- smaller pocket materially improves edge wall.

Do not reduce diameter solely from CAD convenience without force validation.

## 13. Rev.B kernel objective
Generate carrier with:
- one connected B-rep;
- local perimeter ears;
- no rear thickened material inside DML projection;
- pocket wall >=1.2 mm target where practical;
- peel recess unchanged;
- no visible silhouette change.

## 14. Global Z placement
Carrier base remains front-perimeter feature.

Rear local magnetic thickening is legal only outside DML XY projection.

Therefore magnet ears may use local Z to ~3.2 mm carrier coordinates without consuming active fabric-to-DML gap over the DML.

## 15. Peel
Lower center peel recess:
center X160
width28
depth4.

M3C/M4C remain at X70/250, so peel remains centered approximately 90 mm from each lower magnetic station.

Progressive release architecture preserved.

## 16. Mass expectation
Moving reinforcement tangentially around perimeter changes mass only by a few grams.

Carrier target remains:
<=60 g.

Complete front assembly:
<=120 g.

Exact Rev.B/C kernel mass remains authoritative after regeneration.

## 17. Important design finding
The Rev.B collision audit proves that merely clipping a 12 mm pad is insufficient: the magnet itself must also satisfy the DML projected keep-out if its rearward body shares the DML Z region.

Therefore:
**Rev.B centers are withdrawn for physical magnet placement.**

Rev.C-ready outer centers become the new CAD seed.

This prevents hiding a real interference inside pad geometry.

## 18. Automatic checks
C431 Rev.A circular magnet pad withdrawn.
C432 Rev.B centers tested against DML projection.
C433 6 mm magnet radius included in collision test.
C434 Rev.B top stations fail full magnet DML keep-out.
C435 Rev.B bottom stations fail full magnet DML keep-out.
C436 Rev.B left stations fail full magnet DML keep-out.
C437 Rev.B right stations fail full magnet DML keep-out.
C438 minimum center coordinates derived from magnet radius plus clearance.
C439 Rev.C-ready centers defined.
C440 Rev.C-ready 6 mm magnet clears DML projection.
C441 6.6 mm pocket outer-wall thickness flagged as marginal.
C442 local perimeter ear architecture selected.
C443 ear grows tangentially, not toward DML.
C444 visible product silhouette remains unchanged.
C445 magnet pocket axis remains Z.
C446 rear thickening excluded from DML projection.
C447 peel geometry remains clear.
C448 magnet diameter reduction remains force-validation dependent.
C449 final kernel regeneration required.
C450 full front assembly force/RF validation remains open.

## 19. State
Rev.B analysis found that the proposed 2 mm outward move did not fully solve the physical magnet/DML overlap.

Corrected next seed:
M1C=(70,395)
M2C=(250,395)
M3C=(70,5)
M4C=(250,5)
M5C=(5,135)
M6C=(5,275)
M7C=(315,135)
M8C=(315,315).

The correct solution is a perimeter-ear magnet station, not a clipped circular pad around the Rev.B centers.

Status:
**REV_B_CENTER_CHECK_FAILED_PHYSICAL_MAGNET_RADIUS / REV_C_OUTER_CENTER_SEED_DEFINED / PERIMETER_EAR_REQUIRED / C01_TO_C450**.
