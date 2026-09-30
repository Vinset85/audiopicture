# AudioPicture V2.2 — distributed upper-outlet placement search Rev.R

Status: **DISTRIBUTED_SEARCH_IMPLEMENTED / REV_B_AREA_AND_WEB_PRESERVED / 2MM_KEEP_OUT_MARGIN_ADDED / KERNEL_EXECUTION_REQUIRED_BEFORE_FREEZE**

## 1. Purpose
Replace manual vent-slot trial placement with a reproducible geometric feasibility search.

Generator/search:
mechanical/cad/search_upper_outlet_slots_rev_r.py

## 2. Frozen requirements preserved
The search is not allowed to relax:
- 10 upper outlet slots total;
- 5 left + 5 right;
- 3 x 45 mm clear opening per slot;
- gross area 1350 mm2;
- preliminary effective-area seed 1080 mm2 at Rev.B factor 0.80;
- minimum slot-to-slot solid web 3 mm.

## 3. Search domain
Candidate orientations:
- horizontal 45 x 3 mm;
- vertical 3 x 45 mm.

Grid:
- 1 mm nominal search grid.

Rear-shell upper region:
- Y>=315;
- 4 mm seed shell edge margin;
- left/right ownership split at X160.

## 4. Hard exclusions
Candidate slots are rejected around:
- left cleat island;
- right cleat island;
- M1D;
- M2D;
- coarse ESP32 mask;
- MAIN-C.

A 2 mm geometric margin is added around each current hard-exclusion rectangle for the placement search.

This margin is a CAD robustness seed, not a tolerance-stack release value.

## 5. Pairwise web
For every selected slot pair, the search requires >=3 mm solid separation along at least one Cartesian separating direction.

This prevents the Rev.Q failure where five nominally legal slots were packed into a strip too narrow to retain the frozen web.

## 6. Search strategy
The current implementation:
1. enumerates legal H/V candidates;
2. sorts toward upper/perimeter placement;
3. reduces near-duplicate candidates;
4. backtracks to select five per side;
5. reconstructs all selected slots as CadQuery solids;
6. reports 3D intersections against the documented obstacle solids;
7. reports minimum pairwise web.

The solver is a feasibility search, not a thermal optimizer.

## 7. Acceptance
A candidate bank may advance only if the executed result shows:
- slot_count = 10;
- gross area = 1350 mm2;
- effective seed = 1080 mm2 under the Rev.B 0.80 factor;
- minimum pairwise web >=3 mm;
- all reported hard-obstacle intersection volumes = 0;
- all slots remain within edge/domain limits.

## 8. Important limitation
The search currently uses documented rectangular obstacle envelopes.

It does not replace:
- exact shell B-rep;
- exact cleat STEP;
- exact ESP32 antenna STEP/RF mask;
- CFD;
- physical thermal validation.

The final slot set is therefore not frozen until the script is executed in the CadQuery runtime and its coordinates/results are recorded.

## 9. Structural interpretation
The search routes ASA shell openings around PC-CF nodes.

It does not cut the PC-CF R2 return to satisfy ventilation.

R2 remains the preferred M1D structural candidate.

## 10. Automatic checks
C825 distributed vent placement search implemented.
C826 H and V slot candidates allowed.
C827 1 mm search grid defined.
C828 4 mm shell edge margin seed.
C829 5 left + 5 right count hard-constrained.
C830 3 x 45 mm module hard-constrained.
C831 gross outlet 1350 mm2 preserved.
C832 Rev.B effective seed 1080 mm2 preserved.
C833 >=3 mm pairwise web hard-constrained.
C834 cleat islands included as exclusions.
C835 M1D/M2D included as exclusions.
C836 MAIN-C included as exclusion.
C837 coarse ESP32 mask included as exclusion.
C838 2 mm keep-out placement margin added.
C839 candidate set reconstructed as CadQuery solids.
C840 3D obstacle intersections reported.
C841 search explicitly not CFD.
C842 search explicitly not RF release.
C843 PC-CF R2 is not cut for vent placement.
C844 executed coordinates required before freeze.

## 11. State
The upper outlet problem now has a reproducible search mechanism that preserves the Rev.B thermal opening specification rather than weakening it to fit packaging.

Status:
**VENT_PLACEMENT_SOLVER_READY / 1350MM2_AND_3MM_WEB_HARD_CONSTRAINTS / 2MM_KO_MARGIN / EXECUTION_AND_COORDINATE_FREEZE_NEXT / C01_TO_C844**.
