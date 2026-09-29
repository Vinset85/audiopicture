# AudioPicture V2.2 Rev.A — BGT60TR13C RADAR power tree and duty-cycle budget

Status: **RADAR_BURST_SLEEP_POWER_ARCHITECTURE_DEFINED / FINAL_PRESENCE_FRAME_DUTY_CYCLE_RELEASE_GATE**

## 1. Purpose
Close the first quantitative power model for PCB-C RADAR and reconcile the system-level 0.20 W normal allocation with the BGT60TR13C active current.

## 2. Manufacturer current anchors
For VDD domains other than LF at 1.71..1.89 V, Infineon specifies approximately:
- Deep Sleep: 0.12 mA typical, 0.555 mA max;
- Idle: 2.8 mA typical, 5 mA max;
- Init0 3Rx+1Tx: 175 mA typical, 205 mA max;
- Init1 3Rx+1Tx: 185 mA typical, 215 mA max;
- Active 3Rx+1Tx: 201 mA typical, 230 mA max.

At 1.8 V:
- active typical sensor power ≈0.362 W;
- active maximum bound ≈0.414 W at 1.8 V, or ≈0.435 W using the 1.89 V upper supply bound.

Therefore the existing 0.45 W RADAR stress allocation is retained.

## 3. Clock
Use the frozen 80 MHz system-reference clock.

Infineon permits the relevant reference-frequency range around 80 MHz and specifies a 1.8 V CMOS clock.

Do not revert to the superseded 38.4 MHz architecture.

## 4. Rail architecture
BGT60TR13C:
- primary listed VDD domains: 1.8 V;
- VDDLF: 3.3 V per AudioPicture audited architecture.

Baseline:
- NCP167AMX180TBG for clean 1.8 V radar supply;
- local 3.3 V filtering for VDDLF as defined by the audited radar schematic contract;
- close local decoupling per Infineon placement guidance.

Final regulator loss requires exact upstream voltage and frame duty cycle.

## 5. Level translation
Use 2 x SN74AXC4T245BQBRG4 as already selected.

Reasons retained:
- dual configurable rails cover 1.8 V <-> 3.3 V;
- VCC isolation drives outputs high-impedance when either supply collapses;
- Ioff supports partial-power-down behavior;
- static supply current is negligible compared with radar burst power.

Hardware rule:
- output-enable state shall default to high impedance while the 1.8 V radar rail is absent or unstable;
- no ESP32 GPIO shall back-power the radar domain.

## 6. Duty-cycle model
The 0.20 W system reservation is an **average normal-mode allocation**, not the BGT60TR13C active-state power.

Let:
- P_ACTIVE = 0.362 W typical sensor-only active anchor;
- P_SLEEP ≈ negligible at product-watt scale;
- D = active radar duty fraction.

Sensor-only average approximately:
P_RADAR_SENSOR_AVG ≈ D * P_ACTIVE + (1-D) * P_SLEEP.

Examples:
- D=25% -> ~0.091 W sensor average;
- D=40% -> ~0.145 W;
- D=50% -> ~0.181 W.

This leaves the remainder of the 0.20 W normal reservation for oscillator, translators and regulator loss only at moderate duty cycle.

Therefore:
**normal firmware target: radar active duty cycle <=40% unless measured board power proves additional margin.**

This is a power target, not yet the sensing-performance optimum.

## 7. Presence algorithm power states
Define:
- RADAR_DEEP_SLEEP: sensor reset/low-power state when allowed;
- RADAR_PRESENCE_LOW: low-duty presence scan;
- RADAR_TRACK: temporarily elevated frame rate after motion/presence evidence;
- RADAR_DIAGNOSTIC: high-duty/CW engineering mode, time-limited.

The product shall normally alternate burst acquisition and low-power intervals.

Do not operate permanent CW merely to simplify firmware.

## 8. Adaptive duty cycle
Recommended control policy:
1. empty room -> low duty;
2. weak/ambiguous target -> temporarily raise frame rate;
3. confirmed stationary presence -> choose the minimum frame rate that maintains confidence;
4. rapid motion -> TRACK mode;
5. prolonged inactivity -> return to low duty.

This improves both PoE budget and local PCB-C temperature.

## 9. Thermal consequence
At <=40% typical active duty, sensor-only average dissipation is around 0.15 W before auxiliary losses.

At diagnostic/high-duty operation, budget up to 0.45 W for the radar block.

PCB-C is therefore not expected to dominate system thermal load, but RF calibration and antenna/radome temperature sensitivity still require thermal evaluation.

## 10. System power-budget consequence
Retain:
- RADAR normal allocation: **0.20 W**;
- RADAR stress allocation: **0.45 W**.

No change is required to the existing 3.0 W PoE non-audio reservation.

## 11. Release gates
1. define final chirp/frame configuration for stationary-presence performance;
2. derive exact RF active time per frame;
3. calculate oscillator current;
4. calculate NCP167 losses from real upstream rail;
5. calculate translators' dynamic switching power;
6. verify <=40% normal duty does not compromise stationary-human detection;
7. verify radar warm-up/reacquisition latency;
8. validate RF performance through final fabric/radome stack;
9. measure/simulate complete PCB-C average and peak power.

Status: **RADAR_0P20W_NORMAL_0P45W_STRESS_RETAINED / NORMAL_ACTIVE_DUTY_TARGET_LE_40_PERCENT**.
