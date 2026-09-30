# AudioPicture V2.2 Rev.B — front carrier magnetic-pad resolution

Status: **DML_OVERLAP_RESOLVED_BY_PERIMETER_BIASED_STATIONS / REV_B_CAD_CONTRACT_FROZEN / REAL_KERNEL_REGEN_REQUIRED**

## 1. Problem
Rev.A used 12 mm circular magnetic station pads centered close to the DML projected perimeter.

DML projection:
X=10..310
Y=10..390 mm.

The Rev.A circular pads intruded into the DML projected area.

The DML shall not be notched as the baseline solution.

## 2. Rev.B station centers
Use:
M1B=(70,388)
M2B=(250,388)
M3B=(70,12)
M4B=(250,12)
M5B=(12,135)
M6B=(12,275)
M7B=(308,135)
M8B=(308,315).

## 3. Design principle
A conventional circular pad cannot both:
- surround a 6.6 mm magnet pocket with adequate polymer;
- and remain entirely outside a DML projection only 10 mm from the product perimeter.

Therefore the Rev.B station is not a symmetric circular boss.

It is a perimeter-biased pocket integrated into the existing 10 mm carrier ring.

The carrier ring itself is the structural material around the magnet.

No additional DML-facing circular overhang is permitted.

## 4. Pocket family
Magnet pocket:
- diameter 6.6 mm nominal;
- Candidate A 6 x 2 mm magnet;
- process compensation open.

Minimum polymer web around pocket where geometry permits:
- 1.5 mm seed;
- 1.2 mm absolute diagnostic minimum pending print coupon.

The outer-side web may be larger than DML-side web.

## 5. Top stations
M1B/M2B:
center Y=388.

DML top edge:
Y=390.

The station is integrated into the top perimeter carrier.

No added pad extends below Y=390.

Local reinforcement grows toward +Y/product perimeter.

DML-facing boundary:
Y>=390 for any reinforcement beyond the normal carrier geometry.

## 6. Bottom stations
M3B/M4B:
center Y=12.

DML bottom edge:
Y=10.

Reinforcement grows toward -Y/product perimeter.

No added pad extends above Y=10 into DML projected area.

## 7. Left stations
M5B/M6B:
center X=12.

DML left edge:
X=10.

Reinforcement grows toward -X/product perimeter.

No added pad extends right of X=10 as an added boss into DML projected area.

## 8. Right stations
M7B/M8B:
center X=308.

DML right edge:
X=310.

Reinforcement grows toward +X/product perimeter.

No added pad extends left of X=310 as an added boss into DML projected area.

## 9. Important geometric interpretation
The 10 mm perimeter carrier ring already occupies the edge region required to tension the fabric.

The DML overlap check therefore distinguishes:
A. baseline perimeter carrier geometry;
B. additional magnet-station rear intrusion.

The hard rule is:
**no additional rearward magnet-station intrusion over the DML active/hard-clearance projection.**

This avoids falsely treating the required fabric carrier ring as a DML collision while still preventing thick magnetic bosses from occupying DML clearance.

## 10. Local Z
Base carrier:
1.8 mm.

Magnet station local rear thickness:
3.2 mm seed.

The additional 1.4 mm rear thickening is allowed only on the perimeter-facing side outside DML hard clearance.

The DML-facing part of the station remains at base carrier thickness or is relieved as required.

## 11. D-shaped reinforcement
Parametric station reinforcement uses:
- pocket-centered circular/rounded local shape;
- boolean clip by DML hard-clearance half-plane;
- union with perimeter ring;
- fillet at transition.

This produces a D/segment-shaped rear thickening rather than a full circular boss.

## 12. Capture consequence
Because the rear boss is clipped, magnet mechanical capture cannot rely on a full symmetric printed cap.

Preferred Rev.B capture:
- front-side pocket floor;
- perimeter-side printed retaining shoulder;
- thin nonmagnetic polymer service cap/bridge on rear;
- adhesive secondary.

The cap must remain outside DML rear-clearance projection where it adds Z.

## 13. Strength
Local magnet force target per station:
2.5..3.75 N average assembled.

This is small relative to the gross structural capacity of the perimeter ring, but local peel stress at the clipped pocket must be checked.

Qualification:
- 15 N single-station pull proof seed;
- 10 N local peel seed;
- repeated removal cycling.

These are qualification seeds, not production certification values.

## 14. Locator interaction
LOC_A/LOC_B remain separate from magnet stations.

No locator shall be merged into a magnetic pocket unless later FEA/print testing demonstrates benefit.

## 15. Front removal
Lower-center peel recess remains X160, width28, depth4.

M3B/M4B remain far from peel center.

Sequential release remains expected.

## 16. RF
Station coordinates remain subject to exact:
- radar mask;
- ESP32 antenna mask;
- mic acoustic exclusions;
- OPT3004 optical exclusion.

DML geometric resolution does not override RF exclusions.

## 17. CAD regeneration algorithm
1. generate 318.4 x 398.4 carrier ring;
2. generate magnet pocket centers Rev.B;
3. generate local reinforcement;
4. clip added rear reinforcement against DML hard-clearance half-plane;
5. union reinforcement to ring;
6. cut 6.6 mm pocket;
7. generate capture shoulder;
8. cut peel recess;
9. apply edge fillets;
10. validate one solid;
11. measure volume/mass;
12. transform to global Z;
13. run DML rear-intrusion collision check.

## 18. Acceptance
PASS if:
- one connected valid solid;
- all 8 pockets present;
- no added 3.2 mm rear boss overlaps DML hard projection;
- magnet pocket retains printable web;
- peel recess preserves connectivity;
- mass <=60 g carrier budget;
- local station capture geometry is manufacturable.

## 19. Automatic checks
C431 Rev.B station centers used.
C432 DML hard projection explicit.
C433 DML notch prohibited baseline.
C434 added top reinforcement does not enter below Y390.
C435 added bottom reinforcement does not enter above Y10.
C436 added left reinforcement does not enter right of X10.
C437 added right reinforcement does not enter left of X310.
C438 base carrier ring distinguished from added rear boss.
C439 rear thickening clipped by DML half-plane.
C440 magnet pocket diameter 6.6 mm retained.
C441 printable pocket web checked.
C442 clipped station remains connected to ring.
C443 mechanical capture adapted to asymmetric station.
C444 adhesive remains secondary retention.
C445 peel recess retained.
C446 LOC_A/B remain independent.
C447 RF masks remain higher-priority gates.
C448 one-solid kernel validation required.
C449 carrier mass recomputed after regeneration.
C450 global-Z DML collision check required.

## 20. State
Rev.B resolves the design error in Rev.A:
a symmetric 12 mm rear boss is no longer used at the DML edge.

Instead:
**the existing perimeter ring carries the magnet pocket and only the additional rear thickening is biased outward and clipped away from DML clearance.**

Status:
**REV_B_PERIMETER_BIASED_MAGNET_POCKETS / D_SHAPED_REAR_THICKENING / DML_NOTCH_REJECTED / C01_TO_C450 / REAL_BREP_REGEN_NEXT**.
