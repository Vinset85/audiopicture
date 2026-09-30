# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **MAGNET_STATION_REV_B_GEOMETRY_DEFINED / DML_HARD_KEEP_OUT_DRIVES_PAD_SHAPE / REAL_KERNEL_REGEN_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic station geometry after the integrated DMU identified overlap between 12 mm circular pads and the DML projected perimeter.

No DML notch is allowed as the baseline correction.

## 2. Authoritative projected geometry
Product:
X 0..320
Y 0..400.

DML projection:
X 10..310
Y 10..390.

The DML projection is a hard rigid-feature keep-out for front-carrier magnet pads.

A separate compliant/acoustic edge allowance may later increase this keep-out; it may not reduce it without explicit DML release.

## 3. Rev.B magnet centers
Top:
M1B = (70,388)
M2B = (250,388)

Bottom:
M3B = (70,12)
M4B = (250,12)

Left:
M5B = (12,135)
M6B = (12,275)

Right:
M7B = (308,135)
M8B = (308,315).

These are CAD seeds, not yet production-frozen coordinates.

## 4. Fundamental geometry observation
A 6 mm diameter magnet has radius 3 mm.

At center distance 2 mm from the DML edge, a full circular magnet pocket itself crosses the DML projected boundary.

Therefore moving the center from 4 mm to 2 mm from the DML edge does NOT solve the problem if the magnet must remain in the same front Z band.

This invalidates the assumption that pad reshaping alone is sufficient.

## 5. Required architectural correction
The DML hard keep-out applies to rigid features in the DML Z-conflict band.

There are only three legal solution families:

A. move magnet center fully outside DML projection with magnet radius + structural wall allowance;
B. place magnet/target at a different Z where projected XY overlap does not cause physical collision;
C. reduce magnet diameter and redesign pocket while still meeting retention force.

Preferred baseline:
**A — move the magnetic circuit farther toward the product perimeter.**

## 6. Minimum center offset for 6 mm magnet
For magnet radius 3.0 mm and minimum rigid clearance seed 0.5 mm:

required magnet center must be at least:
**3.5 mm outside the DML projected boundary**.

DML starts:
X=10, Y=10
and ends:
X=310, Y=390.

Legal center regions for a 6 mm magnet:
- left: X <= 6.5
- right: X >= 313.5
- bottom: Y <= 6.5
- top: Y >= 393.5.

These regions are very close to the product outer boundary and conflict with the nominal 10 mm front-carrier ring topology.

## 7. Consequence
A conventional 6 mm magnet embedded flat in the same front-carrier plane is geometrically incompatible with:
- DML only 10 mm from product edge;
- 10 mm carrier ring;
- 0.5 mm rigid clearance;
- current wrap/bonding land.

This is a real design conflict and must not be hidden by a D-shaped pad.

## 8. Revised preferred magnetic architecture
Move the **magnets to the product-side/rear perimeter structure** and use thin local ferromagnetic targets in the removable front carrier, or vice versa, at a Z position behind the DML front conflict band.

Preferred Rev.B:
- thin steel target integrated in front carrier perimeter;
- magnet housed in fixed product perimeter/rear structural interface;
- magnetic attraction acts through controlled local gap;
- front carrier no longer requires 2 mm-thick magnet body in the DML-adjacent front Z band.

This reduces front-carrier local Z intrusion.

## 9. Front target geometry
Seed target:
- low-carbon steel;
- 8 x 6 mm rectangular or D-shaped local tab;
- thickness 0.5..0.8 mm initial sweep.

Target may overlap DML XY projection only if its global Z is physically clear and RF/acoustic validation permits; preferred geometry still stays perimeter-biased.

Exact target MPN/material/coating open.

## 10. Fixed-side magnet geometry
Retain 6 x 2 mm N45 Candidate A as packaging reference.

Fixed-side magnet pocket is generated in the non-DML structural perimeter at a legal rearward Z.

This pocket may be tied to:
- ASA shell local nonstructural housing plus mechanical capture; or
- PC-CF structural node outside RF zones.

Avoid PC-CF/radar conflict.

## 11. Force consequence
Moving the magnetic circuit rearward changes effective gap.

