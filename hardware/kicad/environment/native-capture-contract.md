# PCB-D ENV Rev.A — Native KiCad Capture Contract

Status: **READY_FOR_NATIVE_KICAD_STRUCTURE_AND_CAPTURE_WITH_ADDRESS_STRAP_AUDIT**
Target: **KiCad 9.x**

Engineering authority: `hardware/environment/sht45-opt3004-rev-a.md`.

Native KiCad files must be generated/saved/validated by KiCad 9.x or validated automation. Do not hand-author pseudo .kicad_sch/.kicad_pcb files.

## 1. Functional blocks
1. J301 MAIN interface.
2. U301 SHT45 temperature/humidity sensor.
3. U302 OPT3004 ambient-light sensor.
4. local bypass/bulk.
5. optional I2C EMC tuning footprints.
6. thermal-isolation PCB geometry.
7. optical keep-out/tunnel interface.
8. factory test points.

## 2. J301
J301 = **Hirose FH12-8S-0.5SH(55)**, 8 contacts, 0.5 mm pitch, bottom-contact ZIF, horizontal insertion, 0.30 mm FPC:
1 +3V3_SYS
2 +3V3_SYS
3 GND
4 GND
5 I2C_SDA
6 I2C_SCL
7 ENV_INT / RESERVED
8 BOARD_ID / RESERVED

The connector MPN is frozen. Final mating-view orientation/pin-1 must still be cross-checked against the exact Hirose 2D drawing and selected FPC contact side before PCB release.

## 3. U301 SHT45
U301 = **Sensirion SHT45-AD1F**.
- VDD = +3V3_SYS
- GND = GND
- SDA = I2C_SDA
- SCL = I2C_SCL
- fixed 7-bit address = 0x44
- 100 nF X7R directly at VDD/GND
- manufacturer land pattern

PTFE membrane/opening must remain free from solder mask obstruction, coating, adhesive and mechanical contact.

## 4. U302 OPT3004
U302 = **Texas Instruments OPT3004DNPR**, DNP/USON package.
- supply = +3V3_SYS
- GND = GND
- SDA = I2C_SDA
- SCL = I2C_SCL
- local 100 nF X7R bypass
- target Rev.A address = **0x45**

Do not use address 0x44 because SHT45 already owns it.

The exact ADDR pin strap required to obtain 0x45 is an explicit **TI_DATASHEET_PIN_TABLE_AUDIT** gate. ADDR must not float.

Interrupt operation is not required in Rev.A. OPT3004 interrupt output is left uncommitted unless firmware requirements later justify ENV_INT.

## 5. I2C
MAIN is the sole populated owner of bus pull-ups, 4.7 kOhm baseline.

PCB-D:
- no populated SDA/SCL pull-ups;
- optional DNP pull-up footprints allowed for debug only;
- optional small series resistor footprints at the branch for EMC tuning;
- guaranteed functional target at 100 kHz;
- 400 kHz only after full FPC/bus capacitance and rise-time validation.

Rev.A address map:
- 0x44 SHT45
- 0x45 OPT3004 target

## 6. Power
No local regulator.
- +3V3_SYS from J301;
- 100 nF at each sensor;
- optional 1 uF X7R near J301;
- no unnecessary heat-generating devices.

PCB-D is not hot-plug user hardware.

## 7. BOARD_ID
J301 BOARD_ID is reserved.

Do not connect it to an arbitrary ESP32 pin in Rev.A.
If a physical board-ID network becomes mandatory, allocate a reviewed ADC-capable MAIN input and resistor coding in a coordinated MAIN/ENV revision.

Until then: RESERVED/DNP.

## 8. ENV_INT
J301 ENV_INT is RESERVED/DNP for Rev.A unless a reviewed requirement assigns it.

Do not consume a critical MAIN GPIO merely to expose an optional OPT3004 interrupt.

## 9. SHT45 thermal layout
SHT45 shall sit at the board edge/tab facing the passive air chamber.

Required:
- minimum practical copper near sensor;
- no heat source nearby;
- no broad copper thermal bridge from FPC/OPT3004 region;
- optional slots/thin neck around sensing tab after strength review;
- short low-mass signal traces;
- common electrical GND retained.

Thermal isolation is geometric, not a split-ground strategy.

## 10. Air chamber mechanical interface
Required stack:
room air -> hidden inlet microchannels -> isolated passive chamber -> SHT45 membrane -> hidden outlet microchannels.

Mechanical CAD must provide:
- at least two separated air paths;
- no direct warm-air path from MAIN cavity;
- no enclosure rib/screw acting as a thermal bridge into the sensing tab;
- dust/condensation-conscious geometry;
- no visible front opening required.

Exact channel geometry remains a mechanical/CFD release gate.

## 11. OPT3004 optical layout
OPT3004 aperture faces the printed acoustic fabric through a controlled dark tunnel/baffle.

Keep out:
- adhesive;
- conformal coating;
- silkscreen/obstruction over aperture;
- internal status/privacy LED line-of-sight;
- uncontrolled translucent plastic light pipes.

Maintain repeatable fabric-to-sensor geometry.

## 12. Lux calibration
Baseline:
Lux_room = Lux_sensor * K_fabric

Production characterization shall use:
- final printed fabric;
- final optical tunnel;
- multiple illuminance levels;
- representative color temperatures.

If scalar correction is insufficient, firmware may use piecewise/profile calibration by artwork/front-stack family.

## 13. Firmware sampling
SHT45:
- low-duty-cycle periodic sampling;
- normal target 15..60 s;
- expose raw diagnostic reading in service mode.

OPT3004:
- periodic or continuous mode as required for responsive room-light automation.

Avoid excessive SHT45 measurement rate/self-heating.

## 14. Factory test
Mandatory:
1. resistance-to-ground before power;
2. +3V3_SYS;
3. I2C enumeration;
4. SHT45 address/CRC-valid measurement;
5. temperature sanity;
6. RH sanity;
7. OPT3004 target address;
8. dark/light response;
9. internal LED leakage test;
10. calibration-data write/read;
11. FPC flex/contact test.

## 15. Layout priorities
1. SHT45 thermal isolation;
2. SHT45 air exposure;
3. OPT3004 optical aperture/alignment;
4. clean I2C routing;
5. bypass placement;
6. FPC mechanical retention.

Keep PCB-D away from MAIN DC/DC, PoE, TAS5825M and DML exciter thermal paths.

## 16. Release gates
Before production freeze:
1. verify OPT3004 ADDR physical strap for target 0x45 from TI datasheet;
2. verify exact SHT45 and OPT3004 manufacturer footprints;
3. freeze J301 mating orientation/pin-1;
4. finalize PCB-D position;
5. thermal/CFD chamber validation;
6. warm-electronics soak characterization;
7. final SHT45 correction model;
8. final fabric lux calibration;
9. LED leakage validation;
10. condensation/dust review;
11. I2C rise-time/EMC validation with Class-D, Ethernet and radar active.

## 17. Capture status
The electrical architecture, sensor devices, rail, I2C ownership, address map target, interrupt policy, board-ID policy and thermal/optical PCB rules are defined.

Status:
**READY_FOR_NATIVE_KICAD_STRUCTURE_AND_CAPTURE_WITH_ADDRESS_STRAP_AUDIT**.
