# Sheet 03 — Power Monitor / 5 V / 3.3 V Rails Rev.A

Status: **implementable schematic specification**. Exact shunt MPN, 5 V/3.3 V output passives and thermal layout remain subject to final calculation/reference-layout validation.

## 1. Power tree
Input from Sheet 02:
`+24V_RAW`

Main monitored path:
`+24V_RAW -> RSH1 -> +24V_SYS`

Loads:
- +24V_SYS -> TAS5825M audio power
- +24V_SYS -> TPSM63603V5 -> +5V_SYS
- +5V_SYS -> TPS62823 -> +3V3_SYS

INA228 measures the total post-ORing system current consumed from +24V_RAW.

## 2. Current shunt
RSH1:
- 10 mOhm
- 4-terminal/Kelvin
- >=0.5 W
- <=1% tolerance; lower TCR preferred.

Candidate family: Vishay WSK2512 or qualified equivalent.

At 3 A:
- Vshunt = 30 mV
- Pshunt = 90 mW.

At 4 A transient:
- Vshunt = 40 mV
- Pshunt = 160 mW.

This fits the planned INA228 high-sensitivity shunt range with little margin at 4 A; firmware/analog range selection must therefore be verified against actual peak current before freeze.

## 3. INA228
U7: **INA228AIDGSR**.

Connections:
- IN+ Kelvin directly to source side of RSH1.
- IN- Kelvin directly to load side of RSH1.
- VBUS sense = +24V_SYS/load-side voltage as selected by schematic implementation.
- VS = +3V3_SYS.
- I2C = I2C_SDA / I2C_SCL.
- ALERT = POWER_ALERT.

Functions exposed:
- bus voltage
- shunt voltage
- current
- power
- energy
- charge
- die temperature/diagnostics as supported.

Use the high-sensitivity ±40.96 mV shunt range when validated for actual current envelope.

## 4. INA228 input filtering
Provide symmetric input-filter footprints directly at INA228:
- small series resistors in each Kelvin sense input;
- differential capacitor across IN+/IN-;
- values initially DNP/reference-derived and finalized from TI recommendations versus conversion timing/noise.

Do not place large RC values that introduce measurement error.

Kelvin traces:
- no load current;
- route as a tightly coupled pair;
- connect inside the four-terminal shunt sense pads;
- keep away from TPSM63603 switch node and Class-D outputs.

## 5. 24 V system bulk
+24V_SYS supplies amplifier and DC/DC.

Audio-local bulk belongs primarily at TAS5825M Sheet 05.

Sheet 03 provides controlled rail bulk/ceramic decoupling sufficient for converter input stability while respecting:
- Ag5324 startup;
- hot-plug;
- source handover;
- LM74700 behavior.

Total 24 V capacitance is a system value, not independently maximized per sheet.

## 6. 24 V -> 5 V
U8? power-designator assignment at capture: **TPSM63603V5RDHR**.

Input:
- +24V_SYS nominal.

Output:
- +5V_SYS
- up to 3 A module capability subject to thermal/input conditions.

TI minimum-input baseline retained:
- 2 x 4.7 uF, 50 V, X7R/X7S, 1206 directly at VIN/GND.
Candidate families:
- TDK C3216X7R1H475K160AC
- Murata GRM31CR71H475KA12L.

Output baseline:
- 2 x 10 uF, 16 V X7R
- 100 nF high-frequency bypass
- final effective COUT after DC-bias derating must meet TI stability/transient guidance.

Use the fixed 5 V variant and reproduce TI reference placement.

## 7. 5 V loads
+5V_SYS feeds:
- 3.3 V buck;
- VOICE daughterboard where required;
- expansion/service internal loads where explicitly permitted.

USB +5V_SERVICE is NOT tied directly to +5V_SYS.

Budget target:
- reserve sufficient transient current for ESP32 Wi-Fi/BLE, W5500, XVF3800/VOICE, radar support and sensors.
- final measured steady-state 5 V demand should remain comfortably below the 3 A converter rating.

## 8. 5 V -> 3.3 V
U9? power-designator assignment at capture: **TPS62823DLCR**.

Input:
- +5V_SYS.

Output:
- +3V3_SYS.

Target:
- 3.3 V
- up to 3 A capability.

Baseline switching frequency: device nominal ~2.2 MHz.

