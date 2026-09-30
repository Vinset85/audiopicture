# AudioPicture V2.2 two-turn hood LOS sweep Rev.CZ
# Deterministic geometric screening only. NOT acoustic simulation.
import itertools,json
Z=37.8
lower=[(17,20,14,54),(24,27,14,54),(17,20,62,102),(24,27,62,102),(17,20,110,150),(24,27,110,150)]
upper=[(17,62,315,318),(17,62,322,325),(17,62,329,332),(17,62,336,339),(17,62,343,346)]
def mir(r):a,b,c,d=r;return(320-b,320-a,c,d)
frame=[(2,318,2,12,27,35),(2,318,388,398,27,35),(2,12,12,388,27,35),(308,318,12,388,27,35),(25.5,79.5,352,390,27,35),(240.5,294.5,352,390,27,35)]
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
def sources(slots,side):
 out=[]
 for r in slots:
  x0,x1,y0,y1=r if side=="L" else mir(r)
  for fx in (.2,.5,.8):
   for fy in (.2,.5,.8):out.append((x0+(x1-x0)*fx,y0+(y1-y0)*fy,40.05))
 return out
def dest(kind,side):
 xs=((42,55,72) if side=="L" else (248,265,278)) if kind=="lower" else ((42,58,82) if side=="L" else (238,262,278))
 ys=(25,55,90,125,145) if kind=="lower" else (318,327,336,344)
 return [(x,y,z) for x in xs for y in ys for z in (32.5,33.5,34.5,35.5,36.5)]
# Two-turn concept:
# A: shell cheek immediately inward of vent bank, descending from shell.
# B: deeper independent hood farther inward; complementary Y opening.
# C: short return lip on B to prevent diagonal Z shortcut.
def obs(hs,zt,depth,dx,lip):
 o=list(frame)
 # lower left A/B/C
 A=[(29,30.2,14,132,Z-hs,Z),(33,34.2,32,150,Z-hs,Z)]
 B=[(38+dx,39.2+dx,32,150,zt-depth,zt),(43+dx,44.2+dx,14,132,zt-depth,zt)]
 C=[(39.2+dx,39.2+dx+lip,32,33.2,zt-depth,zt),(42+dx-lip,42+dx,130.8,132,zt-depth,zt)]
 # upper left, rotated gate sense in Y
 A += [(64,65.2,315,334,Z-hs,Z),(68,69.2,327,346,Z-hs,Z)]
 B += [(73+dx,74.2+dx,327,346,zt-depth,zt),(78+dx,79.2+dx,315,334,zt-depth,zt)]
 C += [(74.2+dx,74.2+dx+lip,327,328.2,zt-depth,zt),(77+dx-lip,77+dx,332.8,334,zt-depth,zt)]
 boxes=A+B+C
 boxes += [(320-b,320-a,c,d,e,f) for a,b,c,d,e,f in boxes]
 return o+boxes
def audit(o):
 total=op=0
 for kind,slots in (("lower",lower),("upper",upper)):
  for side in ("L","R"):
   for a in sources(slots,side):
    for b in dest(kind,side):
     total+=1
     if not any(hit(a,b,q) for q in o):op+=1
 return total,op
rows=[]
for hs,zt,dep,dx,lip in itertools.product((0.8,1.0),(34.8,34.5,34.2),(1.5,2.0,2.5),(0,2,4),(1.0,2.0,3.0)):
 clearance=(Z-hs)-zt
 total,op=audit(obs(hs,zt,dep,dx,lip))
 rows.append(dict(shell_h=hs,frame_z_top=zt,depth=dep,dx=dx,lip=lip,z_clearance=round(clearance,3),rays=total,open=op))
rows.sort(key=lambda r:(r["open"],-r["z_clearance"],r["depth"],r["lip"],r["dx"]))
zero=[r for r in rows if r["open"]==0 and r["z_clearance"]>0]
print(json.dumps({"tested":len(rows),"best":rows[:15],"zero_open_positive_clearance":zero[:30],"zero_count":len(zero),
"note":"Geometric sampled LOS only. Zero rays is necessary screening, not acoustic attenuation proof."},indent=2))
