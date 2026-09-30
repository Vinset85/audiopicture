# AudioPicture V2.2 Rev.B — front carrier magnetic station redesign for DML clearance

Status: **MAGNET_STATIONS_REV_B_DEFINED / DML_HARD_PROJECTION_CLEARANCE_POLICY_FROZEN / REAL_BREP_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic pads after the integrated DMU showed overlap with the DML projected perimeter.

DML hard projected rectangle:
- X = 10..310 mm
- Y = 10..390 mm.

No rigid magnet pad may extend into this hard rectangle in the front carrier/DML overlapping Z region.

## 2. Rev.B magnet centers
Top:
- M1B = (70,388)
- M2B = (250,388)

Bottom:
- M3B = (70,12)
- M4B = (250,12)

Left:
- M5B = (12,135)
- M6B = (12,275)

Right:
- M7B = (308,135)
- M8B = (308,315).

## 3. Geometric issue
A centered 6.6 mm magnet pocket has radius 3.3 mm.

At 2 mm center offset from the DML boundary, a conventional symmetric pad/pocket envelope cannot remain completely outside the DML projection.

Therefore merely moving centers from 14 to 12 mm / 386 to 388 mm does not solve the problem if the magnet itself remains in the same Z-overlap plane.

This is a hard geometric fact.

## 4. Architecture correction
The magnetic hardware must be moved out of the DML-overlap Z plane, not merely trimmed in XY.

Rev.B adopts a **rear-stepped perimeter magnetic station**:
- front carrier perimeter remains thin near the DML;
- magnet pocket is shifted rearward in Z only in the outer perimeter strip;
- DML edge remains forward/inside the carrier;
- the magnet occupies a rearward perimeter shelf outside the DML physical edge.

The D-shaped pad is retained as a topology aid, but Z separation is the actual collision solution.

## 5. Perimeter shelf concept
Create local shelf from the outer carrier edge toward the DML edge.

Shelf is bounded by product perimeter and DML edge.

Available nominal strip:
10 mm between product edge and DML edge.

Carrier outer boundary begins at 0.8 mm.

Usable geometric strip is approximately:
9.2 mm before DML projection.

This is enough for a 6.6 mm pocket only if:
- pocket center is placed approximately 4.1..5.0 mm from product edge rather than 12 mm global coordinate convention used for center seeds;
- local walls are minimized but process-qualified;
- or magnet is partially behind a structural return.

## 6. Corrected center coordinate target
For a 6.6 mm pocket and minimum 1.2 mm outer polymer wall:
required center distance from outer carrier edge:
>=4.5 mm.

To remain outside DML edge at 10 mm:
center distance from product edge must satisfy:
center + 3.3 <=10 mm
=> center <=6.7 mm.

Therefore legal center band from product edge is approximately:
**4.5..6.7 mm**.

Choose nominal:
**5.5 mm from product edge**.

## 7. Rev.Candidate coordinates
Using product coordinates:

Top:
- M1C = (70,394.5)
- M2C = (250,394.5)

Bottom:
- M3C = (70,5.5)
- M4C = (250,5.5)

Left:
- M5C = (5.5,135)
- M6C = (5.5,275)

Right:
- M7C = (314.5,135)
- M8C = (314.5,315).

These are the first coordinates that geometrically permit the 6.6 mm pocket to remain outside the DML projected rectangle.

## 8. Pocket wall check
For carrier outer boundary at 0.8 mm and center 5.5 mm from product edge:
distance center to carrier outer edge:
4.7 mm.

Minus pocket radius 3.3:
**1.4 mm nominal polymer wall**.

This meets the 1.2 mm seed minimum with 0.2 mm nominal margin.

This margin is small and requires print/process coupon qualification.

## 9. DML-side clearance
For center 5.5 mm and pocket radius 3.3:
pocket DML-facing edge lies at 8.8 mm from product edge.

DML begins at 10 mm.

Nominal XY clearance:
**1.2 mm**.

Thus the bare 6.6 mm pocket clears the DML projection.

A larger symmetric 12 mm pad does not.

