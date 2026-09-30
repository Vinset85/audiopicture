# AudioPicture V2.2 — magnetic interface force gate Rev.E

Status: **S04_02_N_DATASHEET_VERIFIED / 4X2MM_BASELINE_HELD / TARGET_AND_GAP_COUPON_MATRIX_FROZEN / ASSEMBLED_FORCE_REMAINS_PHYSICAL_GATE**

## 1. Purpose
Close the analytical part of the front-frame magnetic-interface gate after the real 4.4 mm-pocket kernel pass.

This gate does not invent an assembled magnetic force. It freezes a testable magnetic circuit and acceptance matrix.

## 2. Repository conflict resolved
A historical file labelled FINAL selected S-04-01-N, 4 x 1 mm, and revised the assembled retention target to 14..20 N.

Later trade-study and real-kernel work restored:
- S-04-02-N class;
- 4 x 2 mm;
- 4.4 mm pocket;
- eight stations;
- 20..30 N assembled target.

The later real-kernel baseline is authoritative.

Therefore:
- S-04-02-N = active baseline;
- S-04-01-N = Z-contingency only;
- 20..30 N assembled normal retention target remains active.

## 3. Manufacturer verification
Manufacturer datasheet verified for S-04-02-N:
- NdFeB;
- disc;
- diameter 4 mm;
- height 2 mm;
- tolerance +/-0.1 mm;
- axial magnetization;
- Ni-Cu-Ni coating;
- N45;
- stated attraction approximately 420 g / 4.12 N under manufacturer conditions;
- stated tangential force approximately 85 g / 0.832 N;
- maximum operating temperature 80 C;
- mass 0.1910 g;
- Br 1.32..1.37 T.

Eight magnets:
- total magnet mass = 1.528 g;
- arithmetic catalogue attraction reference = 32.96 N.

The 32.96 N value is NOT an assembled-force prediction.

## 4. Why 4 x 1 mm is not baseline
S-04-01-N manufacturer data:
- 4 x 1 mm;
- N45;
- attraction approximately 2.45 N;
- tangential force approximately 0.492 N;
- mass approximately 0.0955 g.

Eight catalogue values sum to only 19.6 N before any product gap, target, coating, alignment or tolerance loss.

Therefore 4 x 1 mm cannot support the active 20..30 N target as the primary eight-station baseline.

It remains a Z fallback only if the retention requirement is formally changed or station count/topology is revalidated.

## 5. Magnetic circuit baseline
Architecture:
magnet in removable ASA front carrier + discrete low-carbon steel target on fixed structural perimeter.

Quantity:
8 independent circuits.

No continuous steel ring.

No magnet-to-magnet baseline.

The target shall be positively retained to the structural node; adhesive alone is not the primary loose-part retention method.

## 6. Target geometry matrix
First physical coupon target geometry:
- low-carbon steel, unmagnetized;
- square 7 x 7 mm OR round diameter 8 mm;
- thickness sweep 0.8 / 1.0 / 1.2 mm.

Preferred first article:
**7 x 7 x 1.0 mm low-carbon steel target**.

Reason:
it is larger than the 4 mm pole face without returning to the oversized historical target architecture, and 1.0 mm sits at the center of the already-defined target-thickness sweep.

Exact alloy/coating remains sourcing/test controlled.

## 7. Effective gap definition
Define G_EFF as the total non-ferromagnetic separation between magnet pole face and steel target face in the seated product.

It includes:
- carrier pocket floor or retaining skin if present in the flux path;
- coating/paint;
- anti-rattle film if located in the magnetic path;
- assembly stand-off;
- tolerance-induced residual air gap.

Do not report only nominal air gap.

## 8. Gap coupon matrix
Test S-04-02-N against the selected target at:

G_EFF:
- 0.20 mm
- 0.40 mm
- 0.60 mm
- 0.80 mm.

Target thickness:
- 0.8 mm
- 1.0 mm
- 1.2 mm.

This creates 12 primary magnetic-circuit coupon conditions.

For each condition measure at least 5 assemblies/magnets and report:
- mean normal pull;
- minimum normal pull;
- maximum normal pull;
- standard deviation;
- tangential slip force;
- re-seat behavior;
- visible target bending or carrier deformation.

## 9. Per-station acceptance logic
Eight stations and total target 20..30 N imply average assembled contribution:
2.5..3.75 N/station.

Coupon selection rule:
- nominal configuration mean target: 2.8..3.5 N/station;
- no tested station below 2.5 N at room-temperature nominal assembly condition;
- eight-station assembled frame must independently measure 20..30 N total normal pull.

Per-station arithmetic does not replace the complete-frame measurement.

## 10. Preferred initial build
Start coupon testing with:
- S-04-02-N;
- 7 x 7 x 1.0 mm low-carbon steel target;
- G_EFF = 0.40 mm.

