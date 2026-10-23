# AudioPicture P1 — system specification

Status: **HISTORICAL_P1_84MM / SUPERSEDED_BY_REV_E / NOT MEASURED**. Product authority is now [Rev.E DML ≤ 30 mm](../architecture/v2.2-rev-e-dml-30mm.md). This file records the withdrawn 84 mm cone prototype path (was under [Rev.D](../architecture/v2.2-rev-d-mono-room.md)). Sensor/network function list still informs Rev.E packaging.

## 1. Product

| Item | P1 value | Source |
| --- | --- | --- |
| Outline | 320 × 400 × 84 mm, wall-hung on a French cleat | `mechanical/p1/p1_params.json`, gate "body depth ≤ 84 mm" |
| Acoustics | mono two-way + 2 passive radiators, one sealed volume | Rev.D §1 |
| Drivers | Dayton ND91-4 (woofer), ND20FB-4 rear mount (tweeter), 2 × ND90-PR | BOM section B |
| Net driver air | **4.508 L** (CAD, drivers/ties/ribs/partition deducted) | `evidence/p1/box-model-p1.json` |
| Box model, after DSP | F3 49.3 Hz, 55–500 Hz −0.76/+0.85 dB, 88.2 dB flat max at 1 m | same, `dsp_design_one_supplied_disk` |
| Wall stiffness | rear f1 1308 Hz, baffle f1 565 Hz, wall/air compliance 0.38 % | `evidence/p1/wall-fd.json` |
| Mass | 4.39 kg complete | `evidence/p1/cad-gates.json` |
| Supply | 24 V DC 5.5/2.1 jack, or PoE 802.3at through Ag53024; USB-C for service only | MAIN schematic |
| Network | Ethernet W5500 (10/100), Wi-Fi ESP32-S3 | |
| Sensors | XVF3800 + 4-mic linear array, LD6004 60 GHz radar, SHT45, OPT3004, INA228 | |

All acoustic figures are model results. The bench sweep in [assembly.md](assembly.md) §7 decides the passive added mass and the fibre fill.

## 2. Departures from Rev.D

| Rev.D | P1 | Why |
| --- | --- | --- |
| cabinet material open | SLS PA12, dyed black, 10 mm side walls, ribbed 6 mm rear skin, 16 tie columns | user choice; FD screening keeps every panel mode above 500 Hz and wall compliance < 1 % of the air |
| 4.12 L estimate | 4.508 L from the CAD | the ribs and ties came out lighter than the estimate |
| one 7.3 g disk on each ND90-PR | 4.5 g added mass each is the nominal optimum; the supplied 7.3 g disk is build option A (−1.8 dB flat max) | box model at 4.508 L |
| no passive network | 47 µF NP film-equivalent bipolar cap in series with the tweeter (C71) | DC and fault protection only (fc ≈ 850 Hz into 4 Ω); the TAS DSP still does LR4 3 kHz and must include C71 in the tweeter target curve |
| output filter "retune for 4 Ω" | 10 µH XAL7050 + 0.68 µF per output leg (BTL, both channels) | TAS5825M datasheet BD-mode 4 Ω table |
| electronics in a sealed pocket | pocket 10–80 mm in Y behind the bottom of the baffle, 84 mm deep, gasketed partition | `tub.partition_y` |

## 3. Electronics

One MAIN board (292 × 58 mm, 4 layers, 1.6 mm) carries everything except the XVF3800 Flex core, the mic array and the radar, which are certified modules on harnesses.

Stack-up: F.Cu signals and parts (faces the room), In1 GND, In2 3V3, B.Cu signals plus the 24 V `VBUS24` strip under the amplifier and the bucks. The PoE primary sits in its own copper region with a 2 mm creepage moat and a silkscreen barrier.

| Block | Parts | Notes |
| --- | --- | --- |
| DC input | J1, F1 4 A, D1 SMBJ33A, LM74700 ideal diode U1 | |
| PoE | J2 RJ45, T1 magnetics, 8 × STPS2H100A bridge, Ag53024 U2, LM74700 U3 | R14 sets 22.8 V so the DC jack wins the OR |
| 24 V rail | `VBUS24`, R20 8 mΩ shunt + INA228 U4 | power telemetry, I2C 0x40 |
| 5 V | TPSM53603 U5, 3 A | XVF3800 (switched), LEDs, 3V3 buck |
| 3V3 | TPS62823 U6, 3 A | ESP32-S3, W5500, sensors |
| Amplifier | TAS5825M U11, BTL ch A woofer, ch B tweeter | I2C 0x4C, PVDD 24 V; hand layout in `gen/amp_hand.py` |
| Voice | J5 IDC to the Flex core (pin map: [flex-header.md](flex-header.md)) | hardware privacy mute U13 + U7 |
| Radar | J6 GH 1.25 6-way | shares UART0 |
| Environment | SHT45 U14, OPT3004 U15 on a slotted island at the right edge | I2C 0x44, 0x45 |

### 3.1 ESP32-S3 pin map

