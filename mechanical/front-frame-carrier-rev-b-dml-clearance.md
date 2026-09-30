# AudioPicture V2.2 Rev.B — DML-clear front carrier magnetic stations

Status: **REV_B_MAGNET_STATION_GEOMETRY_DEFINED / DML_FACING_PAD_TRIMMED / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Remove the front-carrier Rev.A magnetic-pad overlap identified by the integrated master DMU audit.

The DML projected hard region is:
- X = 10..310 mm
- Y = 10..390 mm.

The active/compliant DML shall not be notched to accommodate front-frame magnets.

## 2. Rev.B magnetic centers
Top:
- M1B = (70,388)
- M2B = (250,388)

Bottom:
- M3B = (70,12)
- M4B = (250,12)

Left:
- M5B = (12,135)
- M6B = (12,275)

Right:
- M7B = (308,135)
- M8B = (308,315).

## 3. Geometric issue
A symmetric diameter-12-mm pad around these centers still crosses the DML projected boundary.

Therefore station pads are not circular in production geometry.

## 4. D-shaped pad rule
Each station starts from a 12 mm diameter local reinforcement primitive.

The DML-facing portion is trimmed by a keep-out offset from the DML projected boundary.

Define:
DML_PAD_CLEAR = 0.5 mm nominal CAD seed.

Legal rigid pad limits:
- top stations: Y >= 390.5 mm
- bottom stations: Y <= 9.5 mm
- left stations: X <= 9.5 mm
- right stations: X >= 310.5 mm.

Because the product carrier outer boundary is inside approximately X0.8..319.2 / Y0.8..399.2, the remaining crescent/D-shaped material is perimeter-biased.

## 5. Magnet pocket consequence
A centered 6.6 mm cylindrical magnet pocket cannot remain fully inside the legal rigid-pad strip if the magnet center stays only 2 mm outside the DML boundary.

Therefore the magnet itself, not only the reinforcement pad, must be moved farther outward or use a smaller/noncircular circuit.

This is a critical correction.

## 6. Minimum center offset for 6.6 mm pocket
Magnet pocket radius:
3.3 mm.

Add DML_PAD_CLEAR:
0.5 mm.

Minimum magnet center distance outside DML boundary:
**3.8 mm**.

Use >=4.0 mm nominal.

Thus revised centers become:

Top:
M1C = (70,394)
M2C = (250,394)

Bottom:
M3C = (70,6)
M4C = (250,6)

Left:
M5C = (6,135)
M6C = (6,275)

Right:
M7C = (314,135)
M8C = (314,315).

These place magnet centers 4 mm outside the DML projected boundary.

## 7. Outer-boundary feasibility
Carrier projected outer boundary:
X0.8..319.2
Y0.8..399.2.

For 6.6 mm pocket radius 3.3 mm:
- top pocket reaches Y397.3 <399.2
- bottom reaches Y2.7 >0.8
- left reaches X2.7 >0.8
- right reaches X317.3 <319.2.

Therefore the 6.6 mm pocket fits inside the carrier projected envelope at all eight M*C stations.

## 8. Reinforcement pad
A full 12 mm radius-6 pad would exceed some outer carrier limits.

Therefore Rev.B reinforcement is clipped by both:
- carrier outer boundary;
- DML hard keep-out.

The result is an asymmetric perimeter station island integrated into the 10 mm perimeter ring.

No independent circular boss is required.

## 9. Local thickness
Base carrier:
1.8 mm.

Magnet station local total thickness:
3.2 mm diagnostic seed.

The thickened region follows the legal clipped station island only.

No local thickening crosses DML_PAD_CLEAR.

## 10. Pocket wall
Minimum printable wall around 6.6 mm pocket is not uniform because the station is edge-biased.

Use carrier perimeter material as structural wall.

Target minimum local wall:
>=1.2 mm after process compensation.

If this cannot be achieved:
- reduce pocket diameter via alternate magnet;
- increase perimeter ring locally;
- do not intrude toward DML.

## 11. Retention target
Magnetic performance target remains:
20..30 N total assembled.

Moving the magnets outward does not change the force requirement.

Target steel geometry follows the new M*C coordinates.

## 12. RF implications
M8C and other stations still require exact ESP32/radar RF-mask checks.

DML clearance does not imply RF clearance.

Exact RF masks remain higher-priority reject masks.

## 13. Peel feature
Lower peel recess remains centered X160.

M3C/M4C remain at X70/X250.

Progressive peel geometry remains favorable.

## 14. Global Z
Rev.B station thickening is transformed into the global front-carrier placement.

The DML-facing rigid edge is prohibited from entering the DML hard projection.

Fabric may span the DML region; rigid magnet hardware may not.

## 15. CAD boolean order
1. create base perimeter carrier;
2. create M*C station thickening primitives;
3. union station primitives with perimeter;
4. subtract DML hard keep-out + 0.5 mm;
5. clip to carrier outer boundary;
6. subtract 6.6 mm magnet pockets;
7. create mechanical capture feature;
8. subtract peel recess;
9. apply edge fillets;
10. validate one connected solid.

## 16. Required kernel outputs
Record:
- solid count;
- B-rep validity;
- volume;
- ASA carrier-only mass;
- bounding box;
- minimum pocket wall;
- minimum DML rigid clearance;
- pocket count;
- disconnected fragment count.

## 17. Automatic checks
C431 Rev.B M*B centers superseded by M*C for 6.6 mm pockets.
C432 magnet pocket radius included in DML clearance.
C433 nominal DML rigid clearance >=0.5 mm.
C434 M1C/M2C top pockets fit carrier boundary.
C435 M3C/M4C bottom pockets fit carrier boundary.
C436 M5C/M6C left pockets fit carrier boundary.
C437 M7C/M8C right pockets fit carrier boundary.
C438 station reinforcement clipped by DML keep-out.
C439 station reinforcement clipped by carrier outer boundary.
C440 no DML notch used.
C441 local station thickness remains 3.2 mm seed.
C442 minimum local pocket wall target >=1.2 mm.
C443 eight pockets remain generated.
C444 peel recess remains clear.
C445 magnetic total-force target unchanged.
C446 exact RF masks remain mandatory.
C447 station target steel follows M*C coordinates.
C448 CAD boolean order frozen.
C449 real kernel regeneration required.
C450 one-solid validity required.

## 18. State
Rev.B discovered that merely D-shaping a 12 mm pad is insufficient if the 6.6 mm magnet pocket itself crosses the DML boundary.

The correct solution is to move the magnet center at least the pocket radius plus clearance outside the DML projection.

Production seed:
- top Y394
- bottom Y6
- left X6
- right X314.

Status:
**MAGNET_CENTER_GEOMETRY_CORRECTED_FOR_POCKET_RADIUS / MC_COORDINATES_DEFINED / DML_CLEARANCE_0P5MM_SEED / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
