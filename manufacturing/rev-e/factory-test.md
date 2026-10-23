# AudioPicture Rev.E — factory test and QC

Status: **PROCEDURE_DRAFT**  
Inherits pad philosophy from `manufacturing/factory-test-rev-a.md`; acoustics are DML-specific.

## Sequence

| Step | Test | Pass criteria |
| ---: | --- | --- |
| 1 | Unpowered shorts | No rail short |
| 2 | Program UUID + firmware | Info UUID matches label |
| 3 | 3V3 / 5V / 24V rails | Within ±5 % |
| 4 | Ethernet link | DHCP or fixture static |
| 5 | PoE classification (if fitted) | Class expected; OR-ing OK |
| 6 | SHT45 / OPT3004 / INA228 | In METRICS ranges |
| 7 | Privacy mute | Mic rail off; GPIO Hi-Z policy |
| 8 | Radar presence | Fixture target detect |
| 9 | Amp idle | No fault; TAS PDN sequence |
| 10 | DML impedance sweep | EX_LF and EX_WB within OEM window |
| 11 | Acoustic log sweep 1 m | Factory curve ±3 dB 50 Hz–20 kHz (after cal) |
| 12 | Buzz hunt | No audible rattle at limiter −3 dB |
| 13 | Max SPL short | ≥95 dB @ 100 Hz–1 kHz band centre without protect trip |
| 14 | Room role write | SOLO plan accepted; reboot persistent |
| 15 | Final | Seal, pack, serialize |

## Acoustic station

Anechoic or hemi-anechoic preferred; wall baffle fixture matching product stand-off. Use product mics only for relative checks; reference mic for factory curve.

Fail-closed: any buzz, any rail fault, any mute failure → scrap or rework, never ship.
