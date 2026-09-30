# AudioPicture V2.2 Rev.A — master CAD feature tree and derived-model contract

Status: **MASTER_CAD_FEATURE_TREE_FROZEN / SHARED_GEOMETRY_FOR_DMU_FEA_CFD_AND_MANUFACTURING**

## 1. Purpose
Define one parametric source geometry for:
- digital mock-up;
- collision checking;
- structural FEA;
- thermal CFD;
- RF/antenna keep-out review;
- printable structural frame;
- printable rear shell;
- daughterboard carriers;
- front frame;
- service/cable geometry.

STL/3MF are manufacturing derivatives only. They are not design masters.

## 2. Coordinate system
Product master:
- origin P0 = external front lower-left corner;
- +X = right;
- +Y = up;
- +Z = front toward wall/rear;
- product envelope = 320 x 400 x 40 mm.

All imported STEP geometry shall be transformed into this coordinate system through named placement features. Do not destructively edit supplier solids.

## 3. Document/assembly hierarchy
Recommended neutral hierarchy:

AUDIOPICTURE_V22_MASTER
- 00_PARAMETERS
- 01_REFERENCE_GEOMETRY
- 02_SUPPLIER_COMPONENTS
- 03_KEEP_OUTS
- 04_DML_ASSEMBLY
- 05_STRUCTURAL_FRAME_PC_CF
- 06_REAR_SHELL_ASA
- 07_FRONT_FRAME_ASA
- 08_VOICE_CARRIER
- 09_RADAR_CARRIER
- 10_ENV_CARRIER
- 11_MAIN_C_CARRIER
- 12_MAIN_P_CARRIER
- 13_WALL_MOUNT
- 14_HARNESS_AND_CABLES
- 15_AIRFLOW_VOLUMES
- 16_SERVICE_VOLUMES
- 17_ANALYSIS_EXPORTS
- 18_MANUFACTURING_EXPORTS

## 4. Parameter groups

### PRODUCT
- PRODUCT_X = 320
- PRODUCT_Y = 400
- PRODUCT_Z = 40
- WALL_GAP = 4 seed

### DML
- DML_X0 = 10
- DML_Y0 = 10
- DML_X = 300
- DML_Y = 380
- DML_FRONT_Z = approximately 2
- DML_REAR_Z = approximately 8
- PORON_FREE_T = 2.0
- PORON_COMPRESSION = 0.20

### FRAME
- FRAME_WALL = 2.4
- FRAME_RING_W = 10
- FRAME_PRIMARY_RIB = 2.8
- FRAME_MOUNT_RIB = 3.2
- FRAME_GENERAL_FILLET = 1.5
- FRAME_MOUNT_FILLET = 2.0

### PCB Z
- MAIN_P_Z0 = 18.0
- MAIN_P_Z1 = 19.6
- MAIN_C_Z0 = 17.0
- MAIN_C_Z1 = 18.6
- VOICE_Z0 = 12.0
- VOICE_Z1 = 13.6
- RADAR_Z0 = 11.0
- RADAR_Z1 = 12.6
- ENV_Z0 = 12.0
- ENV_Z1 = 13.6

### SERVICE
- CONNECTION_EXIT_X0 = 100
- CONNECTION_EXIT_X1 = 220
- CONNECTION_EXIT_Y0 = 20
- CONNECTION_EXIT_Y1 = 48
- ETH_TUNNEL_Z0 = 22
- ETH_TUNNEL_Z1 = 36

### THERMAL
- INLET_EFFECTIVE_MIN = 600 mm2
- OUTLET_EFFECTIVE_SEED = 750 mm2
- WALL_GAP_CFD = 3 / 4 / 5 mm

## 5. Reference geometry
Create immutable datum objects:
- XY front plane;
- DML front/rear planes;
- PCB Z planes;
- rear inner-shell plane;
- wall plane;
- center X/Y planes;
- lower service datum;
- upper cleat datum;
- airflow axis/reference planes.

All major parts reference datums, not arbitrary faces from neighboring solids.

This prevents topology breakage after feature edits.

