# TAS5825M + DML Rev.A

Status: **implementable schematic baseline**, subject to PCB/EMC/acoustic validation before fabrication.

## 1. Amplifier
U9: **TAS5825MRHBR**, stereo closed-loop Class-D DSP amplifier, RHB VQFN-32.

Operating target:
- PVDD = `+24V_SYS`
- stereo BTL / 2.0 mode
- nominal load = 8 ohm/channel
- system sample rate = 48 kHz
- external 24 V mode: PERFORMANCE profile
- PoE mode: ECO profile with power-aware DSP limiting.

At 24 V / 8 ohm TI specifies approximately 2 x 30 W at 1% THD+N. The AudioPicture limit may be lower after DML thermal/excursion characterization.

## 2. DML topology
Four **Dayton Audio DAEX25FHE-4** exciters, each nominally 4 ohm.

LEFT:
OUT_A/OUT_B BTL -> EX1 -> EX2 -> return, series pair = nominal 8 ohm.

RIGHT:
OUT_C/OUT_D BTL -> EX3 -> EX4 -> return, series pair = nominal 8 ohm.

Do not parallel the 4-ohm exciters in Rev.A.

Connector J3 = LEFT DML pair.
Connector J4 = RIGHT DML pair.

Speaker wiring and connector current rating shall support >=3 A peak with margin.

## 3. Power
PVDD = +24V_SYS.

Required local decoupling per TI:
- bulk low-ESR capacitance >22 uF at the amplifier;
- 1 uF and/or 100 nF high-frequency ceramic capacitors placed immediately at PVDD pins.

AudioPicture baseline:
- C901: 470 uF / 35 V low-ESR electrolytic/polymer, VALIDATE height/ESR/ripple
- C902: 22 uF / 35 V X7R, VALIDATE effective capacitance
- local PVDD groups: 1 uF + 100 nF X7R at the relevant supply pins.

Final bulk may increase toward 1000 uF only after PoE startup/inrush and mechanical-height validation.

## 4. Bootstrap
TI requires one **0.47 uF** bootstrap capacitor from every OUT_X node to corresponding BST_X.

C_BSTA = 0.47 uF
C_BSTB = 0.47 uF
C_BSTC = 0.47 uF
C_BSTD = 0.47 uF

Use X7R/X5R ceramic with voltage rating and package consistent with TI reference design; place directly at device pins.

## 5. Digital audio
ESP32-S3 -> TAS5825M:
- `AUD_BCLK` -> BCLK
- `AUD_LRCLK` -> FSYNC/LRCLK
- `AUD_TX` -> SDIN

No MCLK required for the intended 3-wire digital audio interface.

Baseline format:
- I2S
- 48 kHz
- 32-bit slots
- stereo.

Series damping resistor footprints (initial 22–33 ohm, DNP/adjustable after SI measurement) shall be provided at the source side of BCLK/LRCLK/SDIN.

SDOUT shall be routed to an accessible test/expansion point for future monitoring/AEC/debug use.

## 6. Control
I2C:
- `I2C_SDA`
- `I2C_SCL`

Control/status:
- `AMP_PDN`
- `AMP_FAULT`

Pull states must guarantee amplifier shutdown/mute while MCU is in reset or rails are unstable.

Firmware sequence:
1. establish rails;
2. hold amplifier in shutdown;
3. configure clocks/I2S;
4. load verified TAS5825M DSP profile;
5. clear/check faults;
6. enable output;
7. ramp volume without pop.

On brownout, clock loss, OTA/reboot or critical power fault: mute/disable amplifier before uncontrolled audio can occur.

## 7. Output EMI filter
Rev.A shall use a **real LC output filter**, not ferrite-bead-only filtering, as the default production topology.

Reason:
- up to ~30 W/channel electrical capability;
- long internal DML wiring;
- large radiating panel;
- Wi-Fi/BLE, Ethernet, four microphones and 60 GHz radar coexist in a thin enclosure;
- EMC margin is more important than saving a few components.

Starting electrical target for each BTL output leg:
- L = **10 uH** power inductor
- C differential/network baseline derived from TI reference design, initial **0.68 uF class** where applicable.

Exact topology and capacitor placement must be copied/derived from TI TIDA-060026/TAS5825M reference design and then simulated for the AudioPicture 8-ohm DML load. Do not freeze generic LC values without checking BTL topology, Q and DML impedance.

Inductor requirements:
- low DCR
- saturation/current rating with margin above expected peak current
- shielded construction preferred
- height compatible with 40 mm total product depth.

Output filter status: **VALIDATE_EMC_LOAD**.

## 8. Protection and DSP
Use TAS5825M integrated protections plus AudioPicture software/DSP constraints:
- overcurrent/short protection
- overtemperature warning/shutdown
- UVLO/OVLO
- DRC/AGL
- DML excursion protection model
- DML thermal model
- power-source-aware limiter.

Profiles:
### POWER_PROFILE_POE
INA228 power feedback constrains amplifier demand to maintain PoE rail stability and logic reserve.

### POWER_PROFILE_EXT
Higher headroom with external 24 V / 3 A input, still bounded by DML excursion/thermal model.

No production maximum level shall be frozen before acoustic/thermal characterization of the DML panel.

## 9. DML physical baseline
Panel target approximately 300 x 380 mm.

Initial simulation coordinates, panel origin reference:
- EX1 = (75,105) mm
- EX2 = (225,105) mm
- EX3 = (75,275) mm
- EX4 = (225,275) mm

These coordinates are **NOT production frozen**. Modal/FEA optimization has authority over them.

Exciter wiring must not mechanically preload the DML panel.

## 10. Layout
- Keep PVDD decoupling loops extremely short.
- Keep each H-bridge/output-filter current loop compact.
- Use continuous ground plane.
- Exposed PowerPAD connected to a large ground copper region with thermal-via array.
- Do not place TAS5825M at the PCB edge if avoidable.
- Keep switching outputs/filter physically away from VOICE FPC and environmental sensor routing.
- Route I2S over uninterrupted reference plane.
- Do not route sensitive traces through Class-D switching-current return paths.
- Keep left/right filter networks symmetric.

## 11. Test points
Required:
- TP_PVDD_AUDIO
- TP_AMP_3V3/control rail as applicable
- TP_BCLK
- TP_LRCLK
- TP_SDIN
- TP_SDOUT
- TP_AMP_PDN
- TP_AMP_FAULT

Do not expose raw Class-D switching outputs on casual service pads; use controlled factory measurement points if required.

## 12. Factory audio test
1. amplifier identity/config readback;
2. fault-state test;
3. low-level sine output;
4. each DML pair continuity/impedance sanity;
5. microphone-captured sweep;
6. channel polarity/correlation check;
7. distortion/noise screening;
8. write factory DML baseline data.

## 13. Release gates
Before AUDIO becomes FROZEN:
1. exact LC filter MPNs and SPICE/transfer response;
2. DML panel impedance measurement/model;
3. TAS5825M thermal simulation at external-power worst case;
4. PoE power-limit test;
5. EMC pre-compliance;
6. DML modal/FEA analysis;
7. acoustic sweep/distortion validation;
8. final Smart Amp thermal/excursion model.
