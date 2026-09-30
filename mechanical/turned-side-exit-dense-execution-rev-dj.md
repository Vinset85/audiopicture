# AudioPicture V2.2 — turned side-exit dense audit execution Rev.DJ

Status: **COARSE_ZERO_LOS_FALSE_POSITIVE / DENSE_LOS_FAIL / CAD_PROMOTION_BLOCKED / TERMINAL_CHAMBER_REDESIGN_REQUIRED**

## Execution
Rev.DH was actually executed on the selected compact/high-throat Rev.DF coarse-pass candidate:

- L = 36 mm;
- W = 48 mm;
- roof lower Z = 36.8 mm;
- wall thickness = 1.0 mm;
- Y shift = 0;
- elbow length = 16 mm;
- overlap = 6 mm;
- discharge slot = 16 mm.

Geometric throat proxy = 42.0 mm2.

## Dense sampling
The audit uses:
- 714 source points;
- 1,071 cavity destination points;
- 764,694 straight 3D rays.

The denser set includes edge-biased vent samples and targets close to the exit region.

## Result
The candidate does **not** retain zero LOS under dense sampling.

Therefore the Rev.DF coarse zero-ray result is classified as sampling-dependent and is not sufficient for promotion.

Decision: **FAIL dense sampled geometric LOS.**

No real-product CadQuery duct solid is promoted from this candidate.

## Failure interpretation
Open-ray examples cluster around source/target combinations near duct/exit edge regions.

The current elbow and return wall redirect much of the direct cone but do not form a fully screened terminal chamber.

## Next architecture
Replace the exposed turned side-exit with a terminal chamber:
- duct feeds a small chamber;
- chamber closed on three sides plus roof;
- discharge opening placed on a face whose normal points away from the external vent cone;
- add geometric overlap between duct entrance and chamber exit projections;
- preserve finite throat.

The next parameter search shall use the dense/edge-biased ray population directly rather than using a coarse sweep as the primary pass criterion.

## Checks
C1651 Rev.DH actually executed.
C1652 selected Rev.DF candidate throat proxy 42.0mm2.
C1653 dense source count 714.
C1654 dense destination count 1071.
C1655 dense ray count 764694.
C1656 dense LOS result FAIL.
C1657 Rev.DF coarse zero-LOS classified sampling-dependent.
C1658 candidate CAD promotion blocked.
C1659 terminal chamber selected as next topology.
C1660 dense edge-biased population promoted to primary screening method.
C1661 no acoustic attenuation claim.

Status:
**ACOUSTIC_REV_DJ / TURNED_EXIT_DENSE_FAIL / TERMINAL_CHAMBER_NEXT / C01_TO_C1661**.
