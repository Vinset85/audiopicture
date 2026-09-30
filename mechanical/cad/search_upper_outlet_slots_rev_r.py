# Upper outlet distributed placement search Rev.R
# Geometric feasibility search; final candidates are rechecked as CadQuery solids.
import cadquery as cq
import itertools, json, math

SLOT_W=3.0; SLOT_L=45.0; WEB=3.0; EDGE=4.0; KO_MARGIN=2.0
Z0,Z1=37.8,40.0

def rect_gap(a,b):
    ax0,ax1,ay0,ay1=a; bx0,bx1,by0,by1=b
    dx=max(bx0-ax1,ax0-bx1,0.0)
    dy=max(by0-ay1,ay0-by1,0.0)
    # Solid web requirement: separated along at least one Cartesian direction by WEB.
    return max(dx,dy)

# XY hard exclusions. Use documented coarse envelopes.
excl=[
 ("cleatL",(25.5,79.5,352,390)),
 ("cleatR",(240.5,294.5,352,390)),
 ("M1D",(65,75,390.4,398)),
 ("M2D",(245,255,390.4,398)),
 ("ESP32",(64,119.5,318.5,366.5)),
 ("MAIN_C",(85,235,315,370)),
]
def overlap2d(a,b):
    return min(a[1],b[1])>max(a[0],b[0]) and min(a[3],b[3])>max(a[2],b[2])

def legal(r,side):
    x0,x1,y0,y1=r
    if x0<EDGE or x1>320-EDGE or y0<315 or y1>400-EDGE: return False
    # side ownership prevents center-bank ambiguity
    if side=="L" and x1>160: return False
    if side=="R" and x0<160: return False
    def expand(e,m):
        return (e[0]-m,e[1]+m,e[2]-m,e[3]+m)
    return not any(overlap2d(r,expand(e,KO_MARGIN)) for _,e in excl)

def candidates(side):
    out=[]
    # 1 mm search grid, both orientations
    for orient in ("H","V"):
      for x in range(4,317):
       for y in range(315,397):
        r=(x,x+(SLOT_L if orient=="H" else SLOT_W),
           y,y+(SLOT_W if orient=="H" else SLOT_L))
        if legal(r,side):
            out.append((orient,r))
    # Prefer upper/perimeter placement, then smaller distance to side edge.
    if side=="L":
        out.sort(key=lambda q:(-q[1][3],q[1][0]))
    else:
        out.sort(key=lambda q:(-q[1][3],320-q[1][1]))
    return out

def select5(side):
    cs=candidates(side)
    # greedy seeds with backtracking over first useful candidates
    # de-duplicate nearby placements by 3 mm center grid to keep search compact
    reduced=[]
    seen=set()
    for c in cs:
        r=c[1]; key=(c[0],round((r[0]+r[1])/2/3),round((r[2]+r[3])/2/3))
        if key not in seen:
            seen.add(key); reduced.append(c)
        if len(reduced)>=350: break
    best=None
    def rec(start,chosen):
        nonlocal best
        if best is not None:return
        if len(chosen)==5:
            best=chosen[:]; return
        for i in range(start,len(reduced)):
            c=reduced[i]
            if all(rect_gap(c[1],d[1])>=WEB for d in chosen):
                rec(i+1,chosen+[c])
                if best is not None:return
    rec(0,[])
    return best,len(cs),len(reduced)

L,nL,rL=select5("L"); R,nR,rR=select5("R")
if L is None or R is None: raise RuntimeError("No legal 5-slot bank found")

slots=[]
for side,arr in (("L",L),("R",R)):
 for i,(ori,r) in enumerate(arr,1):
    slots.append((f"U{side}{i}",ori,r))

def box(r,z0,z1):
    x0,x1,y0,y1=r
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

# 3D boolean recheck
obs=[(n,box(r,0,40)) for n,r in excl]
rows=[]
for n,ori,r in slots:
    s=box(r,Z0,Z1)
    iv={}
    for on,o in obs:
        q=s.intersect(o)
        iv[on]=sum(v.Volume() for v in q.solids().vals()) if q.solids().size() else 0
    rows.append({"slot":n,"orientation":ori,"rect":r,"intersections_mm3":iv})

# exact pairwise web
minweb=min(rect_gap(a[2],b[2]) for a,b in itertools.combinations(slots,2))
assert len(slots)==10
assert abs(len(slots)*SLOT_W*SLOT_L-1350.0)<1e-9
assert minweb>=WEB
assert all(all(abs(v)<1e-9 for v in row["intersections_mm3"].values()) for row in rows)
print(json.dumps({
 "candidate_counts":{"left":nL,"right":nR,"left_reduced":rL,"right_reduced":rR},
 "slot_count":len(slots),
 "hard_keepout_margin_mm":KO_MARGIN,
 "gross_area_mm2":len(slots)*SLOT_W*SLOT_L,
 "effective_seed_mm2":len(slots)*SLOT_W*SLOT_L*0.80,
 "minimum_pairwise_web_mm":minweb,
 "slots":rows
},indent=2))
