import cadquery as cq
import json

OUT="AP22_M1D_FEA_SUBMODEL_REV_K.step"
x=70.0
# M1D top station. Rear-ring local span sensitivity seed: +/-40 mm.
span=40.0

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

# rear top ring local segment: ring Y388..398, Z27..35
rear=box(x-span,x+span,388,398,27,35)
# return and tab exactly as Rev.J M1D
ret=box(x-5,x+5,390.4,392.8,6,29)
tab=box(x-5,x+5,390.5,392.5,5.1,9.2)

sub=rear.union(ret).union(tab).clean()
rr=rear.intersect(ret)
rt=ret.intersect(tab)
dml=box(10,310,10,390,3.3,9.3)
iv=sub.intersect(dml)

cq.exporters.export(sub,OUT)
bb=sub.val().BoundingBox()
print(json.dumps({
 "valid":sub.val().isValid(),
 "solid_count":sub.solids().size(),
 "rear_return_overlap_mm3":sum(s.Volume() for s in rr.solids().vals()) if rr.solids().size() else 0,
 "return_tab_overlap_mm3":sum(s.Volume() for s in rt.solids().vals()) if rt.solids().size() else 0,
 "dml_intersection_mm3":sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0,
 "bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
 "rear_ring_half_span_mm":span,
 "artifact":OUT
},indent=2))
