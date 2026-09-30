# AudioPicture V2.2 — ASA vent coupon and metrology Rev.X

Status: **COUPON_GEOMETRY_DEFINED / PROCESS_CHARACTERIZATION_PROTOCOL_DEFINED / PHYSICAL_PRINT_AND_MEASUREMENT_OPEN**

## 1. Purpose
Turn the Rev.W symbolic tolerance budget into a measurable manufacturing experiment for the intended ASA process.

The coupon characterizes local vent geometry.

It does **not** replace full rear-shell warp measurement.

Generator:
mechanical/cad/generate_asa_vent_coupon_rev_x.py

## 2. Coupon geometry
Material/process target:
- same ASA family intended for the rear shell;
- same nominal shell thickness: **2.2 mm**.

Coupon plate:
- 125 x 100 x 2.2 mm nominal.

Vent geometry:
- slot width 3.0 mm;
- slot length 45.0 mm;
- critical adjacent-slot web 4.0 mm.

Features:
- H1/H2: horizontal adjacent pair with 4.0 mm nominal common web;
- V1/V2: vertical adjacent pair with 4.0 mm nominal common web;
- H_REF: isolated horizontal 3 x 45 mm reference slot;
- V_REF: isolated vertical 3 x 45 mm reference slot.

The H/V pairs allow process anisotropy to be observed rather than assumed absent.

## 3. Required print equivalence
For qualification data, print the coupon with the same intended production settings as the rear shell:
- printer;
- nozzle;
- ASA material family and recorded lot;
- layer height;
- extrusion/profile settings;
- enclosure/chamber condition;
- bed preparation;
- cooling strategy;
- print orientation;
- post-processing.

Any deliberate difference must be recorded.

## 4. Measurement equipment
Use an instrument whose resolution is materially smaller than the tolerance being evaluated.

Record:
- instrument type;
- resolution;
- calibration/status if available;
- operator/method;
- ambient condition when relevant.

Do not infer capability from slicer dimensions.

## 5. Measurements per coupon
### Slot width
For H1, H2, V1, V2, H_REF and V_REF:
- measure clear width near 10%, 50% and 90% of slot length;
- record minimum, maximum and mean.

### Slot length
Measure clear slot length for each feature.

### Critical web
For H1/H2 and V1/V2:
- measure common web at 10%, 50% and 90% of its length;
- record minimum web as the primary local acceptance metric.

### Position
Measure feature edges or centerlines from defined coupon datums.

Use the same datum philosophy intended for the shell drawing.

### Flatness
Measure coupon out-of-plane distortion sufficiently to identify local warp.

Coupon flatness is process information, not a substitute for full-shell warp.

## 6. Sample plan
No statistical capability is claimed yet.

Recommended engineering characterization sequence:
- first article: verify method and gross failure modes;
- then multiple coupons from separate print runs;
- include more than one location/orientation on the build plate if that could affect the process.

The final production sample count must be frozen with the manufacturing plan; this document does not invent a statistically sufficient N.

## 7. Link to Rev.W
Rev.W release equation:

**E_width_pair + E_relative_position + E_local_warp <= 1.0 mm**

Coupon data can directly inform:
- E_width_pair;
- local relative-position behavior;
- local warp sensitivity;
- H/V anisotropy.

Full rear-shell measurements are still required for:
- global/local shell warp at the actual vent banks;
- datum transfer over the 320 x 400 mm component;
- interaction with shell ribs and thermal history.

## 8. Data reduction
For every printed coupon retain raw measurements.

Report separately:
- dimensional error from nominal;
- minimum measured web;
- H vs V result;
- run-to-run variation.

Do not combine systematic bias and random spread into one undocumented tolerance number.

If a consistent dimensional bias is found, correct the process/CAD compensation only after repeatability is demonstrated.

## 9. Gate
Local coupon gate:
- no cracking or incomplete web;
- no fused/closed slot;
- measurable 3 x 45 mm features;
- critical web data collected in H and V;
- process metadata complete.

Tolerance-release gate:
- requires measured error terms plus full-shell warp data;
- Rev.W inequality must remain satisfied.

## 10. Automatic checks
C925 Rev.W converted to physical coupon concept.
C926 coupon nominal thickness 2.2 mm.
C927 coupon plate 125 x 100 mm.
C928 3 x 45 mm slot geometry replicated.
C929 4.0 mm critical web replicated.
C930 horizontal critical pair included.
C931 vertical critical pair included.
C932 isolated H reference slot included.
C933 isolated V reference slot included.
C934 H/V process anisotropy measurable.
C935 slot width measured at multiple longitudinal positions.
C936 critical web measured at multiple positions.
C937 position measurement tied to datums.
C938 coupon flatness measurement required.
C939 production-equivalent process metadata required.
C940 slicer dimensions prohibited as capability evidence.
C941 raw measurement retention required.
C942 systematic bias separated from variation.
C943 coupon does not replace full-shell warp test.
C944 physical print remains OPEN.
C945 physical metrology remains OPEN.

## 11. State
Status:
**ASA_VENT_COUPON_REV_X_DEFINED / H_AND_V_4MM_WEB_CHARACTERIZATION / PHYSICAL_PRINT_AND_METROLOGY_REQUIRED / FULL_SHELL_WARP_STILL_REQUIRED / C01_TO_C945**.
