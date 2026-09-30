# AudioPicture V2.2 valid-BREP fluid connectivity rebuild Rev.EC
# Repairs Rev.EA complement construction without changing functional shell/labyrinth geometry.
import cadquery as cq,json
X=320.;Y=400.;R=1.5;EPS=0.02
def box(x0,x1,y0,y1,z0,z1):return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):o,x0,x1,y0,y1=c;return(o,X-x1,X-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mirror(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mirror(c) for i,c in enumerate(upperL)]
def cap(row,zlo,zhi,eps=0.):
 n,o,x0,x1,y0,y1=row;x0-=eps;x1+=eps;y0-=eps;y1+=eps
 if o=="H":
  cy=(y0+y1)/2;rr=(y1-y0)/2;xa=x0+rr;xb=x1-rr
  return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(xa,cy-rr).lineTo(xb,cy-rr).threePointArc((x1,cy),(xb,cy+rr)).lineTo(xa,cy+rr).threePointArc((x0,cy),(xa,cy-rr)).close().extrude(zhi-zlo)
 cx=(x0+x1)/2;rr=(x1-x0)/2;ya=y0+rr;yb=y1-rr
 return cq.Workplane("XY",origin=(0,0,zlo)).moveTo(cx-rr,ya).lineTo(cx-rr,yb).threePointArc((cx,y1),(cx+rr,yb)).lineTo(cx+rr,ya).threePointArc((cx,y0),(cx-rr,ya)).close().extrude(zhi-zlo)
# Build Rev.DX solid.
solid=box(0,320,0,400,37.8,40)
for a,b,c,d in [(0,2.2,148,337),(317.8,320,148,337),(18,302,0,2.2),(18,302,397.8,400)]:solid=solid.union(box(a,b,c,d,35.6,37.8))
for row in vents:solid=solid.cut(cap(row,37.58,40.22,EPS))
for x,y in [(145,383),(175,383),(12,200),(308,200),(80,17),(240,17)]:solid=solid.union(cq.Workplane("XY",origin=(x,y,36)).circle(5).extrude(1.8))
L=36.;CHL=24.;CHW=36.;EXIT=16.;OV=12.;ROOF=36.8;T=1.;ZT=37.85
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
 for row in vents:s=s.cut(cap(row,36.58,38.02,EPS))
 return s.clean()
def mx(s):return s.mirror("YZ",basePointVector=(160,0,0))
for p in [left(14,34),mx(left(14,34)),left(315,35.1),mx(left(315,35.1))]:solid=solid.union(p)
solid=solid.clean()
# Oversized seed prevents coplanar outer boundary with product edges; trim only after boolean.
seed=box(-EPS,320+EPS,-EPS,400+EPS,32.98,40.27)
fluid=seed.cut(solid).clean()
# Trim to intended audit domain using a slightly inset box to avoid coincident boundary artifacts.
trim=box(0.01,319.99,0.01,399.99,33.0,40.25)
fluid=fluid.intersect(trim).clean()
sols=fluid.solids().vals()
probe=box(155,165,195,205,33.2,34.0)
main=None
for i,s in enumerate(sols):
 if cq.Workplane(obj=s).intersect(probe).solids().size():main=i;break
rows={}
for row in vents:
 vp=cap(row,39.91,40.23,0.)
 touching=[]
 for i,s in enumerate(sols):
  q=cq.Workplane(obj=s).intersect(vp)
  if q.solids().size() and sum(z.Volume() for z in q.solids().vals())>1e-8:touching.append(i)
 rows[row[0]]={"components":touching,"connected_to_main":main in touching if main is not None else False}
valid=fluid.val().isValid() and all(s.isValid() for s in sols)
decision=valid and len(sols)==1 and main==0 and all(v["connected_to_main"] for v in rows.values())
print(json.dumps({"epsilon_mm":EPS,"fluid_valid":fluid.val().isValid(),"all_solids_valid":all(s.isValid() for s in sols),
"fluid_components":len(sols),"component_volumes_mm3":[round(s.Volume(),3) for s in sols],"main_component":main,
"connected_count":sum(v["connected_to_main"] for v in rows.values()),"vent_connectivity":rows,
"decision":"PASS" if decision else "FAIL",
"limitations":["topological CAD audit only","epsilon is boolean-construction aid, not production tolerance","pressure loss/CFD/acoustics open"]},indent=2))
