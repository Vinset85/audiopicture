import cadquery as cq
import json

OUT="AP22_STRUCTURAL_SPINE_REV_J.step"
Z0=27.0; DEPTH=8.0

stations=[
 ("M1D",70,394,"top"),("M2D",250,394,"top"),
 ("M3D",70,6,"bottom"),("M4D",250,6,"bottom"),
 ("M5D",6,135,"left"),("M6D",6,275,"left"),
 ("M7D",314,135,"right"),("M8D",314,315,"right")
]

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

# Rear frame Rev.C base
rear=box(2,318,2,398,Z0,Z0+DEPTH)
rear=rear.cut(box(12,308,12,388,Z0-1,Z0+DEPTH+1))
for x0,x1 in ((25.5,79.5),(240.5,294.5)):
    rear=rear.union(box(x0,x1,352,390,Z0,Z0+DEPTH))

keepouts=[
 ("L1",37,99,50,110),("L2",83,145,166,226),
 ("R1",175,237,238,298),("R2",223,285,88,148),
 ("MAIN_C",85,235,315,370),("VOICE",119,201,20,102),
 ("SERVICE",100,220,20,48),("ENV",252,294,35,59)
]
for _,x0,x1,y0,y1 in keepouts:
    rear=rear.cut(box(x0,x1,y0,y1,Z0-1,Z0+DEPTH+1))
rear=rear.clean()

def ret(x,y,s):
    h=5
    if s=="top": return box(x-h,x+h,390.4,392.8,6,29)
    if s=="bottom": return box(x-h,x+h,7.2,9.6,6,29)
    if s=="left": return box(7.2,9.6,y-h,y+h,6,29)
    return box(310.4,312.8,y-h,y+h,6,29)

def tab(x,y,s):
    h=5
    if s=="top": return box(x-h,x+h,390.5,392.5,5.1,9.2)
    if s=="bottom": return box(x-h,x+h,7.5,9.5,5.1,9.2)
    if s=="left": return box(7.5,9.5,y-h,y+h,5.1,9.2)
    return box(310.5,312.5,y-h,y+h,5.1,9.2)

assy=rear
node_report=[]
for name,x,y,s in stations:
    r=ret(x,y,s)
    t=tab(x,y,s)
    rr=rear.intersect(r)
    rt=r.intersect(t)
    node_report.append({
      "station":name,
      "rear_return_overlap_mm3":sum(q.Volume() for q in rr.solids().vals()) if rr.solids().size() else 0,
      "return_tab_overlap_mm3":sum(q.Volume() for q in rt.solids().vals()) if rt.solids().size() else 0
    })
    assy=assy.union(r).union(t)

assy=assy.clean()
dml=box(10,310,10,390,3.3,9.3)
iv=assy.intersect(dml)
dmlv=sum(q.Volume() for q in iv.solids().vals()) if iv.solids().size() else 0
solids=assy.solids().vals()
bb=assy.val().BoundingBox()
cq.exporters.export(assy,OUT)

print(json.dumps({
 "valid":assy.val().isValid(),
 "solid_count":len(solids),
 "disconnected_fragments":max(0,len(solids)-1),
 "volume_mm3":sum(q.Volume() for q in solids),
 "bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
 "z_extent_mm":[bb.zmin,bb.zmax],
 "dml_intersection_mm3":dmlv,
 "node_overlaps":node_report,
 "artifact":OUT
},indent=2))
