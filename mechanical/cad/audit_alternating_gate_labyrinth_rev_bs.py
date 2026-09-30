# AudioPicture V2.2 alternating-gate labyrinth topology Rev.BS
# 2D deterministic topology design/audit. NOT CFD.
import json
# Each gate spans bank height except one opening; second gate opening is opposite.
# x direction is from vents -> cavity.
# lower bank y14..150; upper y315..346.
cases={
 "lower":{"src_x":27.,"dst_x":52.,"ys":[18+i*4 for i in range(33)],
  "obs":[(30,31.2,14,126),(34,35.2,38,150)]}, # gate1 opens top 24; gate2 opens bottom 24
 "upper":{"src_x":62.,"dst_x":86.,"ys":[316+i*2 for i in range(15)],
  "obs":[(65,66.2,315,337),(69,70.2,324,346)]} # gate1 opens top 9; gate2 opens bottom 9
}
def hit(p,q,r):
 x1,y1=p;x2,y2=q;a,b,c,d=r;dx=x2-x1;dy=y2-y1;t0=0;t1=1
 for P,Q in [(-dx,x1-a),(dx,b-x1),(-dy,y1-c),(dy,d-y1)]:
  if abs(P)<1e-12:
   if Q<0:return False
  else:
   t=Q/P
   if P<0:t0=max(t0,t)
   else:t1=min(t1,t)
   if t0>t1:return False
 return True
out={}
for n,c in cases.items():
 clear=[]
 for sy in c["ys"]:
  for dy in c["ys"]:
   if not any(hit((c["src_x"],sy),(c["dst_x"],dy),r) for r in c["obs"]):clear.append((sy,dy))
 out[n]={"clear_straight_paths":len(clear),"los_blocked":not clear,"examples":clear[:5],"obstacles":c["obs"]}
print(json.dumps({"results":out,"criterion":"zero sampled straight source-to-cavity paths","note":"Opposite openings are intended to force lateral travel between gates; exact free throat and 3D integration remain next gates."},indent=2))
