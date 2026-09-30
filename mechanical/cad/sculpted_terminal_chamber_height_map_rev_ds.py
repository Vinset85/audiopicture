# AudioPicture V2.2 sculpted terminal chamber height map Rev.DS
# Analytical XY frame-occupancy map for detailed CadQuery build.
import json
# Rev.C frame material rectangles after inner-ring subtraction can be reasoned as edge bands plus cleat islands,
# with keepouts subtracting material. We encode conservative material tests for candidate sample cells.
frame_rects=[(2,318,2,12),(2,318,388,398),(2,12,12,388),(308,318,12,388),(25.5,79.5,352,390),(240.5,294.5,352,390)]
keepouts=[(37,99,50,110),(83,145,166,226),(175,237,238,298),(223,285,88,148),(85,235,315,370),(119,201,20,102),(100,220,20,48),(252,294,35,59)]
def inside(x,y,r):return r[0]<=x<=r[1] and r[2]<=y<=r[3]
def frame_material(x,y):
 return any(inside(x,y,r) for r in frame_rects) and not any(inside(x,y,k) for k in keepouts)
# sample actual duct envelopes at 1 mm XY grid and classify whether low-Z air may extend below 35.1
banks={"LL":(15,51,14,150),"LR":(269,305,14,150),"UL":(15,51,315,346),"UR":(269,305,315,346)}
out={}
for n,(x0,x1,y0,y1) in banks.items():
 total=blocked=0
 for x in range(int(x0),int(x1)+1):
  for y in range(int(y0),int(y1)+1):
   total+=1
   if frame_material(x,y):blocked+=1
 out[n]={"samples":total,"frame_material_samples":blocked,"open_samples":total-blocked,
         "open_fraction":round((total-blocked)/total,4)}
print(json.dumps({"banks":out,
"height_rule":"solid features over frame material: zlow>=35.1; deeper air/chamber volume may be considered only over verified open XY cells",
"note":"This is an analytical occupancy classifier for the next solid build, not a manufactured geometry or CFD result."},indent=2))
