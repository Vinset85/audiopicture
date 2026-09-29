# PCB-B VOICE Rev.A — Native KiCad Capture Contract

Status: **READY_FOR_NATIVE_KICAD_STRUCTURE_AND_PARTIAL_CAPTURE**
Target: **KiCad 9.x**

This document is the reviewed electrical input for the PCB-B VOICE native schematic. It is not a substitute for a KiCad schematic. Native files must be generated, opened, ERC-checked and saved by KiCad 9.x.

The detailed engineering authority remains `hardware/voice/xvf3800-sq66-rev-a.md`.

## 1. Functional blocks
1. J101 MAIN interface.
2. XVF3800 voice processor.
3. local +0V9_VOICE regulator.
4. local +1V8_VOICE regulator.
5. PLL filtered rail.
6. local QSPI boot flash.
7. hardware microphone privacy switch.
8. four PDM microphones in SQ66 geometry.
9. factory/debug test points.

## 2. MAIN interface — J101
Physical connector: Hirose FH12 family, 0.5 mm pitch, 16 contacts, 0.30 mm FPC.

Logical interface retained from MAIN:
- +5V_SYS x2
- +3V3_SYS
- GND x2 minimum logical returns
- AUD_BCLK
- AUD_LRCLK
- AUD_TX
- AUD_RX
- I2C_SDA
- I2C_SCL
- VOICE_RST
- VOICE_IRQ
- MIC_HW_EN

Two additional physical contacts are GND/reference contacts for the I2S group.

**Do not assign final physical pin numbers 1..16 until the exact PCB-B connector orientation and FPC mating-side drawing are reviewed.** Logical signals are frozen; physical ordering is a mechanical capture gate.

MAIN is the only source of +5V_SYS/+3V3_SYS and the only populated owner of shared I2C pull-ups. PCB-B must not back-power MAIN.

## 3. XVF3800
U101 = **XMOS XVF3800-QF60B-C**.

Frozen supply groups:
- VDD pins 4,12,19,27,34,42,49,57 -> +0V9_VOICE;
- core paddles 61..64 -> +0V9_VOICE;
- V_DDIOL pin 8 -> +3V3_SYS;
- V_DDIOR pin 38 -> +3V3_SYS;
- V_DDIOT pin 52 -> +3V3_SYS;
- VDD_IOB18 pins 17,26 -> +1V8_VOICE;
- PLL_AVDD pin 22 -> +0V9_PLL filtered from +0V9_VOICE;
- VSS paddle pin 65 -> GND with local vias;
- USB_VDD18 pin 31 and USB_VDD33 pin 30 remain unpowered in Rev.A unless XVF3800 USB is explicitly enabled later.

All numeric pins must be rechecked against the current XMOS pin table when the native symbol is created/imported.

## 4. Local rails
Inputs from MAIN:
- +5V_SYS
- +3V3_SYS

Local outputs:
- +0V9_VOICE
- +1V8_VOICE
- +0V9_PLL
- +3V3_MIC switched

Exact +0V9/+1V8 regulator MPNs and their reference passives are **OPEN_REFERENCE_TRANSCRIPTION** from XK-VOICE-SQ66 Design Files 1V1.

Do not choose substitute regulators merely to complete ERC.

## 5. Decoupling
Provide local 100 nF-class high-frequency ceramic bypass at each practical XVF3800 supply-pin group with minimum loop area.

Bulk/domain capacitors and exact PLL filter components must be transcribed from the official SQ66 design files.

+0V9_PLL is a dedicated filtered PLL supply, not a direct connection to a noisy common rail.

## 6. QSPI boot
Normal product boot = local QSPI master boot.

Frozen:
- QSPI_D1 pin 1 -> boot flash D1; no normal-product boot-mode pull-up;
- QSPI_D3 pin 2 -> flash D3;
- QSPI_CS_N pin 3 -> flash CS_N + 4.7 kOhm pull-up;
- QSPI_CLK pin 5 -> flash CLK;
- SPI_CS_N pin 6 -> 4.7 kOhm pull-up.

Remaining QSPI data pins are taken from the current XMOS pin table/reference design during capture, not guessed.

Flash capacity baseline: **>=32 Mbit**.
Exact flash MPN and supply voltage: **OPEN_REFERENCE_TRANSCRIPTION**.

Layout:
- flash adjacent to U101;
- CLK shortest/highest priority;
- no test-pad stubs on QSPI;
- continuous GND reference.

## 7. Host audio/control
XVF3800 is I2S slave.

From MAIN:
- AUD_BCLK -> XVF3800 BCLK
- AUD_LRCLK -> XVF3800 LRCLK
- AUD_TX -> far-end/AEC-reference input

To MAIN:
- processed voice stream -> AUD_RX

System target: 48 kHz, 32-bit slots.

Control:
- I2C_SDA
- I2C_SCL
- VOICE_RST
- VOICE_IRQ

Do not add daughterboard I2C pull-ups by default.

## 8. Microphones
MIC101..MIC104 = **Infineon IM72D128V01XTMA1**.

Status: **FROZEN_DEVICE / FOOTPRINT_ACOUSTIC_VERIFY**.

Array:
- four independent microphones;
- nominal 66 x 66 mm square;
- final CAD coordinates become firmware geometry;
- equal acoustic treatment.

Electrical:
- VDD -> +3V3_MIC;
- local 100 nF X7R per microphone;
- nominal PDM clock = 3.072 MHz;
- MIC_DATA0..3 independent to XVF3800;
- no wire-OR data topology.

