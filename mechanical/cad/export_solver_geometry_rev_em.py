# AudioPicture V2.2 Rev.EM solver-ready geometry exporter
# Rebuilds validated Rev.EC shell/labyrinth obstacle and fluid complement.
import cadquery as cq, json, os, hashlib
X=320.;Y=400.;EPS=.02
OUT="solver_exports_rev_em"; os.makedirs(OUT,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1): return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lower=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upper=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mir(c):o,x0,x1,y0,y1=c;return(o,X-x1,X-x0,y0,y1)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lower)]+[("IR"+str(i+1),)+mir(c) for i,c in enumerate(lower)]+[("UL"+str(i+1),)+c for i,c in enumerate(upper)]+[("UR"+str(i+1),)+mir(c) for i,c in enumerate(upper)]
def cap(r,z0,z1,e=0):
 n,o,x0,x1,y0,y1=r;x0-=e;x1+=e;y0-=e;y1+=e
 if o=="H":
  cy=(y0+y1)/2;rr=(y1-y0)/2;xa=x0+rr;xb=x1-rr
  return cq.Workplane("XY",origin=(0,0,z0)).moveTo(xa,cy-rr).lineTo(xb,cy-rr).threePointArc((x1,cy),(xb,cy+rr)).lineTo(xa,cy+rr).threePointArc((x0,cy),(xa,cy-rr)).close().extrude(z1-z0)
 cx=(x0+x1)/2;rr=(x1-x0)/2;ya=y0+rr;yb=y1-rr
 return cq.Workplane("XY",origin=(0,0,z0)).moveTo(cx-rr,ya).lineTo(cx-rr,yb).threePointArc((cx,y1),(cx+rr,yb)).lineTo(cx+rr,ya).threePointArc((cx,y0),(cx-rr,ya)).close().extrude(z1-z0)
solid=box(0,320,0,400,37.8,40)
for a,b,c,d in [(0,2.2,148,337),(317.8,320,148,337),(18,302,0,2.2),(18,302,397.8,400)]:solid=solid.union(box(a,b,c,d,35.6,37.8))
for r in vents:solid=solid.cut(cap(r,37.58,40.22,EPS))
for x,y in [(145,383),(175,383),(12,200),(308,200),(80,17),(240,17)]:solid=solid.union(cq.Workplane("XY",origin=(x,y,36)).circle(5).extrude(1.8))
CHL=24.;CHW=36.;EXIT=16.;OV=12.;ROOF=36.8;T=1.;ZT=37.85
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
 for r in vents:s=s.cut(cap(r,36.58,38.02,EPS))
 return s.clean()
def mx(s):return s.mirror("YZ",basePointVector=(160,0,0))
# OCC robustness aid: 0.001 mm X offset on mirrored chamber solids avoids
# coincident-face invalidity. CAD-only; below EPS=0.02 mm, not a production dimension.
parts=[left(14,34),mx(left(14,34)).translate((0.001,0,0)),left(315,35.1),mx(left(315,35.1)).translate((0.001,0,0))]
for p in parts:solid=solid.union(p)
solid=solid.clean()
seed=box(-EPS,320+EPS,-EPS,400+EPS,32.98,40.27)
fluid=seed.cut(solid).clean().intersect(box(.01,319.99,.01,399.99,33,40.25)).clean()
fs=fluid.solids().vals()
ss=solid.solids().vals()
ok=solid.val().isValid() and len(ss)==1 and fluid.val().isValid() and all(s.isValid() for s in fs) and len(fs)==1
arts={}
if ok:
 for name,obj in [("solid",solid),("fluid",fluid)]:
  for ext in ("step","stl"):
   p=f"{OUT}/AP22_REV_EM_{name.upper()}.{ext}"
   cq.exporters.export(obj,p)
   with open(p,"rb") as f:digest=hashlib.sha256(f.read()).hexdigest()
   arts[f"{name}_{ext}"]={"path":p,"bytes":os.path.getsize(p),"sha256":digest}
   if ext=="step":
    imported=cq.importers.importStep(p);bb=imported.val().BoundingBox()
    volume=sum(s.Volume() for s in imported.solids().vals())
    original_volume=sum(s.Volume() for s in obj.solids().vals())
    valid=imported.val().isValid() and imported.solids().size()==1 and abs(volume-original_volume)<1e-5
    arts[f"{name}_{ext}"]["reimport"]={"valid":valid,"components":imported.solids().size(),"volume_mm3":volume,"volume_delta_mm3":volume-original_volume,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax]}
    ok=ok and valid
print(json.dumps({"cadquery":cq.__version__,"solid_valid":solid.val().isValid(),"solid_components":len(ss),"solid_volume_mm3":round(sum(s.Volume() for s in ss),3),"fluid_valid":fluid.val().isValid(),"fluid_components":len(fs),"fluid_volume_mm3":round(sum(s.Volume() for s in fs),3),"exported":bool(arts),"export_reimport_pass":ok,"artifacts":arts,"limitations":["local shell/labyrinth audit geometry only; full solver domain not represented","Rev.EN labyrinth coverage/axial LOS FAIL","not a mesh","not CFD/FEA execution"]},indent=2))
if not ok:raise SystemExit(1)
