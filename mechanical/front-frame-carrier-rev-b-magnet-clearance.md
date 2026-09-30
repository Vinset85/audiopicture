# AudioPicture V2.2 Rev.B — front carrier magnet clearance correction

Status: **REV_B_12MM_MAGNET_SEED_REJECTED / 6MM_PERIMETER_CENTERLINE_SELECTED / REAL_CAD_REGEN_REQUIRED**

## 1. Finding
The Rev.B magnet-center seed at 12 mm from the product edge does not geometrically clear the DML hard projection.

DML projection:
X=10..310 mm
Y=10..390 mm.

Candidate-A magnet:
diameter 6.0 mm, radius 3.0 mm.

Pocket:
diameter 6.6 mm, radius 3.3 mm.

A center at X=12 mm has pocket inward edge X=15.3 mm and therefore overlaps DML projection by 5.3 mm.

The same condition applies symmetrically at the other product edges.

Therefore the previous M1B..M8B seed is rejected as a DML-clear magnet-pocket solution.

## 2. Required centerline
For a 6.6 mm pocket to remain entirely outside DML projection with a small geometric margin:

left center <= 10 - 3.3 - margin
right center >= 310 + 3.3 + margin
bottom center <= 10 - 3.3 - margin
top center >= 390 + 3.3 + margin.

With 0.5 mm seed margin:
left/bottom center <=6.2 mm;
right center >=313.8 mm;
top center >=393.8 mm.

Adopt nominal perimeter centerline:
**6.0 mm from product edge**.

## 3. Rev.C coordinate seed
Top:
M1C=(70,394)
M2C=(250,394)

Bottom:
M3C=(70,6)
M4C=(250,6)

Left:
M5C=(6,135)
M6C=(6,275)

Right:
M7C=(314,135)
M8C=(314,315).

## 4. Pocket edge margins
For 6.6 mm pocket at 6 mm centerline:
outer product-edge material coordinate:
6.0 - 3.3 = 2.7 mm from edge on left/bottom;
316? Symmetric equivalent on right/top.

DML-facing edge:
6.0 + 3.3 = 9.3 mm.

DML starts at 10.0 mm.

Nominal DML projected clearance:
**0.7 mm**.

This is geometrically positive but tight and requires tolerance analysis.

## 5. Tolerance warning
0.7 mm nominal projected clearance is not enough to freeze production without accounting for:
- DML XY placement tolerance;
- carrier print shrink/warp;
- pocket location tolerance;
- front-frame locator tolerance.

Therefore 6 mm is a CAD feasibility seed, not production release.

Potential production solutions:
A. reduce magnet/pocket diameter;
B. move center to 5.5 mm if edge structure remains adequate;
C. use elongated/tangential pocket with local outward boss;
D. use smaller magnets at more stations;
E. product-side magnet / front-side thin target architecture.

## 6. D-shaped pad
The local structural pad may be D-shaped, but the magnetic pocket itself must also respect the DML hard projection.

A D-shaped pad cannot solve a circular pocket collision if the pocket overlaps the DML.

Therefore pocket centerline is governing.

## 7. Carrier perimeter compatibility
Nominal carrier boundary:
0.8..319.2 / 0.8..399.2.

At centerline 6 mm with pocket radius3.3:
minimum pocket edge=2.7 mm.

Relative to carrier outer boundary0.8:
available carrier material outside pocket:
**1.9 mm** nominal.

This is thin but feasible as a diagnostic geometry, not yet robust production capture.

Local outward/perimeter thickening and capture-cap geometry are required.

## 8. Preferred next optimization
Before committing to 6x2 mm magnets, evaluate smaller metric magnets:
- 5 mm diameter class;
- 4 mm diameter class;
with higher station count if necessary.

Goal:
increase both:
- DML clearance;
- outer pocket wall thickness;
while retaining 20..30 N total assembled retention.

## 9. Real CAD policy
Do not generate a falsely passing Rev.B solid using clipped pads around an overlapping pocket.

The next real B-rep shall use:
- corrected centerline;
- pocket geometry;
- actual outer wall thickness;
- DML hard-projection subtraction/check.

A CAD model is PASS only if the pocket/capture volume itself clears DML, not merely the pad outline.

## 10. Automatic checks
C431 Rev.B 12 mm centerline rejected.
C432 circular pocket included in DML collision logic.
C433 corrected centerline derived from DML edge and pocket radius.
C434 Rev.C 6 mm centerline defined.
C435 nominal pocket-to-DML projected clearance positive.
C436 nominal pocket-to-DML clearance recorded as 0.7 mm.
C437 outer carrier wall around pocket recorded as 1.9 mm nominal.
C438 0.7 mm is not production tolerance closure.
C439 D-shaped pad cannot mask pocket collision.
C440 smaller magnet optimization required before production freeze.
C441 real CAD regeneration must use corrected pocket.
C442 DML notch remains rejected baseline.
C443 production release requires XY tolerance stack.
C444 front magnetic retention target remains 20..30 N.
C445 magnet count remains parametric.

## 11. State
Rev.B 12 mm seed:
**REJECTED**

Rev.C feasibility centerline:
**6 mm from product edge**

6.6 mm pocket:
- DML projected nominal clearance ~0.7 mm;
- outer carrier wall ~1.9 mm.

These values are too tight for production freeze.

Status:
**MAGNET_GEOMETRY_CONFLICT_CORRECTED / 6MM_CENTERLINE_FEASIBILITY_ONLY / SMALLER_MAGNET_OPTIMIZATION_NEXT / C01_TO_C445**.
