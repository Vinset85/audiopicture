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
