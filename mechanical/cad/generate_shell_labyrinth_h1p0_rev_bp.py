# AudioPicture V2.2 shell + planar labyrinth H1.0 Rev.BP
import cadquery as cq, json, math
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6
BH=1.0;BZ0=Z0-BH;BT=1.2
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
# Rev.BK shell
shell=box((0,X,0,Y),Z0,Z1);returns={}
for n,r in segments:returns[n]=box(r,RZ0,Z0);shell=shell.union(returns[n])
for row in vents:shell=shell.cut(cap(row))
for n,x,y in nodes:shell=shell.union(cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H))
shell=shell.clean()
# Two staggered planar ribs per bank. Ribs do not cover vent footprints.
# Lower ribs are horizontal gates just inward of the two slot columns, alternating openings.
# Upper ribs are vertical gates inward of horizontal slot stacks, alternating Y openings.
baffles=[
 ("LIN_A",(29,30.2,14,82)),("LIN_B",(33,34.2,82,150)),
 ("RIN_A",(289.8,291,14,82)),("RIN_B",(285.8,287,82,150)),
 ("LOUT_A",(64,65.2,315,332)),("LOUT_B",(68,69.2,329,346)),
 ("ROUT_A",(254.8,256,315,332)),("ROUT_B",(250.8,252,329,346))
]
bs={}
for n,r in baffles:
 bs[n]=box(r,BZ0,Z0);shell=shell.union(bs[n])
shell=shell.clean()
# frame Rev.C solid for nominal 3D collision
FZ0=27.;FZ1=35.
frame=box((2,318,2,398),FZ0,FZ1).cut(box((12,308,12,388),FZ0-1,FZ1+1))
for x0,x1 in ((25.5,79.5),(240.5,294.5)):frame=frame.union(box((x0,x1,352,390),FZ0,FZ1))
for r in [(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]:
 frame=frame.cut(box(r,FZ0-1,FZ1+1))
frame=frame.clean()
fq=shell.intersect(frame);fvol=sum(s.Volume() for s in fq.solids().vals()) if fq.solids().size() else 0.
vre={}
for row in vents:
 q=shell.intersect(cap(row));vre[row[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert fvol<1e-8
assert all(v<1e-8 for v in vre.values())
assert bb.zmax<=40.
cq.exporters.export(shell,"AP22_REAR_SHELL_LABYRINTH_H1P0_REV_BP.step")
cq.exporters.export(shell,"AP22_REAR_SHELL_LABYRINTH_H1P0_REV_BP.stl")
print(json.dumps({"valid":True,"solid_count":1,"baffle_height_mm":BH,"baffle_count":len(baffles),"baffle_z_mm":[BZ0,Z0],
"nominal_under_baffle_to_frame_mm":BZ0-35.,"frame_intersection_mm3":fvol,"max_vent_reclosure_mm3":max(vre.values()),
"bbox_z_mm":[bb.zmin,bb.zmax],"artifacts":["AP22_REAR_SHELL_LABYRINTH_H1P0_REV_BP.step","AP22_REAR_SHELL_LABYRINTH_H1P0_REV_BP.stl"],
"limitations":["baffle XY geometry is first parametric seed","two-turn flow path requires path/throat audit","exact RF/radar/harness and CFD open"]},indent=2))
