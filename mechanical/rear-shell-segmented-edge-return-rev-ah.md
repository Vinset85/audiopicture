# AudioPicture V2.2 — segmented ASA rear-shell edge architecture Rev.AH

Status: **SEGMENTED_EDGE_RETURN_EXECUTED_PASS / CONTINUOUS_RETURN_REJECTED / VENT_BANKS_PRESERVED**

## Decision
A continuous inward ASA perimeter return is rejected.

Reason:
- executed lower vents occupy lateral zones X4..14 over Y4..144;
- executed upper vents occupy lateral zones near X4..16 and X300..316 over Y341..396;
- the PC-CF structural outer ring already occupies the perimeter region;
- a continuous return would unnecessarily compete with airflow and structural packaging.

Selected architecture:
**segmented inward ASA edge return**.

## Executed Rev.AG kernel
Return:
- ASA wall 2.2 mm;
- global Z35.6..37.8;
- return depth 2.2 mm;
- rear panel remains Z37.8..40.0.

Segments:
- left middle: X0..2.2, Y148..337;
- right middle: X317.8..320, Y148..337;
- bottom middle: X18..302, Y0..2.2;
- top middle: X18..302, Y397.8..400.

Protected vent-bank regions contain zero return volume below the rear panel.

Coarse PC-CF frame intersection:
0 mm3.

Nominal Z gap from PC-CF coarse frame rear Z35.0 to ASA return front Z35.6:
0.6 mm.

This is a CAD seed, not a released manufacturing tolerance.

## Interpretation
The segmented return:
- preserves the 320 x 400 product XY envelope;
- preserves Z<=40;
- avoids creating a second continuous rigid perimeter ring;
- leaves lateral inlet/outlet banks unobstructed;
- provides shell edge closure/stiffening in non-vented regions;
- leaves retention features to be added locally.

## Checks
C1027 continuous ASA inward return assessed.
C1028 continuous return rejected due vent/PC-CF competition.
C1029 segmented return selected.
C1030 return wall 2.2 mm.
C1031 return Z35.6..37.8.
C1032 product rear Z40 unchanged.
C1033 left lower vent bank return intersection zero.
C1034 right lower vent bank return intersection zero.
C1035 left upper vent bank return intersection zero.
C1036 right upper vent bank return intersection zero.
C1037 coarse PC-CF intersection zero.
C1038 nominal coarse frame-to-return Z gap 0.6 mm.
C1039 0.6 mm not released as manufacturing tolerance.
C1040 retention remains local/open.
C1041 service recess remains open.
C1042 baffles remain open.

Status:
**REAR_SHELL_SEGMENTED_EDGE_RETURN / Z35P6_TO_37P8 / VENT_BANKS_OPEN / PC_CF_COARSE_CLEAR / C01_TO_C1042**.
