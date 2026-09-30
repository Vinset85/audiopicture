# AudioPicture V2.2 — labyrinth LOS topology correction Rev.BT

Status: **REV_BP_FUNCTIONAL_TOPOLOGY_REJECTED / ALTERNATING_GATE_TOPOLOGY_DEFINED / LOS_AUDIT_REQUIRED / 3D_KERNEL_NEXT**

## Rev.BP result
The H=1.0 mm Rev.BP kernel remains a valid packaging experiment.

However, plan-view line-of-sight screening shows that its short staggered ribs do not reliably shield the complete vent-bank-to-cavity path.

Therefore:
- Rev.BP is not promoted as the functional labyrinth;
- its 1.0 mm height result remains useful for nominal Z packaging only;
- the height sweep is paused until topology is corrected.

## Corrected concept
Use two transverse planar gates per bank.

Gate 1 spans most of the bank transverse dimension but leaves an opening at one end.

Gate 2 is displaced inward in X and leaves its opening at the opposite end.

A plan-view path must therefore:
1. approach the first end opening;
2. travel laterally between the gates;
3. reverse lateral direction toward the second opening;
4. enter the main cavity.

The ribs still stop short of the PC-CF in Z, retaining the deliberate under-rib Z bypass.

## Seed geometry — left lower
Bank Y14..150.

Gate 1:
X30..31.2, Y14..126.
Opening: Y126..150.

Gate 2:
X34..35.2, Y38..150.
Opening: Y14..38.

Nominal end openings: 24 mm each.

## Seed geometry — left upper
Bank Y315..346.

Gate 1:
X65..66.2, Y315..337.
Opening: Y337..346.

Gate 2:
X69..70.2, Y324..346.
Opening: Y315..324.

Nominal end openings: 9 mm each.

Right side is mirrored.

## Important limitation
Blocking straight line of sight is necessary but not sufficient.

The final design still requires:
- actual 2D path audit;
- minimum lateral throat calculation;
- 3D CadQuery integration;
- PC-CF/seat/vent collision checks;
- CFD;
- acoustic prototype testing.

## Checks
C1335 Rev.BP plan-view functional topology rejected.
C1336 H1.0 packaging result retained.
C1337 height sweep paused.
C1338 alternating two-gate topology selected.
C1339 lower gate openings alternate top/bottom.
C1340 upper gate openings alternate top/bottom.
C1341 lower seed opening 24 mm.
C1342 upper seed opening 9 mm.
C1343 baffles remain shell-mounted.
C1344 under-rib Z bypass retained.
C1345 LOS audit required.
C1346 throat audit required.
C1347 3D kernel required after topology pass.
C1348 CFD/acoustic validation remain open.

Status:
**LABYRINTH_REV_BT / BP_TOPOLOGY_REJECTED / ALTERNATING_GATES / LOS_NEXT / C01_TO_C1348**.
