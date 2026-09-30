# AudioPicture V2.2 — solver geometry export execution Rev.EM

Status: **BREP_VALID / STEP_STL_EXPORT_PASS / STEP_REIMPORT_PASS / NOT_A_CFD_OR_FEA_RESULT**

Rev.EL was executed locally with CadQuery 2.8.0 and correctly blocked export because the assembled shell/labyrinth solid was invalid although the fluid complement remained valid.

Isolation showed:
- shell + 22 vents: valid;
- all six retention seats: valid;
- each terminal chamber individually: valid;
- invalidity first appears when the mirrored second chamber is fused;
- OCC reported two invalid faces and zero invalid edges.

Rev.EM changes only CAD boolean robustness: mirrored chamber solids receive a 0.001 mm X offset before union. This is below the existing EPS=0.02 mm construction aid and is not a production dimension.

Actual Rev.EM execution:
- solid_valid: true;
- solid_components: 1;
- solid_volume: 287929.522 mm3;
- fluid_valid: true;
- fluid_components: 1;
- fluid_volume: 640018.572 mm3;
- export: PASS.

Generated locally:
- SOLID STEP 1,115,633 bytes;
- SOLID STL 868,134 bytes;
- FLUID STEP 1,135,492 bytes;
- FLUID STL 868,834 bytes.

Independent STEP re-import:
- SOLID valid, 1 solid, 287929.522 mm3, bbox 320 x 400 x 6 mm;
- FLUID valid, 1 solid, 640018.572 mm3, bbox 319.98 x 399.98 x 7.25 mm.

Relative to the previously validated Rev.EC fluid volume 640018.576 mm3, the observed difference is approximately 0.004 mm3 and is attributable to the CAD-only robustness offset.

The exports are solver-ready geometry artifacts only. No volume mesh, CFD solution or structural FEM solution is claimed.

Checks:
C1806 Rev.EL executed rather than inferred.
C1807 Rev.EL invalid solid detected and export correctly blocked.
C1808 invalidity isolated to mirrored chamber boolean fusion.
C1809 individual shell/seats/chambers remain valid.
C1810 Rev.EM CAD-only 0.001 mm robustness offset documented.
C1811 Rev.EM solid BREP valid and one component.
C1812 Rev.EM fluid BREP valid and one component.
C1813 STEP/STL files physically generated and non-empty.
C1814 STEP files independently reimported as valid single solids.
C1815 numerical CFD/FEM gates remain open.

Status: **SOLVER_GEOMETRY_REV_EM / EXPORT_AND_REIMPORT_VALIDATED / C01_TO_C1815**.
