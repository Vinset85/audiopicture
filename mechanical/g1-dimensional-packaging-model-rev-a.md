# AudioPicture V2.2 Rev.A — G1 dimensional packaging model

Status: **G1_DIMENSIONAL_MODEL_DEFINED / COARSE_COLLISION_PASS_WITH_EXACT_STEP_GATE_OPEN**

## 1. Master envelope
Coordinate system P0 front lower-left:
- X 0..320 mm
- Y 0..400 mm
- Z 0..40 mm

DML:
- X 10..310
- Y 10..390
- Z approximately 2..8

Rear rigid inner limit seed:
- Z approximately 37.6..38.0
- generic component static limit approximately Z 36.6

## 2. EX25FHE2-4 keep-outs
Use conservative coarse envelopes until manufacturer solid import:
- projected XY box: 62 x 60 mm
- rear depth keep-out to approximately Z35

Centers:
- L1 (68,80)
- L2 (114,196)
- R1 (206,268)
- R2 (254,118)

Boxes:
- L1 X37..99 Y50..110
- L2 X83..145 Y166..226
- R1 X175..237 Y238..298
- R2 X223..285 Y88..148

These are full-depth structural/electronics exclusion columns to Z35 class.

## 3. MAIN-P
PCB:
- X105..220
- Y112..157
- Z18.0..19.6

Rear component allowance:
- generic approximately 17 mm.

PVDD bulk capacitor:
- horizontal envelope 20 x 12 x 12 mm;
- locate within MAIN-P free local area;
- no exciter-column intersection;
- nonconductive retention cradle required.

Result:
**COARSE PASS**

## 4. MAIN-C
PCB:
- X85..235
- Y315..370
- Z17.0..18.6

C1 Ethernet/PoE:
- product X85..140

C2 PoE/W5500/USB:
- product X140..190

C3 ESP32/FPC:
- product X190..235

### Ag53024
Manufacturer family envelope:
- 57 x 18 x 14 mm class.

Conservative CAD KO:
- 58 x 19 x 15 mm.

Place long axis primarily along MAIN-C X where electrical floorplan permits.
Rear top with 15 mm KO:
- Z approximately 33.6
- residual to generic limit approximately 3.0 mm.

**PASS**

### RJ45
TE 2-1734264-1:
- 13.2 mm connector-height class.
- lower edge C1 direct access.
- seed center approximately X110/Y315.
- mating direction downward Y.

Body-height first-order:
**PASS**

Plug/latch/cable are separate swept keep-outs.

### Ethernet magnetics
Wurth 7490220121:
- exact manufacturer STEP required at G1-EXACT;
- reserve a conservative local C1/C2 collision body until imported.

### USB-C
GCT USB4085:
- 3.46 mm profile;
- 9.17 mm body-length class.
- service connector, not normal installed cable.

**PASS**

## 5. VOICE
PCB:
- X119..201
- Y20..102
- Z12.0..13.6

Mic centers:
- (126.7,26.7)
- (193.3,26.7)
- (193.3,93.3)
- (126.7,93.3)

Carrier:
- separate compliant-isolated solid;
- rear service volume must remain below connection/tunnel geometry.

Coarse XY vs L1:
- nearest boundary gap approximately 20 mm in X.

**PASS**

## 6. RADAR
PCB:
- X249..287
- Y184..216
- Z11.0..12.6

Forward RF keep-out:
- conservative packaging cone, 45-degree half-angle seed only;
- not an antenna-pattern claim.

No:
- PC-CF;
- metal;
- copper-heavy carrier;
- cable bundle
in forward cone.

**COARSE PASS / EM GATE OPEN**

## 7. ENV
PCB:
- X252..294
- Y35..59
- Z12.0..13.6

Separate:
- SHT45 room-air chamber;
- OPT3004 optical tunnel.

Keep thermally isolated from structural frame and main hot chimney.

**COARSE PASS**

## 8. Wall mount
Upper left cleat seed:
- X30..75
- Y350..382

Upper right cleat seed:
- X245..290
- Y350..382

Two lower support pads:
- exact X/Y to follow frame topology.

Wall gap:
- 4 mm nominal seed.

Anti-lift:
- lower reinforced PC-CF node.

No full rear metal plate.

## 9. Connection/service system
Lower service recess seed:
- X100..220
- Y20..48
- rear Z22..40

This is a cable-exit/service recess, not a requirement to relocate all electrical connectors.

Ethernet:
- RJ45 remains MAIN-C;
- direct plug mating;
- passive rear cable tunnel;
- lower cable exit.

