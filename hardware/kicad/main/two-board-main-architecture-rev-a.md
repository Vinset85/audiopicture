# AudioPicture V2.2 Rev.A — split MAIN architecture

Status: **MAIN_P_MAIN_C_FUNCTIONAL_SPLIT_BASELINE_DEFINED / EXACT_RECTANGLE_PACKING_AND_INTERCONNECT_OPEN**

## 1. Reason for split
The production successor EX25FHE2-4 is materially deeper than the legacy exciter. Candidate-B therefore creates four full-depth electronics exclusion columns.

A single long MAIN PCB would require an unnecessarily irregular outline. The baseline is changed to two rectangular or near-rectangular MAIN boards.

## 2. MAIN-C — control / connectivity
MAIN-C owns the complete Ethernet signal chain and system controller.

Functions:
- ESP32-S3-WROOM-1-N16R8;
- W5500;
- 25 MHz W5500 crystal;
- Ethernet magnetics;
- RJ45 interface;
- USB-C service/recovery;
- VOICE FPC;
- RADAR FPC;
- ENV FPC;
- status/service interfaces;
- low-power digital support.

Design rule:
**RJ45 -> magnetics -> W5500 -> ESP32 remain on one PCB.**

Do not route Ethernet MDI pairs or W5500 SPI across the MAIN-C / MAIN-P cable.

ESP32 antenna keep-out remains a hard mechanical/RF constraint and must face an RF-clean unfilled-polymer region.

## 3. MAIN-P — power / audio
MAIN-P owns high-current conversion and Class-D audio.

Functions:
- external 24 V input and protection;
- source ORing/priority;
- isolated 24 V PoE input received from MAIN-C;
- INA228 and shunt;
- 5 V TPSM63603;
- 3.3 V TPS62823 as required by final rail ownership;
- TAS5825M;
- four XAL7050-103MEC output inductors;
- final LC capacitors;
- Panasonic EEU-FR1V471B PVDD bulk;
- speaker/exciter harness outputs;
- amplifier fault/power-control conditioning.

Keep BTL switching loops entirely on MAIN-P.

## 4. Ag53024 ownership — FROZEN ON MAIN-C
The production baseline places **Ag53024 on MAIN-C**, together with the complete PoE front end.

Silvertel documents VIN+ and VIN- as the direct PoE inputs after the input bridge rectifiers, while +VDC/-VDC are the isolated regulated outputs. The Ag53024 provides 24 V output, 24 W continuous / 30 W peak, with 1500 Vdc input-to-output isolation.

Therefore MAIN-C owns:
- RJ45;
- Ethernet magnetics;
- PoE bridge rectifiers/protection/filtering;
- Ag53024;
- W5500 and Ethernet logic.

MAIN-P receives the **isolated 24 V PoE output** only.

This avoids carrying the pre-isolation PoE power domain across the MAIN-C / MAIN-P harness and keeps the isolation boundary physically contained on MAIN-C.

Status: **AG53024_OWNERSHIP_FROZEN_MAIN_C**.

## 5. Inter-board link
The MAIN-C <-> MAIN-P interconnect may carry:
- system power rails;
- ground;
- I2S BCLK/LRCLK/TX/RX;
- I2C SDA/SCL if needed;
- AMP_PDN;
- AMP_FAULT;
- power-good/status;
- source-mode/status;
- optional UART/debug.

Avoid:
- Ethernet MDI;
- W5500 SPI;
- Class-D BTL outputs;
- switching-node copper;
- sensitive analog measurement Kelvin nodes.

Provide multiple ground contacts interleaved with clocks/data where practical.

## 6. Clock ownership
ESP32 on MAIN-C remains I2S clock master.

The inter-board I2S path must be treated as a controlled digital interface:
- source damping remains available;
- ground references adjacent;
- short harness;
- no routing parallel to Class-D output harness;
- SI verification before release.

## 7. Rail ownership
Preferred baseline:
- MAIN-P generates 5 V and the high-current system rails;
- MAIN-C receives regulated power from MAIN-P;
- local point-of-load filtering/regulation may remain on MAIN-C where it improves noise isolation.

Final 3.3 V ownership is not frozen until current budget and cable-drop/noise analysis are complete.

## 8. Fault behavior
MAIN-P must default safe if MAIN-C is absent, booting, reset or cable-disconnected:
- amplifier disabled by hardware default;
- source selection deterministic;
- no uncontrolled Class-D output;
- power-good/status observable after MAIN-C boots.

