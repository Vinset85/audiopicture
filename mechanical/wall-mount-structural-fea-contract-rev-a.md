# AudioPicture V2.2 Rev.A — wall-mount structural FEA contract

Status: **WALL_MOUNT_FEA_CONTRACT_FROZEN / PC_CF_COUPON_AND_EXACT_HARDWARE_CALIBRATION_OPEN**

## 1. Objective
Define the structural simulation required to release the rear PC-CF frame, mount nodes, cleats, inserts and anti-lift system.

Current product mass target:
- nominal first-order mass: 1.55 kg;
- nominal production target: <=1.70 kg.

Internal vertical design load:
- **70 N minimum**.

This is an engineering load case, not a certification rating for wall anchors or building substrates.

## 2. Model scope
Include:
- PC-CF structural perimeter;
- all mount-node ribs/gussets;
- insert/boss geometry;
- upper cleat interfaces;
- lower support interfaces;
- anti-lift local structure;
- rear-shell contacts where they materially transfer load;
- PCB/component lumped masses;
- DML/exciter distributed/lumped mass representation.

Do not model the DML/PORON path as a primary structural support.

## 3. Material model
PC-CF printed structure shall not be represented by a single injection-molded/isotropic strength value for final release.

Use an orthotropic or process-calibrated material model with axes tied to print orientation.

Prusament PC Blend Carbon Fiber published tensile-strength data may be used only as an initial XY reference. Production release requires coupon-derived:
- Ex, Ey, Ez or equivalent;
- tensile strength in principal print directions;
- interlayer/Z strength;
- shear response;
- strain at break;
- temperature dependence where relevant.

Apply conservative knock-down factors before coupon closure.

ASA cosmetic shell shall not be credited with primary gravity-load capacity unless explicitly modeled and validated.

## 4. Mass representation
Use 1.70 kg as the baseline FEA mass even though current nominal estimate is ~1.55 kg.

Mass distribution shall reflect:
- DML panel ~241 g;
- four exciters ~452 g total;
- electronics/harness;
- frame/shell/hardware.

When exact CAD mass properties become available, replace lumped estimates and rerun all cases.

## 5. Load cases

### LC1 — symmetric vertical design load
Total downward product load:
**70 N**

Distributed through actual mass/CG representation.

Both upper cleats engaged.
Lower supports constrain wall-normal rotation as physically appropriate.

Purpose:
- nominal high-margin gravity/load-path check.

### LC2 — single-upper-cleat fault
Apply the full:
**70 N**

through one upper cleat/mount node while the other upper cleat is assumed ineffective.

Lower supports may prevent gross rotation but shall not be credited as full vertical supports unless their geometry truly carries vertical load.

Run left and right variants.

Purpose:
- local boss/rib/insert robustness;
- avoid catastrophic product release after one engagement fault.

### LC3 — wall-normal pull
Initial engineering pull-away load:
**50 N total**

Applied at product CG/front-service load representation.

Purpose:
- cleat disengagement tendency;
- boss bending;
- rear-frame out-of-plane stiffness.

Exact value remains a design target until installation/use-case requirements are finalized.

### LC4 — corner push / torsion
Apply:
**30 N wall-normal service push**
at each front corner separately.

Purpose:
- torsional frame stiffness;
- lower-support reaction;
- buzz/rattle/contact opening;
- local DML/frame interaction risk.

### LC5 — installation seating
Apply short-duration equivalent:
**100 N vertical seating load**
through upper cleat interfaces.

This is a quasi-static equivalent for first-pass structural screening, not a drop simulation.

### LC6 — anti-lift
Apply:
**50 N upward**
to the product while upper cleats remain engaged.

The anti-lift mechanism shall prevent disengagement without relying on friction alone.

### LC7 — print warp / assembly preload
Impose realistic frame dimensional mismatch and rear-shell/cleat assembly tolerances.

Purpose:
- detect high residual stress before external loading;
- prevent assembly preload from consuming structural margin.

## 6. Contact model
Use nonlinear contact where needed:
- cleat engagement;
- lower wall pads;
- insert/boss interfaces if not bonded;
- rear-shell/frame contacts.

Friction shall not be the only mechanism preventing vertical or anti-lift failure.

Perform sensitivity sweeps on friction coefficient rather than choosing one favorable value.

## 7. Insert model
Initial model may use rigid/coupled insert representation for global frame screening.

Final local release requires:
- exact insert geometry;
- thread/knurl engagement zone;
- local PC-CF material;
- pull-out and torque qualification.

Heat-set inserts shall not be assumed to achieve parent-material strength.

## 8. Mesh
Global PC-CF frame:
- target element size <=4 mm.

Mount nodes, boss roots, fillets, cleat contact:
- <=1.0..1.5 mm;
- at least 3 elements through critical local wall/rib thickness where solid elements are used.

Use shell/solid strategy appropriate to actual printed geometry.

Convergence:
- peak displacement change <5%;
- strain-energy / reaction-force closure;
- hotspot stress/strain location stable under one mesh refinement.

Do not release from singular peak stress at an idealized sharp constraint; evaluate physically meaningful averaged/local strain and improve geometry.

## 9. Acceptance criteria
Before material coupon closure:
- no gross yielding/failure prediction under conservative material knock-down;
- no cleat disengagement;
- no insert pull-through;
- no buckling/local instability;
- no contact opening that permits product release.

After coupon calibration:
- minimum structural margin >=2.0 against calibrated allowable for LC1;
- minimum margin >=1.5 for LC2/LC3/LC4/LC6;
- LC5 installation event must not cause permanent damage;
- deformation must not force rear shell into exciter clearance columns;
- deformation must not preload DML/PORON enough to alter the acoustic boundary.

These are internal design criteria.

## 10. Displacement criteria
Initial service targets:
- upper mount-node relative displacement <=0.5 mm under LC1;
- product corner wall-normal displacement <=1.0 mm under LC4;
- no rear-skin intrusion into the 1 mm minimum exciter engineering clearance.

Exact stiffness criteria may tighten after buzz/rattle and DML coupling analysis.

## 11. Geometry optimization order
If margin is inadequate:
1. increase root fillet;
2. add/localize gussets along real load path;
3. widen local rib;
4. improve print orientation;
5. increase boss engagement volume;
6. change insert/cleat geometry;
7. only then consider global frame thickening.

Do not globally thicken the entire PC-CF frame as the first response.

## 12. Physical qualification gate
Even though the project targets direct final-version engineering, printed anisotropic structures cannot be production-released from generic datasheet properties alone.

Minimum material/process qualification:
- tensile coupons in relevant print directions;
- insert pull-out coupons;
- representative cleat-node coupon or subassembly;
- temperature-conditioned samples.

These tests characterize the manufacturing process; they do not require building a complete AudioPicture prototype.

## 13. Outputs
FEA release package shall include:
- displacement plots;
- principal strain/stress;
- reaction forces by cleat/support;
- contact pressure/slip;
- insert/boss loads;
- safety margins;
- deformed-shape collision check against exciters/PCBs;
- sensitivity to material knock-down and print orientation.

## 14. Release gates
1. exact cleat geometry;
2. exact insert/fastener selection;
3. shared CAD mass/CG;
4. PC-CF print orientation;
5. coupon material characterization;
6. nonlinear contact FEA all load cases;
7. local insert qualification;
8. buzz/rattle coupling check;
9. wall-substrate/anchor specification separately.

Status: **70N_SYMMETRIC_AND_SINGLE_CLEAT_CASES_FROZEN / 50N_PULL / 30N_CORNER / 100N_SEATING / 50N_ANTILIFT**.
