# AudioPicture V2.2 — upper outlet exact-placement feasibility Rev.Q

Status: **FIRST_TWO_SEEDS_REJECTED / REV_B_5X_PER_BANK_WEB_CONSTRAINT_EXPOSED / DISTRIBUTED_BANK_REQUIRED**

## 1. Purpose
Convert the Rev.B upper outlet from area/module requirements into executable XY coordinates while preserving:
- 5 slots left + 5 slots right;
- each slot 3 x 45 mm;
- >=3 mm solid web;
- no cleat-island intersection;
- no M1D/M2D structural-node intersection;
- no ESP32 coarse-mask intersection;
- no MAIN-C intersection.

## 2. Seed Q0 — horizontal
First executable seed:
- horizontal 45 mm slots;
- left bank X8..53;
- right bank X267..312;
- staggered upper Y rows.

Result:
**REJECTED**.

Reason:
the left/right horizontal banks intersect the upper cleat islands.

The failure was found by explicit solid intersection, not visual inspection.

## 3. Seed Q1 — vertical lateral banks
Second seed rotates slots 90 degrees:
- 45 mm dimension in Y;
- left bank placed left of left cleat;
- right bank placed right of right cleat.

This removes the major cleat/M1D/M2D/MAIN-C/RF projection conflicts.

However a dimensional feasibility check exposes another issue.

Five parallel slots require transverse width:
- 5 x 3 mm slot width = 15 mm;
- 4 x 3 mm minimum internal web = 12 mm;
- minimum bank width = **27 mm**, excluding edge margins.

Available pure lateral band before the cleat:
- left: from product edge to cleat X25.5, less shell edge margin;
- right: from cleat X294.5 to product edge X320, less shell edge margin.

Therefore a five-slot single-column lateral bank cannot honestly satisfy the >=3 mm web rule plus edge structure.

Result:
**Q1 NOT ACCEPTED AS FINAL BANK**.

## 4. Required topology
The upper outlet must become a **distributed/staggered bank**, not five parallel slots forced into one narrow strip.

Permitted strategies:
- split each 5-slot bank into lateral and top-perimeter subgroups;
- stagger slot orientation where needed;
- use legal regions between structural/RF exclusions;
- preserve each 3 x 45 mm clear module and total 5+5 count.

Do not:
- reduce slot length to hide packaging failure;
- reduce web below 3 mm;
- cut PC-CF structural nodes;
- cut through ESP32 RF keepout;
- count service openings as outlet area.

## 5. R2 consequence
M1D R2 itself is not the source of the Q1 failure.

The limiting geometry is the combination of:
- cleat island width;
- shell edge margin;
- Rev.B five-slot count;
- >=3 mm web.

R2 remains preferred.

## 6. Next CAD gate
Create a distributed upper-outlet placement solver/search over legal shell regions.

For every candidate slot:
1. remain inside shell edge margin;
2. clear cleat islands;
3. clear M1D/M2D;
4. clear MAIN-C;
5. clear ESP32 coarse mask;
6. maintain >=3 mm slot-to-slot solid web;
7. preserve 45 x 3 mm opening;
8. preserve five slots per side.

Prefer symmetric placement where constraints permit, but symmetry is secondary to RF/structure.

## 7. Automatic checks
C807 exact upper-slot coordinate work started.
C808 Q0 horizontal seed executed.
C809 Q0 cleat intersection found.
C810 Q0 rejected.
C811 Q1 vertical lateral seed defined.
C812 Q1 avoids principal projection conflicts.
C813 five-slot minimum transverse width calculated as 27 mm.
C814 27 mm excludes additional shell edge margin.
C815 pure lateral bank insufficient.
C816 Q1 not accepted as final.
C817 Rev.B 3x45 module retained.
C818 Rev.B 5+5 count retained.
C819 Rev.B >=3 mm web retained.
C820 distributed/staggered bank required.
C821 no structural cutting allowed to preserve vent count.
C822 no RF keepout cutting allowed.
C823 R2 remains preferred.
C824 exact placement search is next gate.

## 8. State
The vent problem is now constrained geometrically rather than by area alone.

Two plausible-looking layouts have been rejected before release:
- horizontal banks collide with cleat islands;
- pure lateral vertical banks cannot fit five modules with the required web.

Status:
**UPPER_OUTLET_PLACEMENT_NOT_YET_CLOSED / Q0_REJECTED_CLEATS / Q1_REJECTED_BANK_WIDTH / DISTRIBUTED_SLOT_SEARCH_NEXT / C01_TO_C824**.