## 9. Mechanical objective
Both boards should be simple rectangles where possible.

Prefer two easy-to-manufacture rectangles over one notched board.

Initial rectangle packing shall target the horizontal/diagonal free bands between Candidate-B successor-exciter exclusion columns. Exact dimensions are not frozen in this document.

## 10. Serviceability
MAIN-C should be closer to the external service/communications bay because it owns RJ45 and USB-C.

MAIN-P should be closer to the exciter harness fan-out and should minimize speaker-output harness length.

The two boards must be independently removable without detaching the DML panel.

## 11. Thermal separation
The split is also thermal:
- MAIN-P is the primary heat-producing PCB;
- MAIN-C contains temperature-sensitive digital/RF interfaces.

Keep the ENV chamber thermally isolated from MAIN-P and its exhaust/conduction path.

## 12. Release gates
Before this architecture is frozen:
2. define inter-board connector and pinout;
3. calculate rail currents and connector contact requirements;
4. run I2S SI/harness-length check;
5. solve two rectangle envelopes in shared CAD;
6. import exact RJ45, Ag53024 and successor-exciter models;
7. run thermal coupling analysis;
8. update native KiCad hierarchy to two-board topology.

Status: **MAIN_P_MAIN_C_FUNCTIONAL_SPLIT_BASELINE_DEFINED / AG53024_ON_MAIN_C_FROZEN / RECTANGLE_PACKING_AND_INTERCONNECT_OPEN**.


## 13. First physical rectangle packing

The first packaging pass uses the verified successor-exciter dimensions and the Ag53024 envelope.

### MAIN-C seed
Initial board envelope:
- **150 x 55 mm**
- long axis horizontal
- intended functions: RJ45/magnetics, PoE bridges, Ag53024, W5500, ESP32-S3, USB-C and daughterboard interfaces.

The 55 mm depth is a starting target, not a release dimension. Ag53024 occupies approximately 57.3 x 17.4/18 x 14 mm by itself, so it shall run along the long board axis.

Preferred product placement seed:
- **X = 85..235 mm**
- **Y = 315..370 mm**

This upper horizontal band is clear of the coarse Candidate-B successor-exciter exclusion boxes. Exact perimeter-frame, DML-mount and wall-mount clearance remains to be checked.

MAIN-C shall place the ESP32 antenna toward an outer RF-clean end of the board, not behind Ag53024, magnetics, carbon-filled frame or metal wall hardware.

### MAIN-P seed
Initial board envelope:
- **145 x 55 mm**
- long axis horizontal
- intended functions: external 24 V protection/source priority, INA228, 5 V/3.3 V power conversion as assigned, TAS5825M, output LC, 470 uF bulk and speaker harness egress.

Preferred product placement seed:
- **X = 88..233 mm**
- **Y = 5..60 mm**

This lower band is geometrically attractive but partially competes with the DML/perimeter structural land. Therefore Y=5..60 is only a mathematical free-space seed. Mechanical CAD must move it inward or locally reshape the rear frame without loading the compliant DML perimeter.

### Alternative MAIN-P band
If the lower perimeter cannot provide enough structural/service clearance, evaluate a central horizontal board in the free band between lower and upper exciter pairs, with exact notches only if required.

### Packaging implication
Two approximately 150 x 55 mm horizontal boards use the staggered Candidate-B layout much more efficiently than the former 70 x 220 mm vertical board.

The split also creates physical thermal separation:
- upper MAIN-C: PoE/network/control;
- lower MAIN-P: high-current audio/power.

### Board area sanity check
- MAIN-C seed area: 8250 mm2
- MAIN-P seed area: 7975 mm2
- combined: 16225 mm2

This is larger than the old 220 x 70 board area (15400 mm2) by about 5.4%, which is acceptable at this stage because the split adds connector/keep-out overhead but substantially improves usable placement geometry.

### Not frozen
Do not release either rectangle to PCB layout yet. Required before freeze:
1. rear structural-frame perimeter clearance;
2. exact RJ45 and connection-bay service volume;
3. exact Ag53024 STEP/drawing import;
4. ESP32 antenna RF volume;
5. exact 24 V connector service volume;
6. MAIN-C/MAIN-P inter-board connector selection;
7. thermal zoning;
8. mounting-hole/boss locations.

