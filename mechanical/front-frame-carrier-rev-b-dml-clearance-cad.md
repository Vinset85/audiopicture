# AudioPicture V2.2 Rev.B — front carrier DML-clearance CAD

Status: **REV_B_MAGNET_STATIONS_PERIMETER_BIASED / DML_FACING_PAD_CLIPPED / REAL_KERNEL_REGENERATION_CONTRACT**

## 1. Objective
Remove the Rev.A magnetic-pad overlap with the DML projected perimeter without notching or modifying the DML.

Authoritative product coordinates:
- product 320 x 400 mm;
- DML projection X10..310, Y10..390;
- front carrier outer projected boundary X0.8..319.2, Y0.8..399.2.

## 2. Rev.B magnetic centers
Top:
- M1B (70,388)
- M2B (250,388)

Bottom:
- M3B (70,12)
- M4B (250,12)

Left:
- M5B (12,135)
- M6B (12,275)

Right:
- M7B (308,135)
- M8B (308,315).

These replace Rev.A center seeds for new CAD generation.

## 3. Geometric issue
A symmetric diameter-12 mm pad around any Rev.B center still crosses the DML projection because each center is only 2 mm from the DML edge.

Therefore the pad cannot remain circular.

## 4. D-shaped/perimeter-biased pad
Each station uses:
- magnet pocket diameter 6.6 mm class;
- local structural island biased toward product perimeter;
- DML-facing side clipped by a legal boundary.

The pad is generated from a larger perimeter-side lobe intersected with the carrier ring, then trimmed against the DML hard-clearance mask.

No material is added into the active DML projection merely to preserve a symmetric boss.

## 5. DML hard-clearance mask
For magnetic station solid material, define a conservative no-intrusion boundary at the DML projection.

Baseline:
- top pad material must remain Y >=390 mm where it would otherwise overlie DML;
- bottom pad material must remain Y <=10 mm;
- left pad material must remain X <=10 mm;
- right pad material must remain X >=310 mm.

Because the magnet pocket center itself is currently at 388/12/12/308, a conventional centered 6.6 mm pocket cannot fit wholly outside those limits.

This exposes a second-order conflict:
**the magnet itself, not only the 12 mm pad, overlaps the DML projection if interpreted as a full-depth rear intrusion.**

## 6. Consequence
The Rev.B center shift by 2 mm is insufficient for a full-depth magnet pocket entirely outside the DML projected area.

A diameter 6.6 mm pocket requires its center at least radius 3.3 mm beyond the DML boundary, plus structural/process margin.

For a minimum 0.7 mm geometric margin:
required center offset from DML boundary >=4.0 mm.

## 7. Rev.C recommended centers
Use 5 mm center offset from DML boundary to provide a 1.7 mm geometric margin around a 6.6 mm pocket:

Top:
- M1C (70,395)
- M2C (250,395)

Bottom:
- M3C (70,5)
- M4C (250,5)

Left:
- M5C (5,135)
- M6C (5,275)

Right:
- M7C (315,135)
- M8C (315,315).

## 8. Carrier-boundary feasibility
Carrier outer boundary:
X0.8..319.2, Y0.8..399.2.

For center 5 mm from product edge and radius 3.3 mm pocket:
minimum coordinate =1.7 mm;
maximum =318.3 / 398.3 mm depending axis.

Therefore the 6.6 mm pocket remains inside the 0.8 mm carrier outer boundary with approximately 0.9 mm minimum outer-side material before any capture feature.

That 0.9 mm is too small for a robust printed mechanical capture wall.

## 9. Structural-wall requirement
Target minimum polymer outside magnet pocket:
**>=1.5 mm nominal**, preferably 2.0 mm.

With pocket radius 3.3 mm and carrier edge at 0.8 mm:
minimum center coordinate for 1.5 mm outer wall:
0.8 + 3.3 + 1.5 = **5.6 mm**.

Symmetric opposite edge:
320 - 5.6 = **314.4 mm**;
400 - 5.6 = **394.4 mm**.

## 10. Rev.C production-oriented center seed
Adopt nominal edge center offset:
**6.0 mm**.

Coordinates:
Top:
- M1C (70,394)
- M2C (250,394)

