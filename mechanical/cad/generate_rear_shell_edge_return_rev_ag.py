# AudioPicture V2.2 segmented rear-shell edge return Rev.AG
# Builds on Rev.AF: inward ASA perimeter returns only outside vent-bank zones.
import cadquery as cq, json
X=320.;Y=400.;T=2.2;ZP0=37.8;ZP1=40.;WALL=2.2;RETURN_Z0=35.6
# Rear plate
shell=cq.Workplane("XY").box(X,Y,T,centered=(False,False,False)).translate((0,0,ZP0))
# Vent bank protection zones, expanded 2 mm beyond executed slot extents.
# lower left/right: y 2..146; upper left/right: y 339..398
protected=[("LL",(0,18,2,146)),("LR",(302,320,2,146)),("UL",(0,18,339,400)),("UR",(302,320,339,400))]
# Segment returns: left/right central only; top/bottom central only.
segments=[
 ("LEFT_MID",(0,WALL,148,337)),
 ("RIGHT_MID",(X-WALL,X,148,337)),
 ("BOTTOM_MID",(18,X-18,0,WALL)),
 ("TOP_MID",(18,X-18,Y-WALL,Y)),
]
def box(r,z0,z1):
 x0,x1,y0,y1=r
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
for _,r in segments:shell=shell.union(box(r,RETURN_Z0,ZP0))
shell=shell.clean()
# PC-CF coarse ring 2..318 / 12..308 at z27..35: returns start z35.6 -> 0.6 mm nominal Z gap.
frame=box((2,318,2,398),27,35).cut(box((12,308,12,388),26,36))
q=shell.intersect(frame);iv=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
# Protected vent banks must have no return volume below rear plate.
prot={}
for n,r in protected:
 q=shell.intersect(box(r,RETURN_Z0,ZP0-.001));prot[n]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert iv<1e-8 and all(v<1e-8 for v in prot.values())
assert bb.xlen<=320 and bb.ylen<=400 and bb.zmax<=40
cq.exporters.export(shell,"AP22_REAR_SHELL_EDGE_RETURN_REV_AG.step")
print(json.dumps({"valid":True,"solid_count":1,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
"return_z_mm":[RETURN_Z0,ZP0],"return_depth_mm":ZP0-RETURN_Z0,"return_wall_mm":WALL,
"segments":segments,"vent_bank_return_intersections_mm3":prot,
"coarse_pc_cf_intersection_mm3":iv,"nominal_frame_z_gap_mm":RETURN_Z0-35.,
"limitations":["edge-return kernel only; vent cuts combined in next master","coarse PC-CF frame envelope","retention/service/baffles not added"]},indent=2))
