# AudioPicture V2.2 Rev.B — front carrier magnetic-pad resolution

Status: **REV_B_MAGNETIC_STATIONS_PERIMETER_SHIFTED / DML_FACING_PAD_MATERIAL_REJECTED / CAD_KERNEL_REGENERATION_REQUIRED**

## 1. Purpose
Resolve the Rev.A front-carrier warning in which nominal 12 mm circular magnet pads overlapped the projected DML perimeter.

The DML is not notched or modified to accommodate front-frame magnets.

## 2. Authoritative projected DML boundary
DML:
- X = 10..310 mm
- Y = 10..390 mm.

For magnetic-station rigid material, this rectangle is treated as a hard projected exclusion unless a later detailed perimeter-interface model explicitly proves otherwise.

## 3. Rev.B magnet centers
Top:
- M1B = (70,388)
- M2B = (250,388)

Bottom:
- M3B = (70,12)
- M4B = (250,12)

Left:
- M5B = (12,135)
- M6B = (12,275)

Right:
- M7B = (308,135)
- M8B = (308,315).

These replace the Rev.A station seeds for the next CAD regeneration.

## 4. Important geometric result
A symmetric circular pad centered only 2 mm from the DML boundary cannot satisfy zero projected intrusion if its radius exceeds 2 mm.

Therefore:
- a 12 mm circular pad is invalid;
- a 6.6 mm circular magnet pocket itself also cannot remain centered there if all rigid pocket material must stay outside the DML rectangle.

A D-shaped pad alone does not solve the problem if the magnet bore remains symmetric about the same center.

This means the Rev.B station must be designed as a perimeter cassette/pocket whose magnet center and rigid capture geometry lie fully outside the DML hard projection, or the DML projected exclusion must be refined to its actual mechanical perimeter support geometry.

## 5. Corrected design rule
Do not claim zero DML overlap from the Rev.B center shift alone.

Required:
**MAGNET_POCKET_RIGID_ENVELOPE ∩ DML_HARD_PROJECTION = empty**

This includes:
- pocket wall;
- capture lip;
- magnet body if body is classified hard;
- steel target;
- local carrier thickening.

## 6. Perimeter-space limitation
Product boundary:
X 0..320
Y 0..400.

DML is inset only 10 mm.

Available geometric strip between DML projection and product boundary:
10 mm nominal.

Carrier outer boundary is inset 0.8 mm, leaving approximately:
9.2 mm usable projected strip.

A 6 mm-class magnet can fit in that strip only with carefully controlled wall thickness and center position.

## 7. Revised center calculation
For a 6.6 mm pocket envelope, radius = 3.3 mm.

Assume minimum rigid outer wall to carrier edge:
1.5 mm seed.

Required center from product outer edge:
>= 0.8 + 1.5 + 3.3 = **5.6 mm**.

Required center outside DML boundary:
for left/bottom center <= 10 - 3.3 = **6.7 mm**.
for right center >= 310 + 3.3 = **313.3 mm**.
for top center >= 390 + 3.3 = **393.3 mm**.

Therefore a feasible center interval exists:
- left/bottom approximately 5.6..6.7 mm;
- right approximately 313.3..314.4 mm;
- top approximately 393.3..394.4 mm.

This is narrow but geometrically non-empty.

## 8. Rev.C-ready station seed
Use nominal center 6.15 mm from the relevant product edge/DML side.

Bottom:
- M3C = (70, 6.15)
- M4C = (250, 6.15)

Top:
- M1C = (70, 393.85)
- M2C = (250, 393.85)

Left:
- M5C = (6.15,135)
- M6C = (6.15,275)

Right:
- M7C = (313.85,135)
- M8C = (313.85,315).

These are mathematical packaging seeds, not production coordinates.

## 9. Tolerance warning
The feasible interval is only about 1.1 mm wide before print/process tolerances.

Therefore the 6.6 mm pocket is geometrically possible but tolerance-sensitive.

This strongly favors one or more of:
- smaller magnet diameter;
- reduced pocket wall through insert/cap architecture;
- local carrier outer geometry extension/reveal change;
- refined DML hard projection based on actual perimeter compliance geometry.

## 10. Magnet candidate consequence
The 6 x 2 mm Candidate A remains viable as a magnetic-force candidate but is no longer automatically the best packaging candidate.

A smaller diameter magnet may improve:
- DML clearance;
- carrier wall;
- tolerance robustness;
- locator/magnet separation.

Exact magnet selection is reopened as:
**FORCE + PACKAGING CO-OPTIMIZATION**.

## 11. D-shaped feature role
D-shaped/local asymmetric pads remain useful for:
- reducing pad material toward DML;
- placing reinforcement outward;
- controlling local stiffness.

But they do not mathematically rescue an illegally centered circular magnet bore.

## 12. Steel target
Target must obey the same projected hard exclusion.

A nominal 10 mm target cannot be centered in the 10 mm perimeter strip with comfortable tolerance if constrained to zero DML overlap.

Therefore target geometry should be:
- elongated tangentially along perimeter;
- narrow radially;
- e.g. 4..6 mm radial x 10..16 mm tangential class.

Exact magnetic circuit requires FEA/test.

## 13. Preferred next CAD geometry
For each station:
- tangential elongated outer reinforcement;
- compact circular magnet pocket;
- DML-facing material trimmed to hard boundary;
- outer-side capture wall;
- tangential steel target.

Top/bottom stations elongate in X.
Left/right stations elongate in Y.

## 14. Global Z
This correction is primarily XY.

Global Z remains:
- fabric Z0..0.5;
- DML front Z3.3;
- DML rear Z9.3;
- rear shell inner Z37.8.

No new front-stack thickness is authorized.

## 15. Engineering decision
The previous statement that Rev.B centers plus D-shaped pads would automatically remove DML collision is withdrawn.

The correct result is:
**Rev.B identified the direction; exact zero-overlap requires a further center shift or smaller magnetic package.**

This correction is intentionally made before claiming a successful B-rep.

## 16. Automatic checks
C431 Rev.A magnetic centers retired.
C432 Rev.B centers evaluated geometrically.
C433 12 mm circular pad at Rev.B centers rejected.
C434 6.6 mm symmetric pocket at Rev.B centers rejected for zero-overlap rule.
C435 D-shaped pad alone not accepted as proof.
C436 perimeter strip quantified as ~9.2 mm.
C437 feasible 6.6 mm pocket center interval calculated.
C438 Rev.C-ready center seeds defined.
C439 tolerance sensitivity explicitly flagged.
C440 magnet selection reopened for packaging co-optimization.
C441 steel target must obey DML projected exclusion.
C442 10 mm radial target rejected as default.
C443 tangential narrow target architecture defined.
C444 no DML notch authorized.
C445 no extra Z thickness authorized.
C446 next CAD must prove rigid-envelope/DML intersection empty.
C447 next CAD must remain one valid solid.
C448 next CAD must preserve magnet mechanical capture.
C449 next CAD must preserve carrier outer boundary.
C450 no collision PASS may be claimed before kernel Boolean verification.

## 17. State
The collision issue is now mathematically bounded.

A 6.6 mm pocket can theoretically fit in the perimeter strip, but only in a narrow center interval around 6.15 mm from the relevant outer edge.

Because this is tolerance-sensitive, smaller magnet packaging is now a serious design option.

Status:
**MAGNET_PAD_COLLISION_MATHEMATICALLY_BOUNDED / REV_B_CENTER_SHIFT_INSUFFICIENT / REV_C_READY_SEEDS_DEFINED / C01_TO_C450 / SMALLER_MAGNET_COOPTIMIZATION_RECOMMENDED**.
