# AudioPicture V2.2 — front carrier Rev.C real CAD-kernel result

Status: **ONE_VALID_BREP / DML_PROJECTED_COLLISION_ZERO / DMU_STEP_READY**

## 1. Real kernel
Generated with CadQuery/OpenCASCADE using the Rev.C narrow magnetic station geometry.

Artifact:
AP22_FRONT_CARRIER_REV_C_DMU.step

## 2. Result
Kernel validity: PASS.
Connected solids: **1**.
Volume: **25,356.27 mm3 = 25.356 cm3**.
Bounding box: **318.4 x 398.4 x 3.2 mm**.

ASA mass sensitivity:
- 1.05 g/cm3: **26.62 g**
- 1.10 g/cm3: **27.89 g**.

Carrier-only mass remains far below the 60 g carrier budget.

## 3. Rev.C station geometry
Eight local pads:
- radial width 8.0 mm;
- tangential length 12.0 mm;
- local total thickness 3.2 mm;
- 6.6 mm magnet pocket.

Centers:
M1 (70,394.6)
M2 (250,394.6)
M3 (70,5.4)
M4 (250,5.4)
M5 (5.4,135)
M6 (5.4,275)
M7 (314.6,135)
M8 (314.6,315).

## 4. DML collision audit
DML rectangle:
X10..310 / Y10..390.

Computed pad bounds:
- top pads Y390.6..398.6
- bottom pads Y1.4..9.4
- left pads X1.4..9.4
- right pads X310.6..318.6.

Therefore every pad has **0.6 mm nominal projected separation** from the DML boundary.

Detected pad/DML projected overlaps:
**0 / 8**.

The DML does not require a notch.

## 5. Connectivity
The lower peel recess and all eight pads preserve one connected carrier solid.

PASS.

## 6. RF coarse screen
Using the frozen MAIN-C left-edge ESP32 antenna seed and a conservative 15 mm enclosure clearance expansion, no Rev.C magnet center lies inside the coarse ESP32 RF mask.

Using the current radar board envelope plus the 45-degree coarse forward packaging expansion, no Rev.C magnet center lies in the coarse radar front cone.

Exact STEP/EM masks remain final validation.

## 7. Z
The 3.2 mm station thickening occurs outside the DML projected region.

Therefore it does not consume the active central fabric-to-DML 2.8 mm nominal gap.

## 8. Checks
C461 Rev.C real B-rep generated.
C462 one connected solid.
C463 kernel validity PASS.
C464 volume recorded.
C465 mass sensitivity recorded.
C466 all 8 station pad bounds outside DML projection.
C467 nominal projected DML separation 0.6 mm.
C468 no DML notch.
C469 peel recess preserves connectivity.
C470 Rev.C STEP marked DMU, not manufacturing release.

## 9. State
Status:
**FRONT_CARRIER_REV_C_ONE_SOLID / 25P356CM3 / 26P6_TO_27P9G / ZERO_DML_PAD_OVERLAPS / C01_TO_C470**.
