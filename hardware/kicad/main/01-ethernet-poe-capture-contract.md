# Sheet 01 — Ethernet / PoE native capture contract

Status: **READY_FOR_NATIVE_KICAD_CAPTURE**

This file is the reviewed electrical input for `01-ethernet-poe.kicad_sch`.
It is NOT a substitute for a KiCad schematic. The native schematic shall only be committed after opening/saving/validating it in KiCad 9.x.

## Frozen production parts
- J_ETH: TE Connectivity 2-1734264-1, passive shielded 8P8C right-angle THT.
- T_ETH: Wurth Elektronik 7490220121, 350 uH, 600 mA PoE-capable magnetics.
- U_ETH: WIZnet W5500, LQFP-48 7 x 7 mm, 0.5 mm pitch.
- D_POE1..D_POE8: STMicroelectronics STPST3H100AF, 100 V / 3 A SOD128Flat.
- U_POE: Silvertel Ag53024, Ag53000 family, 24 V isolated Type-2/Class-4 PD module.

## Sheet interface
MCU inputs: SPI_SCLK, SPI_MOSI, ETH_CS, ETH_RST.
MCU outputs: SPI_MISO, ETH_INT.
System outputs: +24V_POE, POE_PRESENT, GND.
Chassis: CHASSIS_ETH.
No PoE-primary net is exported to a non-isolated system sheet.

## RJ45 logical mapping
J_ETH retains standard 8P8C numbering.
- contacts 1/2: 100BASE-TX data pair through T_ETH.
- contacts 3/6: 100BASE-TX data pair through T_ETH.
- contacts 4/5: one Alternative-B PoE leg.
- contacts 7/8: other Alternative-B PoE leg.
- shield/mechanical tabs: CHASSIS_ETH only.

## Transformer
Use exactly two channels for 100BASE-TX.
W5500-side/cable-side mapping must be transcribed from the Wurth schematic and checked against W5500 TXP/TXN/RXP/RXN polarity.
Alternative-A PoE is extracted from cable-side center taps of the two used channels to BR201.
Unused channels are intentionally unused per manufacturer guidance; do not repurpose them.

## PoE bridges
BR201 = D_POE1..D_POE4, fed by Alternative-A center taps.
BR202 = D_POE5..D_POE8, fed by Alternative-B pairs 4/5 and 7/8.
Both are full-wave bridges using STPST3H100AF.
Rectified outputs feed only Ag53024 primary input.
PoE-primary negative is NOT GND_SYS.

## Ag53024
Use official Silvertel Ag53000 V1.1 pin numbering and Figure 13 land pattern.
Footprint authority: 10 THT pins, 2.54 mm pitch, 1.12 mm hole basis, manufacturer >8.46 mm copper keep-out.
Primary connects only to rectified PoE primary.
Isolated secondary creates +24V_POE and GND_SYS.
C_POE_OUT is immediately at the secondary output.
POE_PRESENT is sensed only on the isolated/system side.
Continuous IEEE 802.3at application budget: 22.5 W maximum.

## W5500 minimum capture checklist
- supplies/AVDD per current WIZnet reference at +3V3_SYS;
- local decoupling at every supply group;
- 25 MHz crystal network using selected crystal load model;
- EXRES1 = 12.4 kOhm 1%;
- PMODE straps for intended normal operation;
- boot-safe ETH_RST;
- deliberate ETH_INT pull-up owner;
- SPI_SCLK, SPI_MOSI, SPI_MISO, ETH_CS;
- optional source-side SPI series footprints on MCU-driven fast lines;
- MDI termination exactly per current WIZnet external-transformer reference;
- no integrated-MagJack termination assumptions.

## PCB MDI contract
100 ohm differential, controlled skew, no stubs, no pogo pads, minimize vias, keep away from Class-D and buck switching regions.

## Chassis / EMC
CHASSIS_ETH remains distinct from GND_SYS.
Any chassis-to-system capacitor/resistor network stays configurable/DNP until EMC and safety review.

## ERC / release gates
Do not mark Sheet 01 COMPLETE until:
1. Wurth channel/pin mapping checked from current datasheet.
2. Ag53024 pin numbering checked from Silvertel V1.1.
3. W5500 symbol pin numbers checked against official 48-pin package.
4. TE RJ45 footprint pin numbering checked against customer drawing.
5. no accidental PoE-primary-to-GND_SYS connection.
6. unused pins/channels have explicit NC semantics.
7. ERC is run in KiCad 9.x and exceptions individually justified.
8. schematic is saved by KiCad 9.x, not hand-authored.


## Pin-level review 2026-09-29

