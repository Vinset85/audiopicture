# AudioPicture V2.2 Rev.B — front carrier DML-clear magnetic stations

Status: **MAGNET_STATION_REV_B_GEOMETRY_FROZEN / DML_HARD_PROJECTION_CLEARANCE_ENFORCED / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A front-carrier magnetic station geometry after the integrated master DMU identified overlap between the 12 mm circular station pads and the DML projected perimeter.

The DML is not modified.

## 2. Authoritative global geometry
Product:
X=0..320
Y=0..400.

DML hard projected rectangle:
X=10..310
Y=10..390.

The DML projection is treated as a hard exclusion for rearward rigid magnetic-station thickening.

## 3. Rev.B magnet centers
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

## 4. D-shaped pad rule
Each magnetic station uses a perimeter-biased D-shaped/local pad.

The DML-facing edge is clipped by a hard construction plane.

Top stations:
rear thickening permitted only at Y>=390.

Bottom:
rear thickening permitted only at Y<=10.

Left:
rear thickening permitted only at X<=10.

Right:
rear thickening permitted only at X>=310.

The base 1.8 mm carrier ring may continue through its normal perimeter geometry; the rule specifically controls additional rearward station thickening that could consume the DML clearance.

## 5. Magnet-pocket consequence
A centered 6.6 mm cylindrical pocket around the Rev.B centers would still cross the DML boundary because centers are only 2 mm outside the DML edge.

Therefore the magnet itself cannot remain centered at these coordinates if its full circular envelope must be outside the DML projection.

Required magnet-center minimum offsets for a 6.6 mm pocket with zero extra margin:
- top Y >=393.3
- bottom Y <=6.7
- left X <=6.7
- right X >=313.3.

This is the actual geometric condition.

## 6. Corrected magnet centers Rev.C seed
Use a 0.7 mm additional manufacturing/clearance reserve beyond the 3.3 mm pocket radius.

Required centerline offset:
4.0 mm from DML edge.

Corrected centers:
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

This places the complete nominal 6.6 mm magnet pocket outside the DML projected rectangle with ~0.7 mm reserve.

## 7. Product-edge check
For 6.6 mm pocket radius 3.3 mm:

Top center Y394:
outer pocket edge Y397.3 < carrier outer Y399.2.

Bottom center Y6:
outer edge Y2.7 > carrier outer Y0.8.

Left center X6:
outer edge X2.7 > carrier outer X0.8.

Right center X314:
outer edge X317.3 < carrier outer X319.2.

Therefore all eight corrected pocket circles fit within the carrier projected boundary.

Minimum carrier-edge material between nominal pocket edge and outer carrier edge:
~1.9 mm.

This is thin and requires local structural review/capture design.

## 8. Local station reinforcement
Because edge ligament is only ~1.9 mm, do not use a simple circular 12 mm boss.

Use a perimeter-elongated pad:
- tangential length 12..16 mm;
- radial width constrained by DML boundary;
- filleted into 10 mm carrier ring;
- local thickness 3.0..3.2 mm.

The pad is a racetrack/D hybrid, not a full circle.

## 9. Capture strategy update
At only ~1.9 mm outer ligament, a snap lip cut into the outside edge is undesirable.

Preferred:
- front-side closed pocket floor;
- rear-loaded magnet;
- thin printed retention bridge/cap spanning tangentially into stronger ring material;
- adhesive secondary retention.

Alternative:
separate ultralight polymer cap bonded/welded to carrier.

No steel retention cap.

## 10. DML clearance
Rev.C magnetic pockets:
**full nominal circular pocket projection outside DML hard rectangle**.

Station reinforcement:
also clipped outside DML hard rectangle for all additional rearward thickness.

Thus magnetic station thickening no longer consumes active DML Z clearance.

## 11. Peel recess
Lower peel recess remains:
center X160
width28
depth4.

M3C and M4C remain at X70 and X250.

Horizontal distance from peel center:
90 mm each.

Progressive peel architecture preserved.

## 12. RF status
This geometric correction does not replace RF masks.

M7C/M8C and upper stations still require exact:
- radar RF exclusion;
- ESP32 antenna exclusion.

If an RF mask rejects a station, tangential relocation along the same perimeter is preferred over moving inward toward the DML.

## 13. Fabric bonding land
Magnet pockets locally interrupt/reduce rear bonding land.

At each station:
- maintain a continuous alternate adhesive path around pocket;
- no exposed sharp magnet/cap edge contacts fabric;
- minimum effective fabric bond width to be process-qualified.

## 14. Carrier mass impact
Moving stations outward does not materially increase carrier mass.

The Rev.B/Rev.C elongated reinforcement may add only a few grams relative to the 28.2..29.6 g Rev.A carrier.

Target carrier remains:
<=35 g preferred after final magnet capture details;
<=60 g hard subsystem carrier budget.

## 15. CAD boolean order
1. create 318.4 x398.4 carrier ring;
2. create perimeter-elongated station pads at M1C..M8C;
3. intersect rearward station-thickening solids with legal outside-DML half-planes;
4. fuse pads to ring;
5. cut 6.6 mm magnet pockets;
6. add front-side pocket floors;
7. add capture bridge/cap seats;
8. cut peel recess;
9. add LOC_A/LOC_B;
10. apply edge fillets;
11. validate single solid.

## 16. Kernel validation requirements
Required outputs:
- valid B-rep;
- solid_count=1;
- volume;
- mass sensitivity;
- bounding box;
- DML overlap volume for rearward station thickening = 0;
- pocket-to-product-edge ligament;
- peel connectivity.

## 17. Automatic checks
C431 Rev.B centers evaluated geometrically.
C432 centered 6.6 mm pocket at Rev.B centers identified as DML-overlapping.
C433 Rev.B centers therefore not accepted as final pocket centers.
C434 corrected Rev.C centers defined.
C435 all Rev.C nominal pockets outside DML hard projection.
C436 nominal pocket-to-DML reserve >=0.7 mm.
C437 all Rev.C pockets inside carrier outer boundary.
C438 minimum outer carrier ligament approximately 1.9 mm.
C439 simple 12 mm circular boss rejected.
C440 elongated perimeter pad required.
C441 additional rear thickening clipped outside DML projection.
C442 magnet capture redesigned for thin edge ligament.
C443 no steel retention cap.
C444 peel recess remains clear.
C445 RF masks remain independent hard gate.
C446 RF-rejected station relocates tangentially, not inward.
C447 fabric bonding path remains continuous around station.
C448 final carrier target <=35 g preferred.
C449 kernel must report DML overlap volume zero.
C450 one-solid validation required after regeneration.

## 18. State
The earlier Rev.B center shift alone was insufficient for a 6.6 mm pocket.

The corrected Rev.C center seed is now:
M1C (70,394)
M2C (250,394)
M3C (70,6)
M4C (250,6)
M5C (6,135)
M6C (6,275)
M7C (314,135)
M8C (314,315).

This is the first magnetic center map that geometrically places the complete nominal magnet pocket outside the DML hard projected rectangle while remaining inside the carrier.

Status:
**MAGNET_REV_C_POCKET_CENTERS / 0P7MM_DML_RESERVE / 1P9MM_OUTER_LIGAMENT / C01_TO_C450 / REAL_CAD_KERNEL_REGENERATION_NEXT**.
