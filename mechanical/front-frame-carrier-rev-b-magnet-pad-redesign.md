# AudioPicture V2.2 Rev.B — front carrier magnetic-pad redesign

Status: **REV_B_PERIMETER_BIASED_MAGNET_STATIONS / DML_FACING_PAD_CLIPPED / CAD_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Remove the Rev.A magnetic-pad/DML projected overlap discovered by the integrated master DMU.

Do not modify/notch the active DML as the baseline solution.

## 2. Authoritative projected regions
Product:
X=0..320
Y=0..400.

DML:
X=10..310
Y=10..390.

Front carrier outer:
X=0.8..319.2
Y=0.8..399.2.

Nominal perimeter ring:
10 mm class.

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

These replace the Rev.A seed centers for next CAD generation.

## 4. Geometric problem
A symmetric diameter-12-mm station pad around any of these centers still crosses the DML projected edge.

Therefore station support cannot remain a simple full circular boss.

## 5. Rev.B pad topology
Use perimeter-biased D-shaped / truncated station support.

The magnet pocket remains circular.

The structural pad around the pocket is extended toward the product perimeter and clipped on the DML-facing side.

This separates:
- magnetic pocket geometry;
- supporting polymer geometry;
- DML keep-out.

## 6. Pocket geometry
Magnet pocket baseline remains:
- diameter 6.6 mm;
- Candidate A 6 x 2 mm magnet;
- local process allowance;
- rear-loaded;
- mechanical capture required.

The circular pocket may geometrically approach the DML edge, but no rigid rear protrusion may violate the DML Z clearance.

## 7. DML-facing hard boundary
For pad material that projects rearward into the DML Z region:
- top stations: pad DML-facing edge Y >=390 mm preferred;
- bottom: edge Y <=10 mm preferred;
- left: edge X <=10 mm preferred;
- right: edge X >=310 mm preferred.

Because the magnet center itself is only 2 mm from the DML edge in Rev.B, a 6.6 mm pocket cannot be fully contained outside the DML projection.

Therefore a pure same-Z perimeter pocket is geometrically impossible.

## 8. Required architectural correction
The magnet pocket must use one of two legal Z strategies:

### Strategy F — forward pocket
Place magnet/pocket predominantly forward of the DML front plane in the front-carrier perimeter stack, so XY projection may overlap the DML edge without physical collision.

### Strategy O — outward shift
Move magnet center farther toward product edge enough that the complete 6.6 mm pocket plus structural wall lies outside DML projection.

For a 6.6 mm pocket and minimum ~1.0 mm local polymer wall, required half-width is approximately:
3.3 + 1.0 = 4.3 mm.

Thus center should be at least 4.3 mm outside the DML projected boundary.

With DML edge X=10, legal left center would be X<=5.7 mm.
With carrier outer edge at X=0.8, available outward material becomes too small for a robust symmetric pocket.

Equivalent issue exists at all four edges.

## 9. Selected baseline
Select **Strategy F — forward pocket**.

Reason:
- preserves 320 x 400 footprint;
- preserves DML 300 x 380;
- avoids weakening DML;
- avoids an unrealistically thin outer carrier wall;
- allows the magnet to overlap DML in XY while remaining separated in Z.

This is the key Rev.B correction.

## 10. Forward-pocket Z
Product-global:
- fabric outer Z0;
- fabric rear ~Z0.5;
- DML front Z3.3.

Magnet thickness:
2.0 mm.

Target magnet front/rear envelope seed:
**Z0.8..2.8 mm**

This keeps nominal rear magnet face:
0.5 mm forward of DML front Z3.3.

Add nonmagnetic rear pocket floor / compliant isolation as required.

Hard requirement:
magnet/capture rigid geometry rear extent **<Z3.0 mm nominal** before tolerance closure.

## 11. DML front clearance
Nominal:
DML front Z3.3.

Magnet/capture rear limit target:
Z<=2.8.

Nominal residual:
>=0.5 mm.

This is a local perimeter clearance, separate from the central 2.8 mm fabric-DML acoustic gap.

Worst-case tolerance must remain positive.

## 12. Carrier local geometry
At magnetic station:
- fabric wraps over front;
- magnet is embedded in carrier thickness forward of DML;
- rear support is clipped flush/forward;
- no 3.2 mm rear boss is permitted over DML projection.

Therefore Rev.A 3.2 mm rearward local station thickening is retired where it overlaps DML projection.

## 13. Target-side architecture
Steel target remains on product-side legal perimeter structure.

Target may sit rearward of front magnet with a controlled magnetic gap, but cannot require a rigid bridge through the DML active region.

A local non-DML perimeter target bracket is allowed.

Exact magnetic circuit requires 3D force validation.

## 14. Carrier ring consequence
The 1.8 mm carrier base may locally use front-side thickening hidden by the fabric edge/wrap geometry.

Visible front flatness must remain acceptable.

Do not create visible magnet bumps.

## 15. Alternative if front-side thickening is cosmetically poor
Fallback:
replace 6 x 2 mm magnet with thinner Candidate B or a smaller/thinner magnet family, then re-run force budget.

Do not reduce DML size solely for magnet packaging unless all other options fail.

## 16. Revised collision interpretation
XY overlap alone is no longer a hard collision for front magnets.

Collision is 3D:
- same XY;
- overlapping Z.

The Rev.B solution intentionally permits limited XY projection overlap while enforcing Z separation.

## 17. Required real CAD regeneration
Generate carrier Rev.B with:
- Rev.B centers;
- forward magnet pockets;
- no rearward 3.2 mm boss over DML;
- D-shaped perimeter reinforcement;
- peel recess;
- LOC_A/LOC_B.

Then transform into product-global coordinates.

## 18. Acceptance checks
- one valid solid;
- no carrier/magnet rigid volume intersects DML solid;
- magnet rear face/capture remains forward of DML front with tolerance;
- carrier remains printable;
- pocket floor/capture mechanically viable;
- no visible front bump;
- magnetic force remains tunable to 20..30 N total.

## 19. Automatic checks
C431 Rev.B magnet centers used.
C432 symmetric 12 mm rear boss retired.
C433 DML is not notched baseline.
C434 outward-only strategy evaluated and rejected as baseline.
C435 forward-pocket strategy selected.
C436 magnet nominal Z envelope 0.8..2.8 mm seed.
C437 DML front remains Z3.3.
C438 nominal magnet-to-DML local Z residual >=0.5 mm.
C439 no rear boss over DML projection.
C440 XY overlap is evaluated as 3D collision, not 2D failure.
C441 target does not bridge active DML.
C442 visible front bump prohibited.
C443 thinner magnet fallback retained.
C444 exact magnetic force still validation gate.
C445 real Rev.B B-rep regeneration required.

## 20. State
The previous idea of solving the conflict only by moving centers 2 mm outward and clipping a 12 mm boss is insufficient.

The geometrically correct solution is:
**embed the magnet forward of the DML front plane**.

Status:
**FRONT_MAGNET_FORWARD_POCKET_SELECTED / MAGNET_Z0P8_TO_2P8 / DML_FRONT_Z3P3 / NOMINAL_LOCAL_CLEARANCE_0P5MM / C01_TO_C445 / REAL_BREP_REGEN_NEXT**.
