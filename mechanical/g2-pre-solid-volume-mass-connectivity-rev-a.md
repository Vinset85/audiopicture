# AudioPicture V2.2 Rev.A — G2 pre-solid volume, mass and connectivity

Status: **G2_PRE_SOLID_TOPOLOGY_PASS / MASS_ESTIMATE_WELL_BELOW_250G / TRUE_BREP_AND_FEA_PENDING**

## 1. Purpose
Perform a numerical pre-CAD check before generating the final watertight PC-CF B-rep.

This is not the released CAD mass and not a structural result. It is a topology sanity check using dimensioned primitives from the G2 primitive/node maps.

## 2. Simplified structural primitives
Seed calculation includes:
- closed outer ring;
- two side rails;
- open-web mid/lower bridges;
- two cleat islands;
- four M4 boss volumes;
- representative local gussets.

It intentionally does not claim exact boolean overlap, fillet, cutout or keep-out volume.

## 3. Outer ring seed
Approximate structural projected outer size:
- 312 x 392 mm class
- ring width 10 mm
- thickness 2.4 mm

Calculated raw ring volume:
**32,832 mm3 = 32.83 cm3**

## 4. Rib/bridge seed
Representative combined centerline lengths:
- side rails and structural bridges approximately 1,193 mm total in this pre-model.

Using:
- web 2.8 mm
- average structural depth 7 mm

Raw rib/bridge volume:
**23,383 mm3 = 23.38 cm3**

## 5. Cleat islands
Two representative islands:
- 54 x 28 x 3.2 mm

Raw volume:
**9,677 mm3 = 9.68 cm3**

This is intentionally conservative because final islands will be sculpted/opened.

## 6. M4 boss seed
Four bosses:
- OD 11 mm
- depth 7 mm

Raw cylindrical volume before insert bores:
**2,661 mm3 = 2.66 cm3**

Actual PC-CF volume will be lower after insert-hole subtraction.

## 7. Gusset seed
Representative eight triangular gussets:
- 25 x 12 mm projected triangle
- 3.2 mm thickness

Raw volume:
**3,840 mm3 = 3.84 cm3**

## 8. Gross primitive volume
Before boolean overlap subtraction:
**72,393 mm3 = 72.39 cm3**

Because ring, rails, islands and gussets deliberately overlap at load nodes, gross primitive summation double-counts material.

## 9. Boolean-overlap sensitivity
Until true CAD boolean union exists, use a 10/15/20 percent overlap correction.

Net volume estimate:
- 10 percent correction: 65.15 cm3
- 15 percent correction: 61.53 cm3
- 20 percent correction: 57.91 cm3

Working pre-CAD volume band:
**~58..65 cm3**

## 10. Mass sensitivity
Do not freeze material density from this document.

For numerical sensitivity only, using 1.15 / 1.20 / 1.25 g/cm3:

At 10 percent overlap:
- ~74.9 / 78.2 / 81.4 g

At 15 percent overlap:
- ~70.8 / 73.8 / 76.9 g

At 20 percent overlap:
- ~66.6 / 69.5 / 72.4 g

Working pre-CAD frame mass estimate:
**~67..81 g**

This is not a manufacturer material-property claim. Final mass comes from released CAD volume multiplied by qualified printed-part density or direct measured part mass.

## 11. Budget interpretation
Existing structural frame target:
**<=250 g**

Current pre-CAD estimate is roughly one-third or less of that limit.

Consequence:
- mass budget is not currently the governing constraint;
- FEA stiffness, mount-node strength, print anisotropy and vibration behavior should drive local reinforcement;
- do not remove material merely to chase a lower mass before structural analysis.

A final frame mass significantly above this estimate may still be acceptable if <=250 g and system CG/mass budgets pass.

## 12. Connectivity graph
Define structural graph nodes:
- CL = left cleat island
- CR = right cleat island
- TL = top/left outer ring
- TR = top/right outer ring
- LR = left rail
- RR = right rail
- CM = central open-web network
- LL = lower-left ring
- RL = lower-right ring
- AL = anti-lift U-path
- PL = lower-left support
- PR = lower-right support

