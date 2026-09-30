# AudioPicture V2.2 lateral throat screen Rev.BE
# Geometric reduced-order screen, NOT CFD.
import json, math
R=1.5; GAP_Z=2.8
upper=[("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),("UL5","V",13,16,341,386),("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),("UR5","V",306,309,341,386)]
lower=[]
for side,xs in (("L",[(4,7),(11,14)]),("R",[(313,316),(306,309)])):
 i=1
 for y0,y1 in ((4,44),(52,92),(104,144)):
  for x0,x1 in xs:lower.append((f"I{side}{i}","V",x0,x1,y0,y1));i+=1
def in_capsule(x,y,row):
 _,o,x0,x1,y0,y1=row
 if o=="H":
  cy=(y0+y1)/2; a=x0+R;b=x1-R
  return (a<=x<=b and abs(y-cy)<=R) or (x-a)**2+(y-cy)**2<=R*R or (x-b)**2+(y-cy)**2<=R*R
 cx=(x0+x1)/2;a=y0+R;b=y1-R
 return (a<=y<=b and abs(x-cx)<=R) or (x-cx)**2+(y-a)**2<=R*R or (x-cx)**2+(y-b)**2<=R*R
def frame(x,y):
 s=(2<=x<=318 and 2<=y<=398 and not(12<=x<=308 and 12<=y<=388))
 s=s or (25.5<=x<=79.5 and 352<=y<=390) or (240.5<=x<=294.5 and 352<=y<=390)
 kos=[(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]
 if any(a<=x<=b and c<=y<=d for a,b,c,d in kos):s=False
 return s
# For each slot, rasterize. For shadowed cells find nearest non-frame point in 4 cardinal directions.
# throat proxy = open escape-front length * Z gap. Escape-front length is unique exposed raster edge
# between shadowed slot footprint and non-frame neighboring region; this avoids claiming pressure performance.
STEP=.25
def audit(row):
 n,o,x0,x1,y0,y1=row
 xs=[x0+(i+.5)*STEP for i in range(max(1,math.ceil((x1-x0)/STEP)))]
 ys=[y0+(j+.5)*STEP for j in range(max(1,math.ceil((y1-y0)/STEP)))]
 cells={(i,j) for i,x in enumerate(xs) for j,y in enumerate(ys) if in_capsule(x,y,row)}
 sh={(i,j) for i,j in cells if frame(xs[i],ys[j])}
 area=len(cells)*STEP*STEP; shadow=len(sh)*STEP*STEP
 # estimate minimum lateral travel to free projection from shadowed cell, scanning physical XY.
 dists=[]
 for i,j in sh:
  x,y=xs[i],ys[j]; best=999.
  for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
   for k in range(1,161):
    xx=x+dx*k*STEP;yy=y+dy*k*STEP
    if not frame(xx,yy):best=min(best,k*STEP);break
  dists.append(best)
 # conservative escape perimeter of shadowed footprint adjacent to free projected region
 edge=0.
 for i,j in sh:
  x,y=xs[i],ys[j]
  for dx,dy in ((STEP,0),(-STEP,0),(0,STEP),(0,-STEP)):
   if not frame(x+dx,y+dy):edge+=STEP
 throat=edge*GAP_Z
 return {"slot_area_mm2":area,"shadow_area_mm2":shadow,"shadow_pct":100*shadow/area if area else 0,
 "max_lateral_escape_mm":max(dists) if dists else 0,"escape_edge_mm":edge,
 "lateral_throat_proxy_mm2":throat,"throat_to_slot_area_ratio":throat/area if area else 0}
out={r[0]:audit(r) for r in upper+lower}
print(json.dumps({"gap_z_mm":GAP_Z,"raster_step_mm":STEP,"slots":out,
"warning":"lateral_throat_proxy is geometric only; it is not effective flow area and does not include turning/minor losses.",
"decision_rule_seed":"flag slots with projected shadowing and throat proxy below their own opening area for relocation study before labyrinth freeze"},indent=2))
