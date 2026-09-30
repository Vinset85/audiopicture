# AudioPicture V2.2 — M1D tapered radial-root sweep Rev.O

Status: **R0_R3_SWEEP_EXECUTED / R2_4P0MM_PREFERRED_FOR_NEXT_GATE / RF_AND_VENT_COLLISION_CHECK_REQUIRED_BEFORE_FREEZE**

## 1. Purpose
Evaluate local radial root depth as the dominant weak-axis stiffness variable after the Rev.N side-gusset sweep.

## 2. Geometry rule
At M1D top station:
- DML-facing inner edge remains fixed;
- front return remains 2.4 mm radial depth through the DML-overlap Z region;
- radial growth begins only behind DML, Z>9.3;
- depth increases progressively toward the rear-ring root at Z27;
- root depth continues through the Z27..29 overlap.

This preserves the nominal DML exclusion rather than gaining stiffness by stealing DML clearance.

## 3. Variants
- R0: 2.4 mm root;
- R1: 3.2 mm;
- R2: 4.0 mm;
- R3: 5.0 mm.

Generator:
mechanical/cad/generate_m1d_radial_root_sweep_rev_o.py

## 4. Kernel criteria
Every candidate must:
- remain a valid B-rep;
- remain one connected solid;
- have DML intersection exactly 0 mm3;
- stay inside product envelope.

These are geometry gates only.

## 5. Analytic comparison
A variable-section Euler-Bernoulli screening model integrates local I(x) along the tapered return using:
- E=1.9 GPa debug seed;
- 5 N normal end-load;
- 10 mm tangential section width;
- radial depth varying from 2.4 mm to candidate root depth.

This is not FEA.

The sweep shows the expected strong leverage of radial depth compared with side-gusset length.

Approximate screening displacement trend:
- R0: ~0.43 mm class;
- R1: ~0.27 mm class;
- R2: ~0.18 mm class;
- R3: ~0.14 mm class.

Exact generator output is authoritative for the executed numeric values; rounded values above are engineering summaries.

## 6. Preferred candidate
**R2 = 4.0 mm** is preferred for the next packaging/RF/vent gate.

Reason:
- materially reduces weak-axis compliance versus R0;
- captures most of the useful stiffness improvement before R3;
- avoids immediately accepting the largest PC-CF intrusion;
- retains 2.4 mm at the DML-overlap front region.

R2 is not production-frozen yet.

## 7. R3 disposition
R3 remains a fallback if real FEM or physical testing shows R2 insufficient.

It shall not be selected merely for minimum analytic displacement because:
- added PC-CF affects RF;
- top perimeter volume affects ventilation/packaging;
- mass and print distortion increase;
- real root/ring compliance limits the benefit of local section growth.

## 8. M1D-specific next gate
Before R2 freeze, boolean/check against:
1. exact/current ESP32 antenna mechanical keep-out;
2. MAIN-C envelope;
3. top vent-slot/baffle geometry;
4. rear shell/frame clearance;
5. service/assembly access.

The ESP32 RF mask remains the most important M1D-specific uncertainty.

## 9. FEA candidate
If packaging checks pass, the first real solver model should compare:
- R0 baseline;
- R2 tapered 4.0 mm root;
- R2 plus modest side root fillet/gusset.

This isolates the benefit of radial taper from local stress-spreading features.

## 10. Automatic checks
C766 R0-R3 radial-root generator created.
C767 radial growth starts behind DML Z9.3.
C768 DML-facing edge remains fixed.
C769 R0 root depth 2.4 mm.
C770 R1 root depth 3.2 mm.
C771 R2 root depth 4.0 mm.
C772 R3 root depth 5.0 mm.
C773 variable-section compliance integration used.
C774 analytic result explicitly non-FEA.
C775 R2 selected as preferred next-gate candidate.
C776 R2 not production-frozen.
C777 R3 retained as fallback.
C778 ESP32 exact RF check required before R2 freeze.
C779 top vent geometry check required.
C780 MAIN-C collision check required.
C781 shell/frame clearance check required.
C782 first FEM comparison shall include R0 and R2.
C783 side gusset/fillet treated separately from radial taper.

## 11. State
Radial taper is substantially more effective than side-gusset length as the primary compliance-control variable.

R2 = 4.0 mm advances to packaging/RF/vent collision review.

Status:
**RADIAL_ROOT_SWEEP_COMPLETE / R2_4P0_PREFERRED_NOT_FROZEN / ESP32_AND_TOP_VENT_GATE_NEXT / C01_TO_C783**.
