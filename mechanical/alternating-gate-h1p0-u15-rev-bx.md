# AudioPicture V2.2 — alternating-gate H1.0 U15 integration Rev.BX

Status: **U15_SELECTED_FROM_LOS_SWEEP / H1P0_FULL_SHELL_KERNEL_DEFINED / EXECUTION_GATE_REQUIRED**

## Rev.BU result
The upper opening sweep 9..15 mm was executed against the sampled 2D LOS criterion.

The largest tested opening that retained zero sampled straight paths is 15 mm.

At nominal 2.8 mm flow height:
- upper gate proxy per side: 15 x 2.8 = 42.0 mm2;
- lower gate proxy per side: 24 x 2.8 = 67.2 mm2.

Relative to the original 9 mm upper seed, the geometric upper gate proxy increases from 25.2 to 42.0 mm2 (+66.7%).

This is not a CFD mass-flow result.

## Rev.BW 3D integration
The selected topology is integrated into the promoted Rev.BK shell at H=1.0 mm.

Lower left:
- Gate 1 X30..31.2 Y14..126
- Gate 2 X34..35.2 Y38..150

Upper left:
- Gate 1 X65..66.2 Y315..331
- Gate 2 X69..70.2 Y330..346

Right side is mirrored about X160.

The upper end openings are 15 mm at opposite ends.

## Mandatory execution gate
Rev.BW must be actually executed before promotion.

Required pass:
- valid one-solid B-rep;
- zero vent reclosure;
- zero nominal Rev.C PC-CF collision;
- Zmax <=40;
- nominal under-rib clearance 1.8 mm;
- STEP/STL export;
- repeat LOS audit using exact Rev.BW coordinates.

## Checks
C1361 Rev.BU sweep executed.
C1362 15mm is largest tested upper opening retaining zero sampled LOS.
C1363 upper proxy 42.0mm2 per side.
C1364 lower proxy 67.2mm2 per side.
C1365 upper proxy improvement vs 9mm seed +66.7%.
C1366 proxy is not CFD.
C1367 Rev.BW full-shell source created.
C1368 H remains 1.0mm.
C1369 upper alternating gates updated for 15mm openings.
C1370 right topology mirrored.
C1371 execution required before promotion.
C1372 exact-coordinate LOS recheck required after kernel pass.

Status:
**LABYRINTH_REV_BX / U15_PRE_CAD_SELECTED / H1P0_FULL_SHELL_SOURCE / EXECUTION_NEXT / C01_TO_C1372**.
