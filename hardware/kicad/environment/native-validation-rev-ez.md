# ENV native capture — Rev.EZ, 2026-10-05

**Electrical capture verified; PCB and product integration not released.**
The environment-specific capture contract permits validated automation.
The native GUI seed and official KiCad 9.0.8 demo supply symbol/no-connect
templates; kicad-skip 0.2.5 imports official library objects and connects them.
No handwritten schematic syntax or fabricated KiCad execution is used.

Actual KiCad 9.0.8 CLI ERC: **0 errors, 0 warnings, 0 exclusions**.
Independent KiCad XML netlist check: **10 non-power components, 4 connected
nets, 26 connected pins and 3 explicit no-connect pins**. The GUI also opened
the complete capture without recovery/import errors; its Save command was
issued. The saved automation generator tag is retained honestly.

Verified nets: J301 pins 1/2 supply, 3/4 ground, 5 SDA, 6 SCL; U301 pins
1 SDA, 2 SCL, 3 VDD, 4 VSS; U302 pins 1 VDD, 2 ADDR to VDD (0x45), 3 ground,
4 SCL, 6 SDA, 7 exposed pad to ground. J301 pins 7/8 and U302 pin 5 are
explicit NC. C303 is DNP. MAIN owns I2C pull-ups. Two PWR_FLAG symbols mark
the incoming supply and return from J301.

OPT3004 footprint was created, saved and reloaded using KiCad pcbnew 9.0.8:
six oval 0.50 x 0.25 mm lands at X +/-0.95 and Y -0.65/0/+0.65; exposed pad
0.65 x 1.35 mm; separate paste aperture 0.62 x 1.25 mm, 88.319% coverage.
Source: [TI OPT3004, DNP0006A drawing 4221434/C](https://www.ti.com/lit/ds/symlink/opt3004.pdf).
Mask expansion 0.05 mm and courtyard are design seeds; vias, stencil and
assembly process remain to be qualified. The footprint is not a finished PCB.

SHT45 uses the four-pin no-central-pad footprint: no copper/solder underneath
the central die pad. The [current Sensirion datasheet v7.3](https://sensirion.com/resource/datasheet/sht4x)
corrects the membrane description to polyimide; older product text still says
PTFE. The reel ordering code is SHT45-AD1F-R2, article 3.000.886.

Catalog selections: C301/C302 [TDK C1608X7R1H104K080AA](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H104K080AA),
100 nF +/-10%, X7R, 50 V, 0603; optional DNP C303
[TDK C1608X7R1C105K080AC](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1C105K080AC),
1 uF +/-10%, X7R, 16 V, 0603. Both listed Production when checked.
These nominal catalog properties do not establish effective capacitance,
layout, reflow qualification or permission to order parts.

## Reproduce

Run `automation/complete_env_schematic.py` with the archived native seed,
official KiCad demo and installed KiCad libraries. Then run KiCad CLI
`sch erc --format json --severity-all --exit-code-violations` and
`sch export netlist --format kicadxml`. Pass both outputs to
`automation/verify_env_netlist.py`. For the land pattern use
`automation/create_opt3004_footprint.py` with KiCad's bundled Python.
Raw reports are in `../../../evidence/rev-ez/`.

## Open integration gates

PCB outline, placement/routing/DRC, capacitor lands/placement, FPC contact
orientation, room-air chamber, optical tunnel, copper thermal bridges and
actual sensor tests remain OPEN. The current ENV XY seed is entirely behind
the DML; the geometric normal optical path FAIL is recorded in
`env-optical-path-audit.json`. No optical transmittance is invented.
