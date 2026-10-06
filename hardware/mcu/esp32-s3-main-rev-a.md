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

## 9. Radar SPI — FROZEN Rev.A
Radar shares the host SPI clock/data lines with W5500:
- GPIO11 = SPI_MOSI
- GPIO12 = SPI_SCLK
- GPIO13 = SPI_MISO
- GPIO14 = RADAR_CS
- GPIO15 = RADAR_IRQ
- GPIO16 = RADAR_EN

W5500 retains GPIO10 ETH_CS.

Firmware performs per-device bus arbitration and reconfigures SPI frequency/mode as required before each transaction. PCB-C contains the radar 3.3 V <-> 1.8 V fixed-direction translation.

This avoids consuming strapping pins for the listed peripherals. Rev.EZ separately adds a status-input expander because the original map omitted power-status nets.

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
- GPIO38 = VOICE_RST
- GPIO39 = VOICE_IRQ.

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
| 16 | RADAR_EN |
| 17 | I2C_SDA |
| 18 | I2C_SCL |
| 19 | USB D- |
| 20 | USB D+ |
| 21 | MIC_HW_EN |
| 26..37 | reserved memory |
| 38 | VOICE_RST |
| 39 | VOICE_IRQ |
| 40 | STATUS_LED |
| 41 | SERVICE_TOUCH |
| 42 | RADAR_RST |
| 43 | UART_TX |
| 44 | UART_RX |
| 45 | reserved strap |
| 46 | reserved strap |

Unlisted pins remain uncommitted until final pin-budget review.

## 20. Pin-budget decision
Rev.EZ corrects the incomplete Rev.A pin-budget conclusion: power-status signals need U20 TCA9534PWR at 0x20. See `../kicad/main/power-status-inputs-rev-ez.md`; conditioning and hardware validation remain OPEN.

Shared SPI:
- GPIO11/12/13 = MOSI/SCLK/MISO
- GPIO10 = ETH_CS
- GPIO14 = RADAR_CS

Voice control:
- GPIO38 = VOICE_RST
- GPIO39 = VOICE_IRQ

GPIO42 = RADAR_RST, providing independent radar reset and enable control.

GPIO22..25 are not exposed for use on the WROOM-1 module, GPIO26..37 remain unavailable for module memory, and strapping GPIO0/3/45/46 remain protected.

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
2. final shared-SPI firmware arbitration and per-device clock/mode validation;
3. strapping review;
4. USB ESD/CC interface review with Sheet 06;
5. antenna keep-out placed on PCB floorplan;
6. TPS62823 transient test with Wi-Fi burst;
7. RF coexistence test;
8. recovery/OTA rollback test.


## Espressif pin/reset verification — 2026-09-29

- Strapping pins GPIO0/GPIO3/GPIO45/GPIO46 remain protected.
- GPIO19=USB_D- and GPIO20=USB_D+ are dedicated to service USB.
- GPIO26..37 remain unavailable for production peripherals on N16R8 memory configuration.
- GPIO39..42 are intentionally used despite their pad-JTAG alternate functions; production debug uses USB Serial/JTAG and UART0 instead.
- CHIP_PU RC is frozen at 10 kOhm pull-up to +3V3_SYS and 1 uF to GND, following Espressif guidance.
- Minimum 50 us rail-stabilization and reset-low timing requirements are respected with margin.
- GPIO38=VOICE_RST, GPIO39=VOICE_IRQ, GPIO42=RADAR_RST are committed, not expansion candidates.
- Shared SPI GPIO11/12/13 with independent GPIO10 ETH_CS and GPIO14 RADAR_CS remains valid through the GPIO matrix.
- USB-OTG and USB-Serial/JTAG share the internal PHY and are treated as mutually exclusive service modes.
- For self-powered USB operation, Sheet 06 must ensure valid VBUS-presence handling without back-powering +3V3_SYS.

Status: **GPIO_CONTRACT_VERIFIED / RESET_RC_FROZEN**.


## Hardware safe-state freeze — 2026-09-29

All safety-relevant enables/selects must have deterministic external bias while ESP32-S3 GPIOs are high-impedance during reset.

### Frozen pull network
- GPIO2 / AMP_PDN: **100 kOhm pull-down**. Amplifier hardware state = OFF/PDN during MCU reset.
- GPIO21 / MIC_HW_EN: **100 kOhm pull-down**. Microphone load switch = OFF during reset; privacy default is physical power removal.
- GPIO16 / RADAR_EN: **100 kOhm pull-down**. Radar local power/regulator enable = OFF during reset.
- GPIO42 / RADAR_RST: **10 kOhm pull-down**, interpreted at PCB-C so radar reset is asserted while host is unavailable.
- GPIO10 / ETH_CS: **10 kOhm pull-up to +3V3_SYS**, W5500 deselected.
- GPIO14 / RADAR_CS: **10 kOhm pull-up to +3V3_SYS**, radar deselected before/while its level translator becomes active.
- GPIO8 / ETH_RST: **10 kOhm pull-down**, W5500 held reset until firmware explicitly releases it.

### Input/status nets
- GPIO1 / AMP_FAULT: input; pull ownership belongs to TAS5825M/interface implementation, no duplicate strong MAIN pull.
- GPIO9 / ETH_INT: W5500 interrupt is active-low; provide a single 10 kOhm pull-up to +3V3_SYS if the W5500/reference implementation does not already own it.
- GPIO15 / RADAR_IRQ: input; pull ownership belongs to PCB-C translator/radar implementation.
- GPIO39 / VOICE_IRQ: input; pull ownership belongs to PCB-B.
- GPIO38 / VOICE_RST: **10 kOhm pull-down** on MAIN unless PCB-B reset interface already provides the guaranteed asserted default. Only one effective owner shall be populated.

