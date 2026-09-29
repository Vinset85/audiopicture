# AudioPicture V2.2 Rev.A — passive system thermal budget

Status: **PASSIVE_THERMAL_ARCHITECTURE_BASELINE_DEFINED / CFD_AND_BOARD_THERMAL_SOLVE_REQUIRED**

## 1. Objective
Establish a first-order thermal budget for the sealed/fanless 320 x 400 x 40 mm product before detailed CFD.

This is not a junction-temperature signoff. Published efficiencies are used only to bound dissipation.

## 2. Operating modes

### POE ECO
Ag53024 continuous application power is limited to 24 W output capability by the selected PoE module architecture.

Firmware/DSP shall enforce an ECO power envelope so the complete product remains inside the available PoE and thermal budget.

Do not interpret TAS5825M electrical maximum output capability as simultaneously available under PoE.

### EXTERNAL-24V PERFORMANCE
External source baseline is 24 V / 3 A.

This permits substantially higher instantaneous audio power than PoE, but passive thermal limits still apply.

The product shall use DSP limiting, temperature telemetry and time-dependent derating rather than allowing indefinite worst-case sine-wave dissipation.

## 3. Primary heat sources

### TAS5825M
TI specifies >90% Class-D power efficiency and 2 x 30 W into 8 ohm at 24 V / 1% THD+N under published conditions.

First-order extreme continuous sine bound:
- audio output = 60 W;
- at 90% efficiency, DC input ≈66.7 W;
- amplifier-stage loss ≈6.7 W.

This is a stress bound, not a target continuous product operating condition.

Normal music has substantially lower long-term average power than a full-scale continuous sine, but the release model shall use explicit crest-factor/duty-cycle cases rather than assuming a generic music factor.

### TPSM63603
TI publishes approximately 91% efficiency for 24 V input, 5 V output, 2.5 A, 1 MHz under the stated conditions.

At 12.5 W output:
- input ≈13.74 W;
- module/conversion loss ≈1.24 W.

Actual AudioPicture 5 V load must be calculated from MAIN-C, VOICE, RADAR and auxiliary loads.

### Back-to-back input MOSFETs
ISC035N10NM5LF2 has milliohm-class RDS(on). At the AudioPicture 3 A external-source design current, pure conduction loss is small compared with amplifier/converter losses, but transient linear-mode and hot-swap SOA remain separate release gates.

### Ag53024
Treat module dissipation as a MAIN-C thermal source using the exact efficiency/load curve from the manufacturer during detailed thermal solve.

Do not place ENV thermal sensing in its conductive/convective plume.

## 4. First thermal design envelopes

Use these engineering cases for CFD/thermal simulation:

A. IDLE/VOICE
- network active;
- voice/radar/environment active;
- audio idle/low level.

B. POE ECO CONTINUOUS
- total PoE load limited below the Ag53024 continuous capability with engineering margin;
- sustained representative audio + compute load;
- hottest allowed ambient case.

C. EXTERNAL MUSIC
- 24 V external source;
- realistic high-level music crest factor/duty cycle;
- all subsystems active.

D. EXTERNAL SINE STRESS
- worst-case laboratory audio loading approaching 2 x 30 W;
- transient/limited duration;
- used to validate protection and thermal derating, not indefinite user operation.

## 5. Mechanical heat paths
No fan.

Preferred heat path:
IC/package -> PCB copper/vias -> local spreader area -> rear structural frame / rear-shell internal air and radiation -> external rear shell / room air.

Do not use the DML active panel as the primary heatsink because thermal coupling and rigid attachments can disturb acoustic boundary conditions.

PC-CF and ASA are not treated as metal heatsinks. Their low thermal conductivity relative to aluminum means PCB spreading area and natural convection/radiation remain important.

Do not add an internal metal plate across the radar RF cone or ESP32 antenna zone.

## 6. Board-specific thermal zoning

### MAIN-P
Primary hot regions:
- TAS5825M exposed-pad region;
- four output inductors;
- TPSM63603;
- input protection during abnormal/hot-swap events.

Rules:
- large continuous GND/thermal copper around TAS5825M where electrically valid;
- dense thermal-via field under exposed pad per TI guidance;
- keep 470 uF electrolytic away from the hottest TAS5825M/inductor zone;
- keep speaker harness from blanketing hot copper;
- reserve rear-shell air gap above heat-spreading regions.

### MAIN-C
Primary hot region:
- Ag53024;
- secondary W5500/logic contribution.

Rules:
- isolate Ag53024 thermally from ESP32 antenna region and ENV path;
- preserve natural-convection cavity where orientation permits;
- no thermally conductive bridge from Ag53024 to SHT45 chamber.

## 7. Temperature telemetry and control
Use available internal telemetry where trustworthy:
- TAS5825M protection/diagnostics;
- system current/power from INA228;
- board/sensor temperatures only when their thermal location is understood.

Do not use SHT45 room-temperature measurement as a MAIN-P junction proxy.

Firmware thermal policy shall support:
1. warning threshold;
2. progressive DSP power/volume derating;
3. hard amplifier shutdown if required;
4. hysteretic recovery;
5. Home Assistant diagnostic entity/event.

Exact thresholds remain open until CFD and junction models are solved.

## 8. Preliminary dissipation targets
For passive enclosure design, target sustained electronics heat materially below the 6.7 W amplifier-only full-sine bound.

The detailed CFD shall sweep at least:
- 3 W internal dissipation;
- 5 W;
- 8 W;
- 10 W;
with spatially realistic source placement rather than a single uniform heat source.

This sweep determines whether rear-shell geometry requires hidden convection slots/chimneys or a thermally improved local spreader.

## 9. Enclosure airflow
Maintain the product's hidden aesthetic.

Evaluate:
- bottom-edge hidden intake micro-slots;
- top-edge hidden exhaust micro-slots;
- internal vertical chimney paths that do not acoustically short front/rear DML radiation;
- dust/light ingress control;
- no direct opening that compromises microphone acoustic design.

Passive vents are preferred over a fan if CFD demonstrates a meaningful benefit.

## 10. Release gates
1. obtain Ag53024 loss/efficiency versus load;
2. calculate actual 5 V and 3.3 V subsystem loads;
3. calculate TAS5825M dissipation for ECO and PERFORMANCE limiter profiles;
4. model XAL7050 copper/core loss;
5. perform PCB-level thermal solve for MAIN-P;
6. perform enclosure natural-convection/radiation CFD;
7. sweep ambient temperature;
8. verify electrolytic lifetime at local temperature;
9. define firmware thermal limiter thresholds;
10. verify thermal changes do not degrade DML, VOICE, RADAR or ENV performance.

Status: **PASSIVE_THERMAL_ARCHITECTURE_BASELINE_DEFINED / CFD_AND_BOARD_THERMAL_SOLVE_REQUIRED**.
