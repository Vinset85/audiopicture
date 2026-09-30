# AudioPicture V2.2 — local magnetic-node FEA preparation Rev.K

Status: **FEA_PREPROCESSING_CONTRACT_DEFINED / NO_SOLVER_RESULT_CLAIMED**

## 1. Basis
Rev.J real kernel passed:
- one solid;
- zero fragments;
- DML intersection zero;
- 8/8 rear-return overlaps positive;
- 8/8 return-tab overlaps positive.

This authorizes FEA preprocessing, not a strength conclusion.

## 2. Local submodel
For each station extract:
- front target/tab load application region;
- full local perimeter return;
- sufficient rear-ring length on both tangential sides.

Seed rear-ring cut length:
**40 mm each side of return center**, clipped at corners/keep-outs.

Boundary sensitivity shall compare 30 / 40 / 60 mm each side.

## 3. Loads
Structural seeds:
- LC-K1: 5 N normal pull at target interface;
- LC-K2: 2 N tangential shear;
- LC-K3: 10 N normal installation/service proof;
- LC-K4: 5 N normal + 2 N tangential combined;
- LC-K5: eccentric 5 N normal applied at worst target-edge lever arm.

These remain design loads, not magnetic predictions.

## 4. Boundary conditions
Do not fully fix the return root alone.

Apply constraints at remote rear-ring cut faces/nodes so the return-root compliance remains in the model.

Run boundary-length sensitivity to detect artificial stiffening.

## 5. Material
Release-level FEA requires orthotropic printed PC-CF data for the selected filament/process/orientation.

Required minimum:
- E1/E2/E3;
- G12/G13/G23;
- nu12/nu13/nu23;
- tensile/compressive strengths by direction;
- shear strengths;
- temperature-conditioned values at qualified hot condition.

Until those exist, isotropic catalogue data may be used only for solver/debug trend studies and must not generate release margins.

## 6. Mesh
Use second-order tetrahedral or equivalent solid elements.

Seed:
- global local-submodel size 1.2 mm;
- return/tab root 0.6 mm;
- fillet/capture regions 0.35..0.5 mm.

Convergence:
refine until target displacement and root peak stress away from mathematical singularities change <5%.

## 7. Outputs
Record:
- target normal displacement;
- target tangential displacement;
- change in G_EFF;
- maximum principal strain;
- directional stress/strain appropriate to orthotropic material;
- rear-ring reaction;
- DML minimum deformed clearance.

## 8. Acceptance philosophy
No numerical stress allowable is frozen without qualified material/process data.

Geometric functional criterion:
under service/design loads, deformation shall not close DML clearance or cause target/holder release.

Magnetic functional criterion:
FEA displacement contribution must be included in G_EFF tolerance budget.

## 9. Station priority
First solve:
1. M1D because of ESP32/RF sensitivity;
2. M7D/M8D because radar mask remains open;
3. one representative bottom station;
4. remaining stations after topology/tolerance updates.

Structural similarity does not override RF/geometry differences.

## 10. Automatic checks
C687 Rev.J PASS required before FEA prep.
C688 local submodel includes tab-return-ring path.
C689 rear ring extends beyond return in local model.
C690 30/40/60 mm boundary sensitivity defined.
C691 5 N normal case defined.
C692 2 N tangential case defined.
C693 10 N proof case defined.
C694 combined normal/shear case defined.
C695 eccentric target-edge case defined.
C696 return root not directly fully fixed.
C697 orthotropic printed PC-CF data required for release.
C698 catalogue isotropic data limited to debug/trend studies.
C699 second-order solid mesh preferred.
C700 root mesh refinement defined.
C701 <5% convergence criterion defined.
C702 target displacement reported.
C703 G_EFF displacement contribution reported.
C704 DML deformed clearance reported.
C705 no release stress margin without qualified material data.
C706 M1D first station priority.
C707 radar-side nodes separately checked.
C708 no FEA result claimed by this document.

## 11. State
Rev.J has cleared the geometry gate.

Next engineering activity is local structural FEA, but release-quality results require measured/qualified anisotropic PC-CF properties.

Status:
**LOCAL_FEA_CONTRACT_READY / LOADS_AND_MESH_DEFINED / MATERIAL_DATA_GATE_OPEN / C01_TO_C708**.
