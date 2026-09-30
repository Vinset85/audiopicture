# AudioPicture V2.2 projected vent blockage audit vs PC-CF Rev.BC
import json, math
R=1.5
upper=[("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),("UL5","V",13,16,341,386),("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),("UR5","V",306,309,341,386)]
lower=[]
for side,xs in (("L",[(4,7),(11,14)]),("R",[(313,316),(306,309)])):
 i=1
 for y0,y1 in ((4,44),(52,92),(104,144)):
  for x0,x1 in xs:lower.append((f"I{side}{i}","V",x0,x1,y0,y1));i+=1
# raster integration of capsule area and overlap with Rev.C projected solid.
def in_capsule(x,y,row):
 _,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2; xa=x0+R; xb=x1-R
  if xa<=x<=xb and abs(y-cy)<=R:return True
  return (x-xa)**2+(y-cy)**2<=R*R or (x-xb)**2+(y-cy)**2<=R*R
 cx=(x0+x1)/2; ya=y0+R; yb=y1-R
 if ya<=y<=yb and abs(x-cx)<=R:return True
 return (x-cx)**2+(y-ya)**2<=R*R or (x-cx)**2+(y-yb)**2<=R*R
def frame_proj(x,y):
 # Rev.C ring
 solid=(2<=x<=318 and 2<=y<=398 and not(12<=x<=308 and 12<=y<=388))
 # cleat islands
 solid=solid or (25.5<=x<=79.5 and 352<=y<=390) or (240.5<=x<=294.5 and 352<=y<=390)
 # subtract Rev.C KOs
 kos=[(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]
 if any(a<=x<=b and c<=y<=d for a,b,c,d in kos):solid=False
 return solid
def audit(row,step=.05):
 _,_,x0,x1,y0,y1=row; total=blocked=0
 nx=math.ceil((x1-x0)/step);ny=math.ceil((y1-y0)/step)
 for i in range(nx):
  x=x0+(i+.5)*(x1-x0)/nx
  for j in range(ny):
   y=y0+(j+.5)*(y1-y0)/ny
   if in_capsule(x,y,row):
    da=(x1-x0)/nx*(y1-y0)/ny;total+=da
    if frame_proj(x,y):blocked+=da
 return total,blocked
res={};tot=blk=0
for row in upper+lower:
 a,b=audit(row);res[row[0]]={"area_mm2":a,"projected_frame_overlap_mm2":b,"overlap_pct":100*b/a}
 tot+=a;blk+=b
print(json.dumps({"per_slot":res,"total_vent_area_mm2":tot,"total_projected_overlap_mm2":blk,"overall_overlap_pct":100*blk/tot,
"interpretation":"Projected overlap is a shadowing warning, not a CFD pressure-loss result. Z gap from frame rear to shell remains about 2.8 mm away from local shell features.",
"gate":"baffle design must account for this blockage; do not treat nominal slot area as unobstructed throat area"},indent=2))
