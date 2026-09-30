# AudioPicture V2.2 retention dimensional coupon pair Rev.BA
# Generates representative ASA-seat and PC-CF-interface coupons for metrology.
import cadquery as cq, json
# Coupon sizes chosen for handling/metrology, not product-release geometry.
ASA_X=50.;ASA_Y=30.;ASA_T=2.2;SEAT_D=10.;SEAT_H=1.8
PC_X=50.;PC_Y=30.;PC_T=8.0
# ASA: rear-wall coupon, inner surface z=0, outer surface z=+2.2, seat protrudes inward to -1.8.
asa=cq.Workplane("XY").box(ASA_X,ASA_Y,ASA_T,centered=(True,True,False))
seat=cq.Workplane("XY",origin=(0,0,-SEAT_H)).circle(SEAT_D/2).extrude(SEAT_H)
asa=asa.union(seat).clean()
# PC-CF: representative local interface block, top/rear metrology plane at z=0, body to -8.
pc=cq.Workplane("XY",origin=(0,0,-PC_T)).box(PC_X,PC_Y,PC_T,centered=(True,True,False)).clean()
assert asa.val().isValid() and asa.solids().size()==1
assert pc.val().isValid() and pc.solids().size()==1
cq.exporters.export(asa,"AP22_RETENTION_COUPON_ASA_REV_BA.step")
cq.exporters.export(asa,"AP22_RETENTION_COUPON_ASA_REV_BA.stl")
cq.exporters.export(pc,"AP22_RETENTION_COUPON_PC_CF_REV_BA.step")
cq.exporters.export(pc,"AP22_RETENTION_COUPON_PC_CF_REV_BA.stl")
print(json.dumps({"asa":{"valid":True,"size_mm":[ASA_X,ASA_Y,ASA_T],"seat_d_mm":SEAT_D,"seat_h_nominal_mm":SEAT_H,
"measure":["outer-to-inner wall thickness","inner-plane to seat-front protrusion","local flatness around seat"]},
"pc_cf":{"valid":True,"size_mm":[PC_X,PC_Y,PC_T],"measure":["interface-plane flatness","local thickness/reference repeatability"]},
"paired_measurement":["assemble on common datum/fixture","measure resulting local seat-to-PC-CF gap or datum difference"],
"replication_recommendation":"minimum 5 coupons per material/process condition for pilot screening; production capability requires a statistically justified sample plan",
"limitations":["coupon geometry does not reproduce full 320x400 ASA warpage","coupon does not reproduce full PC-CF frame distortion","no capability claim from CAD","final six-node measurements on full parts remain mandatory"]},indent=2))
