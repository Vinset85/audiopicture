# AudioPicture V2.2 Rev.B — front carrier with perimeter-biased D-shaped magnet pads

Status: **REV_B_MAGNET_PAD_GEOMETRY_DEFINED / DML_HARD_PROJECTION_CLEARANCE_ENFORCED / REAL_KERNEL_REGENERATION_NEXT**

## 1. Purpose
Remove the Rev.A front-carrier magnetic-pad overlap with the DML projected perimeter without modifying or notching the DML.

## 2. Authoritative DML projection
DML hard projected rectangle:
- X = 10..310 mm
- Y = 10..390 mm.

The magnetic station structural pad must remain outside this hard projection.

A nominal CAD guard is added so print/tolerance drift does not reopen contact.

## 3. DML-facing guard
Nominal rigid XY guard:
**0.5 mm**

Therefore magnetic pad material shall remain:
- bottom stations: Y <= 9.5 mm where directly adjacent to DML;
- top stations: Y >= 390.5 mm;
- left stations: X <= 9.5 mm;
- right stations: X >= 310.5 mm.

This applies to the local rear-thickened pad/capture geometry, not to the thin general carrier ring.

## 4. Rev.B magnet centers
Previous proposed centers at 12 mm from the product edge are rejected for the thickened pad if a conventional centered circular pad is used: a 6 mm radius pad would still extend deeply across the DML edge.

Instead separate:
- magnet center;
- structural pad centroid.

Magnet center must itself remain compatible with the 6.6 mm pocket and DML guard.

## 5. Revised magnet center solution
Use centers closer to the product perimeter:

Top:
M1C = (70, 394.0)
M2C = (250, 394.0)

Bottom:
M3C = (70, 6.0)
M4C = (250, 6.0)

Left:
M5C = (6.0, 135)
M6C = (6.0, 275)

Right:
M7C = (314.0, 135)
M8C = (314.0, 315).

For a 6.6 mm pocket:
radius = 3.3 mm.

Nearest pocket edge to DML:
- top: 390.7 mm
- bottom: 9.3 mm
- left: 9.3 mm
- right: 310.7 mm.

Thus the magnet pocket itself clears the DML hard projection and the 0.5 mm nominal guard by approximately:
**0.2 mm additional nominal margin**.

## 6. Important tolerance note
The 0.2 mm extra margin beyond the 0.5 mm guard is not enough to absorb all process uncertainty by itself.

The guard is a CAD exclusion.

Final print-process compensation/tolerance shall be applied to the pocket/pad outer geometry, not by consuming DML clearance.

Production target should prefer >=0.8 mm actual measured clearance if packaging permits.

## 7. D-shaped structural pad
The local station thickening is not a centered diameter-12 circle.

Define each station as:
- compact pocket boss around the 6.6 mm magnet bore;
- perimeter-side reinforcement lobe;
- flat/clipped DML-facing boundary at the legal guard plane.

DML-facing boundary:
- top pads: Y >=390.5
- bottom pads: Y <=9.5
- left pads: X <=9.5
- right pads: X >=310.5.

Perimeter-facing lobe may extend into the carrier ring as needed.

## 8. Pad minimum ligament
Around 6.6 mm pocket:
target polymer ligament:
>=1.5 mm where geometrically possible.

At the DML-facing side the available nominal distance from pocket edge to guard is only about 0.2 mm with the 6 mm center offset.

Therefore a conventional full polymer ligament cannot exist on that side.

This reveals a second-order geometry issue.

## 9. Pocket/capture architecture correction
Do not rely on a full circular printed boss around the magnet.

Preferred Rev.B:
**open-D pocket cradle + separate nonconductive rear capture cap**.

The cradle:
- supports magnet on perimeter side and tangential sides;
- DML-facing wall is minimized/omitted;
- rear cap mechanically traps magnet.

Alternative:
move magnet center farther outward if cosmetic carrier boundary allows.

## 10. Outer-boundary constraint
Carrier projected outer boundary:
X0.8..319.2
Y0.8..399.2.

At center 6.0 mm with 3.3 mm magnet radius:
outer pocket edge = 2.7 mm.

This remains inside the 0.8 mm carrier boundary with 1.9 mm radial space.

At center 394.0:
outer edge =397.3 mm, leaving 1.9 mm to Y399.2.

