# PCB-B VOICE — XVF3800 / SQ66 Rev.A

Status: **implementable architecture baseline**. Exact power passives, boot flash and microphone acoustic mechanics remain subject to XMOS reference-design verification before Gerber release.

## 1. Voice processor
U101: **XVF3800-QF60B-C**.

The device processes four PDM microphones and provides AEC, beamforming, noise suppression, AGC, VAD/DoA functions according to the selected XMOS firmware.

Package/layout shall follow XMOS SQ66/reference hardware rules.

## 2. Microphone array
Rev.A microphone baseline: **4 x Infineon IM69D130** PDM MEMS, or exact SQ66 BOM equivalent after reference-design cross-check.

Geometry is FROZEN:
- square array
- 66 mm x 66 mm
- MIC101..MIC104 at the four corners
- equal acoustic treatment and independent acoustic paths.

XVF3800 MIC_CLK drives all microphones at approximately **3.072 MHz**. MIC_DATA[0..3] return individually to XVF3800.

Microphones must be mechanically isolated from the DML panel. PCB-B mounts to a structural island tied to the outer frame through compliant/elastomer isolation.

## 3. Hardware privacy
Microphone power is a dedicated rail: `+3V3_MIC`.

`+3V3_SYS -> Q101/load switch -> +3V3_MIC -> MIC101..104`

Control: `MIC_HW_EN`.

Requirements:
- OFF physically removes microphone supply.
- default state during reset/boot must be privacy-safe.
- no microphone data shall be considered valid when +3V3_MIC is off.
- privacy indicator shall be logically and, where practical, electrically coherent with actual microphone power state.

Exact load-switch MPN remains VALIDATE.

## 4. I2S host interface
XVF3800 operates as I2S slave.

ESP32-S3 provides:
- `AUD_BCLK` -> XVF3800 I2S_BCLK
- `AUD_LRCLK` -> XVF3800 I2S_LRCK
- `AUD_TX` -> XVF3800 I2S_DATA0 (far-end/AEC reference)
- XVF3800 I2S_DATA1 -> `AUD_RX` (processed microphone audio)

Target system mode:
- 48 kHz host I2S
- 32-bit samples/slots as supported by XVF3800 firmware
- BCLK/LRCLK shared for transmit and receive.

The far-end reference supplied to XVF3800 must correspond to the audio actually sent toward the speaker path and remain time coherent for AEC.

## 5. Audio routing
### VOICE PATH
MIC101..104 PDM
-> XVF3800
-> AEC / beamforming / NS / AGC / VAD / DoA
-> I2S_DATA1
-> ESP32-S3
-> Home Assistant Assist pipeline.

### MEASUREMENT PATH
Room calibration must not use the post-processed voice stream as its measurement source.

The XMOS firmware/configuration shall expose raw or minimally processed individual microphone channels through a supported debug/measurement routing mode. Calibration firmware switches the XVF3800 into MEASUREMENT mode, captures the required raw channels, then restores VOICE mode.

This requirement must be proven with the selected XVF3800 firmware build before production freeze.

## 6. Boot / firmware
Default production strategy: **QSPI boot** local to PCB-B.

U102 external QSPI flash is REQUIRED but exact MPN/capacity remains VALIDATE against:
- current XMOS XVF3800 reference BOM;
- firmware image size;
- update strategy;
- supply availability.

Alternative host-SPI boot is retained only as a recovery/development option, not the normal product boot path unless later validation shows a clear advantage.

## 7. Control interface
Preferred normal control: I2C.

Signals:
- `I2C_SDA`
- `I2C_SCL`
- `VOICE_RST`
- `VOICE_IRQ`
- `MIC_HW_EN`

USB pins/test access may be retained for factory/XMOS debugging but are not part of the normal end-user interface.

