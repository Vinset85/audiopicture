# AudioPicture V2.2 Rev.A — LC1 / LC2 solver-deck contract

Status: **REAL_BREP_READY / FEM_SOLVER_NOT_AVAILABLE_IN_CURRENT_RUNTIME / LC1_LC2_DECK_CONTRACT_READY / NO_FABRICATED_STRESS_RESULTS**

## 1. Geometry source
Authoritative structural geometry:
- AP22_FRAME_REV_B_DMU.step
- OpenCASCADE-generated
- one valid connected primary B-rep
- volume 86.990 cm3
- structural bounding box 312 x 392 x 8 mm
- mass sensitivity 100.04..108.74 g for density 1.15..1.25 g/cm3.

FEA geometry must be derived from this B-rep, not rebuilt independently.

## 2. Solver availability gate
The current execution environment does not provide a validated structural FEM solver such as CalculiX, Code_Aster, Elmer or FEniCS.

Therefore:
- no stress result is reported;
- no displacement result is reported;
- no margin is claimed;
- LC1/LC2 remain unsolved.

This file freezes the reproducible first-run deck.

## 3. Element strategy
Preferred:
- quadratic tetrahedral solids for irregular printed-frame topology;
- linear tetrahedra only for preliminary mesh diagnostics.

Production structural result:
- second-order solid elements required unless a convergence study demonstrates an equivalent alternative.

Boss/insert/contact regions remain 3D solids.

## 4. Mesh controls
Global target:
- 4.0 mm maximum characteristic size.

Local:
- M4 bosses/bores: 1.0..1.5 mm
- boss root fillets: 1.0..1.5 mm
- cleat islands: <=1.5 mm
- rail/bridge junctions: <=2.0 mm
- service-opening corners: <=1.5 mm
- anti-lift: <=1.5 mm.

Require >=3 elements across critical structural depth where practical.

## 5. Mesh convergence
Run at least:
M0 coarse diagnostic
M1 nominal
M2 refined critical regions.

Acceptance:
- upper-node displacement change M1->M2 <5 percent;
- critical non-singular stress/failure-index change <5 percent where mesh behavior is convergent;
- reaction-force closure within solver numerical tolerance.

If a peak diverges with refinement, classify singularity before using it for design.

## 6. Material coordinate systems
Printed PC-CF is orthotropic.

Define local material axes from manufacturing orientation:
- 1 = dominant in-layer structural/toolpath direction;
- 2 = transverse in-layer direction;
- 3 = layer-build/interlayer direction.

Never default to isotropic PC-CF for release.

## 7. Material sensitivity cases
Before coupon calibration:
MAT-A:
- E3/E12 reference = 0.20

MAT-B:
- E3/E12 reference = 0.35

MAT-C:
- E3/E12 reference = 0.50.

Out-of-plane shear sensitivity:
- G13/G12 = 0.25 / 0.40 / 0.60
- G23/G12 = 0.25 / 0.40 / 0.60.

Strength sensitivity:
- interlayer allowable = 0.20 / 0.35 / 0.50 of qualified in-plane allowable.

These are robustness ratios, not claims about a commercial filament.

## 8. Density
For inertia/mass sensitivity only:
- 1150
- 1200
- 1250 kg/m3.

Replace with qualified printed-part density before release.

## 9. Insert model
First numerical pass:
- explicit cylindrical insert volume where geometry exists;
- bonded elastic interface sensitivity.

Second pass:
- reduced interface stiffness.

Release:
- calibrated from M4 heat-set insert pull-out/torque subassembly.

## 10. Cleat boundary representation
Do not fully fix a broad rear face.

Use the four M4 semantic interfaces:
- UL1
- UL2
- UR1
- UR2.

Represent realistic screw/cleat support through bore/seat coupling or distributed coupling nodes.

Left/right cleats remain independent.

## 11. Product load distribution
LC1/LC2 design load:
**70 N downward equivalent product load**.

Preferred application:
- body/inertial loading using subsystem mass distribution.

