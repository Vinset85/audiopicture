# AudioPicture V2.2 Rev.A — rear chimney CFD domain contract

Status: **CFD_DOMAIN_GEOMETRY_CONTRACT_READY / PASSIVE_CONVECTION_SOLVER_REQUIRED / FEA_GATE_REMAINS_OPEN**

## 1. Purpose
Advance the thermal design while structural FEM execution remains unavailable.

This work does not replace or bypass LC1..LC7.

It defines the real fluid-domain geometry and thermal boundary conditions for passive rear-chimney validation.

## 2. Authoritative product envelope
- product 320 x 400 x 40 mm
- nominal wall gap 4 mm
- DML/front system occupies front region
- rear shell inner surface approximately Z37.6..38.0 mm
- structural frame is an obstruction derived from the G2 B-rep.

## 3. Fluid domains
Create separate named domains:
AIR_ROOM_LOWER
AIR_INLET
AIR_REAR_CAVITY
AIR_CHIMNEY_MAIN
AIR_BYPASS_LEFT
AIR_BYPASS_RIGHT
AIR_OUTLET
AIR_WALL_GAP
AIR_SHT45_CHAMBER.

AIR_SHT45_CHAMBER is not merged into the main electronics chimney.

## 4. Lower inlet
Required effective free area after cables:
>=600 mm2.

CAD gross opening must exceed this requirement by allowance for:
- Ethernet cable;
- 24 V cable;
- USB service geometry where relevant;
- structural ribs;
- slot edge/blockage.

Use multiple hidden slots rather than one large visible opening.

## 5. Upper outlet
Seed effective free area:
750 mm2.

Outlet remains hidden/rear-facing.

CFD sweep:
- 50 percent seed area
- 100 percent
- 150 percent.

## 6. Wall gap
Sweep:
- 3 mm
- 4 mm nominal
- 5 mm.

Wall plane is explicitly represented so the rear outlet does not exhaust into an infinite open domain unrealistically.

## 7. Heat sources
Named volumetric/surface heat-source regions:
Q_MAIN_P
Q_MAIN_C
Q_TAS5825M
Q_TPSM63603
Q_POE_AG53024
Q_W5500
Q_ESP32
Q_VOICE
Q_RADAR.

Avoid double counting:
if component-level sources are enabled, subtract them from aggregate MAIN-P/MAIN-C source.

## 8. System heat sweep
Existing system thermal contract:
- 3 W
- 5 W
- 8 W
- 10 W.

Use these as total internal heat scenarios.

The 10 W case is adverse/stress, not claimed nominal operation.

## 9. Ambient cases
- 20 C
- 30 C
- 35 C.

Initial natural-convection study:
ambient pressure, still room air.

## 10. Physics
Required:
- gravity;
- natural convection;
- temperature-dependent air density or validated Boussinesq range;
- solid conduction through relevant frame/shell/PCB simplified bodies;
- surface-to-ambient radiation.

Do not solve pure conduction and label it passive-convection validation.

## 11. Radiation
Use material/emissivity sensitivity until surface finishes are frozen.

Relevant surfaces:
- ASA rear shell;
- PC-CF frame;
- PCB solder mask;
- component packages;
- wall.

Record emissivity assumptions in every run.

## 12. Geometry obstructions
CFD domain must include at least simplified solids for:
- G2 PC-CF frame;
- MAIN-P;
- MAIN-C;
- VOICE;
- RADAR;
- ENV;
- horizontal 470 uF capacitor;
- Ag53024;
- Ethernet cable sweep;
- power harness;
- speaker harness;
- major FPC bundles.

No full-width fictitious porous plate.

## 13. Thermal architecture checks
Verify:
- lower inlet connects to rear cavity;
- vertical chimney remains continuous;
- left/right bypasses are not dead-ended;
- MAIN-P receives useful lower/cooler air;
- MAIN-C does not receive only trapped preheated air;
- upper outlet connects to wall gap/room;
- no recirculating hot pocket behind Ag53024;
- no stagnant hot pocket around TAS5825M/output inductors.

