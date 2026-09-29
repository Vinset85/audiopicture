# AudioPicture V2.2 Rev.B — parametric structural FEA model

Status: **FRAME_FEA_PARAMETERIZATION_FROZEN / PC_CF_COUPON_PROPERTIES_AND_SOLVER_RUN_OPEN**

## 1. Purpose
Turn the Rev.B keep-out-driven rear frame into a solver-ready structural model.

This contract freezes:
- geometry parameter classes;
- interfaces;
- contacts;
- load cases;
- mesh strategy;
- output metrics;
- optimization variables.

It does not invent final through-thickness PC-CF properties.

## 2. Model scope
Include:
- PC-CF outer structural ring;
- upper left/right mount islands;
- M4 insert/boss regions;
- dual side load rails;
- local bridges/gussets;
- MAIN-C/P carrier islands where structurally relevant;
- lower service opening reinforcement;
- lower wall supports;
- anti-lift node;
- exciter-column holes/keep-outs;
- rear-shell contact only where it actually transfers load.

Exclude from primary structural stiffness unless explicitly coupled:
- DML compliant PORON;
- cosmetic fabric;
- non-structural cable clips;
- PCB stiffness as a load-bearing bridge.

## 3. Baseline geometric parameters
Global:
- PRODUCT_X = 320 mm
- PRODUCT_Y = 400 mm
- PRODUCT_Z_MAX = 40 mm

Frame:
- OUTER_RING_WIDTH = 10 mm nominal
- OUTER_RING_WIDTH_RANGE = 8..16 mm local
- FRAME_WALL = 2.4 mm
- PRIMARY_RIB = 2.8 mm
- PRIMARY_RIB_SWEEP = 2.4 / 2.8 / 3.2 mm
- MOUNT_RIB = 3.2 mm seed
- MOUNT_RIB_SWEEP = 3.0 / 3.2 / 3.6 mm
- GENERAL_FILLET = 1.5 mm minimum
- MOUNT_FILLET = 2.0 mm minimum
- MOUNT_FILLET_SWEEP = 2 / 3 / 4 mm

Boss:
- M4 x 0.7
- BOSS_OD = 11 mm seed
- BOSS_OD_SWEEP = 11 / 12 / 13 mm
- INSERT_ENGAGEMENT = >=7 mm where Z permits.

## 4. Mount topology
Two upper cleat nodes.

Each node:
- two M4 fasteners;
- two brass heat-set inserts;
- at least two independent rib/gusset paths into outer ring.

Do not merge left/right cleat boundary conditions into one rigid line.

They are separate interfaces so the single-cleat fault case can be solved.

## 5. Lower supports
Two lower wall-contact pads.

Model as wall-normal contact/support with tangential behavior appropriate to compliant pad.

Do not make lower pads carry the nominal vertical product weight unless actual friction is intentionally credited.

Baseline vertical load path remains upper cleats.

## 6. Anti-lift
Model the anti-lift M4 feature as a separate reinforced lower node.

LC6 applies 50 N upward to this interface.

No load transfer through ASA-only geometry is credited.

## 7. PC-CF material model
Use an orthotropic material model aligned with print/toolpath coordinates.

Required final properties:
- Ex
- Ey
- Ez
- Gxy
- Gxz
- Gyz
- nu_xy
- nu_xz
- nu_yz
- tensile/compressive strengths by principal direction;
- shear strengths;
- strain-to-failure;
- temperature dependence.

Manufacturer bulk/XY values are not sufficient to release the part.

## 8. Seed material sensitivity
Until coupons exist, use normalized sensitivity cases rather than pretending exact Z properties are known.

Define XY modulus reference:
**E_XY_REF = manufacturer/process seed**

Then solve:
- MAT-A: Ez = 0.20 x E_XY_REF
- MAT-B: Ez = 0.35 x E_XY_REF
- MAT-C: Ez = 0.50 x E_XY_REF