## 6. Supplier component policy
Each purchased component is a linked/reference solid with:
- manufacturer;
- MPN;
- source revision/date if available;
- verification class;
- local coordinate transform;
- simplified collision envelope;
- exact STEP where available.

Never remodel an exact supplier component merely to make the assembly prettier.

If exact CAD is unavailable:
- use a clearly named DERIVED_ENVELOPE;
- production release C20 remains failed until resolved where required.

## 7. Keep-out bodies
Keep-outs are first-class solids.

Required:
- EXCITER_L1_KO
- EXCITER_L2_KO
- EXCITER_R1_KO
- EXCITER_R2_KO
- ESP32_RF_KO
- RADAR_RF_KO
- SHT45_AIR_KO
- OPT3004_OPTICAL_KO
- MAIN_C_SERVICE_KO
- MAIN_P_SERVICE_KO
- RJ45_PLUG_KO
- RJ45_LATCH_KO
- ETH_CABLE_SWEEP_KO
- USB_PLUG_KO
- JCP_BEND_KO
- JCS_BEND_KO
- VOICE_FPC_KO
- RADAR_FPC_KO
- ENV_FPC_KO
- CLEAT_SERVICE_KO
- ANTILIFT_SERVICE_KO
- FRONT_REMOVAL_KO
- PCB_REMOVAL_KO.

Frame/shell/carriers are generated after these bodies exist.

## 8. DML assembly
Feature order:
1. DML planform;
2. laminate/core reference layers;
3. perimeter PORON land;
4. hard-stop land;
5. safety capture;
6. exciter supplier solids;
7. exciter wire terminal/service volumes.

DML structural/acoustic FEA receives its own analysis simplification from this assembly.

## 9. PC-CF structural frame
Feature order:
1. outer ring sketch;
2. base ring extrusion;
3. DML support ring;
4. upper cleat islands;
5. M4 bosses;
6. left/right load rails;
7. local bridges;
8. MAIN-C/P support islands;
9. VOICE isolated-anchor islands;
10. radar-side truncated support;
11. ENV low-conduction support;
12. lower service-opening reinforcement;
13. lower wall supports;
14. anti-lift node;
15. subtract all hard keep-outs;
16. add local gussets;
17. apply fillets last;
18. mass-property check.

Do not pattern structural ribs blindly through keep-outs.

## 10. ASA rear shell
Feature order:
1. external rear surface;
2. shell/thickness;
3. wall-gap feet interfaces;
4. lower inlet slots;
5. upper outlet slots;
6. service/cable recess;
7. Ethernet tunnel shaping;
8. USB service aperture;
9. labels ETH / 24V / USB;
10. assembly interfaces to PC-CF;
11. subtract RF/air/service keep-outs;
12. cosmetic fillets/chamfers last.

Rear shell is not credited as the sole primary structural path.

## 11. Front frame
Front frame:
- retains acoustic fabric;
- hides all sensors;
- provides magnetic removable interface;
- does not preload active DML;
- provides controlled optical/acoustic/RF windows through material choice/thickness rather than visible holes where feasible.

Magnets and steel targets become explicit supplier solids/keep-outs before production freeze.

## 12. Carrier philosophy
Each PCB carrier is a separate parametric part.

VOICE:
- compliant/vibration-isolated;
- no rigid bridge under mic array.

RADAR:
- unfilled nonconductive material in forward RF region;
- no PC-CF in cone.

ENV:
- thermally weak support;
- separate SHT45 chamber;
- optical tunnel.

MAIN-C/P:
- local standoffs/rails only;
- open airflow;
- service/removal access.

## 13. Harness solids
Harnesses are swept-volume CAD objects.

Each has:
- center path;
- nominal OD/width;
- bend radius;
- connector straight-exit;
- clip positions;
- assembly/removal sweep.

At minimum model:
- JCP;
- JCS;
- VOICE FPC;
- RADAR FPC;
- ENV FPC;
- LEFT speaker branch;
- RIGHT speaker branch;
- Ethernet cable;
- 24 V cable.

