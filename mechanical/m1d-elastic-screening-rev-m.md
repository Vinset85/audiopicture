# AudioPicture V2.2 — M1D executed kernel and elastic screening Rev.M

Status: **M1D_KERNEL_PASS / FEM_SOLVER_UNAVAILABLE_IN_CURRENT_RUNTIME / ANALYTIC_SCREENING_ONLY / ROOT_GUSSET_REQUIRED_BEFORE_FEA**

## 1. Executed M1D kernel
The Rev.K M1D submodel was executed with CadQuery/OpenCASCADE.

Measured:
- B-rep valid: PASS;
- solid count: 1;
- rear-return overlap: 48.0 mm3;
- return-tab overlap: 64.0 mm3;
- DML intersection: 0 mm3;
- bounding box: 80 x 10 x 29.9 mm;
- rear-ring half-span: 40 mm.

Therefore the local nominal geometry preserves the Rev.J connectivity result.

## 2. Solver availability gate
The current execution runtime was checked for:
- CalculiX/ccx;
- Gmsh;
- SfePy;
- FEniCS/dolfinx;
- scikit-fem;
- meshio.

None is installed.

Therefore no finite-element result is claimed in this revision.

## 3. Analytic screening model
A deliberately simple Euler-Bernoulli cantilever screen was run only to estimate deformation order of magnitude.

Assumptions:
- return blade treated as a free cantilever;
- effective free length L = 17.8 mm, from front structural overlap to rear-ring onset;
- rectangular section 10 x 2.4 mm;
- isotropic debug modulus E = 1.9 GPa;
- no root fillet/gusset stiffness;
- no rear-ring rotational compliance model;
- small-deflection linear elasticity.

This is not FEA and is not a release calculation.

## 4. Screening results
Wall-normal weak-axis bending:
- 5 N: tip displacement ~0.429 mm; nominal root bending stress ~9.27 MPa;
- 10 N: tip displacement ~0.859 mm; nominal root bending stress ~18.54 MPa.

Tangential strong-axis bending:
- 2 N: tip displacement ~0.0099 mm; nominal root bending stress ~0.89 MPa.

The stress numbers are geometric screening outputs only and shall not be compared directly with a universal 63 MPa allowable.

## 5. Engineering consequence
The weak-axis displacement is large enough relative to the magnetic G_EFF budget that the plain rectangular return should not be promoted unchanged to detailed FEA.

The already-required root treatment now becomes a pre-FEA geometry gate.

Preferred next geometry:
- retain 2.4 mm wall blade where packaging requires;
- add two local triangular/tapered PC-CF gussets at the rear-ring transition;
- use root fillet >=1.5 mm;
- extend gusset forward only where it remains outside DML/RF/service keep-outs;
- do not thicken globally toward ESP32.

The goal is to reduce root rotation and normal target displacement without creating a second continuous front ring.

## 6. G_EFF implication
The ~0.43 mm 5 N cantilever result is of the same order as the magnetic coupon G_EFF sweep increments.

It must therefore be treated as a warning that structural compliance can materially affect magnetic retention.

It is not a prediction of assembled displacement because the real gusset/ring stiffness is absent from the analytic model.

## 7. Next geometry sweep
Generate M1D gusset variants:
- G0: no gusset, current baseline;
- G1: 8 mm axial/taper length;
- G2: 12 mm axial/taper length;
- G3: 16 mm axial/taper length.

All:
- two tangential side gussets;
- 2.4 mm seed thickness;
- >=1.5 mm root fillet target;
- DML intersection zero;
- RF mask remains open/authoritative.

Use section-property/analytic comparison first, then solve selected variants in a real FEM solver when available.

## 8. Automatic checks
C728 M1D kernel executed.
C729 M1D B-rep valid.
C730 M1D solid count ==1.
C731 rear-return overlap ==48 mm3.
C732 return-tab overlap ==64 mm3.
C733 DML intersection ==0 mm3.
C734 no FEM solver available in current runtime.
C735 no FEA result claimed.
C736 Euler-Bernoulli model explicitly labeled screening only.
C737 screening E ==1.9 GPa debug seed.
C738 weak-axis 5 N displacement approximately 0.429 mm.
C739 weak-axis 10 N displacement approximately 0.859 mm.
C740 tangential 2 N displacement approximately 0.0099 mm.
C741 screening stresses not treated as release margins.
C742 plain blade not promoted unchanged to FEA.
C743 root gusset becomes pre-FEA gate.
C744 G0/G1/G2/G3 gusset sweep defined.
C745 no global thickening toward ESP32 permitted.
C746 DML zero-intersection retained for gusset sweep.

## 9. State
The local M1D geometry is kernel-valid, but a plain 10 x 2.4 mm perimeter return is too compliant in the simple weak-axis screen to justify freezing it before root optimization.

Status:
**M1D_KERNEL_PASS / NO_FEM_SOLVER / ANALYTIC_WARNING_0P43MM_AT_5N / GUSSET_SWEEP_NEXT / C01_TO_C746**.
