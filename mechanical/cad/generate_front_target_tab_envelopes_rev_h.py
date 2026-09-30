import cadquery as cq
import json

OUT="AP22_FRONT_TARGET_TAB_ENVELOPES_REV_H.step"

stations=[
 ("M1D",70,394,"top"),("M2D",250,394,"top"),
 ("M3D",70,6,"bottom"),("M4D",250,6,"bottom"),
 ("M5D",6,135,"left"),("M6D",6,275,"left"),
 ("M7D",314,135,"right"),("M8D",314,315,"right")
]

# Diagnostic front-envelope only.
# Final tab must be united to the real transformed PC-CF perimeter section.
tangential=10.0
radial=2.0
z0=5.1
z1=9.2

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

def tab(x,y,side):
    h=tangential/2
    if side=="top":
        return box(x-h,x+h,390.5,392.5,z0,z1)
    if side=="bottom":
        return box(x-h,x+h,7.5,9.5,z0,z1)
    if side=="left":
        return box(7.5,9.5,y-h,y+h,z0,z1)
    return box(310.5,312.5,y-h,y+h,z0,z1)

assy=None
for _,x,y,s in stations:
    p=tab(x,y,s)
    assy=p if assy is None else assy.union(p)

dml=box(10,310,10,390,3.3,9.3)
iv=assy.intersect(dml)
inter=sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0.0
cq.exporters.export(assy,OUT)

print(json.dumps({
 "valid":assy.val().isValid(),
 "local_node_count":len(stations),
 "solid_count_expected_independent":assy.solids().size(),
 "dml_intersection_mm3":inter,
 "continuous_front_ring":False,
 "artifact":OUT,
 "note":"diagnostic envelopes only; final union requires transformed rear-frame perimeter section"
},indent=2))
