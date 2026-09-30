# AudioPicture V2.2 Rev.B — front carrier with perimeter-clipped magnetic pads

Status: **MAGNET_PAD_DML_OVERLAP_RESOLVED_BY_CONSTRUCTION / REV_B_CAD_CONTRACT / REAL_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A magnetic-pad overlap with the DML projected perimeter without modifying or notching the DML.

## 2. Authoritative projected regions
Product:
X=0..320
Y=0..400 mm.

DML:
X=10..310
Y=10..390 mm.

The DML projected rectangle is a hard front-carrier magnet-pad exclusion region.

No magnetic pad, target or mechanical capture feature may cross into this rectangle unless a later exact DML edge model explicitly creates a legal non-active region.

Baseline assumes no such exception.

## 3. Rev.B magnet centers
M1B=(70,388)
M2B=(250,388)
M3B=(70,12)
M4B=(250,12)
M5B=(12,135)
M6B=(12,275)
M7B=(308,135)
M8B=(308,315).

These centers alone do not prove legality because several centers still lie inside the DML projected rectangle.

Therefore pad legality is defined by boolean clipping, not center position.

## 4. Perimeter legal bands
Define four carrier-side legal bands outside DML projection:

TOP_BAND:
Y>=390 mm.

BOTTOM_BAND:
Y<=10 mm.

LEFT_BAND:
X<=10 mm.

RIGHT_BAND:
X>=310 mm.

Magnetic structural pad material must remain within the corresponding legal band plus the existing carrier ring material.

## 5. D-shaped pad construction
Start from local circular station support envelope:
D_PAD_SEED=12 mm.

For each station:
PAD_LEGAL = PAD_CIRCLE intersect PERIMETER_LEGAL_BAND intersect CARRIER_STRUCTURAL_DOMAIN.

This produces a D-shaped or segment-shaped local reinforcement.

The DML-facing side is planar/clipped at the DML projected boundary.

## 6. Magnet pocket implication
A 6.6 mm circular magnet pocket cannot be centered at a point that leaves insufficient material outside the DML boundary.

Therefore the Rev.B center seeds are provisional for pocket centers.

Minimum radial material around pocket:
1.5 mm seed where mechanically captured.

Required full local width:
6.6 + 2x1.5 = 9.6 mm.

The nominal legal perimeter strip from product edge to DML edge is only 10 mm.

This means a full 9.6 mm pocket-support feature can fit only with tight edge allocation and cannot use the old center locations blindly.

## 7. Revised pocket center rule
For top/bottom stations:
pocket center Y must be outside DML projection by at least:
R_MAG + WALL_MIN = 3.3 + 1.5 = 4.8 mm.

Thus:
TOP pocket center Y >=394.8 mm.
BOTTOM pocket center Y <=5.2 mm.

For left/right:
LEFT X<=5.2 mm.
RIGHT X>=314.8 mm.

These locations are extremely close to the product edge and conflict with practical carrier edge/wrap geometry.

Conclusion:
**a fully enclosed 6.6 mm cylindrical pocket cannot be robustly packaged in the 10 mm perimeter strip using the current architecture.**

## 8. Architecture correction
Do not force a fragile edge pocket.

Preferred Rev.B:
move the magnet itself to the product-side/rear structural perimeter and place only a thin discrete ferromagnetic target in the removable front carrier.

This is Option B from the original magnetic architecture study.

Benefits:
- front carrier target can be thin 0.8..1.0 mm;
- no 2 mm magnet pocket/thick boss on the front carrier;
- much easier DML-edge clearance;
- lower removable-front mass;
- simpler fabric carrier;
- magnet can be positively captured in the fixed product structure.

## 9. Front target geometry
Use discrete steel target tab in front carrier:
seed:
- 8 x 12 mm rounded rectangle or D-shaped tab;
- thickness 0.8 mm seed;
- locally mechanically trapped.

Target lies only in carrier perimeter legal band.

Its DML-facing edge is clipped at DML projection boundary.

No continuous steel ring.

## 10. Fixed-side magnet
6 x 2 mm class magnet moves to fixed product-side perimeter feature.

It may use the PC-CF/rear structural system or a dedicated non-RF fixed polymer capture feature.

Requirements:
- exact opposing alignment with front target;
- no DML preload;
- no radar/ESP32 keep-out violation;
- mechanically captured if adhesive fails;
- magnetic gap remains tunable.

## 11. Station coordinates become interface coordinates
Keep station tangential positions:
top X=70/250
bottom X=70/250
left Y=135/275
right Y=135/315.

