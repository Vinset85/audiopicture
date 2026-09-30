# AudioPicture V2.2 four-bank sculpted terminal chamber solid Rev.DT
# First real-product CadQuery construction using Rev.BK coordinates and Rev.C frame kernel.
# Mechanical geometry gate only; NOT CFD/acoustic simulation.
import cadquery as cq,json
X=320.; ZTOP=37.8; ROOF=36.8; T=1.0
# Finalist plan dimensions
L=36.; W=48.; CHL=24.; CHW=36.; EXIT=16.; OV=12.
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
# authoritative coarse frame
frame=box(2,318,2,398,27,35).cut(box(12,308,12,388,26,36))
for x0,x1 in ((25.5,79.5),(240.5,294.5)):frame=frame.union(box(x0,x1,352,390,27,35))
for _,x0,x1,y0,y1 in [("L1",37,99,50,110),("L2",83,145,166,226),("R1",175,237,238,298),("R2",223,285,88,148),("MAIN_C",85,235,315,370),("VOICE",119,201,20,102),("SERVICE",100,220,20,48),("ENV",252,294,35,59)]:
 frame=frame.cut(box(x0,x1,y0,y1,26,36))
frame=frame.clean()
# Build normalized wall set transformed to each bank.
# Lower uses zlow=34.0 where legal; upper uses 35.1 fallback then locally cuts any frame intersection as a conservative sculpt.
def left_geom(y0,zlow):
 x0=15.;x1=x0+L;y1=y0+W;zl=zlow
 solids=[]
 solids.append(box(x0,x1,y0,y1,ROOF,ZTOP)) # roof
 solids.append(box(x0,x0+T,y0,y1,zl,ROOF))
 solids.append(box(x0,x1,y0,y0+T,zl,ROOF))
 cx0=x1-CHL;cx1=x1;cy0=y1-CHW;cy1=y1
 solids.append(box(cx1-T,cx1,cy0,cy1,zl,ROOF))
 solids.append(box(cx0,cx1,cy0,cy0+T,zl,ROOF))
 ex0=cx0+T;ex1=min(cx1-T,ex0+EXIT)
 if ex0>cx0:solids.append(box(cx0,ex0,cy1-T,cy1,zl,ROOF))
 if ex1<cx1:solids.append(box(ex1,cx1,cy1-T,cy1,zl,ROOF))
 bx=min(cx1-T,cx0+T+EXIT+OV)
 solids.append(box(bx-T,bx,cy0+T,cy1-T,zl,ROOF))
 s=solids[0]
 for q in solids[1:]:s=s.union(q)
 return s.clean()
def mirror_x(s): return s.mirror("YZ",basePointVector=(160,0,0))
LL=left_geom(14.,34.0)
LR=mirror_x(LL)
UL=left_geom(315.,35.1)
UR=mirror_x(UL)
parts={"LL":LL,"LR":LR,"UL":UL,"UR":UR}
out={}
for n,s in parts.items():
 inter=s.intersect(frame)
 iv=sum(q.Volume() for q in inter.solids().vals()) if inter.solids().size() else 0.
 # sculpt only if needed: remove frame material expanded 0.1 mm in Z by using exact frame collision volume from solid.
 sculpt=s.cut(frame).clean()
 inter2=sculpt.intersect(frame)
 iv2=sum(q.Volume() for q in inter2.solids().vals()) if inter2.solids().size() else 0.
 out[n]={"raw_valid":s.val().isValid(),"raw_frame_overlap_mm3":round(iv,6),
         "sculpt_valid":sculpt.val().isValid(),"sculpt_solids":sculpt.solids().size(),
         "post_sculpt_frame_overlap_mm3":round(iv2,9),"volume_mm3":round(sculpt.val().Volume() if sculpt.solids().size()==1 else sum(q.Volume() for q in sculpt.solids().vals()),3)}
 cq.exporters.export(sculpt,f"AP22_TERMINAL_CHAMBER_{n}_REV_DT.step")
print(json.dumps({"banks":out,"zlow":{"lower":34.0,"upper":35.1},
"artifacts":[f"AP22_TERMINAL_CHAMBER_{n}_REV_DT.step" for n in parts],
"limitations":["fluid connectivity not yet audited","actual-product dense LOS not yet rerun","shell fusion not yet performed","thermal pressure loss open"]},indent=2))
