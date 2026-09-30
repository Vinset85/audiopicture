# AudioPicture V2.2 Rev.A — first real CAD-kernel generation

Status: **REAL_OPENCASCADE_BREP_GENERATED / VALID_SOLIDS / CONNECTIVITY_FAIL_2_BODIES / NOT_FEA_RELEASED**

## 1. Method
The G2 frame was generated with CadQuery using the OpenCASCADE 7.9 STEP processor available in the engineering environment.

This is a real B-rep/STEP generation attempt, not a hand-written STEP or mesh-only approximation.

## 2. Geometry included
- outer ring;
- two upper cleat islands;
- four M4 bosses with bores;
- left/right waypoint rails;
- mid open-web bridges;
- lower bridges;
- lower support nodes;
- central anti-lift boss/path;
- coarse EX25FHE2 hard keep-outs;
- coarse radar hard keep-out;
- lower service recess;
- perimeter-biased legal restoration webs.

## 3. Iteration results
Initial generation:
- valid solids: 4
- total volume: 82.86 cm3
- mass sensitivity 1.15..1.25 g/cm3: 95.3..103.6 g.

Restoration iteration 1:
- valid solids: 3
- volume: 84.32 cm3
- mass sensitivity: 97.0..105.4 g.

Restoration iteration 2:
- valid solids: 2
- volume: 86.56 cm3
- mass sensitivity: 99.5..108.2 g.

All returned bodies are individually valid, but C171 requires one connected primary structural body.

## 4. Engineering conclusion
**C171 FAIL**

The current waypoint/open-web topology is not yet a valid FEA release geometry.

Do not solve LC1..LC7 on this model as though it were one frame.

The real CAD-kernel test has revealed that hard keep-out subtraction severs at least one part of the structural network.

## 5. Mass conclusion
Even the latest real B-rep remains far below the 250 g frame target.

Therefore the next correction may add legal structural material without creating a mass-budget concern.

The previous pre-CAD 58..65 cm3 estimate underpredicted the generated geometry; the real diagnostic B-rep is currently 86.56 cm3 before final topology correction.

This difference is accepted as a diagnostic update, not hidden.

## 6. Required next action
Identify the remaining disconnected body by component bounding box/centroid and trace which hard subtraction creates separation.

Then:
1. modify the responsible rail/bridge path;
2. rebuild from master primitives;
3. reapply all hard keep-outs;
4. require solid_count == 1;
5. validate manifoldness;
6. compute true volume/mass/bounding box;
7. only then export FEA_FRAME and run LC1..LC7.

## 7. Release state
G2 text topology contract: PASS.
Real CAD generation: PASS.
Individual B-rep validity: PASS.
Primary-body connectivity: FAIL.
FEA release: BLOCKED.
Manufacturing release: BLOCKED.

Status: **OPEN_CASCADE_REAL_GEOMETRY / 2_VALID_BODIES_REMAIN / MASS_APPROX_100_TO_108G / CONNECTIVITY_REDESIGN_REQUIRED**.


## 8. Connectivity closure — iteration 3
Disconnected-body diagnostic:
- isolated body volume: 1.196 cm3;
- isolated body CAD centroid approximately (100.5,-142.5,3.0) in centered CAD coordinates;
- product centroid approximately (260.5,57.5,3.0) mm;
- bounding region approximately product X224.9..296.1, Y53.6..61.4;
- identified feature: right lower open-web bridge LB2.

Root cause:
LB2 from the service-right jamb toward the right perimeter did not physically intersect the lower/right primary network after hard keep-out subtraction.

Correction:
- add a local perimeter-biased connector from the LB2 right endpoint near product (296,60) to the lower/right ring near (296,28);
- width 4 mm seed;
- structural depth 6 mm;
- reapply all hard keep-outs after union.

Iteration 3 result:
- primary solid count: **1**
- B-rep validity: **PASS**
- volume: **86.990 cm3**
- mass sensitivity:
  - 1.15 g/cm3 -> 100.04 g
  - 1.20 g/cm3 -> 104.39 g
  - 1.25 g/cm3 -> 108.74 g
- structural bounding box: **312 x 392 x 8 mm**

C171: **PASS**
C164: **PASS at kernel validity/manifold diagnostic level**
C163 mass <=250 g: **PASS with large margin**

The prior connectivity failure is therefore closed without adding a central spine, crossing an exciter keep-out or altering the hard keep-out set.

## 9. Current release interpretation
The generated STEP is now a valid **G2 structural DMU B-rep** and may be used as the source for the first structural mesh preparation.

It is not yet a manufacturing release because:
- exact manufacturer solids are still an import gate;
- semantic face-group persistence must be implemented in the solver/CAD handoff;
- PC-CF orthotropic properties require sensitivity/coupon calibration;
- LC1..LC7 have not yet been solved.

Updated status:
**OPEN_CASCADE_ONE_VALID_PRIMARY_SOLID / 86P990CM3 / MASS_100_TO_109G / 312X392X8 / FEA_MESH_PREPARATION_READY**.
