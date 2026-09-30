# AudioPicture V2.2 shell + four-bank terminal chamber integration Rev.DW
import cadquery as cq,json,math
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5;RW=2.2;RZ0=35.6
SEAT_D=10.;SEAT_H=1.8;SZ0=Z0-SEAT_H
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
segments=[("LEFT_MID",(0,RW,148,337)),("RIGHT_MID",(X-RW,X,148,337)),("BOTTOM_MID",(18,X-18,0,RW)),("TOP_MID",(18,X-18,Y-RW,Y))]
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mirror(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mirror(c) for i,c in enumerate(upperL)]
def boxr(r,z0,z1):
 a,b,c,d=r;return cq.Workplane("XY").box(b-a,d-c,z1-z0,centered=(False,False,False)).translate((a,c,z0))
def box(x0,x1,y0,y1,z0,z1):return boxr((x0,x1,y0,y1),z0,z1)
def cap(row):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(T+.4)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(T+.4)
shell=box(0,X,0,Y,Z0,Z1)
for _,r in segments:shell=shell.union(boxr(r,RZ0,Z0))
for row in vents:shell=shell.cut(cap(row))
for _,x,y in nodes:shell=shell.union(cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H))
shell=shell.clean()
# Rev.DT geometry with 0.05 mm controlled construction overlap into shell panel to ensure robust fusion.
L=36.;W=48.;CHL=24.;CHW=36.;EXIT=16.;OV=12.;ROOF=36.8;TW=1.;ZTIE=37.85
def left_geom(y0,zlow):
 x0=15.;x1=x0+L;y1=y0+W;zl=zlow
 ss=[box(x0,x1,y0,y1,ROOF,ZTIE),box(x0,x0+TW,y0,y1,zl,ROOF),box(x0,x1,y0,y0+TW,zl,ROOF)]
 cx0=x1-CHL;cx1=x1;cy0=y1-CHW;cy1=y1
 ss += [box(cx1-TW,cx1,cy0,cy1,zl,ROOF),box(cx0,cx1,cy0,cy0+TW,zl,ROOF)]
 ex0=cx0+TW;ex1=min(cx1-TW,ex0+EXIT)
 if ex0>cx0:ss.append(box(cx0,ex0,cy1-TW,cy1,zl,ROOF))
 if ex1<cx1:ss.append(box(ex1,cx1,cy1-TW,cy1,zl,ROOF))
 bx=min(cx1-TW,cx0+TW+EXIT+OV);ss.append(box(bx-TW,bx,cy0+TW,cy1-TW,zl,ROOF))
 s=ss[0]
 for q in ss[1:]:s=s.union(q)
 return s.clean()
def mx(s):return s.mirror("YZ",basePointVector=(160,0,0))
parts={"LL":left_geom(14,34.),"LR":mx(left_geom(14,34.)),"UL":left_geom(315,35.1),"UR":mx(left_geom(315,35.1))}
contacts={}
assembly=shell
for n,p in parts.items():
 q=p.intersect(shell);contacts[n]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
 assembly=assembly.union(p)
assembly=assembly.clean()
reclose={}
for row in vents:
 q=assembly.intersect(cap(row));reclose[row[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=assembly.val().BoundingBox()
print(json.dumps({"shell_pre_valid":shell.val().isValid(),"contacts_mm3":contacts,
"assembly_valid":assembly.val().isValid(),"assembly_solids":assembly.solids().size(),
"vent_reclosure_mm3":reclose,"max_vent_reclosure_mm3":max(reclose.values()),
"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],
"construction_overlap_mm":0.05,"decision":"PASS" if assembly.val().isValid() and assembly.solids().size()==1 and max(reclose.values())<1e-8 and all(v>0 for v in contacts.values()) else "FAIL",
"limitations":["0.05mm is CAD construction overlap, not released manufacturing dimension","fluid connectivity open","actual-product LOS open","CFD open"]},indent=2))
cq.exporters.export(assembly,"AP22_REAR_SHELL_TERMINAL_CHAMBERS_REV_DW.step")
cq.exporters.export(assembly,"AP22_REAR_SHELL_TERMINAL_CHAMBERS_REV_DW.stl")
