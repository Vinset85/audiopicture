# PCB-C RADAR — BGT60TR13C Rev.A

Status: **implementable architecture baseline**. RF layout, oscillator, regulator and level-shifter MPNs remain subject to Infineon reference-design validation before Gerber release.

## 1. Radar sensor
U201: **Infineon BGT60TR13C**, PG-VF2BGA40-1, integrated antenna-in-package.

Target function:
- human presence;
- micro-motion / stationary-person detection;
- optional distance/occupancy-confidence features as supported by firmware;
- privacy-preserving room occupancy sensing.

The sensor covers the 60 GHz band and provides 1 TX / 3 RX channels.

## 2. Supply domains
The BGT60TR13C has multiple supply pins.

1.8 V domains:
- VDDD
- VDDA
- VDDVCO
- VDDRF
- VDDPLL

3.3 V domain:
- VDDLF

VAREF is an output/reference node and requires the datasheet/reference-design bypass network.

Therefore PCB-C receives +3V3_SYS and generates a dedicated low-noise +1V8_RADAR locally.

Do not connect BGT60TR13C digital pins directly to 3.3 V ESP32 GPIO.

## 3. 1.8 V regulator
U202: dedicated low-noise 1.8 V regulator, exact MPN VALIDATE.

Requirements:
- input: +3V3_SYS
- output: +1V8_RADAR
- adequate transient current for radar acquisition
- low output noise
- stable with selected ceramic capacitors
- enable/control provision preferred
- local decoupling distributed per Infineon reference design.

The 1.8 V RF/analog and digital domains may require ferrite/RC segmentation exactly as prescribed by the reference design. Do not invent split-ground islands.

## 4. VDDLF 3.3 V
VDDLF is supplied from +3V3_SYS through the filtering/decoupling network derived from the Infineon reference design.

Power sequencing shall ensure no BGT60TR13C pin is driven outside its absolute maximum ratings when either rail is absent.

## 5. Host interface
BGT60TR13C uses standard SPI.

Radar-side logic domain: **1.8 V**.

Signals:
- SPI_SCLK
- SPI_MOSI
- SPI_MISO
- RADAR_CS
- RADAR_IRQ
- RADAR_RST

Target SPI rate: start conservatively during bring-up; production rate may increase after SI validation, within Infineon limits.

## 6. Level translation
A dedicated 3.3 V <-> 1.8 V translation stage is REQUIRED between ESP32-S3 and BGT60TR13C.

Direction groups:
3.3 V -> 1.8 V:
- SCLK
- MOSI
- CS
- RESET

1.8 V -> 3.3 V:
- MISO
- IRQ

Do not use auto-direction I2C-style translators on high-speed SPI.

Preferred architecture:
- fixed-direction translators/buffers;
- separate channel direction where practical;
- translator OE tied to a safe rail/power-good strategy so radar inputs are not driven before +1V8_RADAR is valid.

Exact MPN remains VALIDATE after propagation-delay/SPI-rate and power-off-protection review.

## 7. Clock
BGT60TR13C clock implementation is **OPEN_REFERENCE_RECONCILIATION**. Do not freeze 38.4 MHz or an ~80 MHz-class source until the selected Infineon BGT60TR13C reference schematic, datasheet OSC_CLK requirements and firmware clock configuration are reconciled.

U203 oscillator/crystal implementation: VALIDATE against Infineon embedded reference design.

Clock routing:
- very short;
- isolated from SPI and switching rails;
- controlled return path;
- no test stub on production RF clock unless reference design explicitly permits it.

## 8. FPC J201
Baseline 12-pin interface to MAIN:
1 +3V3_SYS
2 +3V3_SYS
3 GND
4 GND
5 RADAR_SCLK
6 RADAR_MOSI
7 RADAR_MISO
8 RADAR_CS
9 RADAR_IRQ
10 RADAR_RST
11 RADAR_EN
12 RESERVED

Level translation and +1V8_RADAR generation reside on PCB-C.

RADAR_EN controls local radar power/translator enable; exact implementation remains VALIDATE.

## 9. RF PCB and keep-out
BGT60TR13C antennas are integrated in the package. No external 60 GHz antenna is required.

PCB-C must follow Infineon package/reference-board stackup and RF keep-out guidance.

Rules:
- no metal, copper, ground pour, screws, magnets, shield cans or large conductive objects in the antenna radiation keep-out;
- do not place the sensor directly behind MAIN PCB;
- keep DML exciter metal structures outside the radar field/near-field region;
- front acoustic fabric and any plastic support in front of radar must be RF-characterized;
- avoid adhesive layers with unknown dielectric/loss properties in front of antenna;
- orient the sensor normal to the intended room coverage unless simulation/measurement supports another angle.