This is a test starting point, not a predicted PASS.

If force is high:
increase G_EFF before reducing magnet thickness.

If force is low:
first reduce G_EFF, then test 1.2 mm target, then evaluate target-area change.

Do not return to 6 mm magnets.

## 11. Peel gate
Complete-frame normal pull alone is insufficient.

With the selected magnetic circuit measure lower-center progressive peel.

Acceptance seed:
- user can initiate peel by hand using the hidden recess;
- no tool required;
- no fabric/carrier damage;
- no DML contact;
- no magnet/target release;
- release is sequential rather than all stations snapping free simultaneously.

Force-vs-displacement curve shall be recorded.

A numerical peel limit is not frozen in this gate because no measured human-interface evidence currently supports one.

## 12. Temperature gate
Manufacturer maximum operating temperature is 80 C.

Product qualification shall not use 80 C as the desired operating point.

Measure retention:
- room-temperature reference;
- after thermal soak at the product-qualified hot condition;
- after return to room temperature.

The product hot-condition temperature is defined by the system thermal validation, not invented here.

Reject permanent force loss, coating damage, pocket creep or magnet loosening.

## 13. Tolerance gate
Coupon/final test shall include:
- magnet thickness tolerance +/-0.1 mm;
- pocket/process compensation;
- target thickness tolerance from selected supplier;
- carrier warp/seating;
- lateral offset.

Minimum-force samples shall be represented, not only nominal CAD geometry.

## 14. RF/EM separation
Passing magnetic force does not authorize a station location.

Every magnet and steel target remains subject to:
- ESP32 antenna hard keep-out;
- radar hard keep-out;
- microphone/optical exclusions where applicable.

A force-pass target may still be rejected by RF/EM integration.

## 15. Production decision rule
Freeze target thickness and G_EFF only after:
1. coupon normal-pull data pass;
2. complete-frame 20..30 N pull passes;
3. progressive peel is serviceable;
4. vibration/buzz passes;
5. hot-condition retention passes;
6. exact RF/radar validation passes.

Until then:
**target thickness and effective gap are controlled experimental variables, not production dimensions.**

## 16. Automatic checks
C491 current repository HEAD reviewed before force gate.
C492 historical 4x1/14..20N decision identified as conflicting with later kernel baseline.
C493 later real-kernel 4x2 baseline treated as authoritative.
C494 S-04-02-N manufacturer MPN verified.
C495 S-04-02-N diameter 4 mm verified.
C496 S-04-02-N height 2 mm verified.
C497 S-04-02-N N45 verified.
C498 S-04-02-N tolerance +/-0.1 mm verified.
C499 S-04-02-N catalogue attraction 4.12 N recorded as reference only.
C500 S-04-02-N tangential force 0.832 N recorded as reference only.
C501 S-04-02-N max operating temperature 80 C recorded.
C502 eight-magnet mass 1.528 g calculated.
C503 catalogue-force multiplication prohibited as assembled proof.
C504 S-04-01-N retained only as Z contingency.
C505 eight discrete low-carbon steel targets retained.
C506 target sweep 0.8/1.0/1.2 mm frozen for coupon.
C507 target first article 7x7x1.0 mm defined.
C508 G_EFF explicitly includes all non-ferromagnetic separation.
C509 G_EFF sweep 0.2/0.4/0.6/0.8 mm frozen.
C510 twelve primary coupon conditions defined.
C511 minimum five samples per coupon condition required.
C512 per-station nominal mean target 2.8..3.5 N defined.
C513 no nominal room-temperature station below 2.5 N.
C514 complete-frame measured pull remains 20..30 N.
C515 complete-frame measurement required independently of station arithmetic.
C516 initial coupon starts at G_EFF 0.40 mm and 1.0 mm target.
C517 peel force-vs-displacement measurement required.
C518 no unsupported numerical peel acceptance invented.
C519 hot-condition magnetic retention test required.
C520 exact RF/EM masks remain release gates.

## 17. State
Analytical magnetic-interface definition:
**CLOSED FOR COUPON BUILD**

Production magnetic-force validation:
**OPEN**

Baseline:
- 8 x S-04-02-N;
- 4 x 2 mm N45;
- 4.4 mm carrier pocket;
- discrete low-carbon steel targets;
- 7 x 7 x 1.0 mm first target;
- G_EFF 0.40 mm first test;
- 0.2..0.8 mm gap sweep;
- 0.8..1.2 mm target-thickness sweep;
- 20..30 N complete-frame measured normal-retention requirement.

Status:
**MAGNETIC_COUPON_MATRIX_FROZEN / S04_02_N_VERIFIED / NO_FORCE_FEA_CLAIM / C01_TO_C520 / PHYSICAL_FORCE_PEEL_THERMAL_RF_VALIDATION_NEXT**.
