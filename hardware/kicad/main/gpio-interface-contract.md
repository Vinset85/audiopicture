# MAIN Rev.A — GPIO / interface contract

| ESP32-S3 GPIO | Function | Boot requirement |
|---|---|---|
| GPIO0 | BOOT/service | strapping; service only |
| GPIO1 | AMP_FAULT | input |
| GPIO2 | AMP_PDN | hardware-safe amplifier OFF during reset |
| GPIO4 | AUD_BCLK | I2S |
| GPIO5 | AUD_LRCLK | I2S |
| GPIO6 | AUD_TX | I2S TX |
| GPIO7 | AUD_RX | I2S RX |
| GPIO8 | ETH_RST | safe reset state |
| GPIO9 | ETH_INT | input |
| GPIO10 | ETH_CS | inactive at boot |
| GPIO11 | SPI MOSI | W5500 bus |
| GPIO12 | SPI SCLK | W5500 bus |
| GPIO13 | SPI MISO | W5500 bus |
| GPIO14 | RADAR_CS | inactive at boot |
| GPIO15 | RADAR_IRQ | input |
| GPIO16 | RADAR_EN | radar off at boot |
| GPIO17 | I2C SDA | shared |
| GPIO18 | I2C SCL | shared |
| GPIO19 | USB D- | native USB |
| GPIO20 | USB D+ | native USB |
| GPIO21 | MIC_HW_EN | privacy-safe OFF at reset |
| GPIO38 | service/expansion | TBD |
| GPIO39 | expansion IRQ | input |
| GPIO40 | STATUS_LED | hidden LED |
| GPIO41 | SERVICE_TOUCH | hidden service/pairing input |
| GPIO42 | RADAR_RST | radar reset |
| GPIO43 | UART TX | factory/debug |
| GPIO44 | UART RX | factory/debug |

GPIO26..37: **do not use**; module flash/PSRAM reservation.
GPIO3/45/46: avoid casual assignment; strapping implications must be reviewed.

## SPI architecture — FROZEN Rev.A
One shared host SPI bus is used for W5500 and BGT60TR13C:
- GPIO11 = SPI_MOSI
- GPIO12 = SPI_SCLK
- GPIO13 = SPI_MISO
- GPIO10 = ETH_CS
- GPIO14 = RADAR_CS

Rationale: ESP32-S3 GPIO matrix permits peripheral routing, while the WROOM-1-N16R8 pin budget is constrained by non-exposed GPIO22..25 and memory use on GPIO26..37. Independent chip selects and firmware bus arbitration prevent simultaneous transactions.

Additional controls:
- GPIO8 = ETH_RST
- GPIO9 = ETH_INT
- GPIO15 = RADAR_IRQ
- GPIO16 = RADAR_EN\n- GPIO42 = RADAR_RST
- GPIO38 = VOICE_RST
- GPIO39 = VOICE_IRQ

SPI electrical rule: radar-side PCB-C performs 3.3 V <-> 1.8 V translation. W5500 remains 3.3 V native.

## Audio clock ownership
ESP32-S3 is host/master for the synchronized AudioPicture audio domain:
- BCLK
- LRCLK
- TX far-end/program audio
- RX XVF3800 processed microphone path.

Exact peripheral assignment and DMA topology are firmware validation items.


## Pin-budget decision — FROZEN Rev.A
No GPIO expander is required.

Final topology:
- shared SPI data/clock: GPIO11/12/13;
- W5500 CS: GPIO10;
- radar CS: GPIO14;
- VOICE_RST: GPIO38;
- VOICE_IRQ: GPIO39;
- GPIO42 is assigned to RADAR_RST so reset and power/enable remain independent.

Strapping pins GPIO0/3/45/46 remain protected from normal peripheral assignments. GPIO26..37 remain unavailable due to module memory use; GPIO22..25 are not available as module pins.

Firmware must serialize W5500/radar SPI access and support device-specific SPI clock/mode settings per transaction.
