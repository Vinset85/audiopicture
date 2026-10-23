# AudioPicture local diagnostic integration — Rev.EZ

Implemented custom integration for Home Assistant **2026.9.4**. It discovers
`_audiopicture._tcp.local.`, verifies UUID/API/model, asks the user to add the
device and exposes seven diagnostic sensors. No YAML or MQTT is required.
Manual host entry is available if multicast discovery is unavailable.

Copy `custom_components/audiopicture` into the Home Assistant configuration's
`custom_components` directory, restart Home Assistant, then accept discovery
or use Add Integration → AudioPicture. This has not been installed on the
user's running Home Assistant. It is not an official built-in integration.

Sensors expose raw temperature, raw humidity, raw illuminance, bus voltage,
current calculated with the nominal 8 mOhm shunt, calculated electrical power
and monitor die temperature. Missing, invalid or stale measurements are
unavailable, never zero-filled. Labels distinguish diagnostics from calibrated
room readings. Network recovery, unload and DHCP-address changes are handled.

Audio playback, stereo pairing, room groups, voice, radar, firmware upload and
room calibration are **not implemented**. Rev.D requires them as product
behaviour: a lone unit plays a mono downmix; two identical units in one room
become LEFT/RIGHT; three or more share one clock and per-unit delay. See
`docs/architecture/v2.2-rev-d-mono-room.md`. No media player entity is created
for the diagnostic firmware, which explicitly advertises those capabilities as
false.

`room.py` is the first piece of the Rev.D room software. It is pure logic and
not yet exposed as entities or services. It validates a room with the same
rules as firmware `ap_room`: one SOLO, or one LEFT/RIGHT pair plus FILL units,
up to 8, same firmware major. From listener distances it computes per-unit
delay (arrival alignment at 343 m/s) and trim (1/r level match). FILL units
get an extra precedence delay, 10 ms and −3 dB by default. Results beyond the
firmware limits of 50 ms and −30 dB are rejected. `payload()` builds the JSON
body for the future device room-plan endpoint. Distances are estimates; the
microphone calibration in Rev.D §4.4 must refine them.

## Tests actually executed

Tests run against the real Home Assistant fixture runtime and an HTTP
loopback server: discovery/config flow, duplicate discovery, confirmation
identity changes, reconnect/unload, malformed and oversized responses,
timeouts/redirects, finite measurement validation and diagnostics redaction.
Room-planner tests cover delay/trim results, every rejection rule and the
limits. Line coverage is 100% of executable statements. This is not branch coverage or
an ESP32/network hardware test. Evidence: `../evidence/rev-ez/`.

Reproduce in a fresh Python 3.14 virtual environment:

```sh
python -m pip install -r requirements-test.txt
pytest --cov=custom_components.audiopicture --cov-report=term-missing
```

The API is read-only HTTP for a trusted diagnostic LAN. It contains no Wi-Fi
passwords or control endpoint. Authentication, encrypted commissioning and
production update security are separate unimplemented product requirements.
