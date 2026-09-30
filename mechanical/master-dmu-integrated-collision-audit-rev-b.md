# AudioPicture V2.2 Rev.B — integrated master DMU collision audit

Status: **MASTER_DMU_REV_B_ASSEMBLY_CONTRACT_DEFINED / FRONT_Z_DATUM_RECONCILIATION_REQUIRED / FULL_EXACT_STEP_AUDIT_OPEN**

## 1. Purpose
Integrate the real structural-frame and front-carrier B-rep results with the current AudioPicture subsystem envelopes and audit the complete 320 x 400 x 40 mm package.

This audit distinguishes:
- hard collisions;
- intentional interfaces;
- coarse-envelope overlaps;
- unresolved exact-STEP gates.

## 2. Assembly components
DMU assembly includes:
- FRONT_CARRIER real B-rep;
- printed acoustic fabric envelope;
- DML 300 x 380 panel;
- four EX25FHE2 coarse verified-drawing envelopes;
- PC-CF structural frame real B-rep;
- rear ASA shell envelope;
- MAIN-C;
- MAIN-P;
- VOICE;
- RADAR;
- ENV;
- Ag53024 conservative envelope;
- horizontal 470 uF envelope;
- RJ45 plug/latch/cable tunnel;
- wall cleats/lower supports;
- vent/airflow volumes;
- harness/FPC corridors.

## 3. Critical datum reconciliation
The previous front-carrier CAD diagnostic used its own local Z=0..3.2 mm construction coordinates.

That local B-rep Z must NOT be interpreted directly as product-global Z.

Product-global front stack must preserve:
- fabric outer surface at product Z=0 reference;
- carrier local thickness behind the fabric;
- fabric-to-DML minimum gap >=2.0 mm;
- DML structural stack;
- rear component clearances;
- rear shell outer surface <=Z40.

Therefore the front carrier requires an assembly transform in master DMU.

## 4. Front-stack assembly transform
Define:
Z_FABRIC_OUTER = 0.0 mm.

Fabric thickness seed:
T_FABRIC = 0.5 mm.

Nominal clear gap from fabric rear surface to DML front:
G_FABRIC_DML = 2.8 mm.

Thus DML front nominal plane:
Z_DML_FRONT = 0.5 + 2.8 = **3.3 mm**.

For DML structural thickness approximately 6.0 mm:
Z_DML_REAR ~= **9.3 mm**.

This supersedes the older coarse DML Z~2..8 packaging seed for the integrated nominal front-stack datum.

The 40 mm closure must therefore be rechecked using Z_DML_REAR ~9.3 mm.

## 5. Exciter depth consequence
EX25FHE2 rear depth:
25.5 +/-0.5 mm from DML mounting/rear reference as previously verified.

Using conservative 26.0 mm rearward extent from Z_DML_REAR:
Z_EXCITER_REAR ~= 9.3 + 26.0 = **35.3 mm**.

Add preferred 1.0 mm rigid static clearance:
required free envelope to approximately:
**Z36.3 mm**.

Rear shell inner plane at 2.2 mm wall:
Z37.8 mm.

Residual nominal shell clearance:
**~1.5 mm**.

Result:
40 mm product depth remains geometrically plausible, but margin is now much smaller than the older coarse ~2.8 mm estimate.

## 6. Front carrier placement
The carrier supports fabric around the perimeter and must not occupy the central fabric-to-DML air gap as a full plate.

Global placement rule:
- visible fabric defines Z0;
- perimeter carrier sits behind/wrapped by fabric;
- local carrier/magnet pads are allowed only over DML perimeter/non-active legal regions;
- no 3.2 mm pad may intrude into active DML clearance zone.

Therefore magnet-pad collision is checked in XY before accepting its global Z.

## 7. Magnet-pad vs DML projected geometry
DML projected area:
X10..310
Y10..390.

All eight current magnet centers lie within or near this projected rectangle except side/perimeter edge cases.

A simple circular magnet pad at:
- M1/M2 Y386;
- M3/M4 Y14;
- M5/M6 X14;
- M7/M8 X306

is only 4 mm from the DML projected edge at its center.

With 12 mm pad diameter, pad geometry extends into the DML projected region.

This is a real packaging warning.

## 8. Magnet station redesign requirement
Current 12 mm local pads cannot be assumed legal merely because magnet centers are perimeter-biased.

Required options:
A. reduce/local-shape pad inward/outward around DML edge;
B. move magnet centers closer to product perimeter where shell/carrier wall permits;
C. create DML perimeter notch/clearance only if acoustically/structurally legal;
D. move target/magnet architecture rearward to a non-DML-overlap perimeter interface.

Preferred:
**reshape/move magnetic stations rather than modify active DML.**

No DML notch is baseline.

## 9. Proposed revised magnetic center seed
Move stations 2 mm toward product perimeter where possible:

Top:
M1B = (70,388)
M2B = (250,388)

Bottom:
M3B = (70,12)
M4B = (250,12)

Left:
M5B = (12,135)
M6B = (12,275)

Right:
M7B = (308,135)
M8B = (308,315).

Use asymmetric/D-shaped station pads whose DML-facing edge remains outside the DML hard-clearance zone.

Exact pad shape becomes a master-DMU-driven feature.

## 10. Rear Z closure
Rear shell:
- outer Z40.0
- inner Z37.8 nominal.

