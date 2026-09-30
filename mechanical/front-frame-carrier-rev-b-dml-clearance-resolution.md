# AudioPicture V2.2 Rev.B — front carrier magnetic station DML-clearance resolution

Status: **DML_EDGE_GEOMETRY_AUDITED / 6MM_MAGNET_IN_10MM_EDGE_BAND_IS_TIGHT / D_SHAPED_SUPPORT_WITH_OUTBOARD_MAGNET_CENTER_REQUIRED / EXACT_GLOBAL_BREP_NEXT**

## 1. Purpose
Resolve the front-carrier Rev.A magnetic-pad overlap discovered by the integrated DMU.

The hard rule is stronger than center-point clearance:
**the complete rigid magnetic station geometry must remain outside the DML hard projected keep-out unless an explicitly validated perimeter interface permits overlap.**

No DML notch is accepted as baseline.

## 2. Available edge band
Product:
320 x 400 mm.

DML projection:
X=10..310
Y=10..390.

Nominal product-to-DML projected border:
**10 mm per side**.

Front carrier outer boundary:
X=0.8..319.2
Y=0.8..399.2.

Thus usable carrier edge band from carrier outer boundary to DML edge is approximately:
**9.2 mm**.

## 3. Magnet diameter fit
Candidate A magnet:
diameter 6.0 mm.

Pocket:
diameter 6.6 mm.

If a circular 6.6 mm pocket must remain completely outside the DML projection, its center must be at least:
3.3 mm from the DML edge toward the product perimeter.

Legal center limits:
- left X <= 6.7
- right X >= 313.3
- bottom Y <= 6.7
- top Y >= 393.3.

The previous Rev.B centers at X/Y=12/308/388 are therefore NOT sufficient for a complete circular pocket outside the DML projection.

## 4. Corrected station-center architecture
Move each station to the edge on which it is mounted.

Top:
M1C=(70,395.0)
M2C=(250,395.0)

Bottom:
M3C=(70,5.0)
M4C=(250,5.0)

Left:
M5C=(5.0,135)
M6C=(5.0,275)

Right:
M7C=(315.0,135)
M8C=(315.0,315).

These centers provide:
- 5.0 mm center distance from product outer edge;
- 5.0 mm center distance from DML edge.

For 6.6 mm pocket radius 3.3 mm:
- outer-edge residual to nominal product boundary = 1.7 mm;
- DML-edge residual = 1.7 mm.

Relative to carrier outer boundary at 0.8/319.2 etc, local residual is approximately 0.9 mm on the outer side.

Therefore the pocket fits geometrically but local carrier material is thin and requires a shaped station boss/cap.

## 5. D-shaped station pad
The support pad is not a 12 mm circle.

Define local pad as:
- outboard/perimeter-biased lobe;
- flat or clipped DML-facing side;
- local tangential extension along perimeter;
- no rigid material crossing DML hard boundary.

Seed dimensions:
- tangential length 14..18 mm;
- radial width limited to edge band;
- local total Z thickness 3.2 mm;
- root fillets >=1.0 mm where printable.

Pocket remains circular 6.6 mm.

## 6. Structural consequence
Because only ~0.9 mm carrier material remains between pocket and carrier outer boundary in the strict nominal geometry, do not rely on a thin annulus around the pocket.

Use:
- tangential shoulders;
- rear cap/bridge integrated along perimeter;
- mechanical capture spanning beyond pocket diameter.

The magnet pocket is structurally supported along the perimeter direction.

## 7. Fabric wrap consequence
The magnetic station cannot consume the entire rear fabric bonding land.

At each station:
- locally split/route bonding land around station;
- preserve >=5 mm equivalent adhesive path where possible;
- add tangential adhesive land before/after pocket.

Fabric must not bridge a sharp boss edge.

## 8. Target architecture
The product-side steel target must follow the same edge-band rule.

Target cannot be a 10 mm circular disc centered at x/y=5 without approaching the product boundary excessively.

Preferred target:
**elongated tangential steel tab**, approximately:
- 12..16 mm tangential;
- 5..7 mm radial;
- 0.8..1.0 mm thick seed.

Exact magnetic performance requires FEA/bench magnetic circuit validation.

