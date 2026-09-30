# AudioPicture V2.2 Rev.A — passive airflow reduced-order sanity check

Status: **ENERGY_BALANCE_PLAUSIBLE / NATURAL_CONVECTION_FLOW_NOT_YET_PROVEN / CFD_REQUIRED**

## 1. Purpose
Use first-principles energy balance to estimate the air flow required to remove 5/8/10 W for selected bulk air temperature rises.

This does not prove that buoyancy can generate the required flow.

## 2. Assumptions
Air specific heat:
cp = 1005 J/(kg K)

Representative air density:
rho = 1.15 kg/m3

Equation:
Q = m_dot * cp * DeltaT

Thus:
m_dot = Q / (cp * DeltaT)

Volumetric flow:
V_dot = m_dot / rho

Conversion:
1 m3/s = 2118.88 CFM.

## 3. Required flow table

| Heat | DeltaT | Mass flow | Volume flow | CFM |
|---:|---:|---:|---:|---:|
| 5 W | 10 C | 0.4975 g/s | 0.433 L/s | 0.917 |
| 5 W | 15 C | 0.3317 g/s | 0.288 L/s | 0.611 |
| 5 W | 20 C | 0.2488 g/s | 0.216 L/s | 0.459 |
| 8 W | 10 C | 0.7960 g/s | 0.692 L/s | 1.467 |
| 8 W | 15 C | 0.5307 g/s | 0.461 L/s | 0.978 |
| 8 W | 20 C | 0.3980 g/s | 0.346 L/s | 0.733 |
| 10 W | 10 C | 0.9950 g/s | 0.865 L/s | 1.834 |
| 10 W | 15 C | 0.6633 g/s | 0.577 L/s | 1.223 |
| 10 W | 20 C | 0.4975 g/s | 0.433 L/s | 0.917 |

## 4. Mean velocity through 600 mm2 inlet
Area:
A = 600 mm2 = 0.0006 m2.

Representative cases:
- 5 W / 15 C: 0.481 m/s
- 8 W / 15 C: 0.769 m/s
- 10 W / 15 C: 0.961 m/s
- 10 W / 20 C: 0.721 m/s.

These are average free-area velocities if all flow passes through exactly 600 mm2.

## 5. Mean velocity through 750 mm2 outlet
Area:
A = 750 mm2 = 0.00075 m2.

Representative cases:
- 5 W / 15 C: 0.385 m/s
- 8 W / 15 C: 0.615 m/s
- 10 W / 15 C: 0.769 m/s
- 10 W / 20 C: 0.577 m/s.

## 6. Interpretation
The required volumetric flow is sub-1 L/s across all selected cases.

This is not intrinsically absurd for a 400 mm class passive chimney, but the 600 mm2 inlet is restrictive enough that the 10 W / 10..15 C cases demand substantial average inlet velocity.

Therefore:
- 600 mm2 remains a minimum, not an optimization target;
- increasing gross/effective inlet area can materially reduce pressure loss;
- the outlet should not be smaller than the inlet;
- 750 mm2 outlet seed is directionally correct;
- CFD must determine whether buoyancy pressure is sufficient.

## 7. Stack-pressure sanity equation
For small temperature differences, approximate buoyancy pressure:
DeltaP_stack ~= rho * g * H * DeltaT / T.

Use only as an order-of-magnitude screen.

Representative:
- H = 0.35 m
- T = 303 K
- rho = 1.15 kg/m3.

Then:
- DeltaT 10 C -> ~0.130 Pa
- DeltaT 15 C -> ~0.195 Pa
- DeltaT 20 C -> ~0.260 Pa.

Available passive driving pressure is therefore only a few tenths of a pascal.

This confirms why slot/cable/rib pressure losses are critical.

## 8. Ideal-orifice upper-bound screen
If one unrealistically treats an opening as an ideal orifice:
V_dot ~= Cd * A * sqrt(2*DeltaP/rho).

Using Cd = 0.60 only as a screening value and A=600 mm2:
- at 0.130 Pa -> ~0.171 L/s
- at 0.195 Pa -> ~0.210 L/s
- at 0.260 Pa -> ~0.242 L/s.

These idealized values are below many 8/10 W required-flow cases and real labyrinth slots will add further loss.

Do not interpret this simplified orifice model as a full chimney prediction; distributed stack flow is not a single sharp-edged orifice.

## 9. Design consequence
The current 600 mm2 inlet minimum should be reconsidered upward for thermal robustness.

Recommended CFD geometry sweep:
- inlet 600 mm2
- inlet 900 mm2
- inlet 1200 mm2

Outlet:
- 750 mm2
- 1000 mm2
- 1500 mm2.

Preferred architecture goal before CFD:
**effective inlet >=900 mm2 and effective outlet >=1000 mm2 if packaging/cosmetics permit.**

This is a design recommendation from the reduced-order screen, not a validated thermal requirement.

## 10. Wall-gap implication
The 4 mm rear wall gap provides a broad flow region, but local entry/exit contractions may dominate.

CFD shall explicitly include:
- slot contraction;
- cable blockage;
- lower service recess;
- wall plane;
- upper exhaust turn.

## 11. Firmware implication
If passive thermal capacity is below the 10 W adverse case, this is compatible with the existing governor architecture:
- warning;
- DSP/power derating;
- thermal derating;
- shutdown/hysteretic recovery.

Do not increase vent size indefinitely at the expense of acoustics/RF/water/dust behavior; use thermal governance where appropriate.

## 12. Automatic checks
C231 required mass flow calculated from energy balance.
C232 5 W cases evaluated.
C233 8 W cases evaluated.
C234 10 W cases evaluated.
C235 DeltaT 10/15/20 C evaluated.
C236 inlet mean velocity calculated.
C237 outlet mean velocity calculated.
C238 stack-pressure order-of-magnitude calculated.
C239 ideal-orifice result labeled non-authoritative.
C240 600 mm2 retained as minimum only.
C241 900/1200 mm2 inlet CFD sweep added.
C242 1000/1500 mm2 outlet CFD sweep added.
C243 wall-plane restriction remains in CFD.
C244 cable blockage remains in CFD.
C245 thermal governor remains a valid system-level mitigation.

## 13. Result
Energy removal requires approximately:
- 0.22..0.43 L/s at 5 W;
- 0.35..0.69 L/s at 8 W;
- 0.43..0.87 L/s at 10 W,
for DeltaT 20..10 C.

The existing 600/750 mm2 architecture is not disproven, but the passive pressure budget is tight enough that larger effective openings should be evaluated.

Status: **PASSIVE_FLOW_ENERGY_BALANCE_COMPLETE / 600MM2_INLET_IS_MINIMUM_NOT_TARGET / CFD_SWEEP_600_900_1200_AND_750_1000_1500 / C01_TO_C245**.