Normal-axis coordinate is solved by edge-interface CAD rather than the old center seed.

Thus station IDs remain stable while exact magnet/target centers shift across the edge section.

## 12. Front carrier simplification
Remove eight 3.2 mm magnet bosses from removable carrier.

Return front carrier base to:
- 1.8 mm nominal ring;
- local thin target traps only.

This improves:
- front Z stack;
- warp symmetry;
- DML clearance;
- mass;
- printability.

## 13. Expected mass effect
Rev.A real carrier:
26.888 cm3
28.2..29.6 g ASA.

Removing magnet bosses should slightly reduce polymer volume.

Adding eight steel targets:
for an illustrative 8 x 12 x 0.8 mm solid tab:
76.8 mm3 each;
614.4 mm3 total.

At steel density ~7.8 g/cm3 sensitivity:
~4.8 g total target mass before holes/rounding.

This remains compatible with front-frame mass budget.

Exact target CAD is authoritative.

## 14. Magnetic force consequence
Moving magnet to fixed side does not inherently change required assembled retention.

Target remains:
20..30 N total.

Eight stations:
2.5..3.75 N average assembled contribution.

G_MAG remains tuned by:
- fixed-side magnet recess;
- front target recess;
- polymer/air stack;
- target thickness.

## 15. Service consequence
Front assembly contains passive steel targets rather than loose rare-earth magnets.

This improves front FRU robustness.

Fixed magnets are serviced only after rear/internal access if replacement is ever required.

## 16. RF policy
Fixed magnets and front targets remain excluded from:
- radar cone/keep-out;
- ESP32 antenna keep-out.

Target clipping does not override RF masks.

If a station is illegal after exact RF masks:
move tangentially along its perimeter band.

## 17. Fabric wrap
Thin target traps shall not create visible telegraphing through fabric.

Target lies rearward of carrier perimeter.

No sharp steel edge contacts fabric.

## 18. Peel behavior
Target-on-front / magnet-on-fixed-side still supports sequential peel.

Because the removable front carries only thin targets, local stiffness spikes are reduced.

Peel force remains an assembly test gate.

## 19. Rev.B CAD regeneration
Generate:
AP22_FRONT_CARRIER_REV_B_DMU

Features:
- 318.4 x 398.4 outer carrier;
- 10 mm ring;
- 1.8 mm base;
- lower 28 x 4 peel recess;
- LOC_A/LOC_B;
- eight thin target-trap features;
- no front-carrier magnet bosses.

Fixed-side magnet captures are separate assembly components/features.

## 20. Automatic checks
C431 DML projection is hard magnet-pad exclusion.
C432 old circular 12 mm front pads rejected.
C433 full 6.6 mm pocket plus 1.5 mm wall evaluated against 10 mm strip.
C434 fragile edge magnet pocket architecture rejected.
C435 magnet moves to fixed product side.
C436 removable front carries discrete steel targets.
C437 no continuous steel ring.
C438 target thickness seed 0.8 mm.
C439 target geometry clipped to legal perimeter band.
C440 target sharp edges cannot contact fabric.
C441 front carrier 3.2 mm magnet bosses removed.
C442 front carrier nominal base returns to 1.8 mm.
C443 total retention remains 20..30 N.
C444 G_MAG remains tunable.
C445 fixed magnet mechanically captured.
C446 target mechanically trapped.
C447 radar RF masks remain authoritative.
C448 ESP32 RF masks remain authoritative.
C449 station tangential coordinates remain stable.
C450 exact normal-axis station coordinates derived by edge-section CAD.
C451 target mass included in front FRU.
C452 front FRU contains no loose permanent magnets baseline.
C453 peel validation remains required.
C454 Rev.B real B-rep regeneration required.
C455 full assembly collision audit follows regeneration.

## 21. State
The initial idea of simply clipping 12 mm magnet bosses exposed a dimensional issue: the 10 mm product-to-DML perimeter strip is too narrow for a robust 6.6 mm enclosed magnet pocket with useful wall thickness.

The architecture is therefore improved:
**MAGNET FIXED SIDE / THIN STEEL TARGET REMOVABLE FRONT**.

This resolves the DML-edge packaging problem without modifying the DML.

Status:
**FRONT_MAGNET_ARCHITECTURE_REVERSED / FIXED_6X2_MAGNETS / THIN_DISCRETE_FRONT_TARGETS / DML_NOTCH_REJECTED / C01_TO_C455 / REV_B_BREP_NEXT**.
