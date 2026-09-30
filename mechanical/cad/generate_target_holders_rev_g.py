import cadquery as cq
import json

OUT="AP22_TARGET_HOLDERS_REV_G_DMU.step"
DML=(10,310,10,390)
carrier=(0.8,319.2,0.8,399.2)
target=7.0
rail=0.8
clr=0.15
z_target0=4.1
z_target1=5.1
shelf_t=0.8
rail_z0=5.1
rail_h=1.2

stations=[
 ("M1D",70,394,"top"),("M2D",250,394,"top"),
 ("M3D",70,6,"bottom"),("M4D",250,6,"bottom"),
 ("M5D",6,135,"left"),("M6D",6,275,"left"),
 ("M7D",314,135,"right"),("M8D",314,315,"right")
]

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

def holder(x,y,side):
    half=target/2
    tang_half=half+clr
    pieces=[]
    if side in ("top","bottom"):
        # tangential rails
        pieces += [
          box(x-tang_half-rail,x-tang_half,y-half,y+half,rail_z0,rail_z0+rail_h),
          box(x+tang_half,x+tang_half+rail,y-half,y+half,rail_z0,rail_z0+rail_h)]
        if side=="top":
            pieces += [box(x-tang_half-rail,x+tang_half+rail,y+half,y+half+rail,rail_z0,rail_z0+rail_h)]
            pieces += [box(x-tang_half-rail,x+tang_half+rail,y-half,y+half+rail,z_target1,z_target1+shelf_t)]
        else:
            pieces += [box(x-tang_half-rail,x+tang_half+rail,y-half-rail,y-half,rail_z0,rail_z0+rail_h)]
            pieces += [box(x-tang_half-rail,x+tang_half+rail,y-half-rail,y+half,z_target1,z_target1+shelf_t)]
    else:
        pieces += [
          box(x-half,x+half,y-tang_half-rail,y-tang_half,rail_z0,rail_z0+rail_h),
          box(x-half,x+half,y+tang_half,y+tang_half+rail,rail_z0,rail_z0+rail_h)]
        if side=="left":
            pieces += [box(x-half-rail,x-half,y-tang_half-rail,y+tang_half+rail,rail_z0,rail_z0+rail_h)]
            pieces += [box(x-half-rail,x+half,y-tang_half-rail,y+tang_half+rail,z_target1,z_target1+shelf_t)]
        else:
            pieces += [box(x+half,x+half+rail,y-tang_half-rail,y+tang_half+rail,rail_z0,rail_z0+rail_h)]
            pieces += [box(x-half,x+half+rail,y-tang_half-rail,y+tang_half+rail,z_target1,z_target1+shelf_t)]
    h=pieces[0]
    for p in pieces[1:]: h=h.union(p)
    return h.clean()

assembly=None
for _,x,y,s in stations:
    h=holder(x,y,s)
    assembly=h if assembly is None else assembly.union(h)

dml=box(10,310,10,390,3.3,9.3)
iv=assembly.intersect(dml)
inter=sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0.0
bb=assembly.val().BoundingBox()
cq.exporters.export(assembly,OUT)
print(json.dumps({
 "valid":assembly.val().isValid(),
 "solid_count":assembly.solids().size(),
 "dml_intersection_mm3":inter,
 "bbox_mm":[bb.xlen,bb.ylen,bb.zlen],
 "z_extent_mm":[bb.zmin,bb.zmax],
 "artifact":OUT
},indent=2))
