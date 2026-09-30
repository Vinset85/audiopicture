# AudioPicture V2.2 Rev.B — front carrier with perimeter-clipped magnetic pads

Status: **REV_B_MAGNET_PAD_TOPOLOGY_FROZEN / DML_PROJECTED_OVERLAP_REMOVED_BY_CONSTRUCTION / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A front-carrier magnetic-pad overlap with the DML projected perimeter without modifying or notching the DML.

The solution is geometric-by-construction:
magnetic station support material is clipped to legal product-perimeter bands.

## 2. Fixed product geometry
Product:
320 x 400 mm.

DML projected area:
X=10..310
Y=10..390 mm.

Carrier nominal outer projected boundary:
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

These centers are packaging seeds, not independent proof of DML clearance.

## 4. DML hard projection
No rigid magnetic station feature may project into the DML hard zone unless explicitly allowed by a later DML-edge mechanical interface model.

Baseline:
**zero magnetic-pad projected overlap with DML hard zone**.

No DML notch.

## 5. Legal perimeter bands
Define legal magnetic support bands outside the DML projection:

BOTTOM_BAND:
Y < 10 mm.

TOP_BAND:
Y > 390 mm.

LEFT_BAND:
X < 10 mm.

RIGHT_BAND:
X > 310 mm.

Because the carrier outer edge is inset to 0.8/319.2/399.2, usable band width is approximately 9.2 mm.

## 6. D-shaped pad construction
Start from a circular local station pad envelope.

Seed circle:
diameter 12 mm.

Then intersect with:
- carrier material;
- corresponding legal perimeter band.

The DML-facing side becomes flat/clipped at the DML projection boundary.

The resulting feature is D-shaped or segment-shaped rather than a full circle.

## 7. Magnet pocket vs pad
A 6.6 mm magnet pocket centered at only 2 mm outside the DML boundary cannot itself remain entirely outside the DML projection:
radius 3.3 mm > 2 mm center offset.

Therefore simply clipping the 12 mm support pad is insufficient if the magnet pocket center remains at MxB.

This is a second-order collision discovered by dimensional closure.

## 8. Required magnet-center offset
For a 6.6 mm pocket to remain entirely outside the DML projected zone with clearance C_EDGE:

center offset from DML boundary >= 3.3 + C_EDGE.

Use C_EDGE=0.5 mm seed.

Required center offset:
**>=3.8 mm**.

Therefore legal center coordinates should be at least:

BOTTOM:
Y <= 6.2 mm.

TOP:
Y >= 393.8 mm.

LEFT:
X <= 6.2 mm.

RIGHT:
X >= 313.8 mm.

These positions conflict with the 10 mm ring centerline concept and approach the carrier outer edge.

## 9. Consequence
A conventional 6 mm-class circular magnet embedded flat in the front carrier perimeter is not geometrically compatible with:
- DML extending to 10 mm from product edge;
- carrier outer edge at 0.8 mm;
- adequate material around the pocket;
- zero projected overlap.

Therefore Rev.B shall not force the existing 6 x 2 mm magnet into an inadequate perimeter section.

## 10. Preferred architecture change
Move the magnetic circuit out of the front-face/DML coplanar projection.

Preferred:
**edge-tab magnetic retention**.

Front carrier grows local rearward/perimeter tabs outside the DML plane.

Magnets mount in tabs that engage targets on the rear structural/cosmetic perimeter at a different Z plane.

This preserves:
- DML projection;
- front carrier thin ring;
- 6 mm-class magnet candidate;
- serviceability.

## 11. Edge-tab topology
At each station:
- thin carrier ring remains acoustically clean;
- local tab extends rearward at the outer perimeter;
- magnet axis remains approximately product-normal where possible;
- magnet center is placed outside DML projected hard volume in 3D, not merely 2D;
- target is attached to matching non-RF perimeter structure.

Tab must not become a rigid bridge into the DML compliant mount.

## 12. Tab seed dimensions
Initial parametric tab:
- tangential width 14..18 mm;
- radial/perimeter width 5..8 mm;
- rearward Z depth 3.0..5.0 mm local;
- root fillet >=1.5 mm;
- magnet pocket 6.6 mm class.

Exact shape is station-specific near RF keep-outs.

## 13. Front Z impact
The tab is placed at perimeter and rearward, not into the central fabric-DML gap.

Therefore:
- nominal fabric-DML gap remains 2.8 mm;
- active DML front clearance is unchanged.

## 14. Retention-force architecture
Target total remains:
20..30 N assembled.

Eight stations remain baseline.

Controlled magnetic gap remains:
0.5/0.8/1.0/1.2 mm sweep.

Moving the magnetic circuit rearward/perimeter does not change the force requirement.

## 15. Peel behavior
Lower tabs M3/M4 remain separated from center peel recess.

Peel initiation at X160 releases lower magnetic stations sequentially through carrier flexure.

Tab root stiffness is included in peel simulation/test.

## 16. RF constraints
Edge tabs are still rejected if they enter:
- radar keep-out;
- ESP32 antenna keep-out;
- microphone acoustic path;
- OPT3004 optical path.

Targets remain discrete.

No continuous steel.

## 17. Revised CAD feature family
Feature:
MAG_EDGE_TAB(station, tangent_width, radial_width, z_depth, pocket_d, gap_stack).

Boolean order:
1. base carrier ring;
2. locator features;
3. peel recess;
4. legal edge tabs;
5. magnet pockets;
6. mechanical capture features;
7. RF/sensor keep-out cuts;
8. final fillets.

## 18. Rev.A feature retirement
Retire:
- full 12 mm circular coplanar magnet pads;
- assumption that M1B..M8B alone solve DML collision.

Retain:
- eight-station distribution concept;
- 6 mm-class magnet candidate family;
- total retention target;
- magnet-to-steel circuit.

## 19. DMU checks
The next real kernel generation shall test:
- single connected carrier solid;
- no intersection with DML hard volume;
- no tab intrusion into active fabric-DML gap;
- no collision with DML compliant perimeter;
- no collision with rear frame;
- no collision with rear shell;
- peel recess continuity;
- magnet insertion/capture path;
- removal sweep.

## 20. Automatic checks
C431 zero coplanar magnetic-pad overlap with DML hard projection.
C432 no DML notch used.
C433 6.6 mm pocket edge requirement calculated.
C434 M1B..M8B center shift alone declared insufficient.
C435 full circular Rev.A pads retired.
C436 edge-tab magnetic architecture selected.
C437 active fabric-DML gap unchanged.
C438 magnet candidate family retained.
C439 target retention remains 20..30 N.
C440 eight stations retained baseline.
C441 edge-tab root fillet >=1.5 mm seed.
C442 edge-tab Z depth sweep 3..5 mm.
C443 tab does not bridge DML compliant mount.
C444 tab rejects radar RF keep-out.
C445 tab rejects ESP32 RF keep-out.
C446 target remains discrete.
C447 no continuous steel.
C448 peel recess remains clear of lower tabs.
C449 real B-rep regeneration required.
C450 full 3D DML intersection must equal zero before release.

## 21. State
The integrated dimensional check shows that a 6.6 mm pocket cannot be safely embedded in the narrow 9.2 mm coplanar perimeter while maintaining zero DML projected overlap and adequate wall material.

The correct solution is not to shrink margins artificially.

Rev.B therefore changes the magnetic mounting topology to **rearward perimeter edge tabs**.

Status:
**COPLANAR_MAGNET_PAD_REJECTED / EDGE_TAB_MAGNET_ARCHITECTURE_SELECTED / DML_NOT_MODIFIED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
