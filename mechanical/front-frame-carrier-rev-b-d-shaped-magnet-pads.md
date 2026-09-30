# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnet stations

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_PROJECTION_CONFLICT_REMOVED_BY_CONSTRUCTION / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A circular magnet-pad conflict found by the integrated master DMU.

The DML projected hard region is:
- X=10..310 mm
- Y=10..390 mm.

The front carrier magnet support shall not extend into the DML-facing hard-clearance region.

## 2. Revised magnet centers
Rev.B seeds:

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

These supersede the Rev.A centers for CAD generation.

## 3. Problem with circular pads
A 12 mm circular station around a center only 2 mm from the DML projected edge necessarily enters the DML projection.

Therefore a centered circular 12 mm pad is rejected for Rev.B.

The magnet itself is only 6 mm class and can be packaged using a perimeter-biased local lobe integrated with the carrier ring.

## 4. D-shaped station concept
Each station has:
- magnet pocket axis at the listed center;
- outer/perimeter side with sufficient polymer support;
- DML-facing side clipped by a straight chord/keep-out plane;
- local reinforcement extending away from DML.

The D shape is not cosmetic; it is generated from the DML hard boundary.

## 5. DML-facing clipping planes
Top stations:
carrier reinforcement must not extend below Y=390 minus the explicitly allowed perimeter interface tolerance.

Bottom:
must not extend above Y=10 plus allowed interface tolerance.

Left:
must not extend right of X=10 plus allowed interface tolerance.

Right:
must not extend left of X=310 minus allowed interface tolerance.

Because the magnet center itself is inside the nominal DML projected rectangle by 2 mm in these seeds, the magnet pocket cannot satisfy a strict zero-overlap rule if the DML projection is treated as an infinite full-thickness hard solid.

Therefore the master rule is refined:
- DML active structural volume is authoritative in 3D;
- front-carrier station may overlap DML XY projection only if it remains entirely forward of DML front and preserves the >=2.0 mm functional fabric/DML clearance;
- no rearward station material may enter the DML 3D solid or its service-motion envelope.

This resolves the false 2D-only conflict while preserving real 3D clearance.

## 6. Global Z placement
Product-global:
- fabric outer Z=0;
- fabric rear Z~0.5;
- DML front Z=3.3.

Rev.B station maximum rear extent target:
**Z<=2.8 mm**

This leaves:
**>=0.5 mm rigid-to-DML-front local clearance** at magnet stations.

However the acoustic fabric-to-DML central gap remains nominal 2.8 mm and worst-case >=2.0 mm.

Station structures are perimeter-local and are not allowed over active central DML vibration area without explicit clearance.

## 7. Magnet pocket orientation
The previous 3.2 mm local pad depth is too deep for a front-side station if placed directly in the global front stack.

Rev.B therefore changes the magnetic pocket architecture.

Preferred:
- 6 x 2 mm magnet lies in-plane/perimeter pocket with local front-side floor;
- total station rear extent <=2.8 mm;
- mechanical capture uses lateral/rear cap geometry within the perimeter ring.

Alternative:
- move magnet to product-side fixed structure and place thin steel target in the removable carrier.

The latter may provide a thinner removable-front Z stack and remains a strong option.

## 8. Preferred architecture after Z audit
For Rev.B CAD, preferred magnetic circuit becomes:

**MAGNET ON PRODUCT-SIDE FIXED PERIMETER**
+
**THIN STEEL TARGET ON REMOVABLE FRONT CARRIER**

Reasons:
- removes 2 mm magnet thickness from removable front carrier;
- simplifies fabric carrier Z stack;
- allows target thickness 0.8..1.0 mm class;
- makes carrier pad shallower;
- fixed-side magnet can use structural capture;
- front FRU remains light.

This reverses the earlier Candidate-A packaging assumption but retains the same magnetic component candidate.

## 9. Front-carrier target pad
Rev.B removable carrier contains discrete steel-target pockets.

Target seed:
- 8 x 8 to 10 x 10 mm class;
- thickness 0.8 mm nominal;
- 1.0 mm sensitivity;
- rounded/D-shaped local polymer capture.

