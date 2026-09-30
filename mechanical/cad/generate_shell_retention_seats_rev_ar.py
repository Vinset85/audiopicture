# AudioPicture V2.2 ASA six retention-seat packaging kernel Rev.AR
# Local ASA reinforcement pads only; no hole, insert or clamped-contact claim.
import cadquery as cq, json, math
X=320.;Y=400.;Z0=37.8;Z1=40.;T=2.2
SEAT_D=10.;SEAT_H=1.8;SZ0=Z0-SEAT_H
nodes=[("TOP_L",145.,383.),("TOP_R",175.,383.),("SIDE_L",12.,200.),("SIDE_R",308.,200.),("BOT_L",80.,17.),("BOT_R",240.,17.)]
panel=cq.Workplane("XY").box(X,Y,T,centered=(False,False,False)).translate((0,0,Z0))
shell=panel
for _,x,y in nodes:
 p=cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H)
 shell=shell.union(p)
shell=shell.clean()
# exclusions: exact executed vent bounding envelopes + service + anti-lift
upper=[(4,49,393,396),(77,122,393,396),(82,127,386,389),(4,7,341,386),(13,16,341,386),(271,316,393,396),(198,243,393,396),(193,238,386,389),(313,316,341,386),(306,309,341,386)]
lower=[]
for xs in (((4,7),(11,14)),((313,316),(306,309))):
 for yy in ((4,44),(52,92),(104,144)):
  for xx in xs:lower.append((xx[0],xx[1],yy[0],yy[1]))
ex=[("SERVICE",(100,220,20,48)),("ANTILIFT",(145,175,12,24))]
for i,r in enumerate(upper):ex.append((f"U{i+1}",r))
for i,r in enumerate(lower):ex.append((f"L{i+1}",r))
def bx(r):
 a,b,c,d=r
 return cq.Workplane("XY").box(b-a,d-c,50,centered=(False,False,False)).translate((a,c,0))
hits={}
for n,x,y in nodes:
 p=cq.Workplane("XY",origin=(x,y,SZ0)).circle(SEAT_D/2).extrude(SEAT_H)
 hits[n]={en:sum(s.Volume() for s in p.intersect(bx(r)).solids().vals()) if p.intersect(bx(r)).solids().size() else 0. for en,r in ex}
bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert all(v<1e-8 for h in hits.values() for v in h.values())
assert bb.zmax<=40.
vol_added=shell.val().Volume()-panel.val().Volume()
print(json.dumps({"valid":True,"solid_count":1,"seat_count":6,"seat_diameter_mm":SEAT_D,"seat_protrusion_mm":SEAT_H,
"seat_z_mm":[SZ0,Z0],"nominal_gap_to_pc_cf_z35_mm":SZ0-35.,
"added_asa_volume_mm3":vol_added,"exclusion_intersections_mm3":hits,
"limitations":["seat dimensions are packaging seeds","no hole/insert/fastener","1.0mm gap is not clamping stack or production tolerance","full vent-edge master fusion is next gate"]},indent=2))
