# AudioPicture V2.2 — 3D labyrinth line-of-sight audit Rev.CU

Status: **3D_LOS_AUDIT_DEFINED / UNDER_BAFFLE_SHORT_CIRCUIT_TEST / EXECUTION_REQUIRED / NOT_ACOUSTIC_SIMULATION**

## Purpose
Test the unresolved weakness of the shell-only alternating-gate labyrinth.

The previous planar audit proved that the U15 topology blocks sampled straight paths in XY.

It did not test rays that change Z and pass below a partial-height shell baffle.

Rev.CT explicitly tests that path.

## Method
Sample straight 3D segments from points on the rear/external side of the promoted lower and upper vent banks to points in the internal cavity.

Cases:
- H0.8;
- H1.0.

Obstacles:
- eight alternating shell-side baffles;
- conservative coarse PC-CF perimeter/ring boxes;
- upper cleat-island boxes.

The frame representation is intentionally conservative because its keep-out cuts are not restored in this first ray model.

Therefore:
- an OPEN ray is strong evidence that complete 3D geometric LOS blocking has failed;
- zero sampled open rays would still not prove acoustic attenuation.

This is geometry, not wave acoustics.

## Decision rule
If any robust family of sampled rays passes from a vent bank to the cavity without intersecting baffle/frame solids:
- current H0.8/H1.0 shell-only topology is rejected as a complete 3D LOS blocker;
- it may remain a thermal-flow comparison geometry;
- do not call it an acoustically validated labyrinth.

## If rejected
Next topology shall be developed around one of:
1. offset shell/frame-side baffles with guaranteed no-contact clearance;
2. deeper shell-only hood/gate in a PC-CF-free corridor;
3. relocated vent/gate geometry into a deeper free cavity.

Any frame-side acoustic feature must not create a hard structural bridge to the DML and must preserve RF/thermal constraints.

## Checks
C1554 3D LOS audit script Rev.CT defined.
C1555 H0.8 included.
C1556 H1.0 included.
C1557 lower left/right banks included.
C1558 upper left/right banks included.
C1559 shell baffles included as 3D obstacles.
C1560 coarse PC-CF perimeter included as conservative obstacle.
C1561 under-baffle destination Z samples included.
C1562 OPEN-ray criterion explicitly rejects complete LOS blocking.
C1563 zero sampled rays does not equal acoustic attenuation proof.
C1564 no acoustic simulation claimed.

Status:
**ACOUSTIC_REV_CU / 3D_LOS_EXECUTION_NEXT / C01_TO_C1564**.
