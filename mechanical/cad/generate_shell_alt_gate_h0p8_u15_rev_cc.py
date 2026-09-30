# AudioPicture V2.2 alternating-gate shell H0.8 upper15 Rev.CC
# Same XY topology as executed Rev.BW; only baffle height changes.
import cadquery as cq, json
X=320.;Y=400.;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6;BH=0.8;BZ0=Z0-BH
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
segments=[(0,RW,148,337),(X-RW,X,148,337),(18,X-18,0,RW),(18,X-18,Y-RW,Y)]
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mir(c):o,a,b,c0,d=c;return(o,320-b,320-a,c0,d)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mir(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mir(c) for i,c in enumerate(upperL)]
def box(r,a,b):x0,x1,y0,y1=r;return cq.Workplane("XY").box(x1-x0,y1-y0,b-a,centered=(False,False,False)).translate((x0,y0,a))
def cap(row):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(2.6)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(2.6)
shell=box((0,X,0,Y),Z0,Z1)
for r in segments:shell=shell.union(box(r,RZ0,Z0))
for v in vents:shell=shell.cut(cap(v))
for _,x,y in nodes:shell=shell.union(cq.Workplane("XY",origin=(x,y,36.)).circle(5).extrude(1.8))
left=[("LIN1",(30,31.2,14,126)),("LIN2",(34,35.2,38,150)),("LOUT1",(65,66.2,315,331)),("LOUT2",(69,70.2,330,346))]
def mr(r):a,b,c,d=r;return(320-b,320-a,c,d)
baffles=left+[(n.replace("L","R",1),mr(r)) for n,r in left]
for _,r in baffles:shell=shell.union(box(r,BZ0,Z0))
shell=shell.clean()
frame=box((2,318,2,398),27,35).cut(box((12,308,12,388),26,36))
for r in [(25.5,79.5,352,390),(240.5,294.5,352,390)]:frame=frame.union(box(r,27,35))
for r in [(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]:frame=frame.cut(box(r,26,36))
frame=frame.clean()
iv=shell.intersect(frame);fvol=sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0.
vre={}
for v in vents:
 q=shell.intersect(cap(v));vre[v[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1 and fvol<1e-8 and max(vre.values())<1e-8 and bb.zmax<=40
cq.exporters.export(shell,"AP22_REAR_SHELL_ALT_GATE_H0P8_U15_REV_CC.step")
cq.exporters.export(shell,"AP22_REAR_SHELL_ALT_GATE_H0P8_U15_REV_CC.stl")
print(json.dumps({"valid":True,"solids":1,"baffles":8,"H_mm":BH,"upper_opening_mm":15,"lower_opening_mm":24,
"nominal_under_rib_clearance_to_frame_mm":BZ0-35,"frame_intersection_mm3":fvol,"max_vent_reclosure_mm3":max(vre.values()),"zmax_mm":bb.zmax},indent=2))
