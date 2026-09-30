# AudioPicture V2.2 labyrinth height robustness ranking Rev.CA
# Geometry-only screening; NOT CFD and NOT manufacturing tolerance.
import json
GAPS=[2.0,2.4,2.8,3.2]
HS=[0.8,1.0,1.2,1.4]
rows=[]
for h in HS:
 cs=[g-h for g in GAPS]
 rows.append({
  "H_mm":h,
  "clearance_at_gap_2p0_mm":2.0-h,
  "nominal_clearance_at_gap_2p8_mm":2.8-h,
  "minimum_clearance_in_sensitivity_mm":min(cs),
  "nominal_clearance_fraction_of_gap":(2.8-h)/2.8,
  "screen_class":"pre_CFD_candidate" if h<=1.0 else "comparison_only"
 })
print(json.dumps({"rows":rows,
"screen_rule":"Without measured acoustic benefit, do not spend geometric clearance merely to increase rib height.",
"preferred_pre_CFD_set_mm":[0.8,1.0],
"baseline_for_existing_kernel_mm":1.0,
"not_frozen":True},indent=2))
