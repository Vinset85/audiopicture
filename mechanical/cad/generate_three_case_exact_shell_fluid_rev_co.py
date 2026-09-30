# AudioPicture V2.2 exact-shell three-case CFD fluid boolean Rev.CO
# Geometry/boolean gate only. No CFD solver.
# Rebuilds promoted shell family in one script to ensure identical fluid construction.
import cadquery as cq, json
X,Y=320.,400.; Z0,Z1=37.8,40.; R=1.5; RW=2.2; RZ0=35.6
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mir(c):o,a,b,c0,d=c;return(o,320-b,320-a,c0,d)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mir(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mir(c) for i,c in enumerate(upperL)]
def cap(row,z0=37.0,z1=41.0):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return cq.Workplane("XY",origin=(0,0,z0)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(z1-z0)
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return cq.Workplane("XY",origin=(0,0,z0)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(z1-z0)
segments=[(0,RW,148,337),(X-RW,X,148,337),(18,X-18,0,RW),(18,X-18,Y-RW,Y)]
nodes=[(145,383),(175,383),(12,200),(308,200),(80,17),(240,17)]
left_gates=[(30,31.2,14,126),(34,35.2,38,150),(65,66.2,315,331),(69,70.2,330,346)]
def mirror_rect(r):a,b,c,d=r;return(320-b,320-a,c,d)
def shell(h):
 s=box(0,320,0,400,Z0,Z1)
 for r in segments:s=s.union(box(*r,RZ0,Z0))
 for v in vents:s=s.cut(cap(v))
 for x,y in nodes:s=s.union(cq.Workplane("XY",origin=(x,y,36)).circle(5).extrude(1.8))
 if h>0:
  bz=Z0-h
  for r in left_gates+[mirror_rect(r) for r in left_gates]:s=s.union(box(*r,bz,Z0))
 return s.clean()
# coarse frame/boards
frame=box(2,318,2,398,27,35).cut(box(12,308,12,388,26,36))
for r in [(25.5,79.5,352,390),(240.5,294.5,352,390)]:frame=frame.union(box(*r,27,35))
for r in [(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]:frame=frame.cut(box(*r,26,36))
frame=frame.clean()
mp=box(105,220,112,157,18,19.6); mc=box(85,235,315,370,17,18.6)
# Connected seed spans internal cavity + shell slab + rear plenum. Exact shell subtraction opens only real vents.
seed=box(0,320,0,400,10,44)
results={}
for name,h in [("CFD0",0.0),("CFD08",0.8),("CFD10",1.0)]:
 sh=shell(h)
 fluid=seed.cut(sh).cut(frame).cut(mp).cut(mc).clean()
 solids=fluid.solids().size()
 valid=fluid.val().isValid()
 # check air exists immediately on both sides of every exact vent footprint
 per={}
 for v in vents:
  probe=cap(v,37.6,40.2)
  q=fluid.intersect(probe)
  per[v[0]]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0
 results[name]={"valid":valid,"fluid_solids":solids,"all_vent_probes_open":all(x>0 for x in per.values()),
                "min_vent_probe_air_mm3":min(per.values()),"shell_solids":sh.solids().size()}
 cq.exporters.export(fluid,f"AP22_{name}_EXACT_SHELL_FLUID_REV_CO.step")
print(json.dumps(results,indent=2))