### W5500 verified pins
Official W5500 v1.1.0:
- pin 1 TXN
- pin 2 TXP
- pin 3 AGND
- pin 4 AVDD
- pin 5 RXN
- pin 6 RXP
- pin 7 DNC — do not connect
- pin 8 AVDD
- pin 9 AGND
- pin 10 EXRES1
- pin 28 VDD
- pin 29 GND
- pin 30 XI/CLKIN
- pin 31 XO
- pin 32 SCSn = ETH_CS
- pin 33 SCLK = SPI_SCLK
- pin 34 MISO = SPI_MISO
- pin 35 MOSI = SPI_MOSI
- pin 36 INTn = ETH_INT
- pin 37 RSTn = ETH_RST
- pins 43/44/45 PMODE2/PMODE1/PMODE0.

Critical correction: EXRES1 uses **12.4 kOhm 1%** per W5500 v1.1.0. Any earlier 4.12 kOhm value is superseded and must not enter the schematic/BOM.

### 100BASE-TX polarity contract
Follow WIZnet external-transformer reference polarity:
- W5500 TXP -> transformer TD+ PHY side -> cable TX+ -> RJ45 contact 1.
- W5500 TXN -> transformer TD- PHY side -> cable TX- -> RJ45 contact 2.
- W5500 RXP -> transformer RD+ PHY side -> cable RX+ -> RJ45 contact 3.
- W5500 RXN -> transformer RD- PHY side -> cable RX- -> RJ45 contact 6.

RJ45 contacts 4/5 and 7/8 remain spare-pair PoE Alternative-B inputs.

Do not assign numeric 7490220121 transformer pins in the native schematic until the current Wurth drawing/KiCad library symbol has been opened and visually cross-checked. The functional channel mapping above is frozen; numeric transformer-pad mapping remains a native-capture verification gate.

### Ag53024 logical pins
Ag53000 is pin-for-pin compatible with Ag5300/Ag5400. Capture only after cross-checking the current Ag53000 V1.1 table:
- pin 1 VIN+ : rectified PoE primary positive
- pin 2 VIN- : rectified PoE primary negative
- pin 3 AT-DET : Type-2 detection/status function; disposition must be explicitly chosen
- pins 4/5/6 IC : no connect
- pin 7 -VDC : GND_SYS
- pin 8 +VDC : +24V_POE
- pin 9 ADJ : explicit NC/default unless output trim is intentionally used
- pin 10 -VDC : GND_SYS

Pins 7 and 10 are internally common on the module but both PCB connections shall follow Silvertel layout guidance.

### Remaining native-capture checks
- exact numeric pad mapping for Wurth 7490220121;
- exact TE 2-1734264-1 signal-pad numbering from customer drawing;
- W5500 PMODE strap values/state from current reference;
- selected 25 MHz crystal MPN/load capacitors;
- disposition of Ag53024 AT-DET pin 3.


## Micro-gate closure — PHY mode, clock and official EDA authorities

### W5500 PHY strap — FROZEN
PMODE2/PMODE1/PMODE0 = **1/1/1**.
This selects all-capable 10/100BASE-T, half/full duplex with auto-negotiation enabled.

Implement deterministic hardware straps; do not rely on floating pins.

### W5500 crystal — FROZEN MPN
Y_ETH = **Abracon ABM8G-25.000MHZ-18-D2Y-T**.
Electrical basis:
- 25.000 MHz;
- CL = 18 pF;
- frequency tolerance = ±20 ppm;
- frequency stability = ±30 ppm;
- ESR = 60 ohm;
- fundamental mode;
- SMD 3.2 x 2.5 mm;
- -40 to +85 degC.

This satisfies the W5500 requirement for 25 MHz, <= ±30 ppm and CL 18 pF.
Initial C_XI/C_XO = **18 pF each**, matching the WIZnet reference schematic. Final load may be tuned only if measured/PCB parasitics justify it.
Retain the WIZnet reference bias/series topology around XI/XO.

### T_ETH official EDA authority
Wurth publishes a current official KiCad WE-LAN library plus STEP and S-parameter assets for 7490220121.
Native capture/layout shall import or independently verify against that official library.
The datasheet confirms PoE capability up to 600 mA per centre tap applies to pins 13-24.

Status: **OFFICIAL_KICAD_LIBRARY_AVAILABLE / NUMERIC_PIN_MAPPING_VERIFY_ON_IMPORT**.

### J_ETH official drawing authority
TE product 2-1734264-1 remains active and the official design authority is product drawing **ENG_CD_1734264_A2**.
TE explicitly instructs use of the product drawing for design activity.
Native footprint shall be transcribed/imported from that drawing/CAD and pin numbering visually cross-checked before ERC/layout.

Status: **OFFICIAL_DRAWING_CAD_AVAILABLE / PAD_NUMBERING_VERIFY_ON_NATIVE_IMPORT**.

### Remaining Sheet-01 gates
Electrical architecture gates are closed.
Native-tool-only gates remain:
1. visually verify 7490220121 numeric symbol/pad mapping after importing Wurth KiCad library;
2. visually verify TE 2-1734264-1 pad numbering against ENG_CD_1734264_A2;
3. run KiCad 9 ERC;
4. save native schematic with KiCad 9.
