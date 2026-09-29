# AudioPicture V2.2 Rev.A — wall-mount hardware and structural-node specification

Status: **M4_PRODUCT_SIDE_INTERFACE_FROZEN / INSERT_AND_CLEAT_GEOMETRY_CANDIDATES_DEFINED / WALL_ANCHOR_SUBSTRATE_DEPENDENT**

## 1. Scope
Define real hardware interfaces for:
- PC-CF frame to product-side cleat;
- anti-lift;
- lower supports;
- wall-side rail/cleat fastening interface.

Wall anchors are intentionally not universal. Final anchor selection depends on wall substrate.

## 2. Product-side thread standard
Freeze:
**M4 x 0.7 metric thread**

Use M4 for the structural wall-mount nodes.

Rationale:
- sufficient mechanical scale for the 70 N internal design load;
- practical insert/boss geometry in the existing PC-CF perimeter;
- readily available stainless fasteners and threaded inserts;
- avoids unnecessarily large M5/M6 bosses in the 40 mm product.

Do not use self-tapping screws directly into PC-CF as the primary reusable structural mount.

## 3. Threaded insert baseline
Preferred insert class:
**heat-set threaded insert for thermoplastics, M4 x 0.7, approximately 6 mm class installed length**, exact supplier MPN to be selected after coupon testing.

Candidate manufacturer family:
- Ruthex / CNC Kitchen / equivalent brass heat-set insert family for M4 thermoplastic applications.

Because insert pull-out depends strongly on printed polymer, hole geometry, print orientation and installation temperature, no catalog pull-out value is accepted as the AudioPicture allowable.

Initial boss envelope:
- insert OD class approximately 5.5..6.5 mm depending selected part;
- radial PC-CF material >=2.5 mm beyond qualified installation-hole radius;
- initial external boss diameter target **>=11 mm**;
- local engagement depth target **>=7 mm** where Z geometry permits;
- root fillet **>=2 mm**;
- tie boss into at least two load-path ribs/gussets.

Exact dimensions shall follow the selected insert drawing and coupon results.

## 4. Product-side cleat
Use two short upper cleat segments.

Material candidate:
**6061-T6 aluminum, 2.0..2.5 mm nominal thickness**.

Do not use a full-width aluminum rail.

Each product-side cleat segment:
- two M4 fasteners into two independent PC-CF inserts preferred;
- slotted secondary hole allowed for tolerance;
- positive hook geometry carries vertical load;
- friction is not the primary vertical retention mechanism.

Initial cleat segment envelope target:
- length 45..55 mm;
- height 18..25 mm;
- thickness 2.0..2.5 mm;
- hook engagement 5..7 mm class.

Exact hook angle and mating geometry require CAD/contact FEA.

## 5. Fasteners
Product-side cleat fasteners:
**M4 x 0.7 stainless-steel socket/button-head machine screws**, length set from final cleat + washer + insert engagement.

Initial candidate:
- M4 x 10 mm or M4 x 12 mm A2 stainless.

Use washer under screw head if cleat slot/contact pressure requires it.

Do not bottom the screw in the insert.

Threadlocker policy:
- medium-strength removable threadlocker only after compatibility with polymer/insert process is verified;
- otherwise use mechanical locking strategy.

## 6. Upper-node redundancy
Preferred per upper cleat:
- 2 x M4 screws;
- 2 x inserts.

Therefore total upper product interface:
- 4 x M4 structural fasteners;
- 4 x M4 inserts.

LC2 single-cleat fault assumes one entire cleat assembly carries the 70 N design load.

Within that cleat, local analysis shall also check unequal load sharing between its two screws.

## 7. Anti-lift
Baseline:
- one hidden lower/underside **M4 captive screw** or positive latch;
- anti-lift design load 50 N upward;
- not part of normal gravity load path.

Preferred architecture:
- captive M4 screw enters a slotted/tab feature on the wall-side mount after the product is seated;
- accessible from underside with a normal hex/Torx tool;
- screw remains captive in product when loosened.

Avoid magnets as the sole anti-lift mechanism.

