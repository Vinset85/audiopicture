# AudioPicture V2.2 covered lateral duct LOS/throat sweep Rev.DC
# Geometric screening only. NOT CFD and NOT acoustic simulation.
import itertools,json
# Normalized left-bank duct model, mirrored by symmetry in product.
# External source points represent promoted vent apertures; internal targets represent cavity.
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
# Source bank envelope representative of left vent columns.
src=[(x,y,40.05) for x in (17.6,18.5,19.4,24.6,25.5,26.4) for y in (18,34,50,66,82,98,114,130,146)]
# Interior sample cloud deliberately broad in Y/Z.
dst=[(x,y,z) for x in (48,60,75,90) for y in (20,45,70,95,120,145) for z in (32.5,33.5,34.5,35.5,36.5)]
# Duct concept: roof over vent projection + outer cheek + inward end wall;
# discharge is an opening on the cavity-facing side after lateral travel.
# We screen straight rays against roof/cheeks/end wall while preserving an open throat.
def obstacles(L,W,roof_z,t,exit_y_shift):
 x0=15.; x1=x0+L
 y0=14.+exit_y_shift; y1=y0+W
 # roof spans shallow rear zone; walls descend toward frame but stop above lower bound.
 roof=(x0,x1,y0,y1,roof_z,37.8)
 outer=(x0,x0+t,y0,y1,34.0,roof_z)
 # end wall leaves a side discharge slot of 12 mm at shifted end of Y range
 slot=12.
 end1=(x1-t,x1,y0,y1-slot,34.0,roof_z)
 side=(x0,x1,y0,y0+t,34.0,roof_z)
 return [roof,outer,end1,side],slot
rows=[]
for L,W,rz,t,ys in itertools.product((28,36,44,52),(36,48,60),(36.2,36.5,36.8),(1.0,1.2),(0,8,16)):
 obs,slot=obstacles(L,W,rz,t,ys)
 total=op=0
 for a in src:
  for b in dst:
   total+=1
   if not any(hit(a,b,o) for o in obs):op+=1
 # geometric minimum throat proxy: side discharge slot x vertical free height
 free_h=max(0.,rz-34.0)
 throat=slot*free_h
 rows.append(dict(L=L,W=W,roof_z=rz,t=t,y_shift=ys,rays=total,open=op,throat_mm2=round(throat,2)))
rows.sort(key=lambda r:(r["open"],-r["throat_mm2"],r["L"],r["W"],r["t"]))
zero=[r for r in rows if r["open"]==0]
print(json.dumps({"tested":len(rows),"best":rows[:20],"zero_count":len(zero),"zero_candidates":zero[:30],
"note":"Throat is a geometric proxy per normalized duct, not total system effective area. Zero sampled LOS is necessary screening only."},indent=2))
