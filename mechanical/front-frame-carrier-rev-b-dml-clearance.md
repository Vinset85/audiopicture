# AudioPicture V2.2 — front carrier Rev.B DML-clearance CAD result

Status: **REV_B_REAL_BREP_PASS / ONE_VALID_SOLID / MAGNET_RIGID_PADS_OUTSIDE_DML_PROJECTION / DMU_INTEGRATION_READY**

## 1. Objective
Remove the front-carrier Rev.A magnetic-pad overlap with the projected DML hard region while preserving:
- one connected ASA carrier;
- eight magnetic stations;
- 6.6 mm pocket class;
- lower-center peel recess;
- 318.4 x 398.4 mm outer carrier;
- <=3.2 mm local Z extent.

DML projected hard region:
X=10..310 mm
Y=10..390 mm.

## 2. Rev.B architecture
The original circular 12 mm pads are withdrawn.

Rev.B uses perimeter-biased local pads:
- top/bottom: 12 x 8 mm class;
- left/right: 8 x 12 mm class;
- local total thickness 3.2 mm.

The rigid pad body is placed outside the DML projected hard region and joined to the 10 mm carrier ring.

## 3. Station intent vs pocket center
The previous Rev.B station seeds remain useful as attraction/retention layout intent:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

However, a 6.6 mm circular pocket centered at those points would still extend into the DML projection.

Therefore the actual CAD pocket centers are shifted outward.

## 4. Actual Rev.B pocket centers
Top:
- M1P = (70,394)
- M2P = (250,394)

Bottom:
- M3P = (70,6)
- M4P = (250,6)

Left:
- M5P = (6,135)
- M6P = (6,275)

Right:
- M7P = (314,135)
- M8P = (314,315).

These are now the authoritative pocket-center seeds for the Rev.B carrier.

## 5. Pocket geometry
Nominal pocket:
diameter 6.6 mm
depth 2.2 mm class.

Pocket/capture detail remains non-production until:
- print compensation coupon;
- mechanical capture lip/cap;
- assembled-force validation.

## 6. Real CAD-kernel result
Generated using CadQuery/OpenCASCADE.

Kernel validity:
PASS.

Connected solids:
**1**

Volume:
**25.4218 cm3**

Bounding box:
**318.4 x 398.4 x 3.2 mm**.

## 7. Carrier-only mass
ASA density sensitivity:
1.05 g/cm3 -> **26.69 g**
1.10 g/cm3 -> **27.96 g**.

Rev.B carrier-only working mass:
**26.7..28.0 g**.

This excludes fabric, ink, adhesive, magnets, steel targets and pads.

## 8. DML clearance
Rigid magnetic pad geometry is located outside:
X10..310 / Y10..390 DML projected hard region.

Therefore the Rev.A pad/DML projected collision is removed at the rigid-pad level.

A separate tolerance/service clearance still applies at the DML perimeter.

No DML notch is required.

## 9. Peel recess
Lower-center peel recess remains:
28 x 4 mm class around X160.

It does not disconnect the carrier.

It remains separated from bottom magnet pockets at X70 and X250.

## 10. Global Z integration
Local carrier Z remains a CAD-local coordinate.

The master product transform must preserve:
- fabric outer datum Z0;
- nominal 2.8 mm fabric-to-DML gap;
- no rigid pad intrusion into DML hard region.

Because Rev.B pads are outside the DML XY hard projection, their 3.2 mm local rear depth no longer competes directly with active DML clearance.

## 11. Magnetic force consequence
Moving actual pocket centers outward changes target placement and possibly the effective peel curve.

The 20..30 N assembled total-retention target is unchanged.

Actual force must be measured/simulated using:
- real target location;
- G_MAG;
- target thickness;
- local carrier/rear-frame stack.

Do not reuse force assumptions from the old center positions without geometry update.

## 12. STEP artifact
Generated:
**AP22_FRONT_CARRIER_REV_B_DMU.step**

Classification:
DMU / collision / assembly artifact.

Not manufacturing release.

## 13. Automatic checks
C431 Rev.A circular pads withdrawn.
C432 Rev.B perimeter pads generated.
C433 all rigid top pads outside DML Y<=390 hard region.
C434 all rigid bottom pads outside DML Y>=10 hard region.
C435 all rigid left pads outside DML X>=10 hard region.
C436 all rigid right pads outside DML X<=310 hard region.
C437 eight 6.6 mm pocket bores generated.
C438 actual pocket centers recorded.
C439 B-rep validity PASS.
C440 solid count == 1.
C441 volume recorded.
C442 carrier-only mass <35 g.
C443 bounding box remains 318.4 x 398.4 x 3.2.
C444 peel recess preserves connectivity.
C445 no DML notch required.
C446 global Z transform still required at assembly level.
C447 assembled magnetic-force model must use Rev.B actual centers.
C448 exact target geometry remains open.
C449 exact RF keep-out intersection remains a production gate.
C450 STEP remains DMU-only.

## 14. State
Rev.B resolves the known magnetic-pad/DML projection conflict.

Real B-rep:
PASS.

One connected solid:
PASS.

Rigid-pad/DML projected overlap:
REMOVED.

Carrier mass:
26.7..28.0 g.

Status:
**FRONT_CARRIER_REV_B_ONE_SOLID / MAGNET_POCKETS_OUTBOARD_OF_DML / 25P422CM3 / C01_TO_C450 / MASTER_DMU_TRANSFORM_AND_RF_GATE_NEXT**.
