# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnetic stations

Status: **MAGNET_PAD_REV_B_GEOMETRY_DEFINED / DML_OVERLAP_REMOVED_BY_DIRECTIONAL_PAD / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A master-DMU warning in which nominal 12 mm circular magnetic pads crossed the DML projected hard region.

DML hard projection:
- X=10..310 mm
- Y=10..390 mm.

Do not notch or reduce the active DML as the baseline solution.

## 2. Revised station centers
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

## 3. Design issue
A symmetric 12 mm pad around these centers still crosses the DML hard projection.

Therefore station support geometry must be directional.

The magnetic pocket remains compact while the structural support material grows toward the product perimeter, not toward the DML.

## 4. D-shaped pad principle
Each station consists of:
- central magnet pocket region;
- perimeter-side structural lobe;
- DML-facing clipped face.

The DML-facing rigid edge is constrained to remain on the legal side of the DML projected boundary plus a configurable clearance.

## 5. DML projected clearance
Seed hard projected clearance:
**0.5 mm**

Thus carrier magnetic support material shall satisfy:

Top stations:
Y >= 390.5 mm where overlapping DML X span.

Bottom stations:
Y <= 9.5 mm where overlapping DML X span.

Left stations:
X <= 9.5 mm where overlapping DML Y span.

Right stations:
X >= 310.5 mm where overlapping DML Y span.

Because magnet centers themselves are at Y388/Y12/X12/X308, a full 6.6 mm pocket cannot satisfy these limits if its entire rigid pocket is required outside the DML projection.

Therefore the magnet itself cannot remain centered at those Rev.B seed coordinates in the same front-side Z layer.

## 6. Important geometry correction
The Rev.B center shift alone is insufficient.

For a 6.6 mm diameter magnet pocket plus practical wall, the magnetic station center must move farther toward the product perimeter OR be placed in a different Z/interface layer that does not collide with the DML.

Preferred solution:
**move station centers farther outward**.

## 7. Rev.C geometric center proposal
Using 6.6 mm pocket and minimum 1.0 mm DML-facing structural wall:

Required half-width:
3.3 + 1.0 = 4.3 mm.

For 0.5 mm projected DML clearance:

Top center:
Y >= 390 + 0.5 + 4.3 = **394.8 mm**.

Bottom center:
Y <= 10 - 0.5 - 4.3 = **5.2 mm**.

Left center:
X <= **5.2 mm**.

Right center:
X >= **314.8 mm**.

These positions are very close to the product edge and incompatible with a conventional centered 6.6 mm pocket inside the current 318.4 x 398.4 carrier envelope.

## 8. Consequence
A magnet-in-front-carrier architecture using 6 mm class discs at the same Z as the DML perimeter is geometrically poor for a 10 mm DML-to-product edge margin.

Do not force the CAD.

## 9. Preferred architecture change
Move the **magnets to the product-side/rear structural interface** and place thin discrete steel targets in the front carrier.

Front carrier then needs only thin target tabs, which can fit within the shallow perimeter geometry with much less Z/XY intrusion.

This is the inverse of the prior candidate-A magnetic circuit option.

Preferred:
- magnet: product side;
- steel target: removable front carrier.

Benefits:
- front carrier becomes thinner/lighter;
- no 6.6 x 2.2 magnet pocket competing with DML;
- easier fabric carrier geometry;
- magnet mechanically captured in deeper product-side structure;
- front FRU contains no loose brittle magnet;
- target can be thin and shaped to legal perimeter arc.

## 10. Product-side magnet stations
Magnets shall be mounted on legal ASA/PC-CF structural nodes outside:
- radar RF keep-out;
- ESP32 RF keep-out;
- microphone acoustic path;
- DML compliant mount path.

The magnet may sit rearward of the DML front perimeter plane if its flux path reaches the front target through a controlled nonmagnetic gap.

Exact station Z becomes part of magnetic circuit optimization.

## 11. Front-carrier target geometry
Replace each magnet pad with a thin target seat.

Seed target:
- low-carbon steel;
- thickness 0.8..1.0 mm;
- shaped rectangular/D tab;
- nominal 8 x 10 mm class before clipping.

Target can extend primarily toward product perimeter.

Target must be mechanically trapped plus bonded.

No continuous steel ring.

## 12. Front carrier Rev.B effect
Remove:
- eight 6.6 mm magnet pockets;
- eight 3.2 mm local magnetic pad protrusions.

Add:
- eight shallow target seats;
- local carrier reinforcement only as needed.

Expected carrier maximum local thickness can return close to base 1.8..2.2 mm plus target-seat detail rather than 3.2 mm magnet pads.

## 13. Force implication
The previous 20..30 N total assembled target remains.

The magnetic circuit now includes:
- product-side magnet;
- nonmagnetic carrier/shell/gap stack;
- front-side thin steel target.

Actual force must be measured/modelled for this reversed architecture.

Catalogue pull values remain non-authoritative.

## 14. Service implication
When front frame is removed:
- magnets remain safely in the product;
- front assembly carries only steel targets.

This improves service safety and reduces risk of magnet loss.

## 15. RF implication
Steel targets are still prohibited in radar/ESP32 RF hard keep-outs.

Product-side magnets also obey the same RF masks.

Because magnet and target are separated in Z, both must be checked independently.

## 16. CAD decision
Do not generate a misleading Rev.B OpenCASCADE solid with D-shaped magnet pockets that mathematically still overlap the DML.

Instead:
1. retire front-carrier magnet pockets;
2. generate front-carrier target seats;
3. generate product-side magnet capture nodes;
4. run master-DMU collision;
5. run magnetic force sweep.

## 17. Automatic checks
C431 Rev.B center shift alone evaluated.
C432 6.6 mm pocket geometric half-width evaluated.
C433 DML projected hard clearance seed 0.5 mm defined.
C434 top legal magnet-center requirement calculated.
C435 bottom legal magnet-center requirement calculated.
C436 left legal magnet-center requirement calculated.
C437 right legal magnet-center requirement calculated.
C438 product-edge incompatibility identified.
C439 DML notch rejected as baseline.
C440 front-carrier magnet-pocket architecture retired.
C441 product-side magnet architecture selected.
C442 front-carrier thin steel targets selected.
C443 no continuous steel ring.
C444 target mechanically trapped plus bonded.
C445 magnets mechanically captured product-side.
C446 20..30 N total retention target preserved.
C447 catalogue pull force remains non-authoritative.
C448 magnet and target both obey RF masks.
C449 front carrier local 3.2 mm magnet pads removed next CAD revision.
C450 next kernel generation uses target-seat carrier architecture.

## 18. State
Attempting to solve the issue only by D-shaped front magnet pads reveals a fundamental packaging conflict: the 10 mm product-edge margin around a 300 x 380 mm DML is too narrow for robust 6 mm-class magnet pockets in the same perimeter layer.

The architecture is therefore improved rather than forced.

Selected direction:
**MAGNETS_STAY_WITH_PRODUCT / THIN_STEEL_TARGETS_STAY_WITH_REMOVABLE_FRONT_FRAME**

Status:
**FRONT_MAGNET_POCKETS_RETIRED / PRODUCT_SIDE_MAGNETS_SELECTED / THIN_TARGET_FRONT_CARRIER / C01_TO_C450 / REV_C_KERNEL_GENERATION_NEXT**.