Therefore previous G_MAG sweep is retained but must be recalculated from actual:
- polymer wall;
- target thickness;
- air gap;
- assembly tolerance.

Target total assembled retention remains:
20..30 N.

## 12. Front-carrier Rev.B simplification
Remove the eight 3.2 mm-thick magnet bosses from the removable front carrier.

Replace with thin target recess/pocket features.

Benefits:
- lower front mass;
- less local warp;
- more fabric-DML clearance;
- simpler fabric bonding land;
- magnet cannot detach toward DML from removable frame.

## 13. Target station seeds
Retain perimeter station logical positions by X/Y family, but exact center is now solved jointly with fixed-side magnet housing.

Logical stations:
T1 top-left
T2 top-right
T3 bottom-left
T4 bottom-right
T5 left-lower
T6 left-upper
T7 right-lower
T8 right-upper.

Do not freeze old MxB center values as production coordinates.

## 14. RF constraints
No fixed-side magnet or target may enter:
- radar keep-out;
- ESP32 antenna keep-out.

Because magnets are moved rearward, RF validation becomes more important, not less.

No continuous steel ring.

## 15. Acoustic constraints
No target/magnet assembly:
- touches DML;
- bridges compliant DML perimeter;
- creates a rigid short circuit around PORON mount;
- creates buzz/rattle.

## 16. Mechanical retention
Fixed-side magnet:
mechanically captured against adhesive failure.

Front target:
mechanically trapped or bonded in a recessed pocket with secondary capture where practical.

No loose steel part can enter DML/electronics cavity.

## 17. Revised carrier mass expectation
Removing eight local 3.2 mm magnet bosses reduces carrier volume relative to Rev.A.

Adding eight thin steel targets adds local mass.

Exact Rev.B B-rep + target mass shall replace the Rev.A carrier-only mass.

## 18. Rev.B CAD regeneration
Generate:
AP22_FRONT_CARRIER_REV_B_DMU.step

Geometry:
- same 318.4 x 398.4 outer size seed;
- 10 mm perimeter ring;
- 1.8 mm base carrier;
- lower peel recess retained;
- LOC_A/LOC_B retained;
- no 6 x 2 mm magnet bodies in carrier;
- thin target recesses only;
- fabric bonding land preserved.

## 19. Fixed-side magnet carrier
Create a separate CAD feature/body family:
AP22_FRONT_MAGNET_FIXED_STATIONS_REV_A

This belongs to the fixed product structure and is assembled after exact RF/structural keep-out solving.

Do not merge into DML compliant perimeter.

## 20. Automatic checks
C431 DML projection treated as hard rigid-feature keep-out.
C432 6 mm magnet radius included in collision logic.
C433 Rev.B seed center move alone recognized as insufficient.
C434 D-shaped pad not accepted as false collision fix.
C435 DML notch rejected baseline.
C436 flat front-carrier 6 mm magnet architecture withdrawn.
C437 fixed-side magnet architecture adopted baseline.
C438 front carrier uses thin targets instead of 2 mm magnets.
C439 20..30 N total retention target retained.
C440 G_MAG recalculated from actual Rev.B stack.
C441 no continuous steel ring.
C442 fixed magnet mechanically captured.
C443 target cannot detach into DML cavity.
C444 magnetic circuit does not bridge PORON perimeter.
C445 RF keep-outs apply to both magnet and target.
C446 Rev.B carrier B-rep regeneration required.
C447 fixed-side station CAD required.
C448 Rev.A magnet-boss carrier STEP is diagnostic only.
C449 logical eight-station distribution retained.
C450 exact station XY becomes joint carrier/structure optimization.

## 21. State
The attempted D-shaped-pad correction exposed a deeper geometric constraint:

with the DML only 10 mm from the product edge, a flat 6 mm magnet in the removable front-carrier plane cannot be kept outside the DML projection while preserving the existing carrier/bonding architecture.

The correct solution is to move the magnet body to the fixed product-side structure and leave only thin targets in the removable front frame.

Status:
**FRONT_MAGNET_ARCHITECTURE_REVISED / FIXED_SIDE_MAGNETS_PLUS_THIN_FRONT_TARGETS / FALSE_D_SHAPE_FIX_REJECTED / C01_TO_C450 / REV_B_KERNEL_REGEN_NEXT**.
