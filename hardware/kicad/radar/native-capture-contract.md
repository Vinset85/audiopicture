# PCB-C RADAR Rev.A — Native KiCad Capture Contract

Status: **READY_FOR_NATIVE_KICAD_STRUCTURE_AND_PARTIAL_CAPTURE**
Target: **KiCad 9.x**

This document is the reviewed electrical input for PCB-C RADAR native schematic capture. Native .kicad_sch/.kicad_pcb files must only be created, opened, saved and validated by KiCad 9.x.

Detailed engineering authority: `hardware/radar/bgt60tr13c-rev-a.md`.

## 1. Functional blocks
1. J201 MAIN interface.
2. U201 BGT60TR13C.
3. U202 +1V8_RADAR low-noise LDO.
4. per-domain radar supply filtering/decoupling.
5. U204/U205 fixed-direction level translation.
6. 80 MHz OSC_CLK source.
7. RF/antenna keep-out and mechanical window.
8. factory/debug test points.

## 2. J201 MAIN interface
J201 = **Hirose FH12-12S-0.5SH(55)**, 12-contact, 0.5 mm pitch, bottom-contact ZIF, horizontal insertion, 0.30 mm FPC:
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

MAIN controls:
- RADAR_EN = ESP32 GPIO16
- RADAR_RST = ESP32 GPIO42

PCB-C owns +1V8_RADAR, level translation and radar reference clock.

## 3. Radar device
U201 = **Infineon BGT60TR13C**, PG-VF2BGA40-1, integrated antenna.

Supply domains:
- VDDD = 1.8 V
- VDDA = 1.8 V
- VDDVCO = 1.8 V
- VDDRF = 1.8 V
- VDDPLL = 1.8 V
- VDDLF = 3.3 V
- VAREF = output/reference node requiring reference-design bypass

Ground remains a common system ground. Do not invent split-ground islands.

## 4. +1V8_RADAR
U202 preferred family = **onsemi NCP167**, fixed 1.8 V.

Requirements:
- input +3V3_SYS;
- >=300 mA AudioPicture continuous engineering allocation;
- regulator family capability provides substantial transient margin;
- low-noise/high-PSRR implementation;
- exact fixed-1.8 V orderable MPN/package is a BOM gate;
- XDFN4 1x1 mm preferred over WLCSP if lifecycle/assembly review passes.

Manufacturer nominal application uses 1 uF-class ceramic input/output capacitors. Final capacitance/layout follows exact selected order code/datasheet.

## 5. Radar-domain filtering
Do not connect all 1.8 V pins through one long undifferentiated rail.

Capture separate reference-derived filter/decoupling branches for:
- VDDD
- VDDA
- VDDVCO
- VDDRF
- VDDPLL
- oscillator supply where applicable

and the required VAREF bypass.

Exact ferrite/R/C values remain **OPEN_RDK_REFERENCE_TRANSCRIPTION**.

Release verification must address the BGT60TR13C supply-noise requirement, including the stringent 20 kHz..700 kHz noise region.

## 6. VDDLF
VDDLF receives +3V3_SYS through the Infineon-reference filtering/decoupling network.

Do not assume VDDLF is a digital 3.3 V I/O supply; it is the analog supply for the PLL loop-filter level-shifter domain.

## 7. Digital translation
Use two **TI SN74AXC4T245** devices.

U204:
- SPI_SCLK: 3.3 -> 1.8
- SPI_MOSI: 3.3 -> 1.8
- SPI_MISO: 1.8 -> 3.3
- RADAR_IRQ: 1.8 -> 3.3

U205:
- RADAR_CS: 3.3 -> 1.8
- RADAR_RST: 3.3 -> 1.8
- remaining channels unused and disabled/NC per TI requirements.

Rails:
- VCCA = +3V3_SYS
- VCCB = +1V8_RADAR

DIR straps are fixed by channel group.
OE is active-low and must default HIGH/disabled through a pull-up referenced to the controlling supply.

Translation may only be enabled after +1V8_RADAR is valid.

Required properties:
- fixed direction;
- Ioff partial-power-down;
- high impedance during missing-rail condition;
- no parasitic radar powering;
- no shared-SPI MISO contention.

Exact SN74AXC4T245 package remains a PCB fanout/assembly gate.

## 8. SPI
Shared MAIN bus:
- SPI_SCLK
- SPI_MOSI
- SPI_MISO

Dedicated:
- RADAR_CS
- RADAR_IRQ
- RADAR_RST

BGT60TR13C supports SPI operation up to the datasheet limit; AudioPicture does not automatically use the maximum rate.

