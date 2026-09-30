# AudioPicture V2.2 alternating-gate throat optimization Rev.BU
# Sampled LOS + geometric throat sweep. NOT CFD.
import json
GAP=2.8
def hit(p,q,r):
 x1,y1=p;x2,y2=q;a,b,c,d=r;dx=x2-x1;dy=y2-y1;t0=0.;t1=1.
 for P,Q in [(-dx,x1-a),(dx,b-x1),(-dy,y1-c),(dy,d-y1)]:
  if abs(P)<1e-12:
   if Q<0:return False
  else:
   t=Q/P
   if P<0:t0=max(t0,t)
   else:t1=min(t1,t)
   if t0>t1:return False
 return True
def clear_count(srcx,dstx,ys,obs):
 return sum(1 for sy in ys for dy in ys if not any(hit((srcx,sy),(dstx,dy),r) for r in obs))
# Lower fixed 24mm. Upper sweep symmetric end openings in 31mm bank.
out={"lower":{"opening_mm":24,"gate_throat_mm2_per_side":24*GAP}}
ys=[315.5+i for i in range(31)]
sweep=[]
for op in [9,10,11,12,13,14,15]:
 # bank 315..346. gate1 opens top; gate2 opens bottom
 obs=[(65,66.2,315,346-op),(69,70.2,315+op,346)]
 cc=clear_count(62,86,ys,obs)
 sweep.append({"opening_mm":op,"gate_throat_mm2_per_side":op*GAP,"clear_straight_paths":cc,"los_blocked":cc==0})
out["upper_sweep"]=sweep
valid=[x for x in sweep if x["los_blocked"]]
out["preferred_pre_cad"]=max(valid,key=lambda x:x["opening_mm"]) if valid else None
print(json.dumps(out,indent=2))
