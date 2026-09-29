# AudioPicture V2.2 Rev.A — Rear structural frame

Status: **REAR_FRAME_PARAMETRIC_ARCHITECTURE_FROZEN / CAD_COLLISION_AND_STRUCTURAL_FEA_GATE**

## 1. Purpose
The rear structural frame is the primary load-bearing member between wall mount, enclosure shell and electronics. The DML panel is mechanically downstream through its compliant perimeter mount and safety capture.

The frame shall NOT behave as a full-area rigid backplate directly coupled to the DML.

## 2. Coordinate system and envelope
Product datum:
- X = 0..320 mm left-to-right;
- Y = 0..400 mm bottom-to-top;
- Z = 0..40 mm front-to-rear.

Centered DML nominal field:
- X = 10..310 mm;
- Y = 10..390 mm.

Maintain the previously defined Candidate-B exciter keep-outs.

## 3. Frame topology
Baseline topology:
- closed outer structural perimeter;
- narrow DML support/hard-stop perimeter;
- one primary vertical electronics spine;
- local transverse bridges only where required for PCB carriers, wall mount and connection bay;
- isolated VOICE carrier;
- independent RADAR and ENV carriers.

Avoid a continuous rear web behind the active panel.

## 4. Outer structural perimeter
Initial CAD parameters:
- perimeter beam projected width: 8..12 mm;
- printed-wall/rib thickness: 2.0..3.0 mm baseline;
- corner radii rather than sharp internal corners;
- local thickening only at wall-mount and fastener load paths.

Exact section depends on print material/orientation and structural FEA.

## 5. DML hard-stop ring
A narrow hard-stop datum controls the compressed PORON gap.

Baseline:
- PORON free thickness 2.0 mm;
- nominal compressed thickness 1.6 mm;
- frame stop sets this nominal gap;
- stop is discontinuous/local where needed to avoid forming a second stiff acoustic clamp;
- safety capture retains the panel with clearance under normal operation.

No screw torque may determine DML foam compression.

## 6. Primary electronics spine
Reserve a vertical structural corridor for PCB-A MAIN.

Initial parametric corridor:
- usable board length target >=220 mm;
- usable width target >=70 mm before local keep-out reconciliation;
- standoffs attached to the rear frame/spine, never to the DML;
- component side faces the available rear cavity according to final height map;
- local apertures/notches permitted around exciter cylinders.

The exact X location is selected by 3D collision solve, not frozen numerically in this document.

## 7. PCB carrier philosophy
Use replaceable/local carriers or bosses rather than making every PCB feature integral to the cosmetic shell.

MAIN:
- rigidly referenced to structural spine;
- amplifier zone close to speaker harness exits;
- Ethernet/24V/USB service end close to connection bay.

VOICE:
- separate compliant/isolation carrier;
- no shared fastener/post with DML stop ring;
- controlled microphone acoustic paths.

RADAR:
- low-mass non-conductive carrier;
- no metallic fastener in RF window unless EM-qualified.

ENV:
- thermally isolated edge carrier;
- mechanically open to passive-air chamber.

## 8. Rear connection bay
Provide one recessed lower/side service bay carrying:
- RJ45;
- locking 24 V input;
- USB-C service port.

Requirements:
- connector insertion/removal loads react into structural frame;
- bay does not load the DML perimeter;
- enough external finger/cable clearance for installation;
- strain relief occurs on frame side;
- Ethernet shield/chassis strategy remains an electrical/EMC gate.

Bay position remains parametric until MAIN connector edge is frozen.

## 9. Wall-mount load path
Wall loads shall flow:
wall interface -> rear structural frame -> outer perimeter/shell.

They shall not flow through:
- DML panel;
- PORON mount;
- VOICE isolation carrier;
- RADAR PCB.

Provide at least two independent load paths / retention features appropriate to final wall-mount design. Exact bracket system remains open.

## 10. 3D-print design rules
Until final polymer/process is selected:
- avoid large flat unsupported skins where warpage is likely;
- use filleted ribs and closed load paths;
- avoid thin tall posts without gussets;
- use heat-set inserts only in structural regions with adequate surrounding material;
- orient critical insert pull-out loads into reinforced bosses;
- separate cosmetic front frame from structural rear frame where this improves print/service quality.

No production wall/rib thickness is frozen without material/process selection and structural FEA.

## 11. Acoustic isolation rules
Frame ribs must remain outside exciter keep-outs and shall not touch the moving panel.

Provide:
- >=2 mm nominal dynamic/service clearance behind exciter bodies;
- flexible harness loops;
- no loose unsupported wire capable of buzzing against the DML;
- no large rear plate within the immediate DML cavity unless acoustic simulation proves acceptable.

## 12. Thermal integration
The frame may act as a heat-spreading support only where this does not create a DML/VOICE bridge.

Create local thermal zones for:
- PoE module;
- 5 V conversion;
- TAS5825M/output filter.

Do not thermally couple the SHT45 chamber to these zones.

## 13. Parametric CAD master variables
The future CAD model shall expose at minimum:
- PRODUCT_W = 320 mm;
- PRODUCT_H = 400 mm;
- PRODUCT_D_MAX = 40 mm;
- DML_W = 300 mm;
- DML_H = 380 mm;
- DML_STACK_T;
- FOAM_FREE_T = 2.0 mm;
- FOAM_COMPRESSION_NOM = 20%;
- FRAME_BEAM_W;
- FRAME_WALL_T;
- EXCITER_KEEP_OUT_R = 30 mm initial;
- MAIN_BOARD_W/H;
- PCB carrier Z offsets;
- rear-shell thickness;
- connector-bay X/Y/W/H/D.

Candidate-A/B coordinates shall be referenced from the same master datum.

## 14. Structural simulation cases
Before frame freeze evaluate:
1. self-weight, wall-mounted vertical;
2. connector insertion/removal loads;
3. assembly clamp/fastener loads;
4. reasonable handling load;
5. DML harmonic reaction forces;
6. thermal distortion;
7. print tolerance/warpage sensitivity.

Report frame displacement at DML hard-stop datums and VOICE carrier acceleration.

## 15. Release gate
Rear-frame geometry freezes only after:
- exact component STEP collision check;
- selected print material/process;
- wall-mount concept;
- static structural FEA;
- DML harmonic reaction-force mapping;
- VOICE isolation verification;
- thermal simulation;
- assembly/service review.
