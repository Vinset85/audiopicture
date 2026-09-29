# MAIN Rev.A — Native KiCad Capture Manifest

Status: **AUTHORITATIVE_CAPTURE_INDEX**
Target: **KiCad 9.x**

This document is the top-level transcription index for MAIN Rev.A. It does not replace the detailed sheet specifications or manufacturer documentation and it is not a hand-authored KiCad schematic.

## Native hierarchy
Root: `audiopicture-main.kicad_sch`

1. `01-ethernet-poe.kicad_sch`
2. `02-power-input-oring.kicad_sch`
3. `03-power-rails-monitor.kicad_sch`
4. `04-esp32-control.kicad_sch`
5. `05-audio-tas5825m.kicad_sch`
6. `06-usb-service.kicad_sch`
7. `07-daughterboards.kicad_sch`
8. `08-test-production.kicad_sch`

Native files shall be generated, opened, ERC-checked and saved by KiCad 9.x. Do not hand-author .kicad_sch/.kicad_pcb syntax.

## Global power nets
`+24V_POE`, `+24V_EXT`, `+24V_RAW`, `+24V_SYS`, `+5V_SYS`, `+5V_SERVICE`, `+3V3_SYS`, `GND`.

PoE primary and chassis are not ordinary system power nets. Keep PoE-primary isolation explicit. `CHASSIS_ETH` and `CHASSIS_USB` remain controlled EMC/chassis domains.

## Global digital/control nets
`SPI_SCLK`, `SPI_MOSI`, `SPI_MISO`, `ETH_CS`, `ETH_RST`, `ETH_INT`,
`RADAR_CS`, `RADAR_IRQ`, `RADAR_RST`, `RADAR_EN`,
`I2C_SDA`, `I2C_SCL`,
`AUD_BCLK`, `AUD_LRCLK`, `AUD_TX`, `AUD_RX`,
`AMP_PDN`, `AMP_FAULT`,
`VOICE_RST`, `VOICE_IRQ`, `MIC_HW_EN`,
`POWER_ALERT`, `5V_PG`, `3V3_PG`, `POE_PRESENT`, `EXT_PRESENT`,
`USB_D-`, `USB_D+`, `UART_TX`, `UART_RX`, `STATUS_LED`, `SERVICE_TOUCH`.

## Sheet 01 — Ethernet / PoE
Authority: `01-ethernet-poe-capture-contract.md` plus final freeze sections of `w5500-ag5324-rev-a.md`.

Frozen:
- W5500 LQFP-48;
- EXRES1 12.4 kOhm 1%;
- PMODE 111;
- Abracon ABM8G-25.000MHZ-18-D2Y-T;
- Wurth 7490220121;
- TE 2-1734264-1;
- 8 x STPST3H100AF;
- Silvertel Ag53024;
- PoE application continuous budget 22.5 W.

Exports: `+24V_POE`, `POE_PRESENT`, `SPI_MISO`, `ETH_INT`.
Imports: `+3V3_SYS`, `SPI_SCLK`, `SPI_MOSI`, `ETH_CS`, `ETH_RST`.
Native-only gates: Wurth numeric mapping, TE pad numbering, ERC.

## Sheet 02 — Power input / source priority
Authority: `input-oring-priority-rev-a.md`.

Frozen architecture:
- external 24 V / 3 A recommended;
- TPS48100QDGXRQ1 PoE disconnect;
- ISC035N10NM5LF2ATMA1 MOSFET baseline;
- TLV1822QDGKRQ1 external UV/OV window;
- LM4040A25IDBZR reference;
- UV 20.5 V rising / 19.0 V falling;
- OV 25.3 V trip / 24.7 V recovery;
- external source deterministic priority;
- break-before-make, MCU-independent.

Imports: `+24V_POE`.
Exports: `+24V_EXT`, `+24V_RAW`, `EXT_PRESENT`.
Gate: final SOA/transient/thermal verification and exact connector mechanics.

## Sheet 03 — Rails / INA228
Authority: `rails-monitor-rev-a.md`.

Frozen:
- INA228AIDGSR;
- RSH1 = Littelfuse L4CL1206LR008FNR, 8 mOhm true four-terminal Kelvin shunt, 0.5 W;
- TPSM63603V5RDHR 24->5 V;
- TDK C3225X7R1H475K250AB input MLCCs;
- TPS62823DLCR 5->3.3 V;
- TDK TFM201610ALM-R47MTAA 470 nH;
- INA filter 10 Ohm/10 Ohm + 100 nF differential.

Imports: `+24V_RAW`, `I2C_SDA`, `I2C_SCL`.
Exports: `+24V_SYS`, `+5V_SYS`, `+3V3_SYS`, `POWER_ALERT`, `5V_PG`, `3V3_PG`.
BOM gates: 5 V COUT effective capacitance and 3.3 V COUT effective capacitance. RSH1 device/value/package is frozen; PCB thermal/Kelvin routing and calibration remain validation gates.

