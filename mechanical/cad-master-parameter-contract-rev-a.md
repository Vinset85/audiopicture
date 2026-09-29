# AudioPicture V2.2 Rev.A — Master CAD parameter contract

Status: **MASTER_DATUM_AND_PARAMETER_MODEL_FROZEN / EXACT_COMPONENT_STEP_IMPORT_GATE**

## 1. Master coordinate system
All mechanical, PCB-placement, FEA and keep-out documents shall use one product coordinate system.

Origin P0:
- front-view lower-left external corner of the product;
- X positive to the right;
- Y positive upward;
- Z positive from the visible front toward the wall/rear.

External nominal envelope:
- PRODUCT_W = 320.0 mm;
- PRODUCT_H = 400.0 mm;
- PRODUCT_D_MAX = 40.0 mm.

No child model may redefine a local product origin without an explicit transform back to P0.

## 2. DML datum
Nominal active structural panel:
- DML_W = 300.0 mm;
- DML_H = 380.0 mm;
- DML_X0 = 10.0 mm;
- DML_Y0 = 10.0 mm;
- DML_Z_FRONT nominally follows the final front/fabric stack;
- DML_STACK_T nominal baseline = 6.0 mm before adhesive/fabric refinements.

DML local coordinates convert to product coordinates:
X_product = DML_X0 + X_dml
Y_product = DML_Y0 + Y_dml.

## 3. Candidate-B master coordinates
Nominal exciter centers in product coordinates:
- EX_L1 = (68, 80) mm;
- EX_L2 = (114, 196) mm;
- EX_R1 = (206, 268) mm;
- EX_R2 = (254, 118) mm.

Each center is a parameter object, not a sketch-only dimension.

Initial radial collision envelope:
- EXCITER_KEEP_OUT_R = 30 mm.

Initial rearward envelope:
- use selected-exciter STEP when available;
- until then reserve >=23 mm from the DML rear mounting plane.

## 4. Front stack parameters
Expose:
- FABRIC_T;
- FRONT_FRAME_T;
- FABRIC_ADHESIVE_T if applicable;
- DML_FRONT_GAP where applicable.

The front visual surface remains planar unless industrial-design work intentionally changes it.

No visible fastener may penetrate the graphic fabric field.

## 5. DML perimeter mount parameters
Expose:
- FOAM_FREE_T = 2.0 mm baseline;
- FOAM_COMPRESSION_NOM = 0.20;
- FOAM_INSTALLED_T = FOAM_FREE_T * (1 - FOAM_COMPRESSION_NOM) = 1.6 mm baseline;
- FOAM_W = 6.0 mm baseline;
- DML_EDGE_LAND = 5..6 mm design range;
- SAFETY_CAPTURE_CLEARANCE.

Hard-stop geometry, not screw torque, defines FOAM_INSTALLED_T.

## 6. Rear structural frame parameters
Expose:
- FRAME_BEAM_W = 8..12 mm range;
- FRAME_WALL_T = 2.4 mm initial;
- FRAME_RIB_T = 2.4..3.0 mm range;
- FRAME_ROOT_FILLET >=1.5 mm where feasible;
- REAR_SHELL_T;
- WALL_MOUNT_DATUM_Z.

Frame sketches shall reference exciter keep-out objects rather than manually duplicated circles.

## 7. Electronics envelope objects
Create placeholder solids before exact STEP import for:
- MAIN PCB nominal 220 x 70 mm plus height map;
- VOICE PCB/SQ66 microphone carrier;
- RADAR PCB plus RF keep-out cone/window;
- ENV PCB plus passive-air chamber;
- RJ45/magnetics;
- Ag53024;
- 24 V connector;
- USB-C;
- TAS5825M/output-filter height zone;
- bulk capacitors and inductors;
- FPC bend/service volumes.

Every placeholder must carry an OPEN/VERIFIED state.

## 8. PCB placement variables
For each PCB expose:
- BOARD_X;
- BOARD_Y;
- BOARD_Z;
- BOARD_ROT_Z;
- BOARD_COMPONENT_SIDE;
- BOARD_CLEARANCE;
- connector service vector.

