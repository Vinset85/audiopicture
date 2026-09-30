# AudioPicture V2.2 — upper outlet 4 mm web sensitivity Rev.U

Status: **WEB4_SENSITIVITY_DEFINED / BASELINE_REV_T_PRESERVED / EXECUTION_GATE_OPEN**

## 1. Purpose
Test whether the executed Rev.T upper outlet topology can be improved from an active 3.0 mm nominal minimum web to at least 4.0 mm without relaxing any opening-area or keepout requirement.

## 2. Separate sensitivity generator
mechanical/cad/search_upper_outlet_slots_rev_u_web4.py

Rev.T / Rev.R remains unchanged as the demonstrated 3 mm nominal baseline.

## 3. Hard constraints retained
- 10 slots total;
- 5 left + 5 right;
- each slot 3 x 45 mm;
- gross area 1350 mm2;
- effective-area seed 1080 mm2 at factor 0.80;
- shell edge seed 4 mm;
- obstacle keepout margin 2 mm;
- zero documented obstacle intersection.

Only the design web target changes:
- Rev.T executed baseline: >=3 mm;
- Rev.U sensitivity: >=4 mm.

## 4. Interpretation
A Rev.U PASS would justify promoting the 4 mm geometry as the preferred nominal DMU layout.

It would not by itself prove a 3 mm minimum-after-tolerance requirement. That requires a dimensional tolerance stack including:
- ASA process capability;
- slot position/width tolerance;
- shell warp;
- datum strategy;
- post-processing if any.

A Rev.U FAIL would not invalidate Rev.T; it would show that 4 mm cannot be obtained with the current search domain/constraints.

## 5. Automatic checks
C877 Rev.T retained unchanged as executed baseline.
C878 separate Rev.U sensitivity generator created.
C879 slot count remains 10.
C880 slot module remains 3 x 45 mm.
C881 gross area remains 1350 mm2.
C882 effective-area seed remains 1080 mm2.
C883 shell edge seed remains 4 mm.
C884 obstacle keepout margin remains 2 mm.
C885 nominal pairwise web target raised to 4 mm.
C886 Rev.U real execution required before promotion.

## 6. State
Status:
**REV_U_WEB4_SEARCH_READY / REV_T_BASELINE_PRESERVED / REAL_EXECUTION_NEXT / C01_TO_C886**.
