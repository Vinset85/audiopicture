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
