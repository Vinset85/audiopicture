# Sheet 02 — 24 V Input / Ideal-Diode ORing / Source Priority Rev.A

Status: **implementable schematic specification**. Exact fuse, connector, priority comparator and final MOSFET qualification remain VALIDATE before production release.

## 1. Functional requirement
AudioPicture accepts:
- isolated PoE-derived `+24V_POE`;
- external nominal 24 V DC input `+24V_EXT`.

Outputs:
- `+24V_RAW`.

Rules:
1. PoE only -> PoE supplies +24V_RAW.
2. external only -> external supplies +24V_RAW.
3. both present -> external supply has deterministic priority.
4. no backfeed from either source into the other.
5. priority must work before ESP32 boot and with MCU absent/crashed.

## 2. External input
J2: dedicated DC input, nominal 24 V / 3 A recommended.

Exact connector: VALIDATE_MECHANICAL_CURRENT.

Path:
J2
-> F101
-> reverse/transient protection
-> D101 TVS
-> input filtering
-> external ideal-diode branch
-> +24V_RAW.

Connector and wiring shall be rated above 3 A continuous with margin.

## 3. Fuse
F101 exact MPN: VALIDATE.

Target:
- protect wiring/PCB from external-source faults;
- tolerate normal amplifier transients and input bulk charging;
- coordinated with 24 V / 3 A recommended PSU.

Baseline is a replaceable fuse or qualified resettable protection only after trip/hold/thermal curves are checked. Do not freeze a generic 3 A PTC.

## 4. External TVS
D101 baseline candidate: **SMBJ33A**.

Status: VALIDATE_CLAMP.

Check:
- standoff versus 24 V supply tolerance;
- clamp voltage at realistic surge current;
- downstream absolute maximum ratings;
- pulse energy and source impedance.

TVS is placed physically adjacent to J2/protection return.

## 5. Ideal-diode controllers
U4: **LM74700QDBVRQ1** — PoE branch.
U5: **LM74700QDBVRQ1** — external branch.

Each controller drives an external N-channel MOSFET.

Candidate Q201/Q202: **DMT6007LFG** or qualified 60 V equivalent.

Status: VALIDATE_THERMAL_AVAILABILITY.

Required checks:
- VDS >= 60 V class;
- low RDS(on);
- SOA during hot-plug/inrush/handover;
- gate-charge compatibility;
- thermal rise at expected current;
- reverse-current blocking behavior.

## 6. Branches
PoE:
+24V_POE -> U4/Q201 ideal diode -> +24V_RAW.

External:
+24V_EXT -> U5/Q202 ideal diode -> +24V_RAW.

Do not connect +24V_POE and +24V_EXT directly.

## 7. Deterministic external priority
Pure ideal-diode ORing does not guarantee source preference when source voltages are close.

Therefore U4 PoE controller enable is gated by a hardware priority circuit.

Required behavior:
- EXT absent -> U4 enabled.
- EXT valid -> U4 disabled.
- U5 external branch enabled whenever external voltage is valid.
- hysteresis prevents chatter during external plug/unplug.
- priority does not depend on ESP32.

### Baseline architecture
`+24V_EXT`
-> high-impedance divider
-> low-power comparator with internal/external reference
-> hysteresis
-> open-drain/control transistor
-> U4 EN pulled to disable PoE branch.

Comparator circuit must be powered from a rail available whenever either source can be present. Preferred implementation derives a small always-available bias from the source domain without violating source isolation/backfeed.

Exact comparator/reference MPN: VALIDATE_PRIORITY.

Do not power the priority comparator solely from +3V3_SYS if doing so would delay priority until downstream rails start.

## 8. Priority thresholds
Nominal external source = 24 V.

Initial target:
- EXT_VALID assert approximately 20–21 V.
- EXT_VALID deassert approximately 18–19 V.

Final thresholds/hysteresis are VALIDATE and must consider:
- PSU tolerance;
- cable drop;
- undervoltage behavior of TAS5825M/DC-DC;
- handover stability.

