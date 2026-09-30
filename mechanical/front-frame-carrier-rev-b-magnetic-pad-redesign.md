# AudioPicture V2.2 Rev.B — front carrier magnetic-pad redesign

Status: **REV_B_PERIMETER_BIASED_MAGNET_STATIONS / D_SHAPED_PADS / DML_HARD_KEEP_OUT_ENFORCED / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Remove the Rev.A magnetic-pad overlap with the projected DML perimeter without notching or modifying the DML.

## 2. Authoritative DML projection
DML:
- X = 10..310 mm
- Y = 10..390 mm.

For front-carrier magnetic hardware, this projection is treated as a hard XY keep-out unless a later local DML-edge model explicitly proves otherwise.

Baseline:
**no DML notch**.

## 3. Rev.B station centers
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

## 4. Why circular 12 mm pads are rejected
A centered 12 mm circular pad has 6 mm radial reach.

At centers only 2 mm from the DML projected edge, a symmetric pad necessarily extends deeply into the DML projection.

Therefore the Rev.A circular local pad is withdrawn.

## 5. D-shaped station architecture
Each station has:
- compact circular magnet pocket;
- perimeter-side structural lobe;
- flat/clipped DML-facing edge.

The pad grows toward the product perimeter, not toward the DML.

The D-shaped pad is a structural support/capture feature, not the magnetic target itself.

## 6. DML-facing clipping planes
Top stations:
pad material rearward/thickened region shall remain at Y >= 390 mm plus any required hard clearance.

Bottom:
Y <= 10 mm.

Left:
X <= 10 mm.

Right:
X >= 310 mm.

Because the carrier base ring itself may geometrically overlap the DML projection in XY while sitting forward in Z, this rule applies specifically to the **rearward magnet-pad thickening and magnetic hardware intrusion**.

## 7. Pocket feasibility warning
The magnet pocket itself is 6.6 mm diameter class.

A magnet centered at only 2 mm from the DML edge extends ~3.3 mm radially and therefore crosses the DML projected edge by ~1.3 mm.

Thus merely clipping the outer pad does not solve the hard hardware keep-out.

The magnet center must move farther outward or the DML/hardware Z relationship must prove noncollision.

Preferred:
move center outward.

## 8. Rev.B2 corrected center requirement
For a 6.6 mm pocket and 0.5 mm XY hard margin:
required center offset from DML edge:
3.3 + 0.5 = **3.8 mm**.

Use 4.0 mm nominal.

Corrected station centers:
Top:
- M1C = (70,394)
- M2C = (250,394)

Bottom:
- M3C = (70,6)
- M4C = (250,6)

Left:
- M5C = (6,135)
- M6C = (6,275)

Right:
- M7C = (314,135)
- M8C = (314,315).

These centers put the 6.6 mm pocket envelope fully outside the DML projection with ~0.7 mm nominal margin.

## 9. Product-edge feasibility
Carrier projected outer boundary:
X=0.8..319.2
Y=0.8..399.2.

At center 6 mm or 314 mm:
6.6 mm pocket envelope remains inside carrier outer boundary.

Example left:
center X6 - radius3.3 = X2.7 > 0.8.

Example right:
314 + 3.3 = 317.3 <319.2.

Top:
394+3.3=397.3 <399.2.

Bottom:
6-3.3=2.7 >0.8.

Therefore Rev.B2/MxC centers are geometrically feasible.

## 10. Station local pad envelope
Use asymmetric pad nominal envelope:
- tangential length: 12 mm
- inward/outward radial width: 8 mm class
- clipped against DML-side plane.

Local total Z thickness:
3.2 mm first kernel seed.

Pocket:
6.6 mm diameter.

Exact capture lip adds only perimeter-side material where possible.

## 11. DML margin
Pocket nearest edge relative to DML:
nominal:
4.0 - 3.3 = **0.7 mm**.

This is an XY geometric margin only.

Production margin shall be increased if print/process tolerance requires.

Sweep center offset:
4.0 / 4.5 / 5.0 mm from DML edge.

Preferred next CAD:
**4.5 mm offset** if carrier-edge material remains sufficient.

