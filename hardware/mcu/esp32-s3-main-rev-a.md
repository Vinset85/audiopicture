# Sheet 04 — ESP32-S3 Control / USB / Interfaces Rev.A

Status: **implementable schematic specification**. Final antenna placement, USB ESD part and exact reset/boot passives remain subject to Espressif reference-design/layout validation.

## 1. Main MCU module
U1: **ESP32-S3-WROOM-1-N16R8**

Production baseline:
- 16 MB flash
- 8 MB PSRAM
- 2.4 GHz Wi-Fi
- Bluetooth LE
- native USB 2.0 Full-Speed capability
- module antenna version unless final enclosure RF study requires an external-antenna module variant.

Supply: +3V3_SYS.

## 2. Supply
3V3 input shall follow Espressif module hardware-design guidance.

Requirements:
- low-impedance +3V3_SYS path;
- local bulk capacitor near module supply;
- 100 nF-class high-frequency bypass near supply entry;
- design for Wi-Fi current transients without rail collapse;
- 3V3_PG / reset strategy prevents uncontrolled boot on an invalid rail.

Exact local bulk network is frozen only after TPS62823 transient simulation/measurement.

## 3. EN / CHIP_PU
CHIP_PU must have a defined hardware reset network.

Baseline:
- pull-up to +3V3_SYS;
- RC delay/filter according to current Espressif hardware guidelines;
- reset/service button or factory pogo access pulls CHIP_PU low;
- supervisor may assert reset when +3V3_SYS is invalid.

Do not rely on ESP32 internal state alone for power-on reset robustness.

## 4. Boot strap
GPIO0 is reserved as BOOT/service strap.

Baseline:
- pull-up to +3V3_SYS;
- factory/service control can pull GPIO0 low while reset is asserted/released;
- normal user operation never requires access to a visible BOOT button.

GPIO3, GPIO45 and GPIO46 are strapping-sensitive and remain unassigned in Rev.A unless later use is explicitly reviewed against boot behavior.

## 5. Flash / PSRAM pin reservation
For ESP32-S3-WROOM-1-N16R8, GPIO26..GPIO37 are treated as unavailable/reserved for the module memory interface.

They shall not appear on production peripheral nets.

## 6. Native USB
GPIO19 = USB D-
GPIO20 = USB D+

USB-C service connector is implemented in Sheet 06.

MCU-side requirements:
- route D+/D- as USB FS differential pair;
- short, symmetric routing;
- no stubs;
- ESD device close to connector;
- optional series resistor footprints only if recommended by current Espressif reference design/SI validation.

USB is for:
- factory flashing;
- recovery;
- diagnostics/service.

It is not the normal end-user provisioning requirement and +5V_SERVICE does not power the audio rail.

## 7. I2C
GPIO17 = I2C_SDA
GPIO18 = I2C_SCL

Bus devices include:
- INA228
- TAS5825M
- XVF3800 control
- SHT45
- OPT3004
- future expansion.

MAIN owns the primary pull-up network to +3V3_SYS.

Initial pull-up value: 4.7 kOhm each, status VALIDATE_BUS_CAPACITANCE.

Provide accessible test points.

## 8. W5500 SPI
Dedicated baseline host bus:
- GPIO11 = ETH_MOSI
- GPIO12 = ETH_SCLK
- GPIO13 = ETH_MISO
- GPIO10 = ETH_CS
- GPIO8 = ETH_RST
- GPIO9 = ETH_INT

Firmware may map the bus to an available ESP32-S3 general-purpose SPI controller through GPIO matrix.

## 9. Radar SPI
Baseline:
- GPIO14 = RADAR_CS
- GPIO15 = RADAR_IRQ
- GPIO16 = RADAR_RST/EN

Radar clock/MOSI/MISO allocation is NOT assumed to share W5500 pins.

At schematic freeze, allocate the remaining suitable GPIOs/peripheral routing only after checking:
- second SPI host availability in ESP-IDF;
- USB/UART/I2S conflicts;
- strapping pins;
- module memory pins.

If a separate hardware SPI bus cannot be allocated cleanly, sharing W5500 SPI is permitted with separate CS and conservative arbitration. The architecture requirement is isolation of traffic behavior, not unnecessary pin consumption.

## 10. Audio I2S
GPIO4 = AUD_BCLK
GPIO5 = AUD_LRCLK
GPIO6 = AUD_TX
GPIO7 = AUD_RX

ESP32-S3 owns BCLK/LRCLK for the synchronized AudioPicture host audio domain.

AUD_TX distributes far-end/program audio as required by TAS5825M/XVF3800 routing.
AUD_RX receives processed XVF3800 microphone audio.

Exact use of I2S0/I2S1, TDM slots and DMA buffers is a firmware freeze item.

## 11. Amplifier
GPIO1 = AMP_FAULT input.
GPIO2 = AMP_PDN output.

AMP_PDN must have a hardware pull state that keeps TAS5825M disabled/muted while ESP32 is reset or unpowered.

## 12. Privacy / voice
GPIO21 = MIC_HW_EN.

