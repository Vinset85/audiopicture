# AudioPicture V2.2 terminal chamber dense LOS sweep Rev.DK
# Dense deterministic geometric screening. NOT CFD/acoustic simulation.
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
# Dense edge-biased source population derived from Rev.DH.
xs=(17.05,17.3,17.75,18.5,19.25,19.7,19.95,24.05,24.3,24.75,25.5,26.25,26.7,26.95)
ys=tuple(14+i*(136/16) for i in range(17))
src=[(x,y,z) for x in xs for y in ys for z in (40.001,40.05,40.2)]
# Reduced-but-edge-aware destination set for parameter search; finalists require full Rev.DH-size recheck.
dxs=(38,44,52,62,75,90); dys=tuple(14+i*(136/12) for i in range(13)); dzs=(32.2,33.4,34.6,35.8,36.75)
dst=[(x,y,z) for x in dxs for y in dys for z in dzs]
# Covered duct terminates in a roofed chamber. Chamber exit faces +Y.
# baffle overlap shields inlet-to-exit diagonal.
def geom(L,W,rz,t,chL,chW,exitW,ov):
 x0=15.; x1=x0+L; y0=14.; y1=y0+W; zl=34.
 # duct roof + outer/low side
 o=[(x0,x1,y0,y1,rz,37.8),(x0,x0+t,y0,y1,zl,rz),(x0,x1,y0,y0+t,zl,rz)]
 # chamber extends inward in X at duct end
 cx0=x1-chL; cx1=x1; cy0=y1-chW; cy1=y1
 # terminal X wall, chamber -Y wall, internal shielding baffle
 o += [(cx1-t,cx1,cy0,cy1,zl,rz),(cx0,cx1,cy0,cy0+t,zl,rz)]
 # +Y face is mostly closed; exit aperture is near inward-X side
 # wall segments around exit
 ex0=cx0+t; ex1=min(cx1-t,ex0+exitW)
 if ex0>cx0: o.append((cx0,ex0,cy1-t,cy1,zl,rz))
 if ex1<cx1: o.append((ex1,cx1,cy1-t,cy1,zl,rz))
 # baffle hangs inside chamber, offset behind exit projection
 bx=min(cx1-t,cx0+t+exitW+ov)
 o.append((bx-t,bx,cy0+t,cy1-t,zl,rz))
 return o, max(0.,ex1-ex0)*(rz-zl)
rows=[]
for L,W,rz,t,chL,chW,exitW,ov in itertools.product(
 (36,44),(48,60),(36.5,36.8),(1.0,1.2),(16,20,24),(20,28,36),(8,12,16),(4,8,12)):
 o,th=geom(L,W,rz,t,chL,chW,exitW,ov)
 total=op=0
 for a in src:
  for b in dst:
   total+=1
   if not any(hit(a,b,q) for q in o):op+=1
 rows.append(dict(L=L,W=W,roof_z=rz,t=t,chL=chL,chW=chW,exitW=exitW,overlap=ov,
                  throat_mm2=round(th,2),rays=total,open=op))
rows.sort(key=lambda r:(r["open"],-r["throat_mm2"],r["L"],r["chL"],r["chW"]))
zero=[r for r in rows if r["open"]==0 and r["throat_mm2"]>0]
print(json.dumps({"tested":len(rows),"sources":len(src),"destinations":len(dst),"rays_per_case":len(src)*len(dst),
"zero_count":len(zero),"best":rows[:20],"zero_candidates":zero[:30],
"note":"Dense parameter-search LOS screen; any zero candidate still requires full independent Rev.DH-size recheck and real-solid audit."},indent=2))
