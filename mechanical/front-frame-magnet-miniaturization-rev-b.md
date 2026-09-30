# AudioPicture V2.2 Rev.B — miniaturized front-frame magnetic retention

Status: **4X2MM_N45_SELECTED_AS_NEW_BASELINE / POCKET_4P4MM / PAD_7MM_MAX_SEED / DML_PERIMETER_CONFLICT_REDUCED**

## 1. Reason for revision
The previous 6 x 2 mm magnet required a 6.6 mm pocket and approximately 12 mm local carrier pad. In the 10 mm product-to-DML perimeter band this was geometrically inefficient.

The design objective is therefore changed:
**minimize the complete pocket/pad footprint, not merely relocate the previous magnet.**

## 2. New primary candidate
Primary candidate:
Supermagnete S-04-02-N class
- NdFeB
- N45
- diameter 4 mm
- thickness 2 mm
- axial magnetization
- manufacturer table attraction approximately 420 g (~4.12 N) under manufacturer test conditions.

The exact manufacturer product page/datasheet remains the sourcing authority.

## 3. Thin alternative
Alternative:
S-04-01-N
- N45
- diameter 4 mm
- thickness 1 mm
- attraction approximately 250 g (~2.45 N)
- mass approximately 0.096 g
- max operating temperature 80 C.

This is retained if Z thickness becomes more important than normal-force margin.

## 4. Selection logic
Eight S-04-02-N-class stations have an ideal catalogue-force sum around 33 N before assembled-gap losses.

This is much closer to the required 20..30 N assembled system than the previous 6 x 2 mm solution.

The design still does not equate catalogue pull force to assembled retention.

## 5. New pocket
Nominal CAD pocket:
**diameter 4.4 mm**

Process sweep:
4.3 / 4.4 / 4.5 mm.

Pocket depth:
2.15..2.25 mm depending print/process compensation.

This replaces the previous 6.6 mm diameter pocket.

Pocket diameter reduction:
approximately 33%.

Pocket projected area reduction:
from pi*(3.3)^2 to pi*(2.2)^2,
approximately **56% less area**.

## 6. New local pad
Previous:
12 mm circular pad.

New baseline:
**7.0 mm maximum transverse envelope**.

Preferred D-shaped pad:
- outward/perimeter side radius/envelope <=3.5 mm from magnet center;
- DML-facing wall minimized;
- local minimum polymer ligament around pocket 1.2..1.5 mm where mechanically legal.

Optimization target:
6.5 mm pad envelope.

7.0 mm is the first robust CAD seed.

## 7. Pad-area reduction
Equivalent circular comparison:
12 mm -> 7 mm.

Projected pad area ratio:
49/144 ~=0.34.

Thus the new pad occupies about **34%** of the old projected area, a reduction of about **66%**.

## 8. Magnet station centers
Rev.B perimeter centers remain first seed:
M1B (70,388)
M2B (250,388)
M3B (70,12)
M4B (250,12)
M5B (12,135)
M6B (12,275)
M7B (308,135)
M8B (308,315).

With a 7 mm pad, inward reach from a center 12 mm from product edge is approximately 15.5 mm global coordinate on left/bottom cases.

DML starts at 10 mm, so a symmetric pad still overlaps DML projection.

Therefore the pad MUST be asymmetric and/or center moved further outward; miniaturization alone does not justify a false PASS.

## 9. Perimeter-oriented pocket architecture
Preferred geometry:
- magnet center near product perimeter;
- pocket floor integrated into front carrier edge section;
- structural material biased outward;
- only a narrow bridge/ligament on DML-facing side.

The magnet itself may geometrically project over the DML XY rectangle only if Z separation proves there is no hard collision and acoustic/perimeter compliance is not disturbed.

Baseline preference remains:
no rigid magnetic station over active/compliant DML region.

## 10. Candidate center sweep
For top/bottom:
edge offset sweep = 4.5 / 5.0 / 5.5 mm from carrier edge.

For left/right:
same.

Example nominal centers:
top Y=394 mm class;
bottom Y=6 mm class;
left X=6 mm class;
right X=314 mm class.

Exact centers must respect the 318.4 x 398.4 carrier boundary and fabric bonding land.

This is intentionally more perimeter-biased than Rev.B center=12 mm.

## 11. Carrier integration
The 10 mm carrier ring can house a 4.4 mm pocket much more naturally.

The pocket no longer requires a 12 mm boss wider than the nominal ring.

Local 6.5..7.0 mm station geometry can remain within the 10 mm ring in the transverse direction, subject to capture-lip detail.

This is the principal mechanical advantage.

## 12. Z strategy
Keep magnet thickness 2 mm baseline.

Do not increase total front stack.

Local carrier thickening is allowed only toward a legal perimeter cavity.

If a 2 mm magnet cannot be mechanically captured without violating global Z, switch to S-04-01-N and increase station count rather than increasing front thickness.

## 13. Retention strategy
Baseline:
8 x 4x2 mm N45 class.

Target assembled total:
20..30 N.

Tune with:
- steel target area/thickness;
- effective gap;
- pocket floor;
- optional polymer shim.

If assembled retention falls below 20 N:
first evaluate 10 stations before increasing magnet diameter.

This preserves the small-pocket architecture.

## 14. Ten-station fallback
The carrier architecture shall support a 10-station variant.

Additional stations are preferable to returning to 6 mm magnets if:
- RF masks permit;
- peel behavior remains acceptable;
- local targets remain discrete.

## 15. Target miniaturization
Target should also shrink with the magnet.

Initial target seed:
- 6..8 mm class discrete steel tab/disc;
- 0.8..1.0 mm thickness sensitivity.

Do not retain the previous 10 mm target by default.

Exact magnetic-circuit FEA/test determines target saturation adequacy.

## 16. Automatic checks
C431 primary magnet diameter <=4.0 mm.
C432 primary magnet thickness <=2.0 mm.
C433 nominal pocket diameter <=4.4 mm.
C434 pocket projected area reduced >50% vs previous 6.6 mm pocket.
C435 local pad transverse envelope <=7.0 mm baseline.
C436 pad projected area reduced >60% vs old 12 mm circular seed.
C437 local pad can fit inside nominal 10 mm carrier-ring width.
C438 no return to 6 mm magnet without failed 8/10-station 4 mm study.
C439 8-station assembled target remains 20..30 N.
C440 catalogue-force sum not treated as assembled proof.
C441 10-station fallback supported.
C442 target size reduced to 6..8 mm class seed.
C443 station centers move toward carrier perimeter.
C444 fabric bonding land remains manufacturable around stations.
C445 mechanical capture remains required.
C446 exact DML collision check required on new asymmetric pad.
C447 RF masks remain authoritative.
C448 thin 4x1 mm alternative retained for Z contingency.
C449 no increase in total product depth permitted for magnetic retention.
C450 revised carrier B-rep required before release.

## 17. State
Old baseline:
6 x 2 mm magnet / 6.6 mm pocket / 12 mm pad.

New baseline:
**4 x 2 mm N45 / 4.4 mm pocket / 6.5..7.0 mm asymmetric pad**.

Reduction:
- pocket area ~56%;
- pad area ~66% equivalent;
- ring integration substantially improved.

Status:
**MAGNET_MINIATURIZED_TO_4X2 / POCKET_4P4 / PAD_LE_7 / 8_STATION_BASELINE_10_STATION_FALLBACK / C01_TO_C450 / NEW_BREP_COLLISION_AUDIT_NEXT**.