### Boot sequencing
Firmware release order after +3V3_SYS valid:
1. keep AMP_PDN=0, MIC_HW_EN=0, RADAR_EN=0;
2. initialize GPIO directions and shared SPI with both CS high;
3. release ETH_RST and validate W5500;
4. power/enable radar, keep RADAR_RST asserted until PCB-C rails/translators settle, then release;
5. release VOICE_RST only after voice rails are valid;
6. MIC_HW_EN may assert only after privacy state and indicator path are initialized;
7. AMP_PDN may assert only after audio clocks/DSP state are valid and anti-pop sequence is ready.

### Failure behavior
Watchdog reset, brownout reset or firmware crash must naturally return the external pull network to the safe states above.

No safety-relevant enable may rely on ESP32 internal pulls alone.

### Strap isolation
None of these safe-state networks uses GPIO0/GPIO3/GPIO45/GPIO46, so the external bias network does not alter ESP32-S3 strapping.

Status: **SAFE_STATES_FROZEN_FOR_CAPTURE**.


## Final electrical capture gates — 2026-09-29

### ESP32-S3-WROOM-1 local supply network
Rev.A capture baseline:
- module 3V3 supply fed directly from +3V3_SYS with a short/wide low-impedance path;
- **10 uF X7R/X7S local bulk** at the module supply entrance;
- **100 nF X7R local high-frequency bypass** adjacent to the supply entry;
- no ferrite bead in series by default: avoid adding rail impedance during Wi-Fi current bursts unless RF/EMI testing demonstrates a need;
- TPS62823 output/bulk network remains the upstream source of transient energy.

Acceptance gate: +3V3_SYS at the module must remain inside Espressif operating limits during worst-case Wi-Fi/BLE burst plus concurrent Ethernet/radar activity.

### I2C pull-up freeze
MAIN owns the shared I2C pull-ups:
- SDA: **4.7 kOhm to +3V3_SYS**
- SCL: **4.7 kOhm to +3V3_SYS**
- one owner only; daughterboards shall not populate parallel pull-ups by default.

At 3.3 V the static low-state current is about 0.70 mA per asserted line.

For Standard/Fast-mode operation, total bus capacitance must remain within the I2C electrical timing budget. With 4.7 kOhm, use **400 pF as an absolute bus-capacitance ceiling only for Standard-mode analysis**; for 400 kHz operation the practical capacitance target is much lower and must be checked from measured/calculated rise time.

Rev.A firmware baseline:
- boot/discovery: 100 kHz permitted;
- normal target: 400 kHz only after bus rise-time validation across MAIN + FPC + PCB-B/C/D.

Provide SDA/SCL test points near the MAIN bus origin.

### Shared SPI source damping
Populate optional source-side damping footprints:
- GPIO12 / SPI_SCLK: **22 ohm default**
- GPIO11 / SPI_MOSI: **22 ohm default**
- GPIO10 / ETH_CS: **22 ohm default**
- GPIO14 / RADAR_CS: **22 ohm default**

MISO is driven by two different slaves and therefore does not receive a single MCU-source resistor. If SI requires damping, place device-side optional series footprints at each slave output instead.

All series resistors must be physically near the signal source they damp.

Rev.A status:
- 22 ohm = POPULATE_DEFAULT;
- tuning range = 0/22/33 ohm after SI validation.

Firmware must never assert ETH_CS and RADAR_CS simultaneously.

### Shared SPI frequency policy
Do not freeze one global SPI clock.
Firmware configures each transaction for the target slave:
- W5500 according to its validated SPI timing limit and board SI;
- BGT60TR13C according to radar/level-translator timing limits.

Boot starts at conservative clock rates; production firmware may raise each device rate only after hardware validation.

### Antenna implementation gate
For ESP32-S3-WROOM-1 PCB-antenna variant:
- place antenna end at a MAIN PCB edge;
- preferred geometry is antenna projecting beyond the host-board ground/copper boundary;
- no copper, ground, traces, components, screws, metal brackets or shielding inside the Espressif antenna keep-out volume;
- keep Class-D inductors, PoE magnetics/module and DML exciter metal as far as practical;
- do not place conductive DML skin directly over/behind the antenna field region.

The exact keep-out dimensions and module courtyard must be copied from the current Espressif recommended land pattern during native PCB capture, not redrawn from memory.

If enclosure/FEA/RF layout cannot provide a clean antenna zone, change to the WROOM-1U external-antenna variant before PCB release.

### Sheet-04 capture status
Electrical decisions now sufficient for native schematic capture:
- MCU module/version frozen;
- GPIO contract verified;
- memory pins protected;
- strapping pins protected;
- CHIP_PU RC frozen;
- safety pulls frozen;
- native USB pins frozen;
- I2C pull-ups frozen;
- shared SPI topology and source damping frozen;
- I2S pin ownership frozen;
- UART/debug strategy frozen.

Status: **READY_FOR_NATIVE_KICAD_CAPTURE_WITH_LAYOUT_RF_GATES**.

Production/Gerber release remains blocked by:
1. Espressif land-pattern/antenna keep-out transcription and visual audit;
2. enclosure-level Wi-Fi/BLE RF validation;
3. +3V3 transient validation under radio bursts;
4. shared-SPI SI validation including radar translator;
5. USB ESD/VBUS review with Sheet 06;
6. recovery/OTA/factory-mode validation.
