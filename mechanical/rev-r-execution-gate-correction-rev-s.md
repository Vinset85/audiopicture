# AudioPicture V2.2 — Rev.R execution gate correction Rev.S

Status: **REV_R_SOURCE_DEFECT_FOUND_AND_FIXED / SELF_ASSERTIONS_ADDED / EXECUTED_KERNEL_RESULT_STILL_REQUIRED**

## 1. Defect found
Before claiming execution, the repository source of:
mechanical/cad/search_upper_outlet_slots_rev_r.py

was inspected.

A literal escaped newline token had been introduced into the Python dictionary emitted at the end of the script.

That source defect made the prior Rev.R file non-executable as committed.

Therefore the previous state **VENT_PLACEMENT_SOLVER_READY** is corrected to:
**PLACEMENT_SEARCH_DESIGN_READY / SOURCE_EXECUTION_NOT_YET_PROVEN**.

No slot coordinates from the defective revision are treated as valid.

## 2. Correction
The malformed token was removed.

The script now includes hard assertions:
- exactly 10 selected slots;
- gross area exactly 1350 mm2;
- minimum pairwise web >=3 mm;
- every 3D hard-obstacle intersection volume equals zero.

The script must terminate with failure if any of these conditions is false.

## 3. Release discipline
No coordinate set is frozen from Rev.R until the corrected script is actually run in a CadQuery/OpenCASCADE environment and its JSON result is recorded.

This correction prevents a source-generation error from being mistaken for a CAD result.

## 4. Automatic checks
C845 committed Rev.R source inspected before execution claim.
C846 malformed literal newline defect identified.
C847 defective Rev.R not treated as executed.
C848 malformed token corrected.
C849 slot-count assertion added.
C850 gross-area assertion added.
C851 pairwise-web assertion added.
C852 zero-obstacle-intersection assertion added.
C853 coordinate freeze remains blocked until real runtime execution.

## 5. State
Status:
**REV_R_CORRECTED_AND_HARDENED / NO_FALSE_EXECUTION_CLAIM / REAL_CADQUERY_RUN_NEXT / C01_TO_C853**.
