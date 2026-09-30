import cadquery as cq
import json

OUT = "AP22_FRONT_TARGETS_REV_F_DMU.step"

stations = [
 ("M1D",70,394),("M2D",250,394),
 ("M3D",70,6),("M4D",250,6),
 ("M5D",6,135),("M6D",6,275),
 ("M7D",314,135),("M8D",314,315)
]

target_xy=7.0
target_t=1.0
target_z0=4.1

assy=None
for name,x,y in stations:
    t=(cq.Workplane("XY")
       .box(target_xy,target_xy,target_t,centered=(True,True,False))
       .translate((x,y,target_z0)))
    assy=t if assy is None else assy.union(t)

dml=(cq.Workplane("XY")
     .box(300,380,6.0,centered=(False,False,False))
     .translate((10,10,3.3)))

inter=assy.intersect(dml)
inter_vol=sum(s.Volume() for s in inter.solids().vals()) if inter.solids().size() else 0.0

def edge_metrics(x,y):
    if y>390: dmlc=(y-target_xy/2)-390; outer=399.2-(y+target_xy/2)
    elif y<10: dmlc=10-(y+target_xy/2); outer=(y-target_xy/2)-0.8
    elif x<10: dmlc=10-(x+target_xy/2); outer=(x-target_xy/2)-0.8
    else: dmlc=(x-target_xy/2)-310; outer=319.2-(x+target_xy/2)
    return dmlc,outer

metrics={name:edge_metrics(x,y) for name,x,y in stations}
cq.exporters.export(assy,OUT)

print(json.dumps({
 "target_count":len(stations),
 "target_size_mm":[7,7,1],
 "target_z_mm":[4.1,5.1],
 "dml_intersection_mm3":inter_vol,
 "min_target_to_dml_xy_mm":min(v[0] for v in metrics.values()),
 "min_target_to_outer_boundary_xy_mm":min(v[1] for v in metrics.values()),
 "artifact":OUT
},indent=2))
