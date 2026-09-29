# MAIN Rev.A — Symbol / Footprint Audit

Status: IN PROGRESS. Only manufacturer-verified package identities are marked VERIFIED. A package identity is not by itself approval of a KiCad library footprint: pad geometry and exposed-pad treatment must still be compared to the manufacturer land pattern.

| Ref/function | Production MPN | Manufacturer package | Pins | Audit |
|---|---|---:|---:|---|
| U1 MCU | ESP32-S3-WROOM-1-N16R8 | Espressif WROOM-1 module | 41 module pads | VERIFIED_PACKAGE; USE_ESPRESSIF_LAND_PATTERN |
| U2 Ethernet | W5500 | LQFP 7x7 mm, 0.50 mm pitch | 48 | VERIFIED_PACKAGE |
| U4/U5 ideal diode | LM74700QDBVRQ1 | TI DBV SOT-23 | 6 | VERIFIED_PACKAGE |
| U7 power monitor | INA228AIDGSR | TI DGS VSSOP | 10 | VERIFIED_PACKAGE |
| 24->5 V module | TPSM63603V5RDHR | TI RDH B0QFN | 30 | VERIFIED_PACKAGE |
| 5->3.3 V buck | TPS62823DLCR | TI DLC VSON-HR 2.0x1.5 mm | 8 | VERIFIED_PACKAGE |
| Audio amp | TAS5825MRHBR | TI RHB VQFN 5x5 mm + exposed thermal pad | 32 + EP | VERIFIED_PACKAGE |

## Mandatory native-capture rule
Do not commit a hand-written or syntactically guessed .kicad_sch/.kicad_pcb file.

Native KiCad files are committed only after they have been created/saved by KiCad 9.x (or a validated KiCad automation that opens/saves successfully in KiCad), pass parser/open test, and preserve manufacturer pin numbering.

## Footprint acceptance checklist
For every critical IC:
1. package code matches orderable MPN;
2. pin count and pin-1 orientation match datasheet;
3. pad pitch/size checked against manufacturer recommended land pattern;
4. exposed pad dimensions/paste segmentation checked where applicable;
5. courtyard/body height checked for 40 mm product envelope;
6. 3D model is optional and never used as electrical authority;
7. assembly-house minimum geometry checked;
8. thermal-via strategy separately reviewed for power packages.

## Current verified notes
### ESP32-S3-WROOM-1-N16R8
Use Espressif WROOM-1 recommended PCB land pattern and antenna-area keep-out. The module footprint must reproduce the manufacturer dimensions, not a visually similar generic ESP32 footprint.

### W5500
LQFP48, 7 x 7 mm body, 0.50 mm pitch (9 x 9 mm overall lead span class).

### TAS5825MRHBR
TI RHB, 32-pin VQFN, 5 x 5 mm, 0.50 mm pitch, exposed thermal pad. Thermal pad must be soldered and the via/paste pattern is a thermal/layout design item.

### INA228AIDGSR
TI DGS, 10-pin VSSOP.

### TPSM63603V5RDHR
TI RDH, 30-pin B0QFN power module. Do not substitute a generic QFN footprint.

### TPS62823DLCR
TI DLC, 8-pin VSON-HR, 2.0 x 1.5 mm.

### LM74700QDBVRQ1
TI DBV, 6-pin SOT-23.

## Remaining critical footprint gates
Before full native schematic/PCB freeze, verify:
- Ag5324 mechanical/pin drawing;
- exact PoE MagJack;
- DMT6007LFG final MOSFET or replacement;
- exact 24 V input connector;
- USB-C receptacle;
- USB ESD;
- shunt exact MPN;
- radar board FPC family;
- voice board FPC family;
- ENV board FPC family;
- TAS5825M LC inductors/capacitors;
- radar regulator/translators/clock;
- priority comparator;
- rail supervisor if needed.

## Capture sequence
1. create KiCad 9 project/root sheet;
2. capture Sheet 02 and Sheet 03 power first;
3. run ERC and fix pin-power semantics;
4. capture U1 minimum system;
5. capture W5500/PoE;
6. capture TAS5825M;
7. capture USB;
8. daughterboard connectors;
9. factory test points;
10. annotate;
11. assign only audited footprints;
12. ERC;
13. schematic PDF review;
14. PCB floorplan.

## Release policy
A schematic can be electrically complete while some footprints remain VALIDATE. Gerbers are forbidden until all production footprints are VERIFIED.