## 10. D-shaped pad
Use a local pad that grows:
- outward toward product perimeter where legal;
- tangentially along perimeter;
- rearward in Z;
- not inward toward DML.

DML-facing pad boundary:
<=9.0 mm from the relevant product edge nominal.

Target nominal DML projected clearance:
>=1.0 mm.

## 11. Pad dimensions
Seed local pad footprint:
- tangential length 12..16 mm;
- inward radial reach limited by DML boundary;
- outer wall follows carrier perimeter;
- local rear thickness 3.0..3.5 mm.

Pocket:
6.6 mm nominal diameter.

Do not require a 12 mm circular boss.

## 12. Mechanical capture
Because radial wall is limited, use rear cap/lip architecture with tangential material carrying the retention load.

Preferred:
- pocket floor toward visible/front side;
- rear snap/heat-staked/ultrasonic or printed cap concept;
- adhesive secondary.

Exact closure process remains open.

## 13. Target location
Product-side steel target must mirror the perimeter station and remain outside:
- DML physical envelope;
- radar/ESP32 RF keep-outs;
- mic/optical paths.

Target can be elongated tangentially to recover magnetic circuit area without moving inward.

## 14. Force consequence
The revised perimeter pocket geometry does not change the 20..30 N assembled target.

However, asymmetric steel targets and increased local gap can lower force.

Therefore magnetic-force test must use the actual Rev.Candidate geometry.

## 15. Peel consequence
Bottom magnets move from Y14/12 to Y5.5.

This increases separation from the center peel recess and supports progressive peel.

Peel recess remains near X160.

## 16. Carrier outer-boundary consequence
The 0.8 mm inset carrier boundary is now structurally relevant.

At 1.4 mm nominal pocket outer wall, dimensional/process error can consume meaningful margin.

Sensitivity:
- carrier inset 0.6 / 0.8 / 1.0 mm;
- pocket diameter actual;
- print XY compensation;
- magnet diameter tolerance.

No production freeze until coupon fit.

## 17. CAD regeneration rules
The next real B-rep shall:
1. start from Rev.A one-solid carrier;
2. remove old M1..M8 circular 12 mm pads;
3. place M1C..M8C;
4. generate tangential D-shaped/perimeter pads;
5. cut 6.6 mm pockets;
6. preserve front-side floor;
7. preserve lower peel recess;
8. verify one connected solid;
9. boolean-intersect carrier rigid magnet features with DML hard projection; required volume = 0;
10. report minimum nominal XY clearance to DML.

## 18. Automatic checks
C431 old M1..M8 stations retired.
C432 intermediate M1B..M8B not treated as collision solution.
C433 legal magnet center band 4.5..6.7 mm from product edge derived.
C434 nominal center distance 5.5 mm selected.
C435 M1C..M8C generated.
C436 6.6 mm pocket outer wall nominal >=1.2 mm.
C437 6.6 mm pocket DML clearance nominal >=1.0 mm.
C438 symmetric 12 mm circular boss prohibited at perimeter station.
C439 pad grows tangentially/outward/rearward, not inward.
C440 DML-facing pad boundary <=9.0 mm from product edge.
C441 target remains outside DML physical envelope.
C442 actual Rev.Candidate magnetic circuit required for force validation.
C443 peel recess remains clear.
C444 carrier-inset sensitivity added.
C445 print XY compensation is production gate.
C446 magnet diameter tolerance is included.
C447 real B-rep must remain one connected solid.
C448 rigid magnet-feature intersection with DML hard projection must equal zero.
C449 minimum DML clearance must be measured from B-rep.
C450 no DML notch introduced.

## 19. State
The Rev.B analysis rejects the tempting but insufficient 12 mm-center solution.

Corrected station center:
**5.5 mm from the applicable product edge**.

Bare 6.6 mm pocket:
- nominal outer polymer wall ~1.4 mm;
- nominal DML projection clearance ~1.2 mm.

The pad is no longer a 12 mm circle; it is a tangential perimeter feature.

Status:
**MAGNET_CENTER_5P5MM_FROM_EDGE / POCKET_DML_CLEARANCE_1P2MM / OUTER_WALL_1P4MM / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
