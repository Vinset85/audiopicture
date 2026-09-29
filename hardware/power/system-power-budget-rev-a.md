# AudioPicture V2.2 Rev.A — system power budget

Status: **SYSTEM_POWER_BUDGET_BASELINE_DEFINED / XVF_AUX_RAILS_AND_POE_LOSS_CURVE_RELEASE_GATES_OPEN**

## 1. Purpose
Bound non-audio consumption and define the usable TAS5825M budget in PoE ECO and external-24-V PERFORMANCE modes.

All figures are design allocations unless explicitly identified as manufacturer typical/peak values.

## 2. Manufacturer anchors
- ESP32-S3-WROOM-1: Wi-Fi TX peak up to about 355 mA at 3.3 V under the published 802.11b condition (~1.17 W instantaneous module input).
- W5500: normal-operation supply current 132 mA at 3.3 V (~0.44 W).
- XVF3800: typical core VDD power 345 mW in I2S operation. This is core power only; I/O rails, microphones, regulators and clock/flash require additional allocation.
- BGT60TR13C: sensor share can reach roughly 350–400 mW in CW operation; normal duty-cycled use cases are commonly below 100 mW.
- SHT45: average supply current approximately 0.4 uA.
- OPT3004: operating current approximately 1.8 uA.

## 3. Conservative subsystem allocations

### MAIN-C digital/connectivity
Design continuous allocation:
- ESP32-S3 compute/network average: 0.75 W
- W5500 + crystal: 0.50 W
- miscellaneous logic/status/interface losses: 0.15 W

Subtotal: **1.40 W**

Provide separate transient headroom for Wi-Fi TX peaks even when Ethernet is the primary transport.

### VOICE
Design continuous allocation:
- XVF3800 core anchor: 0.345 W typical
- I/O rails, four PDM microphones, QSPI, clock, regulators and margin: 0.455 W

Subtotal design allocation: **0.80 W**

This is deliberately above the published XVF3800 core-only figure. Exact rail-current closure remains mandatory.

### RADAR
Normal presence-mode allocation: **0.20 W**
Stress/CW allocation: **0.45 W**

Firmware shall use duty-cycled presence operation rather than continuous-wave operation unless a diagnostic mode explicitly requests otherwise.

### ENV
SHT45 + OPT3004 sensor consumption is negligible in the product-level watt budget.
Allocate **0.02 W** including pull-ups/local losses and margin.

### LEDs/service/housekeeping
Allocate **0.08 W**.

## 4. Non-audio load baseline
Normal continuous allocation:
- MAIN-C: 1.40 W
- VOICE: 0.80 W
- RADAR: 0.20 W
- ENV: 0.02 W
- housekeeping: 0.08 W

Total downstream non-audio load: **2.50 W**

Use **3.0 W** as the PoE ECO non-audio design reservation to cover rail-conversion losses and normal variability before exact rail closure.

Use an additional transient reserve for Wi-Fi TX/startup events; do not size the audio limiter from a single instantaneous RF peak.

## 5. PoE ECO budget
Ag53024 architecture limit:
- 24 W continuous isolated output capability.

Reserve:
- 3.0 W non-audio normal design budget;
- 2.0 W system engineering headroom for conversion uncertainty, temperature, transients and control margin.

Initial audio-domain DC-input allowance:
**19 W maximum sustained from the 24 V PoE output budget.**

This is DC input to the audio domain, not acoustic/electrical speaker output.

At 90% Class-D efficiency as a deliberately simple first bound:
- 19 W DC -> approximately 17.1 W total speaker electrical output;
- approximately 8.55 W/channel for equal stereo loading.

For 8-ohm nominal branch load this corresponds to approximately:
- 8.27 Vrms/channel;
- 1.03 Arms/channel.

These are first-order limiter targets only; the mounted DML complex impedance Z(f), LC network, supply conversion losses and thermal model supersede them.

### Recommended first ECO limiter target
Do not release the full 19 W as continuous audio immediately.

Use:
- **15 W sustained audio-domain DC target** as the first firmware/thermal ECO baseline;
- **19 W short-duration ceiling** subject to total-power telemetry and thermal state.

At 90% simple efficiency, 15 W DC corresponds to ~13.5 W total speaker output, or ~6.75 W/channel under equal loading.

This leaves extra practical margin while CFD and Ag53024 efficiency/load data are unresolved.

## 6. External 24 V PERFORMANCE budget
External source recommendation:
- 24 V / 3 A = 72 W source capability.

Subtracting a 3 W non-audio reservation leaves roughly 69 W before source-path and conversion losses.

The TAS5825M 2 x 30 W / 8-ohm electrical capability, rather than the adapter wattage, therefore becomes the principal audio ceiling.

However, passive thermal design is the sustained constraint. Do not map 72 W adapter capability directly to continuous amplifier output.

Initial PERFORMANCE policy:
- permit high short-term peaks toward the TAS5825M electrical envelope;
- constrain long-term average power by MAIN-P temperature/power telemetry;
- progressive DSP derating before hard shutdown.

## 7. Firmware power governor
INA228 shall be the system-level power governor input on MAIN-P.

Inputs:
- source mode: PoE / external 24 V;
- measured 24 V bus voltage/current/power;
- amplifier fault/thermal state;
- optional converter power-good states;
- thermal-model state.

POE ECO:
1. sustained target audio-domain DC <=15 W;
2. short ceiling <=19 W;
3. total source power always takes precedence over nominal volume request;
4. reduce bass first only if psychoacoustic tuning demonstrates it is preferable; otherwise use broadband gain reduction plus DRC.

PERFORMANCE:
1. allow higher transient headroom;
2. use thermal time constants to govern sustained power;
3. preserve clipping margin and avoid uncontrolled PVDD droop.

## 8. Home Assistant diagnostics
Expose at minimum:
- active power source;
- measured bus voltage/current/power;
- ECO/PERFORMANCE mode;
- power-limiter active;
- thermal-derating active;
- amplifier fault;
- optional instantaneous/smoothed audio power estimate.

## 9. Release gates
1. close XVF3800 total rail currents including microphones and regulators;
2. close ESP32/W5500 realistic concurrent average from firmware workload;
3. obtain/encode Ag53024 efficiency vs load and temperature;
4. calculate TPSM63603/TPS62823 conversion losses from actual loads;
5. replace nominal 8-ohm audio math with mounted DML Z(f);
6. couple power governor to CFD/thermal limits;
7. verify PoE startup/transient behavior;
8. verify Wi-Fi TX peaks do not nuisance-trigger audio limiting.

Status: **POE_ECO_15W_SUSTAINED_19W_SHORT_AUDIO_DC_BASELINE / PERFORMANCE_THERMALLY_GOVERNED**.
