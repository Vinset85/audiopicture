# AudioPicture V2.2 Rev.B — front carrier DML-clearance redesign

Status: **MAGNET_CENTER_REV_B_REJECTED_AS_INSUFFICIENT / DML_SAFE_POCKET_GEOMETRY_DERIVED / CORNER_STATION_ARCHITECTURE_REQUIRED**

## 1. Purpose
Resolve the Rev.A front-carrier magnetic-pad overlap found by the integrated master DMU.

The DML projected hard region is:
- X = 10..310 mm
- Y = 10..390 mm.

No magnet pocket, hard capture feature, steel target or rigid local boss may intrude into this hard region unless a later detailed DML edge construction explicitly creates a legal non-active perimeter land.

Baseline assumes no such land.

## 2. Required hard margin
Add geometric clearance from DML projected edge:
**0.5 mm nominal hard CAD margin**.

Therefore front-frame magnetic hard features must remain in:
- left strip X <= 9.5 mm;
- right strip X >= 310.5 mm;
- bottom strip Y <= 9.5 mm;
- top strip Y >= 390.5 mm;
or in corner combinations of these strips.

## 3. Available perimeter width
Product outer boundary:
X=0..320
Y=0..400.

DML starts 10 mm from each edge.

Nominal available geometric strip:
10 mm.

With 0.5 mm DML hard margin:
usable hard-feature strip:
**9.5 mm**.

## 4. Consequence for 6 mm magnet
A circular 6.6 mm CAD pocket requires radius:
3.3 mm.

For a pocket entirely outside the DML on a straight edge, its center must satisfy:
left: X <= 9.5 - 3.3 = **6.2 mm**
right: X >= 310.5 + 3.3 = **313.8 mm**
bottom: Y <= **6.2 mm**
top: Y >= **393.8 mm**.

The previously proposed Rev.B centers at X/Y=12 mm or 388 mm are therefore NOT sufficient.

They are rejected.

## 5. Carrier outer-boundary constraint
Carrier nominal outer boundary:
X=0.8..319.2
Y=0.8..399.2.

A 6.6 mm pocket center also needs >=3.3 mm from carrier edge if fully enclosed.

Legal center ranges near edges become approximately:
- minimum X/Y = 0.8+3.3 = **4.1 mm**
- maximum X = 319.2-3.3 = **315.9 mm**
- maximum Y = 399.2-3.3 = **395.9 mm**.

Thus a straight-edge legal band exists, but is narrow:
low side center = **4.1..6.2 mm**
high X center = **313.8..315.9 mm**
high Y center = **393.8..395.9 mm**.

Width only about:
**2.1 mm**.

This is too tolerance-sensitive for eight conventional circular stations on printed ASA.

## 6. Design decision
Do NOT freeze straight-edge 6.6 mm circular pockets.

Preferred architecture changes to:
**corner-biased / elongated perimeter magnetic modules**, where local carrier geometry can gain area in both X and Y while remaining outside the DML rectangle.

The magnet itself may remain 6 x 2 mm, but the supporting/capture geometry is shaped into the product corners/perimeter.

## 7. Corner module principle
At each product corner there is a square region outside the DML rectangle.

Use four primary corner modules:
- CML lower-left
- CMR lower-right
- CUL upper-left
- CUR upper-right.

Each module may contain:
- one magnet, or
- two smaller magnets if force/peel tuning requires.

This allows 4 / 8 effective magnetic elements without forcing eight fragile straight-edge pockets.

## 8. Four-corner center seeds
For 6.6 mm pockets:
- CLL = (6.0, 6.0)
- CLR = (314.0, 6.0)
- CUL = (6.0, 394.0)
- CUR = (314.0, 394.0).

These lie inside the carrier outer boundary and outside the DML rectangle with the 0.5 mm hard-margin policy for a 3.3 mm pocket radius.

Minimum pocket edge:
2.7 mm from product/carrier-adjacent local coordinates depending exact outer datum.

DML-facing pocket edge:
9.3 mm coordinate at low side or 310.7/390.7 high side, preserving about 0.7 mm from the DML boundary.

## 9. Tolerance warning
The corner seeds still have limited geometric margin.

Therefore final production pocket diameter and center must be jointly tolerance-optimized.

Preferred next options:
A. reduce pocket OD with tighter process/capture design;
B. use smaller magnet diameter;
C. locally widen the non-active front perimeter if DML edge construction permits;
D. move magnets to product-side structure with thin steel target in carrier corners.

