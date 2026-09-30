# AudioPicture V2.2 shell-to-PC-CF retention node placement Rev.AM
# Node centers only: fastener diameter/MPN intentionally open.
import json, math
# PC-CF coarse outer ring projected legal strips
# x 2..318/y2..398 with inner opening x12..308/y12..388, plus cleat islands.
# Candidate node must lie on coarse ring and outside exclusions with NODE_R seed clearance envelope.
NODE_R=5.0
seeds=[("T1",80,382),("T2",160,382),("T3",240,382),("S1",12,200),("S2",308,200),("B1",80,18),("B2",160,18),("B3",240,18)]
# avoid wall-cleat islands, vent bank envelopes, service, anti-lift, ESP coarse RF mask
ex=[
 ("CLEAT_L",(25.5,79.5,352,390)),("CLEAT_R",(240.5,294.5,352,390)),
 ("UPPER_VENT_L",(0,129,339,400)),("UPPER_VENT_R",(191,320,339,400)),
 ("LOWER_VENT_L",(0,16,2,146)),("LOWER_VENT_R",(304,320,2,146)),
 ("SERVICE",(100,220,20,48)),("ANTILIFT",(145,175,12,24)),
 ("ESP32_RF_COARSE",(64,119.5,318.5,366.5))
]
def inside_expanded(x,y,r):
 for n,(a,b,c,d) in ex:
  if a-NODE_R<=x<=b+NODE_R and c-NODE_R<=y<=d+NODE_R:return n
 return None
def on_ring(x,y):
 return 2+NODE_R<=x<=318-NODE_R and 2+NODE_R<=y<=398-NODE_R and not(12+NODE_R<x<308-NODE_R and 12+NODE_R<y<388-NODE_R)
# deterministic nearest search around each seed; preserve semantic side/top/bottom.
def candidates(name,sx,sy):
 out=[]
 for x in range(7,314):
  for y in range(7,394):
   if not on_ring(x,y) or inside_expanded(x,y,NODE_R):continue
   if name.startswith("T") and y<370:continue
   if name.startswith("B") and y>18:continue
   if name=="S1" and x>18:continue
   if name=="S2" and x<302:continue
   d=(x-sx)**2+(y-sy)**2
   out.append((d,x,y))
 return sorted(out)
chosen=[];results=[]
for n,sx,sy in seeds:
 cs=candidates(n,sx,sy);pick=None
 for d,x,y in cs:
  if all(math.hypot(x-qx,y-qy)>=30 for _,qx,qy in chosen):
   pick=(n,x,y);break
 if pick:
  chosen.append(pick);results.append({"seed":n,"seed_xy":[sx,sy],"selected_xy":[pick[1],pick[2]],"move_mm":math.hypot(pick[1]-sx,pick[2]-sy)})
# central bottom is expected to fail/move because anti-lift/service architecture.
print(json.dumps({"node_radius_screen_mm":NODE_R,"selected_count":len(results),"nodes":results,
"exclusions":ex,"limitations":["5mm node radius is packaging screen only","fastener MPN/hole/boss not frozen","coarse PC-CF ring only","exact RF/radar and final frame B-rep remain authoritative"]},indent=2))
