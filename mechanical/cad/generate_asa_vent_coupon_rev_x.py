# ASA upper-outlet dimensional coupon Rev.X
# CadQuery/OpenCASCADE parametric coupon for process characterization.
# It does NOT assign manufacturing capability; it creates the specimen to measure.
import cadquery as cq
import json

T=2.2
SLOT_W=3.0
SLOT_L=45.0
WEB_NOM=4.0
EDGE=8.0
PLATE_X=125.0
PLATE_Y=100.0

plate=cq.Workplane("XY").box(PLATE_X,PLATE_Y,T,centered=(False,False,False))

# Two horizontal adjacent slots: common-web measurement in Y.
# Two vertical adjacent slots: common-web measurement in X.
slots=[
 ("H1",15.0,60.0,62.0,65.0),
 ("H2",15.0,60.0,69.0,72.0), # 4 mm nominal web
 ("V1",80.0,83.0,15.0,60.0),
 ("V2",87.0,90.0,15.0,60.0), # 4 mm nominal web
]

cutters=[]
for n,x0,x1,y0,y1 in slots:
    c=cq.Workplane("XY").box(x1-x0,y1-y0,T+2,centered=(False,False,False)).translate((x0,y0,-1))
    cutters.append((n,c))
    plate=plate.cut(c)

# Add isolated reference slots for absolute width/length measurement.
refs=[
 ("H_REF",15.0,60.0,25.0,28.0),
 ("V_REF",105.0,108.0,15.0,60.0),
]
for n,x0,x1,y0,y1 in refs:
    c=cq.Workplane("XY").box(x1-x0,y1-y0,T+2,centered=(False,False,False)).translate((x0,y0,-1))
    plate=plate.cut(c)

assert plate.val().isValid()
assert plate.solids().size()==1
bb=plate.val().BoundingBox()
print(json.dumps({
 "valid":plate.val().isValid(),
 "solid_count":plate.solids().size(),
 "plate_mm":[PLATE_X,PLATE_Y,T],
 "slot_nominal_mm":[SLOT_W,SLOT_L],
 "critical_web_nominal_mm":WEB_NOM,
 "slots":[s[0:1]+s[1:] for s in slots],
 "reference_slots":[s[0:1]+s[1:] for s in refs],
 "bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
 "purpose":"process characterization only; no capability claim"
},indent=2))

cq.exporters.export(plate,"AP22_ASA_VENT_COUPON_REV_X.step")
cq.exporters.export(plate,"AP22_ASA_VENT_COUPON_REV_X.stl")
