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
RSH1 baseline is revised to **7.5 mOhm**:
- 4-terminal/Kelvin;
- >=0.5 W;
- <=0.5% preferred, low TCR.

At 3 A:
- Vshunt = 22.5 mV;
- Pshunt = 67.5 mW.

At 4 A:
- Vshunt = 30 mV;
- Pshunt = 120 mW.

At 5 A transient:
- Vshunt = 37.5 mV;
- Pshunt = 187.5 mW.

With INA228 ADCRANGE=1 (±40.96 mV), 7.5 mOhm gives approximately **5.46 A full-scale**, preserving the high-sensitivity range while providing substantially more transient headroom than 10 mOhm.

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
- Ag53024 startup;
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

Output baseline corrected to TI 5 V guidance:
- minimum required effective COUT = **25 uF**;
- production baseline = **2 x 47 uF, 10 V, 1210 X7R/X7S-class**, selected so combined effective capacitance at 5 V remains >=25 uF;
- TI 24 V -> 5 V example reports approximately 48 uF total effective capacitance using this class;
- retain 100 nF local high-frequency bypass where layout/reference design calls for it.

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
Ag53024 application continuous budget baseline: **22.5 W maximum continuous output** for a fully IEEE 802.3at-compliant application, per the current Silvertel guidance. 30 W is transient/module capability only and is not the continuous application budget.

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


## Sheet-03 first freeze review — 2026-09-29

### INA228 range decision
Use INA228 **ADCRANGE = 1, +/-40.96 mV** with the revised 7.5 mOhm shunt baseline.
This yields approximately 5.46 A measurable full scale.

Do not use the +/-163.84 mV range unless later transient testing proves >5.4 A legitimate system current.

### Shunt exact-part gate
Preferred family remains Vishay WSK2512 / WSLP2512-class 4-terminal low-TCR current-sense resistor, but exact 7.5 mOhm orderable MPN must be verified before BOM freeze.

Target:
- 7.5 mOhm;
- true Kelvin / 4-terminal geometry preferred;
- <=0.5%;
- <=50 ppm/C preferred;
- >=0.5 W, preferably >=1 W for low self-heating.

### 3.3 V converter current gate
Do not freeze TPS62823 solely from its 3 A headline rating. Before final freeze, sum worst-case +3V3_SYS loads including:
- ESP32-S3-WROOM Wi-Fi peaks;
- W5500;
- INA228;
- radar support/local 1.8 V input power reflected to 3.3 V;
- ENV and status logic;
- daughterboard/control overhead.

The XVF3800 main 5 V load is accounted on +5V_SYS, not blindly added to +3V3_SYS.

Status: **TPS62823 RETAINED_CANDIDATE / LOAD_BUDGET_VERIFY**.


## Preliminary rail power budget — 2026-09-29

### +3V3_SYS conservative design budget
Use datasheet peak/normal figures where available and engineering allowances where daughterboard conversion details are not yet frozen.

Direct 3.3 V loads:
- ESP32-S3-WROOM-1-N16R8: reserve **500 mA design peak**. Espressif documents up to ~355 mA Wi-Fi TX peak for the module; additional margin covers PSRAM/digital activity and rail transient design.
- W5500: reserve **150 mA**; datasheet normal/100BASE-TX figures are ~132 mA.
- INA228 + ENV + status/control/I2C pullups: reserve **30 mA**.
- Radar support reflected onto 3.3 V: reserve **180 mA input-equivalent** until the 1.8 V regulator efficiency/duty-cycle profile is frozen. BGT60TR13C can reach ~200-230 mA at 1.8 V while fully active, although duty-cycled presence operation is far lower.
- Voice-board 3.3 V I/O/mic/control allowance: **150 mA** pending the XVF3800 daughterboard regulator tree freeze.
- engineering/transient margin: **300 mA**.

Conservative +3V3_SYS design envelope: approximately **1.31 A**.

Even allowing substantial simultaneous transient margin, this is well below the TPS62823 3 A capability.

Decision: **TPS62823 retained and promoted to FROZEN_CONTROLLER**, subject to thermal/passive/layout validation.

### +5V_SYS conservative design budget
+5V_SYS supplies:
- TPS62823 input. At 3.3 V x 1.31 A = 4.32 W and ~90% conversion efficiency, approximately 0.96 A is drawn from 5 V.
- XVF3800/VOICE local regulator tree: reserve **0.8 A at 5 V** until the exact XU316/XVF3800 rail implementation is frozen.
- expansion/internal 5 V allowance: **0.25 A**.
- transient/design reserve: **0.35 A**.

Conservative 5 V design envelope: approximately **2.36 A**.

Decision: TPSM63603V5 3 A remains suitable with ~0.64 A nominal design margin, but thermal derating at 24 V input and enclosure temperature is mandatory before production freeze.

### Architecture consequence
The 3.3 V converter is not the limiting logic rail. The tighter rail is the 5 V converter because it carries both the entire 3.3 V downstream power and the XVF3800 daughterboard conversion load.

