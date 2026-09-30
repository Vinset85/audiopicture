# AudioPicture V2.2 rear shell master + six ASA retention seats Rev.AT
import cadquery as cq, json, math
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6
SEAT_D=10.;SEAT_H=1.8;SZ0=Z0-SEAT_H
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
segments=[("LEFT_MID",(0,RW,148,337)),("RIGHT_MID",(X-RW,X,148,337)),("BOTTOM_MID",(18,X-18,0,RW)),("TOP_MID",(18,X-18,Y-RW,Y))]
upper=[("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),("UL5","V",13,16,341,386),("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),("UR5","V",306,309,341,386)]
lower=[]
for side,xs in (("L",[(4,7),(11,14)]),("R",[(313,316),(306,309)])):
 i=1
 for y0,y1 in ((4,44),(52,92),(104,144)):
  for x0,x1 in xs:lower.append((f"I{side}{i}","V",x0,x1,y0,y1));i+=1
def box(r,z0,z1):
 a,b,c,d=r;return cq.Workplane("XY").box(b-a,d-c,z1-z0,centered=(False,False,False)).translate((a,c,z0))
def cap(row):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(T+.4)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(T+.4)
# AJ master
shell=box((0,X,0,Y),Z0,Z1)
returns={}
for n,r in segments:
 returns[n]=box(r,RZ0,Z0);shell=shell.union(returns[n])
for row in upper+lower:shell=shell.cut(cap(row))
shell=shell.clean();v_master=shell.val().Volume()
# seats and pre-union seat/return overlaps
seat_return={}
for n,x,y in nodes:
 p=cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H)
 seat_return[n]={}
 for rn,rr in returns.items():
  q=p.intersect(rr);seat_return[n][rn]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
 shell=shell.union(p)
shell=shell.clean()
# verify vents remain open through panel
vent_intersections={}
for row in upper+lower:
 c=cap(row);q=shell.intersect(c);vent_intersections[row[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
# expected overlap only possible side seats vs side returns, but seat center x12/308 is far from 2.2mm return.
bb=shell.val().BoundingBox();dv=shell.val().Volume()-v_master
assert shell.val().isValid() and shell.solids().size()==1
assert all(v<1e-8 for h in seat_return.values() for v in h.values())
assert all(v<1e-8 for v in vent_intersections.values())
assert bb.zmax<=40.
cq.exporters.export(shell,"AP22_REAR_SHELL_MASTER_SEATS_REV_AT.step")
cq.exporters.export(shell,"AP22_REAR_SHELL_MASTER_SEATS_REV_AT.stl")
print(json.dumps({"valid":True,"solid_count":1,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],
"seat_count":6,"seat_diameter_mm":SEAT_D,"seat_z_mm":[SZ0,Z0],
"seat_return_overlap_mm3":seat_return,"vent_reclosure_mm3":vent_intersections,
"master_volume_mm3":v_master,"seat_integrated_volume_mm3":shell.val().Volume(),"net_added_volume_mm3":dv,
"nominal_pc_cf_gap_mm":SZ0-35.,
"artifacts":["AP22_REAR_SHELL_MASTER_SEATS_REV_AT.step","AP22_REAR_SHELL_MASTER_SEATS_REV_AT.stl"],
"limitations":["fastener/insert open","service opening not fused in this master","CFD/RF/process qualification open"]},indent=2))
