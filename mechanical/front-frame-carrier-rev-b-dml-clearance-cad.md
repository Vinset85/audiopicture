# AudioPicture V2.2 Rev.B — front carrier DML-clearance CAD

Status: **REAL_OPENCASCADE_REV_B / MAGNET_PAD_TO_DML_PROJECTED_INTERSECTION_ZERO / ONE_VALID_SOLID**

## 1. Objective
Correct the Rev.A magnetic-station geometry after the integrated DMU showed that circular 12 mm pads overlapped the DML projected perimeter.

The DML remains unchanged.

## 2. Authoritative DML projected hard region
DML projection:
- X = 10..310 mm
- Y = 10..390 mm.

Magnetic station reinforcement material shall have zero positive-volume intersection with this projected hard region.

Shared/tangent boundary is not credited as manufacturing clearance; final CAD adds process clearance.

## 3. Rev.B station centers
The previous intermediate seed centers at 12/308 and 12/388 were insufficient for a symmetric 12 mm reinforcement.

The real CAD-kernel iteration therefore moves the magnetic pocket centers into the outer perimeter band:

Top:
- M1C = (70, 392.4)
- M2C = (250, 392.4)

Bottom:
- M3C = (70, 7.6)
- M4C = (250, 7.6)

Left:
- M5C = (7.6, 135)
- M6C = (7.6, 275)

Right:
- M7C = (312.4, 135)
- M8C = (312.4, 315).

These are CAD iteration coordinates, subject to final cosmetic-edge and target-stack validation.

## 4. Reinforcement pad
The circular 12 mm pad is withdrawn.

Rev.B diagnostic reinforcement:
- tangential length 12 mm;
- radial width 4 mm;
- local Z thickness 3.2 mm;
- perimeter-biased;
- equivalent to a clipped/D-shaped reinforcement concept.

Top/bottom pads:
12 x 4 mm.

Side pads:
4 x 12 mm.

Final fillets and D-shape contour remain detail features.

## 5. Magnet pocket
Diagnostic pocket:
- diameter 6.6 mm;
- rear loaded;
- 0.6 mm front floor seed;
- 2.6 mm rear cut through local 3.2 mm station.

Exact retention cap/lip remains open.

## 6. Real kernel result
CadQuery/OpenCASCADE result:
- solid count = 1;
- B-rep validity = PASS;
- volume = **24,771.62 mm3 = 24.772 cm3**;
- bounding box = **318.4 x 398.4 x 3.2 mm**.

Carrier-only ASA mass sensitivity:
- rho 1.05 -> **26.01 g**
- rho 1.075 -> **26.63 g**
- rho 1.10 -> **27.25 g**.

## 7. DML intersection audit
Reinforcement-pad union intersected with the DML projected hard prism.

Result:
**0.0 mm3 positive-volume intersection**.

Therefore the specific Rev.A pad/DML collision is removed in the Rev.B kernel geometry.

The base perimeter carrier naturally occupies perimeter/support regions associated with the DML boundary and is not the same collision class; the zero-intersection criterion here applies to the added magnetic reinforcement pads.

## 8. Comparison to Rev.A
Rev.A:
- volume 26.888 cm3;
- mass 28.2..29.6 g;
- circular/local pads generated a DML projection warning.

Rev.B:
- volume 24.772 cm3;
- mass 26.0..27.25 g;
- perimeter-biased clipped pads;
- added-pad/DML projected intersection = zero.

Rev.B is lighter and geometrically cleaner.

## 9. Remaining edge clearance
The magnetic pockets now sit close to the product cosmetic perimeter.

Before production freeze check:
- minimum polymer wall to visible outer edge;
- fabric wrap/bonding land;
- target alignment;
- magnet capture wall thickness;
- print tolerance;
- corner/edge impact resistance.

If required, reduce magnet diameter or use a non-circular reinforcement rather than moving material back toward the DML.

## 10. Magnetic-force consequence
Moving the pocket toward the perimeter does not change the 20..30 N total retention target.

However exact target position and effective magnetic gap must be regenerated with the new centers.

Catalogue magnet pull force remains non-authoritative for the assembly.

## 11. STEP
Generated DMU artifact:
**AP22_FRONT_CARRIER_REV_B_DMU.step**

Use:
- master DMU;
- collision checking;
- mass/CG update.

Not manufacturing release.

## 12. Automatic checks
C431 Rev.B real B-rep generated.
C432 solid count == 1.
C433 kernel validity PASS.
C434 circular 12 mm station pad withdrawn.
C435 perimeter-biased pad geometry generated.
C436 magnetic reinforcement/DML positive-volume intersection == 0.
C437 DML geometry unchanged.
C438 carrier volume recorded.
C439 carrier mass sensitivity recorded.
C440 Rev.B carrier lighter than Rev.A.
C441 bounding box remains within carrier envelope.
C442 local maximum Z remains 3.2 mm.
C443 magnet pocket diameter remains 6.6 mm diagnostic.
C444 magnet pocket front floor exists.
C445 final capture lip remains open.
C446 cosmetic outer-edge wall check required.
C447 fabric bonding-land check required with new station centers.
C448 target alignment regenerated with Rev.B centers.
C449 total magnetic retention target remains 20..30 N.
C450 Rev.B STEP remains DMU-only.

## 13. State
The magnetic-pad/DML collision found by the integrated audit has been removed in a real CAD-kernel iteration without modifying the DML.

Status:
**FRONT_CARRIER_REV_B_ONE_SOLID / 24P772CM3 / 26P0_TO_27P25G / MAG_PAD_DML_INTERSECTION_ZERO / C01_TO_C450 / EDGE_AND_FABRIC_LAND_AUDIT_NEXT**.