No PCB location is frozen by this contract.

## 9. Radar RF object
Create a dedicated RADAR_RF_KEEP_OUT solid referenced to the radar PCB coordinate frame.

Until EM optimization:
- treat it as a conservative forward volume;
- exclude carbon-filled polymer, metal inserts, large copper/PCB masses and exciter metal;
- front fabric/radome layers remain separate parameter solids.

The RF volume shall participate in automatic CAD interference checks.

## 10. VOICE acoustic/isolation objects
Create:
- four microphone acoustic-axis objects;
- front acoustic-channel solids;
- VOICE mechanical isolation envelope;
- DML reaction-force exclusion/clearance region.

No structural rib may be added through these objects without explicit review.

## 11. ENV chamber objects
Create separate volumes for:
- room-air inlet/outlet microchannels;
- SHT45 quiet air cavity;
- OPT3004 optical tunnel;
- thermal exclusion distance to MAIN/PoE/amplifier.

These are functional volumes, not leftover voids.

## 12. Connection bay
Expose:
- BAY_X/Y/Z;
- BAY_W/H/D;
- RJ45 service envelope;
- 24V plug service envelope;
- USB-C plug service envelope;
- cable bend envelopes.

External cable/service volumes may extend beyond PRODUCT_D_MAX but must be documented for wall-installation clearance.

## 13. Part decomposition
Master assembly shall contain at minimum:
1. FRONT_FRAME_ASA;
2. FABRIC;
3. DML_PANEL;
4. DML_FOAM_GASKET;
5. DML_SAFETY_CAPTURE;
6. REAR_STRUCTURAL_FRAME_PC_CF;
7. REAR_COSMETIC_SHELL_ASA;
8. MAIN_PCB envelope;
9. VOICE_PCB/carrier;
10. RADAR_PCB/carrier/window;
11. ENV_PCB/chamber;
12. CONNECTION_BAY;
13. WALL_MOUNT_INTERFACE;
14. harness/service-loop envelopes.

Avoid one monolithic printed part.

## 14. Automatic geometry checks
The CAD workflow shall be able to evaluate:
- external envelope <=320 x 400 x 40 mm;
- exciter vs PCB/frame collisions;
- radar keep-out intersections;
- VOICE isolation/acoustic-path intersections;
- ENV thermal-zone intersections;
- minimum rear exciter clearance;
- foam installed gap;
- connector insertion/service clearance;
- PCB removal path;
- wall-mount access.

A passing visual inspection alone is not sufficient.

## 15. STEP import gate
Replace placeholders with exact manufacturer 3D models where trustworthy.

For each imported STEP record:
- manufacturer;
- exact MPN;
- source URL/document revision;
- coordinate/orientation transform;
- verified critical dimensions.

If no trustworthy STEP exists, construct a conservative envelope from the manufacturer mechanical drawing and label it DERIVED_ENVELOPE.

## 16. CAD/FEA configuration states
Master CAD shall support configurations:
- Candidate A;
- Candidate B;
- legacy DAEX25FHE-4 envelope;
- successor EX25FHE2-4 envelope;
- SOFT/NOMINAL/STIFF DML mount;
- service/exploded configuration.

Production release is a named frozen configuration, never merely the latest edited file.

## 17. Output requirements
Before manufacturing release export:
- native parametric CAD;
- STEP assembly;
- individual STEP parts;
- STL/3MF only for qualified printed parts;
- dimensioned PDF drawings for critical interfaces;
- BOM-linked component-placement report;
- interference report;
- mass properties report.

Mesh exports are manufacturing derivatives, not the design master.

## 18. Release rule
Do not freeze cosmetic geometry, PCB positions or frame ribs until exact component envelopes are imported and the automatic collision checks pass.

Status: **MASTER_DATUM_AND_PARAMETER_MODEL_FROZEN / EXACT_COMPONENT_STEP_IMPORT_GATE**.