Status: **MAIN_C_150x55_UPPER_SEED / MAIN_P_145x55_LOWER_SEED / FRAME_AND_CONNECTOR_COLLISION_GATE_OPEN**.


## 14. Rear-frame and DML-perimeter clearance pass

The nominal DML is 300 x 380 mm centered in the 320 x 400 mm product, leaving only 10 mm nominal border per side in front-view projection.

The DML perimeter mount baseline consumes approximately:
- 5..6 mm DML edge land;
- 6 mm foam strip width;
- adjacent hard-stop/support structure;
- rear structural perimeter beam nominally 8..12 mm projected width.

These functions overlap in Z but cannot be treated as free PCB area in XY.

### Protected perimeter zone
For electronics packaging, define a conservative **20 mm protected perimeter band** from the external product edge on all four sides until detailed shared CAD resolves the frame sections.

No MAIN PCB body, tall component, connector mating volume or mounting boss may enter this band in the baseline solve.

This is a packaging rule, not a claim that the final frame is physically 20 mm wide everywhere.

### MAIN-C upper seed correction
Previous MAIN-C seed Y=315..370 mm ends 30 mm from the product top edge and therefore survives the 20 mm protected perimeter rule.

Retain:
- MAIN-C = 150 x 55 mm
- X = 85..235 mm
- Y = 315..370 mm

subject to exact upper-frame/wall-mount and connector service checks.

### MAIN-P lower seed correction
Previous MAIN-P seed Y=5..60 mm violates the protected perimeter band and is withdrawn.

A 55 mm-deep rectangular MAIN-P cannot simply be translated upward while remaining clear of L1's coarse exclusion box at X=37..99, Y=50..110 and R2 at X=223..285, Y=88..148 if centered across the product.

Therefore the lower-band rectangle requires either:
- reduced board depth;
- lateral shift;
- or use of the central free band.

### Preferred MAIN-P revision
Use a first revised target:
- **MAIN-P = 145 x 45 mm**
- horizontal;
- seek placement in a central/lower inter-exciter band rather than the external perimeter.

The 45 mm depth is now the packaging target to be validated against actual component placement. It is not yet a released PCB dimension.

### PORON note
Rogers publishes PORON 4701-30 Very Soft in thicknesses that include the approximately 1.6..3.2 mm range for the 320 kg/m3 family and characterizes it specifically for gasketing, gap filling and vibration isolation. The existing nominal 2.0 mm / ~20% compression DML mount remains a valid engineering baseline, but exact grade/thickness must be selected from an available production thickness and characterized in FEA.

### Mechanical conclusion
- MAIN-C 150 x 55 upper band remains plausible.
- MAIN-P 145 x 55 lower-edge seed is rejected.
- MAIN-P is reduced to a 145 x 45 target and must be repacked into an inter-exciter band.
- the 40 mm product depth remains viable at architecture level; the current blocker is planar packing, not global depth.

Status: **MAIN_C_UPPER_SEED_RETAINED / MAIN_P_LOWER_EDGE_SEED_WITHDRAWN / MAIN_P_145x45_REPACK_REQUIRED**.


## 15. MAIN-P 145 x 45 mm inter-exciter packing solve

### Electrical area sanity
The target is plausible but dense.

The TAS5825M itself is only 5 x 5 mm (RHB VQFN-32). The dominant audio placement objects are instead:
- 4 x XAL7050 inductors, each approximately 8.0 x 7.7 x 5.0 mm;
- local PVDD ceramics placed immediately at the TAS5825M PVDD pins;
- the 470 uF radial bulk pocket;
- output LC capacitors;
- high-current copper and speaker connector/harness egress.

TI explicitly requires PVDD bypass/decoupling capacitors to be placed very close to the TAS5825M PVDD pins. Therefore the audio block shall be treated as a compact placement island and not spread across the board merely to fill free area.

### Geometric result
A useful lower-central band exists between the L1 and R2 successor-exciter columns, but the full 145 x 45 rectangle must avoid both their expanded exclusion boxes and the 20 mm protected product perimeter.

First placement seed:

- **MAIN-P = 145 x 45 mm**
- **BOARD_P_X = 105 mm**
- **BOARD_P_Y = 112 mm**
- occupied rectangle: X=105..250 mm, Y=112..157 mm.

This seed is above L1's coarse box (Y<=110 mm), below L2's box (Y>=166 mm), and below/partly laterally adjacent to R2. Because R2's coarse box is X=223..285, Y=88..148, the raw rectangle overlaps R2 in X=223..250, Y=112..148.

