# AudioPicture V2.2 — front carrier Rev.B DML-clearance redesign

Status: **MAGNET_STATIONS_REV_B_PERIMETER_BIASED / DML_FACING_PAD_MATERIAL_REMOVED / CAD_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A magnetic-station packaging warning found by the integrated master DMU.

The DML projected hard region is:
X=10..310 mm
Y=10..390 mm.

No rigid local magnetic pad may intrude into the DML hard-clearance volume.

## 2. Rev.B station centers
Top:
M1B=(70,388)
M2B=(250,388)

Bottom:
M3B=(70,12)
M4B=(250,12)

Left:
M5B=(12,135)
M6B=(12,275)

Right:
M7B=(308,135)
M8B=(308,315).

## 3. Important geometric consequence
A 6.6 mm circular magnet pocket centered only 2 mm outside a DML projected edge cannot itself remain completely outside the DML projection.

Therefore the DML keep-out cannot be satisfied by center movement alone if the magnet axis remains normal to the front.

The previous assumption that a simple D-shaped 12 mm support pad alone solves the conflict is insufficient: the magnet/pocket envelope itself must also be considered.

## 4. Architecture correction
Do not place the magnet directly behind the DML projected rectangle.

Rev.B uses **outboard perimeter magnetic pockets** whose centers are moved beyond the DML projection by at least:

R_MAG_POCKET + C_DML_MAG

where:
R_MAG_POCKET=3.3 mm
C_DML_MAG=0.7 mm seed.

Required center offset from DML edge:
>=4.0 mm.

## 5. Corrected Rev.C-ready center seeds
To provide the required 4 mm center offset while remaining inside product boundary:

Top:
M1C=(70,394)
M2C=(250,394)

Bottom:
M3C=(70,6)
M4C=(250,6)

Left:
M5C=(6,135)
M6C=(6,275)

Right:
M7C=(314,135)
M8C=(314,315).

These centers are 4 mm outside the DML projected boundary.

For 6.6 mm pocket radius 3.3 mm:
minimum nominal projected clearance to DML edge:
**0.7 mm**.

## 6. Product-edge feasibility
Carrier projected boundary:
X0.8..319.2
Y0.8..399.2.

At center coordinate 6 mm or 314 mm:
a 3.3 mm pocket extends to 2.7 or 317.3 mm.

At Y6/394:
extends to 2.7 or 397.3 mm.

Therefore the 6.6 mm pocket remains inside the carrier projected boundary with nominal edge material to boundary:
~1.9 mm at the nearest side.

This is tight but geometrically feasible.

## 7. Local station geometry
The local structural reinforcement is not a 12 mm circle.

Use a perimeter-biased obround/D-pad:
- magnet pocket 6.6 mm;
- DML-facing reinforcement tangent is clipped to DML keep-out;
- reinforcement grows toward product edge and tangentially along perimeter;
- local root fillets blend into 10 mm perimeter ring.

No reinforcement crosses DML hard projection.

## 8. Pocket floor
Magnet remains rear-loaded with front-side polymer floor.

Floor thickness is a magnetic-force tuning variable and structural feature.

Seed:
0.6..1.0 mm.

Do not reduce below print/process structural qualification.

## 9. Local material constraint
Nearest product-edge ligament around the 6.6 mm pocket is limited.

Therefore station strength is provided by:
- tangential extension along perimeter ring;
- elongated local pad;
- filleted roots;
not by increasing radial diameter toward the product edge.

## 10. Candidate station footprint
Seed local footprint per horizontal-edge station:
- 14 mm tangential length
- 7.5..9 mm radial depth, clipped by DML keep-out/product edge.

Vertical-edge stations rotate this footprint 90 degrees.

Exact B-rep determines final volume.

## 11. Target alignment
Steel target center follows magnet center.

Target geometry must also remain outside:
- DML hard projection;
- radar RF keep-out;
- ESP32 RF keep-out.

A 10 mm circular target may be too large at the product perimeter.

Therefore replace circular target seed with:
**perimeter-oriented rectangular/obround target 10 x 5 mm class**
subject to magnetic-force validation.

## 12. Magnetic-force consequence
Changing target area and magnetic gap changes assembled retention.

The prior 20..30 N total target remains authoritative.

Catalogue magnet force is not sufficient.

Force matrix must include:
- 10x5x0.8 mm target
- 10x5x1.0 mm target
- 12x5x1.0 mm target
- G_MAG 0.5/0.8/1.0/1.2 mm.

## 13. Peel geometry
Bottom magnets at X70 and X250, Y6.

Peel recess remains centered X160.

Horizontal separation remains 90 mm from peel center to each lower magnet.

Progressive peel concept remains valid.

## 14. RF rule
The corrected perimeter locations reduce coupling risk but do not eliminate RF validation.

M7C/M8C in particular require exact radar/ESP32 mask checks.

If an RF mask rejects a station, move tangentially along perimeter rather than inward toward DML.

## 15. Front-carrier regeneration requirements
Next real kernel model shall:
- use corrected C centers;
- cut all eight 6.6 mm pockets;
- create elongated perimeter-biased pads;
- subtract DML hard projection from reinforcement volume;
- preserve one connected solid;
- preserve peel recess;
- report minimum DML clearance;
- report minimum product-edge ligament;
- report volume/mass/bounding box.

## 16. Automatic checks
C431 Rev.B centers evaluated against magnet pocket radius.
C432 center movement alone identified as insufficient.
C433 full magnet/pocket envelope included in DML collision logic.
C434 corrected centers use >=4.0 mm DML-edge offset.
C435 6.6 mm pocket nominal DML clearance >=0.7 mm.
C436 6.6 mm pocket remains inside carrier outer boundary.
C437 nearest carrier-edge ligament >=1.9 mm nominal.
C438 reinforcement grows tangentially/outboard, not into DML.
C439 DML hard projection subtracts reinforcement automatically.
C440 circular 12 mm pad retired.
C441 circular 10 mm steel target retired as baseline.
C442 perimeter target 10x5 mm class introduced.
C443 magnetic force matrix updated for smaller target.
C444 total retention remains 20..30 N.
C445 peel recess remains centered and clear.
C446 RF-rejected stations move tangentially only.
C447 no DML notch introduced.
C448 kernel regeneration must remain one connected solid.
C449 kernel regeneration must measure minimum DML clearance.
C450 kernel regeneration must measure product-edge ligament.

## 17. State
The intermediate M1B..M8B positions are not sufficient for the complete 6.6 mm magnet pocket.

Corrected CAD seeds:
M1C (70,394)
M2C (250,394)
M3C (70,6)
M4C (250,6)
M5C (6,135)
M6C (6,275)
M7C (314,135)
M8C (314,315).

Nominal pocket-to-DML projected clearance:
**0.7 mm**

Nominal nearest pocket-to-carrier-boundary ligament:
**~1.9 mm**

Status:
**MAGNET_CENTER_GEOMETRY_CORRECTED / 6P6MM_POCKET_DML_CLEARANCE_0P7MM / PERIMETER_OBROUND_PAD_REQUIRED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