A partially collapsed external supply must not indefinitely suppress a healthy PoE source.

## 9. Handover
Goal:
- no source-to-source current;
- no reset of 5 V/3.3 V logic during normal plug/unplug where energy storage allows;
- amplifier may be proactively muted during handover if POWER manager detects margin loss.

+24V_RAW bulk capacitance is coordinated with Sheet 03 and Ag5324 startup limits.

Do not solve handover by adding unlimited capacitance.

## 10. Presence sensing
`EXT_PRESENT` derives from external-valid hardware state.

`POE_PRESENT` derives from isolated +24V_POE secondary.

Signals to ESP32 must:
- be 3.3 V safe;
- not phantom-power MCU;
- retain meaningful state through rail sequencing.

Use comparator/open-drain or protected divider topology as appropriate. Exact circuit is captured with Sheet 03 monitoring.

## 11. Input filtering
External input baseline:
- TVS at connector;
- local ceramic capacitance;
- controlled bulk capacitance;
- optional ferrite/CMC only if conducted-EMI measurement requires it.

Do not insert excessive series impedance into the 24 V amplifier path.

## 12. Ground / isolation
+24V_POE used here is the **isolated secondary** of Ag5324.

Its negative output joins GND_SYS only on the secondary side.

No PoE primary/cable-side return is connected to this ORing circuitry.

## 13. Fault behavior
External short/fault:
- F101/protection acts;
- PoE may recover only after EXT_VALID deasserts and priority circuit releases U4.

PoE fault:
- external source can supply system if present.

MCU fault:
- hardware priority remains correct.

Brownout:
- Power Manager mutes TAS5825M based on rail/power telemetry.

## 14. PCB layout
- J2, F101 and D101 at board edge.
- TVS return loop extremely short/wide.
- U4/U5 gate loops compact.
- Q201/Q202 high-current paths short and wide.
- avoid thermal coupling from MOSFETs into INA228 shunt sense.
- +24V_RAW route sized for external performance-mode current.
- keep source nets physically distinguishable before ORing.
- provide probe points TP_24V_POE, TP_24V_EXT, TP_24V_RAW.

## 15. Factory test
1. external 18–26 V sweep.
2. PoE-only startup.
3. external-only startup.
4. both connected.
5. verify external priority before MCU boot.
6. measure reverse current into PoE.
7. measure reverse current into external connector.
8. plug/unplug external under load.
9. external undervoltage/recovery hysteresis.
10. PoE loss while external present.
11. external loss with PoE present.
12. thermal test Q201/Q202 at maximum continuous load.
13. fault/fuse behavior.

## 16. Release gates
Sheet 02 becomes FROZEN only after:
1. J2 exact MPN/current rating;
2. F101 exact protection part;
3. SMBJ33A clamp analysis;
4. Q201/Q202 MOSFET final qualification;
5. exact priority comparator/reference circuit;
6. priority thresholds/hysteresis simulation;
7. hot-plug/inrush simulation;
8. dual-source bench handover;
9. reverse-current measurement;
10. thermal and EMC validation.


## Architecture correction and PoE branch switch selection — 2026-09-29

### LM74700 EN limitation
LM74700 with one external N-MOSFET remains suitable for ideal-diode / reverse-current-blocking service, but its EN function is not accepted as the sole physical source-disconnect mechanism for deterministic EXT-over-PoE priority. A single-FET path can retain a forward body-diode conduction path when gate drive is disabled.

Therefore the earlier concept "EXT_VALID disables the PoE LM74700 EN" is superseded.

### PoE true-disconnect baseline
U_POE_SW = **Texas Instruments TPS4810-Q1 family**, preferred implementation **TPS48100-Q1**, with two external N-channel MOSFETs in back-to-back common-source configuration.

Manufacturer characteristics supporting this selection:
- 3.5 V to 95 V operating range;
- 100 V absolute maximum;
- approximately 35 uA typical operating quiescent current;
- approximately 1 uA shutdown current;
- two independent strong gate drivers, approximately 2 A source/sink;
- explicit support for back-to-back MOSFETs;
- separate INP1 / INP2 controls;
- adjustable UVLO;
- short-circuit protection and FLT output;
- AEC-Q100;
- VSSOP-19 DGX package.

