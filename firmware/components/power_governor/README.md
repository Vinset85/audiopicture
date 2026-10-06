# Rev.EW portable power governor

Host-tested control core. This component has no production calibration defaults.
The caller must provide verified source identification, current/power samples,
rail-good signals and separate thermal/fault inputs. A positive attenuation
request reduces gain; `amp_pdn_asserted=true` requests hardware shutdown.
Apply shutdown before any DSP writes, and verify actuation feedback/timing in
the hardware layer. Do not infer real amplifier shutdown from this pure C state.

The core rejects a PoE emergency threshold above the application's 22.5 W
continuous ceiling. Measurement accuracy and actuation delay require additional
headroom when selecting the real thresholds. The 18/21 W test settings,
20/40 dB transition/fallback values and 100 ms dwell are synthetic test fixtures.
They are not approved device settings or proof of transient power compliance.

Startup and source changes require stable rails, valid measurements and Type 2
verification for PoE. Rail/input loss, stale/future/non-finite/inconsistent
measurements and scheduler stalls fail closed. A hardware/critical-temperature
fault latches until an explicit reset with stable healthy inputs. Clock wrap is
handled with unsigned differences for configured intervals below 2^31 ms.

The optional calibrated monitor-loss fallback permits only one grace sample
from a previously running state with independent valid voltage/source/rail
inputs; prolonged monitor loss shuts down. A reported power/current emergency
or thermal warning never enters that grace path. Keep `fallback_calibrated`
false until real hardware establishes a safe fixed output ceiling.

Executed tests cover 320 input combinations, timer wrap, missing input,
scheduler stalls, invalid configuration, source handover, fault latching and
200000 deterministic event transitions. Address/undefined-behavior sanitizers
reported no errors. Logs and exact source hashes are in Rev.EW / Rev.ET–EX
validation evidence.

Still required: ESP-IDF application build, INA228 and TAS5825M drivers,
independent source/rail acquisition, fast/slow filtering, DSP gain mapping,
watchdog and task scheduling, calibrated thermal estimation, hardware faults,
OTA/rollback, privacy, factory provisioning, networking and Home Assistant.
SHT45 is not used as internal junction telemetry.
