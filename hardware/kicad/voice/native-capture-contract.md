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


## QSPI boot electrical gate closure — 2026-09-29
Official XVF3800 documentation plus the XK-VOICE-SQ66 product specification establish:
- production local boot uses quad-capable QSPI flash;
- XK-VOICE-SQ66 reference capacity = **32 Mbit**;
- QSPI I/O belongs to XVF3800 IOL domain;
- VDDIOL = **+3V3_SYS** in AudioPicture, therefore the selected QSPI flash shall be a 3.3 V device compatible with that I/O domain;
- QSPI_CS_N has an external **4.7 kOhm pull-up**;
- QSPI_D1/BOOTSEL connects directly to flash D1 for QSPI master boot and shall not be strapped high in normal production mode;
- QSPI_D0/D1/D2/D3/CLK/CS are point-to-point local PCB-B nets;
- flash is placed adjacent to U101, QSPI_CLK shortest, continuous GND, no production test stubs.

The exact SQ66 flash order code remains **OPEN_SQ66_ARCHIVE_TRANSCRIPTION**. Do not substitute an arbitrary 1.8 V flash.

Status for U102:
**32_MBIT_3V3_QSPI_ELECTRICAL_INTERFACE_FROZEN / EXACT_MPN_OPEN**.


## XU316 electrical-envelope closure — 2026-09-29
The XVF3800-QF60B silicon power envelope is now tied to the official XU316-1024-QF60B datasheet:
- +0V9_VOICE / VDD operating range: 0.855..0.945 V, nominal 0.900 V.
- XU316 active VDD budget: 300 mA typical / 1110 mA maximum for C32/I32 budgetary conditions; Rev.A +0V9 regulator shall therefore be designed for **>=1.2 A continuous capability**, with transient/thermal margin and XMOS power-estimation validation.
- PLL_AVDD operating range: 0.855..0.945 V; typical current 5 mA.
- +1V8_VOICE / VDDIOB18 operating range: 1.62..1.98 V, nominal 1.8 V; QF60B bank current absolute limit 126 mA. Rev.A regulator allocation = **>=200 mA continuous**.
- QF60B VDDIOL/VDDIOR/VDDIOT are 3.3 V domains and remain supplied from +3V3_SYS.
- reset pulse width minimum = 5 us; boot initialization begins after reset release and is specified at up to 480 us.
- external XIN clock allowed range 8..30 MHz, 24 MHz nominal baseline when oscillator mode is used.

Regulator electrical requirements are therefore frozen even while exact SQ66 order codes remain open:
- U_VOICE_0V9: 3.3 V input preferred, fixed/accurate 0.9 V, >=1.2 A continuous design capability, low-noise/fast-transient suitable for xcore.ai core.
- U_VOICE_1V8: 3.3 V input, fixed/accurate 1.8 V, >=200 mA continuous design capability.
- +0V9_PLL shall be filtered from +0V9_VOICE and is not a separate high-current regulator.

Do not select a low-current 0.9 V LDO merely because average XVF3800 current appears modest.
Exact regulator MPNs, PLL filter values and clock implementation remain SQ66/reference-layout gates.


## VOICE regulator MPN freeze — 2026-09-29
### U_VOICE_0V9
**Texas Instruments TPS62823DLCR**.
- VIN 2.4..5.5 V, fed from +3V3_SYS;
- 3 A capability;
- adjustable down to 0.6 V;
- 1% feedback accuracy;
- DCS-Control, fast transient response;
- PG available;
- VSON-HR DLC 8-pin, 2.0 x 1.5 mm;
- 470 nH-class inductor architecture consistent with the family.

Configure for **0.900 V nominal**. Exact feedback divider, output-capacitance/effective-C network and inductor MPN are capture/BOM validation gates. The use of the same regulator family/MPN already present on MAIN is intentional BOM consolidation, but PCB-B has an independent instance and output network.

### U_VOICE_1V8
**Texas Instruments TPS7A2018PDBVR**.
- fixed 1.8 V;
- 300 mA;
- VIN 1.6..6.0 V, fed from +3V3_SYS;
- 7 uVrms-class low output noise;
- high PSRR;
- 1.5% maximum output tolerance;
- stable with >=1 uF ceramic output capacitance;
- SOT-23-5 DBV package.

This provides 50% current headroom over the 200 mA Rev.A engineering allocation and avoids the tighter 250 mA ceiling of LP5907.

### PLL
+0V9_PLL remains derived from +0V9_VOICE through the XMOS/reference low-pass filter. It shall not be connected directly to the noisy switching node and shall not receive a separate arbitrary LDO unless reference/noise analysis requires one.

Status:
**VOICE_REGULATOR_DEVICES_FROZEN / 0V9_PASSIVES_PLL_FILTER_AND_SEQUENCE_VALIDATE**.


## +0V9_VOICE passive network and PLL filter freeze — 2026-09-29
### TPS62823 0.900 V network
TI TPS6282x Rev.C is the electrical authority.
Rev.A capture baseline:
- VIN = +3V3_SYS;
- L = **470 nH**;
- CIN = **4.7 uF nominal X7R/X5R**, minimum effective capacitance >=3 uF at bias;
- COUT = **2 x 10 uF nominal X7R/X5R**, with minimum total effective capacitance >=5 uF at 0.9 V and expected temperature/bias;
- VOUT = **0.900 V nominal**;
- FB divider shall be calculated from the current TI datasheet equation/reference voltage and then checked for standard-value tolerance; do not guess resistor values from another rail;
- PG may be used for VOICE sequencing/diagnostics but shall not create a new MAIN GPIO requirement unless reviewed.

