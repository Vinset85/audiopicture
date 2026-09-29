# PCB-D ENV — SHT45 + OPT3004 Rev.A

Status: **implementable architecture baseline**. Mechanical air-channel geometry and fabric optical calibration remain subject to final enclosure validation.

## 1. Purpose
PCB-D measures actual room environment while being hidden behind the AudioPicture front/rear structure:
- room temperature;
- relative humidity;
- ambient illuminance.

The board must be physically and thermally isolated from MAIN, amplifier, PoE/DC-DC converters and ESP32 heat.

## 2. Temperature / humidity
U301: **Sensirion SHT45-AD1F**.

Key implementation:
- supply: +3V3_SYS
- interface: I2C
- integrated PTFE membrane variant retained for dust/splash robustness;
- no conformal coating over the sensing opening.

The sensor shall be placed at the edge of PCB-D nearest the passive room-air chamber, with minimum surrounding copper and no local heat-generating components.

## 3. Ambient light
U302: **TI OPT3004DNPR**.

Key implementation:
- supply: +3V3_SYS
- interface: I2C
- sensor optical aperture faces the room through the printed acoustic fabric;
- no status LED or internal light source may directly illuminate the sensor.

The optical path shall include a controlled dark baffle to reduce lateral light contamination from internal LEDs.

## 4. I2C
Shared system bus:
- I2C_SDA
- I2C_SCL

SHT45 default 7-bit address: 0x44.
OPT3004 address is hardware-selectable through ADDR and shall be strapped to a non-conflicting fixed address for production.

Do not add redundant strong pull-ups on every daughterboard. MAIN owns the primary bus pull-up network. PCB-D may provide DNP footprints for debug/tuning.

Provide small series-resistor footprints on SDA/SCL if EMC tuning becomes necessary.

## 5. Power
J301 supplies:
- +3V3_SYS
- GND.

Local bypass:
- 100 nF X7R directly at each sensor supply;
- optional 1 uF local bulk near connector.

No switching regulator on PCB-D.

To minimize self-heating, firmware must use periodic/low-duty-cycle SHT45 measurements rather than continuous high-rate conversion.

## 6. FPC J301
8-pin baseline:
1 +3V3_SYS
2 +3V3_SYS
3 GND
4 GND
5 I2C_SDA
6 I2C_SCL
7 ENV_INT / reserved
8 BOARD_ID

BOARD_ID is resistor-coded so firmware can identify PCB-D hardware revision.

ENV_INT remains reserved because SHT45 does not require an interrupt for normal operation; it may be used by a future environmental sensor revision.

## 7. Thermal chamber
SHT45 must not sample the main electronics cavity.

Mechanical stack:
room air
-> hidden inlet microchannels
-> thermally isolated passive sensing chamber
-> SHT45 membrane
-> hidden outlet microchannels.

Rules:
- chamber located near a lower/side outer edge;
- use at least two separated openings to encourage passive exchange;
- prevent direct line-of-sight dust ingress where practical;
- avoid airflow directly from warm MAIN cavity;
- minimize thermal conduction through screws, large copper areas and frame ribs;
- FPC is the preferred electrical/thermal connection to MAIN.

Exact inlet/outlet geometry is a mechanical VALIDATE item.

## 8. Thermal compensation
Firmware exposes:
- T_room from SHT45;
- RH_room from SHT45;
- T_internal from a separate MAIN temperature measurement.

Factory characterization may derive:
T_room_corrected = T_SHT45 + offset(static or model-based)

Any compensation model must be measured in the final enclosure. Do not hide raw diagnostic values during engineering.

## 9. Lux behind fabric
OPT3004 measures through the printed acoustic fabric.

Production calibration stores a fabric/front-stack coefficient:
Lux_room = Lux_sensor * K_fabric

A single scalar K_fabric is the baseline. If printed artwork causes strong non-linearity/spectral dependence, a piecewise calibration may replace it.

Calibration procedure:
1. reference lux meter at product plane;
2. product front fabric installed;
3. multiple illumination levels and representative color temperatures;
4. fit K_fabric;
5. store profile by fabric/artwork family where necessary.

## 10. Optical mechanics
- create a small black/dark optical tunnel between OPT3004 and fabric;
- prevent light leaks from status/privacy LEDs;
- do not place translucent white structural plastic directly around the aperture if it can pipe internal light;
- keep sensor aperture free from adhesive;
- maintain repeatable fabric-to-sensor distance.

No visible hole is required in the artwork.

## 11. Sampling
Baseline:
- SHT45: adaptive periodic sampling, normally every 15–60 s;
- OPT3004: periodic/continuous conversion as required for responsive lighting automation.

Avoid unnecessarily high SHT45 sampling rates because room temperature/humidity change slowly and self-heating/traffic provide no benefit.

## 12. Home Assistant
Entities:
- sensor room_temperature
- sensor humidity
- sensor illuminance

Diagnostics:
- raw temperature during engineering/service mode
- raw lux
- ENV board revision
- sensor communication/status.

Normal user UI should expose corrected room values, not engineering calibration details.

## 13. Factory test
1. +3V3 rail.
2. BOARD_ID.
3. I2C scan/identity.
4. SHT45 CRC-valid measurement.
5. temperature sanity.
6. RH sanity.
7. OPT3004 dark/light response.
8. LED light-leak test.
9. write environmental calibration coefficients.

## 14. Release gates
ENV becomes FROZEN only after:
1. final PCB-D placement in enclosure;
2. passive chamber CFD/basic thermal validation;
3. warm-electronics soak test;
4. SHT45 offset characterization;
5. fabric lux calibration;
6. internal LED leakage test;
7. condensation/dust/mechanical review;
8. I2C EMC test with Class-D, Ethernet and radar active.


