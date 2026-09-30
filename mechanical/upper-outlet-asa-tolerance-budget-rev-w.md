# AudioPicture V2.2 — ASA upper-outlet tolerance budget Rev.W

Status: **NOMINAL_TO_MINIMUM_BUDGET_DERIVED / PROCESS_CAPABILITY_DATA_MISSING / MEASUREMENT_GATE_DEFINED**

## 1. Basis
Executed Rev.V:
- minimum nominal pairwise web = 4.0 mm;
- required geometric minimum retained for tolerance work = 3.0 mm.

Therefore the available worst-case web-loss budget is:

**4.0 - 3.0 = 1.0 mm total.**

No ASA process tolerance is inferred from generic printing knowledge.

Repository search found no project-specific:
- ASA dimensional capability study;
- shell warp measurements;
- vent-slot coupon results;
- qualified printer/profile tolerance specification.

## 2. Worst-case model
For the critical web between two adjacent slots:

**W_actual_min = 4.0 - (E_width_pair + E_relative_position + E_local_warp)**

where:
- E_width_pair = combined adverse slot-width/edge contribution of the two slots;
- E_relative_position = adverse relative placement error that closes the web;
- E_local_warp = local dimensional distortion projected onto the web direction.

Release condition:

**E_width_pair + E_relative_position + E_local_warp <= 1.0 mm**

This is a budget equation, not a claim that the selected ASA process can achieve it.

## 3. Width interpretation
If each slot is dimensioned symmetrically around a controlled centerline and each slot has total width tolerance +/-Tw, the adverse edge movement toward the common web is Tw/2 from each slot.

For equal adjacent slots:
- pair contribution = Tw.

If manufacturing controls edges directly rather than centerline+width, use the measured edge errors directly and do not apply this simplification.

## 4. Allocation examples — sensitivity only
Examples below are possible budget allocations, not process specifications.

If relative position consumes 0.20 mm and local warp 0.10 mm:
- maximum remaining pair-width contribution = 0.70 mm.

If relative position consumes 0.30 mm and local warp 0.20 mm:
- remaining pair-width contribution = 0.50 mm.

If relative position consumes 0.40 mm and local warp 0.30 mm:
- remaining pair-width contribution = 0.30 mm.

If relative position + warp already reaches 1.0 mm:
- no budget remains for slot-width error;
- the process is not releasable against this stack.

## 5. Measurement plan
Do not production-freeze Rev.V from nominal CAD alone.

Build an ASA shell/coupon measurement set using the intended:
- printer;
- nozzle;
- layer height;
- material batch/family;
- chamber/enclosure condition;
- print orientation;
- slicer/profile;
- cooling strategy;
- post-processing.

Measure at minimum:
1. each 3 mm slot width at multiple positions along the 45 mm length;
2. critical web widths between adjacent slots;
3. slot center/edge positions relative to shell datums;
4. local shell flatness/warp in each vent bank;
5. left/right bank repeatability;
6. repeatability across multiple prints.

## 6. Statistical release
Worst-case geometry and process capability are separate.

Before release, record:
- sample count;
- min/max;
- mean;
- standard deviation where sample count supports it;
- measurement method/resolution;
- environmental condition if relevant.

A process capability criterion may be added only after the dimensional specification and sample plan are frozen.

No Cpk value is claimed here.

## 7. Design decision logic
If measured worst-case stack <=1.0 mm:
- Rev.V can advance toward production tolerance release.

If measured stack >1.0 mm:
- do not weaken the 3 mm minimum silently;
- either increase nominal web through another placement search, improve process capability, or revise slot topology with thermal revalidation.

## 8. Automatic checks
C909 repository searched for ASA project-specific tolerance evidence.
C910 no qualified ASA dimensional capability data found.
C911 no qualified shell warp dataset found.
C912 no vent-slot coupon dataset found.
C913 Rev.V nominal web 4.0 mm retained.
C914 tolerance minimum web 3.0 mm retained.
C915 total worst-case web-loss budget derived as 1.0 mm.
C916 width-pair error term defined.
C917 relative-position error term defined.
C918 local-warp error term defined.
C919 release inequality defined.
C920 allocation examples explicitly sensitivity-only.
C921 measurement plan defined.
C922 process capability claim prohibited until measured.
C923 Cpk not claimed.
C924 failure path preserves 3 mm minimum.

## 9. State
Status:
**REV_V_1P0MM_TOTAL_TOLERANCE_BUDGET / NO_UNSUPPORTED_ASA_TOLERANCE_ASSUMPTION / COUPON_AND_SHELL_MEASUREMENT_REQUIRED / C01_TO_C924**.