The exact 470 nH inductor MPN and capacitor MPNs remain BOM/layout gates; the topology and nominal capacitance are frozen.

### +0V9_PLL
Official XU316-1024-QF60B authority:
- source = +0V9_VOICE;
- series ferrite = **600 ohm @ 100 MHz, DCR <1 ohm**;
- manufacturer example = **Taiyo Yuden BKH1005LM601-T**;
- PLL_AVDD local bypass = **1 uF MLCC** placed immediately at the pin;
- filtered node name = +0V9_PLL;
- no other loads on +0V9_PLL.

For Rev.A, BKH1005LM601-T is the preferred/frozen reference ferrite unless lifecycle/availability review forces an equivalent with matched impedance/DC-current/DCR behavior.

Layout priority: buck switch node and inductor remain physically separated from PLL_AVDD/ferrite/local capacitor; +0V9_PLL is routed only after the ferrite.

Status:
**0V9_TOPOLOGY_CAPACITANCE_AND_PLL_FILTER_FROZEN / FB_VALUES_AND_PASSIVE_MPNS_VALIDATE**.


## 24 MHz clock and reset/support freeze — 2026-09-29
### Crystal clock
Rev.A uses the XU316 internal oscillator with a local 24 MHz crystal rather than adding an external active oscillator.

Frozen reference implementation from the current XU316-QF60B datasheet:
- Y101 = **Seiko Epson FA-238 24.0000MD30X-W5**;
- frequency = 24 MHz;
- load capacitance = 12 pF;
- max ESR = 60 ohm;
- Rf = **1 Mohm** across XIN/XOUT;
- Rd = **680 ohm** damping resistor;
- CL1 = **22 pF**;
- CL2 = **22 pF**;
- XIN = QF60B pin 16;
- XOUT = QF60B pin 15.

The manufacturer-listed network is frozen as the capture baseline. Final oscillator startup/drive/layout verification remains mandatory.

### Reset
QF60B RST_N = pin 21 and is an active-low Schmitt input with internal pull-up.

AudioPicture keeps external VOICE_RST control from MAIN. Because the QF60B I/O rails are not all one common 1.8 V rail, do not rely solely on the internal POR: VOICE_RST shall remain asserted until +0V9_VOICE, +1V8_VOICE and +3V3_SYS are valid and the 24 MHz oscillator can start reliably.

Minimum reset pulse width remains 5 us; firmware/hardware shall use a substantially conservative margin during startup.

No arbitrary RC delay is frozen here: reset release is controlled by MAIN and shall be fail-safe low while MAIN is reset/unpowered according to the single-owner pull policy.

### TPS62823 0.900 V feedback
TPS62823 VFB nominal = **0.600 V**.

For 0.900 V:
VOUT = VFB * (1 + Rtop/Rbottom)
therefore Rtop/Rbottom = **0.5**.

Rev.A preferred capture pair:
- Rbottom (FB to GND) = **100 kohm, 1%**;
- Rtop (VOUT to FB) = **49.9 kohm, 1%**.

Ideal nominal output from these standard values is approximately **0.8994 V**, before reference/resistor tolerance.

Keep the divider immediately adjacent to FB, away from SW/inductor, and sense VOUT from the quiet output-capacitor node.

Status:
**VOICE_CLOCK_RESET_AND_0V9_FB_CAPTURE_BASELINE_FROZEN / STARTUP_LAYOUT_TOLERANCE_VALIDATE**.


## Final pin-audit correction
- XVF3800 pin 14 MCLK_INOUT connects locally to pin 41 MCLK in the standard internal-MCLK configuration.
- XVF3800 pin 25 is mandatory NC.
- XVF3800 USB pins 28..31 remain unconnected/unpowered in Rev.A.

Capture status: **READY_FOR_NATIVE_KICAD_DETAILED_CAPTURE / PRODUCTION_RELEASE_GATES_REMAIN**.


## U102 production QSPI selection
U102 = **Winbond W25Q32JVSSIQ**.
- 32 Mbit / 4 Mbyte serial NOR;
- 2.7..3.6 V supply, powered from +3V3_SYS;
- standard/dual/quad SPI capability;
- SOIC-8 208 mil production package;
- industrial temperature grade;
- local 100 nF X7R decoupling at VCC/GND;
- QSPI_CS_N retains the XVF3800-required 4.7 kohm pull-up;
- WP#/IO2 and HOLD#/RESET#/IO3 are used as QSPI D2/D3, not strapped in a way that conflicts with quad operation.

Status U102: **FROZEN_DEVICE_PACKAGE / BOOT_IMAGE_AND_PROGRAMMING_VALIDATE**.

## J101 physical-map gate refinement
FH12-16S-0.5SH(55) remains frozen as a 16-position, 0.5 mm pitch, bottom-contact horizontal ZIF. The connector drawing alone does not define whether a finished FPC preserves or reverses contact order between its two ends; that depends on the selected same-side/opposite-side FPC contact construction. Therefore final net-to-contact numbering is deliberately not frozen until the production FPC construction/drawing is selected. This is a cable-definition gate, not an electrical-schematic uncertainty.
