# AudioPicture V2.2 pre-mesh feature sizing Rev.CR
# Deterministic meshing contract helper. No mesh is generated.
import json
features={
 "vent_width_mm":3.0,
 "baffle_thickness_xy_mm":1.2,
 "under_baffle_gap_H08_mm":2.0,
 "under_baffle_gap_H10_mm":1.8,
 "rear_wall_gap_mm":4.0,
 "shell_thickness_mm":2.2,
 "pcb_thickness_seed_mm":1.6
}
# Target >=3 cells across the narrowest fluid gap for screening mesh,
# >=5 for refined comparison mesh. These are meshing-resolution rules, not CFD convergence proof.
narrow=min(features["vent_width_mm"],features["under_baffle_gap_H08_mm"],features["under_baffle_gap_H10_mm"],features["rear_wall_gap_mm"])
levels={
 "M0_screen":{"cells_across_narrowest":3,"max_local_cell_mm":narrow/3},
 "M1_refined":{"cells_across_narrowest":5,"max_local_cell_mm":narrow/5},
 "M2_fine":{"cells_across_narrowest":7,"max_local_cell_mm":narrow/7}
}
for v in levels.values():
 v["cells_across_3mm_vent"]=3.0/v["max_local_cell_mm"]
 v["cells_across_H10_under_gap"]=1.8/v["max_local_cell_mm"]
print(json.dumps({"features":features,"narrowest_fluid_feature_mm":narrow,"mesh_levels":levels,
"rules":["same mesh policy for CFD0/CFD08/CFD10","boundary-layer/prism treatment must not close 1.8mm H1.0 bypass","mesh independence requires solution comparison, not cell-size arithmetic","baffle 1.2mm is a solid thickness; resolve its faces without treating it as a fluid gap"]},indent=2))