## 14. SHT45 isolation
AIR_SHT45_CHAMBER:
- room-coupled side/lower micro-air path;
- no direct high-flow connection to main hot chimney;
- weak thermal conduction to PC-CF;
- separate time-constant study.

SHT45 reading is ambient/environmental telemetry, not a junction-temperature proxy.

## 15. OPT3004
Optical tunnel is not an airflow shortcut.

Keep optical path and environmental ventilation paths functionally separate.

## 16. Radar
Radar forward RF keep-out remains free of PC-CF/metal.

Thermal airflow geometry shall not introduce conductive mesh/metal grille into RF cone.

## 17. CFD mesh
Initial:
- bulk air 4..6 mm;
- inlet/outlet slots <=1..2 mm local;
- narrow wall gap >=3 cells through gap where solver permits;
- component hot surfaces <=2 mm local;
- boundary-layer/inflation treatment as solver supports.

Run mesh convergence on:
- maximum air temperature;
- MAIN-P local air temperature;
- MAIN-C inlet air;
- representative component temperature;
- mass/volume flow.

## 18. Output metrics
For each case:
- Tmax air;
- Tmax relevant solid;
- MAIN-P inlet air temperature;
- MAIN-C inlet air temperature;
- Ag53024 local air;
- TAS5825M local air;
- outlet temperature;
- volume flow;
- average inlet velocity;
- average outlet velocity;
- pressure difference;
- stagnant-volume fraction;
- heat balance closure;
- effective system thermal resistance.

## 19. Acceptance philosophy
No arbitrary absolute silicon junction pass is claimed from coarse CFD.

Use:
- component datasheet junction/ambient limits;
- board/component thermal models;
- firmware derating thresholds;
- validated CFD.

Architecture-level pass requires:
- continuous buoyancy path;
- no severe stagnant hot pocket;
- heat balance closure;
- temperatures compatible with subsequent detailed component limits;
- SHT45 chamber not dominated by internal heat.

## 20. First CFD matrix
Prioritize:
1. 5 W / 30 C / 4 mm wall gap
2. 8 W / 30 C / 4 mm
3. 10 W / 35 C / 4 mm
4. 8 W / 35 C / 3 mm
5. 8 W / 35 C / 5 mm.

Then inlet/outlet area sweeps.

## 21. Reduced-order pre-CFD sanity
Before solver execution, calculate:
- available inlet/outlet free area;
- characteristic chimney height;
- hydraulic restrictions;
- required air mass flow for selected allowable air-temperature rise.

Use:
Q = m_dot * cp * DeltaT.

This is only a mass/energy sanity check and does not prove natural convection can generate that flow.

## 22. Automatic checks
C211 CFD fluid domain derives from master CAD.
C212 G2 frame included as obstruction.
C213 effective inlet >=600 mm2 after cable blockage.
C214 outlet seed >=750 mm2 effective.
C215 wall gap 3/4/5 mm sweep defined.
C216 SHT45 domain separate.
C217 optical tunnel not counted as ventilation.
C218 radar RF keep-out preserved.
C219 no harness blocks >20 percent local chimney section without explicit study.
C220 heat-source double counting prohibited.
C221 gravity enabled.
C222 convection physics enabled.
C223 radiation included/sensitivity recorded.
C224 wall plane included.
C225 heat balance closure reported.
C226 CFD mesh convergence reported.
C227 stagnant-volume metric reported.
C228 10 W / 35 C adverse case run.
C229 3 mm wall-gap adverse case run.
C230 CFD result does not claim to replace structural FEM.

## 23. State
Structural B-rep: ready.
Structural FEM numerical run: open due solver availability.
CFD geometry/physics contract: ready.
Passive thermal numerical run: requires CFD solver.

Status: **CFD_REAR_CHIMNEY_CONTRACT_READY / C01_TO_C230 / THERMAL_AND_STRUCTURAL_SOLVERS_REMAIN_NUMERICAL_GATES**.