Status: **FROZEN_ARCHITECTURE / EXACT TPS48100 ORDERABLE SUFFIX_AND_EXTERNAL_FETS_VALIDATE**.

### Corrected PoE path
+24V_POE
-> TPS48100-Q1 controlled back-to-back MOSFET pair
-> PoE protected/switched node
-> ideal-diode / ORing function as required by final dual-source implementation
-> +24V_RAW.

During external-source priority:
- hardware EXT_VALID forces the PoE switch OFF through the TPS4810 control interface;
- both PoE MOSFETs are off, providing true off-state isolation rather than relying on one body diode;
- source selection remains independent of MCU firmware.

### External branch
The external 24 V branch may retain LM74700-Q1 + low-RDS(on) N-MOSFET as the low-loss ideal-diode path, subject to final transient/SOA validation.

### Controller comparison
TPS4811-Q1 was evaluated but is not the baseline because its normal operating quiescent current is substantially higher and its additional current-monitor/protection functions are unnecessary for the PoE source-selection role.

ADI LTC4368 was evaluated as a strong low-Iq alternative with back-to-back MOSFET control and bidirectional circuit breaker behavior. It is not the Rev.A baseline because its normal operating range ends at 60 V, leaving less operating-voltage margin than the 95 V TPS4810-Q1 architecture.

### Next gate
Before freezing the exact Sheet-02 circuit:
1. choose exact TPS48100-Q1 orderable suffix/package;
2. select the two PoE switch MOSFETs with >=80 V preferred VDS margin;
3. determine whether the external LM74700 branch also moves to >=80 V MOSFET;
4. finalize SMBJ33A/transient clamp compatibility;
5. calculate TPS4810 UVLO and EXT_VALID control thresholds;
6. simulate source handover and +24V_RAW inrush.


## Rev.A 100 V power-switch freeze — 2026-09-29

### PoE disconnect controller exact MPN
U_POE_SW = **Texas Instruments TPS48100QDGXRQ1**
- TPS48100-Q1 variant;
- DGX VSSOP-19 package, 5.1 x 3.0 mm class;
- -40 to +125 degC;
- 3.5-95 V operating range, 100 V absolute maximum;
- low-Iq controller for two back-to-back N-MOSFETs.

Status: **FROZEN_DEVICE_PACKAGE**.

### Power MOSFET baseline
Q_POE_A / Q_POE_B and external ideal-diode MOSFET baseline:
**Infineon ISC035N10NM5LF2ATMA1**
- 100 V N-channel;
- RDS(on) max 3.5 mOhm at 10 V;
- SuperSO8 FL / TDSON-8 5 x 6 mm;
- wide SOA Linear FET;
- intended by manufacturer for hot-swap, eFuse and protection/inrush applications;
- active/recommended.

Status: **FROZEN_ELECTRICAL_PACKAGE / SOA_VALIDATE_AT_FINAL_INRUSH_PROFILE**.

Using the same 100 V MOSFET family on PoE and external branches is preferred for BOM/footprint consolidation.

Approximate conduction check:
- one FET at 3 A and 3.5 mOhm max: 31.5 mW;
- two back-to-back FETs at 1 A: 7 mW;
- two back-to-back FETs at 3 A: 63 mW.
These figures exclude temperature rise of RDS(on), switching/inrush stress and PCB/package thermal resistance.

The previous 60 V DMT6007LFG candidate is demoted from Rev.A baseline due to reduced transient-voltage margin.

### Next protection gate
Now calculate the external 24 V transient clamp around the 100 V MOSFET/controller envelope:
- verify SMBJ33A VRWM/VBR/VC against normal 24 V PSU tolerance;
- ensure worst credible clamped voltage remains below downstream absolute maxima;
- define F101 so TVS fault energy is safely interrupted;
- then freeze EXT_VALID assert/deassert divider and hysteresis.


