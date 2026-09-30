# AudioPicture V2.2 — offset-Z labyrinth sweep execution Rev.CY

Status: **72_CASE_OFFSET_Z_SWEEP_EXECUTED / ZERO_LOS_NOT_ACHIEVED / CURTAIN_TOPOLOGY_REJECTED / TWO_TURN_HOOD_NEXT**

## Execution
Rev.CW was actually executed over all 72 defined combinations.

Variables:
- shell baffle H = 0.8 / 1.0 mm;
- frame curtain top Z = 35.0 / 34.8 / 34.5 mm;
- frame curtain depth = 1.0 / 1.5 / 2.0 mm;
- inward X shift = 0 / 2 / 4 / 6 mm.

All tested combinations retain positive shell/frame Z separation by construction for the evaluated parameter set.

## Result
No tested configuration achieved zero sampled 3D line of sight.

The best family remains around 1.18k open rays out of 15,552 sampled rays, substantially below the approximately 4.1k open rays of the shell-only architecture but still a clear complete-LOS failure.

Therefore the offset independent-curtain idea improves geometric shielding but does not close the full 3D direct-path cone.

## Decision
Do not promote any Rev.CW combination as a complete 3D LOS blocker.

Do not attempt to solve the remaining failure merely by increasing curtain depth or shell-baffle height inside the same topology.

The residual failure is treated as topological.

## Next architecture
Proceed to a two-turn hood/channel concept:
- shell-side entry hood or cheek;
- independent deeper guide/hood in a PC-CF-free corridor;
- two staggered direction changes in the air path;
- positive shell/frame clearance throughout;
- no rigid bridge to DML support structure;
- controlled minimum throat retained for thermal flow.

The next geometry must first pass deterministic 3D LOS before any acoustic attenuation study.

## Checks
C1588 Rev.CW executed.
C1589 all 72 combinations evaluated.
C1590 zero-open-ray candidates = 0.
C1591 offset curtain improves LOS count but does not close it.
C1592 no Rev.CW candidate promoted.
C1593 residual failure classified as topological.
C1594 blind height/depth increase rejected.
C1595 two-turn hood/channel selected as next architecture.
C1596 shell-frame mechanical independence remains mandatory.
C1597 no acoustic attenuation result claimed.

Status:
**ACOUSTIC_REV_CY / OFFSET_CURTAIN_SWEEP_FAIL / TWO_TURN_HOOD_CHANNEL_NEXT / C01_TO_C1597**.