Thus the magnet disc itself fits.

## 11. Retention cap
Use a small ASA/nonconductive cap or printed integral flexural/slide capture feature.

No steel cap.

The cap:
- cannot enter DML hard projection;
- must survive adhesive failure;
- remains serviceable at workshop level before fabric wrapping if practical.

## 12. Steel target location
Targets are on product-side perimeter structure opposite the magnets.

Target shape shall also be DML/perimeter clipped.

No target enters:
- DML compliant perimeter;
- radar RF keep-out;
- ESP32 RF keep-out.

Target thickness remains 0.8..1.2 mm sensitivity.

## 13. Force implication
Moving magnet centers outward does not invalidate the 20..30 N total retention target.

However target overlap area may be reduced by clipping.

Therefore actual magnetic force must be measured/simulated using:
- real target shape;
- real gap;
- real lateral alignment.

Catalogue direct-contact pull remains non-authoritative.

## 14. Carrier ring interaction
Nominal 10 mm ring occupies perimeter.

The new magnet centers are embedded naturally in this perimeter zone.

Local pad thickening merges into the ring toward the product edge, not toward the DML.

This is structurally preferable to the Rev.A circular island.

## 15. Front Z interaction
Local magnetic station rear thickness remains target:
3.0..3.2 mm class.

Because stations are now outside DML hard projection, their rear intrusion no longer consumes the central fabric-DML gap.

Global front-stack rule remains:
- fabric outer Z0;
- DML front Z3.3.

Exact carrier global transform still must ensure no peripheral DML mount/foam conflict.

## 16. Locator interaction
LOC_A/LOC_B shall be placed independently of magnet pockets.

Do not combine locator and magnet capture unless tolerance analysis proves it beneficial.

Magnet stations remain normal-force retention only.

## 17. Peel recess
Lower peel recess remains:
- center X160
- width28
- depth4.

M3C/M4C remain at X70/250 and therefore do not obstruct the central release feature.

## 18. Real CAD regeneration requirements
Next kernel generation shall:
1. rebuild 318.4 x398.4 carrier;
2. retain 10 mm ring /1.8 mm base;
3. remove Rev.A circular thickened pads;
4. create eight perimeter-biased D-shaped/open-D cradles;
5. create 6.6 mm pocket envelopes;
6. apply DML guard clipping;
7. subtract peel recess;
8. check one-solid connectivity;
9. compute volume/mass/bbox;
10. run explicit DML hard-projection intersection test.

## 19. Collision acceptance
Hard PASS requires:
intersection volume between:
- thickened magnet/capture geometry
and
- DML hard projected prism
equals:
**0 mm3**.

Additionally report minimum XY distance.

Target:
>=0.5 mm CAD guard.

Preferred production measured:
>=0.8 mm where achievable.

## 20. Automatic checks
C431 Rev.A circular 12 mm magnetic pads retired.
C432 Rev.B proposed 12 mm-center solution rejected for thick-pad legality.
C433 magnet centers moved to 6 mm perimeter offset.
C434 6.6 mm magnet pocket remains inside carrier outer boundary.
C435 magnet pocket clears DML hard projection.
C436 0.5 mm CAD DML guard defined.
C437 D-shaped/open-D thickening clipped to DML guard.
C438 no DML notch introduced.
C439 no full circular polymer ligament assumed at DML-facing side.
C440 nonconductive rear capture architecture defined.
C441 target geometry also perimeter clipped.
C442 target remains discrete.
C443 magnetic force revalidation required after clipping.
C444 local rear thickening does not consume active DML air gap.
C445 peel recess remains clear.
C446 locators remain independent.
C447 real kernel regeneration required.
C448 explicit intersection volume must equal zero.
C449 minimum XY clearance reported by next kernel audit.
C450 preferred production measured clearance >=0.8 mm remains optimization target.

## 21. State
Rev.B correction:
- magnets move to 6 mm from product perimeter;
- magnet pocket fits inside carrier;
- pocket nearest edge remains outside DML projection;
- structural thickening becomes D-shaped/open-D and grows outward;
- DML remains untouched.

Status:
**MAGNET_CENTERS_6MM_FROM_PERIMETER / OPEN_D_CRADLE / DML_GUARD_0P5MM / C01_TO_C450 / REAL_BREP_REGENERATION_NEXT**.
