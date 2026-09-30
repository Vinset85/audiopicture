# AudioPicture V2.2 — spatial CFD heat allocation Rev.CJ

Status: **BOARD_LEVEL_SPATIAL_SOURCE_MODEL_DEFINED / EXACT_TOTAL_HEAT_CONSERVED / MODEL_ALLOCATIONS_NOT_MEASURED_LOSSES / CFD_GEOMETRY_COUPLING_NEXT**

## Purpose
Provide a controlled first spatial distribution for the existing 5/8/10 W enclosure heat cases without inventing component dissipation.

This is a CFD modeling allocation, not a measured or calculated electrical loss budget.

## Board regions
Current packaging seeds used for the coarse thermal source regions:

MAIN-P:
- X105..220 mm;
- Y112..157 mm;
- power/audio board;
- primary hot PCB by existing architecture.

MAIN-C:
- X85..235 mm;
- Y315..370 mm;
- PoE/network/control board.

These XY rectangles are packaging seeds and remain subject to exact CAD/PCB freeze.

## Scenario allocations
### 5 W enclosure case
- MAIN-P: 70% = 3.50 W
- MAIN-C: 30% = 1.50 W
- total = 5.00 W

### 8 W enclosure case
- MAIN-P: 75% = 6.00 W
- MAIN-C: 25% = 2.00 W
- total = 8.00 W

### 10 W adverse enclosure case
- MAIN-P: 80% = 8.00 W
- MAIN-C: 20% = 2.00 W
- total = 10.00 W

## Why the split changes with load
The existing architecture identifies MAIN-P as the primary heat-producing board and MAIN-C as the digital/RF/PoE board.

As total system heat rises in the first model, the extra modeled heat is biased toward MAIN-P to represent increasing audio/power-conversion stress.

This is a modeling hypothesis for enclosure-flow discrimination only.

It is not evidence that the real product has exactly these board losses.

## Comparison rule
For any selected thermal case, use the identical source allocation in:
- CFD-0;
- CFD-08;
- CFD-10.

Example:
the 8 W / 30 C / 4 mm comparison must use MAIN-P=6 W and MAIN-C=2 W in all three geometries.

This isolates the effect of labyrinth geometry.

## Component refinement
When a component-resolved source is introduced:
1. establish its loss from measured/calculated evidence;
2. establish its exact CAD location;
3. subtract the same watts from the parent board aggregate;
4. verify total active heat remains exactly equal to the scenario total.

Example:
if a validated 1.0 W converter source is introduced inside an 8 W case, the relevant board aggregate is reduced by 1.0 W. It is not added as a ninth watt.

## Raspberry Pi 5
The current project packaging/thermal documents do not yet provide a reconciled project-specific Pi 5 heat-source value and exact source abstraction for this CFD model.

Do not hide an assumed Pi loss inside a named Pi source.

For the first enclosure-flow comparison, the 5/8/10 W total source already represents the complete modeled internal heat budget.

A future Pi-resolved model must preserve the selected total or define a new explicitly justified system scenario.

## Solver implementation
First solver implementation may represent each board source as:
- uniform volumetric heat in a simplified PCB solid; or
- uniform surface heat flux over a defined board hot-side area.

Use the same abstraction for all labyrinth geometries.

A later component-resolved model supersedes the uniform board source for final local temperature work.

## Checks
C1457 current MAIN-P seed X105..220/Y112..157 retained for coarse source.
C1458 current MAIN-C seed X85..235/Y315..370 retained for coarse source.
C1459 board rectangles remain packaging seeds, not PCB release dimensions.
C1460 5W case allocated 3.5W MAIN-P + 1.5W MAIN-C.
C1461 8W case allocated 6.0W MAIN-P + 2.0W MAIN-C.
C1462 10W case allocated 8.0W MAIN-P + 2.0W MAIN-C.
C1463 each scenario sum exactly conserved.
C1464 fractions explicitly classified as modeling allocations.
C1465 same allocation required across CFD-0/08/10.
C1466 component source introduction requires equal subtraction from parent aggregate.
C1467 Raspberry Pi 5 local source remains open.
C1468 total heat sweep remains enclosure-level authority.
C1469 uniform board source permitted for first airflow comparison.
C1470 component-resolved model required for final local-temperature claims.

Status:
**THERMAL_REV_CJ / BOARD_LEVEL_SOURCE_MODEL / 5W_8W_10W_EXACT_SUM / CFD_COUPLING_NEXT / C01_TO_C1470**.
