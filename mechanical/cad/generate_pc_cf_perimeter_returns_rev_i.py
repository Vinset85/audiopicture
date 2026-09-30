import cadquery as cq
import json

OUT="AP22_PC_CF_PERIMETER_RETURNS_REV_I.step"
# Diagnostic local perimeter returns connecting front tab envelope to rear ring.
# They are wide wall blades, not slender posts and not a continuous front ring.

stations=[
 ("M1D",70,394,"top"),("M2D",250,394,"top"),
 ("M3D",70,6,"bottom"),("M4D",250,6,"bottom"),
 ("M5D",6,135,"left"),("M6D",6,275,"left"),
 ("M7D",314,135,"right"),("M8D",314,315,"right")
]
z0=6.0
z1=29.0
tangential=10.0
radial=2.4

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

def blade(x,y,side):
    h=tangential/2
    if side=="top": return box(x-h,x+h,390.4,392.8,z0,z1)
    if side=="bottom": return box(x-h,x+h,7.2,9.6,z0,z1)
    if side=="left": return box(7.2,9.6,y-h,y+h,z0,z1)
    return box(310.4,312.8,y-h,y+h,z0,z1)

assy=None
for _,x,y,s in stations:
    p=blade(x,y,s)
    assy=p if assy is None else assy.union(p)

dml=box(10,310,10,390,3.3,9.3)
iv=assy.intersect(dml)
inter=sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0.0
bb=assy.val().BoundingBox()
cq.exporters.export(assy,OUT)

print(json.dumps({
 "valid":assy.val().isValid(),
 "return_count":len(stations),
 "independent_solid_count":assy.solids().size(),
 "dml_intersection_mm3":inter,
 "z_extent_mm":[bb.zmin,bb.zmax],
 "blade_section_mm":[10.0,2.4],
 "continuous_front_ring":False,
 "artifact":OUT,
 "limitations":[
   "exact ESP32/radar masks not booleaned",
   "vent/service booleans not yet imported",
   "must be fused with rear-frame and front-tab kernels for connectivity gate"
 ]
},indent=2))