EX25FHE2 conservative:
- rear ~Z35.3
- +1 mm clearance target -> Z36.3.

Remaining:
~1.5 mm.

This is PASS at nominal geometry but classified:
**TIGHT / EXACT STEP AND TOLERANCE REQUIRED**.

## 11. MAIN-C
MAIN-C:
Z17.0..18.6 PCB.

Ag53024 conservative top:
~Z32.6..33.6 depending reference.

Rear-shell inner:
Z37.8.

Clearance:
>4 mm class in current conservative model.

PASS coarse.

## 12. MAIN-P
MAIN-P:
Z18.0..19.6 PCB.

Horizontal 470 uF:
~12 mm rear envelope class.

Top:
~Z31.6 class depending cradle reference.

Rear-shell inner:
Z37.8.

PASS coarse.

## 13. VOICE
VOICE PCB:
Z12.0..13.6 previous seed.

After front-stack datum reconciliation, the relationship between VOICE microphones, fabric and DML must be re-derived.

The previous ~4 mm DML separation statement is no longer authoritative without transforming VOICE into the revised global front datum.

Status:
**Z_REMAP_REQUIRED**.

## 14. RADAR
RADAR PCB:
previous Z11.0..12.6 seed.

Its antenna-to-fabric/radome distance must be recomputed from revised front stack.

XY coarse packaging remains viable.

Status:
**Z_REMAP_AND_EM_REQUIRED**.

## 15. ENV
ENV PCB:
previous Z12.0..13.6.

SHT45 room-air chamber and OPT3004 optical path require revised front/rear datum mapping.

XY remains coarse PASS.

Status:
**Z_REMAP_REQUIRED**.

## 16. Structural frame
Real frame B-rep bounding Z depth:
8 mm local model extent.

Like the front carrier, its local CAD Z origin must be transformed to product-global placement.

No collision conclusion shall be derived from raw local B-rep Z alone.

Frame XY topology remains valid.

## 17. Wall-mount rear region
Wall cleats/lower supports remain behind/integrated with rear structural region.

No full rear metal plate.

Center rear remains metal-free where RF architecture requires.

PASS architecture-level.

## 18. Ventilation
Rev.B vent targets:
- inlet gross 1440 mm2;
- outlet gross 1350 mm2;
- effective seeds ~1080 mm2 each.

Master DMU must subtract actual:
- structural frame blockage;
- cable blockage;
- shell retention nodes.

Area targets remain valid but exact effective area awaits shell solid/CFD.

## 19. Collision classification
### PASS coarse
- MAIN-P vs exciters
- MAIN-C vs exciters
- MAIN-C/Ag53024 vs rear shell
- MAIN-P/bulk capacitor vs rear shell
- PCB XY placement vs current exciter boxes
- wall mount architecture vs central RF policy.

### WARNING / redesign
- front magnet station pad vs DML projected perimeter.

### REMAP
- VOICE Z
- RADAR Z
- ENV Z
- PC-CF frame local-to-global Z.

### EXACT STEP gate
- EX25FHE2
- Ag53024
- RJ45/plug/boot
- MAIN board tall components
- final shell.

## 20. 40 mm closure state
With revised front datum:
- DML rear ~Z9.3;
- exciter conservative rear ~Z35.3;
- desired rigid clearance to ~Z36.3;
- shell inner Z37.8;
- shell outer Z40.

Nominal closure:
**PASS with ~1.5 mm residual behind worst exciter clearance envelope**.

This is materially tighter than previous coarse packaging.

No further front-stack thickness may be added casually.

## 21. Design consequence
Freeze global product Z datum now.

All subsystem Z coordinates shall be remapped from this master datum before further mechanical release.

Do not continue mixing local CAD coordinates and historical coarse product Z seeds.

## 22. Automatic checks
C381 master DMU uses one product-global coordinate system.
C382 local front-carrier Z is transformed before collision checks.
C383 fabric outer datum fixed at Z0.
C384 fabric thickness seed recorded.
C385 nominal DML front plane recalculated.
C386 nominal DML rear plane recalculated.
C387 EX25FHE2 rear envelope recalculated.
C388 40 mm closure re-evaluated after front-stack reconciliation.
C389 nominal worst-exciter rear clearance positive.
C390 magnet pad/DML projected overlap detected.
C391 magnetic station redesign required before front release.
C392 DML notch not accepted as baseline solution.
C393 MAIN-C rear clearance remains positive.
C394 MAIN-P rear clearance remains positive.
C395 VOICE Z remap flagged.
C396 RADAR Z remap flagged.
C397 ENV Z remap flagged.
C398 frame local/global Z transform required.
C399 exact STEP gates preserved.
C400 no subsystem may use obsolete coarse Z seed after master remap.

## 23. State
The integrated audit found two important facts:

1. The 40 mm enclosure still closes nominally, but worst-exciter rear margin is now only about 1.5 mm after correctly including fabric gap and DML thickness.

2. The current 12 mm magnet pads overlap the DML projected perimeter and must be reshaped/repositioned.

This is a useful DMU correction, not a release failure.

Status:
**MASTER_Z_DATUM_RECONCILED / 40MM_NOMINAL_PASS_WITH_1P5MM_EXCITER_MARGIN / MAGNET_PAD_REDESIGN_REQUIRED / C01_TO_C400**.
