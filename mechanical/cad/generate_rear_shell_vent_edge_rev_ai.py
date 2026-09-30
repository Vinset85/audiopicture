# AudioPicture V2.2 ventilated rear shell + segmented edge return Rev.AI
import cadquery as cq, json, math, itertools
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6
upper=[("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),("UL5","V",13,16,341,386),("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),("UR5","V",306,309,341,386)]
lower=[]
for side,xs in (("L",[(4,7),(11,14)]),("R",[(313,316),(306,309)])):
 i=1
 for y0,y1 in ((4,44),(52,92),(104,144)):
  for x0,x1 in xs:lower.append((f"I{side}{i}","V",x0,x1,y0,y1));i+=1
segments=[("LEFT_MID",(0,RW,148,337)),("RIGHT_MID",(X-RW,X,148,337)),("BOTTOM_MID",(18,X-18,0,RW)),("TOP_MID",(18,X-18,Y-RW,Y))]
def box(r,z0,z1):
 x0,x1,y0,y1=r
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
def cap(row):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(T+.4)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(T+.4)
shell=box((0,X,0,Y),Z0,Z1)
for _,r in segments:shell=shell.union(box(r,RZ0,Z0))
precut=shell.val().Volume()
cuts={}
for row in upper+lower:
 c=cap(row);cuts[row[0]]=c;shell=shell.cut(c)
shell=shell.clean()
Au=(45-3)*3+math.pi*R*R;Al=(40-3)*3+math.pi*R*R;openA=10*Au+12*Al
removed=precut-shell.val().Volume()
# vents are cut only through rear panel; expected removed volume = area*T
expected_removed=openA*T
# coarse PC-CF ring
frame=box((2,318,2,398),27,35).cut(box((12,308,12,388),26,36))
fq=shell.intersect(frame);fiv=sum(s.Volume() for s in fq.solids().vals()) if fq.solids().size() else 0.
# verify no return occupies protected vent banks below panel
protected=[("LL",(0,18,2,146)),("LR",(302,320,2,146)),("UL",(0,18,339,400)),("UR",(302,320,339,400))]
pv={}
for n,r in protected:
 q=shell.intersect(box(r,RZ0,Z0-.001));pv[n]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert abs(removed-expected_removed)<1e-4
assert fiv<1e-8 and all(v<1e-8 for v in pv.values())
assert bb.xlen<=320 and bb.ylen<=400 and bb.zmax<=40
cq.exporters.export(shell,"AP22_REAR_SHELL_VENT_EDGE_REV_AI.step");cq.exporters.export(shell,"AP22_REAR_SHELL_VENT_EDGE_REV_AI.stl")
print(json.dumps({"valid":True,"solid_count":1,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],
"vent_count":22,"precut_volume_mm3":precut,"final_volume_mm3":shell.val().Volume(),
"vent_removed_volume_mm3":removed,"analytic_vent_removed_mm3":expected_removed,"vent_volume_error_mm3":removed-expected_removed,
"upper_real_gross_mm2":10*Au,"lower_real_gross_mm2":12*Al,
"protected_bank_return_intersections_mm3":pv,"coarse_pc_cf_intersection_mm3":fiv,
"nominal_frame_return_z_gap_mm":RZ0-35.,
"artifacts":["AP22_REAR_SHELL_VENT_EDGE_REV_AI.step","AP22_REAR_SHELL_VENT_EDGE_REV_AI.stl"],
"limitations":["service recess/tunnel open","retention open","baffles/ribs open","CFD/RF/ASA qualification open"]},indent=2))
