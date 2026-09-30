# AudioPicture V2.2 — planar vent labyrinth architecture Rev.BO

Status: **PLANAR_LABYRINTH_ARCHITECTURE_SELECTED / FULL_DEPTH_DUCT_REJECTED / BAFFLE_HEIGHT_SWEEP_DEFINED / CAD_INTEGRATION_NEXT**

## Constraint
The current nominal separation between PC-CF rear plane Z35 and rear-shell inner plane Z37.8 is only 2.8 mm.

A conventional deep rear duct or full-height transverse wall would consume or choke this gap and recreate the restriction removed by Rev.BK/BM.

## Selected architecture
Use shell-mounted thin ASA planar deflectors inside the free XY regions adjacent to each vent bank.

Each bank uses two staggered deflectors so the preferred flow path changes direction twice before entering/leaving the electronics cavity.

The deflectors:
- are bonded/printed as part of the ASA shell;
- do not form a structural bridge to PC-CF;
- do not touch the DML structure;
- do not span the complete nominal 2.8 mm shell/frame gap;
- leave a controlled Z bypass below the rib;
- are staggered in XY rather than stacked as a deep duct.

## Why full-depth walls are rejected
A full-depth wall approaching 2.8 mm would:
- create a severe tolerance-sensitive throat;
- risk hard contact with PC-CF;
- couple shell and structural frame;
- make natural-convection pressure loss strongly dependent on local warpage.

Therefore baffle height is a sweep variable, not a frozen dimension.

Initial engineering sweep:
0.8 / 1.0 / 1.2 / 1.4 mm inward from the shell inner plane.

Remaining nominal Z bypass:
2.0 / 1.8 / 1.6 / 1.4 mm respectively.

These are geometry-study values only.

## Functional requirement
The two deflectors shall block direct line-of-sight through the bank in plan view while retaining a broad lateral path.

Do not use foam or dense mesh as the baseline acoustic treatment.

## Bank-specific direction
Lower inlet:
rear/lower vent bank -> lateral turn -> staggered second turn -> electronics cavity.

Upper outlet:
electronics cavity -> staggered lateral turn -> second turn -> rear/upper vent bank -> wall gap.

Left/right banks remain symmetric unless later component/harness geometry requires otherwise.

## Release gates
Before freezing baffle geometry:
1. build exact shell-mounted baffle solids on Rev.BK;
2. verify one connected ASA shell solid;
3. verify no vent reclosure;
4. verify no seat/edge-return intersection;
5. verify no PC-CF contact at nominal CAD;
6. calculate minimum geometric throat for the selected rib height;
7. inspect service/harness/RF/radar keep-outs;
8. CFD remains mandatory for thermal performance;
9. acoustic prototype test remains mandatory for vent radiation/resonance.

## Checks
C1301 nominal shell/frame gap 2.8 mm recognized as dominant constraint.
C1302 conventional full-depth duct rejected.
C1303 planar staggered baffle architecture selected.
C1304 two XY direction changes targeted.
C1305 baffles shell-mounted, not frame-mounted.
C1306 no structural shell-to-PC-CF bridge permitted.
C1307 no DML hard bridge permitted.
C1308 baffle height remains a sweep variable.
C1309 height sweep 0.8/1.0/1.2/1.4 mm defined.
C1310 nominal remaining Z bypass 2.0/1.8/1.6/1.4 mm.
C1311 values are not production tolerances.
C1312 no dense foam/filter baseline.
C1313 left/right symmetry preferred.
C1314 exact CadQuery integration required next.
C1315 CFD remains authoritative for thermal flow.
C1316 acoustic prototype validation required.

Status:
**LABYRINTH_REV_BO / PLANAR_STAGGERED_TWO_TURN / HEIGHT_SWEEP_0P8_TO1P4 / CAD_NEXT / C01_TO_C1316**.