Bottom:
- M3C (70,6)
- M4C (250,6)

Left:
- M5C (6,135)
- M6C (6,275)

Right:
- M7C (314,135)
- M8C (314,315).

Pocket radius 3.3 mm.

Outer wall to carrier boundary:
6.0 - 3.3 - 0.8 = **1.9 mm nominal**.

DML-side clearance:
top: 394 - 3.3 - 390 = **0.7 mm**
bottom: 10 - (6 + 3.3) = **0.7 mm**
left: 10 - (6 + 3.3) = **0.7 mm**
right: (314 - 3.3) - 310 = **0.7 mm**.

Thus the complete magnet pocket projection clears the DML by 0.7 mm nominal.

## 11. Pad shape
Around each Rev.C pocket:
- outer-side wall >=1.9 mm nominal;
- tangential pad extension may grow along perimeter;
- DML-facing pad wall limited to available 0.7 mm gap and shall not cross DML mask.

Therefore mechanical capture should preferentially use:
- tangential ears;
- rear cap retained tangentially;
- not a uniform radial wall.

## 12. Preferred capture architecture
Rev.B/Rev.C carrier uses a tangentially retained pocket cap.

The cap loads from rear and is trapped by two tangential ledges along the perimeter direction.

This preserves:
- thin DML-facing geometry;
- stronger perimeter-side material;
- adhesive as secondary retention.

## 13. Z behavior
Local magnet station thickness remains target:
3.0..3.2 mm class.

The station is legal only because its full projected pocket/capture geometry remains outside the DML projection.

No local station protrudes behind the active DML area.

## 14. Peel feature
Lower peel recess remains:
- center X160
- width28
- depth4.

M3C/M4C at X70/250 remain ~90 mm from peel center.

Progressive release behavior preserved.

## 15. RF gates
Rev.C coordinates improve DML clearance but do not independently prove RF legality.

Exact masks remain required for:
- ESP32 antenna;
- radar;
- microphones;
- optical sensor.

Any RF conflict has priority over the nominal coordinate.

## 16. Kernel-generation acceptance
A real Rev.C carrier B-rep shall pass:
- one connected solid;
- valid kernel;
- all eight pockets generated;
- all eight pocket projections >=0.5 mm from DML projection;
- outer carrier wall >=1.5 mm around pocket where required by capture architecture;
- peel recess preserves connectivity;
- no increase beyond 320 x 400 projected product envelope.

## 17. Automatic checks
C431 Rev.B centers evaluated against full pocket radius.
C432 symmetric 12 mm pad Rev.B rejected.
C433 Rev.B 2 mm edge shift identified as insufficient for full pocket.
C434 pocket radius 3.3 mm included in DML clearance.
C435 process/geometric clearance added.
C436 Rev.C edge offset selected at 6.0 mm.
C437 Rev.C pocket DML clearance nominal >=0.7 mm.
C438 Rev.C outer polymer wall nominal >=1.9 mm.
C439 DML remains unmodified.
C440 pad may grow tangentially only where legal.
C441 DML-facing radial boss wall is not required uniformly.
C442 tangential capture architecture selected.
C443 adhesive remains secondary retention.
C444 local station Z <=3.2 mm class.
C445 lower peel geometry preserved.
C446 RF masks remain higher-priority gates.
C447 real kernel regeneration required.
C448 one-solid criterion retained.
C449 minimum kernel-measured DML clearance target >=0.5 mm.
C450 product projected envelope remains <=320 x 400.

## 18. State
The integrated geometric check showed that the proposed Rev.B centers were still not sufficient once the actual 6.6 mm magnet pocket diameter was included.

The corrected production-oriented seed is Rev.C with 6 mm edge offset.

Rev.C coordinates:
M1C (70,394)
M2C (250,394)
M3C (70,6)
M4C (250,6)
M5C (6,135)
M6C (6,275)
M7C (314,135)
M8C (314,315).

Nominal pocket-to-DML clearance:
**0.7 mm**

Nominal outer polymer wall:
**1.9 mm**

Status:
**REV_B_2MM_SHIFT_REJECTED / REV_C_6MM_EDGE_OFFSET / 0P7MM_DML_CLEARANCE / 1P9MM_OUTER_WALL / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
