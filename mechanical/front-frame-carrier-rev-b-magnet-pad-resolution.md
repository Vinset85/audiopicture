# AudioPicture V2.2 Rev.B — front carrier magnet-pad resolution

Status: **DML_OVERLAP_RESOLVED_BY_PERIMETER_TAB_ARCHITECTURE / REV_B_CAD_CONTRACT_READY / REAL_KERNEL_REGEN_REQUIRED**

## 1. Problem
Rev.A used nominal 12 mm circular magnet pads centered close to the DML perimeter.

DML projection:
- X=10..310
- Y=10..390 mm.

A 12 mm circular pad centered 4 mm from a DML edge necessarily intrudes into that projection.

The master DMU therefore rejected the Rev.A pad topology.

## 2. Design rule
No rigid magnet pocket/pad volume may occupy the DML hard-clearance projection.

Do not notch the DML.

Do not reduce the DML active panel solely to accommodate front-frame magnets.

## 3. Rev.B magnetic centers
Adopt seed centers:
- M1B=(70,388)
- M2B=(250,388)
- M3B=(70,12)
- M4B=(250,12)
- M5B=(12,135)
- M6B=(12,275)
- M7B=(308,135)
- M8B=(308,315).

These centers are retained as magnetic-circuit reference points, but the structural carrier feature is no longer a symmetric circular boss.

## 4. Fundamental geometry constraint
A 6.6 mm diameter magnet centered at Y=388 extends to Y=384.7, inside the DML projection ending at Y=390.

Therefore simply changing a 12 mm boss to a D-shaped boss does NOT remove the magnet itself from the DML projection.

Likewise:
- bottom center Y12 with R3.3 reaches Y15.3 > DML lower edge10;
- left center X12 reaches X15.3 > DML left edge10;
- right center X308 reaches X304.7 < DML right edge310.

Thus the Rev.B center seed from the previous audit is still geometrically incompatible with a strict no-rigid-volume DML projection rule.

## 5. Corrected solution
Move magnet centers fully outside the DML projection plus clearance.

For magnet radius:
R_MAG=3.3 mm.

Use minimum projected DML clearance:
C_MAG_DML=0.7 mm seed.

Required center distance from DML edge:
>=4.0 mm.

Product perimeter available:
10 mm between DML edge and product edge.

Corrected centers:
Top:
- M1C=(70,394)
- M2C=(250,394)

Bottom:
- M3C=(70,6)
- M4C=(250,6)

Left:
- M5C=(6,135)
- M6C=(6,275)

Right:
- M7C=(314,135)
- M8C=(314,315).

At these positions, the 6.6 mm magnet envelope remains outside DML projection with approximately 2.7 mm projected separation to the DML edge.

## 6. Carrier outer-boundary compatibility
Carrier projected boundary:
X0.8..319.2
Y0.8..399.2.

For center coordinate 6 mm and magnet radius3.3:
outer magnet edge=2.7 mm.

For center314:
outer edge=317.3 mm.

For Y394:
outer edge=397.3 mm.

All magnet envelopes remain inside the carrier projected boundary.

PASS.

## 7. Perimeter tab topology
Use local perimeter tabs integrated into the 10 mm carrier ring.

Each tab:
- contains 6.6 mm magnet pocket;
- is biased toward product outer perimeter;
- uses material already within/perimeter-adjacent ring;
- does not protrude toward DML beyond hard keep-out.

The structural pad is clipped by DML keep-out before union.

Boolean order:
1 carrier ring;
2 generate local tab;
3 subtract magnet pocket;
4 subtract DML hard keep-out from tab;
5 union legal tab with carrier;
6 generate mechanical capture feature.

## 8. DML keep-out
DML hard projected keep-out for front carrier rigid material:
X=10..310
Y=10..390.

For initial CAD, use exact projection.

A future additional clearance offset may enlarge this keep-out if DML edge motion/service requires it.

## 9. Pocket
Candidate-A packaging pocket:
- diameter 6.6 mm;
- depth 2.2 mm class.

Local carrier thickness:
3.2 mm seed.

Remaining front floor:
approximately 1.0 mm before final force/gap tuning.

This 1.0 mm polymer floor contributes to effective magnetic gap and is therefore part of G_MAG tuning.

## 10. Force implication
Rev.A magnetic-force study allowed G_MAG 0.5/0.8/1.0/1.2 mm.

The current 1.0 mm pocket floor naturally lands near that sweep.

However effective magnetic gap also includes:
- target coating;
- assembly clearance;
- adhesive/shim;
- any target recess.

Therefore assembled force still requires test/FE magnetic-circuit model.

## 11. Target placement
Product-side steel target center follows M1C..M8C.

Targets must also remain outside:
- DML hard projection;
- radar RF keep-out;
- ESP32 RF keep-out;
- mic/optical keep-outs.

If a target cannot fit at a station, move the complete station along the perimeter; do not move only the target off-axis without magnetic-force recalculation.

## 12. Top stations
M1C/M2C at Y394.

Magnet envelope:
Y390.7..397.3.

