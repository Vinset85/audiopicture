# AudioPicture V2.2 — ESP32-S3 antenna mechanical placement Rev.A

Status: **MAIN_C_LEFT_EDGE_ANTENNA_PLACEMENT_FROZEN_FOR_DMU / 15MM_ENCLOSURE_CLEARANCE_MASK / RF_TEST_REQUIRED**

## 1. Purpose
Close the previously undefined ESP32-S3-WROOM-1 antenna position so the front-frame magnetic system can be checked against a concrete Wi-Fi/BLE keep-out.

## 2. Manufacturer rule
Follow current Espressif module-on-base-board guidance:
- place the module PCB antenna at/outside a base-board edge where possible;
- keep the antenna feed point close to the base-board edge;
- preserve a sufficiently large enclosure clearance around the PCB antenna;
- use at least 15 mm clearance in all directions as the enclosure-level design seed;
- validate final product throughput/range.

Manufacturer RF/layout guidance remains authoritative over this packaging document.

## 3. MAIN-C
MAIN-C:
X=85..235
Y=315..370 mm.

## 4. Frozen DMU placement
Place ESP32-S3-WROOM-1 at the **left edge of MAIN-C**.

Orientation:
- module long axis approximately X;
- antenna end faces -X;
- antenna region overhangs/cutout-supports at the left board edge;
- RF radiation opens toward the left/perimeter unfilled-polymer region.

Seed module body envelope:
X approximately 79..104.5
Y approximately 333.5..351.5 mm
subject to exact module STEP/land-pattern orientation.

Antenna-end region is at the low-X end.

## 5. Enclosure RF mask
Create:
ESP32_RF_KO_A.

Use conservative 15 mm expansion around the exact antenna body/antenna area in X/Y/Z directions where physically applicable.

No:
- steel magnetic target;
- magnet;
- PC-CF;
- wall cleat;
- RJ45 magnetics;
- PoE module;
- Class-D output inductor;
- large metal hardware
inside the RF mask unless RF validation explicitly allows it.

Unfilled ASA and fabric are preferred materials in the RF window.

## 6. Magnet compatibility
Nearest top-left front magnet:
M1C=(70,394.6).

Nearest left-upper magnet:
M6C=(5.4,275).

With antenna placed around MAIN-C left edge near Y342.5:
- M1C is well above the antenna region;
- M6C is far left/lower;
- neither is intended to enter the 15 mm antenna expansion mask.

Exact CAD mask intersection is authoritative.

If exact STEP changes antenna extent, magnet stations may move tangentially only.

## 7. Structural frame consequence
PC-CF left/top rail geometry must be clipped around ESP32_RF_KO_A.

Do not solve a frame stiffness issue by restoring carbon-filled material in the antenna clearance.

Use local load-path diversion around the RF mask.

## 8. MAIN-C layout consequence
Reserve the left-edge RF region first.

Place away from antenna:
- W5500;
- Ethernet magnetics;
- RJ45;
- Ag53024;
- high-current/high-dVdt power;
- USB/UART where practical.

The native PCB layout must inherit the RF keep-out before component placement.

## 9. DML relationship
The DML composite is not treated as metallic shielding in this mechanical screen.

However, final assembled Wi-Fi/BLE validation is mandatory because laminate, adhesive, fabric print, nearby wiring and the wall can detune the antenna.

## 10. Automatic checks
C451 ESP32 module located at MAIN-C board edge.
C452 antenna end faces product perimeter.
C453 base-board copper/component keep-out follows exact Espressif land pattern.
C454 enclosure-level 15 mm antenna clearance mask generated.
C455 no front magnet intersects ESP32_RF_KO_A.
C456 no steel target intersects ESP32_RF_KO_A.
C457 no PC-CF intersects ESP32_RF_KO_A.
C458 no wall cleat intersects ESP32_RF_KO_A.
C459 high-noise MAIN-C components remain outside RF region.
C460 final assembled Wi-Fi/BLE throughput/range test remains mandatory.

## 11. State
DMU antenna placement:
**MAIN-C LEFT EDGE / ANTENNA FACING -X / 15MM ENCLOSURE RF MASK**

This placement is compatible with the Rev.C magnetic station concept at packaging level.

Status:
**ESP32_RF_POSITION_DEFINED / FRONT_MAGNET_COMPATIBLE_COARSE / C01_TO_C460 / EXACT_STEP_AND_RF_TEST_GATE**.
