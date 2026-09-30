# AudioPicture V2.2 — executed upper outlet 4 mm layout Rev.V

Status: **REV_U_EXECUTED_PASS / WEB4_PREFERRED_NOMINAL_DMU / PRODUCTION_TOLERANCE_AND_CFD_OPEN**

## 1. Runtime result
Rev.U was executed in CadQuery 2.8.0 with the OpenCASCADE backend.

All embedded assertions passed.

Results:
- legal candidates: 1879 left, 2572 right;
- reduced search set: 257 left, 345 right;
- selected slots: 10;
- hard keepout margin: 2.0 mm;
- gross outlet area: 1350 mm2;
- Rev.B effective-area seed: 1080 mm2;
- minimum pairwise web: **4.0 mm**;
- all documented obstacle intersection volumes: **0 mm3**.

## 2. Preferred nominal coordinates
Global product XY, mm. Rear-shell cut Z37.8..40.0.

Left:
- UL1 H: X4..49, Y393..396
- UL2 H: X77..122, Y393..396
- UL3 H: X82..127, Y386..389
- UL4 V: X4..7, Y341..386
- UL5 V: X13..16, Y341..386

Right:
- UR1 H: X271..316, Y393..396
- UR2 H: X198..243, Y393..396
- UR3 H: X193..238, Y386..389
- UR4 V: X313..316, Y341..386
- UR5 V: X306..309, Y341..386

Topology per side:
**3 horizontal + 2 vertical**.

## 3. Comparison with Rev.T
Rev.T demonstrated:
- 10 slots;
- 1350 mm2 gross;
- 1080 mm2 effective seed;
- 3.0 mm minimum nominal web;
- zero documented obstacle intersection.

Rev.U/Rev.V demonstrates the same area and obstacle result with:
- **4.0 mm minimum nominal web**.

Therefore Rev.V supersedes Rev.T as the **preferred nominal DMU vent layout**.

Rev.T remains a valid executed fallback/reference.

## 4. What is frozen and what is not
Frozen for nominal DMU:
- slot count;
- slot dimensions;
- nominal Rev.V XY coordinates;
- rear-shell cut Z37.8..40.0;
- 4.0 mm minimum nominal pairwise web in the executed model.

Not production-frozen:
- minimum web after ASA dimensional tolerance;
- slot position tolerance;
- shell warp allowance;
- exact molded/printed edge radii;
- airflow performance;
- RF performance.

## 5. Next gate
Build the ASA rear-shell vent tolerance stack.

The relevant question is no longer whether the slots fit nominally.

The next question is whether a 4.0 mm nominal web provides enough margin to guarantee the required minimum web after:
- slot width error;
- slot positional error;
- shell process distortion/warp;
- datum and inspection uncertainty.

No tolerance values are to be invented. Use process evidence or measured coupon/shell data.

## 6. Automatic checks
C887 Rev.U source verified at repository HEAD.
C888 CadQuery 2.8.0 runtime confirmed.
C889 Rev.U executed.
C890 all embedded assertions passed.
C891 selected slot count 10.
C892 gross outlet area 1350 mm2.
C893 effective-area seed 1080 mm2.
C894 minimum pairwise web 4.0 mm.
C895 cleatL intersections 0 mm3.
C896 cleatR intersections 0 mm3.
C897 M1D intersections 0 mm3.
C898 M2D intersections 0 mm3.
C899 ESP32 coarse-mask intersections 0 mm3.
C900 MAIN-C intersections 0 mm3.
C901 topology is 3H+2V per side.
C902 Rev.V coordinates recorded.
C903 Rev.V preferred over Rev.T for nominal DMU.
C904 Rev.T retained as executed fallback/reference.
C905 production tolerance proof remains OPEN.
C906 CFD remains OPEN.
C907 exact RF release remains OPEN.
C908 ASA vent tolerance stack is next gate.

## 7. State
Status:
**UPPER_OUTLET_WEB4_EXECUTED_PASS / REV_V_PREFERRED_NOMINAL_DMU / 10X_3X45 / 1350MM2_GROSS / 1080MM2_EFFECTIVE_SEED / ZERO_DOCUMENTED_OBSTACLE_INTERSECTION / 4MM_MIN_NOMINAL_WEB / TOLERANCE_CFD_RF_OPEN / C01_TO_C908**.
