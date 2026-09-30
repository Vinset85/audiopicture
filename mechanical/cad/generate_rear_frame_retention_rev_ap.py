# AudioPicture V2.2 PC-CF rear frame + shell-retention top tabs Rev.AP
import cadquery as cq, json
Z0=27.;DEPTH=8.
def rect(x0,x1,y0,y1,z0=Z0,z1=Z0+DEPTH):
 return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
# Rev.C base
base=rect(2,318,2,398).cut(rect(12,308,12,388,Z0-1,Z0+DEPTH+1))
for x0,x1 in ((25.5,79.5),(240.5,294.5)):base=base.union(rect(x0,x1,352,390))
keep=[("L1",37,99,50,110),("L2",83,145,166,226),("R1",175,237,238,298),("R2",223,285,88,148),("MAIN_C",85,235,315,370),("VOICE",119,201,20,102),("SERVICE",100,220,20,48),("ENV",252,294,35,59)]
for _,a,b,c,d in keep:base=base.cut(rect(a,b,c,d,Z0-1,Z0+DEPTH+1))
base=base.clean();v0=base.val().Volume()
tabs=[("TAB_TOP_L",(139,151,378,390)),("TAB_TOP_R",(169,181,378,390))]
frame=base
overlaps={}
for n,(a,b,c,d) in tabs:
 t=rect(a,b,c,d)
 q=base.intersect(t);overlaps[n]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
 frame=frame.union(t)
frame=frame.clean();v1=frame.val().Volume()
# hard exclusions used in retention gate
ex=[("CLEAT_L",(25.5,79.5,352,390)),("CLEAT_R",(240.5,294.5,352,390)),("UPPER_VENT_L",(0,129,339,400)),("UPPER_VENT_R",(191,320,339,400)),("MAIN_C",(85,235,315,370)),("ESP32_RF_COARSE",(64,119.5,318.5,366.5))]
hits={}
for tn,r in tabs:
 t=rect(*r)
 hits[tn]={}
 for en,e in ex:
  # cleat islands are existing structure but tab must not geometrically enter their projected boxes
  a,b,c,d=e;q=t.intersect(rect(a,b,c,d,0,40));hits[tn][en]=sum(s.Volume() for s in q.solids().vals()) if q.solids().size() else 0.
bb=frame.val().BoundingBox();dv=v1-v0
assert frame.val().isValid() and frame.solids().size()==1
assert all(v>0 for v in overlaps.values())
assert all(v<1e-8 for h in hits.values() for v in h.values())
cq.exporters.export(frame,"AP22_REAR_PC_CF_FRAME_RETENTION_REV_AP.step")
print(json.dumps({"valid":True,"solid_count":1,"bbox_mm":[bb.xlen,bb.ylen,bb.zlen],"z_extent_mm":[bb.zmin,bb.zmax],
"base_volume_mm3":v0,"retention_frame_volume_mm3":v1,"volume_delta_mm3":dv,
"mass_delta_g_density_1p20":dv*1.20/1000,"mass_delta_g_density_1p30":dv*1.30/1000,"mass_delta_g_density_1p40":dv*1.40/1000,
"tab_base_overlap_mm3":overlaps,"tab_exclusion_intersections_mm3":hits,
"artifact":"AP22_REAR_PC_CF_FRAME_RETENTION_REV_AP.step",
"limitations":["density values are sensitivity only","no fastener boss/hole yet","coarse keepouts/RF mask","local FEA not run"]},indent=2))
