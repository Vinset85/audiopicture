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