For out-of-plane shear, run:
- Gxz/Gxy = 0.25 / 0.40 / 0.60
- Gyz/Gxy = 0.25 / 0.40 / 0.60

Strength sensitivity:
- Z/interlayer allowable = 0.20 / 0.35 / 0.50 x qualified XY allowable.

These are numerical robustness cases only, not material claims.

## 9. Temperature cases
Solve structural properties at:
- 23 C reference;
- 50 C internal warm case;
- 70 C local adverse case.

Exact modulus/strength derating shall come from coupon/manufacturer evidence.

Do not extrapolate linearly to glass-transition region.

## 10. Insert representation
First model:
- brass insert as bonded/contact rigid or elastic inclusion;
- surrounding PC-CF boss explicitly meshed.

Then sensitivity:
A. perfectly bonded insert;
B. reduced interface stiffness;
C. local equivalent pull-out/contact model after coupon data.

Production release requires insert pull-out/torque coupon results.

## 11. Wall-cleat boundary
Model cleat fastener interfaces separately from wall substrate.

Product-frame FEA answers whether the product-side structure survives.

Wall-anchor qualification is a separate substrate-dependent problem.

For product-side model:
- constrain cleat attachment surfaces/nodes according to realistic screw/cleat contact;
- avoid fully fixing an unrealistically large frame face.

## 12. Load application
Use distributed inertial/body loading where practical rather than a single point force.

Current mass:
- nominal ~1.55 kg;
- production target <=1.70 kg.

Structural design load baseline:
**70 N vertical**

Apply mass distribution from DMU once exact CAD mass properties exist.

Until then distribute 70 N according to subsystem mass regions, with sensitivity to CG.

## 13. Load cases

### LC1 symmetric vertical
- 70 N equivalent downward product load;
- both upper cleats active.

Acceptance:
- margin >=2.0 after qualified material allowables;
- upper mount-node displacement <=0.5 mm.

### LC2 single-cleat fault
- full 70 N;
- left-only and right-only variants.

Acceptance:
- margin >=1.5;
- no disengagement, boss pull-through or unstable rotation.

### LC3 wall-normal pull
- 50 N distributed outward.

Acceptance:
- margin >=1.5;
- no mount disengagement.

### LC4 corner/torsion
- 30 N wall-normal at worst product corner.

Acceptance:
- margin >=1.5;
- corner wall-normal displacement <=1.0 mm.

### LC5 installation seating
- 100 N quasi-static seating load.

Check local cleat/boss/gusset stress and permanent deformation risk.

### LC6 anti-lift
- 50 N upward.

Acceptance:
- margin >=1.5;
- anti-lift remains engaged.

### LC7 print warp/preload
Apply assembly misfit/preload sensitivity.

Initial imposed displacement sweep:
- 0.25 mm
- 0.50 mm
- 1.00 mm

Locations:
- diagonal corner warp;
- local mount-node offset;
- rear-shell/frame assembly mismatch.

## 14. CG sensitivity
Before exact CAD CG:
solve at least:
- centered nominal;
- CG +20 mm X;
- CG -20 mm X;
- CG +15 mm Y;
- CG -15 mm Y.

This tests asymmetric component/print changes.

Exact DMU CG supersedes these seeds.

## 15. Mesh
Element type:
- solid or shell/solid hybrid appropriate to ribs/bosses;
- insert contact regions require 3D solids.

Mesh:
- global <=4 mm;
- ribs/fillets <=2 mm;
- bosses/inserts/cleat contacts <=1.0..1.5 mm;
- service-opening corners <=1.5 mm.

Convergence:
- refine critical regions until peak non-singular stress and displacement change <5 percent;
- ignore mathematical contact/constraint singularities only after hotspot classification.

## 16. Hotspot classification
For every high stress location classify:
A. physical distributed hotspot;
B. geometric notch;
C. contact-edge artifact;
D. constraint singularity;
E. mesh artifact.