24 V:
- MAIN-P ownership retained;
- short protected/mechanically controlled internal route only if direct access is impossible.

USB:
- MAIN-C service access.

## 10. Harness layers
SIGNAL/FPC:
- Z14..18

POWER:
- Z20..26

SPEAKER:
- Z20..28

No swept harness volume may enter any exciter column.

## 11. Thermal fluid geometry
Preserve:
- lower effective inlet >=600 mm2 with cables installed;
- upper outlet seed 750 mm2;
- continuous rear chimney;
- nominal wall gap 4 mm.

No full-width frame/harness curtain.

## 12. Structural frame seed
PC-CF:
- closed outer ring;
- nominal ring width 10 mm;
- general wall 2.4 mm;
- primary rib 2.8 mm;
- mount rib 3.2 mm;
- dual side load rails;
- local bridges only.

All hard keep-outs are subtracted before fillets/gussets.

Frame target mass <=250 g.

## 13. G1 dimensional collision matrix
Current first-order results:

- DML vs product envelope: PASS
- exciters vs product Z: PASS conditional, approximately Z35 class
- MAIN-P vs exciters: PASS
- MAIN-C vs exciters: PASS
- VOICE vs L1/L2: PASS
- RADAR vs R1/R2: PASS coarse
- ENV vs R2: PASS coarse
- Ag53024 vs rear shell limit: PASS, approximately 3 mm conservative residual
- RJ45 body vs rear shell limit: PASS
- USB4085 vs rear shell limit: PASS
- PVDD horizontal capacitor vs rear shell: PASS
- upper cleats vs DML active region: packaging pass, exact frame solve open
- Ethernet installed cable: routed keep-out required
- airflow continuity: architecture pass, CFD open
- radar RF clearance: architecture pass, EM open

No current dimensional evidence forces product depth above 40 mm.

## 14. G1 exact-import placeholders
Create named linked solids:
- REF_EX25FHE2_4_STEP
- REF_AG53024_STEP
- REF_TE_2_1734264_1_STEP
- REF_WE_7490220121_STEP
- REF_GCT_USB4085_STEP

Until imported:
- keep exact-solid visibility OFF;
- keep verified/derived envelope visibility ON;
- mark G1_EXACT=false.

Never use a legacy component solid as an unlabeled substitute.

## 15. Assembly bounding boxes
Master bounding-box table:

| Object | X mm | Y mm | Z mm |
|---|---:|---:|---:|
| Product | 0..320 | 0..400 | 0..40 |
| DML | 10..310 | 10..390 | ~2..8 |
| MAIN-P | 105..220 | 112..157 | 18..19.6 PCB |
| MAIN-C | 85..235 | 315..370 | 17..18.6 PCB |
| VOICE | 119..201 | 20..102 | 12..13.6 PCB |
| RADAR | 249..287 | 184..216 | 11..12.6 PCB |
| ENV | 252..294 | 35..59 | 12..13.6 PCB |
| Service recess | 100..220 | 20..48 | 22..40 |
| Left cleat seed | 30..75 | 350..382 | rear region |
| Right cleat seed | 245..290 | 350..382 | rear region |

## 16. Automated model assertions
C111 all G1 objects have explicit XYZ placement.
C112 all temporary bodies carry VERIFIED or DERIVED class.
C113 Ag53024 conservative body remains inside Z limit.
C114 RJ45 exact body can replace envelope without changing mating datum.
C115 USB4085 exact body can replace envelope without changing service datum.
C116 exact exciter solid can replace coarse box without changing center datum.
C117 PCB carrier generation references PCB datums, not supplier-solid faces.
C118 connection recess does not imply remote Ethernet MDI.
C119 all cable routes are represented as swept volumes before G2.
C120 G1 dimensional model reports product depth <=40 mm.

## 17. Release state
G0 skeleton: **READY**
G1 dimensional packaging: **DEFINED / FIRST-ORDER PASS**
G1 exact manufacturer-solid import: **OPEN**
G2 structural frame CAD: **READY TO START FROM G1 DIMENSIONAL MODEL**
G3 shell CAD: **WAIT FOR G2 FRAME AND SERVICE GEOMETRY**
G4 analysis: **CONTRACTS READY / SOLVER GEOMETRY PENDING**
G5 manufacturing: **NOT RELEASED**

Status: **320X400X40_G1_DIMENSIONAL_PACKAGING_DEFINED / C01_TO_C120 / NO_CURRENT_DEPTH_VIOLATION / G1_EXACT_OPEN**.
