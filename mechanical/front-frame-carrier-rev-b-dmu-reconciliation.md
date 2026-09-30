# AudioPicture V2.2 Rev.B — front carrier magnetic-pad DMU reconciliation

Status: **REV_B_MAGNET_STATIONS_PERIMETER_CLIPPED / DML_PAD_OVERLAP_REMOVED_BY_CONSTRUCTION / EXACT_CAPTURE_DETAIL_OPEN**

## 1. Objective
Resolve the Rev.A front-carrier warning where nominal 12 mm circular magnet pads crossed the projected DML perimeter.

The DML remains unchanged.

## 2. Authoritative geometry
Product:
320 x 400 mm.

DML projection:
X=10..310
Y=10..390.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

The legal magnet-support material is constructed from the carrier perimeter side of the DML boundary.

## 3. Rev.B station centers
M1B = (70,388)
M2B = (250,388)
M3B = (70,12)
M4B = (250,12)
M5B = (12,135)
M6B = (12,275)
M7B = (308,135)
M8B = (308,315).

These are seed magnet centers, not unrestricted circular-pad centers.

## 4. Key correction
A 6 mm magnet centered only 2 mm outside/inside the DML boundary cannot be supported by a symmetric D=12 mm pad without crossing the DML projection.

Therefore Rev.B does NOT use full circular D=12 mm station pads.

Each support island is:
1. generated from a local support primitive;
2. unioned to the perimeter carrier;
3. clipped by the DML hard-clearance half-plane;
4. blended into the perimeter ring.

The resulting island is D-shaped/asymmetric.

## 5. DML-facing limits
Top stations:
support material shall not extend below the legal top perimeter boundary adjacent to DML.

Bottom:
support material shall not extend above the legal bottom perimeter boundary adjacent to DML.

Left:
support material shall not extend rightward into DML hard region.

Right:
support material shall not extend leftward into DML hard region.

The exact clearance offset from DML edge is a parameter:
DML_MAG_CLEAR = 0.5 / 0.8 / 1.0 mm sweep.

Nominal:
**0.8 mm**.

## 6. Important magnet-pocket implication
The magnet itself is D=6 mm class.

A center at only 2 mm from the DML projected boundary means the magnet circular envelope itself can cross that projection.

Therefore support-pad clipping alone is insufficient if the DML projection is a hard full-Z exclusion.

Rev.B introduces a second rule:
**magnet solid itself must remain outside the DML hard 3D volume**.

## 7. Corrected station-center constraint
For a 6.0 mm magnet plus 0.8 mm DML clearance:
minimum magnet-center distance from DML edge:
3.0 + 0.8 = **3.8 mm**.

Hence the 2 mm-offset M1B..M8B centers are rejected as final centers.

Use perimeter-side center seeds at least 3.8 mm outside the DML edge where physical carrier width permits.

## 8. Rev.C-ready legal center seeds
Using 4.5 mm nominal center clearance from DML edge:

Top:
M1C=(70,394.5)
M2C=(250,394.5)

Bottom:
M3C=(70,5.5)
M4C=(250,5.5)

Left:
M5C=(5.5,135)
M6C=(5.5,275)

Right:
M7C=(314.5,135)
M8C=(314.5,315).

These centers are inside the product/front-carrier envelope and place the 6 mm magnet body outside the DML projection with nominal 1.5 mm geometric edge separation.

## 9. Carrier-edge check
Front-carrier outer edge:
0.8 / 319.2 / 399.2.

For center 5.5 and R=3:
outer magnet edge=2.5 mm.

Remaining to carrier outer boundary=1.7 mm.

For center 314.5:
outer magnet edge=317.5.
Remaining to X319.2=1.7 mm.

Top:
center394.5 +3=397.5.
Remaining to Y399.2=1.7 mm.

Thus D=6 mm magnet fits inside carrier projected boundary.

## 10. Pocket-wall consequence
1.7 mm projected material from magnet edge to outer carrier boundary is tight but feasible as a seed for a mechanically captured pocket.

It is not yet sufficient proof for:
- ASA print strength;
- capture lip;
- peel fatigue.

Pocket wall sweep:
1.5 / 1.8 / 2.2 mm equivalent local ligament.

If capture requires more material, magnet diameter or station architecture must change rather than violating DML clearance.

## 11. Preferred Rev.B/Rev.C topology
Adopt:
- 6 mm magnet class;
- centers M1C..M8C;
- perimeter-biased asymmetric support islands;
- nominal DML magnet-body separation 1.5 mm;
- no DML notch;
- no support material crossing DML hard-clearance mask.

## 12. Z placement
Magnet station local thickening remains outside DML XY hard region.

Therefore it may extend rearward locally without consuming the central fabric-to-DML gap.

The master global Z transform still controls:
- fabric Z0;
- DML front Z3.3;
- DML rear Z9.3.

No magnetic feature may enter the DML volume.

## 13. Connectivity
Each asymmetric station island must share a robust root with the 10 mm perimeter ring.

Minimum root width seed:
6 mm.

Preferred:
8 mm where geometry permits.

Root fillet:
R>=1.5 mm.

No isolated magnetic boss is allowed.

## 14. Peel interaction
Lower stations at X70 and X250 remain approximately 90 mm from center peel feature X160.

Moving them in Y does not materially change the intended progressive lower-edge peel behavior.

## 15. RF masks
This geometric correction does not supersede RF exclusion masks.

A station that is geometrically legal relative to DML may still be rejected by:
- radar RF mask;
- ESP32 antenna mask;
- microphone path;
- optical path.

Exact RF masks remain higher-priority placement constraints.

## 16. CAD-kernel generation rule
Next real B-rep shall:
1. build perimeter ring;
2. build asymmetric station roots;
3. cut D=6.6 mm process pocket;
4. create mechanical capture floor/lip;
5. cut peel recess;
6. apply DML keep-out Boolean;
7. validate one connected solid;
8. compute minimum ligament;
9. compute volume/mass;
10. transform into global DMU.

## 17. Checks
C431 Rev.B 2 mm center offsets rejected for 6 mm hard magnet body.
C432 magnet-body radius included in DML clearance.
C433 nominal DML_MAG_CLEAR parameter defined.
C434 M1C/M2C top centers legal by projection.
C435 M3C/M4C bottom centers legal by projection.
C436 M5C/M6C left centers legal by projection.
C437 M7C/M8C right centers legal by projection.
C438 magnet body remains inside carrier outer projection.
C439 minimum projected outer ligament seed ~1.7 mm.
C440 support islands clipped outside DML hard region.
C441 no DML notch introduced.
C442 support root >=6 mm seed.
C443 root fillet >=1.5 mm.
C444 lower peel geometry preserved.
C445 RF masks remain authoritative.
C446 mechanical capture strength still open.
C447 exact ASA print ligament qualification open.
C448 real B-rep generation required.
C449 real one-solid validation required.
C450 global DMU transform required after B-rep.

## 18. State
The first proposed Rev.B centers at 2 mm from DML edge were not sufficient once the physical 6 mm magnet diameter was included.

Corrected legal seed:
- top Y=394.5
- bottom Y=5.5
- left X=5.5
- right X=314.5.

This removes the magnet-body/DML projected overlap while preserving the 320 x 400 product envelope.

Status:
**MAGNET_BODY_CLEARANCE_CORRECTED / M1C_TO_M8C_PERIMETER_SEEDS / NO_DML_NOTCH / C01_TO_C450 / REAL_BREP_NEXT**.
