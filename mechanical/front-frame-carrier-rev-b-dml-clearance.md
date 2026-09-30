# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **MAGNET_STATIONS_REV_B_GEOMETRY_FROZEN / DML_HARD_PROJECTION_CLEAR / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic-station overlap detected by the integrated master DMU.

The DML active/projected hard region is not modified to accommodate magnetic hardware.

## 2. Authoritative product coordinates
Product:
320 x 400 mm.

DML hard projected rectangle:
X = 10..310 mm
Y = 10..390 mm.

The DML-facing boundary of every rigid magnet pad and target support must remain outside this rectangle, with an additional manufacturing clearance where possible.

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

These are magnet-center seeds, not circular-pad centers for an unconstrained 12 mm disc.

## 4. D-shaped pad principle
Each station uses a perimeter-biased pad.

The pad is generated from a nominal local support region and Boolean-clipped by the DML hard projection plus clearance.

The DML-facing side is flat/truncated.

No circular 12 mm pad is retained as a production assumption.

## 5. DML clearance offset
Define:
K_DML_MAG = DML projected rectangle expanded outward by a clearance parameter.

Seed:
**0.5 mm rigid clearance**

Sweep:
0.3 / 0.5 / 0.8 mm.

Rigid pad material is subtracted wherever it intersects this expanded DML keep-out.

The magnet itself must also remain outside the DML hard projection or be moved farther outward.

## 6. Magnet feasibility correction
A diameter 6 mm magnet centered only 2 mm from the DML edge would geometrically cross the DML projection.

Therefore the Rev.B center seeds at 12/308/388/12 are still insufficient for a full 6 mm circular magnet if the DML projection is treated as a strict full-depth keep-out.

Required center distance from DML edge for a 6 mm magnet plus 0.5 mm clearance:
**3.5 mm minimum**.

Hence legal center coordinates become at least:
- left X <= 6.5 mm
- right X >= 313.5 mm
- bottom Y <= 6.5 mm
- top Y >= 393.5 mm.

This is the actual geometric condition.

## 7. Rev.C legal-center candidate
Adopt next kernel seed:
Top:
M1C = (70,394)
M2C = (250,394)

Bottom:
M3C = (70,6)
M4C = (250,6)

Left:
M5C = (6,135)
M6C = (6,275)

Right:
M7C = (314,135)
M8C = (314,315).

For radius 3.0 mm:
- top lower edge Y391 > DML top390;
- bottom upper edge Y9 < DML bottom10;
- left right edge X9 < DML left10;
- right left edge X311 > DML right310.

Minimum nominal magnet-to-DML projected gap:
**1.0 mm**.

This exceeds the 0.5 mm seed.

## 8. Product-edge feasibility
Carrier outer boundary:
X0.8..319.2
Y0.8..399.2.

For 6 mm magnets at centers 6/314/394:
- minimum outer magnet edge = 3.0 mm;
- maximum outer edge = 317.0 or 397.0 mm.

Thus the magnet discs remain inside the carrier projected outer boundary with approximately:
**2.2 mm minimum carrier-edge material envelope before pocket/capture detail**.

This is tight but geometrically feasible.

## 9. Local pad topology
Because only ~2.2 mm remains to the outer carrier boundary, station reinforcement must extend mainly tangentially along the perimeter, not outward.

Use capsule/D-shaped local reinforcement:
- tangential length 12..16 mm;
- inward edge clipped by DML keep-out;
- outward edge clipped by carrier structural edge;
- local Z thickening supplies pocket depth.

No attempt to create a 12 mm circular boss.

## 10. Local Z
Base carrier:
1.8 mm.

Magnet station total local thickness seed:
3.2 mm.

Magnet:
6 x 2 mm candidate envelope.

Mechanical capture detail remains required.

Local Z thickening shall face the legal side of the front stack and must preserve fabric/DML clearance.

## 11. Target alignment
Product-side steel target center follows the final magnet center.

Target cannot be a 10 mm circular disc if that disc enters DML hard keep-out.

Use local tangential rectangular/segment target geometry sized from magnetic FEA/test.

Initial target seed:
- tangential length 10..14 mm
- radial width 4..6 mm
- thickness 0.8..1.2 mm.

Exact target force area remains open.

## 12. Retention-force consequence
Reducing target area and introducing a controlled gap will reduce force relative to ideal catalogue pull.

This is desirable up to the 20..30 N assembled target.

However geometry alone cannot prove force.

Required:
- magnetostatic model or supplier force-vs-gap estimate;
- then coupon/assembly force measurement.

## 13. Peel recess
Lower-center peel recess remains:
center X160
width28
depth4.

M3C/M4C remain 90 mm from center in X and do not conflict with the recess.

## 14. RF policy
Rev.C outward movement is beneficial because magnetic/steel hardware is pushed farther from internal RF regions.

Still required:
- exact radar cone check;
- exact ESP32 antenna keep-out check.

No magnetic station is accepted solely from perimeter position.

## 15. Fabric land
Magnet pockets/reinforcement may locally interrupt the 6 mm nominal adhesive land only if a continuous alternative bonding path of >=5 mm effective width is preserved around the station.

Fabric must not bridge a sharp pocket edge.

## 16. Kernel generation contract
Generate:
AP22_FRONT_CARRIER_REV_B_DMU

with:
- 318.4 x 398.4 outer boundary;
- 10 mm nominal ring;
- 1.8 mm base;
- Rev.C legal magnet centers;
- tangential clipped reinforcement;
- 6.6 mm process-seed pockets;
- 3.2 mm local station Z;
- lower peel recess;
- locator features when their exact XY is frozen.

Checks:
- one valid solid;
- no rigid pad intersects DML hard projection;
- no magnet envelope intersects DML projection;
- all pockets remain inside carrier;
- carrier ring connectivity preserved;
- peel recess connectivity preserved.

## 17. Automatic checks
C431 Rev.B center seeds shown insufficient for 6 mm magnet strict DML keep-out.
C432 minimum legal center distance derived from magnet radius + clearance.
C433 Rev.C legal centers defined.
C434 all 6 mm magnet envelopes clear DML projection.
C435 nominal magnet-to-DML projected gap >=1.0 mm.
C436 all magnet envelopes remain inside carrier outer boundary.
C437 minimum outer carrier-edge envelope approximately 2.2 mm.
C438 circular 12 mm boss retired.
C439 tangential clipped reinforcement defined.
C440 target disc assumption retired.
C441 tangential target seed defined.
C442 DML geometry is not notched for magnets.
C443 peel recess remains clear.
C444 fabric bonding path remains >=5 mm effective.
C445 exact RF masks still authoritative.
C446 assembled force remains 20..30 N target.
C447 catalogue pull force remains non-authoritative.
C448 real B-rep regeneration required.
C449 real B-rep must remain one connected solid.
C450 DML collision check required on generated solid.

## 18. State
The integrated geometry exposes an important correction:
the earlier Rev.B 2 mm outward move was not enough for a 6 mm magnet.

The geometrically legal seed is now:
M1C (70,394)
M2C (250,394)
M3C (70,6)
M4C (250,6)
M5C (6,135)
M6C (6,275)
M7C (314,135)
M8C (314,315).

Status:
**REV_C_MAGNET_CENTERS_GEOMETRICALLY_DML_CLEAR / 1MM_NOMINAL_DML_GAP / TANGENTIAL_PADS_REQUIRED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
