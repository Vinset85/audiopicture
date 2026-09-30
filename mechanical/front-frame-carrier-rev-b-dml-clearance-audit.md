# AudioPicture V2.2 Rev.B — front carrier DML-clearance audit

Status: **MAGNET_DIAMETER_6MM_INCOMPATIBLE_WITH_PURE_10MM_PERIMETER_BAND / D_SHAPED_SUPPORT_DOES_NOT_SOLVE_MAGNET_BODY / ARCHITECTURE_CHANGE_REQUIRED**

## 1. Purpose
Test the proposed Rev.B perimeter-biased magnetic stations against the actual 300 x 380 mm DML projection inside the 320 x 400 mm product.

This is a geometry proof before generating a misleading B-rep.

## 2. Product and DML projection
Product:
X=0..320
Y=0..400.

DML:
X=10..310
Y=10..390.

Therefore the nominal non-DML perimeter band is only:
**10 mm per side**.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

## 3. Candidate magnet
Packaging reference:
6 mm diameter x 2 mm thick.

Magnet radius:
R_MAG=3.0 mm.

Pocket seed:
6.6 mm diameter.

Pocket radius:
R_POCKET=3.3 mm.

The magnet body itself cannot be D-shaped.

## 4. Required center location for zero DML overlap
For a circular 6.6 mm pocket to remain fully outside the DML projection:

Left side:
X_center + 3.3 <= 10
therefore X_center <= **6.7 mm**.

Right side:
X_center - 3.3 >= 310
therefore X_center >= **313.3 mm**.

Bottom:
Y_center <= **6.7 mm**.

Top:
Y_center >= **393.3 mm**.

## 5. Conflict with carrier outer edge
Carrier outer edge begins at X/Y=0.8 and ends at 319.2/399.2.

To retain even 1.0 mm polymer outside a 6.6 mm pocket:

Left minimum center:
0.8 + 1.0 + 3.3 = **5.1 mm**.

Legal left center interval:
**5.1..6.7 mm**.

Width:
only **1.6 mm**.

Equivalent narrow legal interval exists on all four sides.

For a more robust 1.5 mm outer ligament:
minimum center=5.6 mm.
Legal interval=5.6..6.7 mm.
Only **1.1 mm** wide.

This is too tolerance-sensitive for the current printed architecture.

## 6. Rev.B center audit
Previously proposed:
left X=12
right X=308
bottom Y=12
top Y=388.

These centers fail zero-DML-overlap for a 6.6 mm circular pocket.

Moving from 14 to 12 mm improved the conflict but did not solve it.

## 7. D-shaped pad interpretation
A D-shaped polymer support pad can keep its DML-facing polymer boundary clear.

However:
- the magnet remains circular;
- the magnet pocket remains circular;
- therefore a D-shaped support alone cannot make a 6 mm magnet legal at X=12/Y=12/etc.

This invalidates the assumption that pad reshaping alone closes the conflict.

## 8. Architectural options
### Option A — very edge-biased 6 mm magnet
Centers approximately 6.0 mm from the product edge.

Pros:
- retains current magnet candidate.

Cons:
- very narrow polymer ligament;
- print tolerance/warp sensitivity;
- edge cosmetic risk;
- weak pocket structure;
- difficult fabric wrap/bonding land coexistence.

Not preferred.

### Option B — smaller magnets
Use smaller diameter magnets, e.g. 3..4 mm class, distributed over more stations if necessary.

Pros:
- improves edge ligament;
- preserves no-DML-overlap;
- allows more robust carrier.

Cons:
- exact magnetic circuit and force must be reselected.

Preferred direction for magnetic-only architecture.

### Option C — move magnetic retention outside the front-carrier/DML plane
Create product-side perimeter ears/returns at a different Z so magnet/target circuit sits behind the DML edge projection rather than beside it.

Pros:
- can retain 6 mm magnet class;
- more structural material available.

Cons:
- consumes scarce Z;
- must not violate DML compliant mount or 40 mm stack.

Viable only with detailed section design.

### Option D — hybrid retention
Use geometric clips/locators for primary retention and fewer/smaller magnets for seating/anti-rattle.

Pros:
- reduces magnetic force requirement and metal count;
- smaller magnet package possible.

Cons:
- clip fatigue/removal force must be qualified.

Strong candidate.

## 9. Preferred next architecture
Do not generate the previously described 6 mm / X12 Rev.B B-rep as if it were solved.

Preferred:
**hybrid retention with smaller magnets**, while keeping tool-less peel removal.

Seed:
- 8 perimeter stations retained conceptually;
- 4 mechanical registration/retention features;
- 4 to 8 smaller magnetic seating stations depending measured force;
- magnet diameter target <=4 mm class.

Exact topology to be optimized.

## 10. Smaller-magnet geometric screen
For a 4.0 mm magnet:
R=2.0 mm.
Pocket seed approximately 4.4 mm, R=2.2.

Zero DML overlap requires left center <=7.8 mm.

With 1.5 mm outer ligament:
center >=0.8+1.5+2.2=4.5 mm.

Legal center band:
**4.5..7.8 mm**, width 3.3 mm.

This is materially better than 6 mm class.

For a 3.0 mm magnet with ~3.4 mm pocket:
R=1.7.
Legal band with 1.5 mm outer ligament:
4.0..8.3 mm, width 4.3 mm.

## 11. Fabric bonding interaction
The 6 mm rear bonding land also occupies perimeter width.

Magnet pocket, outer ligament and adhesive land cannot all be treated as independent full-width features in the same local section.

At magnetic stations:
- bonding land must locally route around pocket;
- minimum adhesive area must be recovered longitudinally;
- fabric wrap radius remains continuous.

Smaller magnets improve this substantially.

## 12. DML policy
The DML remains unchanged.

No notch in the 300 x 380 active panel is introduced to accommodate front-frame retention.

No hard magnet/target is allowed to preload the compliant DML perimeter.

## 13. CAD consequence
Rev.B solid generation is intentionally blocked until the retention topology is corrected.

This avoids creating a valid kernel solid that is invalid at product level.

Next CAD generation shall use:
- <=4 mm magnet candidate or
- hybrid clip/magnet system or
- proven alternate-Z perimeter return.

## 14. Automatic checks
C431 DML perimeter band calculated as 10 mm.
C432 6.6 mm pocket zero-overlap center bound calculated.
C433 Rev.B X/Y=12/308/388 centers fail zero-DML-overlap.
C434 D-shaped support cannot change circular magnet-body clearance.
C435 6 mm edge-only legal band identified as tolerance-sensitive.
C436 DML notch rejected.
C437 <=4 mm magnet class screened geometrically.
C438 4.4 mm pocket legal center band >=3 mm width.
C439 fabric bonding land interaction recognized.
C440 invalid Rev.B B-rep generation blocked before release.

## 15. State
Important correction:
**the proposed 6 mm magnets cannot robustly coexist with a pure 10 mm non-DML perimeter band using the previous station coordinates.**

The correct engineering action is to change retention packaging rather than hide the conflict in CAD.

Status:
**6MM_MAGNET_PERIMETER_CONFLICT_CONFIRMED / DML_UNCHANGED / SMALLER_OR_HYBRID_RETENTION_REQUIRED / C01_TO_C440**.
