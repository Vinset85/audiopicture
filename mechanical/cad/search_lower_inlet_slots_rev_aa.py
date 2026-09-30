# AudioPicture V2.2 lower inlet placement solver Rev.AA
# Searches 6+6 real R1.5 capsule slots, 3 x 40 mm overall, with preferred 4 mm nominal web.
import cadquery as cq
import json, math

W=3.0; L=40.0; R=1.5; WEB=4.0; EDGE=4.0; KO=2.0
Z0,Z1=37.8,40.0

# Documented lower hard/coarse envelopes.
# Support pads: 18x12 seed around frozen centers; anti-lift uses documented Y12..24 region.
excl=[
 ("L1",(37,99,50,110)),
 ("R2",(223,285,88,148)),
 ("VOICE",(119,201,20,102)),
 ("SERVICE",(100,220,20,48)),
 ("ENV",(252,294,35,59)),
 ("PAD_L",(36,54,22,34)),
 ("PAD_R",(266,284,22,34)),
 ("ANTILIFT",(145,175,12,24)),
]

def overlap(a,b):
    return min(a[1],b[1])>max(a[0],b[0]) and min(a[3],b[3])>max(a[2],b[2])
def expand(r,m): return (r[0]-m,r[1]+m,r[2]-m,r[3]+m)
def gap(a,b):
    dx=max(b[0]-a[1],a[0]-b[1],0.0)
    dy=max(b[2]-a[3],a[2]-b[3],0.0)
    return max(dx,dy)
def legal(r,side):
    x0,x1,y0,y1=r
    if x0<EDGE or x1>320-EDGE or y0<EDGE or y1>155: return False
    if side=="L" and x1>100: return False
    if side=="R" and x0<220: return False
    return not any(overlap(r,expand(e,KO)) for _,e in excl)

def candidates(side):
    out=[]
    for ori in ("H","V"):
      for x in range(4,317):
       for y in range(4,156):
        r=(x,x+(L if ori=="H" else W),y,y+(W if ori=="H" else L))
        if legal(r,side): out.append((ori,r))
    # Prefer low/perimeter locations and then side edge.
    if side=="L": out.sort(key=lambda q:(q[1][2],q[1][0]))
    else: out.sort(key=lambda q:(q[1][2],320-q[1][1]))
    return out

def select6(side):
    cs=candidates(side); reduced=[]; seen=set()
    for c in cs:
        r=c[1]; key=(c[0],round((r[0]+r[1])/2/3),round((r[2]+r[3])/2/3))
        if key not in seen:
            seen.add(key); reduced.append(c)
        if len(reduced)>=500: break
    best=None
    def rec(start,chosen):
        nonlocal best
        if best is not None: return
        if len(chosen)==6: best=chosen[:]; return
        for i in range(start,len(reduced)):
            c=reduced[i]
            if all(gap(c[1],d[1])>=WEB for d in chosen):
                rec(i+1,chosen+[c])
                if best is not None:return
    rec(0,[])
    return best,len(cs),len(reduced)

Lset,nL,rL=select6("L"); Rset,nR,rR=select6("R")
if Lset is None or Rset is None: raise RuntimeError("No 6-slot bank found in reduced search")

slots=[]
for side,arr in (("L",Lset),("R",Rset)):
    for i,(ori,r) in enumerate(arr,1): slots.append((f"I{side}{i}",ori,r))

def capsule(ori,r,z0=Z0,z1=Z1):
    x0,x1,y0,y1=r
    if ori=="H":
        cy=(y0+y1)/2; xa=x0+R; xb=x1-R
        return (cq.Workplane("XY",origin=(0,0,z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R)
          .threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R)
          .threePointArc((x0,cy),(xa,cy-R)).close().extrude((z1-z0)+.4))
    cx=(x0+x1)/2; ya=y0+R; yb=y1-R
    return (cq.Workplane("XY",origin=(0,0,z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb)
      .threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya)
      .threePointArc((cx,y0),(cx-R,ya)).close().extrude((z1-z0)+.4))

def obs(r):
    x0,x1,y0,y1=r
    return cq.Workplane("XY").box(x1-x0,y1-y0,40,centered=(False,False,False)).translate((x0,y0,0))

rows=[]
for n,ori,r in slots:
    c=capsule(ori,r); iv={}
    for on,e in excl:
        q=c.intersect(obs(expand(e,KO)))
        iv[on]=sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0
    rows.append({"slot":n,"orientation":ori,"rect":r,"expanded_keepout_intersections_mm3":iv})

minweb=min(gap(a[2],b[2]) for a,b in __import__("itertools").combinations(slots,2))
area_each=(L-W)*W+math.pi*R*R
gross=12*area_each
eff=.75*gross
assert len(slots)==12 and minweb>=WEB
assert all(all(abs(v)<1e-8 for v in x["expanded_keepout_intersections_mm3"].values()) for x in rows)
assert eff>=900
print(json.dumps({
 "candidate_counts":{"left":nL,"right":nR,"left_reduced":rL,"right_reduced":rR},
 "slot_count":len(slots),"minimum_pairwise_web_mm":minweb,
 "capsule_area_each_mm2":area_each,"gross_actual_mm2":gross,
 "effective_seed_0p75_mm2":eff,"preferred_effective_target_mm2":900,
 "slots":rows,
 "limitations":["coarse documented keepouts","support pads are seed envelopes","anti-lift X span is conservative solver envelope","cable/harness exact swept solids not documented"]
},indent=2))
