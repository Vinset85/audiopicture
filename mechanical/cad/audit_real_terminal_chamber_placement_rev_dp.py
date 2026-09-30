# AudioPicture V2.2 real four-bank terminal chamber placement audit Rev.DP
# Uses authoritative Rev.BK vent coordinates and Rev.C coarse PC-CF frame kernel.
# Geometry/placement audit only; NOT CFD/acoustic simulation.
import cadquery as cq,json
X=320.; ZSHELL=37.8
# Rev.BK banks
lowerL=[(17,20,14,54),(24,27,14,54),(17,20,62,102),(24,27,62,102),(17,20,110,150),(24,27,110,150)]
upperL=[(17,62,315,318),(17,62,322,325),(17,62,329,332),(17,62,336,339),(17,62,343,346)]
def mir2(r):a,b,c,d=r;return(X-b,X-a,c,d)
# Rev.C frame exact coarse kernel
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
frame=box(2,318,2,398,27,35).cut(box(12,308,12,388,26,36))
for x0,x1 in ((25.5,79.5),(240.5,294.5)):frame=frame.union(box(x0,x1,352,390,27,35))
for _,x0,x1,y0,y1 in [
 ("L1",37,99,50,110),("L2",83,145,166,226),("R1",175,237,238,298),("R2",223,285,88,148),
 ("MAIN_C",85,235,315,370),("VOICE",119,201,20,102),("SERVICE",100,220,20,48),("ENV",252,294,35,59)]:
 frame=frame.cut(box(x0,x1,y0,y1,26,36))
frame=frame.clean()
# Rev.DO dimensions. Placement model approximates the total chamber/duct occupied envelope conservatively.
P=dict(L=36.,W=48.,chL=24.,chW=36.)
# Candidate XY envelopes anchored around actual vent-bank bounding boxes; orientations move inward from side edge.
banks={"LL":lowerL,"LR":[mir2(r) for r in lowerL],"UL":upperL,"UR":[mir2(r) for r in upperL]}
def env(bank):
 xs=[v for r in bank for v in r[:2]];ys=[v for r in bank for v in r[2:]]
 return min(xs),max(xs),min(ys),max(ys)
rows=[]
for name,b in banks.items():
 vx0,vx1,vy0,vy1=env(b)
 left=name.endswith("L")
 # inward duct starts just outboard of vent bank and extends L in X; full bank Y envelope retained for conservative collision screen
 if left: x0=15.;x1=15.+P["L"]
 else: x1=305.;x0=x1-P["L"]
 y0=vy0;y1=vy1
 for zlow in (34.0,35.1,35.3,35.5,35.8,36.0):
  occ=box(x0,x1,y0,y1,zlow,ZSHELL)
  inter=occ.intersect(frame)
  iv=sum(s.Volume() for s in inter.solids().vals()) if inter.solids().size() else 0.
  free_h=36.8-zlow
  throat=max(0.,16.-1.)*max(0.,free_h)
  rows.append(dict(bank=name,xy=[x0,x1,y0,y1],zlow=zlow,frame_overlap_mm3=round(iv,6),
                   throat_proxy_mm2=round(throat,3),pass_no_frame=iv<1e-8 and throat>0))
print(json.dumps({"frame_valid":frame.val().isValid(),"frame_solids":frame.solids().size(),
"bank_envelopes":{k:env(v) for k,v in banks.items()},"placements":rows,
"passing":[r for r in rows if r["pass_no_frame"]],
"note":"Conservative occupied-envelope screen. A pass permits detailed chamber solid construction; a fail does not prove every sculpted topology impossible."},indent=2))