## Transient-envelope correction — 2026-09-29

### SMBJ33A role corrected
SMBJ33A is NOT sufficient as the sole downstream overvoltage protection for +24V_RAW.

Reason:
- TAS5825M PVDD recommended maximum = 26.4 V, absolute maximum = 30 V.
- TPSM63603 recommended input maximum = 36 V, absolute maximum = 40 V.
- A 33 V-standoff TVS necessarily clamps above the safe TAS5825M PVDD envelope.

Therefore D101/SMBJ33A, if retained, is only a connector/front-end surge-energy suppressor protecting the 100 V input-switching devices from high-energy transients. It must not be treated as the protection that guarantees safe +24V_RAW voltage.

### Mandatory external-input OVP disconnect
The external 24 V path shall include hardware overvoltage disconnect before +24V_RAW.

Required behavior:
- nominal 24 V source passes normally;
- approaching the TAS5825M safe operating ceiling, external source is disconnected before +24V_RAW can exceed the system limit;
- target OVP threshold shall be below 26.4 V recommended PVDD maximum with tolerance budget;
- initial design target: approximately 25.5-26.0 V nominal trip, final value after resistor/reference tolerance analysis;
- OVP must be independent of MCU firmware.

The 100 V MOSFET/controller front-end absorbs the voltage-rating burden while the disconnect protects the lower-voltage downstream electronics.

### Fuse F101
Do NOT freeze F101 merely as a nominal 3 A fuse.

Requirements:
- normal 24 V / 3 A adapter operation shall not nuisance-trip;
- tolerate audio crest current and controlled input-capacitor charging;
- interrupt sustained TVS crowbar/short fault safely;
- voltage rating suitable for the protected input;
- time-current curve and I2t must coordinate with D101 and PCB/wiring;
- exact MPN remains OPEN until maximum continuous external input current and final inrush profile are frozen.

Initial engineering class: approximately 4 A time-delay fuse, subject to thermal derating and I2t coordination. This is not yet a production MPN.

### Protection architecture
J2 -> F101 -> surge TVS/front-end suppression -> 100 V protected switch / ideal-diode stage with hardware OVP -> +24V_RAW.

This separates:
1. high-energy transient survival at the connector;
2. true overvoltage disconnect for sensitive downstream electronics;
3. reverse-current / source-ORing behavior.

### Release gate added
Before Sheet 02 is frozen:
- calculate worst-case OVP trip including resistor/reference/controller tolerances;
- demonstrate +24V_RAW remains below 26.4 V in normal protection operation and below 30 V absolute maximum during fault/transient response;
- calculate TVS pulse current/energy for the selected external PSU/wiring model;
- select F101 from manufacturer time-current and I2t data rather than current rating alone.


## External-input supervision architecture — 2026-09-29

### TPS48100 function boundary
TPS48100-Q1 provides adjustable **UVLO** through EN/UVLO and independent back-to-back MOSFET gate controls, but it does not provide a programmable external-input OVP threshold suitable for protecting TAS5825M at ~26 V.

Therefore EXT_OVP is implemented with an independent hardware comparator window. Do not emulate OVP in firmware.

### Window comparator baseline
U_EXT_MON = **Texas Instruments TLV1822QDGKRQ1**
- dual comparator;
- open-drain outputs;
- 2.4 V to 40 V supply;
- rail-to-rail inputs;
- ~5 uA/channel typical;
- POR for deterministic startup;
- AEC-Q100;
- VSSOP-8 DGK.

Status: **FROZEN_DEVICE_PACKAGE / THRESHOLD_NETWORK_CALCULATE**.

TI documents the TLV182x family explicitly for 24 V window-comparator supervision.

### Hardware states
The dual comparator supervises +24V_EXT after connector surge protection and before connection to +24V_RAW.

Define:
- EXT_UV_OK: external input above undervoltage threshold;
- EXT_OV_OK: external input below overvoltage threshold;
- EXT_VALID = EXT_UV_OK AND EXT_OV_OK, implemented in fail-safe open-drain logic.