DML ends Y390.

Projected gap:
0.7 mm minimum from magnet envelope to DML projection.

Structural tab must not cross Y390.

## 13. Bottom stations
M3C/M4C at Y6.

Magnet envelope:
Y2.7..9.3.

DML starts Y10.

Projected gap:
0.7 mm.

Bottom peel recess centered X160 remains well separated.

## 14. Left stations
M5C/M6C at X6.

Magnet envelope:
X2.7..9.3.

DML starts X10.

Projected gap:
0.7 mm.

## 15. Right stations
M7C/M8C at X314.

Magnet envelope:
X310.7..317.3.

DML ends X310.

Projected gap:
0.7 mm.

## 16. Why 0.7 mm
0.7 mm is a geometric seed, not production tolerance proof.

It is the result of:
- 4.0 mm center offset from DML edge;
- 3.3 mm magnet-envelope radius.

Final value must absorb:
- print tolerance;
- DML placement tolerance;
- carrier registration tolerance;
- DML edge motion.

Likely production keep-out may require larger separation.

## 17. Tolerance sweep
Sweep center offset from DML edge:
- 4.0 mm
- 4.5 mm
- 5.0 mm.

Corresponding nominal projected clearances for R3.3:
- 0.7 mm
- 1.2 mm
- 1.7 mm.

All remain inside the available 10 mm perimeter band geometrically.

Preferred pre-release:
**5.0 mm center offset / 1.7 mm nominal projected clearance**, if target/carrier outer-edge strength remains acceptable.

That gives:
top Y395, bottom Y5, left X5, right X315.

This becomes Candidate D for tolerance robustness.

## 18. Rev.B vs Candidate D
Candidate C:
center 4 mm outside DML edge; clearance0.7.

Candidate D:
center5 mm outside DML edge; clearance1.7.

Candidate D is preferred for production development because it increases tolerance margin while still fitting the product/carrier boundary.

## 19. Outer-edge ligament
Candidate D center X5 with pocket R3.3 leaves:
5-0.8-3.3=0.9 mm nominal carrier material to outer projected boundary if interpreted as simple circular hole.

This is too small for an unsupported printed pocket wall.

Therefore Candidate D requires:
- local inward/outward tab topology;
- closed fabric-wrap edge independent of pocket wall;
or
- slightly smaller magnet/pocket.

Candidate C center6 leaves:
6-0.8-3.3=1.9 mm outer ligament.

Candidate C is mechanically healthier for the current 6.6 mm pocket.

Thus:
**Candidate C remains baseline** until print-wall qualification.

## 20. Baseline freeze
Use Candidate C:
top Y394
bottom Y6
left X6
right X314.

Projected magnet-to-DML clearance:
0.7 mm nominal.

Outer carrier ligament:
~1.9 mm nominal at side/bottom/top equivalent.

This is a better first balanced geometry than Candidate D.

## 21. Real-CAD regeneration requirements
Regenerate front carrier with:
- 318.4 x398.4 outer boundary;
- 10 mm ring;
- 1.8 mm base;
- eight Candidate-C stations;
- 3.2 mm local station thickness;
- 6.6 mm pockets;
- DML hard keep-out subtraction;
- lower peel recess.

Measure:
- solid count;
- validity;
- volume;
- mass;
- minimum pocket-to-DML distance;
- minimum pocket-to-outer-edge ligament.

## 22. Automatic checks
C431 Rev.B 388/12/308 seed proven insufficient under strict DML rule.
C432 magnet envelope itself included in collision logic.
C433 corrected Candidate-C centers generated.
C434 all 6.6 mm magnet envelopes outside DML projection.
C435 all magnet envelopes inside carrier outer boundary.
C436 nominal magnet-to-DML projected clearance >=0.7 mm.
C437 outer carrier ligament >=1.9 mm nominal for Candidate C.
C438 DML keep-out clips structural tabs.
C439 DML is not notched.
C440 DML size is not reduced for magnets.
C441 target remains coaxial baseline.
C442 target obeys RF exclusions.
C443 1.0 mm pocket floor included in magnetic-gap model.
C444 Candidate D tolerance option documented.
C445 Candidate D not baseline due outer-wall ligament.
C446 Candidate C selected as balanced first geometry.
C447 real kernel regeneration required.
C448 final tolerance may require smaller magnet or station topology change.
C449 peel recess remains clear.
C450 production freeze requires RF plus assembled-force plus print-wall validation.

## 23. State
Rev.B seed was checked mathematically and found insufficient.

Corrected Candidate C:
- top centers Y394;
- bottom Y6;
- left X6;
- right X314;
- 6.6 mm magnet envelope;
- 0.7 mm nominal DML projected clearance;
- ~1.9 mm nominal outer ligament.

Status:
**MAGNET_ENVELOPE_COLLISION_LOGIC_CORRECTED / CANDIDATE_C_6MM_PERIMETER_CENTERS / DML_OVERLAP_NOMINALLY_RESOLVED / C01_TO_C450 / REAL_BREP_REGEN_NEXT**.