If subsystem solids are absent from frame-only model:
- distribute equivalent forces across LOAD_* interfaces according to current mass budget;
- reaction total must equal 70 N.

Do not apply 70 N to a single arbitrary node.

## 12. LC1
Name:
**LC1_VERTICAL_BOTH_CLEATS**

Load:
- 70 N total downward.

Supports:
- left cleat active;
- right cleat active;
- lower pads wall-normal only if installed-condition contact is represented;
- no vertical friction credit at lower pads baseline.

Outputs:
- max displacement;
- left/right cleat displacement;
- M4 reactions;
- rail strain energy;
- orthotropic failure index;
- boss/root hotspot classification.

Release targets after calibration:
- margin >=2.0;
- upper mount displacement <=0.5 mm.

## 13. LC2-L
Name:
**LC2_VERTICAL_LEFT_ONLY**

Load:
- full 70 N downward.

Support:
- left cleat only for primary vertical restraint;
- right cleat released according to fault scenario;
- lower pads may provide wall-normal stabilization only.

Required:
- nonlinear geometric/contact solve if large rotation/contact opening develops.

Release target:
- calibrated margin >=1.5;
- no boss pull-through;
- no unstable rotation/disengagement.

## 14. LC2-R
Name:
**LC2_VERTICAL_RIGHT_ONLY**

Mirror intent of LC2-L, but do not assume identical result because frame keep-outs are asymmetric.

Load:
- full 70 N downward.

Support:
- right cleat only.

Release target:
- calibrated margin >=1.5.

## 15. First-run matrix
Minimum preliminary runs:
1. LC1 MAT-A orientation A
2. LC1 MAT-B orientation A
3. LC1 MAT-C orientation A
4. LC2-L MAT-A orientation A
5. LC2-R MAT-A orientation A.

Then expand:
- orientations B/C;
- temperature cases;
- shear sensitivity;
- insert-interface sensitivity.

MAT-A single-cleat cases are prioritized because they are likely to expose weak interlayer load paths earliest.

## 16. Mandatory result table
For every run:
- geometry commit/revision;
- mesh revision;
- element type/count;
- material case;
- print orientation;
- temperature;
- applied load;
- reaction closure;
- max U;
- U at each cleat;
- boss reactions;
- failure index;
- hotspot coordinates;
- hotspot class;
- convergence state.

## 17. Stop conditions
Stop and redesign before broader sweep if:
- model becomes disconnected;
- reaction closure fails;
- rigid-body mode exists unexpectedly;
- LC1 displacement grossly exceeds 0.5 mm;
- LC2 loses stable support;
- boss/rail load path shows obvious interlayer peel concentration;
- contact setup produces nonphysical restraint.

## 18. Automatic checks
C191 FEA mesh derives from released G2 B-rep.
C192 second-order solid mesh used for release.
C193 boss local mesh <=1.5 mm.
C194 cleat interfaces are independent.
C195 lower-pad vertical friction not credited baseline.
C196 total LC1 load equals 70 N.
C197 LC2-L full 70 N applied.
C198 LC2-R full 70 N applied.
C199 reaction closure verified.
C200 mesh convergence verified.
C201 orthotropic material axes recorded.
C202 MAT-A/B/C ratio cases recorded.
C203 no isotropic production release.
C204 insert interface sensitivity run.
C205 LC2 left/right not assumed symmetric.
C206 rigid-body mode check passes.
C207 nonlinear solve used when contact/rotation requires.
C208 hotspot classification recorded.
C209 no stress/margin reported without a real solver result.
C210 calibrated coupon data required before production structural release.

## 19. Current state
Geometry gate: PASS.
Connectivity gate: PASS.
Mass gate: PASS.
Mesh/deck definition: READY.
Numerical FEM execution: BLOCKED by current runtime solver availability.
Structural release: OPEN.

Status: **LC1_LC2_REPRODUCIBLE_DECK_READY / C01_TO_C210 / REAL_SOLVER_REQUIRED_FOR_NUMERICAL_RESULTS**.
