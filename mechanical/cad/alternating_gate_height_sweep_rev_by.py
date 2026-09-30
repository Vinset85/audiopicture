# AudioPicture V2.2 alternating-gate height sweep Rev.BY
# Geometry/tolerance sensitivity only. NOT CFD.
import json
GAP=2.8
UP=15.;LOW=24.
# conservative engineering sensitivity on shell-frame separation, not production tolerance:
GAPS=[2.0,2.4,2.8,3.2]
HS=[0.8,1.0,1.2,1.4]
rows=[]
for h in HS:
 row={"H_mm":h,"nominal_under_rib_mm":GAP-h,
      "upper_gate_planar_proxy_mm2_per_side":UP*GAP,
      "lower_gate_planar_proxy_mm2_per_side":LOW*GAP,
      "under_rib_clearance_sensitivity_mm":{str(g):g-h for g in GAPS},
      "contact_if_gap_le_H":any(g-h<=0 for g in GAPS)}
 rows.append(row)
print(json.dumps({"nominal_gap_mm":GAP,"gap_sensitivity_mm":GAPS,"rows":rows,
"interpretation":["XY gate opening proxies do not depend on rib height in this reduced-order screen","rib height directly reduces under-rib bypass","lower H is less sensitive to shell/frame gap loss","final H requires physical gap/warpage evidence and CFD/acoustic test"]},indent=2))