Hardware default: microphones OFF while MCU is reset/unpowered.

VOICE:
- VOICE_RST and VOICE_IRQ require final GPIO assignment during pin-budget freeze if not implemented through an I/O expander/control device.

Privacy behavior must not depend solely on firmware.

## 13. Service / UI
GPIO40 = STATUS_LED.
GPIO41 = SERVICE_TOUCH / hidden pairing-reset input.
GPIO43 = UART_TX.
GPIO44 = UART_RX.

GPIO38, GPIO39, GPIO42 remain expansion/service candidates.

Hidden service control:
- ~3 s provisioning/pairing action;
- ~10 s factory reset action;
- implementation may use capacitive touch or sealed hidden switch after mechanical validation.

## 14. Status LED
STATUS_LED is hidden behind the product structure.

Functions:
- boot
- provisioning
- Assist/listening state
- microphone privacy/mute indication
- error/service.

Optical leakage toward OPT3004 must be prevented mechanically.

Exact LED/driver topology remains VALIDATE_MECHANICAL_OPTICAL.

## 15. UART
GPIO43 TX
GPIO44 RX

Factory/debug UART exposed only on internal pogo/test pads.

No external consumer UART connector.

## 16. Antenna keep-out
If ESP32-S3-WROOM-1 PCB-antenna version is used:
- module antenna must be placed at a MAIN PCB edge;
- no copper/ground/components beneath or immediately around antenna keep-out according to Espressif land-pattern/layout guidance;
- keep away from RJ45 magnetics, PoE module, Class-D LC inductors, large metal brackets and DML exciter structures;
- enclosure plastic/fabric is preferred in front of antenna.

Final RF placement requires enclosure-level Wi-Fi/BLE validation.

## 17. Reset / boot factory access
Factory pogo signals:
- GND
- +3V3_SYS
- CHIP_PU / RESET
- GPIO0 / BOOT
- UART_TX
- UART_RX
- USB D+
- USB D- optional if fixture supports it.

Normal product recovery uses USB-C plus controlled reset/boot procedure.

## 18. Watchdog / recovery
Firmware requirements:
- task watchdog;
- hardware watchdog;
- brownout detection;
- dual OTA partitions;
- rollback;
- recovery image/USB flashing path.

Hardware must permit recovery even if application firmware is invalid.

## 19. GPIO freeze table
| GPIO | Rev.A assignment |
|---|---|
| 0 | BOOT/service |
| 1 | AMP_FAULT |
| 2 | AMP_PDN |
| 3 | reserved strap |
| 4 | AUD_BCLK |
| 5 | AUD_LRCLK |
| 6 | AUD_TX |
| 7 | AUD_RX |
| 8 | ETH_RST |
| 9 | ETH_INT |
| 10 | ETH_CS |
| 11 | ETH_MOSI |
| 12 | ETH_SCLK |
| 13 | ETH_MISO |
| 14 | RADAR_CS |
| 15 | RADAR_IRQ |
| 16 | RADAR_RST/EN |
| 17 | I2C_SDA |
| 18 | I2C_SCL |
| 19 | USB D- |
| 20 | USB D+ |
| 21 | MIC_HW_EN |
| 26..37 | reserved memory |
| 38 | expansion candidate |
| 39 | expansion IRQ candidate |
| 40 | STATUS_LED |
| 41 | SERVICE_TOUCH |
| 42 | expansion candidate |
| 43 | UART_TX |
| 44 | UART_RX |
| 45 | reserved strap |
| 46 | reserved strap |

Unlisted pins remain uncommitted until final pin-budget review.

## 20. Important unresolved pin-budget item
The previous conceptual architecture named separate RADAR_SCLK/MOSI/MISO and VOICE_RST/VOICE_IRQ but did not assign safe ESP32 GPIOs for all of them.

This is now explicitly a release gate.

Preferred solutions in order:
1. verify unused safe GPIO availability on the exact WROOM-1-N16R8 module and allocate them;
2. share W5500 SPI bus with radar using separate CS if electrical/firmware timing is acceptable;
3. move low-speed reset/IRQ/control functions to a small I2C GPIO expander if needed.

Do NOT consume strapping or memory pins merely to preserve the earlier conceptual map.

## 21. Factory test
1. 3.3 V rail/current.
2. CHIP_PU reset timing.
3. BOOT strap/recovery.
4. USB enumeration.
5. UART.
6. flash/PSRAM self-test.
7. Wi-Fi RF test.
8. BLE provisioning test.
9. I2C scan.
10. W5500 SPI.
11. I2S clocks/loopback.
12. GPIO safe-state test during reset.
13. microphone privacy default-OFF test.
14. watchdog/recovery.

## 22. Release gates
Sheet 04 becomes FROZEN only after:
1. exact Espressif reference reset/decoupling network transcribed;
2. final pin-budget table including radar and voice controls;
3. strapping review;
4. USB ESD/CC interface review with Sheet 06;
5. antenna keep-out placed on PCB floorplan;
6. TPS62823 transient test with Wi-Fi burst;
7. RF coexistence test;
8. recovery/OTA rollback test.