Do not add arbitrary new 5 V expansion loads without re-running this budget.

### Radar power note
Infineon lists BGT60TR13C active current in the ~200 mA class at 1.8 V and also documents sub-5 mW operation with duty cycling. Size the regulator and decoupling for active peaks; use duty cycling only for average-power budgeting.

### Voice power note
XVF3800 is not a native 5 V IC. Its documented rails include 0.9 V core, 1.8 V I/O/USB and 3.3 V I/O. The 5 V budget above is therefore an allocation to the PCB-B local regulator tree, not a direct 5 V XVF3800 supply. Sheet PCB-B must freeze those local regulators before this allowance becomes a verified number.


## Converter passive freeze — 2026-09-29

### TPSM63603V5 24 V -> 5 V
Controller/module exact MPN remains **TPSM63603V5RDHR** and is now **FROZEN_DEVICE_PACKAGE**.

Frequency:
- set approximately **1 MHz**;
- R_RT = **13.0 kohm** to AGND per TI 5 V design guidance.

Input:
- C5VIN1/C5VIN2 = **4.7 uF, 50 V, 1210, X7R/X7S**, two pieces minimum;
- effective capacitance under 24-26 V DC bias must be checked from the selected manufacturer curves;
- add 100 nF local HF ceramic if permitted by reference placement.

Output:
- C5VOUT1/C5VOUT2 = **47 uF, 10 V, 1210, X7R/X7S**, two pieces;
- combined effective capacitance at 5 V must be >=25 uF;
- target around 40-50 uF effective is preferred for voice/3.3 V transient loading.

Other TI reference connections:
- fixed 5 V variant: FB connected to VOUT as specified by TI;
- VLDOIN connected to VOUT for efficiency;
- VCC decoupled with **1 uF** close to VCC/PGND;
- RBOOT/CBOOT connection follows TI efficiency recommendation;
- PGOOD is available and shall become **5V_PG**.

### TPS62823 5 V -> 3.3 V
U_3V3 = **TPS62823DLCR**, now **FROZEN_DEVICE_PACKAGE**.

Minimum/reference power stage:
- L_3V3 = **470 nH**, shielded;
- CIN = **4.7 uF** minimum ceramic directly at VIN/PGND;
- COUT = **10 uF** minimum ceramic directly at VOUT/PGND;
- PG becomes **3V3_PG**.

Because AudioPicture has burst loads (ESP32 radio and Ethernet/digital activity), production baseline adds:
- **22 uF local 3.3 V bulk ceramic** near the ESP32/network load region, separate from the converter control-loop minimum capacitor;
- normal 100 nF local decouplers at individual ICs.

### 470 nH inductor qualification
Exact MPN remains OPEN. Required:
- 470 nH nominal;
- shielded;
- low DCR;
- saturation current comfortably above TPS62823 peak current limit, target >=4.5 A;
- temperature-rise current >=3 A with margin;
- compact low-profile package suitable for the 40 mm enclosure;
- verify inductance retention under DC bias.

### Capacitor selection rule
Nominal printed capacitance is not acceptance criteria.
For every MLCC in these converter networks, verify manufacturer DC-bias curves at:
- 26 V for 50 V input capacitors;
- 5 V for 10/16 V 5 V output capacitors;
- 3.3 V for 3.3 V output capacitors.

Status: **CONTROLLER_AND_PASSIVE_VALUES_FROZEN / EXACT_L_C_MPN_DC_BIAS_VERIFY**.


## Exact inductor and INA228 filter freeze — 2026-09-29

### TPS62823 inductor exact MPN
L_3V3 = **TDK TFM201610ALM-R47MTAA**
- 470 nH +/-20%;
- magnetically shielded metal-core thin-film;
- 2.0 x 1.6 x 1.0 mm;
- DCR 28 mOhm typ / 34 mOhm max;
- saturation-current rating 5.8 A typ / 5.1 A max-spec criterion at 30% inductance drop;
- temperature-rise current 5.0 A typ / 4.5 A max-spec criterion at +40 C rise;
- -40 to +125 C including self-heating;
- production status.

TI lists this exact part among inductors tested with TPS6282x.

Status: **FROZEN_MPN_FOOTPRINT**.

### TPS62823 output-capacitance baseline refinement
TI identifies 470 nH + 2 x 10 uF or 22 uF as the standard combination for most applications and permits 47 uF/100 uF with appropriate conditions.

Rev.A:
- converter-local COUT = **22 uF nominal ceramic** or 2 x 10 uF equivalent, selected for effective capacitance after 3.3 V DC bias;
- additional 22 uF local bulk remains near ESP32/network region;
- do not place remote bulk inside the converter feedback-loop placement envelope.

### INA228 input filter
TI recommends symmetric input filtering and warns against RFILTER >100 ohm because larger values degrade gain error/nonlinearity.

