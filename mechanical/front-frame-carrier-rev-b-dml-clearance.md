# AudioPicture V2.2 Rev.B — front carrier DML-clearance redesign

Status: **PERIMETER_WIDTH_CONFLICT_IDENTIFIED / ORIGINAL_6MM_MAGNET_STATIONS_NOT_GEOMETRICALLY_LEGAL_OUTSIDE_DML / MAGNET_ARCHITECTURE_RELOCATION_REQUIRED**

## 1. Purpose
Test the proposed Rev.B perimeter-biased magnet stations against the authoritative projected DML rectangle before generating a misleading production-like B-rep.

Product:
320 x 400 mm.

DML projection:
X=10..310
Y=10..390 mm.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2 mm.

## 2. Available perimeter strip
Between DML projection and carrier outer boundary, the nominal available strip is only:

Left:
10.0 - 0.8 = **9.2 mm**

Right:
319.2 - 310.0 = **9.2 mm**

Bottom:
10.0 - 0.8 = **9.2 mm**

Top:
399.2 - 390.0 = **9.2 mm**.

This strip must accommodate any magnet pocket, capture wall, edge wall and tolerance clearance if the station is to remain fully outside the DML projection.

## 3. Candidate-A pocket requirement
S-06-02-N class magnet:
6.0 mm diameter.

Current pocket seed:
6.6 mm diameter.

Minimum radial structural wall seed:
>=1.2 mm each side for a printed captured pocket before local optimization.

Minimum station width:
6.6 + 2(1.2) = **9.0 mm**.

This leaves only:
9.2 - 9.0 = **0.2 mm**

for combined:
- carrier outside-edge wall/offset;
- DML-side clearance;
- print tolerance;
- assembly tolerance.

Therefore a fully circular captured 6.6 mm pocket is not robustly feasible in the 9.2 mm strip.

## 4. Rev.B center test
Proposed top/bottom centers:
Y=388 / 12.

A 6.6 mm pocket has radius 3.3 mm.

Top station at Y388 extends to Y384.7..391.3.
DML ends at Y390.
Overlap into DML projection:
**5.3 mm from DML-facing pocket edge to boundary geometry context; pocket crosses Y390 by 1.3 mm on rear side and extends substantially inside the DML projected band on its inward side.**

Bottom station at Y12 extends Y8.7..15.3.
DML begins Y10.
It crosses into DML projection to Y15.3.

Side stations show the same issue.

The proposed 2 mm outward shift does not solve the hard projected-overlap problem.

## 5. D-shaped pad limitation
Making only the external support pad D-shaped does not solve the problem if the cylindrical magnet pocket itself still intersects the DML projection.

The magnet pocket/capture geometry is the governing minimum feature.

Therefore:
**D-shaped support pad alone is insufficient.**

## 6. Geometric conclusion
With:
- 300 x 380 DML centered at 10 mm margins;
- carrier outer boundary at 0.8 mm;
- captured 6 mm-class round magnet;

there is no comfortable tolerance-robust perimeter-only circular station fully outside the DML projection.

This is a packaging conflict, not a CAD-kernel problem.

## 7. Rejected solution
Do not:
- notch the active DML;
- reduce DML dimensions casually;
- accept near-zero printed wall;
- allow magnet pocket over active DML merely to preserve the previous eight-station concept.

## 8. Preferred architecture change
Move magnetic retention rearward/outboard to a **side-return / edge-latch magnetic circuit** rather than keeping the magnet pocket in the flat front carrier plane.

Concept:
- front carrier develops local side-return tabs around product perimeter;
- magnets sit with their cylindrical axis in a locally legal edge/return volume;
- steel targets attach to corresponding ASA/PC-CF non-RF perimeter nodes;
- the visible front remains thin;
- DML front projection remains untouched.

The return feature uses product edge/perimeter Z volume rather than the 9.2 mm front planar strip.

