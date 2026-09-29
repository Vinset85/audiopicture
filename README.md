# AudioPicture

Smart acoustic picture / complete Home Assistant room node.

**V2.2 target:** 320 x 400 x 40 mm, DML audio, far-field voice, 60 GHz presence sensing, temperature/humidity/light sensing, Ethernet + Wi-Fi, PoE+ + 24 V external power, automatic acoustic calibration and plug-and-play Home Assistant integration.

## Project areas
- `hardware/` — electronics, BOM and KiCad design
- `mechanical/` — enclosure, DML panel and front-frame design
- `firmware/` — ESP32-S3 production firmware
- `home-assistant/` — AudioPicture Home Assistant integration
- `manufacturing/` — factory provisioning and test
- `docs/` — architecture and engineering specifications

## Current status
**V2.2 Rev.A engineering.** Architecture-level decisions are tracked as `FROZEN`; parts and values requiring reference-design/layout verification are tracked as `VALIDATE`.

See `docs/architecture/v2.2-rev-a.md` and `hardware/bom/audiopicture-v2.2-rev-a.csv`.
