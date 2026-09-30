# AudioPicture V2.2 complete ventilated rear-shell nominal kernel Rev.AE
import cadquery as cq, json, math, itertools
X=320.;Y=400.;T=2.2;Z0=37.8;Z1=40.;R=1.5
upper=[("UL1","H",4,49,393,396),("UL2","H",77,122,393,396),("UL3","H",82,127,386,389),("UL4","V",4,7,341,386),("UL5","V",13,16,341,386),("UR1","H",271,316,393,396),("UR2","H",198,243,393,396),("UR3","H",193,238,386,389),("UR4","V",313,316,341,386),("UR5","V",306,309,341,386)]
lower=[]
for side,xs in (("L",[(4,7),(11,14)]),("R",[(313,316),(306,309)])):
 i=1
 for y0,y1 in ((4,44),(52,92),(104,144)):
  for x0,x1 in xs:
   lower.append((f"I{side}{i}","V",x0,x1,y0,y1));i+=1
def capsule(row):
 n,o,x0,x1,y0,y1=row; w=(y1-y0 if o=="H" else x1-x0)
 if abs(w-3)>1e-9:raise ValueError(n)
 if o=="H":
  cy=(y0+y1)/2;xa=x0+R;xb=x1-R
  return(cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(xa,cy-R).lineTo(xb,cy-R).threePointArc((x1,cy),(xb,cy+R)).lineTo(xa,cy+R).threePointArc((x0,cy),(xa,cy-R)).close().extrude(T+.4))
 cx=(x0+x1)/2;ya=y0+R;yb=y1-R
 return(cq.Workplane("XY",origin=(0,0,Z0-.2)).moveTo(cx-R,ya).lineTo(cx-R,yb).threePointArc((cx,y1),(cx+R,yb)).lineTo(cx+R,ya).threePointArc((cx,y0),(cx-R,ya)).close().extrude(T+.4))
shell=cq.Workplane("XY").box(X,Y,T,centered=(False,False,False)).translate((0,0,Z0))
cuts={}
for row in upper+lower:
 c=capsule(row);cuts[row[0]]=c;shell=shell.cut(c)
shell=shell.clean()
def rect(row):return(row[2],row[3],row[4],row[5])
def sep(a,b):
 return max(max(b[0]-a[1],a[0]-b[1],0.),max(b[2]-a[3],a[2]-b[3],0.))
min_upper=min(sep(rect(a),rect(b)) for a,b in itertools.combinations(upper,2))
min_lower=min(sep(rect(a),rect(b)) for a,b in itertools.combinations(lower,2))
upper_ex=[("cleatL",(25.5,79.5,352,390)),("cleatR",(240.5,294.5,352,390)),("M1D",(65,75,390.4,398)),("M2D",(245,255,390.4,398)),("ESP32",(64,119.5,318.5,366.5)),("MAIN_C",(85,235,315,370))]
lower_ex=[("L1",(35,101,48,112)),("R2",(221,287,86,150)),("VOICE",(117,203,18,104)),("SERVICE",(98,222,18,50)),("ENV",(250,296,33,61)),("PAD_L",(34,56,20,36)),("PAD_R",(264,286,20,36)),("ANTILIFT",(143,177,10,26))]
def obs(r):x0,x1,y0,y1=r;return cq.Workplane("XY").box(x1-x0,y1-y0,40,centered=(False,False,False)).translate((x0,y0,0))
ints={}
for row in upper:
 ints[row[0]]={n:sum(v.Volume() for v in cuts[row[0]].intersect(obs(r)).solids().vals()) for n,r in upper_ex}
for row in lower:
 ints[row[0]]={n:sum(v.Volume() for v in cuts[row[0]].intersect(obs(r)).solids().vals()) for n,r in lower_ex}
Au=(45-3)*3+math.pi*R*R;Al=(40-3)*3+math.pi*R*R
Ag=10*Au;Ig=12*Al
vol_expected=X*Y*T-(Ag+Ig)*T
vol=shell.val().Volume();bb=shell.val().BoundingBox()
assert shell.val().isValid() and shell.solids().size()==1
assert len(cuts)==22 and min_upper>=4 and min_lower>=4
assert all(abs(v)<1e-8 for d in ints.values() for v in d.values())
assert .8*Ag>=1000 and .75*Ig>=900
assert abs(vol-vol_expected)<1e-4
cq.exporters.export(shell,"AP22_REAR_SHELL_VENTILATED_REV_AE.step");cq.exporters.export(shell,"AP22_REAR_SHELL_VENTILATED_REV_AE.stl")
print(json.dumps({"valid":True,"solid_count":1,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],"vent_count":22,"upper_count":10,"lower_count":12,"min_upper_web_mm":min_upper,"min_lower_web_mm":min_lower,"upper_real_gross_mm2":Ag,"upper_effective_seed_mm2":.8*Ag,"lower_real_gross_mm2":Ig,"lower_effective_seed_mm2":.75*Ig,"total_real_open_mm2":Ag+Ig,"kernel_volume_mm3":vol,"analytic_volume_mm3":vol_expected,"volume_error_mm3":vol-vol_expected,"all_documented_intersections_zero":True,"artifacts":["AP22_REAR_SHELL_VENTILATED_REV_AE.step","AP22_REAR_SHELL_VENTILATED_REV_AE.stl"],"limitations":["flat rear-panel kernel only","service recess not yet modeled as separate rear-form feature","baffles/perimeter returns/retention not yet added","CFD and physical ASA qualification open"]},indent=2))