Exact radar X/Y position is NOT frozen.

## 10. Mechanical integration
PCB-C is a small dedicated board near the front plane, behind the fabric.

The front stack in the radar window should be as electromagnetically simple and repeatable as possible:
room -> printed acoustic fabric -> controlled plastic/air region -> BGT60TR13C antenna face.

Do not put the DML panel conductive skin in front of the radar window. If the DML construction includes conductive skins, a radar aperture/window must be designed.

## 11. Firmware interface
Radar Engine responsibilities:
- power-up/reset;
- SPI identity/self-test;
- register/config profile loading;
- FIFO acquisition;
- signal processing;
- presence/micro-motion state;
- diagnostics;
- calibration/noise-floor adaptation.

Home Assistant target entities:
- binary_sensor presence
- optional distance
- optional still_presence
- optional motion
- occupancy confidence diagnostic
- radar health/status.

Do not expose unstable experimental quantities as normal HA entities.

## 12. Factory test
1. +3V3_SYS / +1V8_RADAR rails.
2. reference clock.
3. level-shifter direction and power-off state.
4. SPI chip-ID/register access.
5. IRQ.
6. hardware reset.
7. raw radar frame acquisition.
8. target/motion sanity test.
9. stationary-person/micro-motion test.
10. interference test with Wi-Fi, Ethernet and Class-D audio active.

## 13. Release gates
RADAR becomes FROZEN only after:
1. exact Infineon embedded reference schematic captured;
2. U202 1.8 V regulator frozen;
3. level-shifter MPN frozen;
4. oscillator/reference-clock circuit frozen;
5. RF stackup and keep-out copied/validated;
6. fabric/front-stack attenuation measurement or simulation;
7. DML structure/radar interaction checked;
8. SPI SI test at production clock;
9. presence and stationary-person performance validated in final enclosure;
10. EMC/coexistence test.


## Rev.A radar electrical correction — 2026-09-29

### Shared SPI naming
PCB-C uses the MAIN shared host bus:
- SPI_SCLK
- SPI_MOSI
- SPI_MISO
- RADAR_CS

There are no separate RADAR_SCLK/RADAR_MOSI/RADAR_MISO MAIN nets in Rev.A.

### Reference clock correction
The previous "~80 MHz class" placeholder is **SUPERSEDED**.
**Do not freeze either 38.4 MHz or ~80 MHz yet.** The clock is now an explicit reference-reconciliation gate. Exact frequency, source topology, oscillator MPN, drive level and firmware setting must be taken as one coherent set from the selected current Infineon BGT60TR13C hardware/firmware reference.

### J201 frozen interface
J201 remains 12 contacts:
1 +3V3_SYS
2 +3V3_SYS
3 GND
4 GND
5 SPI_SCLK
6 SPI_MOSI
7 SPI_MISO
8 RADAR_CS
9 RADAR_IRQ
10 RADAR_RST
11 RADAR_EN
12 RESERVED

Independent controls:
- RADAR_EN = ESP32 GPIO16
- RADAR_RST = ESP32 GPIO42

PCB-C owns the 1.8 V rail, fixed-direction translation and radar clock.


## 1.8 V power / translation design review — 2026-09-29

### Radar current and rail performance
Infineon specifies approximately 200 mA-class active current for BGT60TR13C. Current Infineon 60 GHz FMCW schematic guidance requires the radar supply to be treated as a low-noise transient-sensitive rail, including fast load-step response and adequate local energy storage.

Design +1V8_RADAR for **>=300 mA continuous engineering allocation** and substantially higher regulator current capability/margin. Do not size the regulator from digital-domain current alone.

### U202 preferred baseline
Preferred +1V8_RADAR regulator family: **onsemi NCP167**, 1.8 V fixed-output variant, subject to exact orderable suffix/package verification.

Rationale:
- NCP167 is explicitly listed by Infineon among tested/recommended LDO families for 60 GHz radar supply design;
- current capability up to the 700 mA class provides useful transient margin above the BGT60TR13C active-current envelope;
- appropriate low-noise/high-PSRR class for the radar application.

Status: **PREFERRED_REFERENCE_VALIDATED_FAMILY / EXACT_1V8_MPN_PACKAGE_VERIFY**.

Before production freeze verify the exact 1.8 V ordering code, stability/output-capacitance requirements, PSRR/noise and thermal performance from +3V3_SYS under the final radar duty cycle.

### Supply filtering
Do not feed all BGT60TR13C 1.8 V pins from one undifferentiated long trace.

