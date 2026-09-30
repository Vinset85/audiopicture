# AudioPicture V2.2 Rev.B — front carrier corrected magnet geometry kernel gate

Status: **CORRECTED_MAGNET_POCKET_GEOMETRY_ANALYTIC_PASS / 0P7MM_POCKET_TO_DML_CLEARANCE / FULL_CAD_KERNEL_EXPORT_GATE_OPEN**

## 1. Corrected station set
M1C (70,394)
M2C (250,394)
M3C (70,6)
M4C (250,6)
M5C (6,135)
M6C (6,275)
M7C (314,135)
M8C (314,315).

Pocket diameter:
6.6 mm.

Pocket radius:
3.3 mm.

## 2. Carrier boundary check
Carrier:
X0.8..319.2
Y0.8..399.2.

All eight 6.6 mm pocket circles are fully inside the carrier projected outer boundary.

PASS.

## 3. DML clearance check
DML:
X10..310
Y10..390.

Each corrected magnet center is 4.0 mm outside the nearest DML edge.

Pocket radial extent:
3.3 mm.

Resulting nominal pocket-to-DML projected clearance:
**0.7 mm**.

This exceeds the 0.5 mm seed requirement by 0.2 mm.

PASS analytically.

## 4. Interpretation
The previous M*B set is retired for the 6.6 mm pocket.

The M*C set is the current authoritative seed for front-carrier CAD.

This check proves projected pocket clearance, not:
- exact mechanical capture clearance;
- exact RF clearance;
- printed tolerance closure;
- assembled magnetic force.

## 5. Station reinforcement
Local thickening must be clipped to preserve at least the same DML-facing rigid clearance.

A reinforcement primitive may not reduce the 0.7 mm pocket result below the hard 0.5 mm CAD seed.

## 6. Manufacturing tolerance consequence
0.7 mm is a CAD nominal geometric clearance, not yet a manufacturing release clearance.

Print dimensional tolerance and warp can consume this margin.

Before production release either:
- demonstrate process capability that preserves the hard clearance; or
- move stations farther outward / reduce magnet diameter.

## 7. Next kernel gate
The complete Rev.B B-rep shall implement:
- M*C coordinates;
- clipped station islands;
- 6.6 mm pockets;
- mechanical capture;
- peel recess;
- locator features.

Required outputs:
one valid connected solid, volume, mass, bounding box, minimum wall and exact B-rep DML distance.

## 8. Automatic checks
C451 all eight corrected pockets inside carrier outer boundary.
C452 all eight corrected pockets outside DML projection.
C453 nominal pocket-to-DML projected clearance =0.7 mm.
C454 0.7 mm exceeds 0.5 mm CAD seed.
C455 M*B coordinates retired for 6.6 mm pocket.
C456 reinforcement may not reduce DML clearance below 0.5 mm.
C457 manufacturing tolerance not credited in analytic pass.
C458 exact RF clearance still open.
C459 mechanical capture B-rep still open.
C460 full corrected kernel export remains next gate.

## 9. State
Projected geometry:
**PASS**

Minimum nominal pocket-to-DML clearance:
**0.7 mm**

Status:
**MC_MAGNET_POCKETS_ANALYTICALLY_CLEAR_DML / 0P7MM_NOMINAL / C01_TO_C460 / FULL_REV_B_BREP_NEXT**.
