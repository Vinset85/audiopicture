# AudioPicture

Smart acoustic picture / complete Home Assistant room node.

**V2.2 target:** 320 x 400 x 40 mm, DML audio, far-field voice, 60 GHz presence sensing, temperature/humidity/light sensing, Ethernet + Wi-Fi, PoE+ + 24 V external power, automatic acoustic calibration and plug-and-play Home Assistant integration.

## Project areas
- `hardware/` — electronics, BOM and KiCad design
- `mechanical/` — enclosure, DML panel and front-frame design
- `firmware/` — ESP32-S3 diagnostic implementation; production functions remain open
- `home-assistant/` — AudioPicture Home Assistant integration
- `manufacturing/` — factory provisioning and test
- `docs/` — architecture and engineering specifications

## Current status
**V2.2 Rev.A engineering.** Architecture-level decisions are tracked as `FROZEN`; parts and values requiring reference-design/layout verification are tracked as `VALIDATE`.

See `docs/architecture/v2.2-rev-a.md` and `hardware/bom/audiopicture-v2.2-rev-a.csv`.

## Digital validation checkpoint Rev.EN–EY

Rev.EM export/reimport is reproduced, but its labyrinth treatment fails:
only 4/22 vents have full chamber-footprint coverage, and 22/22 axial rays
are open. Fluid connectivity is not labyrinth treatment.

Rev.EQ is a verified geometric candidate with 22 stepped cells, not a
production freeze. Rev.ES corrects a conservative ESP32 RF-mask intrusion
in the frame kernel. Full-product structural/thermal, exact DMU/RF,
native electronics, material/process and physical qualification gates remain open.

See `mechanical/digital-validation-rev-en-es.md` and
`mechanical/test/physical-qualification-rev-er.json`.

Rev.EY adds real full-candidate frame screens, three mesh levels, 27 orthotropic
sensitivities, CG cases and buckling. EU.4 fails mass, torsion and
baffle clearance. EU.8, EU.9 and EU.10 recover mass/clearance but fail torsion; these
candidates are not fabrication-ready. Elmer natural-convection
benchmarks now converge and reproduce a published reference, but product CFD
is still OPEN. A portable power-governor core is host-tested; complete
ESP-IDF firmware, native electronics and Home Assistant remain OPEN.

## Checkpoint Rev.EZ — 2026-10-05

EU.11 recovers coarse geometry/mass/clearance but still fails the 1 mm LC4
criterion (1.544203 mm); no qualified frame is released. ENV native electrical
capture passes actual KiCad ERC and an independent pin-netlist check. Its
normal front optical path fails the DML geometric interference audit and PCB
integration remains open. Diagnostic ESP32-S3 firmware is actually compiled;
three host suites and 32 Home Assistant integration tests pass. Full product
firmware, all PCBs, native MAIN/VOICE/RADAR, qualified mechanics, full-product
CFD and physical qualification are still incomplete.

Evidence and remaining dependencies at that revision: `mechanical/digital-validation-rev-ez.md`
and `mechanical/validation/rev-ez/gate-register.json`.

## Current checkpoint Rev.FA — 2026-10-06

A perimeter optical-island candidate clears the DML and a conservative +/-35
degree field of view. Carrier/coupon STEP reimport and STL integrity pass;
retention, interconnect, PCB split, baffle and physical calibration remain open.
EU.12 improves the LC1 normalized displacement to 1.337438 mm at 246.086 g
calculated mass, but still fails the LC4 corner limit: 1.455950 mm vs 1 mm.
Its executed nonlinear LC3 outward-pull screen also predicts DML interference
(20.933640 mm maximum displacement without DML contact). EU.12 is rejected
for assembly; improved vertical stiffness does not qualify the candidate.
No production CAD, qualified structural acceptance or product CFD is claimed.

Latest evidence and work still required:
`mechanical/digital-validation-rev-fa.md`,
`mechanical/optical-perimeter-candidate-rev-fa.md` and
`mechanical/validation/rev-fa/gate-register.json`.
