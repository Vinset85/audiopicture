# AudioPicture V2.2 thermal-source matrix Rev.CG
# Source-derived CFD setup helper. No CFD is executed.
import json
system_heat_W=[3,5,8,10]
ambient_C=[20,30,35]
wall_gap_mm=[3,4,5]
sources={
 "Q_TAS5825M":{"status":"documented_bound","W":6.7,"basis":"60 W output at 90% efficiency -> ~6.7 W stage loss; extreme continuous sine stress bound"},
 "Q_TPSM63603":{"status":"documented_operating_point","W":1.24,"basis":"24V->5V, 12.5 W output, ~91% efficiency published condition"},
 "Q_MAIN_C_NONAUDIO":{"status":"allocation_not_heat","W":1.40,"basis":"electrical load allocation; do not equate directly to heat without conversion/efficiency closure"},
 "Q_VOICE":{"status":"allocation_not_heat","W":0.80,"basis":"electrical load allocation"},
 "Q_RADAR_NORMAL":{"status":"allocation_not_heat","W":0.20,"basis":"electrical load allocation"},
 "Q_RADAR_STRESS":{"status":"allocation_not_heat","W":0.45,"basis":"electrical load allocation"},
 "Q_ENV":{"status":"allocation_not_heat","W":0.02,"basis":"electrical load allocation"},
 "Q_HOUSEKEEPING":{"status":"allocation_not_heat","W":0.08,"basis":"electrical load allocation"},
 "Q_POE_AG53024":{"status":"open","W":None,"basis":"exact efficiency/load curve required"},
 "Q_RPI5":{"status":"open","W":None,"basis":"no project-specific heat-source value found in reviewed thermal/power contracts"}
}
first_matrix=[
 {"heat_W":5,"ambient_C":30,"wall_gap_mm":4},
 {"heat_W":8,"ambient_C":30,"wall_gap_mm":4},
 {"heat_W":10,"ambient_C":35,"wall_gap_mm":4},
 {"heat_W":8,"ambient_C":35,"wall_gap_mm":3},
 {"heat_W":8,"ambient_C":35,"wall_gap_mm":5}
]
print(json.dumps({"system_heat_sweep_W":system_heat_W,"ambient_sweep_C":ambient_C,"wall_gap_sweep_mm":wall_gap_mm,
"sources":sources,"first_matrix":first_matrix,
"rules":["system heat sweep is primary enclosure-level comparison","component sources may replace aggregate sources but must not be added on top without subtraction","electrical load allocations are not automatically heat","10 W is adverse/stress, not nominal"],"CFD_run":False},indent=2))