## 9. Side-return geometry seed
Local front-frame return:
- projected edge length per station: 12..16 mm;
- return depth in +Z: 4..7 mm where subsystem keep-outs permit;
- wall: 1.6..2.0 mm ASA;
- magnet pocket remains 6.6 mm class;
- local capture cap/lip.

Return must stay inside product 320 x 400 XY boundary and global Z envelope.

## 10. Retention direction
A side-return magnet/steel geometry may produce a mixed normal/shear circuit.

The design must still provide:
- front-frame normal seating;
- anti-rattle preload;
- progressive peel removal.

If magnetic force direction is unsuitable, use the return only to house magnet while shaping a local ferromagnetic target to close the flux in the normal direction.

Exact circuit is an electromagnetic/mechanical subproblem.

## 11. Alternative architecture
Alternative B:
use smaller magnets, e.g. 4 mm class, with more stations.

This may fit the 9.2 mm strip but:
- increases station count;
- reduces individual capture-wall margin;
- requires a new real-component search and force model.

Do not silently substitute smaller magnets.

## 12. Alternative architecture C
Use hidden mechanical micro-clips plus weaker/smaller magnets only for seating.

This can reduce magnetic force and magnet size while retaining tool-less removal.

It introduces clip fatigue/tolerance qualification.

Keep as fallback.

## 13. Current eight-station coordinates
The previous Rev.B coordinates remain useful as **station arc/edge locations**, not as flat circular pocket centers:
- top around X70 and X250;
- bottom around X70 and X250;
- left around Y135 and Y275;
- right around Y135 and Y315.

Their exact pocket coordinates move into local return geometry.

## 14. CAD consequence
Do not generate a Rev.B flat-carrier STEP claiming DML clearance.

First generate one representative side-return station as a parametric coupon/sub-body and prove:
- DML projection clearance;
- magnet capture;
- global Z legality;
- peel kinematics;
- target support.

Then pattern legal station variants around the perimeter.

## 15. Global Z consequence
Front visible plane remains unchanged.

Side returns occupy local +Z edge volume.

They must not:
- enter DML edge compliance;
- block perimeter acoustic mount;
- interfere with rear frame;
- enter radar/ESP32 RF keep-outs;
- block vent paths.

## 16. Checks
C431 perimeter strip calculated as 9.2 mm.
C432 6.6 mm pocket plus robust walls consumes essentially full strip.
C433 proposed Rev.B flat pocket still overlaps DML projection.
C434 D-shaped pad alone does not fix cylindrical-pocket overlap.
C435 DML notch rejected baseline.
C436 near-zero tolerance wall rejected.
C437 false Rev.B collision-free STEP prohibited.
C438 side-return magnetic architecture selected for next CAD study.
C439 original eight station edge arcs retained.
C440 side-return Z depth limited parametrically.
C441 exact magnetic circuit force remains validation gate.
C442 smaller-magnet architecture remains explicit alternative, not silent substitution.
C443 hybrid micro-clip architecture retained as fallback.
C444 representative station must pass before full pattern.
C445 DML compliant perimeter remains protected.
C446 front global Z datum unchanged.
C447 RF keep-outs remain authoritative.
C448 ventilation keep-outs remain authoritative.
C449 peel/removal kinematics required.
C450 next CAD artifact is a side-return station coupon, not a falsely cleared full carrier.

## 17. State
The attempted Rev.B flat-pocket correction is **not geometrically robust**.

The important design result is that the 10 mm DML edge margin and a captured 6 mm-class magnet compete for the same perimeter strip.

Preferred next architecture:
**local side-return magnetic stations using edge Z volume**.

Status:
**FLAT_6MM_MAGNET_PERIMETER_CONFLICT_CONFIRMED / DML_UNCHANGED / SIDE_RETURN_MAGNETIC_STATION_SELECTED / C01_TO_C450 / COUPON_CAD_NEXT**.
