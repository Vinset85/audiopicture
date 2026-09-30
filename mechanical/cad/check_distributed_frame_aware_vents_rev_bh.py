# AudioPicture V2.2 frame-aware distributed vent layout Rev.BH
# Explicit distributed seed, verified against coarse Rev.C projection.
import math,json
R=1.5;CLEAR=1.0
def frame(x,y):
 s=(2<=x<=318 and 2<=y<=398 and not(12<=x<=308 and 12<=y<=388))
 s=s or (25.5<=x<=79.5 and 352<=y<=390) or (240.5<=x<=294.5 and 352<=y<=390)
 kos=[(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]
 if any(a<=x<=b and c<=y<=d for a,b,c,d in kos):s=False
 return s
def capsule_pts(c,step=.25):
 o,x0,x1,y0,y1=c;pts=[]
 for i in range(math.ceil((x1-x0)/step)):
  x=x0+(i+.5)*(x1-x0)/math.ceil((x1-x0)/step)
  for j in range(math.ceil((y1-y0)/step)):
   y=y0+(j+.5)*(y1-y0)/math.ceil((y1-y0)/step)
   if o=="V":
    cx=(x0+x1)/2;a=y0+R;b=y1-R;ok=(a<=y<=b and abs(x-cx)<=R) or (x-cx)**2+(y-a)**2<=R*R or (x-cx)**2+(y-b)**2<=R*R
   else:
    cy=(y0+y1)/2;a=x0+R;b=x1-R;ok=(a<=x<=b and abs(y-cy)<=R) or (x-a)**2+(y-cy)**2<=R*R or (x-b)**2+(y-cy)**2<=R*R
   if ok:pts.append((x,y))
 return pts
def clear(c):
 return all(not any(frame(x+dx,y+dy) for dx,dy in ((0,0),(CLEAR,0),(-CLEAR,0),(0,CLEAR),(0,-CLEAR))) for x,y in capsule_pts(c))
def mirror(c):
 o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
def gap(a,b):
 _,a0,a1,c0,c1=a;_,b0,b1,d0,d1=b
 dx=max(b0-a1,a0-b1,0);dy=max(d0-c1,c0-d1,0);return math.hypot(dx,dy)
# Distributed lower: use known frame openings created by inner ring + KOs; avoid service/voice/env obstacles.
LL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
# Upper: move inside top ring (y<=387) and use left free corridor; 5 vertical slots distributed x.
UL=[("V",17,20,315,360),("V",24,27,315,360),("V",31,34,315,360),("V",38,41,315,360),("V",45,48,315,360)]
LR=[mirror(c) for c in LL];UR=[mirror(c) for c in UL]
groups={"LL":LL,"LR":LR,"UL":UL,"UR":UR}
checks={}
for k,g in groups.items():
 checks[k]={"all_frame_clear":all(clear(c) for c in g),"min_pair_gap_mm":min(gap(a,b) for i,a in enumerate(g) for b in g[i+1:])}
print(json.dumps({"groups":groups,"checks":checks,
"all_frame_clear":all(v["all_frame_clear"] for v in checks.values()),
"all_web_ge_4":all(v["min_pair_gap_mm"]>=4 for v in checks.values()),
"note":"Explicit seed may fail because documented keepouts/cleat islands constrain these corridors; failure is informative and triggers search refinement."},indent=2))
