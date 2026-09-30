# AudioPicture V2.2 rear shell frame-aware master Rev.BK
import cadquery as cq, json, math
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6
SEAT_D=10.;SEAT_H=1.8;SZ0=Z0-SEAT_H
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
segments=[("LEFT_MID",(0,RW,148,337)),("RIGHT_MID",(X-RW,X,148,337)),("BOTTOM_MID",(18,X-18,0,RW)),("TOP_MID",(18,X-18,Y-RW,Y))]
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):
 o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mirror(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mirror(c) for i,c in enumerate(upperL)]
def box(r,z0,z1):
 a,b,c,d=r;return cq.Workplane("XY").box(b-a,d-c,z1-z0,centered=(False,False,False)).translate((a,c,z0))
def cap(row):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(T+.4)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(T+.4)
shell=box((0,X,0,Y),Z0,Z1)
returns={}
for n,r in segments:
 returns[n]=box(r,RZ0,Z0);shell=shell.union(returns[n])
for row in vents:shell=shell.cut(cap(row))
shell=shell.clean();preseat=shell.val().Volume()
seat_return={}
for n,x,y in nodes:
 p=cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H)
 seat_return[n]={rn:(sum(s.Volume() for s in p.intersect(rr).solids().vals()) if p.intersect(rr).solids().size() else 0.) for rn,rr in returns.items()}
 shell=shell.union(p)
shell=shell.clean()
vent_reclosure={}
for row in vents:
 q=shell.intersect(cap(row));vent_reclosure[row[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert all(v<1e-8 for d in seat_return.values() for v in d.values())
assert all(v<1e-8 for v in vent_reclosure.values())
assert bb.zmax<=40.
ain=(40-3)*3+math.pi*R*R;aout=(45-3)*3+math.pi*R*R
cq.exporters.export(shell,"AP22_REAR_SHELL_FRAME_AWARE_MASTER_REV_BK.step")
cq.exporters.export(shell,"AP22_REAR_SHELL_FRAME_AWARE_MASTER_REV_BK.stl")
print(json.dumps({"valid":True,"solid_count":1,"vent_count":len(vents),"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],
"real_area_mm2":{"inlet":12*ain,"outlet":10*aout},"seat_count":6,"seat_return_overlap_mm3":seat_return,
"vent_reclosure_mm3":vent_reclosure,"preseat_volume_mm3":preseat,"final_volume_mm3":shell.val().Volume(),
"artifacts":["AP22_REAR_SHELL_FRAME_AWARE_MASTER_REV_BK.step","AP22_REAR_SHELL_FRAME_AWARE_MASTER_REV_BK.stl"],
"limitations":["service opening still architecture-only","exact RF/radar open","CFD open","process qualification open"]},indent=2))
