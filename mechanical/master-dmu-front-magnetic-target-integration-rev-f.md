# AudioPicture V2.2 — master DMU front magnetic target integration Rev.F

Status: **TARGETS_INTEGRATED_AT_NOMINAL_DMU_LEVEL / GLOBAL_Z_COMPATIBLE_ONLY_OUTSIDE_DML / ESP32_COARSE_PASS / RADAR_EXACT_MASK_OPEN**

## 1. Purpose
Integrate the Rev.E magnetic coupon first-article geometry into the master DMU without converting experimental magnetic variables into production-frozen dimensions.

Integrated nominal test configuration:
- 8 x S-04-02-N, 4 x 2 mm;
- 8 x discrete low-carbon-steel targets;
- target first article 7 x 7 x 1.0 mm;
- G_EFF = 0.40 mm;
- current Rev.D station centers.

## 2. Governing global Z
Product-global datum remains:
- fabric outer Z0;
- fabric rear Z0.5;
- DML front Z3.3;
- DML rear Z9.3;
- rear shell outer <=Z40.

Front carrier Rev.D:
- local Z0 -> global Z0.5;
- base carrier global Z0.5..2.3;
- local magnetic station global Z0.5..3.7.

No global datum is changed by this integration.

## 3. Magnet pole and target placement
The Rev.D 2.2 mm pocket depth in a 3.2 mm local station leaves a nominal 1.0 mm front-side floor.

For the 2.0 mm magnet:
- pocket bottom/global front support is nominally Z1.5;
- magnet occupies nominally Z1.5..3.5;
- diagnostic rear capture occupies the local station rear region to approximately Z3.7.

G_EFF is defined between the magnet pole face and target face.

For nominal G_EFF = 0.40 mm:
- target front face nominal = Z3.9 if referenced directly from magnet pole at Z3.5;
- target rear face nominal = Z4.9 for 1.0 mm target.

Because diagnostic capture nubs may locally extend rearward to Z3.7, the exact target-seat geometry must avoid nub interference. A conservative DMU target-seat plane of Z4.1 is used for packaging:
- target Z = **4.1..5.1 mm**.

The 0.2 mm difference is treated as capture/seat packaging allowance, not silently added to the magnetic G_EFF definition.

Production CAD must explicitly separate:
- magnetic pole-to-target G_EFF;
- mechanical capture protrusion;
- target seating datum.

## 4. DML consequence
DML occupies:
- XY X10..310 / Y10..390;
- Z3.3..9.3.

Therefore any target occupying Z4.1..5.1 would collide with the DML if its XY footprint entered the DML projected rectangle.

Hard rule:
**the complete steel target footprint must remain outside the DML projected hard region.**

No target may bridge across the DML edge.

No DML notch is permitted.

## 5. Current station-center check
Rev.D centers:
- top: (70,394), (250,394)
- bottom: (70,6), (250,6)
- left: (6,135), (6,275)
- right: (314,135), (314,315).

A symmetric 7 x 7 mm target extends 3.5 mm from center.

Projected target limits:
- top inner edge Y390.5;
- bottom inner edge Y9.5;
- left inner edge X9.5;
- right inner edge X310.5.

DML boundary:
- top Y390;
- bottom Y10;
- left X10;
- right X310.

Therefore nominal target-to-DML projected clearance is:
**0.5 mm at every station.**

This is geometrically positive but small.

## 6. Target tolerance interpretation
The 0.5 mm nominal target/DML clearance shall not be declared production-safe from nominal CAD alone.

It must absorb:
- target XY tolerance;
- target placement tolerance;
- carrier-to-fixed-frame registration tolerance;
- fixed target-holder tolerance;
- thermal/print variation.

Therefore:
- nominal DMU geometry: PASS;
- production tolerance closure: OPEN.

If tolerance closure cannot preserve positive clearance, preferred corrections are:
1. reduce target transverse dimension;
2. move target/station outward where carrier boundary permits;
3. use an asymmetric target biased outward.

Do not move target inward over DML.

## 7. Carrier outer-boundary check
Carrier projected outer boundary:
X0.8..319.2 / Y0.8..399.2.

7 mm target at current centers:
- top outer edge Y397.5 <399.2;
- bottom outer edge Y2.5 >0.8;
- left outer edge X2.5 >0.8;
- right outer edge X317.5 <319.2.

Nominal minimum target-to-carrier projected outer-boundary margin:
**1.7 mm**.

Thus the first-article target fits the carrier perimeter projection.

