# AudioPicture V2.2 — PC-CF front-to-rear perimeter return Rev.I

Status: **SEGMENTED_PERIMETER_RETURN_SELECTED / 8X_WIDE_BLADE_SEEDS / DML_BOOLEAN_ZERO_TARGET / FULL_UNION_NEXT**

## 1. Purpose
Define the missing structural section between the front magnetic target nodes near Z6..9 and the real rear PC-CF ring at Z27..35.

## 2. Existing constraints
Authoritative:
- product 320 x 400 x 40 mm;
- DML hard projection X10..310 / Y10..390;
- DML Z3.3..9.3;
- rear PC-CF ring generic Z27..35;
- rear ASA shell Z37.8..40 and non-primary;
- DML PORON compliant mount is mechanically separate;
- no continuous second front rigid ring.

## 3. Selected topology
Use eight **segmented PC-CF perimeter returns**.

Each return is a short-width wall blade:
- tangential width 10 mm seed;
- radial thickness 2.4 mm seed;
- front overlap starts nominally Z6.0;
- rear overlap reaches nominally Z29.0;
- overlaps the rear ring Z27..29 by 2 mm;
- overlaps the front local tab/holder structural envelope.

These are not slender isolated posts: their section is a 10 x 2.4 mm wall blade aligned with the product perimeter.

They do not join tangentially into a continuous front ring.

## 4. XY placement
Top returns:
Y390.4..392.8.

Bottom:
Y7.2..9.6.

Left:
X7.2..9.6.

Right:
X310.4..312.8.

Thus their DML-facing edge remains nominally outside:
X10 / X310 / Y10 / Y390.

## 5. DML relationship
For Z6..9.3 the returns coexist in Z with the DML.

Therefore exact XY exclusion is mandatory.

Diagnostic target:
**return/DML intersection = 0 mm3**.

No return is permitted to contact the panel or replace PORON.

## 6. Rear-ring overlap
Rear ring begins at Z27.

Return extends to Z29.

Nominal axial overlap:
**2.0 mm**.

Final union shall use filleted/gusseted roots; the 2 mm overlap is only a kernel connectivity seed.

## 7. Front-node overlap
Front tab envelope from Rev.H occupies approximately Z5.1..9.2.

Return begins Z6.0.

Therefore there is nominal Z overlap for real boolean fusion.

Exact holder/tab solid must be included in the combined kernel.

## 8. Shell relationship
ASA shell remains cosmetic/service closure.

PC-CF return is inside the product perimeter and shall preserve nominal shell/frame XY clearance where the shell wraps it.

Shell does not carry magnetic retention load.

## 9. Airflow
Eight local 10 mm-wide returns do not create a full-width horizontal airflow barrier.

Nevertheless top/bottom returns intersect the same perimeter region used by hidden vent architecture.

Therefore final return geometry must be boolean-clipped or tangentially shifted around:
- lower inlet slots;
- upper outlet slots;
- baffles;
- service recess.

No thermal PASS is claimed here.

## 10. ESP32
M1D remains the RF-sensitive magnetic station.

The M1D return may be shortened, shifted tangentially, or suppressed if exact ESP32 antenna mask intersects it.

PC-CF is conductive/RF-relevant material; coarse distance is not sufficient for production release.

## 11. Radar
Exact radar EM mask remains unavailable.

Any right-side return conflicting with the final radar mask must be shifted/suppressed.

Segmented topology permits this without redesigning the entire perimeter.

## 12. Structural seed
Local blade section:
10 x 2.4 mm.

Approximate gross area:
24 mm2.

This is a topology seed only.

No strength, stiffness or buckling PASS is inferred from gross area.

Local FEA must include:
- 5 N normal target load;
- 2 N tangential target load;
- 10 N installation/service proof;
- eccentricity;
- root fillet/gusset;
- PC-CF orthotropy and print orientation.

## 13. Why this is preferable to a post
A narrow post spanning roughly 20 mm would concentrate bending and interlayer peel.

The perimeter blade:
- uses a wider tangential section;
- follows the enclosure perimeter;
- permits broad root gussets into rear ring;
- remains individually suppressible for RF/airflow;
- avoids a second continuous front acoustic boundary.

This is an engineering topology decision, not an FEA result.

## 14. Required combined kernel
Next generator shall import/rebuild:
1. real one-solid rear ring Rev.C;
2. eight Rev.I perimeter returns;
3. eight Rev.H front target-tab envelopes;
4. Rev.G target-holder structural bodies where appropriate.

Then:
- fuse;
- clean;
- check B-rep validity;
- assert primary structural solid count;
- report disconnected fragments;
- boolean DML;
- boolean known electronics/exciter keep-outs.

Only a one-solid result may proceed to local FEA meshing.

## 15. Automatic checks
C621 rear shell remains non-primary structural part.
C622 no continuous second front ring introduced.
C623 eight segmented PC-CF perimeter returns selected.
C624 return tangential width seed 10 mm.
C625 return radial thickness seed 2.4 mm.
C626 return nominal Z6..29.
C627 rear-ring overlap seed 2.0 mm.
C628 front-tab Z overlap present.
C629 top return inner edge remains outside DML.
C630 bottom return inner edge remains outside DML.
C631 left return inner edge remains outside DML.
C632 right return inner edge remains outside DML.
C633 return/DML intersection target zero.
C634 PORON not used in magnetic load path.
C635 ASA shell not credited structurally.
C636 returns do not form full-width airflow barrier.
C637 vent-slot exact collision remains open.
C638 M1D return remains ESP32 RF conditional.
C639 radar-side returns remain EM conditional.
C640 gross blade area not treated as FEA proof.
C641 local orthotropic FEA remains required.
C642 combined rear-frame/return/tab kernel required next.
C643 combined primary solid count must equal one.
C644 disconnected structural fragments prohibited.
C645 exact keep-out booleans remain release gates.

## 16. State
The missing Z6-to-Z27 structural path is now defined as a segmented perimeter wall-return architecture rather than a free-standing post or second rigid front ring.

Status:
**8X_SEGMENTED_PC_CF_RETURNS / 10X2P4MM_BLADE_SEED / Z6_TO_29 / 2MM_REAR_RING_OVERLAP / C01_TO_C645 / COMBINED_ONE_SOLID_KERNEL_NEXT**.
