# AudioPicture Rev.E — electronics packaging ≤ 30 mm

Status: **PACKAGING_SPEC / NOT_A_PCB_RELEASE**  
Authority: [`docs/architecture/v2.2-rev-e-dml-30mm.md`](../docs/architecture/v2.2-rev-e-dml-30mm.md)

## 1. Problem

Rev.E keeps the full room node (MCU, Ethernet, PoE, amp, voice, radar, climate, light, power monitor) inside a **≤ 30 mm** picture. Tall modules (PoE PD, RJ45, inductors) fight the acoustic stack. This document fixes the packaging rules before the MAIN respin.

## 2. Service-rail layout

Prefer a **bottom service rail** across the 320 mm width, height ~45–60 mm in Y, depth ≤ 30 mm in Z:

| Zone (left → right, example) | Contents |
| --- | --- |
| Power | DC jack and/or PoE RJ45 + magnetics + PD; input protection; OR-ing |
| Rails | 24 V sense (INA228), 5 V and 3V3 bucks |
| Compute | ESP32-S3 module, W5500, flash keep-outs |
| Audio | TAS5825M, LC filters, short leads to exciters |
| Voice / I/O | Flex header to XVF3800, mute latch, LED |

The DML panel occupies the area **above** the rail. The rail is part of the frame mass, not bonded as a stiffener across the radiating aperture.

Top and side frame members host:

- 4-mic array (horizontal bar preferred);
- OPT3004 optical window;
- SHT45 vent;
- LD6004 radar window;
- status LED and edge buttons.

## 3. Function checklist (must all ship)

| Function | Part class | Packaging rule |
| --- | --- | --- |
| MCU + Wi-Fi | ESP32-S3-WROOM-1-N16R8 | Antenna keep-out; no continuous ground under antenna |
| Ethernet | W5500 + LAN transformer + RJ45 | RJ45 on bottom edge; verify shell vs 30 mm |
| PoE | Ag53024 class or thinner OEM PD | **Height gate:** if PD + magnetics exceed budget, wall-recessed inlet or alternate PD — PoE stays a product requirement |
| Ext. 24 V | Locking DC | Same edge as PoE OR |
| Amp | TAS5825M dual BTL | Short twisted pairs / flex to EX_LF and EX_WB; LC retuned for exciter Z |
| Voice DSP | XVF3800 Flex core | Behind rail or thin stack; 80 mm IDC as P1 intent if depth allows, else board-to-board |
| Microphones | 4-mic array | Frame-mounted; hardware mute kills mic/Flex 5 V |
| Presence | LD6004 60 GHz | Edge RF window |
| Temp / RH | SHT45 | Room vent, away from PVDD heat |
| Light | OPT3004 | Optical island |
| Power monitor | INA228 + 8 mΩ shunt | On 24 V rail |
| User | Mute + action | Edge; privacy LED |
| Service | USB-C | Bottom edge |

## 4. Thickness and thermal gates

Before releasing Gerbers:

1. Stack-up drawing: fabric → panel → exciters → rear skin → wall gap, with every IC height.
2. PoE PD + RJ45 + DC jack 3D keep-out vs 30.0 mm.
3. Thermal: amp and PD ΔT with product on wall, fabric on, 1/8 and 1/1 rated drive.
4. Buzz: sine sweep at limiter with full electronics populated.
5. Mic SNR with panel playing 80 dB at 1 m (AEC path stress).

## 5. Electrical inheritance

Rev.A / P1 power tree, PoE OR-ing intent, INA228 telemetry, and privacy-mute hardware policy remain unless a height conflict forces a drop-in alternate with equal safety behaviour. Acoustic load changes from 4 Ω cones to two DML exciters: **revalidate** LC filter, stability, and TAS PVDD budgeting.

## 6. Firmware hooks (unchanged intent)

- UART0 = radar; logs on USB-Serial-JTAG only.
- While muted: I2S/I2C GPIOs to voice are Hi-Z.
- `TAS_PDN` low until rails valid and DML coefficients loaded.
- On PoE brown-out: program ceiling drops (power governor).

Room roles, clock, and HA planner: Rev.E architecture §3.
