# AudioPicture V2.2 — M1D gusset sweep Rev.N

Status: **G0_G3_GEOMETRY_SWEEP_EXECUTED / SIDE_GUSSET_ONLY_STRATEGY_INSUFFICIENT / RADIAL_ROOT_DEPTH_NEXT**

## 1. Purpose
Evaluate G0/G1/G2/G3 before committing a variant to FEM.

The comparison uses:
- real CadQuery/OpenCASCADE geometry for connectivity/collision/volume;
- an analytic stepped-beam stiffness screen only for relative trend.

No FEA result is claimed.

## 2. Variants
G0:
- no side gusset.

G1:
- 8 mm side-root reinforcement length.

G2:
- 12 mm.

G3:
- 16 mm.

All retain the 2.4 mm nominal return wall and local side reinforcement only.

## 3. Kernel result
All generated variants:
- are valid B-reps;
- remain one connected solid;
- preserve zero nominal DML intersection.

Therefore the side-gusset concept is geometrically feasible at M1D in the current nominal hard-volume model.

## 4. Stiffness-screen result
The analytic stepped-beam screen shows only a modest improvement as side-gusset length increases.

The reason is structural:
the wall-normal bending stiffness is dominated by the return's **radial thickness cubed**.

Adding narrow tangential side strips increases effective section width, but it does not materially increase the weak-axis section depth.

Therefore simply extending G1 -> G2 -> G3 has diminishing value.

## 5. Decision
Do not freeze G3 merely because it is the longest variant.

The G0-G3 side-gusset-only family is **not selected** as the final stiffness solution.

Retain side gussets for root stress spreading, but open a new primary variable:
**local radial root depth**.

## 6. Next sweep
Keep nominal front/perimeter wall:
- 2.4 mm radial thickness where DML clearance is governing.

Increase radial depth only rearward of the DML Z region and toward the rear-ring root.

Candidate root-depth values:
- R0 = 2.4 mm;
- R1 = 3.2 mm;
- R2 = 4.0 mm;
- R3 = 5.0 mm.

Use a tapered transition rather than an abrupt step.

Constraints:
- no growth into DML hard volume at Z<=9.3;
- no growth toward ESP32 antenna without exact RF clearance;
- preserve shell/frame fit;
- preserve top vent path;
- maintain segmented-node topology.

## 7. Why radial depth is high leverage
For rectangular weak-axis bending:
I = b*h^3/12.

With constant width b, increasing h from:
- 2.4 to 3.2 mm gives theoretical local I ratio ~2.37;
- 2.4 to 4.0 mm gives ~4.63;
- 2.4 to 5.0 mm gives ~9.04.

These are local section-property ratios only, not whole-node displacement reductions.

They show why radial depth is a more efficient design variable than side-gusset length alone.

## 8. FEA implication
A real FEM solve should compare:
- plain baseline;
- selected tapered radial-depth root;
- radial-depth root plus modest side gussets.

Do not spend solver effort on G1/G2/G3 as if their length alone solved the compliance issue.

## 9. Automatic checks
C747 G0/G1/G2/G3 generator created.
C748 all variants use real OpenCASCADE geometry.
C749 all variants require one-solid connectivity.
C750 all variants require DML intersection zero.
C751 analytic comparison labeled non-FEA.
C752 side-gusset length alone gives limited stiffness leverage.
C753 G3 not frozen solely by maximum length.
C754 weak-axis stiffness recognized as radial-depth dominated.
C755 local radial-depth sweep opened.
C756 R0 2.4 mm defined.
C757 R1 3.2 mm defined.
C758 R2 4.0 mm defined.
C759 R3 5.0 mm defined.
C760 tapered root transition required.
C761 no radial growth into DML Z region.
C762 ESP32 RF constraint remains authoritative.
C763 top ventilation remains a geometry gate.
C764 side gussets retained only as complementary root treatment.
C765 FEM candidates shall include radial-depth variant.

## 10. State
The G0-G3 exercise prevented a low-value optimization: longer side gussets do not address the dominant weak-axis compliance efficiently.

The next geometry gate targets the correct stiffness variable: local radial root depth.

Status:
**SIDE_GUSSET_SWEEP_COMPLETE / G3_NOT_FROZEN / RADIAL_DEPTH_2P4_3P2_4P0_5P0_NEXT / C01_TO_C765**.