Therefore the seed is **not collision-free** and is rejected as a simple rectangle.

### Collision-free rectangular conclusion
With the current conservative 62 x 60 mm successor-exciter boxes, a 145 x 45 mm board cannot occupy the obvious L1/L2 horizontal gap while also spanning centrally toward the right without intersecting R2.

The preferred response is **not** to notch MAIN-P immediately.

Reduce the first rectangle target to:
- **MAIN-P = 115 x 45 mm**

Candidate seed:
- **X=105..220 mm**
- **Y=112..157 mm**

This clears:
- L1 by Y;
- L2 by Y;
- R2 by X;
- R1 by Y;
while remaining outside the 20 mm protected perimeter.

### Area consequence
MAIN-P area becomes 5175 mm2.

This is aggressive but potentially feasible because:
- Ag53024, RJ45, W5500, ESP32, USB and daughterboard connectors have moved to MAIN-C;
- TAS5825M is a 5 x 5 mm device;
- XAL7050 inductors total only about 246 mm2 of body footprint before spacing.

However, feasibility is not released until source-selection/protection, converters, bulk, connectors and copper/thermal areas are floorplanned.

### Functional floorplan target
Within 115 x 45 mm:
- one end: external 24 V input/protection/source priority;
- center: DC/DC + INA228;
- opposite end: compact TAS5825M + LC island;
- 470 uF bulk adjacent to the PVDD/audio island but outside its hottest copper;
- speaker harness exits directly toward the DML wiring routes.

### Decision
The 145 x 45 MAIN-P target is demoted.
The new preferred rectangle is **115 x 45 mm at X=105, Y=112** for detailed floorplanning.

Status: **MAIN_P_115x45_X105_Y112_PLACEMENT_SEED / DETAILED_POWER_AUDIO_FLOORPLAN_REQUIRED**.


## 16. MAIN-P detailed power/audio floorplan — first pass

The 115 x 45 mm seed is retained for a detailed functional floorplan.

### Placement coordinates
Use local MAIN-P coordinates:
- PX = 0..115 mm along the long axis;
- PY = 0..45 mm along the short axis.

Product placement remains:
- product X = 105 + PX;
- product Y = 112 + PY.

### Zone P1 — 24 V ingress / protection
Reserve approximately:
- PX = 0..30 mm
- PY = 0..45 mm

Contains:
- external 24 V connector interface/harness landing;
- fuse/TVS;
- TPS48100-Q1;
- back-to-back MOSFETs;
- source-priority switching interface;
- high-current copper entry.

The TPS48100 package is not area-dominant; the MOSFETs, protection spacing, connector/service volume and copper width dominate this zone.

### Zone P2 — measurement / conversion
Reserve approximately:
- PX = 30..65 mm
- PY = 0..45 mm

Contains:
- INA228 + Kelvin shunt;
- TPSM63603 24 V -> 5 V;
- TPS62823 5 V -> 3.3 V if final rail ownership remains on MAIN-P;
- input/output capacitor banks.

Verified package anchors:
- TPSM63603: 4 x 6 x 1.8 mm;
- TPS62823: 2 x 1.5 mm;
- INA228: small 10-pin VSSOP.

Copper, thermal vias and capacitor derating space dominate over IC package area.

### Zone P3 — Class-D audio island
Reserve approximately:
- PX = 65..115 mm
- PY = 0..45 mm

Contains:
- TAS5825M;
- local PVDD ceramic decoupling;
- four bootstrap capacitors;
- four XAL7050-103MEC inductors;
- final LC capacitors;
- speaker harness egress;
- AMP_FAULT / AMP_PDN local conditioning.

Keep each BTL half-bridge path compact and symmetric. Do not route switching nodes through P1/P2.

### PVDD bulk placement
The EEU-FR1V471B 470 uF capacitor is assigned near the P2/P3 boundary rather than directly beside the hottest output inductors.

Reserve its 12 x 12 x 19 mm mechanical pocket approximately around:
- PX = 58..70 mm
- PY = 28..40 mm

Exact position remains movable to preserve PVDD current path, thermal separation and frame clearance.

Local ceramic PVDD decoupling remains immediately at TAS5825M. The radial bulk is not a substitute for those ceramics.

### Thermal copper policy
MAIN-P cannot be validated from component-body area alone.

