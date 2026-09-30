# AudioPicture V2.2 — front-frame magnetic station Rev.C final geometry

Status: **DML_COMPATIBLE_MAGNET_STATION_GEOMETRY_FROZEN / RF_MASK_OVERRIDE_RETAINED / FORCE_COUPON_GATE_ONLY**

## 1. Problem closed
DML projection:
X=10..310, Y=10..390 mm.

Front carrier:
X=0.8..319.2, Y=0.8..399.2 mm.

Available projected perimeter annulus:
9.2 mm nominal.

The previous 12 mm circular magnet pad cannot fit entirely in this annulus.
The 6 mm magnet itself can.

Therefore the incompatible feature is retired:
- 12 mm circular station pad: RETIRED
- 10 mm radial steel target: RETIRED.

## 2. Final station section
Magnet:
S-06-02-N packaging reference
- magnet diameter 6.0 mm
- magnet thickness 2.0 mm
- pocket diameter 6.6 mm process seed.

Carrier station pad:
**8.4 mm radial x 12.0 mm tangential**
with rounded ends/corners.

Radial position:
carrier outer-side edge >=1.0 mm from product edge;
DML-facing pad edge <=9.8 mm product coordinate equivalent on left/bottom, or >=310.2 mm on right/top.

This preserves at least 0.2 mm projected separation from the nominal DML boundary before tolerance allocation.

## 3. Tolerance-safe DML separation
Production target projected gap between rigid magnetic pad and DML:
**>=0.8 mm nominal**

Hard minimum after XY tolerance:
**>=0.3 mm**

This is separate from fabric-to-DML Z clearance.

To achieve this, pad width may locally reduce from 8.4 to 8.0 mm after print-process capability is known.

No pad may touch the DML or compliant foam path.

## 4. Steel target
Final target seed:
**8.0 mm radial x 10.0 mm tangential x 0.8 mm thick**
low-carbon steel class.

Target is mechanically trapped in a legal perimeter support feature.

No 10 x 10 target baseline.

Target DML-facing edge obeys the same hard projected clearance.

## 5. Station center lines
Nominal side center line:
X=5.4 mm left
X=314.6 mm right.

Nominal bottom/top center line:
Y=5.4 mm bottom
Y=394.6 mm top.

These lines place an 8.4 mm radial pad from 1.2 to 9.6 mm, leaving 0.4 mm nominal to DML.

Preferred final pad width after tolerance study:
8.0 mm -> 1.4..9.4, leaving 0.6 mm nominal.

## 6. Eight-station layout
To reduce RF concentration and keep symmetric peel behavior:

M1C top-left = (70,394.6)
M2C top-right = (250,394.6)

M3C bottom-left = (70,5.4)
M4C bottom-right = (250,5.4)

M5C left-lower = (5.4,135)
M6C left-upper = (5.4,275)

M7C right-lower = (314.6,135)
M8C right-upper = (314.6,315).

All are outside the DML projected rectangle when the final narrow pad geometry is used.

## 7. RF override
These coordinates are mechanically frozen seeds, not permission to violate an exact RF mask.

Automatic rule:
if any station intersects the final ESP32 or radar keep-out, slide it tangentially along its same perimeter side.

Do not move it radially toward DML.

Maximum initial tangential search:
+/-35 mm.

If no legal location exists on that side, reassign that station to another legal perimeter side while maintaining total count 8 or use validated 6-station force equivalent.

## 8. Radar coarse check
Radar board:
X249..287, Y184..216.

The right-side stations:
M7C Y135
M8C Y315

are separated tangentially from the radar board by 49 mm and 99 mm respectively at the nearest board edge.

They are also at X314.6, outside the radar board envelope.

The exact forward 45-degree packaging cone remains authoritative; final EM mask check is still required.

## 9. ENV coarse check
ENV:
X252..294, Y35..59.

M4C:
(250,5.4), separated in Y by ~29.6 mm from ENV board lower edge.

M7C:
Y135, separated by 76 mm from ENV upper edge.

Coarse PASS.

## 10. VOICE coarse check
VOICE:
X119..201, Y20..102.

Bottom stations:
X70 and 250, Y5.4.

They remain outside VOICE board XY envelope.

Coarse PASS.

## 11. DML mount
The magnetic target/pad shall not bridge the compliant PORON DML mount.

DML foam support remains approximately 5..6 mm at panel edge.

Magnetic system belongs to the cosmetic front-carrier/product perimeter interface, structurally independent of the compliant DML retention.

## 12. Z architecture
Magnet station local thickening remains front-perimeter-only.

The local 3.2 mm carrier station thickness shall be positioned outside the DML projected region.

Therefore it does not consume the active fabric-to-DML 2.8 mm gap.

This removes the prior Z conflict between local magnet pads and active DML clearance.

## 13. Force architecture
Eight stations retained.

Total assembled normal retention target:
20..30 N.

Average target:
2.5..3.75 N/station.

Force is tuned by:
- effective magnetic gap;
- 8 x 10 x 0.8 steel target;
- optional nonmagnetic shim.

Catalogue direct-contact pull force remains non-authoritative.

## 14. Final magnetic gap coupon
Required small subassembly coupon only, not full product prototype.

Coupon matrix:
G_MAG 0.5 / 0.8 / 1.0 / 1.2 mm
target thickness 0.8 / 1.0 mm
candidate magnet S-06-02-N.

Measure:
- normal pull;
- lateral shear;
- peel initiation;
- temperature 20 / 40 / 60 C where practical.

Select stack giving 2.5..3.75 N/station mean with acceptable tolerance.

## 15. Failure safety
Magnet:
mechanically trapped.

Steel target:
mechanically trapped.

Adhesive:
secondary retention only.

No loose magnetic item can enter DML/electronics cavity.

## 16. Automatic checks
C431 old 12 mm circular pad retired.
C432 old 10 mm radial target retired.
C433 magnet pocket remains compatible with 6 mm magnet.
C434 station radial pad <=8.4 mm.
C435 preferred station radial pad 8.0 mm available.
C436 target radial width <=8.0 mm.
C437 station pad outside nominal DML projection.
C438 target outside nominal DML projection.
C439 hard pad/DML projected clearance >=0.3 mm after tolerance.
C440 no magnetic feature bridges DML compliant mount.
C441 M1C..M8C generated.
C442 bottom stations clear VOICE coarse envelope.
C443 right-lower/right-upper stations clear RADAR board coarse envelope.
C444 lower-right station clears ENV coarse envelope.
C445 exact radar RF mask can tangentially relocate stations.
C446 exact ESP32 RF mask can tangentially relocate stations.
C447 radial relocation toward DML prohibited.
C448 local magnetic Z thickening outside active DML projection.
C449 magnetic force coupon defined.
C450 no full-product prototype required for magnetic force gate.

## 17. State
Final compatible station geometry:
- 6 x 2 mm magnet class;
- 6.6 mm pocket;
- 8.0..8.4 mm radial carrier pad;
- 12 mm tangential pad;
- 8 x 10 x 0.8 mm target seed;
- perimeter centerline 5.4 mm / complementary opposite edge;
- eight distributed stations.

The DML does not need to be notched or reduced.

Status:
**MAGNET_STATION_REV_C_DML_COMPATIBLE / 8_STATIONS / NO_DML_NOTCH / C01_TO_C450 / FORCE_COUPON_AND_EXACT_RF_MASK_GATE**.