The Infineon shield/reference architecture uses per-domain low-pass/pi filtering because the radar is sensitive to supply noise/crosstalk.

Native capture shall provide reference-derived filtering/decoupling for:
- VDDD
- VDDA
- VDDVCO
- VDDRF
- VDDPLL
- oscillator supply where applicable

and the required VAREF bypass.

Exact filter values are **OPEN_REFERENCE_TRANSCRIPTION** from the current Infineon reference schematic. Do not create split ground islands.

### Level translation requirements
Radar digital I/O is referenced to VDDD = +1V8_RADAR.
Required fixed directions:
3.3 V -> 1.8 V:
- SPI_SCLK
- SPI_MOSI
- RADAR_CS
- RADAR_RST

1.8 V -> 3.3 V:
- SPI_MISO
- RADAR_IRQ

Translator requirements:
- explicit DIR/fixed-direction architecture, no auto-direction bus switch;
- adequate timing margin for production SPI rate;
- Ioff/power-off protection or equivalent isolation so MAIN cannot parasitically power an unpowered radar;
- OE or power-domain arrangement that leaves radar inputs inactive while +1V8_RADAR is absent;
- no bus contention on shared SPI_MISO.

Exact translator MPN remains **OPEN_POWER_OFF_TIMING_REVIEW**.

### SPI rate
BGT60TR13C datasheet specifies SPI timing up to 50 MHz under stated 1.8 V conditions.

AudioPicture policy:
- conservative low-speed initialization/bring-up;
- production clock selected only after translator + FPC + shared-bus SI validation;
- never assume 50 MHz simply because the sensor permits it.

### RADAR_EN behavior
RADAR_EN must control the local radar power/isolation state, not merely a firmware flag.

Required OFF state:
- +1V8_RADAR disabled or otherwise brought to the validated low-power state;
- 3.3->1.8 translator outputs high-impedance/inactive;
- 1.8->3.3 paths must not back-power either domain;
- RADAR_RST remains asserted according to the MAIN safe-state contract.

Enable sequence:
1. MAIN +3V3_SYS valid;
2. assert RADAR_RST;
3. enable +1V8_RADAR;
4. wait for rail/filter/clock settling;
5. enable translation;
6. release RADAR_RST;
7. initialize SPI at conservative rate;
8. configure radar profile/IRQ.

Disable sequence reverses control so digital drive is removed before the radar rail is allowed to collapse.


## Level translator freeze / clock reconciliation — 2026-09-29

### U204 translation baseline
U204 = **Texas Instruments SN74AXC4T245**.

Use dual rails:
- 3.3 V side = +3V3_SYS;
- 1.8 V side = +1V8_RADAR.

Use the two independently controlled 2-bit groups:
- group A: SPI_SCLK, SPI_MOSI, direction 3.3 V -> 1.8 V;
- group B: SPI_MISO, RADAR_IRQ, direction 1.8 V -> 3.3 V.

The remaining MAIN->RADAR controls RADAR_CS and RADAR_RST require a second fixed-direction translation element or an equivalent reviewed grouping; do not leave them at 3.3 V.

SN74AXC4T245 is selected because it provides:
- explicit direction control;
- output enable;
- partial-power-down Ioff;
- VCC isolation/high impedance when either supply is below the device isolation threshold;
- data-rate margin far above the BGT60TR13C SPI requirement.

Status: **FROZEN_TRANSLATOR_FAMILY / EXACT_PACKAGE_AND_SECOND_CONTROL_CHANNEL_IMPLEMENTATION_VERIFY**.

OE must default to the disabled/high-impedance state during power-up/down. Follow TI's recommended OE bias referenced to the controlling supply. Translation must not become active until +1V8_RADAR is valid.

### Clock status correction
The earlier 38.4 MHz statement is **NOT a production freeze**.

Clock status is now:
**OPEN_REFERENCE_RECONCILIATION**.

Before oscillator capture, reconcile as one set:
1. current BGT60TR13C datasheet OSC_CLK electrical/timing requirements;
2. current Infineon reference/shield schematic;
3. firmware clock/profile configuration;
4. exact oscillator/source frequency and MPN.

No 38.4 MHz or ~80 MHz oscillator may be released to BOM merely from an example or platform-level clock statement.


## Reference shield reconciliation — 2026-09-29

### Clock baseline resolved
Infineon BGT60TR13C Shield User Guide Rev. 2.50 (2025-02-04) shows the sensor OSC_CLK driven by an `OSC_80M` source. The BGT60TR13C datasheet describes OSC_CLK as an 80 MHz (example) crystal/clock input.

