# AudioPicture V2.2 Rev.A — adaptive power governor

Status: **POWER_GOVERNOR_CONTROL_ARCHITECTURE_FROZEN / THRESHOLD_CALIBRATION_AND_HW_VALIDATION_OPEN**

## 1. Objective
Prevent AudioPicture from violating PoE, external-source, PVDD, amplifier and passive-thermal limits while preserving maximum useful audio headroom.

The governor is source-aware and uses measured power rather than a fixed volume cap.

## 2. Inputs
Primary:
- INA228 bus voltage;
- INA228 current;
- INA228 calculated power;
- INA228 die temperature as a local diagnostic only;
- active source: POE / EXT24;
- TAS5825M AMP_FAULT;
- TAS5825M OTW/OTE state where available through control/status;
- 5V_PG;
- 3V3_PG.

Secondary:
- firmware thermal-state estimator;
- radar mode/duty;
- Wi-Fi activity state;
- audio DSP level estimate;
- startup/source-transition state.

SHT45 room-temperature measurement is not used as a MAIN-P junction-temperature proxy.

## 3. INA228 acquisition
Use two software time domains derived from INA228 data.

FAST loop:
- target control update: ~5 ms class;
- low/no averaging;
- detects bus droop and short power excursions;
- does not chase individual Class-D switching cycles.

SLOW loop:
- target update: 100 ms class;
- filtered/averaged power;
- feeds sustained-power and thermal estimator.

A third energy window integrates approximately 1..10 s behavior for thermal/audio duty decisions.

Exact INA228 conversion time/averaging register values remain calibration parameters. The device supports 50 us..4.12 ms conversion times and 1..1024 averaging.

## 4. Governor states
- BOOT_SAFE
- POE_ECO
- EXT_PERFORMANCE
- DERATE_POWER
- DERATE_THERMAL
- FAULT_LATCH
- RECOVERY

BOOT_SAFE:
- AMP_PDN asserted;
- identify source;
- validate rails;
- establish INA228 valid readings;
- release amplifier only after stable power.

## 5. POE ECO thresholds
Ag53024 capability anchor:
- 24 W continuous;
- 30 W peak under manufacturer conditions.

Do not use 30 W as normal operating power.

System baseline:
- 3 W non-audio reservation;
- 2 W engineering margin;
- 15 W sustained audio-domain DC target;
- 19 W short audio-domain ceiling.

Initial total measured-power control targets:
- GREEN: <=18 W total smoothed source power;
- SOFT LIMIT: 18..21 W;
- HARD ECO CONTROL: >=21 W;
- EMERGENCY/FOLD-DOWN: at or below 22.5 W total source power, or abnormal bus droop. Calibration must retain margin for sensing error, actuator latency and stored energy; 23 W sustained is superseded by the frozen 22.5 W application budget.

These are initial firmware calibration thresholds, not production release limits.

Never intentionally regulate at 24 W continuously; retain margin for Ag53024 tolerance, temperature, conversion uncertainty and load steps.

## 6. External 24 V PERFORMANCE thresholds
External adapter recommendation: 24 V / 3 A.

Initial source-power policy:
- allow audio peaks toward amplifier capability;
- normal governor ceiling below adapter 72 W nameplate;
- prioritize PVDD droop, amplifier OTW and thermal model over a simple watt ceiling.

Initial electrical guard:
- begin rapid gain reduction if measured current approaches 2.7 A sustained;
- hard fold-down before 3.0 A sustained;
- exact thresholds depend on source-path drop and adapter tolerance.

Do not promise 2 x 30 W continuous output merely because the adapter is 72 W.

## 7. Gain-control law
Use DSP gain/DRC, not rapid amplifier power-cycling, as the normal actuator.

Priority:
1. prevent clipping/PVDD collapse;
2. obey source power;
3. obey thermal limit;
4. preserve spectral balance.

