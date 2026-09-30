# AudioPicture V2.2 — covered lateral duct sweep execution Rev.DE

Status: **288_CASE_COVERED_DUCT_SWEEP_EXECUTED / ZERO_LOS_NOT_ACHIEVED / SIDE_EXIT_NEEDS_TURN / ELBOW_TERMINATION_NEXT**

## Execution
Rev.DC was executed over all 288 normalized covered-lateral-duct combinations.

Parameters:
- lateral length 28 / 36 / 44 / 52 mm;
- width 36 / 48 / 60 mm;
- roof lower Z 36.2 / 36.5 / 36.8 mm;
- wall thickness 1.0 / 1.2 mm;
- Y shift 0 / 8 / 16 mm.

## Result
Zero sampled-LOS candidates: **0**.

The best region retains approximately 2,486 open rays out of 32,400 sampled rays, approximately 7.7%.

This is a substantial geometric reduction relative to an unshielded/direct topology, but it fails the required complete sampled-LOS criterion.

## Interpretation
The roof blocks much of the direct rearward cone.

The residual rays predominantly exploit visibility through the lateral discharge.

Increasing duct length alone is therefore not selected as the next move.

## Next topology
Add an elbow/turned termination at the internal discharge:
- retain covered lateral collection duct;
- turn the final discharge so its opening faces a blocking wall/cheek rather than the external vent projection;
- preserve a finite discharge throat;
- keep the roof and termination mechanically independent from any opposing structural surface;
- re-run 3D LOS before real-solid promotion.

This changes exit orientation rather than simply adding length/material.

## Checks
C1624 Rev.DC executed.
C1625 all 288 combinations evaluated.
C1626 zero sampled-LOS candidates = 0.
C1627 best region approximately 2486/32400 open rays.
C1628 covered roof materially reduces but does not eliminate direct LOS.
C1629 residual path associated with lateral discharge visibility.
C1630 further pure-length sweep rejected.
C1631 elbow/turned side-exit selected next.
C1632 nonzero thermal throat remains mandatory.
C1633 no CFD/acoustic attenuation result claimed.

Status:
**ACOUSTIC_REV_DE / COVERED_DUCT_LOS_FAIL / TURNED_SIDE_EXIT_NEXT / C01_TO_C1633**.