Required graph edges:
- CL-TL
- CL-LR
- CR-TR
- CR-RR
- TL-TR through top ring
- LR-LL
- RR-RL
- LR-CM
- CM-RR
- LL-AL
- AL-RL
- LL-PL
- RL-PR

This graph is connected without requiring:
- a central full-height spine;
- a full rear deck;
- a bridge through an exciter column.

## 13. Independent cleat-path requirement
Each cleat has two local paths:
LEFT:
1. CL -> TL -> top ring
2. CL -> LR -> lower/perimeter network

RIGHT:
1. CR -> TR -> top ring
2. CR -> RR -> lower/perimeter network

Exact geometric independence is checked after B-rep generation and keep-out subtraction.

## 14. Hard failure conditions
Pre-solid generation fails if any of the following occurs:
- boolean union creates disconnected primary frame bodies;
- L1 subtraction severs left rail without legal restoration;
- radar RF subtraction severs right mount load path;
- service opening severs lower anti-lift path;
- airflow subtraction creates a disconnected mount island;
- a restoration bridge intersects an exciter/RF/service hard keep-out.

## 15. Watertight B-rep requirements
The generated structural solid shall:
- be one valid closed primary solid where feasible;
- have no self-intersections;
- have no zero-thickness faces;
- have no non-manifold edges;
- retain explicit insert bores;
- retain hard keep-out clearances;
- remain within Z<=40 mm product envelope.

Separate compliant/non-structural carrier parts are not fused into the primary PC-CF body merely to satisfy connectivity.

## 16. Mass-property outputs from true CAD
Once B-rep exists, record:
- volume;
- surface area;
- centroid;
- inertia tensor;
- material-assigned mass;
- bounding box;
- minimum wall/rib thickness;
- disconnected-body count.

Compare true CAD volume against pre-CAD 58..65 cm3 band.

If difference >25 percent, classify why:
- overlap estimate;
- deeper ribs;
- keep-out subtraction;
- mount reinforcement;
- shell/frame interface;
- modeling error.

## 17. FEA readiness gate
Before meshing:
- geometry validity PASS;
- one-primary-body connectivity PASS;
- cleat dual paths PASS;
- exciter/RF/service keep-outs PASS;
- mass properties recorded;
- named boundary faces generated.

Then export FEA_FRAME from the same master geometry.

## 18. New automatic checks
C156 primary structural connectivity graph complete.
C157 left cleat has two independent local paths.
C158 right cleat has two independent local paths.
C159 anti-lift remains connected after service subtraction.
C160 lower pads remain connected to perimeter.
C161 pre-CAD net volume recorded.
C162 true CAD volume compared against pre-CAD band.
C163 true frame mass <=250 g.
C164 B-rep has zero non-manifold edges.
C165 B-rep has zero zero-thickness structural connections.
C166 insert bores do not sever boss walls.
C167 hard keep-out subtraction does not disconnect cleat island.
C168 FEA boundary faces remain uniquely named after boolean rebuild.
C169 structural centroid/inertia exported.
C170 no structural reinforcement is added solely to match the pre-CAD mass estimate.

## 19. Result
Topology sanity:
**PASS**

Pre-CAD volume:
**~58..65 cm3**

Pre-CAD mass sensitivity:
**~67..81 g**

Mass target:
**<=250 g**

Interpretation:
The current frame concept has substantial mass headroom. Structural optimization should therefore prioritize stiffness, boss/insert strength, print-direction robustness, vibration control and service/RF/thermal compatibility rather than aggressive lightweighting.

Status: **G2_PRE_SOLID_58_TO_65CM3 / MASS_SENSITIVITY_67_TO_81G / CONNECTED_LOAD_GRAPH / C01_TO_C170 / TRUE_BREP_NEXT**.
