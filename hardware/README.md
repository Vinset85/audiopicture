# Hardware

AudioPicture V2.2 uses four PCBs: MAIN, VOICE, RADAR and ENV.

## Design status
Rev.A architecture is frozen at block level. Current Rev.A device families are frozen where documented. Remaining release gates include exact passive/MPN selections, XVF3800 reference-derived regulators/flash/support networks, radar reference-derived filter/oscillator details, FPC orientation/suffixes, DML output-filter validation and mechanical/RF/thermal verification.

## KiCad target
The electrical design will be captured sheet-by-sheet:
1. Ethernet / PoE / W5500
2. External 24 V protection and source ORing
3. INA228 and DC/DC rails
4. ESP32-S3
5. TAS5825M and DML outputs
6. XVF3800 / SQ66 microphone array
7. BGT60TR13C radar
8. SHT45 / OPT3004
9. USB-C / boot / recovery
10. Inter-board connectors and production test points
