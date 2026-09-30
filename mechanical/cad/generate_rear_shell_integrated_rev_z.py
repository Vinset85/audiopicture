# AudioPicture V2.2 rear shell integrated nominal kernel Rev.Z
# Real 2.2 mm ASA rear panel with Rev.V upper outlets using R1.5 capsule ends.
# Lower inlet geometry remains a separate unresolved placement gate and is NOT invented here.
import cadquery as cq
import json, math

X=320.0; Y=400.0; T=2.2
Z0=37.8; Z1=40.0
SLOT_W=3.0; SLOT_L=45.0; R=1.5

upper=[
 ("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),
 ("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),
 ("UL5","V",13,16,341,386),
 ("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),
 ("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),
 ("UR5","V",306,309,341,386),
]

def capsule(name,ori,x0,x1,y0,y1):
    # 3 mm wide, 45 mm overall-length capsule; through-cut with small Z overshoot.
    if ori=="H":
        cy=(y0+y1)/2
        xa=x0+R; xb=x1-R
        shape=(cq.Workplane("XY",origin=(0,0,Z0-0.2))
               .moveTo(xa,cy-R).lineTo(xb,cy-R)
               .threePointArc((x1,cy),(xb,cy+R))
               .lineTo(xa,cy+R)
               .threePointArc((x0,cy),(xa,cy-R))
               .close().extrude(T+0.4))
    else:
        cx=(x0+x1)/2
        ya=y0+R; yb=y1-R
        shape=(cq.Workplane("XY",origin=(0,0,Z0-0.2))
               .moveTo(cx-R,ya).lineTo(cx-R,yb)
               .threePointArc((cx,y1),(cx+R,yb))
               .lineTo(cx+R,ya)
               .threePointArc((cx,y0),(cx-R,ya))
               .close().extrude(T+0.4))
    return shape

shell=cq.Workplane("XY").box(X,Y,T,centered=(False,False,False)).translate((0,0,Z0))
cuts=[]
for row in upper:
    c=capsule(*row)
    cuts.append((row[0],c))
    shell=shell.cut(c)
shell=shell.clean()

# Obstacles from executed Rev.V gate; shell slots must have zero intersection.
excl=[
 ("cleatL",(25.5,79.5,352,390)),("cleatR",(240.5,294.5,352,390)),
 ("M1D",(65,75,390.4,398)),("M2D",(245,255,390.4,398)),
 ("ESP32",(64,119.5,318.5,366.5)),("MAIN_C",(85,235,315,370)),
]
def obstacle(r):
    x0,x1,y0,y1=r
    return cq.Workplane("XY").box(x1-x0,y1-y0,40,centered=(False,False,False)).translate((x0,y0,0))

intersections={}
for sn,c in cuts:
    intersections[sn]={}
    for on,r in excl:
        q=c.intersect(obstacle(r))
        intersections[sn][on]=sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0.0

solids=shell.solids().vals()
bb=shell.val().BoundingBox()
gross_capsule_one=(SLOT_L-SLOT_W)*SLOT_W+math.pi*R*R
gross_total=10*gross_capsule_one
effective_seed=.80*gross_total

assert shell.val().isValid()
assert len(solids)==1
assert all(abs(v)<1e-8 for d in intersections.values() for v in d.values())
assert effective_seed>=1000.0

cq.exporters.export(shell,"AP22_REAR_SHELL_UPPER_REV_Z.step")
cq.exporters.export(shell,"AP22_REAR_SHELL_UPPER_REV_Z.stl")
print(json.dumps({
 "valid":shell.val().isValid(),
 "solid_count":len(solids),
 "bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
 "z_extent_mm":[bb.zmin,bb.zmax],
 "upper_slot_count":len(upper),
 "slot_overall_mm":[SLOT_W,SLOT_L],
 "slot_end_radius_mm":R,
 "capsule_area_each_mm2":gross_capsule_one,
 "upper_gross_actual_mm2":gross_total,
 "upper_effective_seed_0p80_mm2":effective_seed,
 "preferred_effective_target_mm2":1000.0,
 "intersections_mm3":intersections,
 "limitations":[
  "upper outlet only; lower inlet exact XY placement still open",
  "flat rear panel kernel; perimeter returns, retention, baffles and service recess not yet added",
  "CFD not run",
  "industrial FDM supplier tolerance is not yet a part-specific acceptance result"
 ]
},indent=2))
