# AudioPicture V2.2 — system packaging compatibility freeze Rev.A

Status: **MECHANICAL_PACKAGING_SOLUTION_COMPATIBLE / 320X400X40_PRESERVED / PRODUCTION_VALIDATION_GATES_EXPLICIT**

## 1. Scope
This document freezes the current compatible mechanical packaging solution after resolving the front-frame/DML conflict and reconciling the global Z datum.

It does not claim that supplier STEP, RF, acoustic, thermal or structural qualification has already been physically performed.

## 2. Product envelope
External target:
**320 x 400 x 40 mm maximum**.

Current nominal rear shell outer plane:
Z40.0 mm.

PASS nominal.

## 3. Authoritative global front stack
Fabric:
Z0.0..0.5.

Nominal fabric/DML air gap:
0.5..3.3 = 2.8 mm.

DML:
Z3.3..9.3.

EX25FHE2 conservative:
Z9.3..35.3.

Preferred rigid rear clearance:
to Z36.3.

Rear shell inner:
Z37.8.

Rear shell outer:
Z40.0.

Governing nominal residual:
**1.5 mm**.

## 4. Front frame
Rev.C carrier:
318.4 x 398.4 mm.
10 mm perimeter architecture.
1.8 mm base.
3.2 mm only at local perimeter magnetic stations.
Real B-rep:
25.356 cm3.
ASA carrier-only mass:
~26.6..27.9 g.

## 5. DML compatibility
DML:
300 x 380 mm at X10..310/Y10..390.

Rev.C magnetic pads:
all outside projected DML rectangle.

Nominal projected pad-to-DML gap:
0.6 mm.

No DML notch/reduction.

PASS nominal geometry.

## 6. Magnetic architecture
Eight 6 x 2 mm class magnet stations.
Narrow 8 x 12 mm carrier station.
8 x 10 x 0.8 mm steel-target seed.
No continuous steel ring.

Total assembled target:
20..30 N.

Final force stack is selected by coupon measurement; catalogue force is not release evidence.

## 7. ESP32 RF compatibility
ESP32-S3-WROOM-1 is assigned to MAIN-C left edge with antenna facing -X/perimeter.

Generate a conservative enclosure RF mask expanded at least 15 mm around the exact antenna region following Espressif enclosure guidance.

Current Rev.C magnet seeds do not enter the coarse mask.

PC-CF and metal are prohibited from the exact mask.

## 8. Radar compatibility
Radar:
X249..287/Y184..216 seed.

Rev.C right magnets:
(314.6,135) and (314.6,315).

No current coarse overlap with radar board or 45-degree forward packaging cone.

Exact antenna/radome EM result remains authoritative.

## 9. VOICE compatibility
VOICE:
X119..201/Y20..102.

Bottom magnets:
(70,5.4),(250,5.4).

No coarse XY overlap.

VOICE Z remains functional sweep 12.5/13.0/13.5 mm front-board candidates, to be chosen by mic acoustic/isolation optimization.

## 10. ENV compatibility
ENV:
X252..294/Y35..59.

Nearest bottom/right magnetic stations remain outside the board envelope.

SHT45 chamber and OPT3004 optical path remain independent front-system features.

## 11. MAIN-C / MAIN-P
MAIN-C:
Z17..18.6 board, tall Ag53024 coarse rear clearance >4 mm class.

MAIN-P:
Z18..19.6 board, horizontal 470 uF top ~Z31.6 class, rear residual ~6.2 mm.

Neither governs 40 mm depth.

## 12. PC-CF frame
Real primary frame remains one valid B-rep from prior generation.

Assembly placement:
sparse legal structural regions approximately Z27..35.

Hard exclusions:
- EX25 columns;
- radar forward RF volume;
- ESP32 antenna RF mask;
- VOICE isolation;
- ENV thermal isolation.

The frame is routed around these volumes.

## 13. Harness
FPC:
Z14..18 corridor.

Power:
Z20..26.

Speaker:
Z20..28.

RJ45/cable:
Z22..36 only where XY legal.

No cable enters EX25 rear clearance Z35.3..36.3 at exciter columns.

## 14. Rear shell
ASA 2.2 mm nominal.
Inner Z37.8.
Outer Z40.

Rev.B vent geometry retained:
1440 mm2 gross inlet;
1350 mm2 gross outlet.

Shell remains removable.

## 15. Wall mount
Two upper aluminum cleats + two lower supports + M4 anti-lift retained.

No full rear metal plate.

RF masks override cleat/metal placement.

## 16. Collision result
Current parametric/real-B-rep packaging:
- front carrier vs DML: PASS
- front magnets vs DML: PASS
- front magnets vs VOICE: PASS coarse
- front magnets vs ENV: PASS coarse
- front magnets vs RADAR: PASS coarse
- front magnets vs ESP32 coarse 15 mm RF mask: PASS
- EX25 vs rear shell: PASS nominal, tight
- MAIN-C vs rear shell: PASS coarse
- MAIN-P vs rear shell: PASS coarse
- harness architecture vs hard columns: PASS by routing rule.

## 17. Remaining release gates
These are validation gates, not unresolved architecture:
1. exact EX25FHE2 STEP collision/tolerance;
2. exact ESP32 module STEP and enclosure RF test;
3. radar EM/radome validation;
4. magnetic force coupon;
5. selected printed-fabric acoustic/optical/RF characterization;
6. full DML FEA/acoustic solve;
7. structural LC1..LC7 solver run;
8. rear-chimney CFD;
9. ASA/PC-CF print-process coupons/warp;
10. exact tall-component STEP collision audit.

A full product prototype is not required by this architecture, but component/subassembly qualification remains required.

## 18. Freeze policy
The mechanical packaging architecture is now frozen unless a validation gate fails.

Do not change:
- 320 x 400 x 40 envelope;
- DML 300 x 380 baseline;
- global Z datum;
- Rev.C narrow magnetic perimeter architecture;
- two-board MAIN architecture;
- sparse PC-CF frame;
- passive rear ventilation;
- two-cleat wall mount
without a documented failed gate.

## 19. Checks
C471 external envelope preserved.
C472 global Z stack coherent.
C473 governing 1.5 mm rear margin positive.
C474 Rev.C front carrier valid one-solid B-rep.
C475 magnet/DML collision count zero.
C476 DML remains unnotched.
C477 ESP32 antenna position defined.
C478 coarse ESP32 magnet conflict count zero.
C479 coarse radar magnet conflict count zero.
C480 VOICE magnet conflict count zero.
C481 ENV magnet conflict count zero.
C482 MAIN-C depth non-governing.
C483 MAIN-P depth non-governing.
C484 harness excluded from exciter rear-clearance region.
C485 rear shell remains <=Z40.
C486 wall-mount architecture preserved.
C487 validation gates explicitly separated from architecture.
C488 no fabricated FEM/CFD/RF/acoustic result used.
C489 no full-product prototype assumed.
C490 architecture changes require failed validation gate.

## 20. State
The current mechanical packaging solution is internally compatible at the available CAD/envelope resolution.

Status:
**PACKAGING_ARCHITECTURE_FROZEN / 320X400X40 / ZERO_FRONT_MAGNET_DML_COLLISIONS / 1P5MM_GOVERNING_Z_MARGIN / C01_TO_C490 / VALIDATION_PHASE_NEXT**.
