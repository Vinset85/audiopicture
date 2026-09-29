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


## Datasheet/reference freeze review — 2026-09-29

### TAS5825M production device
U_AUDIO = **TAS5825MRHBR**
- RHB VQFN-32, 5 x 5 mm;
- PVDD operating range up to 26.4 V;
- 2.0 mode supports approximately 2 x 30 W into 8 ohm at 24 V / 1% THD+N under TI test conditions;
- 3-wire digital audio supported without MCLK;
- SDOUT retained for monitoring/AEC/debug.

Status: **FROZEN_DEVICE_PACKAGE_MODE**.

### Bootstrap network
Per TI datasheet:
- BST_A to OUT_A = **0.47 uF**
- BST_B to OUT_B = **0.47 uF**
- BST_C to OUT_C = **0.47 uF**
- BST_D to OUT_D = **0.47 uF**

Use low-ESR ceramic and place immediately at the corresponding pins.

Status: **FROZEN_VALUE_TOPOLOGY**.

### PVDD decoupling
TI requires good low-ESL/low-ESR supply decoupling larger than 22 uF close to the amplifier.

AudioPicture Rev.A capture:
- C_AUDIO_BULK = **470 uF / 35 V low-ESR** baseline;
- C_AUDIO_MID = **22 uF / 35 V ceramic** nominal, effective capacitance under 24-26 V bias to be verified;
- local **1 uF + 100 nF** ceramic groups at PVDD supply pins/reference placement.

470 uF remains a system-level baseline, not an instruction to increase capacitance arbitrarily: PoE startup, source handover and inrush remain authority.

### Digital audio
Capture baseline remains:
- 48 kHz;
- I2S;
- 32-bit slots;
- ESP32 owns BCLK/LRCLK;
- AUD_TX -> TAS5825M SDIN;
- SDOUT -> test/expansion/AEC path.

Source-side damping footprints:
- BCLK 22 ohm default;
- LRCLK 22 ohm default;
- SDIN 22 ohm default;
- tune 0/22/33 ohm after SI validation.

### Amplifier safe state
AMP_PDN hardware pull-down on Sheet 04 has authority: amplifier remains disabled while ESP32 is reset/unpowered.

AMP_FAULT is an input to ESP32. Pull-up ownership and exact electrical implementation shall follow the TAS5825M pin behavior/reference circuit; avoid duplicate pull owners.

### DML electrical topology
Each channel remains one series pair of DAEX25FHE-4 exciters:
- LEFT = EX1 + EX2 series;
- RIGHT = EX3 + EX4 series;
- nominal channel load = 8 ohm.

The series midpoint is not tied to ground and is not a service-ground reference.

Use polarized/keyed channel connectors or unambiguous harness marking so factory assembly preserves BTL polarity.

### LC output filter
TI reference/EVM material demonstrates a **10 uH + 0.68 uF-class** LC implementation for TAS5825M.

Rev.A capture baseline:
- four inductors, one in each BTL leg: **10 uH**;
- capacitor network: **0.68 uF class starting value/reference topology**;
- all four legs/layout symmetric.

However, exact capacitor topology/value and inductor MPN remain **NOT PRODUCTION FROZEN** because AudioPicture does not drive a simple resistive 8-ohm loudspeaker. The two-exciter DML branch plus panel has frequency-dependent impedance and electromechanical resonances.

Production freeze requires:
1. electrical impedance model/measurement of one complete two-exciter series branch mounted on the final panel;
2. SPICE/AC analysis of LC + measured/modelled load;
3. check filter Q/peaking and phase through the audio band;
4. Class-D stability/EMC review;
5. thermal/current validation of each 10 uH inductor.

Do not increase C blindly: output capacitance affects idle current and amplifier behavior.

### Output-current sizing
At the TI 2 x 30 W / 8-ohm reference point:
- load current ~= 1.94 Arms per channel;
- sinusoidal peak ~= 2.74 A.

Therefore each LC inductor and speaker connector/harness shall be designed for at least **3 A peak** with additional saturation/thermal margin. Inductor target Isat >=4 A is preferred pending filter simulation.

### Sheet-05 capture status
Status: **READY_FOR_NATIVE_KICAD_CAPTURE_WITH_LC_DML_RELEASE_GATE**.

Native schematic capture may proceed using the reference 10 uH / 0.68 uF-class filter placeholders and explicit NOT-FROZEN notes.

Gerber/production release remains blocked by:
- exact LC topology/MPNs after DML impedance model;
- exact PVDD ceramic/bulk MPNs and inrush check;
- thermal simulation of TAS5825M exposed pad/PCB;
- EMC validation;
- DML panel modal/acoustic validation;
- final Smart Amp protection model.


## Output-inductor production candidate — 2026-09-29

The first production-qualified candidate for each of the four 10 uH BTL output inductors is:

**Coilcraft XAL7050-103MEC**
- L = 10 uH +/-20%;
- shielded molded construction;
- DCR = 25 mOhm typ / 29 mOhm max;
- Isat = 12.1 A typ at 30% inductance drop;
- Irms = 6.3 A for 20 C rise / 8.5 A for 40 C rise under Coilcraft reference conditions;
- body family envelope approximately 8.0 x 7.7 x 5.0 mm;
- manufacturer provides datasheet, loss-analysis resources and 3D model.

This candidate has substantially more saturation-current margin than the >=5 A project gate and is preferred over the lower-profile XAL7030-103 for thermal/DCR reasons. XAL7030-103 remains an alternate mechanical corner only: although about 3.1 mm high and Isat 12 A, its DCR is 60.4 mOhm typ and its 20 C-rise Irms is only 2.6 A.

Release conditions remain:
1. evaluate Coilcraft core/copper loss at the TAS5825M switching waveform/frequency and actual audio current distribution;
2. verify PCB thermal rise in the sealed 40 mm enclosure;
3. co-simulate the complete LC network with mounted DML complex Z(f);
4. EMC test/simulation;
5. import and cross-check the manufacturer 3D model.

Status: **OUTPUT_INDUCTOR_CANDIDATE_XAL7050_103_SELECTED / LC_AND_THERMAL_RELEASE_GATES_REMAIN**.
