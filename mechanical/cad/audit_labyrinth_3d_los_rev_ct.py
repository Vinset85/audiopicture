# AudioPicture V2.2 3D acoustic line-of-sight audit Rev.CT
# Deterministic geometric ray audit. NOT acoustic simulation.
import math, json
# Coordinates: Z increases rearward. Shell inner face Z=37.8; frame rear Z=35.
# Test rays from rear/external side of each bank toward interior cavity.
# Obstacles: shell-side alternating baffles and coarse PC-CF ring/cleat projection.
# A ray is blocked if it intersects any baffle box or frame box.
X=320.; Z_SHELL=37.8
lowerL=[(17,20,14,54),(24,27,14,54),(17,20,62,102),(24,27,62,102),(17,20,110,150),(24,27,110,150)]
upperL=[(17,62,315,318),(17,62,322,325),(17,62,329,332),(17,62,336,339),(17,62,343,346)]
gatesL=[(30,31.2,14,126),(34,35.2,38,150),(65,66.2,315,331),(69,70.2,330,346)]
def mirror(r):x0,x1,y0,y1=r;return(320-x1,320-x0,y0,y1)
# Coarse frame as boxes: ring strips plus cleat islands, minus KOs are conservatively NOT modeled here;
# this means frame blocking can be overestimated. Any OPEN ray is therefore strong evidence of LOS.
frame_boxes=[
 (2,318,2,12,27,35),(2,318,388,398,27,35),(2,12,12,388,27,35),(308,318,12,388,27,35),
 (25.5,79.5,352,390,27,35),(240.5,294.5,352,390,27,35)
]
def seg_box(p0,p1,b):
 # slab intersection, segment t in [0,1]
 lo,hi=0.,1.
 for a,c,mn,mx in zip(p0,p1,b[::2],b[1::2]):
  d=c-a
  if abs(d)<1e-12:
   if a<mn or a>mx:return False
  else:
   t1=(mn-a)/d;t2=(mx-a)/d
   if t1>t2:t1,t2=t2,t1
   lo=max(lo,t1);hi=min(hi,t2)
   if lo>hi:return False
 return True
def baffle_boxes(h):
 z0=Z_SHELL-h
 rs=gatesL+[mirror(r) for r in gatesL]
 return [(a,b,c,d,z0,Z_SHELL) for a,b,c,d in rs]
def sample_bank(slots,side):
 pts=[]
 for r in slots:
  x0,x1,y0,y1=r if side=="L" else mirror(r)
  for fx in (.2,.5,.8):
   for fy in (.2,.5,.8):
    pts.append((x0+(x1-x0)*fx,y0+(y1-y0)*fy,40.05))
 return pts
def destinations(kind,side):
 # interior points beyond gates, z values deliberately include under-baffle corridor
 if kind=="lower":
  xs=(40,55,75) if side=="L" else (245,265,280)
  ys=(25,70,120,145)
 else:
  xs=(40,55,80) if side=="L" else (240,265,280)
  ys=(318,330,342)
 return [(x,y,z) for x in xs for y in ys for z in (34.2,35.2,36.0,36.8)]
def audit(h):
 obs=baffle_boxes(h)+frame_boxes
 out={}
 for kind,slots in [("lower",lowerL),("upper",upperL)]:
  for side in ("L","R"):
   src=sample_bank(slots,side); dst=destinations(kind,side)
   total=openr=0; example=None
   for a in src:
    for b in dst:
     total+=1
     if not any(seg_box(a,b,o) for o in obs):
      openr+=1
      if example is None:example={"source":a,"destination":b}
   out[kind+"_"+side]={"rays":total,"open":openr,"blocked":total-openr,"open_fraction":openr/total,"example_open":example}
 return out
res={}
for h in (0.8,1.0):
 a=audit(h);res[str(h)]={"banks":a,"any_open":any(v["open"]>0 for v in a.values()),"total_open":sum(v["open"] for v in a.values()),"total_rays":sum(v["rays"] for v in a.values())}
print(json.dumps({"method":"sampled 3D segment-vs-box LOS; frame model conservative blocking","results":res,
"interpretation":"Any open ray disproves complete geometric 3D LOS blocking for the sampled domain. Zero open rays would not prove acoustic attenuation."},indent=2))