## 12. 4.5 mm preferred centers
Top:
M1D=(70,394.5)
M2D=(250,394.5)

Bottom:
M3D=(70,5.5)
M4D=(250,5.5)

Left:
M5D=(5.5,135)
M6D=(5.5,275)

Right:
M7D=(314.5,135)
M8D=(314.5,315).

Pocket-to-DML nominal margin:
4.5-3.3 = **1.2 mm**.

Pocket-to-carrier outer-edge minimum:
5.5-3.3-0.8 = **1.4 mm**.

This is tight but viable for the pocket wall/capture architecture only with local perimeter lobe optimization.

## 13. Selected next-kernel seed
Select compromise:
**4.0 mm DML-edge offset / MxC coordinates**

Reason:
- 0.7 mm DML XY margin;
- ~1.9 mm material from pocket edge to carrier outer boundary;
- better outer capture-wall feasibility than 4.5 mm offset.

Production may move to 4.5 mm after print/capture detail optimization.

## 14. Peel recess
Lower peel recess remains:
- center X160
- width28
- depth4.

Bottom magnets:
X70 and X250.

No conflict.

Progressive peel remains symmetric.

## 15. Locator interaction
LOC_A/LOC_B must be placed between magnetic stations or locally shifted.

No locator may share a thin outer pocket wall.

Magnet capture and locator load paths remain independent.

## 16. Fabric land interaction
At magnet stations, the rear bonding land may locally narrow but shall remain:
>=5 mm where adhesive is required.

If magnet pocket consumes bonding land:
use local fabric wrap bridge around the station rather than placing adhesive over the pocket.

## 17. RF masks
Moving stations closer to product perimeter improves but does not automatically prove RF compliance.

Exact:
- ESP32 antenna keep-out;
- radar cone;
- mic port;
- optical path
remain authoritative.

Any station intersecting exact RF mask is shifted tangentially along the same perimeter edge, not inward toward DML.

## 18. Kernel generation requirements
Generate Rev.B real B-rep with:
- 318.4 x398.4 outer;
- 10 mm ring;
- 1.8 mm base;
- MxC centers;
- D-shaped local station pads;
- 6.6 mm pockets;
- local total thickness3.2 mm;
- peel recess28x4;
- one connected solid.

## 19. Acceptance
Kernel:
solid_count=1.
valid=true.

Hard geometry:
- pocket envelope does not intersect DML projection;
- rearward pad thickening does not intersect DML projection;
- pocket remains inside carrier;
- peel recess preserves connectivity.

Mass:
carrier-only <=35 g preferred;
<=60 g hard subsystem carrier budget.

## 20. Automatic checks
C431 Rev.A circular 12 mm pad withdrawn.
C432 Rev.B 2 mm-offset centers rejected for 6.6 mm pocket hard keep-out.
C433 minimum center offset equation uses pocket radius plus margin.
C434 MxC centers use 4.0 mm DML-edge offset.
C435 pocket-to-DML nominal margin >=0.7 mm.
C436 pocket remains inside carrier outer boundary.
C437 D-shaped thickening grows perimeter-side.
C438 no DML notch baseline.
C439 peel recess unchanged and clear.
C440 locator cannot share thin pocket wall.
C441 fabric adhesive land locally protected.
C442 RF mask can shift station tangentially only.
C443 one-solid kernel required.
C444 valid B-rep required.
C445 carrier-only mass <=60 g.
C446 preferred carrier-only mass <=35 g.
C447 exact print tolerance may force 4.5 mm offset.
C448 magnet capture detail must preserve outer wall.
C449 global Z transform remains tied to master datum.
C450 full master-DMU collision audit follows kernel regeneration.

## 21. State
The earlier Rev.B center shift by only 2 mm is insufficient for the actual 6.6 mm magnet pocket.

The corrected next-kernel station centers are:
- (70,394)
- (250,394)
- (70,6)
- (250,6)
- (6,135)
- (6,275)
- (314,135)
- (314,315).

Status:
**MAGNET_CENTER_OFFSET_CORRECTED_TO_4MM / 6P6MM_POCKET_OUTSIDE_DML / D_SHAPED_PAD_CONTRACT / C01_TO_C450 / REAL_BREP_NEXT**.
