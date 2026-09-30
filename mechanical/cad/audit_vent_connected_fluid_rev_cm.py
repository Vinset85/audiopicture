# AudioPicture V2.2 vent-connected fluid connectivity audit Rev.CM
# Geometric connectivity audit only. No CFD.
import cadquery as cq, json
X,Y=320.,400.; R=1.5
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mir(c):o,a,b,c0,d=c;return(o,320-b,320-a,c0,d)
vents=[("IL"+str(i+1),)+c for i,c in enumerate(lowerL)]+[("IR"+str(i+1),)+mir(c) for i,c in enumerate(lowerL)]+[("UL"+str(i+1),)+c for i,c in enumerate(upperL)]+[("UR"+str(i+1),)+mir(c) for i,c in enumerate(upperL)]
def cap(row,z0=35.0,z1=44.0):
 n,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2; xa=x0+R; xb=x1-R
  return cq.Workplane("XY",origin=(0,0,z0)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(z1-z0)
 cx=(x0+x1)/2; ya=y0+R; yb=y1-R
 return cq.Workplane("XY",origin=(0,0,z0)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(z1-z0)
# Internal seed reaches shell inner plane; rear plenum is the 4mm wall gap behind product.
internal=box(0,320,0,400,10,37.8)
rear_plenum=box(0,320,0,400,40,44)
channels=None
for v in vents:
 c=cap(v,35,44)
 channels=c if channels is None else channels.union(c)
fluid=internal.union(channels).union(rear_plenum).clean()
# coarse frame and boards are removed as solid obstructions
frame=box(2,318,2,398,27,35).cut(box(12,308,12,388,26,36))
for r in [(25.5,79.5,352,390),(240.5,294.5,352,390)]: frame=frame.union(box(*r,27,35))
for r in [(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]: frame=frame.cut(box(*r,26,36))
frame=frame.clean()
main_p=box(105,220,112,157,18,19.6); main_c=box(85,235,315,370,17,18.6)
fluid=fluid.cut(frame).cut(main_p).cut(main_c).clean()
# Per-vent channel connectivity: every channel must intersect both internal and rear plenum.
checks={}
for v in vents:
 c=cap(v,35,44)
 a=c.intersect(internal); b=c.intersect(rear_plenum)
 checks[v[0]]={"to_internal_mm3":sum(s.Volume() for s in a.solids().vals()) if a.solids().size() else 0,
               "to_rear_mm3":sum(s.Volume() for s in b.solids().vals()) if b.solids().size() else 0}
bb=fluid.val().BoundingBox()
print(json.dumps({"valid":fluid.val().isValid(),"fluid_solids":fluid.solids().size(),"vent_count":len(vents),
"all_vents_touch_internal":all(v["to_internal_mm3"]>0 for v in checks.values()),
"all_vents_touch_rear_plenum":all(v["to_rear_mm3"]>0 for v in checks.values()),
"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"zmin":bb.zmin,"zmax":bb.zmax,
"note":"This is a connectivity audit. It does not yet subtract the exact shell/baffle solid or include the external room domain."},indent=2))
cq.exporters.export(fluid,"AP22_CFD_VENT_CONNECTED_FLUID_SEED_REV_CM.step")
