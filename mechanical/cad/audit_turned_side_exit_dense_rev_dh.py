# AudioPicture V2.2 turned side-exit dense LOS recheck Rev.DH
# Independent denser geometric audit. NOT acoustic simulation.
import json
# Selected compact/high-throat coarse-pass candidate is encoded below from Rev.DF execution.
P=dict(L=36,W=48,roof_z=36.8,t=1.0,y_shift=0,elbow=16,overlap=6,slot=16)
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
 L,W,rz,t,ys,e,ov,slot=[p[k] for k in ("L","W","roof_z","t","y_shift","elbow","overlap","slot")]
 x0=15.;x1=x0+L;y0=14.+ys;y1=y0+W;zl=34.
 return [(x0,x1,y0,y1,rz,37.8),(x0,x0+t,y0,y1,zl,rz),(x0,x1,y0,y0+t,zl,rz),
 (x1-t,x1,y0,y1-slot,zl,rz),(x1-e,x1,y1-slot-ov,y1-slot-ov+t,zl,rz),
 (x1-e,x1-e+t,y1-slot-ov,y1,zl,rz)]
obs=geom(P)
# Dense edge-biased source cloud over both vent columns and full lower-bank Y span.
xs=(17.05,17.3,17.75,18.5,19.25,19.7,19.95,24.05,24.3,24.75,25.5,26.25,26.7,26.95)
ys=tuple(14+i*(136/16) for i in range(17))
zs=(40.001,40.05,40.2)
src=[(x,y,z) for x in xs for y in ys for z in zs]
# Dense cavity targets, including near exit edges and multiple Z planes.
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
throat=(P["slot"]-P["t"])*(P["roof_z"]-34.0)
print(json.dumps({"candidate":P,"sources":len(src),"destinations":len(dst),"rays":total,"open":op,
"open_fraction":op/total,"throat_proxy_mm2":throat,"examples":examples,
"decision":"PASS sampled geometric LOS" if op==0 else "FAIL sampled geometric LOS",
"note":"Dense geometric LOS only; zero rays would still not prove acoustic attenuation."},indent=2))
