# AudioPicture V2.2 Rev.B — front carrier magnetic edge resolution

Status: **DML_EDGE_CONFLICT_ANALYTICALLY_RESOLVED / D_SHAPED_PADS_REQUIRED / MAGNET_AXIS_REQUIRES_EDGE-BIASED POCKET / REAL CAD REGENERATION GATE**

## 1. Purpose
Resolve the Rev.A circular magnet-pad overlap with the 300 x 380 mm DML projection inside the 320 x 400 mm product.

Product:
320 x 400 mm.

DML:
X=10..310
Y=10..390.

Available nominal perimeter band:
10 mm on each side.

## 2. Rev.B magnet centers
Seed centers:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

## 3. Key geometric finding
Moving the old centers only 2 mm toward the perimeter does NOT by itself solve a 12 mm circular pad overlap.

Example top:
center Y=388, circular pad radius 6 -> inner edge Y=382.

DML reaches Y=390.

Therefore the pad still projects 8 mm into the DML rectangle.

Likewise bottom:
center Y=12, R6 -> outer/inner edge reaches Y18, inside DML starting Y10.

Same issue on left/right.

Therefore the Rev.B solution must use a non-circular perimeter-biased station body and a magnet pocket whose axis is placed in the legal perimeter material.

## 4. Legal magnet-center condition
For a 6.6 mm pocket, radius:
R_POCKET=3.3 mm.

To keep the pocket itself outside the DML projection on top:
Y_CENTER - 3.3 >= 390
=> Y_CENTER >= **393.3 mm**.

Bottom:
Y_CENTER + 3.3 <=10
=> Y_CENTER <= **6.7 mm**.

Left:
X_CENTER +3.3 <=10
=> X_CENTER <= **6.7 mm**.

Right:
X_CENTER -3.3 >=310
=> X_CENTER >= **313.3 mm**.

This is the actual geometry condition if the entire magnet pocket must remain outside the DML projected area.

## 5. Carrier outer boundary consequence
Carrier projected outer boundary:
X=0.8..319.2
Y=0.8..399.2.

A 6.6 mm pocket at:
top Y=394.0 gives outer edge397.3, legal.
bottom Y=6.0 gives outer edge2.7, legal.
left X=6.0 gives outer edge2.7, legal.
right X=314.0 gives outer edge317.3, legal.

Therefore the 6 x 2 mm magnet class remains geometrically compatible with the 10 mm product perimeter band.

No smaller magnet is required solely for DML edge clearance.

## 6. Rev.C geometric center proposal
Use edge-biased centers:

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

These are the preferred next CAD centers.

## 7. D-shaped station pad
The magnet pocket remains circular.

The structural pad around it is D-shaped / perimeter-biased.

For each side:
- pocket diameter 6.6 mm;
- minimum material around pocket toward external carrier edge: process-qualified >=1.2..1.5 mm seed where geometry allows;
- DML-facing structural extension terminates at or before DML keep-out;
- perimeter-direction pad length can expand to carry load.

Seed station footprint:
approximately 10..14 mm along perimeter,
8..9 mm across perimeter band,
clipped by DML keep-out.

## 8. Top station example
M1C=(70,394).

Pocket:
Y=390.7..397.3.

DML top boundary:
Y=390.

Pocket-to-DML projected gap:
**0.7 mm**.

This is positive but small.

Recommended CAD keep-out margin:
>=0.5 mm minimum seed.

Thus M1C/M2C pass analytically with 0.7 mm nominal projected margin.

## 9. Bottom station example
M3C=(70,6).

Pocket:
Y=2.7..9.3.

DML begins:
Y=10.

Projected margin:
**0.7 mm**.

PASS analytic.

## 10. Side stations
Left X=6:
pocket X=2.7..9.3.
DML starts X=10.
margin0.7 mm.

Right X=314:
pocket X=310.7..317.3.
DML ends X=310.
margin0.7 mm.

PASS analytic.

## 11. Tolerance implication
0.7 mm nominal projected margin must absorb:
- carrier print XY tolerance;
- DML placement tolerance;
- pocket compensation;
- assembly locator tolerance.

Therefore 0.7 mm is a geometric feasibility proof, not production margin.

