# AudioPicture V2.2 — CFD meshing contract Rev.CS

Status: **PRE_MESH_FEATURE_AUDIT_DEFINED / MESH_LEVELS_DEFINED / MESHER_NOT_AVAILABLE_IN_CURRENT_RUNTIME / NO_MESH_GENERATED / NO_CFD_RESULT**

## Runtime capability check
The current execution environment was checked before claiming a mesh run.

Available:
- CadQuery 2.8 / OpenCASCADE.

Not found:
- gmsh executable;
- gmsh Python module;
- OpenFOAM blockMesh/snappyHexMesh and solver binaries;
- ElmerSolver;
- meshio;
- PyVista;
- FreeCADCmd.

Therefore no real CFD mesh is claimed in this revision.

## Critical geometric scales
Current comparison geometry:
- vent width = 3.0 mm;
- alternating-gate baffle XY thickness = 1.2 mm;
- H0.8 nominal under-baffle fluid gap = 2.0 mm;
- H1.0 nominal under-baffle fluid gap = 1.8 mm;
- rear wall gap = 4.0 mm;
- shell thickness = 2.2 mm.

The narrowest modeled fluid feature among these is the H1.0 under-baffle gap at 1.8 mm.

## Local mesh levels
These levels are pre-mesh targets, not convergence proof.

### M0 — screening
Target at least 3 cells across 1.8 mm:
- local maximum cell size = 0.60 mm.

This gives nominally:
- 5 cells across a 3 mm vent;
- 3 cells across H1.0 under-baffle gap.

M0 may be used only to detect gross setup/pathology.

### M1 — refined comparison
Target at least 5 cells across 1.8 mm:
- local maximum cell size = 0.36 mm.

Nominally:
- 8.33 cells across a 3 mm vent;
- 5 cells across H1.0 under-baffle gap.

M1 is the preferred first comparison mesh target.

### M2 — fine
Target at least 7 cells across 1.8 mm:
- local maximum cell size ≈0.257 mm.

Nominally:
- 11.67 cells across a 3 mm vent;
- 7 cells across H1.0 under-baffle gap.

M2 is a convergence-check level, not automatically the production mesh.

## Bulk region
The older CFD contract allowed an initial bulk size of 4..6 mm.

Retain that only away from:
- vent banks;
- rear wall gap;
- baffle gates;
- MAIN-P/MAIN-C surfaces;
- PC-CF obstruction edges;
- thermal plume corridor.

Use graded transitions between bulk and local refinement.

## Wall and boundary treatment
Natural-convection CFD requires wall treatment appropriate to the selected solver/turbulence model.

Do not add prism layers mechanically if they collapse or consume the 1.8 mm H1.0 bypass.

The mesher must demonstrate that the under-baffle channel remains open after all layer inflation/refinement operations.

## Three-case fairness
CFD0, CFD08 and CFD10 shall use:
- same outer domain;
- same base mesh policy;
- same refinement boxes;
- same board/frame treatment;
- same wall treatment;
- same solver settings.

Only geometry-induced local changes are permitted.

Cell counts do not need to be numerically identical, but refinement criteria must be identical.

## Mesh-independence gate
A mesh cannot be called independent from geometry alone.

For at least the 8 W / 30 C / 4 mm comparison, solve M1 and M2 and compare:
- total natural-convection mass flow;
- lower-inlet and upper-outlet mass flow balance;
- pressure difference;
- MAIN-P representative temperature metric;
- MAIN-C representative temperature metric;
- outlet air temperature;
- maximum relevant solid/air temperature;
- heat balance.

No percentage threshold is frozen here without solver behavior and numerical evidence.

## Recommended export/mesher path
The Rev.CO STEP fluid bodies are the authoritative current meshing inputs.

A future environment with Gmsh or OpenFOAM shall:
1. import the three STEP domains;
2. preserve or reconstruct named inlet/outlet/wall/source surfaces;
3. apply M0 for setup debugging;
4. run M1 as first comparison;
5. run M2 for convergence;
6. reject meshes with closed vents, inverted elements or collapsed 1.8 mm bypasses.

## Acoustic caveat
Meshing the thermal domain does not close the unresolved 3D acoustic under-rib LOS gate.

The H0.8/H1.0 baffles remain thermal comparison candidates, not acoustically validated labyrinths.

## Checks
C1538 runtime mesher/solver availability explicitly checked.
C1539 CadQuery 2.8 available.
C1540 Gmsh unavailable in current runtime.
C1541 OpenFOAM unavailable in current runtime.
C1542 Elmer unavailable in current runtime.
C1543 no mesh generation claimed.
C1544 narrowest modeled fluid feature identified as 1.8mm.
C1545 M0 local size 0.60mm defined.
C1546 M1 local size 0.36mm defined.
C1547 M2 local size approx 0.257mm defined.
C1548 identical refinement policy required for three cases.
C1549 layer inflation must preserve H1.0 bypass.
C1550 M1/M2 solution comparison required for mesh independence.
C1551 Rev.CO STEP domains remain current meshing inputs.
C1552 acoustic 3D LOS remains open.
C1553 no CFD result claimed.

Status:
**THERMAL_REV_CS / PRE_MESH_CONTRACT / M0_0P60_M1_0P36_M2_0P257 / EXTERNAL_MESHER_REQUIRED / C01_TO_C1553**.