| GPIO | Net | Use |
| --- | --- | --- |
| IO0 | `ESP_BOOT` | strap, SW3 |
| EN | `ESP_EN` | reset, RC + SW4 |
| IO1 / IO2 | `I2C0_SDA` / `I2C0_SCL` | TAS5825M, INA228, SHT45, OPT3004 |
| IO3 | `PG_5V` | 5 V power-good input |
| IO4 / IO5 / IO6 / IO7 | `XVF_BCLK` / `XVF_LRCK` / `XVF_DATA1` / `ESP_XVF_DOUT` | I2S1 slave to the XVF3800 |
| IO8 | `TAS_FAULT` | open-drain, 10 kΩ pull-up |
| IO9 | `RADAR_IO` | LD6004 presence output |
| IO10–IO14, IO21 | `ETH_CS`, `ETH_MOSI`, `ETH_SCLK`, `ETH_MISO`, `ETH_INT`, `ETH_RST` | SPI2 to W5500 |
| IO15 / IO16 / IO17 | `ESP_TAS_BCLK` / `ESP_TAS_LRCK` / `ESP_TAS_SDIN` | I2S0 master to the TAS5825M, 33 Ω series |
| IO18 | `TAS_PDN` | 100 kΩ pull-down: amp off until firmware is up |
| IO19 / IO20 | USB D− / D+ | console and flashing (USB-Serial-JTAG) |
| IO38 | `INA_ALERT` | |
| IO39 | `MUTE_STATE` | high = mics unpowered |
| IO40 | `BTN_ACTION` | SW2 |
| IO41 / IO42 | `ESP_SDA1` / `ESP_SCL1` | I2C1 to the XVF3800 |
| IO47 | `ESP_X1D13` | XVF GPIO |
| IO48 | `LED_DIN` | WS2812B-2020 status LED (5 V, D5 level drop) |
| RXD0 / TXD0 | `RADAR_TX` / `RADAR_RX` | UART0 to LD6004 |
| IO35–IO37 | — | used by the octal PSRAM of the N16R8 |

Firmware rules that the hardware relies on:

1. UART0 belongs to the radar. Logs and flashing go over USB-Serial-JTAG only.
2. While `MUTE_STATE` is high, IO4–IO7, IO41, IO42 and IO47 are inputs without pull-ups.
3. `TAS_PDN` stays low until PVDD is valid (`PG_5V` high and INA228 bus voltage > 20 V) and the DSP coefficients are loaded.
4. On PoE (bus voltage < 23.5 V) the amplifier limiter drops the program ceiling as in Rev.D §2.

### 3.2 Power budget (estimate, 24 V side)

| Load | Typ. | Peak | Basis |
| --- | ---: | ---: | --- |
| ESP32-S3 + W5500 + sensors (3V3) | 0.9 W | 2.0 W | Wi-Fi TX bursts 350 mA, W5500 130 mA |
| XVF3800 Flex + mics (5 V) | 1.0 W | 1.5 W | VERIFY on bench |
| Radar LD6004 | 0.4 W | 0.6 W | VERIFY datasheet |
| Status LED | 0.05 W | 0.3 W | one WS2812B |
| Buck losses | 0.4 W | 0.8 W | 85–90 % |
| TAS5825M, music at 85 dB / 1 m | 3 W | — | crest factor 12 dB |
| TAS5825M, limiter ceiling | — | 30 W (DC) / 18 W (PoE) | woofer 30 W rating, PoE class 4 headroom |
| **Total** | **≈ 6 W** | **≈ 35 W DC, ≈ 23 W PoE** | the 24 V / 2.5 A adapter covers DC |

## 4. Materials

| Part | Material | Finish |
| --- | --- | --- |
| Tub, baffle, front frame, mic and radar retainers, 2 button rods | SLS PA12 (EOS PA 2200 or HP 3D HR PA12) | dyed black (frame dyed to finish); 6 mm rear skin, 10 mm side walls, 12 mm baffle |
| French cleat pair (picture cleat 130 × 24 × 8, wall rail 150 × 24 × 8) | EN AW-6082 T6 | anodised |
| Light pipes (3) | PMMA rod Ø3 × 30.3 mm | polished ends |
| Gaskets | PORON 4701-30 die-cut rings under the driver flanges; EPDM closed-cell 6 × 2 mm on the baffle perimeter (0.8 mm compressed) | |
| Inserts | Ruthex RX-M3x5.7 (58) and RX-M4x8.1 (20), heat-set brass | |
| Screws | A2 stainless: ISO 10642 countersunk for the baffle, ISO 7380 for drivers, boards and retainers | |
| Front cloth | ShowTex Speaker Mesh Print 3838, printed picture; frame held by 14 N52 8 × 3 magnets on DC01 steel discs | |
| Damping | polyester fibre in the driver chamber, 40 g start value; optional 2 mm butyl CLD on the rear skin | trimmed on the impedance sweep / accelerometer scan |

## 5. Open items (VERIFY)

The BOM marks 11 lines as VERIFY. They are checks against a part drawing, not design gaps:

- Flex XVF3800 header pitch and pin numbering (W1, J5).
- LD6004 harness pinout (J6, W2).
- Ag53024 ADJ resistor table for 22.8 V (R14).
- PJ-063AH vs PJ-063BH land (J1), Amphenol 54602 suffix (J2), TFM201610 land (L1).
- C21 height (16 mm) against its 16.5 mm envelope.
- driver tab sizes for the FASTON receptacles (W3).
- fabric print transfer (F1) and fibre fill amount (D1).