## 8. FPC J101
14-pin baseline:
1 +5V_SYS
2 +5V_SYS
3 GND
4 GND
5 AUD_BCLK
6 AUD_LRCLK
7 AUD_TX
8 AUD_RX
9 I2C_SDA
10 I2C_SCL
11 VOICE_RST
12 VOICE_IRQ
13 MIC_HW_EN
14 +3V3_SYS

FPC ground adjacency and signal ordering may change during SI/layout review. Exact connector MPN remains VALIDATE.

## 9. Power
PCB-B receives +5V_SYS and +3V3_SYS.

Do not assume XVF3800 core rails can be powered directly from +3V3_SYS. All XVF3800 internal/core supply rails and sequencing shall reproduce the current XMOS reference design. Local regulators/passives remain VALIDATE until the SQ66 schematic/BOM is transcribed.

Microphones use switched +3V3_MIC subject to final microphone operating-voltage confirmation.

## 10. Acoustic/mechanical rules
- SQ66 center near top-center of product.
- Array plane must remain mechanically stable.
- No microphone port may be directly blocked by frame ribs, adhesive or fabric support.
- Each microphone gets an independent short acoustic path.
- Avoid a common front cavity that acoustically couples microphones.
- Fabric attenuation must be characterized.
- DML vibration transfer to PCB-B must be measured.
- Keep switching power and Class-D output wiring away from microphone data/clock routes.

## 11. Factory test
1. XVF3800 boot/version readback.
2. QSPI integrity.
3. MIC_CLK frequency.
4. individual MIC101..104 activity.
5. microphone sensitivity matching.
6. hardware mute: verify physical loss of microphone signal.
7. processed voice path.
8. AEC reference path.
9. raw four-channel measurement mode.
10. DoA sanity test.

## 12. Release gates
VOICE becomes FROZEN only after:
1. exact SQ66/reference BOM captured;
2. exact PDM microphone MPN/package verified;
3. XVF3800 rail/regulator network verified;
4. QSPI flash MPN/capacity verified;
5. raw 4-mic measurement mode demonstrated;
6. AEC reference latency verified end-to-end;
7. DML vibration isolation test;
8. fabric/acoustic-port validation;
9. EMC test with Class-D and Wi-Fi active.


## Rev.A electrical capture review — 2026-09-29

### XVF3800 rail contract
Per current XMOS XVF3800 documentation:
- VDD core = 0.9 V nominal, all VDD pins connected;
- VDDIOL/VDDIOR/VDDIOT = 3.3 V;
- VDDIOB18 = 1.8 V;
- PLL_AVDD = filtered 0.9 V derived from the core rail;
- USB_VDD18/USB_VDD33 may remain unpowered/floating when XVF3800 USB is not used;
- exposed/package ground paddles connect directly to GND with local vias.

PCB-B therefore requires local regulated **+0V9_VOICE** and **+1V8_VOICE** rails. +3V3_SYS is the I/O rail and microphone-source rail. Exact regulator MPNs/passives remain a capture gate until the current XK-VOICE-SQ66 design files are transcribed.

### QSPI boot contract
Normal production boot remains local QSPI master boot.
Frozen pin behavior:
- QSPI_D1 boot-selection pin is not strapped high for normal boot; it connects to flash D1;
- QSPI_CS_N has external 4.7 kOhm pull-up;
- SPI_CS_N has external 4.7 kOhm pull-up;
- QSPI_D0/D1/D2/D3, CLK and CS route only to the local boot flash with short traces.

XMOS current development-kit documentation identifies **32 Mbit flash storage**. Rev.A capacity baseline is therefore 32 Mbit minimum; exact production flash MPN remains OPEN pending the current SQ66 BOM/design-file transcription.

### Microphone lifecycle correction
**Infineon IM69D130 is not frozen for production.** Infineon currently marks it "not for new design".

Preferred Rev.A replacement candidate:
**Infineon IM72D128V01XTMA1**
- active/preferred product;
- digital PDM;
- 1.62 to 3.60 V;
- 72 dB(A) SNR;
- 128 dBSPL AOP;
- -36 dBFS sensitivity;
- 4.0 x 3.0 x 1.2 mm PG-LLGA-5-3;
- suited to multi-microphone arrays.

