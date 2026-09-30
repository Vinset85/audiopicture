import cadquery as cq
import json

# Rev.Q exact seed coordinates for rear-shell upper outlet slots.
# Shell rear plate Z37.8..40.0; slots cut through ASA only.
# 5 left + 5 right, each 45 x 3 mm, long axis X.
Z0,Z1=37.8,40.0
slots=[]
# Staggered Y rows; left/right banks chosen outside cleat islands and M1D/M2D X footprints.
ys=[374,368,362,356,350]
# Left bank x 8..53; right bank x267..312.
for i,y in enumerate(ys):
    slots.append((f"UL{i+1}",8,53,y-1.5,y+1.5))
    slots.append((f"UR{i+1}",267,312,y-1.5,y+1.5))

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

# Structural/RF exclusion projections from authoritative docs.
cleatL=box(25.5,79.5,352,390,27,40)
cleatR=box(240.5,294.5,352,390,27,40)
m1=box(65,75,390.4,398,5.1,35)
m2=box(245,255,390.4,398,5.1,35)
esp=box(64,119.5,318.5,366.5,0,40)
mainc=box(85,235,315,370,0,40)

rows=[]
gross=0
for n,x0,x1,y0,y1 in slots:
    s=box(x0,x1,y0,y1,Z0,Z1)
    gross+=(x1-x0)*(y1-y0)
    def iv(o):
        q=s.intersect(o)
        return sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0
    rows.append({"slot":n,"x":[x0,x1],"y":[y0,y1],
      "cleat_intersection_mm3":iv(cleatL)+iv(cleatR),
      "M1_M2_intersection_mm3":iv(m1)+iv(m2),
      "ESP32_coarse_mask_intersection_mm3":iv(esp),
      "MAIN_C_intersection_mm3":iv(mainc)})
print(json.dumps({"slot_count":len(slots),"gross_area_mm2":gross,
 "effective_seed_mm2":gross*0.80,"slots":rows},indent=2))
