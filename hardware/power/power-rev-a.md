# POWER Rev.A — Electrical Design Specification

Status: **engineering baseline**. This document defines the first implementable power schematic. Items marked VALIDATE must pass schematic/layout/thermal validation before Gerber release.

## 1. Power sources

### PoE+
J1 Ethernet/PoE -> Silvertel Ag5324 -> `+24V_POE`.

The Ag5324 secondary output belongs to `GND_SYS`. Ethernet/PoE primary-side isolation boundaries must follow the module and MagJack manufacturer requirements.

### External DC
Target input: **24 VDC nominal, 3 A recommended**.

`J2 -> F101 -> transient/reverse protection -> +24V_EXT`.

J2 must be locking/keyed. Final connector MPN remains VALIDATE pending mechanical rear-bay design.

## 2. Source ORing

Two LM74700-Q1 controllers are retained:
- U4: `+24V_POE -> +24V_RAW`
- U5: `+24V_EXT -> +24V_RAW`

Controller orderable baseline: **LM74700QDBVRQ1**.

External N-MOSFET baseline for each branch: **DMT6007LFG** or electrically equivalent 60 V MOSFET. TI uses this device as a design example with LM74700-class circuitry. Final footprint/availability and thermal performance remain **VALIDATE**.

Design target for each ORing MOSFET:
- VDS >= 60 V
- VGS rating >= ±20 V preferred
- low RDS(on), target ~6.5–10 mOhm
- ID comfortably above 3 A continuous
- thermal copper sized from actual package.

LM74700 local components:
- VCAP capacitor: **>=0.1 uF**, and >=10 x MOSFET CISS expressed in uF; final value after MOSFET freeze.
- CIN local: >=22 nF
- COUT local: >=100 nF
- EN network: source-enabled by default, with provision for controller/test override.

### Source priority
Rev.A requirement: when both sources exist, external DC is preferred. Pure ideal-diode ORing alone does not guarantee deterministic preference when source voltages are nearly equal. Therefore U4 PoE EN shall be controllable by a hardware/MCU priority circuit. Boot-safe default must not create backfeed.

This priority circuit remains **VALIDATE** and must work before ESP32 firmware is running.

## 3. External-input transient protection

Baseline TVS candidate: **SMBJ33A**, 33 V standoff / 600 W class.

Status: **VALIDATE**. Its maximum clamp must be checked against every downstream absolute maximum and expected external-adapter transient profile. It is not frozen merely because nominal input is 24 V.

F101: resettable or replaceable fuse sized for 3 A normal operation and startup/inrush; final technology and MPN VALIDATE.

## 4. Main power measurement

`+24V_RAW -> RSH1 -> +24V_SYS`

U6: **INA228AIDGSR**.

RSH1 target:
- **10 mOhm**
- true 4-terminal/Kelvin construction
- >=0.5 W
- <=1%, preferably 0.5%
- candidate family: Vishay **WSK2512**, exact 10 mOhm orderable MPN to verify.

At 3 A:
- shunt drop = 30 mV
- dissipation = 90 mW

This allows use of INA228's ±40.96 mV high-sensitivity shunt range for the 3 A design target. Firmware must switch/configure range intentionally.

Kelvin sense traces from RSH1 to INA228 must not carry load current.

Signals:
- `I2C_SDA`
- `I2C_SCL`
- `POWER_ALERT`

## 5. 24 V system bus

`+24V_SYS` feeds:
- TAS5825M audio power stage
- TPSM63603 24-to-5 V module
- reserved expansion only where explicitly permitted.

Audio bulk capacitance baseline: 470–1000 uF low-ESR plus local ceramics. Exact value remains VALIDATE against amplifier transient load, PoE startup/hold-up and enclosure height.

## 6. 24 V -> 5 V

U7: **TPSM63603V5RDHR**.

Rev.A input capacitors follow TI minimum:
- C701/C702: 4.7 uF, 50 V, X7R/X7S, 1206 minimum baseline
- candidate: TDK C3216X7R1H475K160AC or Murata GRM31CR71H475KA12L.

Output baseline:
- minimum effective capacitance per TI stability requirement;
- initial population: 2 x 10 uF, 16 V X7R plus 100 nF local bypass;
- final effective capacitance checked including DC-bias derating.

Net: `+5V_SYS`.

Layout: reproduce TI recommended high-current loop and ground geometry as closely as the board partition permits.

## 7. 5 V -> 3.3 V

U8 is now selected as **TPS62823DLCR**:
- 2.4–5.5 V input
- up to 3 A
- 1% regulation family
- VSON-HR DLC-8
- nominal switching frequency ~2.2 MHz.

Target: `+5V_SYS -> +3V3_SYS`, 3.3 V.

Baseline inductor: **470 nH**, saturation/current rating selected for TPS62823 3 A operation. Exact MPN and output capacitor network remain VALIDATE against TI's 3.3 V design equations/reference circuit.

The 3 A choice intentionally provides transient margin for ESP32-S3, W5500 and digital peripherals.

## 8. Radar rails

Important: BGT60TR13C is not a single-rail 1.8 V load. Its datasheet includes multiple 1.8 V domains **and VDDLF at 3.3 V**.

PCB-C therefore receives both:
- `+3V3_SYS`
- a locally generated low-noise `+1V8_RADAR`

Exact LDO and domain filtering remain VALIDATE against Infineon reference layout.

## 9. USB-C service power

USB-C VBUS creates `+5V_SERVICE`.

Service power may boot/program logic through a controlled power mux/load switch but **must not energize the TAS5825M 24 V power stage**.

No uncontrolled backfeed is allowed from `+5V_SERVICE` into `+5V_SYS`.

## 10. Source/status signals

Required:
- `POE_PRESENT`
- `EXT_PRESENT`
- `POWER_ALERT`
- `5V_PG`
- `3V3_PG`

Presence detection dividers/comparators must be safe with ESP32 unpowered and shall not phantom-power the MCU through GPIO protection structures.

## 11. PCB constraints

- MAIN target: 4 layers.
- L2: continuous solid ground plane.
- Do not split ground under high-speed digital buses.
- Keep switch nodes compact and away from microphone/radar interconnects.
- Separate high-current amplifier return geometry from sensitive measurement routing by placement/return-path control, not arbitrary ground-plane cuts.
- Kelvin route RSH1.
- Put TPSM63603 input ceramics directly at the module pins.
- Put source protection and TVS physically at the relevant connector/input.
- Keep PoE isolation/creepage boundary explicit in schematic and PCB.

## 12. Validation gates before FROZEN electrical release

1. Ag5324 startup and hold-up with selected downstream bulk capacitance.
2. Dual-source handover with no backfeed.
3. External-source priority before MCU boot.
4. LM74700 MOSFET SOA/thermal and light-load behavior.
5. TVS clamp vs all absolute maximum ratings.
6. TPSM63603 effective CIN/COUT under DC bias.
7. TPS62823 3.3 V transient response with ESP32/W5500 load steps.
8. INA228 accuracy and calibration with final Kelvin shunt.
9. PoE ECO limiter power budget.
10. Full-board conducted/radiated EMI pre-compliance.