Only A/B drive structural redesign directly.

C/D/E require model correction/engineering interpretation.

## 17. Buckling
Run eigenvalue buckling as a screening analysis for:
- long side rails;
- thin service-opening bridge;
- local mount ribs.

Any low buckling factor requires nonlinear follow-up with imperfections.

Do not use eigenvalue buckling alone as production proof.

## 18. Nonlinear cases
Run geometric/contact nonlinear solve for:
- LC2 single-cleat fault;
- LC4 torsion;
- LC5 seating;
- LC6 anti-lift;
- any case with contact opening/sliding.

Material nonlinearity may be added after coupon curves exist.

## 19. Optimization variables
Priority order:
1. fillet radius;
2. gusset length/angle;
3. rib depth;
4. bridge path;
5. boss OD;
6. local wall thickness;
7. print orientation;
8. global ring width last.

Optimization objectives:
- satisfy margins/displacement;
- frame mass <=250 g;
- preserve all C01..C80 DMU keep-outs;
- preserve airflow/RF/service corridors.

## 20. Print-orientation study
At least three manufacturing orientations:
A. rear face parallel to build plate;
B. long edge on build plate;
C. segmented/subframe orientation if one-piece anisotropy is poor.

Map local principal structural stresses against weak interlayer direction.

Preferred orientation minimizes peel/opening stress at upper mount bosses.

## 21. Required outputs
Per load/material/temperature case:
- max displacement;
- mount-node displacement;
- corner displacement;
- principal stresses/strains;
- orthotropic failure index;
- insert/boss interface loads;
- cleat screw reactions;
- lower-pad reactions;
- anti-lift reaction;
- buckling factor;
- mass;
- strain-energy map.

Export hotspot coordinates back into master CAD.

## 22. Coupon program
No full product prototype is required for material calibration.

Minimum coupon/subassembly set:
- XY tensile;
- Z/interlayer tensile or equivalent;
- shear;
- flexural coupon relevant to printed rib;
- M4 heat-set insert pull-out;
- M4 insert torque-to-failure;
- local boss/gusset subassembly.

Print coupons with same:
- material lot/family;
- nozzle;
- layer height;
- chamber/bed conditions;
- drying;
- raster/toolpath policy;
- post-processing.

## 23. Digital-to-physical correlation
Production release can use coupon/subassembly correlation rather than a complete product prototype.

Required:
- coupon material calibration;
- mount-node subassembly load test;
- compare stiffness/failure mode to FEA;
- update material/contact model;
- rerun LC1..LC7.

## 24. DMU/FEA checks
Add:
C81 orthotropic axes match print orientation.
C82 material case sensitivity recorded.
C83 mount insert contacts explicitly modeled.
C84 left/right cleats are independent boundaries.
C85 LC2 left and right both solved.
C86 CG sensitivity solved.
C87 temperature sensitivity solved.
C88 mesh convergence achieved.
C89 hotspot type classified.
C90 buckling screen completed.
C91 nonlinear contact cases completed.
C92 frame mass <=250 g.
C93 no FEA optimization violates RF keep-out.
C94 no FEA optimization violates airflow.
C95 no FEA optimization violates exciter clearance.
C96 coupon-calibrated model rerun before release.

## 25. Release sequence
1. generate shared frame CAD;
2. assign print orientation;
3. mesh baseline;
4. run MAT-A/B/C sensitivities;
5. run LC1..LC7;
6. optimize topology locally;
7. print/test coupons and mount-node subassembly;
8. calibrate orthotropic/contact model;
9. rerun final cases;
10. freeze structural Rev.C geometry.

Status: **LC1_TO_LC7_SOLVER_CONTRACT_READY / ORTHOTROPIC_SENSITIVITY_20_35_50_PERCENT_Z / COUPON_CALIBRATION_REQUIRED**.
