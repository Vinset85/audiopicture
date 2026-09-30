# AudioPicture V2.2 Rev.B — front carrier magnetic-pad DMU closure

Status: **REV_B_MAGNETIC_STATIONS_REDESIGNED / DML_PROJECTED_COLLISION_CLOSED_BY_DIRECTIONAL_PADS / REAL_KERNEL_REGENERATION_GATE**

## 1. Purpose
Close the front-carrier/DML perimeter conflict identified by the integrated master DMU.

The active DML projected rectangle remains:
- X = 10..310 mm
- Y = 10..390 mm.

No DML notch is introduced.

## 2. Rev.B magnet centers
Adopt:
- M1B = (70,388)
- M2B = (250,388)
- M3B = (70,12)
- M4B = (250,12)
- M5B = (12,135)
- M6B = (12,275)
- M7B = (308,135)
- M8B = (308,315).

## 3. Why a circular 12 mm pad still fails
A 12 mm diameter pad has radius 6 mm.

At a center 2 mm inside the DML projected boundary, a symmetric circular pad necessarily extends 4 mm into the DML region.

Moving the center alone therefore does not solve the conflict.

## 4. Directional pad concept
Each station uses a perimeter-biased local boss.

The DML-facing side is clipped at the DML hard boundary plus a clearance allowance.

Define:
DML_PAD_CLR = 0.5 mm nominal seed.

Legal limits for carrier magnetic boss material:
- top stations: Y >= 390.5
- bottom stations: Y <= 9.5
- left stations: X <= 9.5
- right stations: X >= 310.5.

Because magnet centers remain at 388/12/12/308, the magnet itself cannot be housed entirely in a boss that obeys these limits.

Therefore the Rev.B conclusion is important:
**the magnet center itself must move outside the DML projected rectangle, not only the pad.**

## 5. Rev.C-compatible corrected center seeds
To house a 6.6 mm pocket with 0.5 mm minimum structural wall toward DML, minimum center distance from DML boundary is:
3.3 + 0.5 = 3.8 mm.

Corrected legal centers:
Top:
- M1C = (70,394)
- M2C = (250,394)

Bottom:
- M3C = (70,6)
- M4C = (250,6)

Left:
- M5C = (6,135)
- M6C = (6,275)

Right:
- M7C = (314,135)
- M8C = (314,315).

These centers are 4 mm beyond the DML projected boundary.

## 6. Product-edge feasibility
Carrier outer projected boundary:
X=0.8..319.2
Y=0.8..399.2.

At center coordinate 6 mm, a 6.6 mm pocket reaches 2.7 mm from product datum, leaving ~1.9 mm between pocket edge and carrier outer boundary at 0.8 mm.

At center 314 mm, same result mirrored.

At Y394/6 likewise.

This is tight but geometrically feasible for the magnet pocket.

A symmetric 12 mm boss is not feasible because it would approach/cross the carrier edge.

Therefore local boss is D-shaped/asymmetric:
- magnet pocket remains circular;
- structural material grows preferentially along the perimeter/tangential direction and away from product edge;
- DML-facing wall minimum controlled.

## 7. Local station envelope
Pocket:
- diameter 6.6 mm.

Minimum DML-facing wall:
- 0.5 mm seed.

Minimum outer-edge wall:
- 1.5 mm target where geometry permits.

Tangential boss length:
- 12..16 mm seed.

Radial boss width:
- generated from legal boundary constraints, not fixed diameter.

Local thickness:
- 3.2 mm first CAD seed.

## 8. DML collision criterion
For every station:
intersection(
  magnetic_boss_solid,
  DML_PROJECTED_HARD_KEEP_OUT
) = 0.

The keep-out is extruded through the relevant carrier local Z range.

This is a hard boolean test.

## 9. Pocket collision criterion
The 6.6 mm magnet pocket itself must also not intersect the DML hard keep-out.

This prevents a nominally legal boss with an illegal magnetic body.

## 10. Magnetic circuit consequence
Moving centers from 12/308/388 to 6/314/394 shifts magnetic targets closer to the product perimeter.

Rear/product-side target features must be added to corresponding legal perimeter structural regions.

No steel target may bridge onto the DML compliant support.

## 11. Peel recess
Lower peel recess remains:
- center X=160
- width 28 mm
- depth 4 mm.

It remains far from M3C/M4C at X70/250.

No change required.

## 12. RF
M7C/M8C remain subject to radar/ESP32 exact keep-outs.

Passing the DML boolean does not imply RF release.

If RF mask rejects a right-side station, tangential Y relocation is preferred before moving radially inward.

## 13. Carrier connectivity
Directional pads must union into the 10 mm perimeter ring.

Required:
solid_count == 1.

No floating boss is allowed.

## 14. Z integration
Carrier local magnetic pad thickness:
3.2 mm.

Global transform must preserve:
- fabric seating;
- >=2.0 mm worst-case fabric-DML gap;
- no local boss intrusion into active DML volume.

The corrected radial placement allows the boss to occupy perimeter-only product space.

## 15. Mass expectation
Rev.A real carrier:
26.888 cm3
~28.2..29.6 g ASA.

Replacing circular local pads with directional pads is expected to change mass only slightly.

Release target remains:
carrier <=35 g preferred,
<=60 g hard subsystem carrier budget.

Actual regenerated B-rep mass is authoritative.

## 16. Automatic checks
C431 Rev.B center-only move identified as insufficient.
C432 symmetric 12 mm pad rejected.
C433 minimum pocket-to-DML center offset derived.
C434 corrected M1C/M2C Y=394.
C435 corrected M3C/M4C Y=6.
C436 corrected M5C/M6C X=6.
C437 corrected M7C/M8C X=314.
C438 6.6 mm pocket remains inside carrier outer boundary.
C439 outer-edge wall target evaluated.
C440 D-shaped/asymmetric boss required.
C441 boss/DML intersection must equal zero.
C442 pocket/DML intersection must equal zero.
C443 boss unions with perimeter ring.
C444 final carrier solid count must equal one.
C445 no DML notch introduced.
C446 steel target remains discrete.
C447 target does not bridge DML compliant support.
C448 peel recess unchanged and clear.
C449 RF masks remain separate hard gate.
C450 regenerated real B-rep required for release.

## 17. State
The Rev.B analysis found that the previously proposed centers at 12/308/388 mm still cannot solve the DML conflict with a 6.6 mm magnet pocket.

Corrected legal seed centers are therefore:
- top Y394
- bottom Y6
- left X6
- right X314.

This is a deliberate engineering correction before generating a false-positive CAD pass.

Status:
**MAGNET_CENTERS_CORRECTED_TO_PRODUCT_PERIMETER / DIRECTIONAL_BOSS_REQUIRED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