Target nominal thresholds:
- UV assert valid: 20.5 V;
- UV release invalid: 19.0 V;
- OV trip invalid: 25.8 V;
- OV recovery valid: 25.0 V.

These are design targets, NOT frozen resistor values. Final thresholds must include comparator offset, resistor tolerance, reference tolerance, hysteresis injection and temperature.

### Source-priority behavior
EXT_VALID high:
- external protected path enabled;
- PoE TPS48100 back-to-back path commanded OFF;
- EXT_PRESENT reported true.

EXT_VALID low:
- external path disabled or prevented from feeding +24V_RAW;
- PoE path permitted ON if +24V_POE is present;
- EXT_PRESENT false.

The logic must default to PoE-safe behavior during comparator POR/unpowered states and must not require +3V3_SYS or MCU boot.

### Threshold/reference implementation gate
Do not derive the final window thresholds directly from the 24 V rail without checking startup and fault behavior.
Preferred next step:
- select a precision low-Iq reference available whenever external input is present, or use a divider topology referenced to a validated auxiliary bias;
- use <=0.5% divider resistors, preferably 0.1% where threshold stack-up benefits;
- calculate explicit positive feedback for hysteresis;
- SPICE worst-case corners before native capture.


## Precision reference and threshold-network baseline — 2026-09-29

### Reference architecture
Use a 2.500 V precision shunt reference biased directly from the protected +24V_EXT domain. This avoids creating a separate low-voltage regulator solely for the window comparator.

Baseline family: **TI LM4040A-2.5 V**, A-grade preferred.
- 2.500 V fixed shunt reference;
- A grade initial accuracy up to +/-0.1%;
- minimum regulation current in the tens of microamps;
- stable with capacitive loads and no output capacitor required;
- series bias resistor from +24V_EXT is mandatory and shall be dimensioned across the complete valid/fault input range.

Exact orderable MPN/package: **VALIDATE_ORDERABLE_Q_GRADE** before BOM freeze.

### Comparator error budget
TLV1822-Q1:
- maximum input offset over the qualified temperature range: +/-4 mV class;
- no internal hysteresis;
- external positive feedback is mandatory for slow 24 V rail crossings.

Consequently the divider and feedback network shall be solved as one circuit. Do not select a nominal divider and add hysteresis afterwards.

### Threshold targets retained
Undervoltage channel:
- rising EXT_VALID threshold = 20.5 V nominal;
- falling invalid threshold = 19.0 V nominal;
- hysteresis span = 1.5 V.

Overvoltage channel:
- rising invalid threshold = 25.8 V nominal;
- falling valid threshold = 25.0 V nominal;
- hysteresis span = 0.8 V.

### Zero-hysteresis divider sanity check
With VREF = 2.500 V and RLOW = 100 kohm, ideal no-feedback upper resistances would be:
- 20.5 V threshold: RHIGH = 720 kohm;
- 25.8 V threshold: RHIGH = 932 kohm.

These are sanity-check values only and MUST NOT be used as final schematic values because positive-feedback hysteresis changes both switching points.

### Final resistor-network requirements
- use E96/E192 values;
- <=0.1% preferred for threshold-setting resistors;
- explicitly include comparator offset, VREF initial accuracy/drift, resistor tolerance and temperature coefficient;
- target worst-case OVP trip safely below TAS5825M 26.4 V recommended PVDD maximum;
- include RC noise filtering only where it cannot compromise OVP response;
- calculate startup/POR state with TLV1822 open-drain outputs high-impedance during POR;
- fail-safe logic must never interpret comparator POR as a valid external source.

Status: **TOPOLOGY_FROZEN / RESISTOR_VALUES_PENDING_WORST_CASE_SOLVE**.


## Threshold worst-case refinement — 2026-09-29

### OVP target derated for production margin
The previous 25.8 V nominal OVP trip target is superseded.

Reason: the complete error stack includes TLV1822-Q1 input offset, LM4040A25 full-temperature reference error, divider/feedback resistor tolerance and temperature coefficient. A nominal trip too close to the TAS5825M 26.4 V recommended PVDD ceiling leaves inadequate production/temperature margin.