## 10. Smaller-magnet sensitivity
A 5 mm magnet with ~5.5 mm process pocket has radius 2.75 mm.

Legal straight-edge center:
<=9.5-2.75 = 6.75 mm.

Carrier containment:
>=0.8+2.75 =3.55 mm.

Legal band:
3.55..6.75 mm = **3.20 mm**.

Better, but still narrow.

A 4 mm magnet with ~4.5 mm pocket radius 2.25 mm:
legal band:
3.05..7.25 mm = **4.20 mm**.

Therefore smaller magnets materially improve manufacturability.

## 11. Retention-force implication
Previous target total assembled retention remains:
20..30 N.

Four 6 mm corner stations require:
5..7.5 N average assembled per station, which may be too close to ideal catalogue pull for controlled peel.

Eight smaller magnets distributed as two per corner module can provide better force tuning and redundancy.

Preferred next evaluation:
**8 x 4..5 mm class magnets, two per corner module**, subject to real catalogue selection and magnetic-circuit calculation/test.

## 12. RF benefit
Corner concentration also reduces the amount of magnetic/steel hardware along the side edges and can simplify exclusion from:
- radar right-side region;
- ESP32 upper electronics region;
- microphone acoustic paths.

However upper-right corner remains subject to exact ESP32 antenna keep-out.

No corner is automatically RF legal until exact antenna/radar masks are applied.

## 13. Peel behavior
Corner-only retention changes peel curve.

Lower-center peel feature first bends/separates the lower span, then releases lower corner modules.

This can be favorable because no magnet sits immediately adjacent to the peel recess.

Frame flexural stress must be checked.

## 14. Rev.B carrier solid policy
Do not regenerate a misleading “collision-free” solid using the rejected 12/388 coordinates.

The next real B-rep shall use:
- corner module architecture;
- selected smaller magnet candidate if adopted;
- explicit DML hard keep-out boolean;
- explicit 0.5 mm clearance offset.

CAD generation must boolean-subtract the DML hard keep-out plus margin from every magnetic hard feature.

## 15. Parametric keep-out
Define:
DML_KO_MAG =
DML projected rectangle expanded by 0.5 mm:
X=9.5..310.5
Y=9.5..390.5.

All magnet/capture/target hard solids must satisfy:
intersection(feature, DML_KO_MAG) = 0.

This becomes an automatic CAD assertion.

## 16. Automatic checks
C431 DML magnetic keep-out expanded by 0.5 mm.
C432 Rev.B 12/388 edge-center proposal rejected.
C433 6.6 mm pocket legal straight-edge center band calculated.
C434 narrow 2.1 mm straight-edge band flagged as tolerance-sensitive.
C435 no DML notch used.
C436 four corner-module architecture defined.
C437 6 x 2 magnet corner seed coordinates defined.
C438 corner pocket vs DML_KO_MAG zero intersection required.
C439 corner pocket vs carrier exterior containment required.
C440 5 mm magnet sensitivity calculated.
C441 4 mm magnet sensitivity calculated.
C442 smaller magnet improves printable tolerance band.
C443 20..30 N total retention target unchanged.
C444 8 smaller magnets / 2 per corner module promoted for evaluation.
C445 exact upper-right RF legality remains open.
C446 peel behavior recheck required.
C447 next B-rep must use explicit DML keep-out boolean.
C448 rejected coordinate map cannot be promoted to production.
C449 magnet selection must be revisited before B-rep freeze.
C450 front carrier Rev.B remains open pending smaller-magnet selection.

## 17. State
The integrated geometric solve demonstrates that simply moving the previous 6 mm magnets from 14 to 12 mm from the edge does not solve the DML collision.

For a 6.6 mm pocket and 0.5 mm DML margin, a straight-edge center has only about 2.1 mm of legal positioning width.

This is not robust enough for the printed production carrier.

Preferred direction:
**corner modules + smaller magnets, likely eight 4..5 mm class elements arranged two per corner, followed by real component selection and B-rep regeneration.**

Status:
**REV_B_EDGE_MAGNET_LAYOUT_REJECTED / DML_KO_0P5MM_DEFINED / CORNER_MODULE_ARCHITECTURE_SELECTED / SMALLER_MAGNET_SELECTION_NEXT / C01_TO_C450**.
