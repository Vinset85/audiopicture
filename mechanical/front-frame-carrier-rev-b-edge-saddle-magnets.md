# AudioPicture V2.2 Rev.B — edge-saddle magnetic carrier correction

Status: **REV_B_12MM_PAD_CONCEPT_REJECTED / EDGE_SADDLE_MAGNET_ARCHITECTURE_SELECTED / CAD_KERNEL_REGEN_REQUIRED**

## 1. Finding
The prior Rev.B magnetic center seed at 12/308/388 mm does not geometrically clear the DML projection X10..310, Y10..390.

For a 6.6 mm pocket, radius 3.3 mm, a magnet/pocket entirely outside the DML projection requires center:
- left/bottom <=6.7 mm;
- right >=313.3 mm;
- top >=393.3 mm.

A 12 mm circular reinforcement pad would require center <=4 mm or >=316/396 mm, which is incompatible with a conventional symmetric pad and useful outer carrier wall.

Therefore the symmetric 12 mm pad concept is rejected.

## 2. Selected architecture
Use an **edge-saddle station**:
- magnet pocket remains entirely in the 10 mm perimeter band outside the DML;
- reinforcement grows tangentially along the product perimeter, not inward toward DML;
- local rear thickening is clipped at the DML hard boundary;
- no DML notch.

## 3. Rev.C center seeds
Using carrier outer boundary 0.8..319.2 / 0.8..399.2 and 6.6 mm pocket:

Bottom:
M3C=(70,5.5)
M4C=(250,5.5)

Top:
M1C=(70,394.5)
M2C=(250,394.5)

Left:
M5C=(5.5,135)
M6C=(5.5,275)

Right:
M7C=(314.5,135)
M8C=(314.5,315).

## 4. Geometric margins
Pocket radius:
3.3 mm.

At low-side center 5.5:
- outer carrier boundary margin = 5.5 - 3.3 - 0.8 = **1.4 mm**;
- DML-edge clearance = 10 - (5.5 + 3.3) = **1.2 mm**.

Equivalent margins apply at opposite sides.

These are CAD nominal margins and require print/tolerance review.

## 5. Saddle reinforcement
Symmetric circular 12 mm pad is removed.

Use tangential capsule/saddle reinforcement:
- radial width limited to legal perimeter band;
- tangential length seed 14..18 mm;
- local total Z thickness 3.2 mm seed;
- root fillets >=1.0 mm where space permits.

The DML-facing boundary of every saddle is clipped to remain outside the DML hard projection plus tolerance reserve.

## 6. Pocket/capture
6.6 mm process-seed pocket retained for 6 x 2 mm reference magnet.

Mechanical capture remains mandatory.

Because only ~1.4 mm nominal polymer remains between pocket and carrier outer boundary, capture detail must not rely on a fragile thin radial lip.

Preferred capture:
- closed front floor;
- rear printed/inserted cap spanning tangential saddle;
- adhesive secondary retention.

## 7. Tolerance gate
Nominal DML clearance 1.2 mm is sufficient for DMU separation but not yet production release.

Allocate reserve for:
- carrier print XY error;
- DML placement;
- pocket compensation;
- assembly registration.

Production target:
>=0.5 mm worst-case rigid-to-DML projected clearance after tolerance stack.

If this cannot be demonstrated, reduce pocket diameter/component or revise carrier perimeter architecture.

## 8. Consequence for magnet choice
The 6 x 2 mm S-06-02-N remains packaging candidate.

The 6.35 mm D41 is less attractive geometrically because it consumes more of the narrow radial perimeter band despite being thinner.

Exact MPN remains validation-open.

## 9. CAD regeneration requirements
Regenerate front carrier with:
- Rev.C centers;
- edge-saddle pads;
- DML hard clipping;
- existing 28 x 4 lower peel recess;
- one connected solid;
- all eight pockets/captures;
- no material crossing DML projection in local thickened station features.

## 10. Checks
C431 prior 12/308/388 seed rejected.
C432 symmetric 12 mm pad rejected.
C433 6.6 mm pocket outside DML projection nominally.
C434 pocket outer-boundary material >=1.4 mm nominal.
C435 pocket-to-DML clearance >=1.2 mm nominal.
C436 saddle reinforcement grows tangentially.
C437 saddle DML-facing boundary clipped.
C438 no DML notch.
C439 mechanical capture does not rely on thin radial lip.
C440 exact tolerance stack must preserve >=0.5 mm rigid clearance.
C441 Rev.C centers regenerate parametrically.
C442 lower peel recess remains clear of M3C/M4C.
C443 D41 remains alternate but not preferred for radial packaging.
C444 real B-rep regeneration required.
C445 one-solid kernel validity required.

## 11. State
Rev.B magnetic-pad geometry exposed a real incompatibility and is superseded.

New seed:
**EDGE-SADDLE / CENTERS 5.5 MM FROM PRODUCT EDGE / 6.6 MM POCKET / 1.2 MM NOMINAL DML CLEARANCE**

Status:
**MAGNET_PAD_COLLISION_CORRECTED_ANALYTICALLY / REV_C_EDGE_SADDLE_SEED / C01_TO_C445 / REAL_BREP_REGEN_NEXT**.
