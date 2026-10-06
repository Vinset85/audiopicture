# MAIN power-status allocation — Rev.EZ, 2026-10-05

Status: **DIGITAL_ALLOCATION_DEFINED / ANALOG_CONDITIONING_AND_NATIVE_CAPTURE_OPEN**.

The previous statement that the complete pin budget was resolved without an
expander omitted POWER_ALERT, 5V_PG, 3V3_PG, EXT_PRESENT and POE_PRESENT. No free
non-strapping ESP32 input was assigned to those nets. Preserve the existing
ESP32 peripheral map and add a diagnostic input expander on the existing I2C
bus. This is a design revision, not evidence of a manufactured circuit.

## Input device and pin mapping

Candidate U20: **TI TCA9534PWR**, PW TSSOP-16. A0/A1/A2 (pins 1/2/3) connect to
GND; 7-bit address 0x20. Pin 16 VCC = +3V3_SYS, pin 8 GND, pin 14 SCL,
pin 15 SDA. Fit local 100 nF bypass. MAIN retains sole SDA/SCL pull-up ownership.
INT pin 13 is deliberately NC; the diagnostic firmware polls.

- P0 / pin 4: POWER_ALERT, INA228 active-low open-drain alarm.
- P1 / pin 5: 5V_PG, high means the 5 V regulator asserts power good.
- P2 / pin 6: 3V3_PG, high means the 3.3 V regulator asserts power good.
- P3 / pin 7: EXT_PRESENT, secondary-domain external-source window-valid logic.
- P4 / pin 9: POE_PRESENT, secondary-domain PoE-output-valid logic, sensed before
  the controlled PoE disconnect. It must not be inferred from common +24V_SYS.
- P5 / pin 10: POE_TYPE2_N, optocoupler collector, low means physical-layer
  multiple-event detection only.
- P6 / pin 11: SERVICE_VBUS_PRESENT, conditioned 3.3 V diagnostic logic.
- P7 / pin 12: reserved, tie to GND; never configure as an output.

All eight ports remain inputs. Pull each open-drain status net to +3V3_SYS at
MAIN (10 kOhm design seed, validate rise time/leakage during capture). P3/P4/P6
require explicit input conditioning; never connect 24 V or USB VBUS directly.
Exact conditioning devices, thresholds, power-off leakage and MPNs remain
OPEN. The expander input range is not permission to inject power into an
unpowered 3.3 V domain.

Verified source: [TI SCPS197D](https://www.ti.com/lit/ds/symlink/tca9534.pdf),
pin table, address table and registers 0..3. All ports reset as inputs.
The device has no identity register. Readback verifies configuration only.

## PoE isolation and power permission

Ag53024 pin 3 TYP2_DET is **primary referenced**. The manufacturer uses VIN+
through a current-limiting resistor and optocoupler LED to TYP2_DET. Only the
isolated collector/emitter side may connect to +3V3_SYS/GND and P5. Preserve the
module's isolation barrier in the PCB layout. LED current, optocoupler CTR
over temperature/life, resistor power/voltage rating and creepage/clearance
are not yet calculated or released.

Source: Silvertel *Ag53000 Datasheet V1.1, 2026-06-22*, section 2.3 and Figure 4
(retrieved vendor PDF retained in the source audit). The datasheet also warns
that some PSEs retain the lower power budget until data-link confirmation.
Thus POE_TYPE2_N alone **must not** set governor `type2_verified`. In the
diagnostic application that field stays false and the amplifier stays off.
Qualification requires the implemented classification/negotiation path and
tests on the supported PSEs. The 22.5 W application limit remains a ceiling,
not permission to draw that power from an unqualified PSE.

## Firmware and timing scope

`ap_status_configure` writes configuration 0xFF then polarity 0x00 and checks
both. `ap_status_read` rechecks them before reading register 0; on error it
preserves the caller's value. The app publishes a nullable raw byte plus the
error code and samples at its diagnostic interval. It does not infer source
priority, safety, power permission or calibrated source power from the byte.

No AMP_PDN, reset, regulator-enable, microphone-enable or source-switch output
is driven through U20. Existing external safe-state bias and autonomous source
priority are still required. The final governor needs a separate bounded
fast acquisition schedule, stale-data handling and measured end-to-end
latency; 30-second diagnostic polling does not satisfy that requirement.

## Required evidence before closing the hardware gate

1. Native schematic/ERC: all eight bits, correct supply and address straps,
   individual NCs and PoE isolation visible; no 24 V/USB input directly at U20.
2. Conditioning calculations including worst-case input thresholds, leakage,
   unpowered-domain injection and all source combinations.
3. Oscilloscope captures of each status transition and hardware-safe amplifier
   state through reset, brownout, missing I2C devices and stuck bus.
4. Type-1/Type-2 and supported PSE negotiation tests at the permitted source
   power. Missing or contradictory evidence keeps the amplifier inhibited.
5. Exact BOM and footprints, PCB DRC and independent pin-map review.

This allocation closes the missing *digital destination* in the contract;
it does not close any of the five hardware evidence requirements above.