Carrier local rear extent target:
<=2.0..2.4 mm where possible.

No continuous steel ring.

## 10. Fixed-side magnet pocket
Fixed product perimeter receives:
- S-06-02-N class 6 x 2 mm magnet;
- mechanically captured pocket;
- adhesive secondary retention;
- controlled G_MAG through carrier polymer/target stack.

Fixed magnet pocket is clipped by:
- DML 3D volume;
- DML service envelope;
- radar RF keep-out;
- ESP32 RF keep-out;
- mic/optical exclusions.

## 11. Retention target unchanged
Total assembled normal retention:
20..30 N.

Eight stations:
2.5..3.75 N average/station assembled target.

Exact force remains an assembly measurement/FEA-magnetic or test gate.

## 12. Removal behavior
Lower peel recess remains:
- center X=160;
- width 28 mm;
- depth 4 mm seed.

Thin front targets reduce front-frame inertia and do not change sequential peel principle.

## 13. RF policy
Steel targets remain prohibited in radar/ESP32 hard RF masks.

If any Rev.B station intersects an exact RF mask:
- move station along perimeter;
- do not shrink the RF keep-out to preserve symmetry.

## 14. Mass consequence
Moving magnets to fixed product side:
- removable front loses ~3.44 g of magnet mass;
- gains thin steel targets.

Total system mass changes negligibly.
Service front mass is reduced.

## 15. CAD boolean order
1. generate 318.4 x 398.4 carrier ring;
2. apply peel recess;
3. generate target station lobes;
4. clip lobes against functional perimeter/DML 3D clearance mask;
5. cut target pockets;
6. add target mechanical capture;
7. add LOC_A/LOC_B;
8. subtract mic/radar/optical exclusions;
9. validate one connected solid;
10. transform to product-global Z;
11. run DML solid intersection.

## 16. Required real-kernel outputs
Next kernel run shall report:
- solid count;
- validity;
- volume;
- mass sensitivity;
- bounding box;
- carrier vs DML intersection volume;
- minimum carrier/DML rigid clearance at stations;
- target pocket connectivity;
- peel-recess connectivity.

## 17. Acceptance
PASS only if:
- one connected carrier solid;
- valid B-rep;
- DML solid intersection volume = 0;
- station rigid clearance >=0.5 mm seed;
- central fabric-DML functional clearance remains >=2.0 mm worst-case;
- all target stations mechanically capturable;
- no RF hard-mask intersection.

## 18. Automatic checks
C431 Rev.B centers replace Rev.A centers.
C432 centered 12 mm circular pads rejected.
C433 station geometry generated from functional keep-outs.
C434 2D projected overlap is not alone classified as 3D collision.
C435 real DML 3D intersection is authoritative.
C436 station rear extent <=2.8 mm if front-side magnetic architecture used.
C437 rigid station-to-DML local clearance >=0.5 mm seed.
C438 central fabric-to-DML worst-case >=2.0 mm.
C439 magnet-on-fixed-side architecture preferred after Z audit.
C440 removable carrier uses thin discrete steel targets baseline.
C441 no continuous steel ring.
C442 fixed magnets mechanically captured.
C443 target pieces mechanically captured.
C444 total assembled retention remains 20..30 N.
C445 RF hard masks override station symmetry.
C446 peel recess retained.
C447 real-kernel intersection-volume report required.
C448 one connected solid required.
C449 valid B-rep required.
C450 exact target/magnet stack force remains open.

## 19. State
The integrated Z audit changes the preferred magnetic architecture:

Rev.A:
magnet in removable front carrier.

Rev.B preferred:
**magnet in fixed product perimeter + thin steel target in removable front carrier**.

This is mechanically cleaner inside the 40 mm front stack and removes the previous deep local front pad.

Status:
**FRONT_CARRIER_REV_B_FIXED_MAGNET_THIN_TARGET / D_SHAPED_PERIMETER_STATIONS / C01_TO_C450 / REAL_KERNEL_AND_3D_INTERSECTION_NEXT**.