The existing 66 x 66 mm acoustic geometry remains frozen. The new microphone footprint/acoustic port must be transcribed from the IM72D128 manufacturer drawing and validated against the front-stack mechanical model.

### Microphone rail/privacy
+3V3_SYS -> hardware load switch -> +3V3_MIC -> four microphones.
Each microphone gets local 100 nF bypass close to VDD.

MIC_HW_EN default OFF is mandatory. The load switch shall include reverse-current/back-power protection appropriate to the final topology; microphone PDM/clock pins must not sustain +3V3_MIC through protection structures when the rail is OFF.

Exact privacy load-switch MPN remains OPEN until reverse-current behavior and output-discharge requirement are verified.

### PDM clock
3.072 MHz remains the nominal high-performance microphone clock target. Final microphone candidate must explicitly support this clock and required duty-cycle tolerance.

### J101 physical update
J101 is now a **16-contact physical interface** using the Hirose FH12 0.5 mm family.
The original 14 logical signals remain unchanged; two additional contacts are GND/reference contacts for improved I2S return paths.
Preferred MAIN mating part is FH12-16S-0.5SH(55). Exact PCB-B mating orientation and physical pin order are frozen only with the FPC cable drawing.

### Measurement-mode gate
Do not mark PCB-B production-ready until the selected XVF3800 firmware build demonstrates access to four raw or minimally processed microphone channels suitable for room impulse/response measurement. Standard processed voice output alone does not satisfy AudioPicture calibration requirements.

### Capture status
Status: **READY_FOR_DETAILED_CAPTURE_AFTER_SQ66_POWER_BOM_TRANSCRIPTION**.

Open electrical gates:
1. exact +0V9_VOICE regulator and passives;
2. exact +1V8_VOICE regulator and passives;
3. exact 32-Mbit-or-larger QSPI flash MPN from validated XMOS-compatible list/reference BOM;
4. exact privacy load switch;
5. IM72D128 footprint/acoustic-port verification;
6. current XK-VOICE-SQ66 schematic/BOM transcription;
7. raw four-channel measurement firmware proof.


## XMOS reference-design verification gate — 2026-09-29

Official XMOS resources verified:
- XK-VOICE-SQ66 Design Files version 1V1, dated 2023-06-28, remain the hardware-reference package;
- current XVF3800 datasheet is the pin/power authority;
- current XVF3800 v3.2.1 firmware documentation is the software/tuning authority.

The design-file ZIP is not transcribed in this repository yet. Therefore **do not infer regulator or flash MPNs from generic xcore.ai designs**.

### Frozen XVF3800 supply pin groups
Native capture must implement:
- VDD pins 4,12,19,27,34,42,49,57 and core paddles 61..64 -> +0V9_VOICE;
- V_DDIOL pin 8 -> +3V3_SYS;
- V_DDIOR pin 38 -> +3V3_SYS;
- V_DDIOT pin 52 -> +3V3_SYS;
- VDD_IOB18 pins 17,26 -> +1V8_VOICE;
- PLL_AVDD pin 22 -> filtered +0V9_VOICE;
- VSS paddle pin 65 -> GND with direct local via strategy;
- USB_VDD18 pin 31 and USB_VDD33 pin 30 are not populated/powered in AudioPicture Rev.A unless XVF3800 USB is later enabled.

All package paddles 61..65 must be electrically and thermally implemented exactly as required by XMOS.

### Frozen boot pins
- pin 1 QSPI_D1: connect to boot-flash D1; no boot-mode pull-up in normal product mode;
- pin 2 QSPI_D3 -> flash D3;
- pin 3 QSPI_CS_N -> flash CS_N plus 4.7 kOhm external pull-up;
- pin 5 QSPI_CLK -> flash CLK;
- pin 6 SPI_CS_N -> 4.7 kOhm external pull-up;
- remaining QSPI data pins are captured from the current XVF3800 pin table and SQ66 design files, not guessed.

