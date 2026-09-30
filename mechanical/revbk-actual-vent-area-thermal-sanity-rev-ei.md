# AudioPicture V2.2 — Rev.BK actual vent-area thermal sanity Rev.EI

Status: **ACTUAL_VENT_AREA_ENERGY_BALANCE_PASS / NATURAL_CONVECTION_CAPACITY_NOT_PROVEN / CFD_SOLVER_GATE_OPEN**

This revision applies the existing reduced-order energy balance to the current Rev.BK vent geometry. It is not CFD.

## Geometry inputs
Exact capsule gross areas already established by the Rev.BK geometry:
- lower inlet bank gross area: 1416.823002 mm2;
- upper outlet bank gross area: 1330.685835 mm2.

Existing effective-area proxies:
- lower inlet: 75% -> **1062.617251 mm2**;
- upper outlet: 80% -> **1064.548668 mm2**.

These proxy factors are modeling assumptions, not measured discharge coefficients.

The current geometry therefore exceeds the pre-CFD architecture goals:
- effective inlet >=900 mm2;
- effective outlet >=1000 mm2.

## Energy-balance assumptions
- cp = 1005 J/(kg K);
- rho = 1.15 kg/m3;
- Q = m_dot cp DeltaT;
- volume flow = m_dot/rho.

| Q W | DeltaT C | mass g/s | volume L/s | inlet velocity m/s | outlet velocity m/s |
|---:|---:|---:|---:|---:|---:|
|3|10|0.2985|0.2596|0.2443|0.2438|
|3|15|0.1990|0.1730|0.1629|0.1626|
|3|20|0.1493|0.1298|0.1221|0.1219|
|5|10|0.4975|0.4326|0.4071|0.4064|
|5|15|0.3317|0.2884|0.2714|0.2709|
|5|20|0.2488|0.2163|0.2036|0.2032|
|8|10|0.7960|0.6922|0.6514|0.6502|
|8|15|0.5307|0.4615|0.4343|0.4335|
|8|20|0.3980|0.3461|0.3257|0.3251|
|10|10|0.9950|0.8652|0.8143|0.8128|
|10|15|0.6633|0.5768|0.5428|0.5419|
|10|20|0.4975|0.4326|0.4071|0.4064|

## Interpretation
Compared with the old 600/750 mm2 minimum architecture, the Rev.BK effective-area proxies materially reduce the mean velocity required for the same energy transport. At 10 W / 15 C, the old inlet screen required about 0.961 m/s; Rev.BK requires about **0.543 m/s** under the same bulk-flow assumption.

This does not prove buoyancy can generate that flow. Labyrinth turns, wall-gap losses, cable blockage, viscous losses and local recirculation remain solver/measurement questions.

No pressure-drop coefficient is invented here.

## Gate
C1776 Rev.BK exact gross inlet area carried forward: 1416.823002 mm2.
C1777 Rev.BK exact gross outlet area carried forward: 1330.685835 mm2.
C1778 effective-area proxy inlet: 1062.617251 mm2.
C1779 effective-area proxy outlet: 1064.548668 mm2.
C1780 current proxy inlet exceeds 900 mm2 architecture goal.
C1781 current proxy outlet exceeds 1000 mm2 architecture goal.
C1782 3/5/8/10 W energy-balance flow calculated for DeltaT 10/15/20 C.
C1783 Rev.BK mean inlet/outlet velocities calculated.
C1784 natural-convection capacity remains unproven.
C1785 CFD solver/mesh-convergence gate remains open.

Status: **THERMAL_REDUCED_ORDER_REV_EI / ACTUAL_REV_BK_AREA_CHECK_COMPLETE / CFD_NUMERICAL_GATE_OPEN / C01_TO_C1785**.
