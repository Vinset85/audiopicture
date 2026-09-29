# AudioPicture V2.2 Rev.A — passive ventilation and acoustic-isolation architecture

Status: **PASSIVE_CHIMNEY_ARCHITECTURE_FROZEN / CFD_SLOT_AREA_AND_ACOUSTIC_LEAKAGE_RELEASE_GATES_OPEN**

## 1. Objective
Define fanless cooling while preserving the 40 mm envelope, DML acoustic separation, hidden appearance, RF zones and wall-mount structure.

## 2. Fundamental rule
No direct low-impedance airflow path is allowed from the front acoustic-fabric volume around the DML edge to the rear electronics cavity.

Maintain a continuous acoustic perimeter seal around the active DML boundary.

Ventilation path:
**room -> hidden lower/rear inlet -> rear electronics cavity -> hidden upper/rear outlet -> room**

## 3. Passive chimney
Use the wall stand-off and rear-shell cavity as a vertical natural-convection chimney:
1. cool air enters at lower rear edge;
2. passes behind/around MAIN-P;
3. rises through open vertical corridors;
4. passes the MAIN-C upper region;
5. exits through upper rear slots.

No fan in the baseline architecture.

## 4. Wall stand-off
Current CFD seed: **4 mm nominal**.
Sweep: **3 / 4 / 5 mm**.

The stand-off shall be controlled by mount/support geometry.

## 5. Inlet slots
Initial total free-area seed: **600 mm2**.
Use multiple hidden lower/rear slots.
Individual slot width seed: **2..3 mm**.

Example geometric equivalent: 10 x 3 x 20 mm.

Actual free area must account for ribs/grills/labyrinths.

## 6. Outlet slots
Initial total free-area seed: **750 mm2**.
Outlet area is intentionally larger than inlet.

Example geometric equivalent: 10 x 3 x 25 mm.

Keep outlets away from structural cleat nodes, ESP32 RF-clean region and the DML acoustic seal.

## 7. Internal flow corridors
Maintain at least one primary vertical corridor and side bypasses where possible.

Do not let cable bundles, FPCs, full-width PC-CF bridges or PCB shelves block the chimney.

## 8. MAIN-P thermal region
Provide an open convective path from TAS5825M/TPSM63603/XAL7050 regions into the vertical chimney.

Do not use the 470 uF capacitor as a flow obstruction and avoid directing the hottest exhaust onto it where layout alternatives exist.

## 9. MAIN-C upper region
CFD shall check Ag53024, W5500, ESP32 and Ethernet magnetics because MAIN-C receives pre-heated rising air.

No conductive thermal spreader may invade the ESP32 antenna keep-out.

## 10. Thermal spreaders
Allowed:
- PCB copper;
- local RF-compatible metal outside radar/ESP32 zones;
- safe local thermal interfaces.

Not baseline:
- full-area rear metal plate;
- metal through radar cone;
- metal across ESP32 antenna keep-out;
- DML as primary heatsink.

## 11. Acoustic isolation
The DML compliant perimeter remains acoustically sealed.

Required:
- continuous PORON or acoustically equivalent seal;
- ventilation slots behind the sealed DML boundary;
- sealed/labyrinth cable penetrations;
- no straight front-to-rear slot adjacent to the DML edge.

Coupled acoustic simulation shall compare leakage cases against a sealed reference before release.

## 12. Labyrinth crossings
Any service/cable path crossing near the acoustic boundary shall use at least two direction changes and compliant cable/FPC sealing.

Open-cell ventilation foam is not the primary DML perimeter seal.

## 13. SHT45 chamber
The SHT45 environmental chamber is separate from the main electronics chimney.

Requirements:
- side/lower passive micro-air chamber;
- thermally isolated carrier;
- hidden openings to room air;
- restricted coupling to MAIN-P hot plume.

## 14. Radar and optical sensor
No conductive/carbon structure enters the radar RF cone.

The OPT3004 optical path is not used as a primary ventilation opening.

## 15. Dust strategy
Do not add a dense filter by default.

Prefer downward/rear-facing slots, labyrinth geometry and cleanable external openings. Any future filter pressure-drop curve must be included in CFD.

## 16. CFD model
Installed vertically against a wall.

Wall-gap sweep:
- 3 mm
- 4 mm
- 5 mm

Internal dissipation:
- 3 W
- 5 W
- 8 W
- 10 W

Ambient:
- 20 C
- 30 C
- 35 C

Model natural convection plus radiation.

Slot-area sweep:
- 50 percent seed
- 100 percent seed
- 150 percent seed

## 17. CFD outputs
Record:
- component/PCB temperatures;
- rear-shell temperature map;
- wall-facing surface temperature;
- inlet/outlet mass flow;
- velocity field;
- recirculation/dead zones;
- air temperature reaching MAIN-C;
- wall-gap sensitivity;
- pressure drop.

## 18. Firmware linkage
CFD shall produce:
- effective steady-state thermal resistance versus power;
- dominant thermal time constants;
- safe sustained dissipation envelope versus ambient.

These parameters feed the adaptive firmware power governor.

## 19. CAD parameters
- WALL_GAP_NOM = 4 mm
- WALL_GAP_SWEEP = 3/4/5 mm
- INLET_FREE_AREA_SEED = 600 mm2
- OUTLET_FREE_AREA_SEED = 750 mm2
- SLOT_WIDTH_SEED = 2..3 mm
- DML_ACOUSTIC_PERIMETER = SEALED
- MAIN_CHIMNEY = VERTICAL_REAR
- ENV_AIR_CHAMBER = SEPARATE_FROM_MAIN_CHIMNEY

## 20. Release gates
1. shared CAD airflow volumes;
2. exact slot geometry;
3. CFD power/ambient sweep;
4. wall-gap sensitivity;
5. rear-shell touch-temperature review;
6. coupled acoustic leakage simulation;
7. RF keep-out verification;
8. SHT45 thermal-bias CFD;
9. update firmware thermal model;
10. freeze production slot/labyrinth geometry.

Status: **4MM_WALL_GAP_CFD_SEED / 600MM2_INLET / 750MM2_OUTLET / SEALED_DML_PERIMETER**.
