# AudioPicture V2.2 — integrated ASA rear-shell upper kernel Rev.Z

Status: **REAL_RADIUS_UPPER_OUTLET_KERNEL_PASS / INDUSTRIAL_FDM_ASA_PREFERRED / LOWER_INLET_PLACEMENT_NEXT**

## 1. Manufacturing direction
Preferred rear-shell manufacturing route:
**industrial FDM in unfilled ASA**, using an external qualified service if needed.

This preserves the frozen ASA material architecture while avoiding dependence on a desktop printer for the 320 x 400 mm shell.

Supplier-published generic dimensional capability is screening information only. Part-specific acceptance remains required because the shell is large and thin.

## 2. Executed nominal kernel
Generator:
mechanical/cad/generate_rear_shell_integrated_rev_z.py

Executed geometry:
- rear panel X = 320 mm;
- rear panel Y = 400 mm;
- thickness = 2.2 mm;
- global Z = 37.8..40.0 mm;
- 10 Rev.V upper outlet slots;
- slot overall envelope = 3 x 45 mm;
- real slot-end radius = R1.5 mm.

Kernel:
- valid B-rep: PASS;
- connected solid count: 1;
- nominal product envelope preserved;
- all ten openings through-cut;
- documented Rev.V obstacle intersections = 0 mm3.

## 3. Corrected real opening area
Earlier Rev.B/Rev.V sizing used the 3 x 45 mm bounding rectangle:
135 mm2/slot.

For the actual R1.5 capsule with 45 mm overall length:

A = (45 - 3) x 3 + pi x 1.5^2
= **133.0686 mm2/slot**.

Ten slots:
**1330.686 mm2 actual geometric gross outlet area**.

Using the existing preliminary 0.80 CAD blockage factor:
**1064.549 mm2 effective seed**.

Preferred outlet threshold:
1000 mm2.

Nominal seed margin:
**+64.549 mm2**, about **+6.45%** over the preferred effective threshold.

Therefore the real R1.5 slot geometry still clears the preliminary area target.

This does not replace CFD.

## 4. Why lower inlet is not yet cut
Rev.B freezes:
- 12 slots;
- 3 x 40 mm nominal module;
- 6 left + 6 right;
- R1.5 ends;
- lower-left/lower-right architecture;
- central service recess excluded;
- ENV excluded.

It does not freeze exact slot XY coordinates.

Inventing those coordinates directly in the shell would bypass the structural/service/ENV collision gate.

Therefore Rev.Z intentionally integrates the executed upper layout only.

## 5. Next geometric gate
Create a lower-inlet placement solver analogous to Rev.R/U with:
- 12 capsule slots;
- 6 per side;
- 3 x 40 mm overall envelope;
- R1.5 ends;
- >=4 mm nominal web preferred if feasible;
- shell edge margin;
- L1/R2 structural keep-outs;
- VOICE exclusion where applicable;
- central service X100..220/Y20..48 exclusion;
- ENV X252..294/Y35..59 exclusion;
- lower supports and anti-lift exclusions;
- cable/harness clearance where documented.

After an executed lower layout PASS, integrate it into Rev.Z successor and then add shell perimeter/retention/baffles.

## 6. Manufacturing acceptance
For external industrial FDM:
- request ASA explicitly;
- request the supplier's dimensional tolerance applicable to this exact 320 x 400 x 2.2 mm geometry;
- require confirmation of warp/flatness capability;
- do not accept generic website tolerance as automatic compliance;
- preserve Rev.W web-loss budget unless later geometry improves it.

If the supplier cannot guarantee the required geometry, the design should be adjusted before ordering rather than accepting a thinner web.

## 7. Automatic checks
C965 industrial FDM ASA selected as preferred rear-shell route.
C966 external service permitted.
C967 320 x 400 x 2.2 rear panel kernel generated.
C968 global Z37.8..40 preserved.
C969 Rev.V ten-slot coordinates integrated.
C970 real R1.5 slot ends integrated.
C971 kernel B-rep valid.
C972 kernel connected solid count 1.
C973 all upper slots through-cut.
C974 documented obstacle intersection volume zero.
C975 real capsule area derived as 133.0686 mm2/slot.
C976 actual upper gross area 1330.686 mm2.
C977 0.80 effective seed 1064.549 mm2.
C978 preferred 1000 mm2 outlet threshold retained.
C979 nominal effective-area margin +64.549 mm2.
C980 CFD remains required.
C981 generic supplier tolerance not treated as part-specific proof.
C982 lower inlet exact XY remains OPEN.
C983 lower inlet placement solver defined as next gate.
C984 lower slots must use real R1.5 geometry.
C985 lower inlet 4 mm nominal web preferred if feasible.

## 8. State
Status:
**ASA_REAR_SHELL_REV_Z_UPPER_KERNEL_PASS / 320X400X2P2 / REAL_R1P5_OUTLETS / 1330P686MM2_GROSS / 1064P549MM2_EFFECTIVE_SEED / INDUSTRIAL_FDM_ASA_PREFERRED / LOWER_INLET_SOLVER_NEXT / C01_TO_C985**.
