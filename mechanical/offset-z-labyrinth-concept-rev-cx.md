# AudioPicture V2.2 — offset-Z labyrinth concept sweep Rev.CX

Status: **OFFSET_Z_CONCEPT_DEFINED / SHELL_FRAME_NO_CONTACT_REQUIRED / PARAMETRIC_3D_LOS_SWEEP / EXECUTION_NEXT**

## Objective
Replace the failed shell-only H0.8/H1.0 complete-LOS concept without creating a rigid ASA-shell to PC-CF bridge.

## Architecture
Retain the existing shell-side alternating gates as the first obstruction.

Add a second set of independent frame-side curtains:
- mechanically attached to the PC-CF side only;
- positioned farther inward in X;
- opposite/staggered gate sense in Y;
- ending below the shell-side gates with positive Z clearance.

The air path therefore remains open through an offset throat while a straight 3D path is challenged by two separated obstacle planes.

## Sweep variables
Rev.CW screens:
- shell baffle H = 0.8 / 1.0 mm;
- frame-curtain top Z = 35.0 / 34.8 / 34.5 mm;
- frame-curtain depth = 1.0 / 1.5 / 2.0 mm;
- inward X shift = 0 / 2 / 4 / 6 mm.

Total combinations: 72.

## Mechanical isolation rule
No candidate may contact the shell baffle.

Z clearance is explicitly computed as:
(shell-baffle lower Z) - (frame-curtain upper Z).

A geometric LOS pass with zero/negative clearance is invalid even if rays are blocked.

## Decision rule
Promote only candidates with:
- positive shell/frame Z clearance;
- zero sampled straight 3D rays in the Rev.CW audit;
- retained fluid throat;
- no new DML hard bridge.

A zero-ray result remains a geometric screening result only. It is not an acoustic attenuation measurement or simulation.

## Checks
C1578 offset-Z architecture defined.
C1579 frame-side curtain mechanically independent from shell.
C1580 72-case parametric sweep defined.
C1581 shell H0.8/H1.0 included.
C1582 frame top-Z sweep defined.
C1583 frame curtain depth sweep defined.
C1584 inward X shift sweep defined.
C1585 positive Z-clearance rule required.
C1586 zero sampled 3D LOS required for promotion.
C1587 no acoustic attenuation claim.

Status:
**ACOUSTIC_REV_CX / OFFSET_Z_SWEEP_EXECUTION_NEXT / C01_TO_C1587**.
