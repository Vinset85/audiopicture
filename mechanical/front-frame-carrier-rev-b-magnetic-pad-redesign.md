# AudioPicture V2.2 Rev.B — front carrier magnetic-pad redesign

Status: **REV_B_MAGNET_STATIONS_PERIMETER_SHIFTED / D_SHAPED_PADS_DEFINED / DML_HARD_KEEPOUT_POLICY_FROZEN / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Remove the Rev.A magnetic-pad conflict with the DML projected perimeter without modifying or notching the DML.

## 2. Authoritative product geometry
Product:
320 x 400 mm.

DML:
X10..310
Y10..390.

Front carrier outer projected boundary:
X0.8..319.2
Y0.8..399.2.

Base perimeter ring:
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

## 4. Conflict mechanism
A symmetric 12 mm diameter station pad around these centers would still cross the DML projected edge.

Therefore circular local thickening is rejected.

The magnet itself remains 6 mm class, but its structural support is clipped toward the product perimeter.

## 5. DML hard-clearance line
No rigid magnetic-station thickening may extend into the DML projected active hard region.

Seed no-go:
- top station DML-facing edge: Y <=390 prohibited for pad thickening;
- bottom: Y >=10 prohibited;
- left: X >=10 prohibited;
- right: X <=310 prohibited.

Because the base carrier ring already occupies perimeter support geometry, this rule specifically governs the extra rearward station thickening and magnet capture volume.

## 6. D-shaped pad concept
Each station uses:
- 6.6 mm magnet pocket;
- local rearward thickening biased toward the product edge;
- flat/clipped DML-facing side;
- rounded perimeter-facing side.

Nominal local envelope along perimeter:
12 mm class.

Nominal inward extra-thickening projection:
limited to the legal side of the DML hard line.

## 7. Pocket placement issue
A 6.6 mm pocket centered only 2 mm from the DML edge cannot be fully contained outside the DML projection.

Therefore the magnet center itself must move farther outward than the Rev.B seed if the complete rearward magnet body is treated as rigid DML keep-out.

Required center distance from DML edge:
magnet radius 3.3 mm + clearance seed 0.5 mm =
**3.8 mm minimum**.

## 8. Rev.C-ready corrected centers
Use 4.0 mm outward offset from DML edge as the minimum nominal center distance.

Top:
Y=394 mm gives 4 mm outside DML Y=390.

Bottom:
Y=6 mm gives 4 mm outside DML Y=10.

Left:
X=6 mm gives 4 mm outside DML X=10.

Right:
X=314 mm gives 4 mm outside DML X=310.

Corrected candidate centers:

M1C=(70,394)
M2C=(250,394)

M3C=(70,6)
M4C=(250,6)

M5C=(6,135)
M6C=(6,275)

M7C=(314,135)
M8C=(314,315).

## 9. Carrier-boundary feasibility
Carrier outer boundary is 0.8..319.2 / 0.8..399.2.

For 6.6 mm magnet pocket radius 3.3 mm:

At X=6:
outer pocket edge X=2.7 mm >0.8.

At X=314:
outer edge X=317.3 <319.2.

At Y=6:
outer edge Y=2.7 >0.8.

At Y=394:
outer edge Y=397.3 <399.2.

Therefore all corrected pockets fit inside the front-carrier projected boundary.

## 10. DML clearance feasibility
For center distance 4.0 mm from DML edge and pocket radius 3.3 mm:
residual projected separation:
**0.7 mm**.

This is a seed clearance, not a production tolerance closure.

Recommended CAD hard-clearance target:
>=0.5 mm.

Production tolerance analysis may require moving centers another 0.3..0.8 mm outward.

## 11. Revised station pad
Use asymmetric pad generated from:
- circular outer support region;
- boolean clipping by DML hard-clearance half-space;
- minimum material around magnet pocket;
- local bridge to base perimeter ring.

The pad must remain one connected body with the carrier.

## 12. Magnet capture
Magnet body itself remains outside DML projection at corrected centers.

Rear-loaded pocket:
- 6.6 mm seed diameter;
- Candidate A 6 x 2 mm reference;
- mechanical capture;
- adhesive secondary.

Capture lip/cap must also obey DML hard-clearance half-space.

## 13. Local Z
Base carrier:
1.8 mm.

Station local thickness:
3.2 mm seed.

Because station is now outside DML projection, local rearward thickening no longer consumes the central fabric-DML gap.

Exact product-global transform still required.

## 14. Peel feature
Lower peel recess remains:
center X160
width28
depth4.

M3C/M4C at X70/250 remain 90 mm from peel center in X.

No change required.

## 15. RF masks
Corrected perimeter positions improve separation from central functional regions but do not replace RF checking.

Exact:
- radar mask;
- ESP32 antenna mask;
- mic paths;
- optical path

remain hard placement filters.

If any corrected station intersects an RF mask, slide along its perimeter edge rather than inward toward DML.

## 16. Structural note
Moving magnets farther toward the product edge increases local peel leverage.

This may reduce user removal force for the same normal magnetic force.

Therefore assembled 20..30 N normal target remains, but peel-force validation must be repeated with corrected coordinates.

## 17. CAD generation sequence
1. generate 318.4 x398.4 base ring;
2. generate corrected M1C..M8C pocket axes;
3. generate local station support;
4. clip each support by DML hard half-space;
5. union station support to base ring;
6. subtract 6.6 mm pockets;
7. generate mechanical capture geometry;
8. subtract peel recess;
9. validate one solid;
10. measure volume/mass/bbox;
11. transform into product-global Z;
12. run DML collision.

## 18. Automatic checks
C431 Rev.B seed overlap mechanism documented.
C432 symmetric 12 mm station pads rejected.
C433 full magnet body treated as rigid DML keep-out.
C434 minimum center offset from DML edge >=3.8 mm.
C435 corrected nominal center offset=4.0 mm.
C436 M1C/M2C at Y394.
C437 M3C/M4C at Y6.
C438 M5C/M6C at X6.
C439 M7C/M8C at X314.
C440 all 6.6 mm pockets fit inside carrier outer boundary.
C441 projected magnet-pocket separation from DML >=0.7 mm nominal.
C442 station support clipped by DML half-space.
C443 station thickening remains connected to base ring.
C444 magnet capture remains outside DML projection.
C445 local station Z remains 3.2 mm seed.
C446 peel recess remains clear.
C447 RF masks remain authoritative.
C448 RF conflict resolves by sliding along perimeter, not inward.
C449 peel validation repeated after coordinate move.
C450 real OpenCASCADE regeneration required.

## 19. State
The intermediate Rev.B centers are not sufficient for a full 6.6 mm magnet pocket outside the DML projection.

Corrected centers M1C..M8C solve the geometric issue at nominal dimensions while remaining inside the front-carrier boundary.

This correction is adopted for real CAD regeneration.

Status:
**MAGNET_CENTERS_CORRECTED_TO_4MM_OUTSIDE_DML / 0P7MM_NOMINAL_POCKET_CLEARANCE / D_SHAPED_SUPPORT / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