## Rev.A electrical capture review — 2026-09-29

### SHT45 electrical baseline
U301 = **Sensirion SHT45-AD1F**.
- supply = +3V3_SYS;
- fixed 7-bit I2C address = 0x44;
- local 100 nF ceramic bypass directly at VDD/GND;
- PTFE membrane/sensing opening remains completely free of coating, adhesive and enclosure contact.

Status: **FROZEN_DEVICE / MANUFACTURER_LAND_PATTERN**.

### OPT3004 address requirement
U302 = **Texas Instruments OPT3004DNPR**.

Do **not** strap OPT3004 ADDR to a state that resolves to I2C address 0x44 because SHT45 already owns 0x44 on the same bus.

The exact ADDR strap is **OPEN_DATASHEET_TABLE_CONFIRMATION** and must be selected from the TI address table to a fixed non-conflicting production address before native capture release.

### I2C ownership
MAIN is the sole populated owner of SDA/SCL pull-ups (4.7 kOhm baseline).
PCB-D:
- no populated parallel pull-ups by default;
- may provide DNP footprints only;
- may provide optional small series-resistor footprints at the FPC branch for EMC tuning;
- must remain functional at 100 kHz;
- 400 kHz operation is permitted only after complete system/FPC rise-time validation.

### ENV_INT
Rev.A does not require an interrupt for SHT45.
OPT3004 interrupt capability is optional.

J301 pin 7 ENV_INT remains **RESERVED/DNP** unless the final firmware architecture demonstrates a need for hardware threshold interrupts. Do not consume a MAIN GPIO merely because the OPT3004 exposes an interrupt output.

### BOARD_ID
J301 pin 8 BOARD_ID remains reserved for hardware revision identification, but Rev.A shall not require an additional MAIN ADC GPIO unless one is explicitly allocated.

Preferred implementation hierarchy:
1. identify PCB-D revision in firmware from known sensor/device combination where sufficient;
2. if a physical BOARD_ID is required, allocate a reviewed ADC-capable MAIN input and resistor coding;
3. otherwise leave BOARD_ID reserved/DNP.

Do not invent a resistor value or connect BOARD_ID to an unallocated ESP32 pin during native capture.

### Local power
No regulator on PCB-D.
Use:
- 100 nF X7R at SHT45;
- 100 nF X7R at OPT3004;
- optional 1 uF X7R local bulk near J301.

Avoid unnecessary ferrites that could create DC drop or thermal gradients. Any FPC-branch ferrite/0R option belongs at the MAIN/interface side and is a tuning feature, not required sensor circuitry.

### Thermal-layout rule
SHT45 placement is a PCB-layout constraint, not merely an enclosure note:
- sensor at a board edge/tab nearest the passive air chamber;
- minimum copper around the sensor except required pads/traces;
- no ground/power pour directly used as a thermal bridge from connector/OPT3004 region into the SHT45 island;
- thin neck/tab or slots may be used after mechanical-strength review;
- keep OPT3004 and any FPC connector thermal mass away from the immediate SHT45 sensing island.

Do not create a separate electrical ground island; thermal isolation is achieved geometrically while maintaining valid signal return.

### Optical-layout rule
OPT3004 optical aperture must have:
- manufacturer keep-out respected;
- no silkscreen, solder mask obstruction, adhesive or conformal coating over the optical path;
- no status/privacy LED line-of-sight;
- dark mechanical baffle/tunnel aligned in mechanical CAD.

Exact fabric-to-sensor distance is a mechanical calibration parameter.


## OPT3004 production address freeze — 2026-09-29

U302 OPT3004 must not use 0x44 because U301 SHT45 already occupies fixed address 0x44.

Production capture requirement:
- strap OPT3004 ADDR to a TI-datasheet-defined non-0x44 address;
- preferred target = **0x45**, subject to exact ADDR-to-rail connection confirmation during symbol pin-table audit;
- ADDR must never float;
- firmware shall treat SHT45=0x44 and OPT3004=0x45 as the Rev.A target map.

Status: **TARGET_ADDRESS_FROZEN / PHYSICAL_STRAP_CONNECTION_VERIFY_FROM_TI_PIN_TABLE**.

The distinction is deliberate: the bus address is frozen, but the schematic shall not guess whether the ADDR pin reaches that address via GND, VDD, SDA or SCL until the exact OPT3004 datasheet address table is transcribed into the native-capture review.


## Rev.A thermal and optical mechanical contract — 2026-09-29
### SHT45 chamber
The SHT45-AD1F sensing tab shall communicate with room air through two separated hidden openings. The chamber is isolated from the warm electronics cavity but is not hermetically sealed. Use a thin PCB neck and/or routed slots around the sensor tab to reduce conduction while preserving common electrical ground. No copper pour shall form a broad thermal bridge from J301/OPT3004 to the SHT45 tab. Place the membrane in free air volume with no adhesive or wall contact.
Mechanical CFD/thermal model shall include MAIN/DML heat sources, wall mounting orientation and passive natural convection. Calibration is performed only after the final enclosure/front stack is installed.

### OPT3004 dark tunnel
Create a matte-black, non-light-piping optical tunnel from the OPT3004 aperture to the back of the printed acoustic fabric. The tunnel shall prevent line-of-sight from internal LEDs and minimize lateral illumination. Keep the sensor/fabric spacing mechanically repeatable. Do not freeze a universal K_fabric: characterize the final fabric, print/ink and tunnel at multiple illuminance levels and representative color temperatures; store calibration by front-artwork family when required.

Status: **ENV_ELECTRICAL_CAPTURE_READY / THERMAL_CFD_AND_OPTICAL_CALIBRATION_RELEASE_GATES_REMAIN**.
