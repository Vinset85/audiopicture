# AudioPicture V2.2 — turned side-exit coarse-pass and dense recheck Rev.DI

Status: **REV_DF_COARSE_ZERO_LOS_FOUND / DENSE_INDEPENDENT_RECHECK_DEFINED / PROMOTION_PENDING_DENSE_RESULT**

Rev.DF was executed over the full 2,592-case normalized sweep.

Unlike the earlier labyrinth families, the turned side-exit family produced coarse sampled candidates with:
- zero direct 3D LOS in the Rev.DF sample set;
- non-zero geometric throat.

This is the first architecture in the current sequence to reach the zero-LOS coarse gate.

No acoustic qualification is inferred.

Rev.DH independently rechecks a compact/high-throat coarse-pass candidate with:
- edge-biased source points close to vent boundaries;
- multiple source Z values;
- denser Y sampling;
- cavity targets extending close to the duct/exit region;
- seven target Z planes.

Promotion requires Rev.DH open rays = 0.

If Rev.DH fails, the coarse result is treated as sampling-dependent and the candidate is rejected or refined.

If Rev.DH passes, the next gate is a real CadQuery solid mapped to actual lower/upper left/right banks, followed by collision and fluid-connectivity audits.

Checks:
C1644 Rev.DF executed over 2592 cases.
C1645 at least one coarse zero-LOS/nonzero-throat candidate found.
C1646 first coarse zero-LOS architecture in current redesign sequence.
C1647 coarse pass not treated as acoustic qualification.
C1648 dense independent edge-biased recheck Rev.DH defined.
C1649 dense zero-open-ray result required before CAD promotion.
C1650 real-product mapping remains subsequent gate.

Status: **ACOUSTIC_REV_DI / TURNED_EXIT_COARSE_PASS / DENSE_RECHECK_EXECUTION_NEXT / C01_TO_C1650**.