### Firmware/acoustic geometry
The XMOS v3.2.1 square/rectangular geometry example uses microphone coordinates at +/-33.3 mm in X/Y, corresponding to approximately 66.6 mm corner spacing. AudioPicture's nominal 66 mm square array is therefore retained as the firmware-coordinate baseline; final as-built coordinates shall be entered in mic_geometries.yaml from PCB/mechanical CAD.

### Production firmware requirement
The production XVF3800 firmware must be rebuilt/tuned for AudioPicture rather than using an unmodified evaluation-kit binary. At minimum the product configuration must reflect:
- exact microphone coordinates;
- DML loudspeaker/AEC reference behavior;
- microphone gain/sensitivity;
- AudioPicture I2S routing;
- raw/minimally processed measurement mode requirement.

### Remaining SQ66 transcription gate
Before marking PCB-B READY_FOR_NATIVE_KICAD_CAPTURE, obtain and inspect the official XK-VOICE-SQ66 Design Files 1V1 and record:
1. +0V9 regulator exact MPN, feedback/passives and sequencing;
2. +1V8 regulator exact MPN, feedback/passives and sequencing;
3. boot QSPI flash exact MPN/capacity/decoupling;
4. reset/clock/support networks and decoupling values;
5. any power-good/sequencing constraints not explicit in the XVF3800 datasheet.

Until that transcription is complete these MPNs remain OPEN, not guessed.


## Microphone privacy / PDM electrical freeze — 2026-09-29

### Production microphone baseline
MIC101..MIC104 = **Infineon IM72D128V01XTMA1**.

Electrical capture baseline:
- VDD = +3V3_MIC;
- operating supply range supports 3.3 V;
- PDM clock target = 3.072 MHz;
- maximum microphone supply current at 3.072 MHz is approximately 1.12 mA per microphone per manufacturer data;
- provide 100 nF X7R local bypass at each microphone;
- preserve manufacturer acoustic-port/land-pattern keep-out exactly.

Status: **FROZEN_DEVICE / FOOTPRINT_ACOUSTIC_VERIFY**.

### Hardware privacy load switch
Q101 = **Texas Instruments TPS22913C** family baseline.

Required characteristics used by AudioPicture:
- 1.4 to 5.5 V input range;
- low-Ron load switch;
- full-time reverse-current protection;
- controlled turn-on;
- quick output discharge;
- active-high ON compatible with MIC_HW_EN.

Connections:
- IN -> +3V3_SYS;
- OUT -> +3V3_MIC;
- ON -> MIC_HW_EN;
- GND -> GND.

MAIN already owns a 100 kOhm pull-down on MIC_HW_EN. PCB-B shall not add a conflicting pull-up. A local weak pull-down may be DNP-only unless sequencing analysis proves it necessary.

The exact TPS22913C orderable suffix/package is a footprint/manufacturing gate. Do not substitute TPS22930 without re-review: its reverse-current protection behavior is weaker for this privacy use case.

### Privacy-off signal isolation
Power removal alone is not sufficient if digital pins can parasitically power the microphone rail.

Therefore native capture/layout shall include optional small series-resistor footprints on each microphone CLOCK/DATA path close to the powered source/device boundary. Populate only after signal-integrity and power-off injection analysis.

Acceptance condition:
- with MIC_HW_EN low, +3V3_MIC discharges through Q101 QOD;
- no microphone is powered through CLOCK/DATA protection structures;
- no valid PDM stream is available;
- factory privacy test measures the physical rail state.

### PDM topology
MIC_CLK from XVF3800 fans out to all four microphones.
Use a star/controlled short-branch topology from the processor region; avoid long daisy-chain stubs.
Provide source damping footprint at MIC_CLK driver, initial DNP/0-ohm capture baseline, tune by edge/SI measurement.

