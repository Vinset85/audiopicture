# AudioPicture

Smart acoustic picture / complete Home Assistant room node.

**V2.2 target:** 320 x 400 x 40 mm, DML audio, far-field voice, 60 GHz presence sensing, temperature/humidity/light sensing, Ethernet + Wi-Fi, PoE+ + 24 V external power, automatic acoustic calibration and plug-and-play Home Assistant integration.

**Current verified checkpoint: [Rev.FD](mechanical/digital-validation-rev-fd.md).** The user-authorized mass increase supersedes the 250 g frame target. EU.20 passes the four-corner normalized displacement screen; production qualification remains OPEN.

## Project areas
- `hardware/` — electronics, BOM and KiCad design
- `mechanical/` — enclosure, DML panel and front-frame design
- `firmware/` — ESP32-S3 diagnostic implementation; production functions remain open
- `home-assistant/` — AudioPicture Home Assistant integration
- `manufacturing/` — factory provisioning and test
- `docs/` — architecture and engineering specifications

## Architecture baseline
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

## Checkpoint Rev.FA — 2026-10-06

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

## Checkpoint Rev.FB — 2026-10-07

Six actual LC1/LC3/LC4 runs compare EU.13 cruciform ribs and EU.14 intermediate
rail-to-perimeter ties. Both reduce LC3 displacement and show no sampled-node
DML interference; this does not qualify continuous deformed clearance. EU.13
fails mass (268.514 g), and both fail the 1 mm LC4 corner limit (1.412146 and
1.434103 mm). EU.14 mass is 249.525 g before unfinished interfaces. Neither
candidate is released for assembly. Registry: 38 PASS / 17 FAIL / 15 OPEN,
including historical and explicitly scoped diagnostic results.

See [Rev.FB report](mechanical/digital-validation-rev-fb.md),
[gate register](mechanical/validation/rev-fb/gate-register.json) and
[checkpoint publication policy](docs/validation-checkpoints.md).
The [complete Rev.FA baseline](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fa-2026-10-06)
is published: all 10 attachment sizes and SHA-256 digests match local files.
The [Rev.FB supplement](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fb-2026-10-07)
is also published: all 3 attachment sizes and SHA-256 digests are verified.
Receipts: `evidence/rev-fa/github-publication.json` and
`evidence/rev-fb/github-publication.json`.

## Checkpoint Rev.FC — 2026-10-07

Four new CAD candidates and five actual CalculiX runs are consolidated.
EU.18 weighs 249.328 g at catalog density but fails LC4 on both meshes:
1.389561 mm / 1.392602 mm versus 1 mm; the displacement difference is 0.218%.
LC1 is 7.179289 mm and LC3 is 8.952446 mm maximum normalized displacement.
No sampled LC3 node enters the DML; continuous deformed clearance is open.
EU.15 fails mass and torsion, EU.16 is CAD-only, EU.17 meshing failed twice.
No candidate is released for assembly. Registry: 47 PASS / 23 FAIL / 17 OPEN,
including historical and scoped diagnostics, not a completion percentage.

The 250 g frame target originated as a system mass allocation, excluding
inserts and metal cleats; it is not a material limit. The historical 1.55 kg
system budget is stale. Mass must be reviewed together with stiffness and
complete-assembly CAD; no new target or assembled mass is released.

See [Rev.FC results](mechanical/digital-validation-rev-fc.md),
[mass-budget review](mechanical/system-mass-review-rev-fc.md),
[gate register](mechanical/validation/rev-fc/gate-register.json) and
[publication status](docs/validation-checkpoints.md).

The [Rev.FC supplement](https://github.com/Vinset85/audiopicture/releases/tag/checkpoint-rev-fc-2026-10-07)
is published: all three asset sizes and SHA-256 digests are verified against
GitHub. Receipt: `evidence/rev-fc/github-publication.json`.

## Current checkpoint Rev.FD — 2026-10-08

The [mass policy](mechanical/mass-policy-rev-fd.md) removes the 250 g rejection
gate without inventing a replacement ceiling. Mass/CG and load adequacy remain
tracked; 70 N is the minimum vertical seed, with actual additional 90 N screens.

Two CAD candidates, four meshes and 13 new CalculiX runs are verified. EU.19
weighs 442.655 g at catalog density and still fails LC4: 1.006463 / 1.004060 mm.
EU.20 weighs 456.315 g and passes the normalized four-corner 30 N displacement
screen: LR 0.953041, LL 0.955552, UL 0.163397, UR 0.166741 mm. Fine-mesh LR is
0.957329 mm, a 0.448% two-mesh change. This does not qualify stress, real mounts,
material/process, full LC1–LC7 sensitivity/buckling, or production readiness.

EU.20 LC1 maxima are 2.314278 mm at 70 N and 2.975500 mm at 90 N; nonlinear
LC3 outward-pull maximum is 2.049186 mm. A conservative Bernstein enclosure
checks every full quadratic FEA element against the fixed DML box at final
LC3 load: no overlapping bounds, at least 0.324156 mm modeled separation.
Exact deformed CAD, tolerances and physical assembly clearance remain open.

Registry including history: 64 PASS / 25 FAIL / 18 OPEN. Eight historical
mass-only gates are explicitly superseded; counts are not completion percentages.
See the [report](mechanical/digital-validation-rev-fd.md),
[register](mechanical/validation/rev-fd/gate-register.json), and
[publication record](docs/validation-checkpoints.md).
