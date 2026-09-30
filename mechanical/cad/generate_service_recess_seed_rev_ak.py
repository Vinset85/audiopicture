# AudioPicture V2.2 service-recess architecture kernel Rev.AK
# Parametric shell recess seed only. RJ45/boot dimensions are intentionally NOT frozen.
import cadquery as cq, json
X=320.;Y=400.;Z0=37.8;Z1=40.;T=2.2
SERVICE=(100.,220.,20.,48.)
# Seed opening deliberately inside frozen service region, leaving reinforcement land.
OPEN_W=72.; OPEN_H=16.; RAD=3.
cx=160.;cy=34.
x0=cx-OPEN_W/2;x1=cx+OPEN_W/2;y0=cy-OPEN_H/2;y1=cy+OPEN_H/2
assert x0>=SERVICE[0] and x1<=SERVICE[1] and y0>=SERVICE[2] and y1<=SERVICE[3]
# rear panel-only test coupon/kernel
panel=cq.Workplane("XY").box(X,Y,T,centered=(False,False,False)).translate((0,0,Z0))
# rounded rectangle made from rect + fillet, extruded through panel
cut=(cq.Workplane("XY",origin=(cx,cy,Z0-.2)).rect(OPEN_W,OPEN_H).vertices().fillet(RAD).extrude(T+.4))
shell=panel.cut(cut).clean()
# Inlet bounding rectangles from Rev.AD; opening must not intersect.
inlets=[]
for xs in (((4,7),(11,14)),((313,316),(306,309))):
 for yy in ((4,44),(52,92),(104,144)):
  for xx in xs:inlets.append((xx[0],xx[1],yy[0],yy[1]))
def box2(r,z0=0,z1=40):
 a,b,c,d=r
 return cq.Workplane("XY").box(b-a,d-c,z1-z0,centered=(False,False,False)).translate((a,c,z0))
ints=[]
for r in inlets:
 q=cut.intersect(box2(r));ints.append(sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0.)
# Frozen anti-lift conservative envelope from lower inlet gate
anti=(145,175,12,24)
q=cut.intersect(box2(anti));anti_iv=sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0.
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert all(v<1e-8 for v in ints) and anti_iv<1e-8
cq.exporters.export(shell,"AP22_SERVICE_RECESS_SEED_REV_AK.step")
print(json.dumps({"valid":True,"solid_count":1,"service_region":SERVICE,
"seed_opening_bbox_mm":[x0,x1,y0,y1],"seed_opening_wh_mm":[OPEN_W,OPEN_H],"corner_radius_mm":RAD,
"land_to_service_region_mm":{"left":x0-SERVICE[0],"right":SERVICE[1]-x1,"bottom":y0-SERVICE[2],"top":SERVICE[3]-y1},
"inlet_intersections_mm3":ints,"anti_lift_intersection_mm3":anti_iv,
"limitations":["opening size is architecture seed, not connector release","RJ45 MPN absent","plug/latch/boot sweep absent","24V/USB exact connector envelopes absent","not credited as thermal inlet"]},indent=2))
