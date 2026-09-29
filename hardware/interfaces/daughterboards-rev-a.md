# Sheet 07 — Daughterboard Interfaces / Expansion Rev.A

Status: **interface contract FROZEN Rev.A**. Exact FPC connector family/pitch remains VALIDATE_MECHANICAL_SI.

## 1. Design rules
MAIN connects to:
- PCB-B VOICE through J101;
- PCB-C RADAR through J201;
- PCB-D ENV through J301;
- optional internal expansion through J401.

Rules:
- every daughterboard gets multiple ground returns where bandwidth/current requires;
- no undefined power direction;
- no daughterboard may back-power MAIN through signal pins;
- FPC pin numbering is verified from the mating-side drawing before PCB release;
- connector contacts must be rated for rail current with margin.

## 2. J101 VOICE — 14 pins
Baseline/frozen logical pinout:

| Pin | Net | Direction at MAIN | Purpose |
|---|---|---|---|
| 1 | +5V_SYS | OUT | voice power |
| 2 | +5V_SYS | OUT | parallel power contact |
| 3 | GND | — | return |
| 4 | GND | — | return |
| 5 | AUD_BCLK | OUT | ESP32 audio clock |
| 6 | AUD_LRCLK | OUT | ESP32 frame clock |
| 7 | AUD_TX | OUT | far-end/AEC reference toward XVF3800 |
| 8 | AUD_RX | IN | processed voice audio |
| 9 | I2C_SDA | BIDIR | control |
| 10 | I2C_SCL | OUT/BIDIR | control clock |
| 11 | VOICE_RST | OUT | XVF3800 reset/control |
| 12 | VOICE_IRQ | IN | XVF3800 interrupt/status |
| 13 | MIC_HW_EN | OUT | hardware microphone power control |
| 14 | +3V3_SYS | OUT | logic/support rail |

GPIO:
- VOICE_RST = GPIO38
- VOICE_IRQ = GPIO39
- MIC_HW_EN = GPIO21.

PCB-B owns +3V3_MIC switching and all XVF3800-specific local rails.

## 3. J101 signal integrity
I2S clock/data shall have continuous ground reference across FPC.

Current pinout has adjacent GND near the power/upper group but not interleaved ground between every I2S signal. Therefore:
- FPC length should be kept short;
- source-side series damping footprints are provided on MAIN;
- if SI/EMI simulation requires more ground interleaving, connector pin count may increase before mechanical freeze without changing logical interface.

Logical interface is frozen; physical contact count may be revised upward for SI.

## 4. J201 RADAR — 12 pins
Corrected Rev.A pinout for the **shared SPI bus**:

| Pin | Net | Direction at MAIN | Purpose |
|---|---|---|---|
| 1 | +3V3_SYS | OUT | radar board input |
| 2 | +3V3_SYS | OUT | parallel power |
| 3 | GND | — | return |
| 4 | GND | — | return |
| 5 | SPI_SCLK | OUT | shared W5500/radar SPI clock |
| 6 | SPI_MOSI | OUT | shared SPI data to radar |
| 7 | SPI_MISO | IN | shared SPI data from radar |
| 8 | RADAR_CS | OUT | dedicated radar chip select |
| 9 | RADAR_IRQ | IN | radar interrupt |
| 10 | RADAR_RST | OUT | reset |
| 11 | RADAR_EN | OUT | local radar power/translator enable |
| 12 | RESERVED | — | future/service |

PCB-C performs:
- +3V3_SYS -> +1V8_RADAR regulation;
- 3.3 V <-> 1.8 V fixed-direction level translation;
- radar reference clock.

W5500 remains on MAIN and shares only SPI_SCLK/MOSI/MISO; ETH_CS and RADAR_CS remain independent.

## 5. Radar reset/enable implementation
The current ESP32 map uses GPIO16 for radar reset/enable control.

If PCB-C requires independent RADAR_RST and RADAR_EN electrical controls, J201 pins 10/11 shall be resolved by:
- deriving one signal locally with a reset supervisor/load-switch timing network; or
- assigning the remaining GPIO42 to the second function.

Preferred freeze target:
- GPIO16 = RADAR_EN
- GPIO42 = RADAR_RST

This uses the available expansion pin and avoids ambiguous tied reset/enable behavior.