Keep microphone ports, land pattern and acoustic keep-outs per Infineon manufacturer drawing.

## 9. PDM routing
XVF3800 MIC_CLK fans out to all four microphones.

Use short controlled branches/star-like distribution and continuous GND reference.
Provide optional source-damping footprint at MIC_CLK driver; initial value is a capture/tuning placeholder, not a production freeze.

MIC_DATA0..3 return independently.
Keep PDM away from DML/Class-D switching paths.

## 10. Hardware privacy
Q101 baseline = **TI TPS22913C family**.

Topology:
+3V3_SYS -> Q101 IN
Q101 OUT -> +3V3_MIC
MIC_HW_EN -> Q101 ON
Q101 GND -> GND

Required behavior:
- MIC_HW_EN LOW = microphones physically unpowered;
- reverse-current protection;
- quick output discharge;
- no back-power through PDM pins.

MAIN owns the 100 kOhm MIC_HW_EN pull-down. PCB-B shall not add a conflicting pull-up.

Exact orderable TPS22913C suffix/package remains a footprint/manufacturing gate.

Optional series footprints on PDM CLOCK/DATA may be used to control power-off injection/SI after validation.

## 11. Reset / sequencing
Required sequence:
1. +3V3_SYS/+5V_SYS valid;
2. +0V9_VOICE/+1V8_VOICE valid;
3. QSPI flash supply valid;
4. VOICE_RST release;
5. XVF3800 boot/control validation;
6. MIC_HW_EN remains LOW until privacy/voice state initialized;
7. +3V3_MIC enabled only when explicitly required.

Brownout/reset returns microphone power to OFF through MAIN hardware bias.

Any additional XMOS reset conditioning/supervisor network must be transcribed from SQ66 reference design.

## 12. Voice vs measurement mode
VOICE mode:
4x PDM -> XVF3800 -> AEC/beamforming/NS/AGC/VAD/DoA -> AUD_RX.

MEASUREMENT mode:
must expose four raw or minimally processed microphone channels suitable for room impulse/response measurement.

Production freeze is prohibited until the selected XVF3800 firmware build demonstrates the measurement path.

## 13. Mechanical/acoustic constraints
- SQ66 board mechanically isolated from DML vibration;
- independent short acoustic path per microphone;
- no shared front cavity that strongly cross-couples ports;
- printed acoustic fabric attenuation characterized;
- no frame rib/adhesive blocks a microphone port;
- keep switching regulators and Class-D wiring away from microphone region.

## 14. Factory test points
Provide accessible test capability for:
- +5V_SYS
- +3V3_SYS
- +1V8_VOICE
- +0V9_VOICE
- +3V3_MIC
- GND
- VOICE_RST
- VOICE_IRQ
- MIC_HW_EN
- MIC_CLK
- I2C SDA/SCL
- I2S BCLK/LRCLK
- QSPI integrity by functional boot rather than long high-speed pogo stubs.

## 15. ERC rules
- no blanket PWR_FLAG suppression;
- no duplicate I2C pull-up ownership;
- no unpowered microphone backfeed;
- explicit NC on unused XVF3800 USB pins/domains as required by XMOS;
- every reset/enable has a deterministic state;
- do not mark OPEN_REFERENCE_TRANSCRIPTION values as production-frozen.

## 16. Mandatory gates before full native capture/release
Obtain and inspect official **XK-VOICE-SQ66 Design Files 1V1** and transcribe:
1. +0V9 regulator MPN/network;
2. +1V8 regulator MPN/network;
3. PLL filter values;
4. exact QSPI flash MPN/supply/decoupling;
5. clock/support network;
6. reset/support network.

Then verify:
7. IM72D128 manufacturer footprint/acoustic port;
8. exact TPS22913C orderable suffix/package;
9. J101 PCB-B orientation and 16-contact FPC mapping;
10. raw four-channel measurement firmware;
11. AEC latency/reference coherence;
12. DML vibration isolation and fabric acoustic behavior.

## 17. Capture status
The hierarchy, interfaces, XVF3800 power-pin groups, boot concept, PDM topology, microphone device, privacy topology and sequencing are ready for native schematic structure/capture.

**Do not complete the regulator/PLL/flash/clock/reset sections from inference.**

Status: **READY_FOR_NATIVE_KICAD_STRUCTURE_AND_PARTIAL_CAPTURE / BLOCKED_ON_XK_VOICE_SQ66_REFERENCE_TRANSCRIPTION**.


## J101 physical-contact capture gate
J101 has **16 physical contacts** and 14 logical signals plus two additional GND references.

The historical 1..14 logical ordering is not permission to assign the final FH12 physical contacts 1..16 by extension. Before native connector capture:
1. open the exact FH12-16S-0.5SH(55) mating-side drawing;
2. establish PCB connector orientation and FPC contact-side orientation;
3. place the two additional GND references adjacent/near the I2S group for return continuity;
4. document the resulting physical 1..16 map here and in Sheet 07;
5. cross-check both ends of the FPC.

Until this is complete, J101 is **LOGICALLY_FROZEN / PHYSICAL_PIN_MAP_OPEN**.


## J101 connector MPN freeze
J101 = **Hirose FH12-16S-0.5SH(55)**.
Verified family attributes: 16 positions, 0.5 mm pitch, bottom-contact ZIF, horizontal insertion, 0.30 mm FPC, 0.5 A/contact.

The MPN is frozen. The final 1..16 net assignment remains blocked only on mating-view/FPC-orientation review; do not infer it by mirroring the legacy 14-signal table.
