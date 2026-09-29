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
- EXRES1 = 4.12 kOhm 1%;
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
