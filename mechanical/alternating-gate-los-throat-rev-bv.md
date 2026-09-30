# AudioPicture V2.2 — alternating-gate LOS/throat gate Rev.BV

Status: **ALTERNATING_GATE_LOS_PASS / UPPER_THROAT_SWEEP_DEFINED / CAD_GATE_NEXT**

## Rev.BS execution
The sampled 2D line-of-sight audit was executed.

Result:
- lower alternating-gate seed: zero sampled straight vent-bank-to-cavity paths;
- upper alternating-gate seed: zero sampled straight vent-bank-to-cavity paths.

This is a sampled geometric screen, not CFD and not an acoustic ray model.

## Initial throat observation
At nominal Z flow height 2.8 mm:
- lower 24 mm end opening -> 67.2 mm2 geometric gate area per side;
- upper 9 mm end opening -> 25.2 mm2 geometric gate area per side.

The upper seed is therefore intentionally not frozen.

## Rev.BU optimization
The upper end-opening width is swept from 9 to 15 mm while retaining:
- two opposite end openings;
- 1.2 mm gate thickness;
- gate X positions;
- bank Y315..346;
- sampled LOS criterion.

The preferred pre-CAD value is the largest opening that still returns zero sampled straight paths.

No thermal-performance claim is made from gate area alone.

## Design rule
Do not minimize the gate opening merely to maximize visual shielding.

Prefer the largest opening that:
1. maintains the no-straight-path topology;
2. remains compatible with surrounding hardware;
3. can be integrated as one ASA shell solid;
4. does not contact PC-CF;
5. preserves manufacturable rib geometry.

## Next gate
Take the Rev.BU preferred upper opening and build the alternating-gate topology into the full Rev.BK shell at H=1.0 mm.

Then verify:
- one connected solid;
- 22 vents remain open;
- zero nominal PC-CF collision;
- seat/return compatibility;
- gate dimensions and nominal under-rib clearance;
- no direct sampled LOS after exact coordinates.

Only then resume the H=0.8..1.4 sweep.

## Checks
C1349 Rev.BS LOS audit executed.
C1350 lower sampled straight paths zero.
C1351 upper sampled straight paths zero.
C1352 LOS result is geometric only.
C1353 lower 24mm x 2.8mm gate proxy = 67.2mm2 per side.
C1354 upper 9mm x 2.8mm gate proxy = 25.2mm2 per side.
C1355 upper 9mm seed not frozen.
C1356 upper opening sweep 9..15mm defined.
C1357 largest LOS-passing opening preferred pre-CAD.
C1358 gate area is not thermal-flow proof.
C1359 full Rev.BK integration required next.
C1360 height sweep remains after topology CAD pass.

Status:
**LABYRINTH_REV_BV / LOS_PASS / THROAT_OPTIMIZATION / FULL_SHELL_CAD_NEXT / C01_TO_C1360**.