Reserve substantial continuous copper for:
- 24 V high-current path;
- MOSFET heat spreading;
- TPSM63603 thermal pads;
- TAS5825M exposed pad;
- ground return;
- output filter current paths.

Do not fill the nominally unused board area with unrelated signals until thermal/current polygons are solved.

### Inter-board connector edge
Reserve a connector strip along the upper long edge of P1/P2, away from the Class-D output switching region.

The link should carry isolated PoE 24 V / system power as finally defined plus digital control/audio signals with multiple ground contacts.

### Speaker harness edge
Prefer speaker/exciter harness exits from the P3 short/right edge so BTL currents leave the board without crossing the control/power-conversion zones.

### Preliminary fit result
The 115 x 45 mm board is **electrically plausible** for the assigned functions because the selected converters and controller packages are compact, but it is not yet released.

The remaining area risks are:
1. exact external-24-V connector and mating/service envelope;
2. back-to-back MOSFET copper/thermal requirement;
3. final LC capacitor footprints;
4. inter-board connector;
5. mounting holes/boss keep-outs;
6. thermal-via fields;
7. creepage/clearance around protection nodes.

Do not reduce below 115 x 45 mm at this stage.

Status: **MAIN_P_115x45_FLOORPLAN_P1_P2_P3_DEFINED / CONNECTOR_THERMAL_COPPER_RELEASE_GATES_OPEN**.


## 17. MAIN-C <-> MAIN-P interconnect architecture

Use **two physically separate interconnects** rather than one mixed power/signal connector.

### JCP — power interconnect
Function:
- isolated PoE 24 V from MAIN-C to MAIN-P;
- shared power return;
- optional low-current power-status/sense only if connector family/pin allocation supports it cleanly.

Baseline electrical allocation:
- 2 contacts: +24V_POE_ISO
- 2 contacts: GND/24V return

Parallel contacts reduce contact resistance and provide margin.

Target connector requirements:
- >=3 A system-level continuous capability with derating;
- positive latch;
- polarized;
- compact wire-to-board family;
- 30 VDC or higher;
- production crimp tooling and readily available terminals;
- low-profile right-angle PCB header preferred where enclosure service allows.

Do not use a fine-pitch FPC for this power path.

### JCS — signal interconnect
Function:
- I2S;
- I2C;
- control/status;
- ground references.

Baseline 16-contact allocation:

1 GND
2 I2S_BCLK
3 GND
4 I2S_LRCLK
5 GND
6 I2S_TX
7 GND
8 I2S_RX
9 GND
10 I2C_SDA
11 I2C_SCL
12 AMP_PDN
13 AMP_FAULT
14 5V_PG
15 3V3_PG
16 GND

This intentionally spends many contacts on ground to improve return paths for the I2S harness.

### Signal connector family
A 0.5 mm-pitch FPC/FFC connector is acceptable for JCS because no high-current system power is assigned to it.

The existing Hirose FH12 family used elsewhere in AudioPicture is a strong baseline candidate for consistency, but exact orientation and cable bend/service volume must be validated.

### Power connector candidate
A 4-circuit Molex Micro-Fit 3.0-class connection is the preferred first candidate for JCP, subject to exact right-angle header, mating housing, terminal/wire gauge and service-volume verification.

The design shall not assume the nominal family current rating is available in the sealed enclosure; apply temperature, contact-count, wire-gauge and PCB-copper derating.

### I2S signal-integrity rules
- keep JCS cable short;
- ground contacts interleave BCLK/LRCLK/data;
- retain source-series damping footprints on MAIN-C;
- no long parallel run beside speaker/BTL harness;
- no routing over MAIN-P switching-node area;
- validate edge rate and ringing on final harness geometry.

### Fault behavior
JCP present / JCS absent:
- MAIN-P receives power but amplifier remains hardware-disabled.

JCS present / JCP absent:
- no back-powering from signal pins into MAIN-P power domains.

Both absent:
- safe/off.

Add connector-detect only if it provides a real diagnostic benefit without creating a new unsafe back-power path.

### Mechanical placement
On MAIN-P:
- JCP at P1/P2 side, close to source-priority/power entry;
- JCS along P1/P2 upper edge;
- both kept away from P3 Class-D switching/output edge.

On MAIN-C:
- JCP near Ag53024 isolated-output side;
- JCS near ESP32 digital/audio interface region.

