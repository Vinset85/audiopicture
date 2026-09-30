# AudioPicture V2.2 — fixed magnetic target-holder kernel Rev.G

Status: **TARGET_HOLDER_KERNEL_DEFINED / OUTWARD_BIASED_CAPTURE / DML_HARD_CLEARANCE_INCREASED / RADAR_MASK_GATE_OPEN**

## 1. Purpose
Create a real fixed-side holder architecture for the eight 7 x 7 x 1.0 mm steel magnetic targets introduced in Rev.F.

The holder must:
- retain the target positively;
- remain outside the DML hard projection;
- preserve the magnetic face;
- avoid adhesive-only loose-part retention;
- remain compatible with the 40 mm global envelope;
- stay regenerable when the exact radar mask arrives.

## 2. Critical finding from Rev.F
A symmetric 7 x 7 mm target at the Rev.D station centers has only 0.5 mm nominal DML clearance.

That is insufficient margin for a robust printed holder on the DML-facing side.

Therefore the holder is not wrapped symmetrically around the target.

## 3. Selected holder topology
Use an **outward-biased three-sided target cassette**.

Features:
- target face toward the removable carrier remains magnetically exposed;
- target is supported from the fixed side/rear;
- two tangential side rails capture lateral motion;
- one outer-edge rail/lip prevents outward escape;
- DML-facing side remains open and contains no retaining wall;
- a rear support shelf controls target Z;
- assembly insertion occurs from the DML-facing/open side before final positive closure feature is engaged.

The holder grows toward the product perimeter, never toward the DML.

## 4. Target geometry
First article remains:
- 7.0 x 7.0 mm;
- 1.0 mm thick;
- low-carbon steel.

The target itself is not reduced in this gate because magnetic coupon geometry should remain unchanged until force data exists.

## 5. Holder nominal dimensions
Diagnostic kernel seed:
- side-rail thickness: 0.8 mm;
- outer rail thickness: 0.8 mm;
- rear support thickness: 0.8 mm;
- target XY running clearance: 0.15 mm per tangential side;
- target Z running clearance: 0.15 mm;
- capture lip overlap: 0.35 mm seed;
- root fillet target: >=0.6 mm where printable geometry permits.

These are CAD/process seeds, not production tolerances.

## 6. DML-facing rule
No holder polymer is permitted between the target DML-facing edge and the DML hard projection.

For the current target:
- nominal target/DML gap = 0.5 mm.

The holder's DML-facing boundary is therefore the target boundary itself.

This preserves the full 0.5 mm nominal hard clearance instead of consuming it with a wall.

Production tolerance closure remains open.

## 7. Outward envelope
The holder adds 0.8 mm nominal structure on the product-perimeter side of the target.

Rev.F target-to-carrier outer-boundary margin:
1.7 mm.

After 0.8 mm outward rail:
remaining nominal projected margin:
**0.9 mm**.

This remains positive at nominal CAD level.

It is not a production tolerance PASS.

## 8. Tangential envelope
Target tangential size:
7.0 mm.

With 0.15 mm running clearance each side and 0.8 mm side rails:
overall tangential holder width:
**8.9 mm**.

The stations are widely separated, so holder-to-holder collision is not governing.

## 9. Global Z
Target packaging envelope remains:
Z4.1..5.1 mm conservative DMU seed.

Rear support shelf:
Z5.1..5.9 mm nominal.

Local rear capture structure may extend to:
**Z6.3 mm maximum diagnostic seed**.

This remains inside the front/perimeter region and does not threaten the rear 40 mm closure.

Because DML occupies Z3.3..9.3, all holder material at Z4.1..6.3 must remain outside the DML XY projection.

## 10. Structural attachment
The target holder is a fixed-side local node.

It shall ultimately attach to a legal non-DML structural path.

This Rev.G kernel validates the local cassette geometry only.

It does NOT yet claim a continuous structural bridge from Z~6 to the rear PC-CF band at Z27..35.

Such a bridge must be generated only after exact front-perimeter fixed-frame/shell geometry is integrated.

Do not create a long unsupported post merely to connect these datums.

## 11. Positive retention
Adhesive may be used for anti-rattle only.

Positive retention is provided by:
- rear shelf;
- tangential rails;
- outer rail;
- local snap/closure lip seed.

Target ejection toward the removable carrier must be blocked mechanically.

Production lip dimensions require print coupon and insertion/removal testing.

## 12. Magnetic face
No polymer sheet is added across the magnet-facing target surface in the baseline.

This avoids silently increasing G_EFF.

If a protective film/coating is later required, its thickness becomes part of G_EFF.

## 13. DML collision classification
At nominal CAD:
- steel target/DML XY clearance = 0.5 mm;
- holder DML-facing wall = none;
- holder/DML hard-volume intersection target = 0 mm3.

Result:
**NOMINAL GEOMETRIC PASS**.

Tolerance closure:
**OPEN**.

## 14. ESP32 and radar
ESP32:
Rev.F coarse PASS remains unchanged because holder growth is local and biased outward from the DML/product interior.

Exact RF mask boolean remains required when exact module geometry is available.

Radar:
exact EM hard mask remains unavailable.

Therefore Rev.G holder geometry is parametrically suppressible/movable tangentially and no radar PASS is claimed.

## 15. Removal sweep
The fixed holder does not travel with the front carrier.

The carrier/magnet rear capture must clear the exposed target/holder lips during peel.

A swept-solid peel simulation remains required after carrier locators and holder attachment are present in the same DMU.

## 16. Automatic checks
C546 Rev.F 0.5 mm target/DML margin treated as too small for symmetric holder wall.
C547 outward-biased three-sided cassette selected.
C548 no DML-facing holder wall.
C549 target remains 7x7x1.0 mm for coupon consistency.
C550 target magnetic face remains exposed.
C551 holder side-rail seed 0.8 mm.
C552 holder outer-rail seed 0.8 mm.
C553 rear support seed 0.8 mm.
C554 tangential running clearance 0.15 mm/side.
C555 overall tangential holder width 8.9 mm.
C556 holder outward nominal margin to carrier boundary 0.9 mm.
C557 holder nominal outer margin positive.
C558 holder rear support starts behind target.
C559 diagnostic holder rear extent <=Z6.3 mm.
C560 all Z4.1..6.3 holder material prohibited inside DML XY projection.
C561 positive mechanical target retention required.
C562 adhesive-only retention prohibited.
C563 no polymer cover silently added to G_EFF.
C564 exact fixed structural bridge remains open.
C565 long unsupported bridge to rear PC-CF not invented.
C566 ESP32 compatibility remains coarse only.
C567 radar exact mask remains open.
C568 exact peel swept-solid remains open.
C569 holder dimensions remain process-coupon seeds.
C570 real holder kernel generator added.

## 17. State
The 0.5 mm DML margin does not support a conventional symmetric target pocket.

The viable local architecture is an outward-biased cassette with an open DML-facing side.

This preserves target geometry for the magnetic coupon while avoiding consumption of the scarce DML-side clearance.

Status:
**OUTWARD_3SIDED_TARGET_CASSETTE / TARGET_7X7X1_UNCHANGED / DML_SIDE_OPEN / NOMINAL_DML_BOOLEAN_PASS_REQUIRED / C01_TO_C570 / STRUCTURAL_BRIDGE_RADAR_TOLERANCE_PEEL_OPEN**.
