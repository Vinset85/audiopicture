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
- PoE DC output input from Ag53024;
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

## 4. Ag53024 ownership
Baseline: **Ag53024 belongs to MAIN-P**, while RJ45/magnetics remain on MAIN-C.

This requires carrying only the PoE isolated/rectified interface appropriate to the finalized PoE architecture between the connector/magnetics side and the module side. Before freezing this split, verify the Ag53024 input architecture and whether separating it from the RJ45/magnetics creates undesirable high-voltage/common-mode routing across the inter-board harness.

If that verification is unfavorable, move Ag53024 to MAIN-C and send only its isolated DC output to MAIN-P.

Therefore Ag53024 ownership is **provisional**, unlike the Ethernet signal-chain ownership.

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
1. verify exact Ag53024 input/output pin architecture and decide final board ownership;
2. define inter-board connector and pinout;
3. calculate rail currents and connector contact requirements;
4. run I2S SI/harness-length check;
5. solve two rectangle envelopes in shared CAD;
6. import exact RJ45, Ag53024 and successor-exciter models;
7. run thermal coupling analysis;
8. update native KiCad hierarchy to two-board topology.

Status: **MAIN_P_MAIN_C_FUNCTIONAL_SPLIT_BASELINE_DEFINED / AG53024_OWNERSHIP_AND_RECTANGLE_PACKING_OPEN**.
