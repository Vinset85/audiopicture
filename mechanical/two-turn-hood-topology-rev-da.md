# AudioPicture V2.2 — two-turn hood topology Rev.DA

Status: **TWO_TURN_HOOD_PARAMETRIC_SWEEP_DEFINED / 162_CASES / 3D_LOS_GATE / EXECUTION_NEXT**

The Rev.CW independent-curtain family reduced direct LOS but did not eliminate it. Rev.CZ changes topology.

The candidate uses three geometric elements per flow bank:
1. a shell-side cheek descending from the ASA shell;
2. a deeper independent PC-CF-side hood displaced inward;
3. a short return lip intended to intercept diagonal Z shortcuts.

The shell and frame features remain mechanically independent.

Sweep:
- shell cheek H: 0.8 / 1.0 mm;
- frame hood top Z: 34.8 / 34.5 / 34.2 mm;
- frame hood depth: 1.5 / 2.0 / 2.5 mm;
- inward X shift: 0 / 2 / 4 mm;
- return lip: 1 / 2 / 3 mm.

Total: 162 combinations.

Promotion requires zero sampled straight 3D rays and positive shell/frame Z clearance. A zero-ray result is only a geometric LOS screening pass; it does not establish acoustic insertion loss.

Checks:
C1598 two-turn topology defined.
C1599 shell cheek defined.
C1600 independent deeper hood defined.
C1601 diagonal-blocking return lip defined.
C1602 162 combinations defined.
C1603 positive Z clearance required.
C1604 zero sampled 3D LOS required.
C1605 no acoustic attenuation claim.

Status: **ACOUSTIC_REV_DA / TWO_TURN_HOOD_SWEEP_EXECUTION_NEXT / C01_TO_C1605**.