Initial attack/release concept:
- emergency droop/fault: immediate or single-control-cycle attenuation;
- fast power excess: attack 10..30 ms;
- sustained power: attack 100..300 ms;
- recovery: slow, approximately 2..5 s, with hysteresis.

Avoid audible pumping. Exact constants require listening and load simulation.

## 8. Thermal model
Maintain a first-order estimated hot-state variable driven by measured power and mode.

Inputs:
- smoothed system power;
- amplifier activity;
- elapsed high-power time;
- TAS5825M OTW;
- available board-temperature diagnostics.

Behavior:
- WARN -> reduce allowed sustained audio envelope;
- DERATE -> progressive DSP gain reduction;
- CRITICAL -> AMP_PDN / amplifier shutdown;
- RECOVERY only after temperature/state falls below hysteresis threshold for a defined dwell time.

TAS5825M native OTW/OTE, over-current and UV/OV protection remain independent last-line protections.

## 9. Source transition
### EXT24 -> POE
This is the critical direction.

On loss of external 24 V:
1. immediately enter transition hold;
2. clamp DSP to POE_ECO ceiling before accepting normal playback continuation;
3. verify PoE rail/source valid;
4. reset FAST/SLOW power filters as needed to avoid stale external-mode state;
5. ramp audio to the maximum permitted ECO level.

Do not wait for the PoE module to overload before reducing audio.

### POE -> EXT24
1. detect stable external source;
2. maintain current ECO gain initially;
3. switch source according to break-before-make hardware policy;
4. verify bus stable;
5. enter EXT_PERFORMANCE;
6. release additional headroom slowly.

No audible step-up is required.

## 10. Fault policy
Immediate AMP_PDN or hard mute for:
- TAS5825M hard fault requiring shutdown;
- invalid/unstable main rail;
- repeated source-switch failure;
- persistent severe undervoltage;
- firmware power-monitor sanity failure when safe operation cannot otherwise be guaranteed.

A transient normal power-limit event shall not become a latched fault.

## 11. Measurement sanity
Cross-check:
- INA228 bus voltage against source-state expectations;
- power = V x I within numerical tolerance;
- impossible/stale samples;
- I2C communication timeout.

On INA228 loss:
- POE mode falls back to a conservative fixed ECO DSP ceiling;
- external mode falls back to conservative output plus TAS5825M native protections;
- expose diagnostic fault.

## 12. Home Assistant entities
Expose:
- power_source;
- operating_mode ECO/PERFORMANCE;
- bus_voltage;
- bus_current;
- input_power;
- power_limit_active;
- thermal_derating_active;
- power_headroom estimate;
- amplifier_fault;
- governor_state;
- optional accumulated energy.

User-facing volume remains normal 0..100%. The governor transparently constrains physical output when required.

## 13. Calibration tests
Before production release:
1. PoE full-load sweep at min/nom/max input conditions;
2. music crest-factor sweeps;
3. sine/burst stress;
4. Wi-Fi TX + radar TRACK + voice + audio concurrent load;
5. EXT24 unplug during high-level playback;
6. PoE -> EXT24 insertion;
7. thermal-soak at high ambient;
8. INA228 I2C fault injection;
9. TAS5825M OTW/OTE injection or controlled thermal test;
10. listening test for limiter pumping/artifacts.

Status: **DUAL_LOOP_FAST_SLOW_GOVERNOR_DEFINED / POE_INITIAL_TOTAL_SOFT_HARD_18_21W_EMERGENCY_MAX_22P5W / PRODUCTION_CALIBRATION_OPEN**.


## Rev.EW executed software scope

A portable C control core now exists under `components/power_governor`, with host tests under `tests`. It implements safe startup, independent rail/Type-2 checks, source transitions, bounded gain requests, fault latching and monitor fallback gating. This is not complete ESP-IDF firmware: INA228/TAS5825M drivers, DSP application, dual-loop acquisition/filtering, calibrated thermal estimator, timing integration and hardware tests remain OPEN. All test fixture settings are explicitly synthetic calibration inputs.
