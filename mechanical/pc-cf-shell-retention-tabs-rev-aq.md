# AudioPicture V2.2 — PC-CF shell-retention tab B-rep Rev.AQ

Status: **TOP_RETENTION_TABS_BREP_PASS / ONE_SOLID / PACKAGING_CLEAR / LOCAL_FEA_AND_FASTENER_OPEN**

## Executed source
mechanical/cad/generate_rear_frame_retention_rev_ap.py

The Rev.C PC-CF frame was rebuilt with the two Rev.AO top shell-retention tabs.

Tab seeds:
- left X139..151 / Y378..390;
- right X169..181 / Y378..390;
- structural Z27..35.

## Kernel result
- valid B-rep: PASS;
- connected solid count: 1;
- existing frame and both tabs are fused;
- each tab overlaps the existing top ring by 192 mm3;
- net PC-CF volume added by the two tabs: 1920 mm3.

Mass sensitivity for the added material only:
- density 1.20 g/cm3: ~2.30 g;
- density 1.30 g/cm3: ~2.50 g;
- density 1.40 g/cm3: ~2.69 g.

These are density sensitivities, not a released material mass claim.

## Packaging checks
Executed tab intersections:
- upper vent exclusions: 0 mm3;
- wall-cleat island exclusions: 0 mm3;
- MAIN-C: 0 mm3;
- coarse ESP32 RF mask: 0 mm3.

The frame remains inside the existing structural Z27..35 band.

STEP export:
AP22_REAR_PC_CF_FRAME_RETENTION_REV_AP.step

## Structural interpretation
The two tabs are now proven as real connected CAD features, not just projected rectangles.

This does NOT yet prove retention strength.

Before production release:
- select fastener/insert family;
- add boss/seat geometry;
- preserve shell removability;
- run local retention load cases;
- verify exact transformed RF/radar masks and final frame;
- verify printed PC-CF coupon/process properties.

## Next design gate
The six-point architecture can now progress to the shell-side interface.

Do not drill generic holes yet.

First define a parametric local ASA seat/pad at each of the six retention nodes with:
- sufficient land for a future fastener family;
- no vent-area reduction;
- no broad hard shell/frame contact;
- controlled local Z contact only;
- compatibility with shell removal.

Then select fastener/insert dimensions against the resulting stack.

## Checks
C1101 Rev.C frame rebuilt with top retention tabs.
C1102 left top tab fused to existing frame.
C1103 right top tab fused to existing frame.
C1104 resulting frame valid.
C1105 resulting frame one connected solid.
C1106 each top tab/frame overlap 192 mm3.
C1107 net tab volume delta 1920 mm3.
C1108 added-mass sensitivity recorded without material-release claim.
C1109 upper vent intersection zero.
C1110 cleat island intersection zero.
C1111 MAIN-C intersection zero.
C1112 coarse ESP32 RF-mask intersection zero.
C1113 frame Z27..35 preserved.
C1114 STEP export generated.
C1115 local retention FEA not claimed.
C1116 fastener/insert remains open.
C1117 exact RF/radar release remains open.
C1118 shell-side six-node seat geometry is next gate.

Status:
**PC_CF_RETENTION_REV_AQ / TWO_TOP_TABS_FUSED / ONE_SOLID / +1920MM3 / PACKAGING_PASS / SHELL_SEATS_NEXT / C01_TO_C1118**.