MIC_DATA0..3 are independent returns to XVF3800; do not wire-OR microphone data in Rev.A.

Keep PDM traces referenced to continuous GND and away from DML/Class-D switching nodes.

### Current budget
Four microphones at the manufacturer 3.072 MHz maximum-current figure consume approximately 4.48 mA total before margin. Design +3V3_MIC for at least 20 mA continuous allocation to include startup, tolerance and engineering margin; the TPS22913C current capability is therefore far above the microphone load and is selected for isolation/privacy behavior rather than ampacity.


## XVF3800 local support network capture contract — 2026-09-29

### Decoupling ownership
All XVF3800 supply domains receive local high-frequency ceramic decoupling at the device. Native capture shall place a dedicated 100 nF-class MLCC at each practical supply-pin group, with the smallest loop to the ground paddle/plane.

Bulk/domain capacitance and any ferrite/RC values shall be transcribed from the official XK-VOICE-SQ66 1V1 design files before production freeze. Do not consolidate all local bypass capacitors into a distant bulk capacitor.

Domains:
- +0V9_VOICE core;
- +0V9_PLL after the XMOS-reference PLL filter;
- +1V8_VOICE;
- +3V3_SYS I/O;
- +3V3_MIC switched microphone domain.

### PLL rail
PLL_AVDD is not connected directly to a noisy shared rail. It is derived from +0V9_VOICE through the filtering topology specified by XMOS/reference design and receives dedicated local decoupling.

Exact filter component values remain **OPEN_REFERENCE_TRANSCRIPTION** until XK-VOICE-SQ66 1V1 is inspected.

### Reset
VOICE_RST from MAIN controls the XVF3800 reset path.
MAIN provides the system-safe reset ownership. PCB-B shall not add a pull network that fights MAIN.

Native capture must preserve any XMOS-required reset conditioning/supervisor topology from the SQ66 reference design. Firmware release of reset is allowed only after +0V9_VOICE, +1V8_VOICE and +3V3_SYS are valid and the local boot flash is powered.

### Boot flash power
U102 QSPI flash is powered from the voltage domain required by the exact XMOS SQ66 reference BOM/selected flash. Do not assume +3V3_SYS until the production flash is frozen.

QSPI routing rules:
- flash adjacent to XVF3800;
- CLK shortest/highest-priority trace;
- no test-pad stubs on CLK/data;
- continuous GND reference;
- CS pull-up physically local;
- optional source damping only if supported by SI/edge-rate validation.

### Clocking
Do not add an arbitrary external oscillator to XVF3800 merely to satisfy schematic completeness.
The system clock/PLL implementation shall be transcribed from the current XMOS SQ66 reference design and firmware requirements.

MIC_CLK nominal target remains 3.072 MHz and is generated/controlled by the XVF3800 firmware/hardware configuration.

### Power sequencing
Rev.A sequencing requirement:
1. MAIN +3V3_SYS/+5V_SYS become valid;
2. PCB-B local +0V9_VOICE/+1V8_VOICE regulators become valid;
3. QSPI flash supply is valid;
4. VOICE_RST may be released;
5. XVF3800 boots and exposes control/status;
6. MIC_HW_EN remains OFF until privacy state and voice firmware are initialized;
7. +3V3_MIC is enabled only on explicit product state.

Brownout/reset shall return the microphone domain to OFF through the MAIN hardware pull-down on MIC_HW_EN.

### Capture gate summary
The following are deliberately NOT guessed:
- exact +0V9 regulator;
- exact +1V8 regulator;
- regulator feedback/compensation/passives;
- PLL filter values;
- exact QSPI flash MPN and its supply voltage;
- any external reference-clock component;
- reference-specific reset supervisor/RC.

These six items must come from the official XK-VOICE-SQ66 1V1 package or a later XMOS design authority before PCB-B can be marked READY_FOR_NATIVE_KICAD_CAPTURE.
