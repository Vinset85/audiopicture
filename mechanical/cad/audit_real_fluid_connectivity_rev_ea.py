# AudioPicture V2.2 real vent-to-cavity fluid connectivity Rev.EA
# Topological CAD audit; NOT CFD.
import cadquery as cq,json
X=320.;Y=400.;R=1.5
# Rebuild Rev.DX solid by importing generated logic compactly.
def box(x0,x1,y0,y1,z0,z1):return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mirror(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mirror(c) for i,c in enumerate(upperL)]
def cap(row,zlo,zhi):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(zhi-zlo)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(zhi-zlo)
# shell
solid=box(0,320,0,400,37.8,40)
for a,b,c,d in [(0,2.2,148,337),(317.8,320,148,337),(18,302,0,2.2),(18,302,397.8,400)]:solid=solid.union(box(a,b,c,d,35.6,37.8))
for row in vents:solid=solid.cut(cap(row,37.6,40.2))
for x,y in [(145,383),(175,383),(12,200),(308,200),(80,17),(240,17)]:
 solid=solid.union(cq.Workplane("XY",origin=(x,y,36)).circle(5).extrude(1.8))
# chambers
L=36.;W=48.;CHL=24.;CHW=36.;EXIT=16.;OV=12.;ROOF=36.8;T=1.;ZT=37.85
def left(y0,zl):
 x0=15.;x1=51.;y1=y0+48
 ss=[box(x0,x1,y0,y1,ROOF,ZT),box(x0,x0+T,y0,y1,zl,ROOF),box(x0,x1,y0,y0+T,zl,ROOF)]
 cx0=x1-CHL;cx1=x1;cy0=y1-CHW;cy1=y1
 ss += [box(cx1-T,cx1,cy0,cy1,zl,ROOF),box(cx0,cx1,cy0,cy0+T,zl,ROOF)]
 ex0=cx0+T;ex1=min(cx1-T,ex0+EXIT)
 ss += [box(cx0,ex0,cy1-T,cy1,zl,ROOF),box(ex1,cx1,cy1-T,cy1,zl,ROOF)]
 bx=min(cx1-T,cx0+T+EXIT+OV);ss.append(box(bx-T,bx,cy0+T,cy1-T,zl,ROOF))
 s=ss[0]
 for q in ss[1:]:s=s.union(q)
 for row in vents:s=s.cut(cap(row,36.6,38.0))
 return s.clean()
def mx(s):return s.mirror("YZ",basePointVector=(160,0,0))
for p in [left(14,34),mx(left(14,34)),left(315,35.1),mx(left(315,35.1))]:solid=solid.union(p)
solid=solid.clean()
# Fluid seed spans cavity through apertures and slightly outside rear face.
# It is intentionally limited to product XY; external room-domain connection is a later CFD-domain operation.
fluid=box(0,320,0,400,33.0,40.25).cut(solid).clean()
sols=fluid.solids().vals()
# identify the main internal component using a probe in central cavity
probe=box(155,165,195,205,33.2,34.0)
main_idx=None
for i,s in enumerate(sols):
 if cq.Workplane(obj=s).intersect(probe).solids().size():main_idx=i;break
rows={}
for row in vents:
 vp=cap(row,39.9,40.24)
 touching=[]
 for i,s in enumerate(sols):
  q=cq.Workplane(obj=s).intersect(vp)
  v=sum(z.Volume() for z in q.solids().vals()) if q.solids().size() else 0.
  if v>1e-8:touching.append(i)
 rows[row[0]]={"components":touching,"connected_to_main":main_idx in touching if main_idx is not None else False}
vols=[round(s.Volume(),3) for s in sols]
print(json.dumps({"fluid_valid":fluid.val().isValid(),"fluid_components":len(sols),"component_volumes_mm3":vols,
"main_component":main_idx,"vent_connectivity":rows,
"connected_count":sum(1 for v in rows.values() if v["connected_to_main"]),
"decision":"PASS" if main_idx is not None and all(v["connected_to_main"] for v in rows.values()) else "FAIL",
"limitations":["topological CAD connectivity only","external room not included","pressure loss not evaluated","CFD and acoustic attenuation open"]},indent=2))
