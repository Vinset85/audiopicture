# AudioPicture V2.2 lower inlet distributed placement solver Rev.AB
# Optimize 6+6 real R1.5 capsule slots for distributed lower-side intake.
import cadquery as cq, math, json, itertools

W=3.; L=40.; R=1.5; WEB=4.; EDGE=4.; KO=2.
excl=[
 ("L1",(37,99,50,110)),("R2",(223,285,88,148)),("VOICE",(119,201,20,102)),
 ("SERVICE",(100,220,20,48)),("ENV",(252,294,35,59)),
 ("PAD_L",(36,54,22,34)),("PAD_R",(266,284,22,34)),("ANTILIFT",(145,175,12,24))
]
def overlap(a,b): return min(a[1],b[1])>max(a[0],b[0]) and min(a[3],b[3])>max(a[2],b[2])
def expand(r,m): return (r[0]-m,r[1]+m,r[2]-m,r[3]+m)
def sep(a,b):
    dx=max(b[0]-a[1],a[0]-b[1],0.); dy=max(b[2]-a[3],a[2]-b[3],0.)
    return max(dx,dy)
def legal(r,side):
    x0,x1,y0,y1=r
    if x0<EDGE or x1>320-EDGE or y0<EDGE or y1>155:return False
    # keep banks lateral and out of central service/voice corridor
    if side=="L" and x1>100:return False
    if side=="R" and x0<220:return False
    return not any(overlap(r,expand(e,KO)) for _,e in excl)

# Deliberately use a 7 mm grid: 3 mm slot + 4 mm nominal web.
# Enumerate H/V and optimize for Y spread, lateral placement, and orientation diversity.
def candidates(side):
    cs=[]
    for ori in ("H","V"):
      for x in range(4,317,7):
       for y in range(4,156,7):
        r=(x,x+(L if ori=="H" else W),y,y+(W if ori=="H" else L))
        if legal(r,side):
          cx=(r[0]+r[1])/2; cy=(r[2]+r[3])/2
          lateral=(cx if side=="L" else 320-cx)
          cs.append((ori,r,cx,cy,lateral))
    return cs

def score(sel):
    ys=[c[3] for c in sel]
    yspread=max(ys)-min(ys)
    # reward vertical distribution; penalize drifting toward product center
    lateral=sum(c[4] for c in sel)/len(sel)
    # reward both orientations but do not require a quota
    diversity=len(set(c[0] for c in sel))
    return 10*yspread - .5*lateral + 5*diversity

def solve(side):
    cs=candidates(side)
    # retain strong lateral candidates across Y bins, not just lowest-Y candidates
    bins={}
    for c in cs:
      b=int(c[3]//14)
      bins.setdefault(b,[]).append(c)
    pool=[]
    for b,arr in bins.items():
      arr.sort(key=lambda c:(c[4],c[3]))
      pool.extend(arr[:18])
    best=None; bestscore=-1e9
    def rec(start,chosen):
      nonlocal best,bestscore
      if len(chosen)==6:
        s=score(chosen)
        if s>bestscore:bestscore=s;best=chosen[:]
        return
      if len(pool)-start < 6-len(chosen):return
      for i in range(start,len(pool)):
        c=pool[i]
        if all(sep(c[1],d[1])>=WEB for d in chosen):
          rec(i+1,chosen+[c])
    rec(0,[])
    return best,len(cs),len(pool),bestscore

Ls,nL,pL,sL=solve("L"); Rs,nR,pR,sR=solve("R")
if not Ls or not Rs: raise RuntimeError("No distributed solution")

slots=[]
for side,arr in (("L",Ls),("R",Rs)):
  arr=sorted(arr,key=lambda c:(c[3],c[2]))
  for i,c in enumerate(arr,1): slots.append((f"I{side}{i}",c[0],c[1]))

# exact capsule geometry for collision audit
def capsule(ori,r):
 x0,x1,y0,y1=r
 if ori=="H":
  cy=(y0+y1)/2; xa=x0+R; xb=x1-R
  return (cq.Workplane("XY",origin=(0,0,37.6)).moveTo(xa,cy-R).lineTo(xb,cy-R)
    .threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R)
    .threePointArc((x0,cy),(xa,cy-R)).close().extrude(2.6))
 cx=(x0+x1)/2; ya=y0+R; yb=y1-R
 return (cq.Workplane("XY",origin=(0,0,37.6)).moveTo(cx-R,ya).lineTo(cx-R,yb)
   .threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya)
   .threePointArc((cx,y0),(cx-R,ya)).close().extrude(2.6))
def obs(r):
 x0,x1,y0,y1=r
 return cq.Workplane("XY").box(x1-x0,y1-y0,40,centered=(False,False,False)).translate((x0,y0,0))

rows=[]
for n,o,r in slots:
 c=capsule(o,r); ints={}
 for en,e in excl:
  q=c.intersect(obs(expand(e,KO))); ints[en]=sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0.
 rows.append({"slot":n,"orientation":o,"rect":r,"center":[(r[0]+r[1])/2,(r[2]+r[3])/2],"intersections_mm3":ints})
minweb=min(sep(a[2],b[2]) for a,b in itertools.combinations(slots,2))
area=(L-W)*W+math.pi*R*R; gross=12*area; eff=.75*gross
yspans={}
for side in ("L","R"):
 yy=[x["center"][1] for x in rows if x["slot"].startswith("I"+side)]
 yspans[side]=max(yy)-min(yy)
assert len(slots)==12 and minweb>=WEB and eff>=900
assert all(all(abs(v)<1e-8 for v in x["intersections_mm3"].values()) for x in rows)
print(json.dumps({"candidate_counts":{"L":nL,"R":nR,"poolL":pL,"poolR":pR},
 "scores":{"L":sL,"R":sR},"slot_count":12,"minimum_pairwise_web_mm":minweb,
 "center_y_span_mm":yspans,"capsule_area_each_mm2":area,"gross_actual_mm2":gross,
 "effective_seed_0p75_mm2":eff,"slots":rows,
 "limitations":["coarse documented keepouts","support pads seed envelopes","anti-lift X span conservative","exact harness swept solids unavailable"]},indent=2))