## 9. Retention-force implication
Reducing target radial dimension may reduce magnetic force relative to ideal thick-plate catalogue conditions.

This is acceptable because:
- catalogue Candidate A force exceeds required per-station force;
- product target is only 2.5..3.75 N average per station.

G_MAG and target dimensions are co-optimized.

## 10. Corner policy
Do not place magnets in corners.

Reasons:
- fabric wrapping complexity;
- carrier stress concentration;
- peel behavior;
- less room for tangential target tabs.

Current mid-edge stations remain preferred.

## 11. DML clearance result
For center distance 5.0 mm from DML edge and pocket radius 3.3 mm:
nominal rigid-pocket-to-DML projected clearance:
**1.7 mm**.

This is positive.

Apply manufacturing/tolerance allowance before release.

Target hard minimum after tolerance:
**>=1.0 mm projected clearance**.

## 12. Product-edge result
For center 5.0 mm from product boundary and pocket radius 3.3 mm:
nominal pocket-to-product-edge residual:
**1.7 mm**.

Relative to carrier boundary inset 0.8 mm:
nominal pocket-to-carrier-edge residual:
**0.9 mm**.

This is too small for an unsupported circular boss, hence tangential cap/shoulder architecture is mandatory.

## 13. Peel feature
M3C/M4C remain at X70/250.

Lower-center peel recess X160 width28 remains approximately 76 mm clear from nearest pocket edge in X.

Progressive peel remains viable.

## 14. RF policy
The corrected coordinates remain seed values only until exact:
- ESP32 antenna keep-out;
- radar RF cone;
- microphone acoustic keep-outs;
- OPT3004 optical keep-out

are booleaned into the carrier.

Any station failing those masks is shifted tangentially, not radially into DML.

## 15. CAD construction order
1. create 318.4 x 398.4 perimeter ring;
2. create revised M1C..M8C station tangential lobes;
3. union lobes with ring;
4. subtract 6.6 mm magnet pockets;
5. add mechanical capture bridge/lip;
6. subtract DML projected hard keep-out with >=1.0 mm tolerance margin;
7. subtract RF/acoustic/optical keep-outs;
8. create peel recess;
9. validate one-solid B-rep;
10. transform into global product Z.

## 16. Automatic checks
C431 full magnet pocket, not only center, checked against DML.
C432 9.2 mm nominal carrier edge band recorded.
C433 legal circular-pocket center limit derived.
C434 Rev.B x/y=12/308/388 seeds retired for strict DML-clearance use.
C435 Rev.C seed centers at 5/315/395 defined.
C436 6.6 mm pocket has nominal 1.7 mm DML projected clearance.
C437 6.6 mm pocket has nominal 1.7 mm product-edge residual.
C438 carrier-edge residual ~0.9 mm identified as structural warning.
C439 12 mm circular station pad retired.
C440 tangential D-shaped station architecture required.
C441 station tangential length sweep 14..18 mm.
C442 target changed from generic 10 mm disc baseline to tangential tab preference.
C443 target radial width 5..7 mm seed.
C444 target thickness 0.8..1.0 mm seed.
C445 no DML notch baseline.
C446 >=1.0 mm projected DML clearance after tolerance required.
C447 fabric bonding land routed around stations.
C448 corner magnets prohibited baseline.
C449 peel recess remains clear.
C450 failed RF station moves tangentially, never radially into DML.

## 17. State
The DMU warning is geometrically resolved at the dimensional-contract level.

Key correction:
**magnet center must move to 5 mm from the product edge, not 12 mm, for a 6.6 mm pocket to remain fully outside a DML starting 10 mm from the product edge.**

This creates a new local structural issue:
only ~0.9 mm remains between pocket and carrier outer edge.

Solution:
**tangential D-shaped/lobed station with perimeter capture bridge**, not a circular boss.

Status:
**MAGNET_CENTERS_REV_C_EDGE_5MM / 6P6MM_POCKET_DML_CLEARANCE_1P7MM / TANGENTIAL_D_PAD_REQUIRED / C01_TO_C450 / REAL_BREP_AND_TOLERANCE_AUDIT_NEXT**.
