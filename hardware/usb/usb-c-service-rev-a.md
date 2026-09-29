# Sheet 06 — USB-C Service / Recovery Rev.A

Status: **implementable schematic specification**. Exact connector and ESD MPNs remain subject to mechanical/availability validation.

## 1. Purpose
USB-C is a service/recovery interface for:
- factory flashing;
- serial/JTAG/USB diagnostics as supported by ESP32-S3;
- firmware recovery when application firmware is invalid.

USB-C is NOT:
- the main product power input;
- a USB-PD sink for amplifier power;
- a normal requirement for Home Assistant provisioning.

## 2. USB role
AudioPicture is a **USB 2.0 device/UFP**.

No USB-PD controller is required.

Connector J6:
- USB Type-C receptacle
- USB 2.0 data
- VBUS
- CC1
- CC2
- GND
- shield.

SuperSpeed pins are absent or left unconnected depending on connector type.

## 3. CC resistors
CC1 -> **5.1 kOhm Rd** -> GND
CC2 -> **5.1 kOhm Rd** -> GND

Use 1% resistors.

These advertise a USB device/sink attachment. AudioPicture does not request PD voltages.

## 4. Data
ESP32-S3 native USB:
- GPIO19 = USB_D-
- GPIO20 = USB_D+.

For reversible Type-C USB2 connector:
- A6/B6 D+ pins joined at connector region;
- A7/B7 D- pins joined at connector region;
- then routed as one D+/D- differential pair to ESD and ESP32.

Keep branch/stub lengths from duplicated connector pins extremely short.

## 5. ESD
U_USB_ESD: low-capacitance USB 2.0 ESD protector.

Placement:
USB-C connector -> ESD -> ESP32.

Requirements:
- IEC 61000-4-2 class protection suitable for external connector;
- very low line capacitance;
- low dynamic resistance/clamp;
- package permitting short symmetric routing.

Exact Rev.A MPN: **Texas Instruments TPD2EUSB30ADRTR**.
- dual-channel USB 2.0 ESD protector;
- approximately 0.8 pF line capacitance;
- IEC 61000-4-2 contact/air ESD capability;
- DRL/DRT low-profile package option; Rev.A uses DRT where routing/fabrication permits.

Status: **FROZEN_DEVICE / PACKAGE_LAYOUT_VERIFY**.

Provide optional common-mode choke footprint only if EMC testing shows it is required. Default DNP to avoid unnecessary USB signal degradation.

## 6. Series resistors
Provide DNP/adjustable series resistor footprints in D+ and D- near the ESP32 if current Espressif hardware guideline/reference layout recommends them or SI tuning requires them.

Default value is determined from the exact ESP32-S3 reference design; do not arbitrarily populate 22 ohm.

## 7. VBUS / +5V_SERVICE
USB VBUS creates:
`+5V_SERVICE`.

+5V_SERVICE is used only for:
- VBUS detection;
- optional low-power service/recovery support if explicitly implemented;
- factory fixture sensing.

It must NOT directly connect to:
- +5V_SYS
- +24V_SYS
- TAS5825M
- DML/audio power path.

## 8. No backfeed
There shall be no uncontrolled path from +5V_SYS to USB VBUS and no uncontrolled path from USB VBUS to +5V_SYS.

Preferred Rev.A:
- treat VBUS primarily as a sensed input;
- normal USB recovery is performed while AudioPicture has PoE or external 24 V power.

Optional USB-powered MCU-only recovery may be added later only with an explicit power mux/load switch that isolates all high-power rails and meets ESP32 startup current.

Do not imply that a laptop USB port can power the complete product.

## 9. VBUS sense
ESP32/service logic may sense USB VBUS through a protected divider or dedicated detector.

Signal: USB_VBUS_PRESENT, GPIO assignment optional/service-only.

If no safe free GPIO remains, VBUS presence need not be exposed to application firmware; native USB attach behavior is sufficient for recovery.

The divider/detector must not phantom-power ESP32 when +3V3_SYS is absent.

## 10. Shield
USB connector shield net: CHASSIS_USB.

Do not blindly connect shield to digital ground at multiple uncontrolled points.

Provide configurable EMC connection near connector:
- direct/0R option;
- capacitor option;
- RC option as appropriate after enclosure EMC review.

Final chassis strategy must be coordinated with CHASSIS_ETH.

## 11. Recovery controls
USB recovery requires access to:
- CHIP_PU / RESET
- GPIO0 / BOOT.

Normal product:
- hidden service touch/control can initiate software recovery when firmware is alive.

Hard recovery:
- internal factory pogo pads;
- optional concealed mechanical sequence/access depending enclosure design.

A bricked application must remain recoverable without desoldering the ESP32 module.

## 12. USB boot / firmware
Production process:
1. assert BOOT strap as required;
2. reset;
3. ESP32 ROM USB download/recovery mode;
4. flash factory/recovery image;
5. verify flash/PSRAM;
6. reboot normal firmware.

OTA remains the normal field-update mechanism.