## 6. J301 ENV — 8 pins
| Pin | Net | Direction at MAIN | Purpose |
|---|---|---|---|
| 1 | +3V3_SYS | OUT | ENV power |
| 2 | +3V3_SYS | OUT | parallel/contact redundancy |
| 3 | GND | — | return |
| 4 | GND | — | return |
| 5 | I2C_SDA | BIDIR | SHT45/OPT3004 |
| 6 | I2C_SCL | OUT/BIDIR | bus clock |
| 7 | ENV_INT | IN/reserved | future ENV interrupt |
| 8 | BOARD_ID | IN | resistor-coded board revision |

ENV_INT need not be assigned to an ESP32 GPIO in Rev.A unless a future sensor requires it.

BOARD_ID may be read through:
- ADC-capable safe GPIO if available; or
- I2C identification EEPROM/device in a later revision.

Do not consume a critical GPIO solely for BOARD_ID before production need is demonstrated.

## 7. I2C distribution
MAIN owns I2C pull-ups.

Branches:
- local MAIN devices;
- J101 VOICE;
- J301 ENV;
- expansion J401.

Rules:
- total bus capacitance must be calculated after FPC lengths are known;
- optional small series resistor footprints at each daughterboard branch;
- no daughterboard strong pull-up unless explicitly DNP/configured;
- default bus target 400 kHz only if measured capacitance/rise time supports it; otherwise reduce frequency.

## 8. Power protection at FPC
Daughterboard power outputs shall include:
- local MAIN bulk/ceramic support as appropriate;
- optional 0R/ferrite/current-measure footprint for bring-up;
- no large hot-plug capacitance on daughterboard without system inrush review.

FPC connectors are internal, not intended for hot-plug by users.

## 9. Expansion J401
Internal service/expansion connector baseline:
- +5V_SYS
- +3V3_SYS
- GND x2
- I2C_SDA
- I2C_SCL
- UART_TX
- UART_RX
- GPIO/INT reserved
- optional board-detect.

Target future devices:
- CO2
- VOC/air-quality
- additional environmental sensing.

Expansion must not be advertised as arbitrary user-accessible 5 V power without current-budget qualification.

## 10. ESD
Internal FPCs do not automatically receive heavy external-interface TVS arrays.

Use ESD protection only where:
- cable is service-accessible;
- mechanical design permits external contact;
- EMC testing demonstrates susceptibility.

Avoid unnecessary capacitance on I2S/SPI.

## 11. Grounding
All daughterboard grounds return to common system GND.

Do not create isolated analog ground islands.

Mechanical/radar RF keep-outs do not change electrical GND strategy.

## 12. Connector selection
J101/J201/J301 exact family: VALIDATE.

Selection criteria:
- locking FPC/FFC or board-to-board connector;
- contact current rating;
- pitch compatible with assembly;
- insertion-cycle requirement;
- height compatible with 40 mm enclosure;
- readily available production part;
- clear mating-side pin numbering;
- optional shield/ground contacts where beneficial.

## 13. Factory test
With daughterboards attached:
1. rail resistance-to-ground before power.
2. board power.
3. I2C scan.
4. VOICE reset/IRQ.
5. I2S clock/data.
6. microphone hardware enable.
7. radar enable/reset.
8. radar shared-SPI access while Ethernet traffic active.
9. ENV measurements.
10. connector flex/contact test.

## 14. Release gates
Sheet 07 becomes production FROZEN after:
1. exact connector family/pitch;
2. mating orientation/pin-1 drawing;
3. FPC lengths;
4. I2S SI/EMI validation;
5. I2C capacitance/rise-time validation;
6. radar reset/enable pin split frozen;
7. daughterboard power-current measurement;
8. mechanical retention/vibration test.


## Rev.A connector freeze
Connector family: Hirose FH12, 0.5 mm pitch, ZIF, 0.30 mm FPC.

VOICE uses a 16-contact physical connector; the existing 14 logical signals remain unchanged and two extra contacts are ground references for the I2S group. Preferred part: FH12-16S-0.5SH(55).

RADAR uses 12 contacts. ENV uses 8 contacts. Keep the existing duplicated power and ground contacts.

Radar controls are independently frozen: GPIO16 = RADAR_EN and GPIO42 = RADAR_RST.

MAIN is the only source of +5V_SYS and +3V3_SYS on daughterboard interfaces. Daughterboards must not back-power MAIN. MAIN remains the only populated owner of shared I2C pull-ups.

Status: READY_FOR_NATIVE_KICAD_CAPTURE_WITH_FPC_MECHANICAL_DRAWING_GATE.