For AudioPicture Rev.A, which follows the Infineon Shield/reference topology, the capture baseline is therefore:
- OSC_CLK nominal = **80 MHz**;
- exact oscillator/source MPN and its supply/filter network = **OPEN_RDK_HARDWARE_TRANSCRIPTION**;
- firmware clock/profile settings must remain coherent with the selected 80 MHz reference.

The prior 38.4 MHz proposal is **SUPERSEDED / DO_NOT_USE**.

### U202
U202 family = **onsemi NCP167**, fixed 1.8 V output.
Manufacturer datasheet confirms:
- VIN 1.9..5.5 V;
- fixed-output options include 1.8 V;
- up to 700 mA;
- 1 uF ceramic input and 1 uF ceramic output nominal application;
- WLCSP4 and XDFN4 package families.

AudioPicture preference: choose the **XDFN4 1 mm x 1 mm** 1.8 V orderable variant if lifecycle/availability are acceptable, because it is more manufacturing-friendly than WLCSP for the custom board. Exact ordering code remains a BOM gate.

### Digital translation implementation
Use **two TI SN74AXC4T245 devices** rather than mixing translator families.

U204:
- group 1: SPI_SCLK + SPI_MOSI, 3.3 -> 1.8 V;
- group 2: SPI_MISO + RADAR_IRQ, 1.8 -> 3.3 V.

U205:
- group 1: RADAR_CS + RADAR_RST, 3.3 -> 1.8 V;
- group 2 unused and disabled/NC per TI requirements.

Rails:
- VCCA = +3V3_SYS;
- VCCB = +1V8_RADAR.

Configure DIR pins as fixed straps for the required direction. OE is active-low; each OE gets a pull-up to its controlling VCCA so translation defaults disabled/high-Z during power-up/down. RADAR_EN-controlled logic may pull OE low only after +1V8_RADAR is valid.

SN74AXC4T245 provides Ioff partial-power-down and VCC isolation; if either VCC is below 100 mV, outputs become high impedance. This is required for radar-off back-power prevention.

Status:
- U204/U205 family **FROZEN**;
- exact package preference = UQFN/WQFN/TSSOP selection at PCB assembly/fanout review;
- do not use auto-direction translators.

### Supply-noise release gate
BGT60TR13C datasheet specifies a stringent supply-noise condition, including a 20 uVpp limit in the 20 kHz..700 kHz band for the stated operating specification. Therefore the final NCP167 + domain-filter network must be verified by simulation/measurement against the Infineon reference network; generic decoupling alone is not a release criterion.

### Reference files authority
Infineon states that Shield schematics and PCB design files are distributed with the Radar Development Kit (RDK) under its hardware assets. The exact 80 MHz oscillator MPN and the per-domain filtering values shall be transcribed from that hardware package before BOM release.


## 80 MHz oscillator freeze — 2026-09-29
Rev.A reference oscillator = **Kyocera KC2016K80.0000C1GE00CT**, 80 MHz.

Infineon reference capture baseline:
- +1V8_RADAR -> ferrite -> oscillator VDD;
- 10 nF + 1 uF local supply bypass;
- oscillator OUT -> 150 ohm series -> OSC_80M / BGT60TR13C OSC_CLK.

The series resistor is explicitly a tuning point: phase-noise and Range-Doppler validation remain mandatory. Do not substitute 38.4 MHz.

Status: **FROZEN_REFERENCE_DEVICE / FILTER_MPN_AND_PHASE_NOISE_VALIDATE**.


## Supply-filter transcription freeze — 2026-09-29
Current Infineon reference hardware establishes the Rev.A capture baseline:
- VDDD: 1V8 -> 10 uF -> 600-ohm ferrite -> 1 uF local.
- VDDA: 1V8 -> 10 uF -> 600-ohm ferrite -> 1 uF local.
- VDDVCO: 1V8 -> 10 uF -> 600-ohm ferrite -> 1 uF local.
- VDDPLL: 1V8 -> 10 uF -> 600-ohm ferrite -> 1 uF local.
- VDDLF: 3V3 -> 10 uF -> 600-ohm ferrite -> 1 uF local.
- VDDRF: 1V8 -> 10 uF -> 600-ohm ferrite -> 10 uF + 3 x 1 uF local.
- VAREF is a 1.2 V sensor output/reference; do not drive it from 1V8/3V3.

Exact ferrite order code/impedance-vs-frequency curve and VAREF bypass value remain open. The complete rail network remains subject to the BGT60TR13C low-noise requirement and final PCB layout validation.

Status: **FILTER_TOPOLOGY_AND_CAP_VALUES_FROZEN_REFERENCE / FERRITE_MPN_VAREF_NOISE_VALIDATE**.
