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


## Audit pass 2 — power / service mechanical blockers

### PoE module
**Preferred new-production qualification: Silvertel Ag53024.**

Manufacturer status:
- 24 V output;
- 24 W continuous, 30 W peak;
- >90% efficiency family claim;
- pin-for-pin compatible with Ag5300/Ag5400 family.

Legacy baseline Ag5324 remains an allowed qualification fallback. Its documented SIL envelope is approximately 57 x 18 x 14 mm.

Decision:
- PCB footprint shall be built around the manufacturer pin-compatible SIL family drawing only after exact pin coordinates are transcribed from the current Ag53000 datasheet/STEP.
- BOM architecture remains 24 V PoE Class-4; firmware limiter assumptions remain based on 24 W continuous, not 30 W continuous.

### ORing MOSFET
DMT6007LFG remains preferred candidate:
- 60 V N-MOSFET;
- PowerDI3333-8;
- approximately 3.3 x 3.3 mm body;
- 0.65 mm terminal pitch class;
- RDS(on) max 6 mOhm at VGS=10 V.

Status: VERIFIED_PACKAGE / VALIDATE_LM74700_GATE_DRIVE_THERMAL_SOA.

### Current shunt
Vishay WSK2512 family is mechanically suitable:
- 2512-class, approx. 6.35 x 3.18 x 0.64 mm;
- 1 W family rating;
- 3 mOhm to 10 mOhm family range includes required 10 mOhm.

Preferred target: 10 mOhm, <=1%, low TCR, Kelvin routing.
Status: VERIFIED_FAMILY / EXACT_ORDER_CODE_VALIDATE.

### USB-C service connector
GCT USB4085 is a strong mechanical candidate:
- USB 2.0 Type-C receptacle;
- 16 contacts;
- horizontal/top-mount;
- through-hole shell/mechanical retention;
- approx. 3.46 mm profile;
- 20,000 mating-cycle manufacturer rating.

Because AudioPicture uses USB only for service/recovery, the mechanically robust USB2-only connector is preferred over a denser USB3 connector.

Status: CANDIDATE_MPN / VERIFY_DRAWING_WITH_ENCLOSURE.

## Still blocking PCB outline/floorplan
1. exact PoE MagJack with compatible center-tap/PoE extraction;
2. exact external 24 V connector;
3. exact FPC connector family and pitch;
4. exact TAS output inductors;
5. exact USB ESD protector;
6. exact Ag53024/Ag5324 SIL land pattern coordinates from current manufacturer drawing.


## Audit pass 3 — Ethernet / PoE topology gate

### Rejected MagJack candidate
Pulse J0011D21BNL is REJECTED for the AudioPicture PoE production BOM.
Reason: manufacturer product data classifies it as NON-POE even though it is a valid 10/100 integrated-magnetics RJ45 and appears in WIZnet W5500 recommendations.

Do not confuse W5500 electrical compatibility with PoE power-path compatibility.

### W5500 center-tap rule
WIZnet documents a special case for integrated-transformer RJ45 parts with internally connected center taps:
- RX matching network must be isolated from the 3.3 V center tap with added capacitors;
- omission can impair W5500 operation;
- connected center taps can increase dissipation.

AudioPicture preference is therefore:
1. PoE-rated integrated MagJack whose transformer/center-tap topology is explicitly accessible and compatible with the selected PoE extraction scheme; OR
2. discrete 10/100 Ethernet transformer + shielded RJ45 if this produces a cleaner, auditable PoE power path.

A generic integrated MagJack is not acceptable.

### PoE bridge topology
Silvertel Ag5300 family reference connection confirms two bridge rectifiers on the PoE input for IEEE 802.3at polarity support.

Rev.A keeps:
- bridge path A for data-pair feed;
- bridge path B for spare-pair feed;
- bridge outputs combined only on the PoE module input side as shown by the Silvertel reference architecture;
- isolated secondary remains +24V_POE / GND_SYS.

### Ag53024 output capacitor correction
For 24 V Ag5300-family output, use the current Silvertel reference minimum/output-stability guidance rather than copying the 5/12 V example value.
Exact production capacitance, voltage rating, ESR and temperature grade shall be frozen from the selected Ag53024 datasheet revision.

### MagJack selection gate
Exact MagJack MPN remains VALIDATE_POE_PINOUT.

It may be frozen only when the datasheet proves all of:
- 10/100BASE-T compatibility;
- transformer ratio/termination compatible with W5500;
- IEEE 802.3af/at current path capability for intended pairs;
- center taps / spare pairs exposed in a topology compatible with the two-bridge Silvertel input;
- shield pins available for CHASSIS_ETH;
- <=40 mm product-depth mechanical envelope;
- production availability.

Do not use Pulse J0011D21BNL as the PoE production connector.


## Audit pass 4 — Ethernet physical architecture FROZEN
Decision: use **discrete Ethernet magnetics + shielded 8P8C RJ45** for MAIN Rev.A.

Integrated MagJack candidates are no longer floorplan blockers.

Initial transformer candidate:
- Pulse H1102NL, listed by WIZnet for W5500 external-transformer use.
- Status remains CANDIDATE until PoE+ DC current/insulation capability is verified against the current Pulse datasheet.

RJ45 requirement:
- plain shielded 8P8C;
- no hidden magnetics or bridge rectifiers;
- all 8 cable contacts exposed;
- robust right-angle THT mechanical retention preferred.

This architecture gives explicit access to:
- data-pair cable-side center taps for PoE Alternative A;
- spare pairs for Alternative B;
- W5500 PHY-side transformer terminations;
- CHASSIS_ETH.

PCB floorplanning may now reserve separate footprints/zones for RJ45, transformer and two PoE bridges instead of one MagJack envelope.


## Audit pass 5 — PoE magnetics correction
### H1102NL rejected
Pulse H1102NL is now REJECTED for MAIN Rev.A.
Manufacturer data explicitly marks it NON-POE. Its media-side OCL specification is characterized with only 8 mA DC bias, so it shall not carry the Alternative-A Class-4 PoE feed.

Remove it as the production transformer candidate.

### Replacement transformer requirements
Select a PoE+ rated transformer/magnetics part with:
- 10/100BASE-T electrical compatibility with W5500;
- 1:1 data windings as required by W5500 reference topology;
- cable-side center taps exposed;
- IEEE 802.3at / PoE+ current rating explicitly stated;
- >=1500 V isolation as required by selected safety architecture;
- industrial temperature preferred;
- manufacturer land pattern available.

Wurth 749022011 has been identified as an active PoE+ rated LAN transformer family candidate, but it is a 10/100/1000 four-channel device and therefore oversized for W5500. Do not freeze it solely because it is PoE+ rated; continue search for a 10/100 two-channel PoE+ part or accept the size penalty only after floorplan comparison.

### Bridge rectifiers
Silvertel Ag5300 reference explicitly requires two external bridge rectifiers for input polarity / data-pair vs spare-pair compatibility.

DF01S is documented by Silvertel as a suitable low-cost example for Ag5300-family designs, but AudioPicture shall not freeze DF01S until bridge conduction loss and enclosure thermal rise are calculated at Class-4 worst-case current.

Selection options:
1. conventional silicon bridge — cheapest, highest loss;
2. Schottky bridge/discrete Schottky — lower loss;
3. MOSFET active bridge — lowest loss, higher BOM/complexity.

For the 40 mm fanless enclosure, choose based on measured/calculated thermal budget rather than component count alone.
