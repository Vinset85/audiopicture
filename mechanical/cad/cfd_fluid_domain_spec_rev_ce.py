# AudioPicture V2.2 CFD fluid-domain specification Rev.CE
# Geometry specification/check only. Does NOT run CFD.
import json
product={"x":[0,320],"y":[0,400],"z":[0,40]}
# External domain seed in product coordinates: enough room for buoyant plume development,
# deliberately parameterized for later domain-independence study.
domains=[
 {"name":"D1","x_margin_mm":100,"y_bottom_mm":100,"y_top_mm":200,"rear_wall_gap_mm":4,"front_margin_mm":100},
 {"name":"D2","x_margin_mm":160,"y_bottom_mm":160,"y_top_mm":300,"rear_wall_gap_mm":4,"front_margin_mm":160}
]
cases=[
 {"id":"CFD-0","geometry":"Rev.BK/BM no baffle","baffle_h_mm":0.0},
 {"id":"CFD-08","geometry":"Rev.CC U15","baffle_h_mm":0.8},
 {"id":"CFD-10","geometry":"Rev.BW U15","baffle_h_mm":1.0}
]
for d in domains:
 d["bbox_seed_mm"]={"x":[-d["x_margin_mm"],320+d["x_margin_mm"]],
 "y":[-d["y_bottom_mm"],400+d["y_top_mm"]],
 "z":[-d["front_margin_mm"],40+d["rear_wall_gap_mm"]]}
 d["volume_box_mm3"]=(320+2*d["x_margin_mm"])*(400+d["y_bottom_mm"]+d["y_top_mm"])*(40+d["rear_wall_gap_mm"]+d["front_margin_mm"])
print(json.dumps({"product":product,"cases":cases,"domain_seeds":domains,
"rules":["D1/D2 are solver-domain seeds, not frozen boundaries","wall gap stays 4 mm in comparison","perform domain-independence check","fluid volume must subtract all solid product bodies represented in CFD","open/far-field boundaries identical across cases","gravity orientation identical across cases"],
"not_claimed":["CFD solution","adequate domain size","heat-source values","mesh convergence"]},indent=2))
