# AudioPicture V2.2 — CFD solver availability and next numerical gate Rev.EH

Status: **CFD_GEOMETRY_READY / NUMERICAL_SOLVER_UNAVAILABLE_IN_CURRENT_RUNTIME / NO_THERMAL_RESULT_CLAIMED**

**Superseded environment/readiness assessment (Rev.EN–ES):** Gmsh 4.15.2
and native Elmer are now installed. Rev.EM/EC is not a full-product CFD
domain, and historical sampled LOS does not prove labyrinth treatment.
Natural-convection regression reference matching includes a coupled-convergence
warning; radiation regression matches its reference. No AudioPicture CFD
matrix has been solved. See `digital-validation-rev-en-es.md`.

A local runtime capability audit was executed before attempting any thermal CFD.

Available:
- Python 3.13.5;
- CadQuery 2.8.0;
- VTK 9.6.2.

Not available in the current runtime:
- gmsh executable;
- gmsh Python module;
- OpenFOAM blockMesh;
- snappyHexMesh;
- simpleFoam;
- buoyantSimpleFoam;
- buoyantPimpleFoam;
- foamRun;
- cfMesh / cartesianMesh;
- meshio;
- PyVista;
- FEniCS / dolfinx.

Engineering consequence:
no natural-convection CFD result, mesh-convergence result, pressure-drop result, flow-rate result, or thermal pass/fail may be claimed from this runtime.

Geometry gates already closed and usable as CFD inputs:
- Rev.EC/EE valid BREP fluid topology;
- one main fluid component;
- 22/22 vents connected;
- Rev.EF/EG dense sampled LOS: 1782/1782 blocked.

The authoritative CFD contract remains `mechanical/cfd-rear-chimney-domain-contract-rev-a.md`.

First numerical matrix remains:
1. 5 W / 30 C / 4 mm wall gap;
2. 8 W / 30 C / 4 mm;
3. 10 W / 35 C / 4 mm;
4. 8 W / 35 C / 3 mm;
5. 8 W / 35 C / 5 mm.

Required physics remain gravity, natural convection with temperature-dependent density or justified Boussinesq approximation, solid conduction, and radiation. Pure conduction is not acceptable as passive-convection validation.

Next valid advancement requires an actual CFD-capable solver environment. Before solving, the Rev.EC fluid BREP and simplified solid obstructions/heat-source regions shall be exported into solver-ready geometry and meshed with a documented mesh-convergence sequence.

Checks:
C1768 local CFD capability audit executed.
C1769 CadQuery 2.8.0 available.
C1770 VTK 9.6.2 available.
C1771 OpenFOAM solver chain unavailable.
C1772 Gmsh unavailable.
C1773 no CFD numerical result claimed.
C1774 CFD geometry remains qualified by Rev.EE.
C1775 next numerical gate requires actual CFD solver plus mesh convergence.

Status: **THERMAL_CFD_REV_EH / GEOMETRY_READY / SOLVER_GATE_OPEN / C01_TO_C1775**.

## Rev.EY verification update

Elmer is available as the alternative solver. Natural-convection coupling now
converges. The separate de Vahl Davis Ra1000/Pr0.71 benchmark was executed on
three meshes with 0.02993% finest-grid Nusselt error and closed wall-flux balance.
See `validation/rev-et-ey/cavity-benchmark.json`. This supersedes the earlier
benchmark convergence warning only; the full AudioPicture CFD model remains OPEN.
