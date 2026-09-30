import cadquery as cq
import json

# Rev.Q corrected seed: 5+5 vertical upper outlet slots, each 3 x 45 mm.
# The rejected horizontal seed intersected the cleat islands.
Z0,Z1=37.8,40.0
slots=[]
# Left bank kept entirely left of cleatL X25.5 and ESP32 coarse mask X64+.
# Right bank kept entirely right of cleatR X294.5.
xs_left=[4.5,8.5,12.5,16.5,20.5]
xs_right=[299.5,303.5,307.5,311.5,315.5]
for i,x in enumerate(xs_left):
    slots.append((f"UL{i+1}",x-1.5,x+1.5,345,390))
for i,x in enumerate(xs_right):
    slots.append((f"UR{i+1}",x-1.5,x+1.5,345,390))

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

cleatL=box(25.5,79.5,352,390,27,40)
cleatR=box(240.5,294.5,352,390,27,40)
m1=box(65,75,390.4,398,5.1,35)
m2=box(245,255,390.4,398,5.1,35)
esp=box(64,119.5,318.5,366.5,0,40)
mainc=box(85,235,315,370,0,40)

rows=[]; gross=0
for n,x0,x1,y0,y1 in slots:
    s=box(x0,x1,y0,y1,Z0,Z1); gross+=(x1-x0)*(y1-y0)
    def iv(o):
        q=s.intersect(o)
        return sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0
    rows.append({"slot":n,"x":[x0,x1],"y":[y0,y1],
      "cleat_intersection_mm3":iv(cleatL)+iv(cleatR),
      "M1_M2_intersection_mm3":iv(m1)+iv(m2),
      "ESP32_coarse_mask_intersection_mm3":iv(esp),
      "MAIN_C_intersection_mm3":iv(mainc)})
print(json.dumps({"slot_count":len(slots),"gross_area_mm2":gross,
 "effective_seed_mm2":gross*0.80,"minimum_web_mm":1.0,
 "slots":rows},indent=2))