## 14. Airflow volumes
Create CFD fluid domains from the same master:
- lower room-air inlet;
- rear electronics cavity;
- vertical chimney;
- side bypass;
- upper outlet;
- 4 mm wall gap;
- SHT45 chamber as separate fluid domain.

Cable/component solids are included as obstructions.

## 15. Analysis configurations
Use derived configurations, not separate manually redrawn CAD.

### DMU_FULL
All relevant exact/simplified solids + keep-outs.

### FEA_FRAME
Suppress:
- cosmetic fabric;
- electronics detail not contributing load;
- tiny cosmetic features.

Retain:
- structural frame;
- inserts/interfaces;
- mass representations;
- service cutout.

### CFD_SYSTEM
Retain:
- heat-source envelopes;
- shell/frame obstructions;
- cables;
- wall gap;
- inlet/outlet.

Suppress irrelevant tiny fastener detail.

### RF_REVIEW
Retain:
- conductive/metal/carbon-filled bodies;
- radar/ESP antenna references;
- radome/shell dielectric region.

## 16. Export contract
Neutral engineering:
- STEP AP242 preferred;
- exact units mm;
- product coordinate system preserved.

Analysis:
- STEP/Parasolid where solver supports;
- mesh is disposable derivative.

Manufacturing:
- 3MF preferred for additive manufacturing;
- STL permitted as derivative only;
- never edit STL and feed it back as master geometry.

Drawing:
- PDF/DXF only from released CAD revision.

## 17. Naming and revision
Part names:
AP22_<SYSTEM>_<PART>_REV_<LETTER>

Examples:
- AP22_MECH_FRAME_REV_B
- AP22_MECH_REAR_SHELL_REV_A
- AP22_CARRIER_VOICE_REV_A

Every export records:
- source CAD revision;
- git commit/document contract;
- date;
- material/process;
- units.

## 18. Automatic geometry tests
C01..C96 remain authoritative.

Add:
C97 all major solids reference master datums.
C98 supplier solids retain source metadata.
C99 hard keep-outs exist before structural generation.
C100 frame boolean subtract succeeds without invalid body.
C101 rear-shell boolean subtract succeeds.
C102 no carrier crosses assigned PCB removal sweep.
C103 harness sweeps have defined bend radii.
C104 CFD fluid domain is continuous inlet-to-outlet.
C105 SHT45 fluid domain remains separately coupled to room.
C106 RF review contains all conductive/carbon-filled bodies.
C107 STEP export preserves 320 x 400 x <=40 envelope.
C108 3MF/STL checksum/revision maps to released master.
C109 mass properties are generated from released solids.
C110 no mesh/STL-derived geometry is used as design master.

## 19. Geometry release stages
G0 — skeleton:
- datums;
- product envelope;
- DML;
- PCB boxes;
- keep-outs.

G1 — packaging:
- supplier STEP;
- carriers;
- harness sweeps;
- service volumes.

G2 — structural:
- PC-CF frame;
- cleats;
- supports;
- anti-lift.

G3 — shell:
- rear/front ASA;
- vents;
- service recess;
- fabric/magnets.

G4 — analysis:
- DMU C01..C110;
- FEA;
- CFD;
- RF review;
- acoustic coupling review.

G5 — manufacturing release:
- final STEP;
- 3MF;
- drawings;
- BOM links;
- print parameters.

## 20. Immediate CAD blockers
Before G1 can be declared complete:
1. EX25FHE2 exact STEP/import;
2. Ag53024 exact envelope/CAD;
3. TE 2-1734264-1 exact CAD;
4. Wurth 7490220121 exact CAD;
5. USB4085 exact CAD;
6. exact cleat coordinate/detail;
7. actual FPC constructions/bend radii;
8. magnet/target selection for front frame.

These do not block building G0 skeleton now.

Status: **G0_SKELETON_SPEC_READY / ONE_MASTER_GEOMETRY / STEP_AP242_NEUTRAL / 3MF_STL_DERIVATIVE_ONLY / C01_TO_C110**.
