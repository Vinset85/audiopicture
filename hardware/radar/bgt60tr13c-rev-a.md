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
- RADAR_SCLK
- RADAR_MOSI
- RADAR_MISO
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
BGT60TR13C requires an external reference clock in the ~80 MHz class according to the selected operating/reference design.

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
