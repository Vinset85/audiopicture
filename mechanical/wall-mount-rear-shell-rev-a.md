# AudioPicture V2.2 Rev.A — rear shell and wall-mount architecture

Status: **PERIMETER_LOAD_PATH_WALL_MOUNT_BASELINE_FROZEN / PRODUCT_MASS_FASTENER_AND_FEA_RELEASE_GATES_OPEN**

## 1. Objective
Define a wall-mount system compatible with:
- 320 x 400 x 40 mm product envelope;
- four full-depth EX25FHE2-4 exclusion columns;
- MAIN-P and MAIN-C local electronics cavities;
- ESP32 antenna keep-out;
- 60 GHz radar keep-out;
- passive thermal airflow;
- removable/serviceable product.

A full-area rear metal plate is prohibited.

## 2. Structural principle
Wall load shall bypass:
- DML panel;
- PORON perimeter compliance layer;
- exciters;
- VOICE isolation carrier;
- RADAR RF window;
- ENV air chamber.

Primary load path:
**product mass -> PC-CF rear structural perimeter -> dedicated mount nodes -> wall cleat/anchors -> wall.**

No product weight shall be reacted through the DML.

## 3. Mount topology
Baseline:
- two separated upper structural engagement points/rail segments;
- two lower anti-rotation/anti-lift support points;
- all attached to PC-CF structural perimeter nodes;
- center rear area remains open.

Preferred user interaction:
1. fix wall rail/cleats;
2. lower AudioPicture onto upper engagement features;
3. product self-seats laterally;
4. lower features prevent rotation;
5. hidden anti-lift lock prevents accidental upward removal.

No visible front fasteners.

## 4. Upper load rail
Use two short metal cleat segments rather than one full-width metal rail.

Initial CAD zones:
- upper-left structural node near product X=25..75 mm;
- upper-right structural node near X=245..295 mm;
- both close to upper perimeter but outside MAIN-C connector/service and ESP32 RF keep-out.

Exact Y/Z depend on MAIN-C final service envelope.

Metal segments must not extend into:
- ESP32 antenna RF-clean volume;
- radar cone;
- exciter exclusion columns.

A non-metallic high-strength cleat is an alternative if RF/packaging demands it, but metal is acceptable at controlled perimeter nodes.

## 5. Lower supports
Two lower supports react:
- wall-normal moment;
- lateral rocking;
- touch/service loads.

They do not need to carry the entire vertical mass under normal installation.

Initial CAD zones:
- lower-left perimeter node;
- lower-right perimeter node.

Use compliant pads to prevent buzz/rattle against the wall.

## 6. Anti-lift
Provide a hidden independent anti-lift feature.

Candidate:
- one or two underside-accessible captive screws/latches;
- accessible without removing the acoustic front;
- not located behind exciter columns.

The anti-lift feature shall not be the primary gravity load path.

## 7. Structural design load
Until final product mass is closed:
- define design vertical load = **4 x final product weight** minimum;
- separately apply wall-normal pull and torsional service loads.

FEA load cases:
A. 4g-equivalent vertical static design case;
B. pull-away from wall;
C. one-corner touch/push;
D. asymmetric support / one upper cleat carrying majority load;
E. installation impact/seating;
F. thermal/print-warp preload.

This 4x factor is an internal engineering design target, not a certification claim.

## 8. Printed structural nodes
PC-CF perimeter/mount nodes:
- no mount screw loads directly into thin shell;
- use local ribs/gussets;
- use metal threaded inserts or captive hardware qualified for PC-CF;
- keep insert heat-set process away from thin cosmetic ASA;
- orient print layers so primary load is not carried only by inter-layer tension.

Initial local rules:
- >=2.5 mm radial material beyond insert as already established;
- generous fillets;
- mount-node ribs tied into perimeter beams;
- avoid abrupt rib termination.

Exact insert size and boss geometry wait for mass/FEA.

## 9. Rear shell
Rear shell is not the primary structural member.

Baseline:
- ASA unfilled cosmetic rear shell;
- approximately 2.0..2.4 mm local skin in exciter projection regions;
- locally thicker/ribbed only where Z-space allows;
- mechanically attached to PC-CF frame.

Do not add rear-shell ribs behind EX25FHE2-4 columns.

## 10. Thermal ventilation
Wall gap and mount topology shall support passive convection.

Create a controlled rear stand-off from the wall rather than placing the whole rear shell flush.

Initial target:
- **3..5 mm wall stand-off** in open convection regions, subject to the 40 mm product-depth definition and industrial-design interpretation.

If the 40 mm maximum must include wall stand-off hardware while installed, this target must be solved inside the 40 mm envelope.

Use:
- hidden lower intake paths;
- vertical rear cavity/chimney;
- hidden upper exhaust paths.

Do not create an acoustic short path around the DML front/rear boundary.

## 11. RF zones
ESP32:
- no wall-mount metal in the antenna keep-out/forward radiation volume;
- avoid PC-CF directly adjacent to antenna.

RADAR:
- no mount metal or carbon-filled structure through the 60 GHz forward cone.

Mount segments shall be placed only after both RF volumes are visible in shared CAD.

## 12. Cable/service access
Provide a lower/side connection bay for:
- 24 V external power;
- Ethernet;
- USB-C service.

Wall mount must permit connector insertion/removal and cable bend radii without taking the product off the wall where practical.

Do not route mains voltage into AudioPicture.

## 13. Installation tolerances
Mount system shall accommodate:
- wall rail placement tolerance;
- printed-frame shrink/warp;
- rear-shell tolerance;
- small wall flatness error.

Use one locating datum and one compliant/slotted secondary feature to avoid over-constraint.

Do not use four rigid precision pins as simultaneous locating features.

## 14. Serviceability
Target:
- hidden anti-lift release;
- lift product upward/off cleats;
- disconnect low-voltage/Ethernet;
- front cosmetic frame remains independently removable.

Electronics service shall not require disturbing DML adhesive/exciter bonds unless the DML assembly itself is being replaced.

## 15. Release gates
1. close total product mass and center of gravity;
2. place exact MAIN-C/RF/service envelopes;
3. select wall-cleat material and exact geometry;
4. select wall-anchor strategy by wall type;
5. select inserts/fasteners;
6. structural FEA with anisotropic printed PC-CF;
7. 4x vertical design-load verification;
8. pull/torsion/one-support fault cases;
9. verify wall stand-off and 40 mm envelope interpretation;
10. verify convection benefit in thermal CFD;
11. verify RF performance with mount hardware;
12. run buzz/rattle modal/contact check.

Status: **TWO_UPPER_CLEATS_TWO_LOWER_SUPPORTS_ANTI_LIFT / CENTER_REAR_METAL_FREE**.
