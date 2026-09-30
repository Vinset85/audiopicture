# AudioPicture V2.2 planar labyrinth line-of-sight audit Rev.BR
# 2D geometric topology screen; NOT CFD/acoustic simulation.
import json, math
# left banks; right symmetric
# obstacle rectangles from Rev.BP
LOW=[(29,30.2,14,82),(33,34.2,82,150)]
UP=[(64,65.2,315,332),(68,69.2,329,346)]
# source samples at inward edge of vent banks, cavity target samples further inward
cases={
 "lower_left":{"src":[(27,y) for y in range(18,147,8)],"dst":[(45,y) for y in range(18,147,8)],"obs":LOW},
 "upper_left":{"src":[(62,y) for y in range(316,346,3)],"dst":[(82,y) for y in range(316,346,3)],"obs":UP}
}
def seg_rect(p,q,r):
 x1,y1=p;x2,y2=q;rx0,rx1,ry0,ry1=r
 # Liang-Barsky inclusive
 dx=x2-x1;dy=y2-y1;t0=0.;t1=1.
 for p_,q_ in [(-dx,x1-rx0),(dx,rx1-x1),(-dy,y1-ry0),(dy,ry1-y1)]:
  if abs(p_)<1e-12:
   if q_<0:return False
  else:
   t=q_/p_
   if p_<0:t0=max(t0,t)
   else:t1=min(t1,t)
   if t0>t1:return False
 return True
out={}
for name,c in cases.items():
 clear=[]
 for s in c["src"]:
  for d in c["dst"]:
   if not any(seg_rect(s,d,r) for r in c["obs"]):clear.append((s,d))
 out[name]={"source_count":len(c["src"]),"target_count":len(c["dst"]),"clear_line_count":len(clear),"example_clear_lines":clear[:5],
 "direct_los_blocked":len(clear)==0}
print(json.dumps({"audit":"all sampled source-to-cavity straight lines must be blocked for LOS pass","results":out,
"limitations":["sampled 2D screen","does not prove two-turn streamline","under-baffle Z bypass intentionally exists","not CFD or acoustic ray model"]},indent=2))
