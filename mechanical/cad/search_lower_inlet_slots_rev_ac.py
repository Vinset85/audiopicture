# AudioPicture V2.2 lower inlet deterministic band solver Rev.AC
# Six slots per side, distributed by construction across three lower Y bands.
import math, json, itertools
W=3.; L=40.; R=1.5; WEB=4.; EDGE=4.; KO=2.
excl=[("L1",(37,99,50,110)),("R2",(223,285,88,148)),("VOICE",(119,201,20,102)),
("SERVICE",(100,220,20,48)),("ENV",(252,294,35,59)),("PAD_L",(36,54,22,34)),
("PAD_R",(266,284,22,34)),("ANTILIFT",(145,175,12,24))]
def overlap(a,b):return min(a[1],b[1])>max(a[0],b[0]) and min(a[3],b[3])>max(a[2],b[2])
def expand(r,m):return(r[0]-m,r[1]+m,r[2]-m,r[3]+m)
def sep(a,b):return max(max(b[0]-a[1],a[0]-b[1],0.),max(b[2]-a[3],a[2]-b[3],0.))
def legal(r,side):
 x0,x1,y0,y1=r
 if x0<EDGE or x1>316 or y0<EDGE or y1>155:return False
 if side=="L" and x1>100:return False
 if side=="R" and x0<220:return False
 return not any(overlap(r,expand(e,KO)) for _,e in excl)
# Three bands force vertical distribution; choose two legal features per band.
bands=[(4,48),(52,100),(104,155)]
def candidates(side,band):
 out=[]
 for ori in ("H","V"):
  for x in range(4,317):
   for y in range(band[0],band[1]+1):
    r=(x,x+(L if ori=="H" else W),y,y+(W if ori=="H" else L))
    if r[3]<=band[1] and legal(r,side):
     cx=(r[0]+r[1])/2
     lateral=cx if side=="L" else 320-cx
     out.append((lateral,y,ori,r))
 return sorted(out)
def solve(side):
 chosen=[]
 for band in bands:
  cs=candidates(side,band); pair=None
  for i,a in enumerate(cs):
   for b in cs[i+1:]:
    if sep(a[3],b[3])>=WEB and all(sep(a[3],q[2])>=WEB and sep(b[3],q[2])>=WEB for q in chosen):
     pair=(a,b);break
   if pair:break
  if not pair:raise RuntimeError("No legal pair in band")
  for q in pair:chosen.append((q[2],q[3]))
 return chosen
Ls=solve("L");Rs=solve("R")
slots=[]
for side,arr in (("L",Ls),("R",Rs)):
 for i,(o,r) in enumerate(arr,1):slots.append((f"I{side}{i}",o,r))
minweb=min(sep(a[2],b[2]) for a,b in itertools.combinations(slots,2))
area=(L-W)*W+math.pi*R*R;gross=12*area;eff=.75*gross
assert len(slots)==12 and minweb>=WEB and eff>=900
assert all(legal(r,n[1]) for n,o,r in slots)
print(json.dumps({"slot_count":12,"minimum_pairwise_web_mm":minweb,
"capsule_area_each_mm2":area,"gross_actual_mm2":gross,"effective_seed_0p75_mm2":eff,
"bands_y_mm":bands,"slots":slots,
"limitations":["coarse documented keepouts","support pads seed envelopes","anti-lift X span conservative","exact harness swept solids unavailable"]},indent=2))
