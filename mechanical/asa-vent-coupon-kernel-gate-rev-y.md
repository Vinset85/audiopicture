# AudioPicture V2.2 — ASA vent coupon executed kernel gate Rev.Y

Status: **REV_X_KERNEL_EXECUTED_PASS / STEP_AND_STL_GENERATION_VERIFIED / PHYSICAL_PRINT_OPEN**

## 1. Executed source
mechanical/cad/generate_asa_vent_coupon_rev_x.py

The committed Rev.X generator was executed in the project CAD runtime using CadQuery/OpenCASCADE.

## 2. Kernel result
Executed checks:
- B-rep valid: PASS;
- connected solid count: 1;
- bounding box: 125.0 x 100.0 x 2.2 mm;
- six intended slot openings are through-cuts;
- H1/H2 nominal common web: 4.0 mm;
- V1/V2 nominal common web: 4.0 mm.

Nominal plate volume before cuts:
125 x 100 x 2.2 = 27,500 mm3.

Six nominal slot volumes:
6 x 3 x 45 x 2.2 = 1,782 mm3.

Expected final nominal volume:
27,500 - 1,782 = **25,718 mm3**.

Kernel volume agrees with this nominal subtraction within numerical precision.

This is a geometry consistency check, not a manufacturing result.

## 3. Export
The executed generator produced:
- AP22_ASA_VENT_COUPON_REV_X.step
- AP22_ASA_VENT_COUPON_REV_X.stl

Export success demonstrates file generation in the CAD runtime.

The repository currently retains the parametric source as the authoritative artifact; binary export publication can be handled separately if required.

## 4. Measurement template
Added:
mechanical/test/asa-vent-coupon-measurements-rev-x.csv

It records:
- specimen/run metadata;
- production settings;
- instrument/resolution;
- H/V feature identity;
- 10/50/90% measurement positions;
- nominal and measured width;
- nominal and measured length;
- nominal and measured web;
- datum position;
- local flatness;
- notes.

No unmeasured value is pre-populated as a result.

## 5. Physical gate
The next evidence must come from printed ASA specimens.

Required sequence:
1. print Rev.X using the intended rear-shell process;
2. measure the coupon per Rev.X protocol;
3. populate the CSV with raw values;
4. derive width-pair and relative-position terms;
5. measure full-shell local/global warp separately;
6. evaluate the Rev.W <=1.0 mm total-loss inequality.

## 6. Automatic checks
C946 Rev.X committed source inspected before execution.
C947 Rev.X kernel executed.
C948 B-rep validity PASS.
C949 connected solid count 1.
C950 bbox 125 x 100 x 2.2 mm.
C951 six intended through-openings verified.
C952 H critical nominal web 4.0 mm.
C953 V critical nominal web 4.0 mm.
C954 analytic pre-cut volume 27500 mm3.
C955 analytic removed slot volume 1782 mm3.
C956 analytic final volume 25718 mm3.
C957 kernel volume consistent with analytic result.
C958 STEP export generated in runtime.
C959 STL export generated in runtime.
C960 geometry execution not treated as process capability.
C961 measurement CSV template added.
C962 raw physical measurements remain OPEN.
C963 full-shell warp measurement remains OPEN.
C964 Rev.W tolerance release remains OPEN.

## 7. State
Status:
**ASA_VENT_COUPON_KERNEL_PASS / STEP_STL_EXPORT_VERIFIED / METROLOGY_TEMPLATE_READY / PHYSICAL_ASA_PRINT_AND_FULL_SHELL_WARP_REQUIRED / C01_TO_C964**.
