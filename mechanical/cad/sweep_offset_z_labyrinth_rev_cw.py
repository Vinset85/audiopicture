# AudioPicture V2.2 offset-Z labyrinth sweep Rev.CW
# Deterministic 3D geometric LOS screening. NOT acoustic simulation.
import json,itertools
Z_SHELL=37.8
lowerL=[(17,20,14,54),(24,27,14,54),(17,20,62,102),(24,27,62,102),(17,20,110,150),(24,27,110,150)]
upperL=[(17,62,315,318),(17,62,322,325),(17,62,329,332),(17,62,336,339),(17,62,343,346)]
shell_gates=[(30,31.2,14,126),(34,35.2,38,150),(65,66.2,315,331),(69,70.2,330,346)]
def mirror(r):x0,x1,y0,y1=r;return(320-x1,320-x0,y0,y1)
frame_boxes=[(2,318,2,12,27,35),(2,318,388,398,27,35),(2,12,12,388,27,35),(308,318,12,388,27,35),(25.5,79.5,352,390,27,35),(240.5,294.5,352,390,27,35)]
def hit(p0,p1,b):
 lo,hi=0.,1.
 for a,c,mn,mx in zip(p0,p1,b[::2],b[1::2]):
  d=c-a
  if abs(d)<1e-12:
   if a<mn or a>mx:return False
  else:
   u=(mn-a)/d;v=(mx-a)/d
   if u>v:u,v=v,u
   lo=max(lo,u);hi=min(hi,v)
   if lo>hi:return False
 return True
def pts(slots,side):
 q=[]
 for r in slots:
  x0,x1,y0,y1=r if side=="L" else mirror(r)
  for fx in (.2,.5,.8):
   for fy in (.2,.5,.8):q.append((x0+(x1-x0)*fx,y0+(y1-y0)*fy,40.05))
 return q
def dst(kind,side):
 xs=((40,55,75) if side=="L" else (245,265,280)) if kind=="lower" else ((40,55,80) if side=="L" else (240,265,280))
 ys=(25,70,120,145) if kind=="lower" else (318,330,342)
 return [(x,y,z) for x in xs for y in ys for z in (33.0,34.0,35.0,36.0)]
# Candidate frame-side curtains sit below shell baffles, with deliberate Z clearance.
# They are shifted inward in X and use opposite Y gate sense.
def candidate_boxes(h_shell,z_top,depth,dx):
 sg=[(a,b,c,d,Z_SHELL-h_shell,Z_SHELL) for a,b,c,d in shell_gates+[mirror(r) for r in shell_gates]]
 # lower: two inward shifted curtains spanning complementary Y windows
 fl=[(36+dx,37.2+dx,38,150),(40+dx,41.2+dx,14,126)]
 # upper: complementary windows
 fl += [(71+dx,72.2+dx,330,346),(75+dx,76.2+dx,315,331)]
 fl=fl+[mirror(r) for r in fl]
 fg=[(a,b,c,d,z_top-depth,z_top) for a,b,c,d in fl]
 return sg+fg+frame_boxes
def audit(obs):
 total=openr=0
 for kind,slots in (("lower",lowerL),("upper",upperL)):
  for side in ("L","R"):
   for a in pts(slots,side):
    for b in dst(kind,side):
     total+=1
     if not any(hit(a,b,o) for o in obs):openr+=1
 return total,openr
rows=[]
for hs,zt,dep,dx in itertools.product((0.8,1.0),(35.0,34.8,34.5),(1.0,1.5,2.0),(0,2,4,6)):
 total,op=audit(candidate_boxes(hs,zt,dep,dx))
 gap=(Z_SHELL-hs)-zt
 rows.append({"shell_h":hs,"frame_z_top":zt,"frame_depth":dep,"dx":dx,"z_clearance":round(gap,3),"rays":total,"open":op})
rows.sort(key=lambda r:(r["open"],-r["z_clearance"],r["frame_depth"],r["dx"]))
print(json.dumps({"best":rows[:12],"zero_open":[r for r in rows if r["open"]==0],"tested":len(rows),
"note":"Zero sampled straight rays is only a geometric screening pass, not acoustic attenuation proof. Frame-side curtains remain mechanically independent from shell."},indent=2))
