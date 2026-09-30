# AudioPicture V2.2 — executed upper outlet layout Rev.T

Status: **REV_R_EXECUTED_PASS / NOMINAL_COORDINATES_FROZEN_FOR_DMU / TOLERANCE_AND_CFD_RELEASE_OPEN**

## 1. Runtime
The committed Rev.R search was executed in a real local CAD runtime:
- CadQuery 2.8.0;
- OpenCASCADE backend available.

All embedded assertions passed.

## 2. Executed result
Candidate counts:
- left legal candidates: 1879;
- right legal candidates: 2572;
- reduced search sets: 257 left / 345 right.

Selected slot count: **10**.

Opening:
- each slot 3 x 45 mm;
- gross area = **1350 mm2**;
- Rev.B effective-area seed at factor 0.80 = **1080 mm2**.

Minimum pairwise solid web = **3.0 mm**.

All reported 3D intersections with:
- cleatL;
- cleatR;
- M1D;
- M2D;
- ESP32 coarse mask;
- MAIN-C

were **0 mm3**.

## 3. Nominal coordinates
Global product XY, mm.

Left:
- UL1 H: X4..49, Y393..396
- UL2 H: X77..122, Y393..396
- UL3 V: X4..7, Y345..390
- UL4 V: X13..16, Y345..390
- UL5 V: X19..22, Y345..390

Right:
- UR1 H: X271..316, Y393..396
- UR2 H: X198..243, Y393..396
- UR3 V: X313..316, Y345..390
- UR4 V: X306..309, Y345..390
- UR5 V: X300..303, Y345..390

Rear shell cut depth:
- Z37.8..40.0.

Topology per side:
**2 horizontal upper + 3 vertical lateral**.

## 4. Pairwise web audit
The minimum 3.0 mm web is active, not generous.

Pairs at the 3.0 mm nominal limit include:
- UL1 vs UL3/UL4/UL5;
- UL4 vs UL5;
- UR1 vs UR3/UR4/UR5;
- UR4 vs UR5.

Therefore:
- nominal geometry PASS;
- manufacturing-tolerance release is **OPEN**.

A production drawing should not treat 3.0 mm nominal as tolerance-proof if 3.0 mm is also the hard minimum.

## 5. Interpretation
This closes the **nominal coordinate-placement gate**.

It does not close:
- shell manufacturing tolerance;
- exact shell B-rep edge/radius interactions;
- exact ESP32 antenna RF release;
- airflow CFD;
- thermal chamber validation;
- acoustic noise/whistle assessment.

## 6. Recommended next geometric refinement
Before production freeze, increase nominal web above the hard 3 mm threshold, preferably by rerunning the solver with a design web target >3 mm while retaining the 3 mm requirement as the minimum-after-tolerance criterion.

A 4 mm nominal search is the next sensible sensitivity case; it must be executed rather than assumed feasible.

## 7. Automatic checks
C854 GitHub HEAD Rev.R source verified clean.
C855 CadQuery 2.8.0 runtime confirmed.
C856 OpenCASCADE runtime confirmed.
C857 Rev.R executed.
C858 all Rev.R assertions passed.
C859 selected slot count 10.
C860 gross upper outlet area 1350 mm2.
C861 effective-area seed 1080 mm2.
C862 minimum pairwise web 3.0 mm.
C863 cleatL intersection 0 mm3 all slots.
C864 cleatR intersection 0 mm3 all slots.
C865 M1D intersection 0 mm3 all slots.
C866 M2D intersection 0 mm3 all slots.
C867 ESP32 coarse-mask intersection 0 mm3 all slots.
C868 MAIN-C intersection 0 mm3 all slots.
C869 mixed 2H+3V topology per side established.
C870 nominal coordinates recorded.
C871 nominal coordinate placement gate PASS.
C872 3 mm active web limit identified.
C873 manufacturing-tolerance release remains OPEN.
C874 CFD remains OPEN.
C875 RF final validation remains OPEN.
C876 4 mm nominal web sensitivity opened as next gate.

## 8. State
Status:
**UPPER_OUTLET_NOMINAL_LAYOUT_PASS / 10_SLOTS / 1350MM2_GROSS / 1080MM2_EFFECTIVE_SEED / ZERO_DOCUMENTED_OBSTACLE_INTERSECTION / 3MM_ACTIVE_WEB / 4MM_WEB_SENSITIVITY_NEXT / CFD_AND_TOLERANCE_OPEN / C01_TO_C876**.
