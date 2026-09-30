# AudioPicture V2.2 frame-aware vent relocation solver Rev.BG
# Deterministic grid search: zero projected overlap with Rev.C PC-CF + documented KOs.
import math,json
R=1.5; WEB=4.; EDGE=4.; FRAME_CLEAR=1.0
def frame(x,y):
 s=(2<=x<=318 and 2<=y<=398 and not(12<=x<=308 and 12<=y<=388))
 s=s or (25.5<=x<=79.5 and 352<=y<=390) or (240.5<=x<=294.5 and 352<=y<=390)
 kos=[(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]
 if any(a<=x<=b and c<=y<=d for a,b,c,d in kos):s=False
 return s
def cap_points(o,x0,x1,y0,y1,step=.5):
 pts=[]
 nx=max(1,math.ceil((x1-x0)/step));ny=max(1,math.ceil((y1-y0)/step))
 for i in range(nx):
  x=x0+(i+.5)*(x1-x0)/nx
  for j in range(ny):
   y=y0+(j+.5)*(y1-y0)/ny
   if o=="H":
    cy=(y0+y1)/2;a=x0+R;b=x1-R
    inside=(a<=x<=b and abs(y-cy)<=R) or (x-a)**2+(y-cy)**2<=R*R or (x-b)**2+(y-cy)**2<=R*R
   else:
    cx=(x0+x1)/2;a=y0+R;b=y1-R
    inside=(a<=y<=b and abs(x-cx)<=R) or (x-cx)**2+(y-a)**2<=R*R or (x-cx)**2+(y-b)**2<=R*R
   if inside:pts.append((x,y))
 return pts
def clear_frame(c):
 o,x0,x1,y0,y1=c
 for x,y in cap_points(*c):
  # conservative 1mm cardinal clearance around sampled capsule points
  if any(frame(x+dx,y+dy) for dx,dy in ((0,0),(FRAME_CLEAR,0),(-FRAME_CLEAR,0),(0,FRAME_CLEAR),(0,-FRAME_CLEAR))):return False
 return True
def bbox_gap(a,b):
 _,ax0,ax1,ay0,ay1=a;_,bx0,bx1,by0,by1=b
 dx=max(bx0-ax1,ax0-bx1,0);dy=max(by0-ay1,ay0-by1,0)
 return math.hypot(dx,dy)
def select(cands,n):
 # deterministic spread: prefer candidates furthest from already selected, then central-ish x.
 sel=[]
 for c in cands:
  if all(bbox_gap(c,s)>=WEB for s in sel):sel.append(c)
  if len(sel)==n:return sel
 return []
# Search free interior bands, away from outer PC-CF ring. Preserve hidden lower/upper rear architecture.
# Lower 3x40: vertical, x in 17..99 left and mirrored right, y in 4..155.
# Upper 3x45: vertical/horizontal in projected-free zones y315..396.
lowerL=[]
for x in range(17,97):
 for y in range(4,116):
  c=("V",x,x+3,y,y+40)
  if x>=EDGE and x+3<=160-EDGE and y>=EDGE and y+40<=155 and clear_frame(c):lowerL.append(c)
# rank lateral-first then low/mid/high sweep
lowerL.sort(key=lambda c:(c[1],c[3]))
# custom select aims 6 with separation
LL=select(lowerL,6)
def mirror(c):
 o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
LR=[mirror(c) for c in LL]
# upper candidates in free interior; enumerate both orientations, left half only
upperL=[]
for o in ("H","V"):
 if o=="H":
  for x in range(17,112):
   for y in range(315,394):
    c=(o,x,x+45,y,y+3)
    if x+45<=156 and y+3<=396 and clear_frame(c):upperL.append(c)
 else:
  for x in range(17,153):
   for y in range(315,349):
    c=(o,x,x+3,y,y+45)
    if y+45<=396 and clear_frame(c):upperL.append(c)
upperL.sort(key=lambda c:(-c[3],c[1],c[0]))
UL=select(upperL,5);UR=[mirror(c) for c in UL]
assert len(LL)==6 and len(UL)==5
allc=LL+LR+UL+UR
assert all(clear_frame(c) for c in allc)
# area exact capsule
ain=(40-3)*3+math.pi*R*R
aout=(45-3)*3+math.pi*R*R
print(json.dumps({"frame_clearance_seed_mm":FRAME_CLEAR,"web_target_mm":WEB,
"lower_left":LL,"lower_right":LR,"upper_left":UL,"upper_right":UR,
"counts":{"lower":len(LL)+len(LR),"upper":len(UL)+len(UR)},
"real_areas_mm2":{"lower":12*ain,"upper":10*aout},
"status":"candidate zero-projected-frame-overlap layout found; exact pairwise/web and other keepout validation next"},indent=2))
