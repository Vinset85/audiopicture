# AudioPicture V2.2 terminal chamber full dense LOS audit Rev.DM
# Independent full dense audit. NOT CFD/acoustic simulation.
import json
# Selected from Rev.DK zero-LOS family: compact candidate with favorable nonzero throat.
P=dict(L=36,W=48,roof_z=36.8,t=1.0,chL=24,chW=36,exitW=16,overlap=12)
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
def geom(p):
 L,W,rz,t,chL,chW,exitW,ov=[p[k] for k in ("L","W","roof_z","t","chL","chW","exitW","overlap")]
 x0=15.;x1=x0+L;y0=14.;y1=y0+W;zl=34.
 o=[(x0,x1,y0,y1,rz,37.8),(x0,x0+t,y0,y1,zl,rz),(x0,x1,y0,y0+t,zl,rz)]
 cx0=x1-chL;cx1=x1;cy0=y1-chW;cy1=y1
 o += [(cx1-t,cx1,cy0,cy1,zl,rz),(cx0,cx1,cy0,cy0+t,zl,rz)]
 ex0=cx0+t;ex1=min(cx1-t,ex0+exitW)
 if ex0>cx0:o.append((cx0,ex0,cy1-t,cy1,zl,rz))
 if ex1<cx1:o.append((ex1,cx1,cy1-t,cy1,zl,rz))
 bx=min(cx1-t,cx0+t+exitW+ov)
 o.append((bx-t,bx,cy0+t,cy1-t,zl,rz))
 return o,(ex1-ex0)*(rz-zl)
obs,throat=geom(P)
xs=(17.05,17.3,17.75,18.5,19.25,19.7,19.95,24.05,24.3,24.75,25.5,26.25,26.7,26.95)
ys=tuple(14+i*(136/16) for i in range(17));zs=(40.001,40.05,40.2)
src=[(x,y,z) for x in xs for y in ys for z in zs]
dxs=(36.2,40,44,48,52,58,66,75,90)
dys=tuple(14+i*(136/16) for i in range(17))
dzs=(32.2,33.0,33.8,34.6,35.4,36.2,36.75)
dst=[(x,y,z) for x in dxs for y in dys for z in dzs]
total=op=0;examples=[]
for a in src:
 for b in dst:
  total+=1
  if not any(hit(a,b,o) for o in obs):
   op+=1
   if len(examples)<10:examples.append({"source":a,"destination":b})
print(json.dumps({"candidate":P,"sources":len(src),"destinations":len(dst),"rays":total,"open":op,
"open_fraction":op/total,"throat_proxy_mm2":round(throat,2),"examples":examples,
"decision":"PASS sampled geometric LOS" if op==0 else "FAIL sampled geometric LOS",
"note":"Full dense geometric LOS only. PASS does not prove acoustic attenuation or thermal performance."},indent=2))
