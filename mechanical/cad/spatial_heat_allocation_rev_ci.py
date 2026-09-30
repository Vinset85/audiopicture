# AudioPicture V2.2 spatial heat allocation Rev.CI
# Scenario-based enclosure CFD source allocation. NOT measured component dissipation.
import json
boards={
 "MAIN_P":{"xy_mm":[105,220,112,157],"role":"power/audio primary hot PCB"},
 "MAIN_C":{"xy_mm":[85,235,315,370],"role":"PoE/network/control"}
}
# Fractions are modeling allocations, deliberately scenario-based.
# They are NOT component loss measurements.
scenarios={
 "CFD_5W":{"total_W":5.0,"fractions":{"MAIN_P":0.70,"MAIN_C":0.30}},
 "CFD_8W":{"total_W":8.0,"fractions":{"MAIN_P":0.75,"MAIN_C":0.25}},
 "CFD_10W":{"total_W":10.0,"fractions":{"MAIN_P":0.80,"MAIN_C":0.20}}
}
out={}
for n,s in scenarios.items():
 q={k:round(s["total_W"]*v,6) for k,v in s["fractions"].items()}
 assert abs(sum(q.values())-s["total_W"])<1e-9
 out[n]={"total_W":s["total_W"],"Q_W":q,"sum_W":sum(q.values())}
print(json.dumps({"board_regions":boards,"scenarios":out,
"status":"MODEL_ALLOCATION_ONLY",
"rules":["fractions are not measured losses","same allocation must be used across CFD-0/08/10 for a given heat case","do not add component heat on top unless aggregate board source is reduced by the same amount","Pi heat remains open and must be incorporated only after its actual model/location/load is reconciled"]},indent=2))