Rev.A freeze:
- R_INP = **10 ohm, 0.1%**
- R_INN = **10 ohm, 0.1%**
- C_DIFF = **100 nF, X7R**
- VS decoupling = **100 nF** directly at INA228 VS/GND.

This is intentionally a moderate filter; firmware conversion time/averaging provides additional noise rejection.

Status: **FROZEN_ELECTRICAL_VALUES**.

### Power-good nets
TPSM63603 PGOOD -> **5V_PG**.
TPS62823 PG -> **3V3_PG**.

Both are treated as open-drain status nets:
- one deliberate pull-up owner per net;
- pull up to +3V3_SYS only where startup sequencing cannot create a false-valid condition;
- otherwise use the upstream-valid domain or supervisor gating in the native schematic;
- MCU inputs must never be phantom-powered.

Do not add separate rail supervisors unless native-capture sequencing analysis shows the converter PG behavior is insufficient.


## MLCC and shunt production-part review — 2026-09-29

### 24 V -> 5 V input MLCC
C5VIN1/C5VIN2 baseline MPN:
**TDK C3225X7R1H475K250AB**
- 4.7 uF +/-10%;
- 50 V;
- X7R;
- EIA 1210;
- production;
- manufacturer DC-bias models available.

Status: **FROZEN_MPN / EFFECTIVE_CAPACITANCE_MODEL_RETAIN**.

Because the manufacturer curve shows material capacitance loss around the 24-26 V operating point, provide **C5VIN3 as an optional identical 1210 footprint**. Populate only if final TI stability/transient/thermal simulation or bench validation requires additional effective CIN.

### 5 V and 3.3 V MLCC policy
Do not freeze a 47 uF/10 V or 22 uF/10 V part solely from search/catalog nominal value.
Selection requires an active-production X7R/X7S part with manufacturer DC-bias model demonstrating:
- TPSM63603: combined effective COUT >=25 uF at 5 V across tolerance/temperature;
- TPS62823: effective converter-local COUT consistent with TI stability guidance at 3.3 V.

Until a specific production MPN satisfies that evidence, retain the already frozen nominal footprints/values but keep exact output-capacitor MPN status OPEN.

### RSH1 shunt
Vishay **WSK2512 family** is verified as:
- true 4-terminal SMD current-sense construction;
- resistance range down to 0.5 mOhm;
- 0.5% capability down to 1 mOhm;
- low-TCR metal-element construction;
- AEC-Q200 family.

However, an exact active/orderable **7.5 mOhm** WSK2512 order code has not yet been verified from the manufacturer catalog.

Therefore:
- family/package/specification = **FROZEN**;
- target value = **7.5 mOhm**;
- exact orderable MPN = **OPEN — DO NOT INFER PART NUMBER**.

If no clean 7.5 mOhm WSK2512 order code is confirmed, qualify an equivalent true 4-terminal shunt from another manufacturer rather than fabricating a Vishay code.

### Sheet-03 capture status
The sheet may be captured natively with:
- WSK2512 4-terminal footprint and RSH1 value 7.5 mOhm marked MPN-TBD;
- C5VIN1/2 = C3225X7R1H475K250AB;
- C5VIN3 optional/DNP identical footprint;
- output MLCC footprints sized for the frozen nominal capacitance classes but exact MPN held open.

Gerber release remains blocked until exact shunt and output-MLCC MPNs are verified.


## Sheet-03 release-state refinement — 2026-09-29

### Effective-capacitance acceptance rule
For TPS62823, TI explicitly recommends 470 nH with 2 x 10 uF or 22 uF as the standard combination for most applications and notes that effective ceramic capacitance may vary substantially with package, voltage rating and dielectric.

Therefore Rev.A acceptance is:
- nominal converter-local COUT: 22 uF class;
- manufacturer DC-bias curve/model mandatory;
- effective COUT at 3.3 V must remain inside TI's qualified LC region after tolerance and bias;
- exact MPN remains OPEN until this evidence is attached to the BOM audit.

### RSH1 no-inference rule
Vishay WSK2512 remains the preferred true 4-terminal family. Manufacturer data verifies the family architecture and tolerance capability, but an exact 7.5 mOhm catalog/order code is not yet verified.

Do not derive a Vishay part number syntactically from another resistance value.

### Capture/release distinction
Sheet 03 electrical capture is now sufficiently defined for native KiCad work:
- topology frozen;
- controllers frozen;
- rail voltages frozen;
- inductor MPN frozen;
- INA228 filter frozen;
- CIN MPN frozen;
- PG nets defined.

Status: **READY_FOR_NATIVE_KICAD_CAPTURE_WITH_BOM_RELEASE_GATES**.

Gerber/BOM production release remains blocked by:
1. exact RSH1 7.5 mOhm 4-terminal MPN;
2. exact 5 V COUT MPN with >=25 uF combined effective capacitance at 5 V;
3. exact 3.3 V COUT MPN with verified effective capacitance;
4. final transient/thermal validation.
