# AudioPicture V2.2 Rev.A — system mass and center-of-gravity budget

Status: **SYSTEM_MASS_FIRST_ORDER_1P55KG_NOMINAL / CAD_VOLUME_AND_CG_RELEASE_GATE**

**Historical first-order allocation, not the current assembled mass.**
Rev.FC identifies stale shell mass and an exciter-model mismatch in this
budget. See `system-mass-review-rev-fc.md` and
`../evidence/rev-fc/mass-budget-review.json`. The original values below are
retained as history; do not use 1.55 kg or its apparent headroom as a current
production claim. The 250 g frame allocation is an optimization target;
the product mass and structural acceptance gates remain independent.

## 1. Purpose
Create a first-order product mass budget before detailed shared CAD volume extraction.

The objective is to:
- bound wall-mount loads;
- estimate center-of-gravity direction;
- identify dominant mass items;
- provide a mass target for rear-frame optimization.

Values are nominal engineering estimates unless explicitly tied to manufacturer data.

## 2. DML assembly

### A1 structural panel
Previously closed first-order mass:
- two GFRP skins + 5 mm ROHACELL 51 IG-F core:
**~241 g**

This excludes adhesive, fabric and edge/mount materials.

### Exciters
4 x EX25FHE2-4:
- current distributor/manufacturer-family mass anchor: approximately 113 g each.

Budget:
**452 g**

### DML adhesive / exciter bonding / local tapes
Reserve:
**25 g**

DML + exciters subtotal:
**~718 g**

This is already the dominant product mass block.

## 3. Front cosmetic/acoustic system
Printed acoustic fabric:
- reserve 35 g

Magnetic removable front-frame polymer/magnets/adhesive:
- reserve 90 g

Subtotal:
**125 g**

Exact textile areal density and magnet count remain open.

## 4. Electronics

### MAIN-P
PCB 115 x 45 x 1.6 mm plus copper:
- bare-board first estimate ~18 g

Components:
- 470 uF capacitor;
- 4 x XAL7050;
- TAS5825M;
- power converters/protection;
- connectors;
- passives.

Component reserve:
~45 g

MAIN-P subtotal:
**~63 g**

### MAIN-C
PCB 150 x 55 x 1.6 mm:
- bare-board first estimate ~29 g

Components:
- Ag53024;
- RJ45/magnetics;
- ESP32;
- W5500;
- USB-C;
- connectors/passives.

Component reserve:
~55 g

MAIN-C subtotal:
**~84 g**

### VOICE / RADAR / ENV
Three daughterboards plus components/carriers:
- VOICE ~30 g
- RADAR ~18 g
- ENV ~10 g

Subtotal:
**~58 g**

### Harnesses/cables
- speaker wiring;
- JCP;
- JCS FPC;
- daughterboard FPCs;
- connection-bay wiring.

Reserve:
**45 g**

Electronics + harness subtotal:
**~250 g**

This subtotal must be replaced by BOM-derived component masses and final PCB Gerber mass estimates.

## 5. Structural frame
PC-CF rear structural perimeter, ribs, carriers, bosses and gussets.

No exact CAD volume yet.

First design allocation:
**220 g nominal**
with working range:
**170..280 g**

This is a mass-control target, not a measured prediction.

Frame mass shall be optimized after anisotropic FEA rather than minimized before structural solve.

## 6. Rear shell
ASA unfilled cosmetic rear shell, local 2.0..2.4 mm skins and required local features.

First allocation:
**150 g nominal**
working range:
**110..210 g**

Do not thicken the full shell merely to gain stiffness; stiffness belongs primarily in the PC-CF frame.

## 7. Wall-mount / fasteners / magnets
Product-side cleat hardware, inserts, anti-lift, fasteners, pads and remaining magnets:
**85 g nominal**
working range:
**60..120 g**

Wall-side anchors/screws are excluded from product mass unless shipped/attached to the product.

## 8. First-order total
Nominal:
- DML/exciters: 718 g
- front system: 125 g
- electronics/harness: 250 g
- PC-CF frame: 220 g
- ASA rear shell: 150 g
- product-side hardware: 85 g

Total:
**~1548 g = 1.55 kg**

Working uncertainty range using structural/shell/hardware bounds and current electronics uncertainty:
**approximately 1.35..1.80 kg**

Set provisional product mass target:
**<=1.7 kg nominal production configuration**

Do not treat 1.55 kg as a final specification.

## 9. Wall-mount design load
Using the current nominal mass:
- weight ≈15.2 N at 1g;
- 4x vertical internal design case ≈60.7 N.

Using the provisional 1.7 kg target:
- weight ≈16.7 N;
- 4x vertical design case ≈66.7 N.

Use **70 N minimum vertical structural design load** for the next wall-mount FEA.

Also run the previously defined asymmetric one-cleat, pull-away and torsional cases.

This is an internal engineering load case, not a wall-anchor certification rating.

## 10. Center-of-gravity direction
Exact XYZ CG requires CAD masses.

Qualitative result:
- four exciters (~452 g) plus DML (~241 g) put ~693 g close to the front active assembly;
- MAIN-C is high in Y;
- MAIN-P is central/lower;
- frame/shell shift mass rearward.

Therefore the Z center of gravity is expected to remain closer to the DML/front half than a conventional rear-electronics enclosure.

This is favorable for wall pull-out moment compared with placing a large rear heatsink/transformer at Z~40 mm.

Y-CG may shift slightly upward due to MAIN-C/wall-mount hardware, but exciter placement dominates the moving assembly distribution.

No numeric CG coordinate is released until shared CAD volumes and component masses are assigned.

## 11. Mass-control rules
1. do not add full-area metal plates;
2. do not solve local frame weakness by globally thickening PC-CF;
3. use ribs/gussets along load paths;
4. keep cosmetic ASA non-structural where possible;
5. use local inserts only at real load/service nodes;
6. maintain DML mass model separately from enclosure mass;
7. every >20 g CAD change triggers mass-budget review;
8. every >50 g asymmetric change triggers CG review.

## 12. Release gates
1. extract PC-CF volume from master CAD;
2. extract ASA shell/front-frame volumes;
3. assign actual printed densities from qualified coupons;
4. replace PCB estimates with stackup/Gerber mass;
5. attach manufacturer component masses where available;
6. include exact magnets/inserts/cleats;
7. compute XYZ CG;
8. update wall-mount FEA with final mass distribution;
9. verify shipping/drop loads separately;
10. freeze production mass target/tolerance.

Status: **NOMINAL_MASS_1P55KG / WORKING_RANGE_1P35_TO_1P80KG / NEXT_WALL_FEA_VERTICAL_LOAD_70N**.