### Next release gates
1. choose exact 4-circuit JCP MPN/header/housing/terminal;
2. choose exact 16-contact JCS FPC MPN and orientation;
3. define cable length;
4. calculate JCP contact/wire temperature rise at PoE and external-power operating cases;
5. verify I2S SI;
6. verify connector mating/removal path in shared CAD.

Status: **DUAL_INTERCONNECT_JCP_POWER_JCS_SIGNAL_ARCHITECTURE_FROZEN / EXACT_MPN_AND_HARNESS_RELEASE_GATES_OPEN**.


## 18. Exact MAIN-C <-> MAIN-P connector selections

### JCP — power connector frozen candidate
PCB header:
**Molex 43650-0411**
- Micro-Fit 3.0;
- right-angle;
- single row;
- 4 circuits;
- metal PCB retention clip;
- gold mating finish;
- manufacturer status Active at selection;
- 8.5 A maximum per contact published for the part;
- 600 V maximum published for the part;
- mated height 6.98 mm.

Mating receptacle family:
**Molex 43645, 4-circuit variant**, exact housing suffix and 43030 terminal suffix to be frozen with wire gauge and harness process.

Electrical assignment remains:
1 +24V_POE_ISO
2 +24V_POE_ISO
3 GND
4 GND

The published current rating is not used as the design current without derating. Two contacts per pole are retained for lower resistance, thermal margin and contact redundancy.

Mechanical release still requires the exact mating housing, crimp terminal, wire gauge, bend radius and unplug service volume.

Status: **JCP_HEADER_43650_0411_SELECTED / MATING_HOUSING_TERMINAL_WIRE_RELEASE_OPEN**.

### JCS — signal connector frozen
**Hirose FH12-16S-0.5SH(55)**
- 16 positions;
- 0.5 mm pitch;
- horizontal FPC/FFC insertion;
- ZIF;
- bottom contact;
- body approximately 12.1 x 6.4 x 2.0 mm;
- manufacturer STEP available.

Use the same exact connector on MAIN-C and MAIN-P unless cable contact orientation proves that an alternate top-contact variant is required.

Pin allocation remains:
1 GND
2 I2S_BCLK
3 GND
4 I2S_LRCLK
5 GND
6 I2S_TX
7 GND
8 I2S_RX
9 GND
10 I2C_SDA
11 I2C_SCL
12 AMP_PDN
13 AMP_FAULT
14 5V_PG
15 3V3_PG
16 GND

Status: **JCS_FH12_16S_0_5SH_55_SELECTED / FPC_ORIENTATION_AND_LENGTH_RELEASE_OPEN**.

### Harness-length seed from current board placement
Current product-space seeds:
- MAIN-C: X=85..235, Y=315..370 mm;
- MAIN-P: X=105..220, Y=112..157 mm.

The minimum board-edge separation is therefore approximately 158 mm between MAIN-P top edge Y=157 and MAIN-C bottom edge Y=315.

Do not use a 158 mm cable. The harness must include connector setback, routing around exciter/frame volumes, bend radius and assembly/service slack.

Initial CAD harness targets:
- JCS FPC developed length: **220 mm**
- JCP wire harness developed length: **230 mm**

These are routing seeds, not production cut lengths.

### First power-drop bound
Ag53024 continuous output power is 24 W at 24 V, corresponding to approximately 1 A nominal continuous output current before conversion losses/load dynamics.

With two JCP contacts in parallel per pole, connector contact current is approximately 0.5 A/contact at the nominal 24 W PoE operating point. This is far below the published 8.5 A maximum/contact rating of the selected header; wire/contact temperature-rise verification remains mandatory.

For the JCP harness, start with **AWG22 copper** as the baseline candidate. Final gauge depends on actual routing, temperature rise, crimp terminal qualification and mechanical flexibility.

### I2S SI seed
At approximately 220 mm FPC length, treat I2S as a transmission-line-sensitive digital link even at 48 kHz audio rate because edge rate, not sample rate, controls ringing.

Retain source damping footprints on MAIN-C:
- BCLK: 22 ohm default, options 0/22/33;
- LRCLK: 22 ohm default, options 0/22/33;
- TX/RX: 22 ohm default where direction/source permits.

Final values require bench/SI validation or field-solver/IBIS-quality simulation with the chosen FPC geometry.

Status: **JCP_JCS_EXACT_HEADERS_SELECTED / HARNESS_220_230MM_SEEDS_DEFINED / FINAL_CABLE_AND_TERMINAL_RELEASE_OPEN**.