## 13. ESD / power protection
USB connector region shall include:
- data-line ESD;
- VBUS transient/ESD protection if required by selected protector architecture;
- short discharge path to the intended chassis/ground reference.

Do not route ESD current through ESP32 ground necks or sensitive INA228/microphone paths.

## 14. Layout
- J6 at rear/service-accessible edge.
- ESD device immediately behind connector.
- D+/D- routed over continuous reference plane.
- maintain USB 90-ohm differential target according to board stackup/fabricator rules.
- avoid vias where practical.
- no switching node or Class-D trace near USB pair.
- keep CC resistors close to connector.
- shield stitching/chassis treatment localized.

## 15. Mechanical
Connector must survive repeated service insertions without loading the PCB solder joints excessively.

Preferred:
- mid-mount or reinforced SMT/through-hole shield tabs;
- enclosure mechanically supports cable insertion forces.

Preferred connector remains **GCT USB4085** family, USB 2.0 Type-C receptacle with reinforced shell.
Status: **PREFERRED_CANDIDATE / MECHANICAL_DRAWING_AND_EXACT_VARIANT_VERIFY**.
Do not freeze footprint from a distributor drawing; transcribe the exact GCT manufacturer drawing only after the enclosure/PCB mounting style is selected.

## 16. Factory test
1. CC attach detection.
2. VBUS presence.
3. USB enumeration.
4. ROM download mode.
5. firmware flash.
6. reset/boot sequence.
7. verify no +5V_SYS backfeed to host.
8. verify USB host cannot energize amplifier/DML.
9. ESD pre-compliance.
10. repeated insertion mechanical test.

## 17. Release gates
Sheet 06 becomes FROZEN only after:
1. exact USB-C receptacle MPN;
2. exact low-capacitance ESD MPN;
3. Espressif D+/D- reference network verified;
4. USB stackup/90-ohm routing calculation;
5. shield/chassis strategy coordinated with Ethernet;
6. hard recovery procedure demonstrated;
7. backfeed test in all power combinations;
8. USB ESD test.


## USB electrical freeze review — 2026-09-29

### Power architecture
Rev.A USB is **data/service only with respect to product power**.

VBUS from the host creates +5V_SERVICE solely for:
- attachment/VBUS detection;
- ESD/transient handling;
- optional factory sensing.

There is **no power-path connection** from +5V_SERVICE to +5V_SYS or +3V3_SYS in Rev.A.

Therefore:
- AudioPicture must be powered by PoE or external 24 V during USB recovery;
- host USB cannot energize W5500, voice, radar, TAS5825M or DML;
- no ideal-diode/power-mux is required on Sheet 06.

This is now **FROZEN_ARCHITECTURE**.

### CC network
- CC1 -> 5.1 kOhm 1% -> GND
- CC2 -> 5.1 kOhm 1% -> GND

Status: **FROZEN_VALUES**.

### USB data ESD
U_USB_ESD = **TPD2EUSB30ADRTR**.
Place directly behind the receptacle before the pair traverses the PCB.

Status: **FROZEN_MPN / FOOTPRINT_VERIFY_TI_LAND_PATTERN**.

### ESP32 data interface
- USB_D- = GPIO19
- USB_D+ = GPIO20
- no external pull-up/pull-down on D+/D-;
- D+/D- series footprints remain optional/DNP until Espressif SI/reference-layout review;
- no common-mode choke populated by default.

### VBUS presence
Do not consume another general-purpose ESP32 GPIO merely for application-level VBUS indication in Rev.A.

USB recovery/attach uses the ESP32 native USB behavior while the system is already powered.

Provide a high-impedance **USB_VBUS_TEST** divider/test node for factory measurement, but do not connect it to +3V3_SYS and do not permit phantom powering through an MCU protection diode.

If future USB-device firmware requires explicit VBUS sensing, add a dedicated high-impedance detector in a controlled revision rather than improvising a direct GPIO divider.

### Shield/chassis
J_USB shield = **CHASSIS_USB**.
Reserve configurable local coupling to GND_SYS:
- 0 ohm option DNP;
- capacitor option DNP;
- RC/EMI option DNP.

Populate only after whole-product EMC strategy is coordinated with CHASSIS_ETH.

### Hard recovery
Hardware recovery remains independent of application firmware:
- USB D+/D- available;
- GPIO0 BOOT available at factory pogo;
- CHIP_PU RESET available at factory pogo.

A software-only hidden touch sequence is convenience, not the sole recovery mechanism.

### Sheet-06 capture status
Status: **READY_FOR_NATIVE_KICAD_CAPTURE_WITH_CONNECTOR_MECHANICAL_GATE**.

Production release remains blocked by:
1. exact USB4085 variant/manufacturer footprint;
2. TI ESD land-pattern verification during native capture;
3. 90-ohm differential routing against final stackup;
4. CHASSIS_USB/CHASSIS_ETH EMC decision;
5. USB ROM-download/recovery validation;
6. ESD and backfeed compliance tests.
