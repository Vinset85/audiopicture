# AudioPicture V2.2 Rev.A — XVF3800 VOICE power tree

Status: **VOICE_0P80W_SYSTEM_ALLOCATION_RETAINED / EXACT_XVF_IO_RAIL_CURRENT_AND_REGULATOR_LOSS_RELEASE_GATE**

## 1. Purpose
Close the first quantitative power-tree model for PCB-B VOICE and verify the 0.80 W system allocation used by the AudioPicture system power budget.

## 2. XVF3800 supply domains
Manufacturer-required rails:
- VDD digital core: 0.9 V nominal;
- PLL_AVDD: 0.9 V nominal, low-pass isolated from other 0.9 V loads;
- VDDIOB18: 1.8 V nominal;
- VDDIOL/VDDIOR/VDDIOT: 3.3 V nominal;
- USB_VDD18 / USB_VDD33 may remain unpowered/floating as permitted by XMOS when USB is unused.

AudioPicture baseline does not use XVF3800 USB in normal operation.

## 3. Core power
XMOS published typical core VDD consumption:
- I2S operation: 345 mW;
- USB operation: 400 mW.

Use **345 mW typical** as the normal I2S processing anchor.

Do not convert 345 mW into an exact 0.9 V rail current for production regulator signoff until the manufacturer's definition of core-power coverage and operating conditions is fully reconciled with the chosen firmware build.

## 4. Microphone rail
4 x Infineon IM72D128V01 at 1.8 V.

At 3.072 MHz PDM clock, manufacturer electrical characteristics:
- 430 uA typical per microphone;
- 525 uA maximum per microphone.

Four-microphone array:
- typical current = 1.72 mA;
- maximum current = 2.10 mA;
- typical power at 1.8 V = 3.10 mW;
- maximum power at 1.8 V = 3.78 mW.

Therefore microphone electrical consumption is negligible relative to XVF3800 core power.

## 5. PDM clock
XVF3800 MIC_CLK = 3.072 MHz baseline.
Feed this clock directly to all four PDM microphones as required by the XVF3800 architecture.

Do not introduce independent microphone oscillators.

## 6. Peripheral allocations
Until exact dynamic-current closure:
- QSPI W25Q32JV: reserve 50 mW active-design allowance;
- 24 MHz oscillator: reserve 20 mW;
- 3.3 V / 1.8 V I/O switching and pull networks: reserve 80 mW;
- privacy/load switch and miscellaneous: reserve 15 mW.

These are engineering allocations, not claimed typical component consumptions.

## 7. Regulator architecture
Input from MAIN system low-voltage supply as defined by daughterboard interface.

Baseline:
- TPS62823 -> 0.9 V core rail;
- filtered branch from 0.9 V -> PLL_AVDD;
- TPS7A2018 -> 1.8 V rail;
- 3.3 V rail supplied according to final daughterboard power ownership.

Regulator-loss budget reserve: **100 mW** until exact input voltage/current and efficiency curves are solved.

## 8. Budget closure
Known/allocated:
- XVF3800 core typical: 345 mW
- 4 microphones typical: 3.1 mW
- QSPI allowance: 50 mW
- oscillator allowance: 20 mW
- I/O allowance: 80 mW
- privacy/misc allowance: 15 mW
- regulator-loss allowance: 100 mW

First conservative total:
**~613 mW**

Add ~187 mW unresolved/current-variation margin.

Retain system-level VOICE allocation:
**0.80 W continuous design reservation**

The existing 0.80 W system budget is therefore not increased.

## 9. Thermal consequence
At approximately 0.6–0.8 W board input, PCB-B VOICE is not expected to dominate the enclosure thermal budget.

However, its carrier must remain mechanically/vibrationally isolated from the DML and thermally separated from MAIN-C Ag53024 plume.

Do not add a thermal bridge that compromises microphone mechanical isolation.

## 10. Power-state opportunity
Future firmware may reduce VOICE consumption by:
- disabling microphone clock when privacy/hardware-mute policy permits;
- using microphone clock-off mode;
- placing XVF3800/peripherals into supported low-power states.

These savings are not credited to the baseline PoE ECO budget.

## 11. Release gates
1. obtain exact XVF3800 I/O-rail currents for selected firmware mode;
2. close W25Q32JV active/standby current from exact boot/runtime behavior;
3. close oscillator exact MPN current;
4. calculate TPS62823 and TPS7A2018 losses at measured loads;
5. verify 0.9 V transient response under XVF workload;
6. verify microphone supply noise and PSR;
7. thermal-check XVF3800 package/carrier;
8. measure or simulate full VOICE board power before production release.

Status: **VOICE_POWER_FIRST_ORDER_0P613W / 0P80W_CONTINUOUS_RESERVATION_CONFIRMED**.