Revised nominal window:
- UV rising / EXT_VALID assert: 20.5 V
- UV falling / invalid: 19.0 V
- OV rising / invalid trip: **25.3 V**
- OV falling / valid recovery: **24.7 V**

The narrower 0.6 V OV hysteresis is intentional. A correct nominal 24 V adapter remains comfortably inside the valid window.

### Conservative first-pass error envelope
For engineering screening, use:
- TLV1822-Q1 Vos: +/-4 mV;
- LM4040A25 full-range reference tolerance/error: use datasheet full-temperature bound, not only 25 C initial tolerance;
- threshold resistors: 0.1% max, low-TCR;
- include feedback-resistor tolerance independently.

A simplified conservative input-referred screen puts a 25.3 V nominal OVP point approximately in the 25.0-25.6 V region before a full correlated network solve. This is comfortably below 26.4 V and is therefore a safer basis than 25.8 V nominal.

This screening range is NOT a substitute for exact corner analysis.

### Reference bias
Bias LM4040A25 at >=100 uA nominal around the valid 24 V input so that it is comfortably above the full-temperature minimum cathode-current requirement.

Initial series-resistor class:
(24 V - 2.5 V) / 100 uA ~= 215 kohm.

Use approximately 200 kohm as the starting E96 class, then account for comparator/reference loading and the lowest valid EXT voltage. Exact value is pending current-budget corner analysis.

### Capture rule
Do not freeze final UV/OV feedback resistor values until the exact three-resistor hysteresis equations have been solved for the selected comparator input polarity and open-drain pull-up domain, and all tolerance corners have been enumerated.

Status remains **TOPOLOGY_FROZEN / NOMINAL_THRESHOLDS_REFINED / EXACT_RESISTORS_PENDING_CORNER_SOLVE**.


## Exact comparator network solve — 2026-09-29

### UV channel — values frozen
Non-inverting Schmitt network, VREF = 2.500 V:
- R_UV_IN = 660 kohm, 0.1%
- R_UV_GND = 100 kohm, 0.1%
- R_UV_FB = 1.10 Mohm, 0.1%
- comparator open-drain output pulled up to VREF domain.

Ideal thresholds:
- rising = 20.500 V
- falling = 19.000 V

Conservative brute-force corner screen using resistor +/-0.1%, LM4040A25 full-range +/-19 mV reference bound and TLV1822-Q1 +/-4 mV Vos:
- UV rising approx 20.276 to 20.725 V
- UV falling approx 18.790 to 19.211 V

### OV channel — values frozen
Inverting window channel:
- R_OV_TOP = 912 kohm, 0.1%
- R_OV_BOT = 100 kohm, 0.1%
- R_OV_REF = 100 kohm, 0.1%
- R_OV_FB = 4.12 Mohm, 0.1%
- comparator open-drain output pulled up to VREF domain.

Ideal thresholds:
- rising trip = 25.300 V
- falling recovery = 24.7005 V

Conservative brute-force corner screen with the same assumptions:
- OV rising trip approx 25.022 to 25.579 V
- OV falling recovery approx 24.427 to 24.975 V

The worst screened OV trip remains below the TAS5825M 26.4 V recommended PVDD ceiling by approximately 0.82 V.

### Important implementation note
The 4.12 Mohm feedback leg is electrically valid but high impedance. Layout shall keep this node short/clean, away from switching nodes, flux residue and high-leakage protection structures. If PCB contamination/leakage analysis later makes 4.12 Mohm undesirable, scale the OV network downward while preserving ratios and re-run bias-current/power calculations.

### Status
Threshold resistor ratios: **FROZEN_ELECTRICAL**.
Still pending before Sheet-02 production freeze:
- exact LM4040A25-Q1/orderable package decision;
- reference bias resistor exact value and dissipation;
- fail-safe open-drain AND/interlock transistor implementation;
- SPICE transient verification including comparator propagation, MOSFET gate turn-off and +24V_RAW overshoot.