## 19. MAIN-C 150 x 55 mm detailed floorplan — first pass

Use local MAIN-C coordinates:
- CX = 0..150 mm along the horizontal long axis;
- CY = 0..55 mm vertically.

Product seed remains:
- product X = 85 + CX;
- product Y = 315 + CY.

### C1 — external Ethernet / PoE front end
Reserve approximately:
- CX = 0..55 mm
- CY = 0..55 mm

Contains:
- RJ45 connection-bay interface;
- TE 2-1734264-1 / final jack;
- Würth 7490220121 magnetics;
- PoE bridge rectifiers and input protection/filtering;
- Ag53024 input side.

Rules:
- keep Ethernet MDI differential pairs short and direct;
- keep PoE input bridge loops compact;
- preserve Ag53024 isolation barrier and manufacturer keep-outs;
- do not route SELV logic copper through the primary/non-isolated PoE domain.

### C2 — isolated PoE output / Ethernet controller / service
Reserve approximately:
- CX = 55..105 mm
- CY = 0..55 mm

Contains:
- Ag53024 body/output side as its final orientation requires;
- W5500;
- 25 MHz crystal;
- JCP 24 V isolated output connector;
- USB-C service connector where connection-bay geometry permits;
- local filtering and protection.

The Ag53024 body is long enough that it may span C1/C2. Its isolation boundary, not the arbitrary zone boundary, controls placement.

W5500 shall remain on the same PCB as magnetics/RJ45; route MDI pairs without crossing the PoE isolation boundary unnecessarily.

### C3 — MCU / RF / daughterboards
Reserve approximately:
- CX = 105..150 mm
- CY = 0..55 mm

Contains:
- ESP32-S3-WROOM-1-N16R8;
- JCS signal FPC to MAIN-P;
- VOICE FPC;
- RADAR FPC;
- ENV FPC;
- service/status low-power circuitry.

### ESP32 antenna placement
Place the ESP32-S3 module at the far right end of MAIN-C with the PCB antenna facing the board/product edge.

Create an RF-clean region beyond and around the antenna:
- no copper beneath/forward of antenna according to Espressif module guidance;
- no Ag53024, magnetics, RJ45 shield, carbon-filled frame, wiring bundle or wall-mount metal in the forward antenna volume;
- prefer unfilled ASA/non-conductive local shell.

The exact module position and enclosure cut-free RF window are release-critical.

### Connector-edge strategy
Do not put every external/service connector on the same 150 mm board edge.

Preferred:
- RJ45 near C1 connection-bay end;
- USB-C near C2 connection-bay access;
- JCP/JCS on internal/lower edge toward MAIN-P;
- VOICE/RADAR/ENV FPCs on internal edge with routing directions matched to daughterboard positions.

### Isolation zoning
MAIN-C has three electrical domains:
1. Ethernet/PoE input and pre-isolation power;
2. isolated 24 V output;
3. SELV digital/control.

The Ag53024 isolation boundary must be explicit in schematic, PCB copper, silkscreen/assembly documentation and mechanical keep-out.

Do not allow mounting hardware or conductive PC-CF inserts to bridge the intended isolation clearance region.

### Area assessment
150 x 55 mm is **plausible but significantly more constrained than MAIN-P** because:
- Ag53024 is approximately 57 mm long and ~14 mm high;
- RJ45/magnetics require connector/service volume;
- ESP32 needs empty RF volume rather than merely package area;
- five internal/external connector systems compete for board edges.

Therefore 150 x 55 mm remains the minimum preferred seed, not a target to reduce.

If exact CAD shows conflict, first increase MAIN-C width within the upper free band before introducing notches or moving the ESP32 antenna inward.

### Thermal note
Ag53024 and W5500 heat must not bias the ENV daughterboard. Keep ENV physically separated and avoid routing its passive-air chamber through MAIN-C thermal plume/conduction paths.

### Release gates
1. import exact Ag53024 STEP;
2. import exact RJ45/magnetics geometry;
3. define Ag53024 isolation keep-out from manufacturer data;
4. place ESP32 antenna against real rear-shell/frame geometry;
5. validate all connector mating/service volumes;
6. run Ethernet SI/EMI placement review;
7. run PoE creepage/clearance review;
8. run upper-board thermal model.

Status: **MAIN_C_150x55_C1_C2_C3_FLOORPLAN_DEFINED / POE_ISOLATION_RF_AND_CONNECTOR_CAD_GATES_OPEN**.