## 8. Lower supports
Two lower wall-contact pads:
- elastomer/foam pad;
- mechanically captured or high-reliability bonded;
- used for wall-normal support, tolerance and buzz/rattle control.

Initial pad:
- 10..15 mm footprint;
- 1..3 mm compliant thickness after installation.

Exact material/hardness to be selected from buzz/rattle and compression-set tests.

## 9. Wall-side cleat
Wall-side metal pieces:
- two matching short 6061-T6 cleat segments or one non-RF-conflicting segmented assembly;
- nominal 2.0..2.5 mm thickness;
- mounting holes sized for the selected substrate fastener system.

The product mechanical interface is fixed independently of wall-anchor type.

## 10. Wall anchors
Do not ship or specify one universal anchor as structurally equivalent across all substrates.

Installation classes:
A. reinforced concrete / solid masonry;
B. hollow brick/block;
C. plasterboard/drywall;
D. timber stud;
E. other substrate requiring installer assessment.

The installation manual shall provide compatible anchor classes and required load ratings for each supported substrate.

Where possible, timber-stud installation should use structural screws directly into the stud rather than hollow-wall anchors.

Wall anchors shall be selected with their own safety factor and manufacturer-approved substrate/load data.

The AudioPicture 70 N internal product FEA load is not automatically the required anchor rating.

## 11. RF constraints
Upper/right cleat and fasteners must remain outside the final ESP32 antenna keep-out.

All wall-mount metal must remain outside the BGT60TR13C 60 GHz RF cone.

If the current two-cleat location violates either final RF volume, move the cleat along the PC-CF perimeter; do not place RF-absorbing/shielding metal into the RF window merely to preserve cosmetic symmetry.

## 12. Corrosion and galvanic considerations
Indoor product baseline:
- aluminum cleats;
- stainless fasteners;
- brass inserts.

Avoid moisture traps.
Where aluminum/stainless contact creates fretting/corrosion concern, use suitable finish/coating/washer strategy.

No conductive treatment shall bridge PoE isolation or RF keep-out zones.

## 13. Assembly sequence
1. heat-set inserts installed into qualified PC-CF nodes using controlled temperature/depth fixture;
2. inspect insert flushness/axis;
3. attach product-side cleats with M4 machine screws;
4. torque to process-controlled value established by coupon testing;
5. install lower pads and anti-lift hardware;
6. functional engagement gauge check;
7. final product seats onto wall-side cleats;
8. engage anti-lift.

Do not define final M4 torque from generic steel-thread tables; brass insert/polymer allowable governs.

## 14. Qualification coupons
Required before release:
- M4 insert pull-out in printed PC-CF, relevant orientations;
- insert torque-out;
- two-screw cleat-node bending/shear coupon;
- heat-aged/temperature-conditioned repeat;
- installation-process repeatability.

Use these results to calibrate the FEA insert/boss interface.

## 15. CAD parameters
Add to master CAD:
- MOUNT_THREAD = M4x0.7
- UPPER_CLEAT_COUNT = 2
- FASTENERS_PER_CLEAT = 2
- CLEAT_LENGTH_SEED = 50 mm
- CLEAT_HEIGHT_SEED = 22 mm
- CLEAT_THICKNESS_SEED = 2.5 mm
- HOOK_ENGAGEMENT_SEED = 6 mm
- BOSS_OD_SEED = 11 mm
- BOSS_ROOT_FILLET_MIN = 2 mm
- ANTILIFT_THREAD = M4x0.7

All are seeds until exact insert and cleat drawing release.

## 16. Release gates
1. select exact M4 insert MPN and manufacturer drawing;
2. print/process coupon qualification;
3. freeze cleat profile and exact alloy/finish;
4. exact screw length/head style;
5. torque qualification;
6. contact/nonlinear FEA;
7. RF keep-out collision check;
8. wall-substrate installation specification;
9. assembly gauge/tolerance plan.

Status: **M4_X0P7 / TWO_50MM_CLASS_6061_T6_CLEATS / TWO_M4_FASTENERS_PER_CLEAT / M4_ANTILIFT**.
