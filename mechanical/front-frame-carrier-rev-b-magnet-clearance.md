# AudioPicture V2.2 Rev.B — front carrier magnet-clearance correction

Status: **REV_B_PREVIOUS_MAGNET_SEED_REJECTED / REV_C_PERIMETER_SEED_GEOMETRICALLY_VALID / REAL_BREP_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the magnet-pad/DML projected overlap discovered by the integrated master DMU.

## 2. Governing geometry
DML projection:
X=10..310 mm
Y=10..390 mm.

Magnet pocket:
diameter 6.6 mm
radius 3.3 mm.

Minimum structural wall around pocket used for this geometric screen:
1.0 mm.

Required center offset from DML projected edge:
3.3 + 1.0 = **4.3 mm minimum**.

Therefore a magnet station completely outside the DML projection requires approximately:
- top center Y >=394.3
- bottom center Y <=5.7
- left center X <=5.7
- right center X >=314.3.

## 3. Rejection of previous Rev.B coordinates
Previous seed:
- top Y388
- bottom Y12
- left X12
- right X308.

These centers are still inside the DML projection.

A D-shaped pad alone cannot make the 6.6 mm magnet pocket plus structural wall fully external to the DML projection.

Therefore the previous Rev.B seed is:
**REJECTED FOR HARD DML CLEARANCE**.

## 4. Revised perimeter seed — Rev.C
Adopt:

Top:
M1C=(70,394.8)
M2C=(250,394.8)

Bottom:
M3C=(70,5.2)
M4C=(250,5.2)

Left:
M5C=(5.2,135)
M6C=(5.2,275)

Right:
M7C=(314.8,135)
M8C=(314.8,315).

## 5. Carrier outer boundary check
Carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

Pocket radius:
3.3 mm.

At center coordinate 5.2:
nearest pocket edge=1.9 mm.

At center coordinate 314.8:
outer pocket edge=318.1 mm.

At top Y394.8:
outer pocket edge=398.1 mm.

At bottom Y5.2:
outer pocket edge=1.9 mm.

Therefore the 6.6 mm pocket itself remains inside the carrier projected boundary.

## 6. DML clearance check
Pocket envelope at every Rev.C station is outside the DML projected rectangle.

Geometric screen:
**PASS**.

This statement applies to the 6.6 mm pocket envelope.

The full structural station pad/capture geometry must still be shaped so its DML-facing material does not violate the required DML hard-clearance volume.

## 7. Station pad topology
Use perimeter-biased D-shaped/local boss.

Rules:
- pocket center remains at Rev.C coordinate;
- DML-facing structural edge is clipped to legal perimeter zone;
- outward side may grow toward carrier edge only while preserving outer-wall strength;
- magnet capture is integrated into perimeter ring rather than a free circular island.

## 8. Structural concern
The revised centers are close to the carrier outer edge.

Therefore the old symmetric 12 mm circular pad is retired.

The perimeter ring itself becomes the structural support for each magnet pocket.

Use local tangential reinforcement along the perimeter, not radial growth toward the DML.

## 9. Pocket wall
The 1.0 mm value above is only a minimum geometric screen.

Production wall thickness must be print-process qualified.

Preferred ASA local wall target:
>=1.2 mm where geometry permits.

If 1.2 mm cannot be maintained with the 6.6 mm pocket and outer edge, locally adjust:
- carrier edge profile;
- station center by <=0.5 mm;
- magnet diameter candidate;
- capture-cap architecture.

Do not move inward into DML hard space.

## 10. Front carrier B-rep regeneration
Next real kernel model shall include:
- 318.4 x 398.4 carrier;
- 10 mm ring;
- 1.8 mm base;
- Rev.C magnet centers;
- perimeter-integrated magnet bosses;
- 6.6 mm pockets;
- lower peel recess;
- locator features when defined.

Required kernel checks:
- one connected solid;
- valid B-rep;
- no magnet pocket intersects DML projection;
- no station structural material enters DML hard-clearance volume;
- peel recess preserves connectivity;
- mass remains <=60 g carrier budget.

## 11. Magnetic force consequence
Moving stations outward does not change the 20..30 N assembled-force target.

G_MAG remains a magnetic-circuit variable.

However target placement on the mating product structure must now provide legal target support very close to the product perimeter.

No continuous steel ring.

## 12. RF consequence
More peripheral stations are favorable in principle for central sensing clearance, but exact:
- ESP32 antenna keep-out;
- radar keep-out;
- cable/metal interactions

remain authoritative.

No RF pass is claimed from geometry alone.

## 13. Automatic checks
C431 previous Rev.B magnet seed rejected.
C432 pocket radius 3.3 mm explicitly modeled.
C433 1.0 mm minimum structural-wall screen included.
C434 required 4.3 mm DML-edge center offset derived.
C435 Rev.C top centers >=394.3.
C436 Rev.C bottom centers <=5.7.
C437 Rev.C left centers <=5.7.
C438 Rev.C right centers >=314.3.
C439 all 6.6 mm pockets remain inside carrier outer boundary.
C440 all 6.6 mm pockets clear DML projected rectangle.
C441 symmetric 12 mm circular station pad retired.
C442 perimeter-integrated station topology required.
C443 inward station growth into DML prohibited.
C444 local ASA wall >=1.2 mm preferred.
C445 exact RF masks remain required.
C446 20..30 N retention target unchanged.
C447 target support must be generated near perimeter.
C448 no continuous steel target ring.
C449 real B-rep regeneration required.
C450 real solid must prove structural pad DML clearance, not pocket clearance only.

## 14. State
The attempted Rev.B concept exposed a geometric incompatibility before manufacturing release.

Corrected seed:
M1C (70,394.8)
M2C (250,394.8)
M3C (70,5.2)
M4C (250,5.2)
M5C (5.2,135)
M6C (5.2,275)
M7C (314.8,135)
M8C (314.8,315).

Status:
**REV_B_SEED_REJECTED / REV_C_MAGNET_CENTERS_CLEAR_DML_POCKET_PROJECTION / C01_TO_C450 / REAL_CAD_REGENERATION_NEXT**.
