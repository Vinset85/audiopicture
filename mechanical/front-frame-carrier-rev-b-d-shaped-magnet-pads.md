# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnet pads

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_PROJECTED_OVERLAP_REMOVED_BY_BOOLEAN_CLIP / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Correct the Rev.A magnetic-station packaging warning found by the integrated master DMU.

The active DML projected rectangle is:
- X=10..310 mm
- Y=10..390 mm.

No rigid magnet pad may intrude into the DML hard projected keep-out.

## 2. Revised magnet centers
Adopt Rev.B seeds:

Top:
- M1B=(70,388)
- M2B=(250,388)

Bottom:
- M3B=(70,12)
- M4B=(250,12)

Left:
- M5B=(12,135)
- M6B=(12,275)

Right:
- M7B=(308,135)
- M8B=(308,315).

## 3. Important geometric consequence
A circular 12 mm pad centered only 2 mm from the DML edge still overlaps the DML projected rectangle.

Therefore moving the centers alone is insufficient.

Rev.B uses a perimeter-biased clipped/D-shaped station.

## 4. DML hard keep-out
Define:
K_DML_MAG = projected DML rectangle plus a positive rigid clearance.

Nominal rigid XY clearance:
**0.8 mm**

Sweep:
0.5 / 0.8 / 1.0 mm.

Thus magnet-pad material is boolean-clipped against:
- X=9.2..310.8
- Y=9.2..390.8
for the nominal 0.8 mm case.

The DML itself is never notched for magnet packaging.

## 5. Station construction
Each station begins from a nominal circular support primitive:
- outer diameter 12 mm;
- local total Z thickness 3.2 mm class.

Then:
1. union support primitive to perimeter carrier;
2. subtract K_DML_MAG from the support extension;
3. preserve only the perimeter-side material;
4. create magnet pocket only if minimum wall/capture constraints remain.

The resulting shape is D-shaped/segment-like where clipped.

## 6. Pocket feasibility issue
A centered 6.6 mm pocket cannot be fully surrounded by a pad if its center is too close to the DML hard boundary.

Therefore the magnet center and support-pad center are decoupled parametrically.

Define:
- station nominal datum point MxB;
- magnet center offset outward from DML by DELTA_MAG_OUT.

Initial:
**DELTA_MAG_OUT = 3.0 mm**

This produces first magnet-center seeds:
Top:
- M1M=(70,391)
- M2M=(250,391)

Bottom:
- M3M=(70,9)
- M4M=(250,9)

Left:
- M5M=(9,135)
- M6M=(9,275)

Right:
- M7M=(311,135)
- M8M=(311,315).

These coordinates are near/outside the DML projection while remaining inside the 320 x 400 carrier envelope.

## 7. Edge packaging
Carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

For a 6.6 mm magnet pocket centered at X=9 or Y=9:
minimum center-to-carrier-edge distance is ~8.2 mm.

This is sufficient for a 3.3 mm pocket radius plus local outer wall in the nominal geometry.

For right center X311:
distance to outer carrier edge ~8.2 mm.

For top Y391:
distance to outer carrier edge ~8.2 mm.

Thus outward relocation is geometrically plausible.

## 8. Revised support primitive
Use asymmetric pad:
- perimeter-side extent: 6.0 mm nominal beyond magnet center where legal;
- DML-side extent: clipped to preserve K_DML_MAG;
- tangential width: 12 mm seed.

Minimum wall around magnet pocket:
**1.2 mm seed**
where structurally required.

If clipping reduces wall below 1.2 mm:
- enlarge tangential pad;
- move magnet farther outward;
- do not violate DML keep-out.

## 9. Magnet pocket
Candidate A remains:
6 x 2 mm magnet.

Pocket:
- diameter 6.6 mm process seed;
- depth/capture compatible with local 3.2 mm station thickness.

Front-side floor:
target >=0.5 mm nominal before process qualification.

Rear mechanical capture:
cap/lip feature remains required.

## 10. Global Z behavior
Rev.B does not increase nominal front stack.

Base carrier:
1.8 mm local structural thickness.

Station:
3.2 mm local maximum.

The local thickening is allowed only in perimeter regions outside DML hard keep-out.

Therefore the active fabric-to-DML gap remains governed by the fabric/DML stack, not the magnet station.

## 11. DML collision rule
Hard condition:
intersection(PAD_SOLID, K_DML_MAG_EXTRUDED) = empty.

Hard condition:
intersection(MAGNET_SOLID, K_DML_MAG_EXTRUDED) = empty.

No tolerance waiver is allowed.

## 12. Tangential station width
If 12 mm is insufficient after clipping:
sweep:
12 / 14 / 16 mm.

Increase tangential width before increasing intrusion toward DML.

## 13. Carrier connectivity
Each clipped station must remain connected to the perimeter ring by a minimum neck.

Seed minimum neck:
**3.0 mm tangentially continuous polymer path**.

Exact FEA not required for front-frame wall structure unless handling test/warp indicates weakness, but geometric connectivity is mandatory.

## 14. Peel interaction
Bottom magnets move outward to Y=9.

Peel recess remains:
- center X160
- width28
- depth4.

No interference with M3M/M4M.

Greater separation from the center peel feature supports progressive release.

## 15. RF rules
Coordinate movement does not override:
- radar keep-out;
- ESP32 antenna keep-out;
- microphone keep-outs;
- optical keep-out.

Exact RF masks can still reject an individual station.

Station tangential sliding is allowed before changing station count.

## 16. CAD regeneration algorithm
For each station:
1. place magnet center MxM;
2. create pocket/capture local frame;
3. create tangential support primitive;
4. intersect support with legal perimeter region;
5. subtract DML hard keep-out;
6. union with base carrier;
7. cut magnet pocket;
8. validate minimum wall;
9. validate connected solid.

Then regenerate full carrier and run:
- B-rep validity;
- solid count;
- volume;
- mass;
- bbox;
- DML intersection.

## 17. Acceptance
PASS only if:
- one valid primary carrier solid;
- all eight stations connected;
- all eight magnet pockets geometrically viable;
- zero DML hard-keepout intersection;
- carrier remains within 320 x 400;
- front stack unchanged;
- peel recess retained.

## 18. Automatic checks
C431 Rev.B station datum points generated.
C432 magnet centers offset outward by 3 mm seed.
C433 DML magnetic keep-out includes 0.8 mm nominal rigid clearance.
C434 pad/DML intersection == 0.
C435 magnet/DML intersection == 0.
C436 DML is not notched for magnet packaging.
C437 magnet pocket diameter 6.6 mm seed retained.
C438 minimum pocket wall target >=1.2 mm.
C439 station tangential width sweep 12/14/16 supported.
C440 minimum station neck >=3.0 mm.
C441 carrier outer envelope <=318.4 x 398.4 nominal boundary.
C442 local station max thickness remains 3.2 mm class.
C443 front acoustic Z stack unchanged.
C444 bottom stations clear peel recess.
C445 RF masks remain authoritative.
C446 station tangential sliding permitted.
C447 station count remains 8 baseline.
C448 full carrier must regenerate as one valid B-rep.
C449 CAD mass/volume must be remeasured after regeneration.
C450 exact DML intersection audit required from regenerated B-rep.

## 19. State
Rev.B corrects the conceptual error in Rev.A:
perimeter-biased center points alone do not guarantee DML clearance.

The station geometry is now explicitly clipped against a DML hard keep-out, while the magnet itself is moved farther toward the product perimeter.

Status:
**D_SHAPED_PERIMETER_MAGNET_STATIONS / MAGNET_CENTERS_OUTWARD_3MM / DML_KO_0P8MM / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