Production optimization sweep:
edge-center offset from product boundary:
- 5.5 mm
- 6.0 mm
- 6.5 mm.

For a 3.3 mm pocket radius:
top center Y=394.5/394.0/393.5 respectively.

Smaller offset gives more DML margin but less outer-edge material.

Optimize both.

## 12. Outer-edge ligament
At top center Y394 with carrier outer edge399.2:
available from pocket outer edge397.3 to carrier edge:
**1.9 mm**.

Bottom/left/right symmetric:
~1.9 mm.

This is workable as a first printed ASA seed but requires local strength/print validation.

A local tangential extension distributes magnetic load into the perimeter ring.

## 13. Magnet capture revision
Because the pocket is close to the outer edge:
- rear capture cap/lip must not rely on a thin radial ring everywhere;
- use tangential bridge/cap geometry tied into perimeter ring;
- front floor remains closed;
- adhesive remains secondary.

## 14. Fabric bonding land interaction
The 6 mm rear bonding land conflicts locally with magnet stations.

Therefore:
- bonding land may locally neck around each magnet station;
- minimum adhesive land path around station >=3 mm locally;
- recover full 6 mm land immediately outside station.

Fabric bond continuity is maintained around the perimeter but not necessarily at constant width.

## 15. Magnetic target placement
Targets align with M1C..M8C on product-side perimeter structure.

Targets remain discrete.

Target geometry must also remain outside DML projected hard zone and RF masks.

## 16. RF state
This geometric correction solves DML projection only.

It does NOT prove:
- radar compatibility;
- ESP32 antenna compatibility;
- magnetic field compatibility.

Exact RF masks remain a separate clipping operation.

## 17. Front-carrier real-CAD regeneration contract
Generate Rev.B carrier using:
- outer 318.4 x398.4;
- ring 10 mm;
- base1.8 mm;
- M1C..M8C;
- 6.6 mm pockets;
- D-shaped/tangential station reinforcement;
- peel recess28 x4 at lower center;
- LOC_A/LOC_B.

Then report:
- valid solid count;
- volume;
- mass sensitivity;
- bbox;
- minimum pocket-to-DML projected margin;
- minimum outer-edge ligament;
- ring connectivity after peel recess.

## 18. Acceptance
PASS if:
- one connected valid solid;
- all pocket material outside DML hard projection;
- nominal pocket-to-DML projected margin >=0.5 mm;
- outer-edge ligament >=1.5 mm;
- no station intersects peel recess;
- carrier mass <=60 g;
- no central structural member added.

## 19. Automatic checks
C431 old M1B..M8B 2 mm shift rejected as insufficient by itself.
C432 exact 6.6 mm pocket legal-center inequalities defined.
C433 6 x2 magnet class retained geometrically.
C434 M1C/M2C top centers Y394.
C435 M3C/M4C bottom centers Y6.
C436 M5C/M6C left centers X6.
C437 M7C/M8C right centers X314.
C438 nominal pocket-to-DML projected margin0.7 mm.
C439 nominal outer-edge ligament1.9 mm.
C440 D-shaped pad required.
C441 pocket remains circular.
C442 pad may expand tangentially.
C443 magnet capture tied tangentially to ring.
C444 fabric bonding land locally necks around stations.
C445 local adhesive land target >=3 mm.
C446 full 6 mm bonding land recovers outside stations.
C447 target pieces remain outside DML hard projection.
C448 RF clipping remains required.
C449 edge-offset sweep5.5/6.0/6.5 defined.
C450 real OpenCASCADE Rev.B regeneration required next.

## 20. State
The previous magnet-pad warning is now geometrically understood.

A 6 x2 mm magnet remains compatible with the 10 mm perimeter, but its center must be approximately 6 mm from the product edge rather than 12 mm.

Preferred next CAD centers:
- top Y394
- bottom Y6
- left X6
- right X314.

Nominal:
- pocket-to-DML margin0.7 mm;
- outer-edge ligament1.9 mm.

Status:
**MAGNET_AXIS_EDGE_BIASED_6MM / 0P7MM_DML_MARGIN / 1P9MM_OUTER_LIGAMENT / D_SHAPED_REINFORCEMENT / C01_TO_C450 / REAL_CAD_REGENERATION_NEXT**.
