# AudioPicture V2.2 covered duct with turned side-exit sweep Rev.DF
# Deterministic geometric LOS screening only. NOT CFD/acoustic simulation.
import itertools,json
def hit(a,b,q):
 lo,hi=0.,1.
 for p,r,mn,mx in zip(a,b,q[::2],q[1::2]):
  d=r-p
  if abs(d)<1e-12:
   if p<mn or p>mx:return False
  else:
   u,v=(mn-p)/d,(mx-p)/d
   if u>v:u,v=v,u
   lo=max(lo,u);hi=min(hi,v)
   if lo>hi:return False
 return True
src=[(x,y,40.05) for x in (17.6,18.5,19.4,24.6,25.5,26.4) for y in (18,34,50,66,82,98,114,130,146)]
dst=[(x,y,z) for x in (48,60,75,90) for y in (20,45,70,95,120,145) for z in (32.5,33.5,34.5,35.5,36.5)]
# Baseline covered duct plus an internal elbow:
# terminal cheek shields direct side opening; discharge is turned toward +Y.
def geom(L,W,rz,t,ys,elbow,overlap,slot):
 x0=15.;x1=x0+L;y0=14.+ys;y1=y0+W;zl=34.0
 roof=(x0,x1,y0,y1,rz,37.8)
 outer=(x0,x0+t,y0,y1,zl,rz)
 side0=(x0,x1,y0,y0+t,zl,rz)
 # terminal wall spans most width, leaving a controlled +Y-side throat
 end=(x1-t,x1,y0,y1-slot,zl,rz)
 # elbow cheek extends back toward -X from the terminal wall near the throat
 cheek=(x1-elbow,x1,y1-slot-overlap,y1-slot-overlap+t,zl,rz)
 # cap/return above plan-view throat region; same z range as solid wall
 returnwall=(x1-elbow,x1-elbow+t,y1-slot-overlap,y1,zl,rz)
 return [roof,outer,side0,end,cheek,returnwall]
rows=[]
for L,W,rz,t,ys,elbow,ov,slot in itertools.product(
 (36,44,52),(48,60),(36.5,36.8),(1.0,1.2),(0,8),(8,12,16),(2,4,6),(10,12,16)):
 obs=geom(L,W,rz,t,ys,elbow,ov,slot)
 total=op=0
 for a in src:
  for b in dst:
   total+=1
   if not any(hit(a,b,o) for o in obs):op+=1
 free_h=rz-34.0
 throat=max(0.,slot-t)*free_h
 rows.append(dict(L=L,W=W,roof_z=rz,t=t,y_shift=ys,elbow=elbow,overlap=ov,slot=slot,
                  throat_mm2=round(throat,2),rays=total,open=op))
rows.sort(key=lambda r:(r["open"],-r["throat_mm2"],r["L"],r["elbow"],r["overlap"]))
zero=[r for r in rows if r["open"]==0 and r["throat_mm2"]>0]
print(json.dumps({"tested":len(rows),"zero_count":len(zero),"best":rows[:20],"zero_candidates":zero[:40],
"note":"Normalized geometric screening. Zero sampled LOS is necessary, not sufficient, and throat is only a local geometric proxy."},indent=2))