Policy:
- conservative bring-up clock;
- per-device ESP32 transaction configuration;
- production clock only after translator + FPC + shared-bus SI validation;
- firmware must never assert ETH_CS and RADAR_CS simultaneously.

## 9. Reference clock
BGT60TR13C system-reference specification:
- allowed reference-frequency range: 75..85 MHz;
- nominal baseline: **80 MHz**;
- **78 MHz is prohibited** by the device datasheet.

AudioPicture Rev.A uses an 80 MHz OSC_CLK baseline coherent with the Infineon BGT60TR13C Shield/reference architecture.

Exact oscillator MPN, supply/filtering, output electrical format and layout are **OPEN_RDK_HARDWARE_TRANSCRIPTION**.

Do not substitute 38.4 MHz.

## 10. Power/reset sequencing
OFF/safe state:
- RADAR_EN low;
- translation disabled/high-Z;
- RADAR_RST asserted;
- no back-power through SPI/IRQ.

Enable:
1. +3V3_SYS valid;
2. assert RADAR_RST;
3. enable +1V8_RADAR;
4. wait for LDO/filter/clock settling;
5. enable translators;
6. release RADAR_RST;
7. initialize SPI conservatively;
8. configure radar/FIFO/IRQ.

Disable in reverse order so digital drive disappears before the radar rail collapses.

## 11. RF / antenna rules
BGT60TR13C antenna-in-package region is a strict RF keep-out.

No:
- copper/ground in prohibited antenna region;
- metal screws;
- magnets;
- shield cans;
- large conductive structures;
- DML conductive skin directly in front;
- uncontrolled adhesive/dielectric stack in front of antenna.

Target front stack:
room -> printed acoustic fabric -> characterized plastic/air window -> BGT60TR13C antenna face.

If the DML panel has conductive skins, provide a dedicated radar aperture/window.

Exact PCB-C X/Y/angle remain mechanical/RF optimization variables.

## 12. Layout
Follow Infineon reference-board stackup and package/layout rules.

Priorities:
1. antenna keep-out and front window;
2. oscillator-to-OSC_CLK path;
3. radar-domain supply filters/decoupling;
4. ground-via implementation;
5. short translated SPI;
6. separation from DML/Class-D currents and switching converters.

No production test stub on OSC_CLK.

## 13. Factory test
Provide test capability for:
- +3V3_SYS
- +1V8_RADAR
- GND
- RADAR_EN
- RADAR_RST
- RADAR_IRQ
- translated SPI functional access
- reference clock verification

Mandatory tests:
1. unpowered rail resistance;
2. 1.8 V startup/current sanity;
3. translator OFF isolation;
4. OSC_CLK frequency;
5. chip/register access;
6. reset/IRQ;
7. raw radar frame;
8. moving-target sanity;
9. stationary/micro-motion presence;
10. simultaneous Ethernet/shared-SPI traffic;
11. Wi-Fi/Class-D coexistence.

## 14. ERC rules
- no blanket PWR_FLAG;
- no direct 3.3 V drive into BGT60TR13C VDDD-domain digital pins;
- deterministic OE/reset/enable states;
- no powered MAIN signal may back-power disabled +1V8_RADAR;
- explicit NC on unused translator channels/pins per TI requirements;
- OPEN_RDK values are not production freezes.

## 15. Release gates
Before PCB-C production freeze:
1. exact NCP167 1.8 V orderable MPN/package;
2. Infineon RDK per-domain filter/decoupling transcription;
3. exact 80 MHz oscillator MPN and supply network;
4. exact U204/U205 package/fanout;
5. BGT60TR13C manufacturer land pattern/reference layout audit;
6. RF stackup/antenna keep-out implementation;
7. front fabric/plastic RF characterization;
8. DML/radar interaction validation;
9. shared-SPI SI at production clock;
10. final enclosure stationary-person performance;
11. EMC/coexistence validation.

Physical connector MPN is frozen; final mating-view orientation/pin-1 cross-check against the Hirose 2D drawing remains mandatory before PCB release.

## 16. Capture status
J201, rail domains, preferred LDO family, dual fixed-direction translator architecture, safe sequencing, 80 MHz nominal clock requirement and RF keep-out rules are defined.

The remaining open items are reference-design/BOM/layout release gates, not architecture gaps.

Status:
**READY_FOR_NATIVE_KICAD_STRUCTURE_AND_PARTIAL_CAPTURE / BLOCKED_ON_RDK_FILTER_OSCILLATOR_TRANSCRIPTION**.
