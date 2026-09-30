# AudioPicture V2.2 — real terminal chamber placement execution Rev.DR

Status: **FOUR_BANK_ENVELOPE_PLACEMENT_PASS_AT_Z35P1 / THROAT_PENALTY_IDENTIFIED / SCULPTED_MAPPING_NEXT**

## Execution
Rev.DP was executed against the authoritative coarse PC-CF Rev.C kernel and the actual Rev.BK vent-bank coordinates.

The conservative occupied-envelope audit covers LL, LR, UL and UR.

## Result
For all four banks, the first tested collision-free lower Z is:

**Z = 35.1 mm**

At Z35.1:
- frame overlap = 0 in the conservative occupied-envelope test;
- local throat proxy = 15 mm x (36.8 - 35.1) mm = **25.5 mm2 per duct**.

The normalized Rev.DO geometry used Z34.0 and had a local throat proxy of 44.8 mm2.

Therefore a uniform elevation of the complete chamber above the PC-CF rear face would reduce the local proxy substantially.

## Decision
Do not freeze a uniform Z35.1 chamber as the preferred design yet.

Use Z35.1 as the guaranteed collision-free fallback plane.

Next, construct a sculpted mapping:
- keep solid chamber/duct features above Z35.1 where they project onto PC-CF material;
- allow locally deeper air volume only where Rev.C has genuine XY openings/keepouts;
- never create shell-to-frame hard contact;
- retain the Rev.DO plan-view LOS topology;
- maximize the minimum real throat subject to those constraints.

The sculpted geometry must then be checked as actual CadQuery solids, not only occupied envelopes.

## Checks
C1699 Rev.DP executed against Rev.C frame.
C1700 LL first tested collision-free lower Z 35.1mm.
C1701 LR first tested collision-free lower Z 35.1mm.
C1702 UL first tested collision-free lower Z 35.1mm.
C1703 UR first tested collision-free lower Z 35.1mm.
C1704 Z35.1 local throat proxy 25.5mm2 per duct.
C1705 normalized 44.8mm2 throat not preserved by uniform elevation.
C1706 uniform Z35.1 retained only as fallback.
C1707 sculpted keepout-aware real mapping selected next.
C1708 real solid collision/connectivity gate remains open.

Status:
**MECHANICAL_REV_DR / FOUR_BANK_Z35P1_FALLBACK_PASS / SCULPTED_REAL_MAPPING_NEXT / C01_TO_C1708**.