## 8. ESP32 RF keep-out
Frozen DMU antenna seed:
- ESP32-S3-WROOM-1 at MAIN-C left edge;
- approximate module X79..104.5 / Y333.5..351.5;
- antenna at low-X end;
- conservative enclosure-level 15 mm expansion around exact antenna region.

Nearest relevant magnetic stations remain M1D and M6D.

At packaging-envelope level neither the 4 mm magnet nor 7 mm target is intended to enter ESP32_RF_KO_A.

Result:
**ESP32 magnetic hardware compatibility = COARSE PASS.**

Exact module STEP/antenna-body mask and assembled RF throughput/range test remain mandatory.

## 9. Radar
The repository retains radar Z sweep and an EM-authoritative forward region, but no exact frozen radar antenna/EM hard-mask geometry sufficient for a definitive target intersection calculation is present in this gate.

Therefore:
**RADAR target/magnet compatibility = OPEN.**

No PASS is inferred from distance or visual plausibility.

## 10. Removal path
Lower-center peel recess remains at X160.

Bottom targets remain centered at X70 and X250.

This preserves the intended symmetric spacing from peel initiation.

However exact removal sweep with target holders and final locators is not yet a solved swept-solid result.

Status:
**PEEL TOPOLOGY PASS / EXACT SWEEP OPEN.**

## 11. Target holder architecture
Steel targets belong to the fixed structural side.

Each target requires a local non-DML structural holder/node that:
- positively retains the steel target;
- does not rely on adhesive alone for loose-part safety;
- remains outside DML hard projection;
- does not bridge DML compliant mounting;
- does not enter radar/ESP32 hard masks;
- preserves the selected magnetic pole-to-target G_EFF.

No continuous target rail/ring is allowed.

## 12. Global-depth consequence
Target rear Z <=5.1 mm in this nominal DMU seed.

This is far forward of:
- VOICE/RADAR/ENV PCB Z sweep;
- MAIN-C/MAIN-P;
- rear PC-CF structural band;
- rear shell.

Therefore target depth does not threaten the global 40 mm rear closure.

Its governing collision is the DML XY hard projection, not rear product depth.

## 13. Required next CAD feature
Generate a fixed-side target-holder B-rep family around each current station.

The holder must be clipped by:
- DML hard volume;
- carrier/product perimeter envelope;
- ESP32_RF_KO_A;
- radar hard mask when exact mask becomes available.

Target-holder geometry must expose a controlled target seating plane while keeping target mechanically trapped.

## 14. Automatic checks
C521 master global Z datum unchanged.
C522 Rev.D carrier transform retained.
C523 nominal 4x2 magnet pole position derived from real pocket geometry.
C524 G_EFF kept distinct from mechanical capture allowance.
C525 conservative target DMU Z set to 4.1..5.1 mm for packaging.
C526 target in DML XY projection prohibited because Z overlaps DML.
C527 eight 7x7 target projected envelopes evaluated.
C528 nominal target-to-DML clearance == 0.5 mm.
C529 nominal target-to-carrier outer margin == 1.7 mm.
C530 nominal target projection fits carrier perimeter.
C531 0.5 mm DML target margin not treated as production tolerance PASS.
C532 outward/asymmetric target correction preferred if tolerance fails.
C533 no DML notch allowed.
C534 ESP32 15 mm enclosure RF mask retained.
C535 ESP32 magnetic hardware compatibility coarse PASS only.
C536 exact ESP32 STEP/RF test remains open.
C537 radar exact EM hard-mask geometry remains open.
C538 no radar PASS inferred without exact mask.
C539 peel topology preserved around X160 recess.
C540 exact removal swept-solid gate remains open.
C541 target positively retained on fixed structural node.
C542 adhesive-only target retention prohibited.
C543 target holder may not bridge DML compliant mount.
C544 target depth does not consume governing rear 40 mm closure.
C545 target-holder real B-rep required next.

## 15. State
Nominal first-article magnetic targets can be integrated into the global-Z package without changing the 40 mm envelope.

The limiting issue is not rear depth. It is the small **0.5 mm nominal XY clearance between each 7 mm target and the DML projection**.

This is sufficient for a nominal DMU placement but not sufficient to claim production tolerance closure.

Status:
**8X_TARGET_7X7X1_DMU_NOMINAL_PASS / TARGET_Z_4P1_TO_5P1 / DML_MARGIN_0P5_NOMINAL_ONLY / ESP32_COARSE_PASS / RADAR_EXACT_MASK_OPEN / C01_TO_C545 / TARGET_HOLDER_BREP_NEXT**.
