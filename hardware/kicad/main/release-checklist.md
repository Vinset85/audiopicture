# MAIN Rev.A schematic release checklist

- [ ] Every IC MPN matches BOM.
- [ ] Every package/footprint checked against manufacturer land pattern.
- [ ] ESP32 antenna keep-out implemented.
- [ ] ESP32 strapping states reviewed.
- [ ] W5500 reference termination/clock/reset copied and verified.
- [ ] PoE MagJack/module isolation reviewed.
- [ ] LM74700 source-priority circuit works without MCU.
- [ ] TVS clamp verified.
- [ ] INA228 Kelvin routing represented in PCB constraints.
- [ ] TPSM63603 reference layout followed.
- [ ] TPS62823 inductor/COUT calculated.
- [ ] TAS5825M bootstrap/decoupling exact.
- [ ] TAS5825M LC filter simulated for 8-ohm DML pair.
- [ ] USB-C CC/ESD/service power path verified.
- [ ] Daughterboard FPC pin numbering checked from mating side.
- [ ] Hardware mic mute defaults OFF.
- [ ] Radar cannot be driven while 1.8 V rail is absent.
- [ ] Test points accessible in assembled rear shell.
- [ ] ERC clean with justified exceptions only.
- [ ] BOM contains manufacturer orderable MPNs for all production parts.
- [ ] No VALIDATE component accidentally marked production-ready.


## Native capture gate
- [ ] Review `symbol-footprint-audit.md`.
- [ ] No hand-authored/guessed KiCad native files.
- [ ] Every production footprint verified against manufacturer land pattern before Gerber release.
- [ ] ESP32 module antenna land-pattern/keep-out checked against Espressif drawing.
- [ ] Power-package exposed-pad and thermal-via patterns reviewed.