## Sheet 04 — ESP32 control
Authority: `esp32-s3-main-rev-a.md` and `gpio-interface-contract.md`.

U1: ESP32-S3-WROOM-1-N16R8.
GPIO26..37 unavailable. GPIO0/3/45/46 protected straps.
CHIP_PU: 10 kOhm pull-up + 1 uF to GND.
GPIO19/20 = USB D-/D+.
Shared SPI: GPIO11 MOSI, GPIO12 SCLK, GPIO13 MISO; GPIO10 ETH_CS; GPIO14 RADAR_CS.
I2S: GPIO4..7.
Voice: GPIO38 RST, GPIO39 IRQ.
Radar: GPIO16 EN, GPIO42 RST.
UART0: GPIO43/44.

Hardware safe states are mandatory and external.
Gate: antenna keep-out/layout and RF/transient/SI validation.

## Sheet 05 — TAS5825M / DML
Authority: `tas5825m-dml-rev-a.md`.

Frozen:
- TAS5825MRHBR;
- +24V_SYS PVDD;
- four 0.47 uF bootstrap capacitors;
- 48 kHz I2S, 32-bit slots;
- four DAEX25FHE-4 as two series pairs, nominal 8 Ohm/channel;
- real LC filter architecture;
- 10 uH per BTL leg is capture baseline;
- 0.68 uF-class capacitor network is reference/capture placeholder only.

Exports: `AMP_FAULT`, left/right DML connectors.
Imports: `+24V_SYS`, `I2C_SDA/SCL`, `AUD_BCLK/LRCLK/TX`, `AMP_PDN`.
Production gate: final LC topology/MPNs after mounted-DML impedance model plus thermal/EMC/acoustic validation.

## Sheet 06 — USB service
Authority: `usb-c-service-rev-a.md`.

Frozen:
- USB 2.0 UFP/device only;
- CC1/CC2 each 5.1 kOhm to GND;
- GPIO19 D-, GPIO20 D+;
- TPD2EUSB30ADRTR ESD;
- VBUS creates +5V_SERVICE sensing/service domain only;
- no power path from USB to +5V_SYS/+3V3_SYS;
- common-mode choke DNP default.

Preferred connector family: GCT USB4085; exact mechanical variant remains gate.
Recovery uses hardware GPIO0 + CHIP_PU and ESP32 ROM path.

## Sheet 07 — Daughterboards
Authority: `daughterboards-rev-a.md`.

Connector family: Hirose FH12, 0.5 mm ZIF, 0.30 mm FPC.
- J101 VOICE: 16 physical contacts, 14 logical signals + 2 additional GND references; preferred FH12-16S-0.5SH(55).
- J201 RADAR: 12 contacts.
- J301 ENV: 8 contacts.
- MAIN owns I2C pull-ups and system rails.
- no daughterboard back-power.

Gate: exact physical ordering/contact side/cable drawing and FPC lengths.

## Sheet 08 — Production test
Authority: `factory-test-rev-a.md`.

TP01..TP20 baseline is mandatory for native capture.
Every-unit test includes hardware safe-state and microphone privacy OFF validation.
USB normally uses the real USB-C connector, not extra pogo contacts.
TP03 direct injection is engineering/diagnostic only.

Gate: final pogo coordinates, fixture alignment and production limits.

## ERC rules
- no blanket PWR_FLAG suppression;
- one deliberate pull-up owner per open-drain bus;
- explicit NC semantics;
- no undefined reset/enable;
- no signal injection into unpowered daughterboards;
- no PoE-primary to GND_SYS connection;
- no duplicate/conflicting global labels;
- justified ERC exceptions documented individually.

## Initial PCB net classes
`POWER_24V_HIGH`, `POWER_5V`, `POWER_3V3`, `CLASS_D`, `ETH_MDI`, `USB_FS`, `I2S`, `SPI_FAST`, `SENSITIVE`.

Widths/clearances remain PCB-stackup/current/thermal calculations, not schematic guesses.

## Native capture order
1. Create project/root hierarchy in KiCad 9.x.
2. Capture Sheet 02 power input.
3. Capture Sheet 03 rails.
4. Capture Sheet 04 ESP32 minimum system.
5. Capture Sheet 01 Ethernet/PoE.
6. Capture Sheet 05 audio.
7. Capture Sheet 06 USB.
8. Capture Sheet 07 daughterboards.
9. Capture Sheet 08 test points.
10. Run ERC and resolve every exception.
11. Run symbol/footprint audit.
12. Begin PCB floorplan only after schematic review.

## Stop conditions
Do not improvise a value/MPN/footprint when a detailed specification marks it OPEN, VALIDATE, DNP or a release gate.
Do not convert a capture baseline into a production freeze merely to satisfy ERC.
Do not start routing before isolation, antenna, connector and high-current floorplan constraints are represented.

Status: **MAIN_REV_A_SPECIFICATION_READY_FOR_NATIVE_KICAD_CAPTURE**.
