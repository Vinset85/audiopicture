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
| GPIO16 | RADAR_RST/EN | radar off/reset at boot |
| GPIO17 | I2C SDA | shared |
| GPIO18 | I2C SCL | shared |
| GPIO19 | USB D- | native USB |
| GPIO20 | USB D+ | native USB |
| GPIO21 | MIC_HW_EN | privacy-safe OFF at reset |
| GPIO38 | service/expansion | TBD |
| GPIO39 | expansion IRQ | input |
| GPIO40 | STATUS_LED | hidden LED |
| GPIO41 | SERVICE_TOUCH | hidden service/pairing input |
| GPIO42 | expansion | TBD |
| GPIO43 | UART TX | factory/debug |
| GPIO44 | UART RX | factory/debug |

GPIO26..37: **do not use**; module flash/PSRAM reservation.
GPIO3/45/46: avoid casual assignment; strapping implications must be reviewed.

## SPI architecture
Rev.A preference:
- SPI controller/bus A: W5500.
- radar interface exposed separately to PCB-C and may use a second ESP32 SPI controller if driver/resource validation permits.

Do not force W5500 and radar onto one clock domain solely to save pins.

## Audio clock ownership
ESP32-S3 is host/master for the synchronized AudioPicture audio domain:
- BCLK
- LRCLK
- TX far-end/program audio
- RX XVF3800 processed microphone path.

Exact peripheral assignment and DMA topology are firmware validation items.