Initial inductor:
- 470 nH
- shielded
- low DCR
- saturation/current rating with margin above converter peak current.

Exact MPN: VALIDATE.

Input/output ceramic network shall be calculated from TI datasheet/reference design, including effective capacitance under DC bias.

## 9. 3.3 V loads
+3V3_SYS feeds:
- ESP32-S3-WROOM-1-N16R8
- W5500
- INA228
- ENV board
- radar VDDLF/support and local 1.8 V regulator input
- VOICE support/control as appropriate
- status/service logic.

Microphones use separately switched +3V3_MIC on PCB-B.

## 10. Power-good
Required system signals:
- 5V_PG
- 3V3_PG
- POWER_ALERT.

If selected converters do not expose a directly suitable PG output, use a supervisor/comparator implementation rather than infer rail validity from MCU ADC alone.

Boot sequence must not enable audio/radar/voice until required rails are valid.

Exact supervisor topology: VALIDATE_CAPTURE.

## 11. PoE power budget
Ag5324 continuous budget baseline: ~24 W available from its isolated 24 V output under rated conditions.

System design shall reserve power for:
- conversion losses;
- MCU/network/voice/radar/sensors;
- transient margin.

Therefore TAS5825M in PoE mode is software/DSP power-limited.

Initial engineering allocation, NOT a production guarantee:
- logic/voice/network/radar/environment: target <=5–7 W worst-case envelope;
- conversion and margin: several watts reserved;
- remaining continuous electrical budget available to audio roughly in the low-to-mid teens of watts, with short peaks allowed only if rail/PoE telemetry remains stable.

The final PoE audio limiter shall use measured system efficiency and INA228 telemetry, not this rough allocation.

## 12. External power budget
Recommended external adapter:
- 24 V
- 3 A
- ~72 W input capacity.

This is substantially above the expected system requirement and allows PERFORMANCE audio mode.

It does NOT imply 72 W may be continuously dissipated inside the 320 x 400 x 40 mm enclosure.

Final limit is determined by:
- TAS5825M output/efficiency;
- DML thermal/excursion limits;
- PCB/enclosure thermal model;
- connector/wiring rating.

## 13. Power telemetry / Home Assistant
Expose:
- source: PoE / external
- input voltage
- input current
- input power
- accumulated energy
- power mode ECO/PERFORMANCE
- power-limit/headroom diagnostic
- POWER_ALERT state
- 5 V rail status
- 3.3 V rail status.

Update rate should be useful without excessive I2C traffic.

## 14. Brownout / load shedding
Priority order under insufficient power:
1. preserve 3.3 V control/network.
2. preserve 5 V voice/control where possible.
3. reduce/mute amplifier first.
4. optional radar power reduction only if required by severe fault policy.

Firmware monitors INA228 and rail state and applies TAS5825M limiting before hard collapse.

## 15. PCB layout
- RSH1 in main 24 V current path with true Kelvin pads.
- INA228 adjacent to shunt but thermally separated from hot MOSFETs/converters.
- TPSM63603 VIN caps immediately at module pins.
- TPSM63603 switch/current loops compact.
- TPS62823 inductor and input/output capacitors follow TI reference layout.
- L2 continuous GND plane.
- no sensitive sense/I2C traces through switching-current loops.
- provide TP_24V_SYS, TP_5V_SYS, TP_3V3_SYS, TP_POWER_ALERT.

## 16. Factory test
1. shunt resistance/continuity sanity.
2. INA228 identity.
3. 24 V measurement calibration.
4. current calibration at multiple known loads.
5. 5 V no-load/full-load.
6. 3.3 V no-load/full-load.
7. transient Wi-Fi/audio load response.
8. POWER_ALERT.
9. 5V_PG / 3V3_PG.
10. PoE full-system load/limiter.
11. external PERFORMANCE load.
12. converter thermal soak.
13. efficiency measurement.

## 17. Release gates
Sheet 03 becomes FROZEN only after:
1. exact RSH1 MPN/TCR;
2. INA228 filter values;
3. TPSM63603 effective CIN/COUT calculation;
4. TPS62823 inductor and CIN/COUT frozen;
5. PG/supervisor circuit frozen;
6. full power-budget spreadsheet/measurement;
7. PoE limiter threshold validated;
8. converter thermal simulation/measurement;
9. load-transient validation;
10. EMI pre-compliance.
