# AudioPicture V2.2 — two-turn hood sweep execution Rev.DB

Status: **162_CASE_TWO_TURN_HOOD_SWEEP_EXECUTED / ZERO_LOS_NOT_ACHIEVED / THIN_WALL_Z_LABYRINTH_FAMILY_REJECTED / COVERED_LATERAL_DUCT_NEXT**

## Execution
Rev.CZ was executed over all 162 combinations.

Variables:
- shell cheek H = 0.8 / 1.0 mm;
- frame hood top Z = 34.8 / 34.5 / 34.2 mm;
- frame hood depth = 1.5 / 2.0 / 2.5 mm;
- inward X shift = 0 / 2 / 4 mm;
- return lip = 1 / 2 / 3 mm.

## Result
Zero sampled-LOS candidates: **0**.

The best candidates still retain approximately 1.1k open straight 3D rays in the sampled audit.

Therefore the added return lip does not eliminate the residual direct-path cone.

## Decision
Reject the current thin-wall shell-cheek + frame-hood + return-lip family as a complete 3D LOS blocker.

Do not continue blind optimization of wall height/depth inside this family.

The available shell-to-frame Z space is too shallow for a robust vertical labyrinth based only on partial-height thin walls while preserving mechanical separation and thermal throat.

## Next architecture: covered lateral duct
Move the internal opening laterally away from the vent projection.

Concept:
- external vent enters a shallow shell-side collection chamber;
- chamber is covered over the direct projection;
- air travels laterally in XY for a finite distance;
- internal discharge opening is offset from all external vent sight lines;
- shell-side cover and independent structural surroundings retain positive clearance;
- no hard bridge to DML support.

This architecture seeks LOS blocking by plan-view displacement plus a roof/hood, rather than relying on repeated partial-height Z curtains.

## Checks
C1606 Rev.CZ executed.
C1607 all 162 combinations evaluated.
C1608 zero-open-ray candidates = 0.
C1609 return lip does not close residual 3D cone.
C1610 two-turn thin-wall family rejected.
C1611 further blind height/depth sweep rejected.
C1612 shallow Z packaging identified as architectural limitation.
C1613 covered lateral duct selected as next concept.
C1614 lateral displacement of internal opening required.
C1615 no acoustic attenuation result claimed.

Status:
**ACOUSTIC_REV_DB / TWO_TURN_HOOD_FAIL / COVERED_LATERAL_DUCT_NEXT / C01_TO_C1615**.
