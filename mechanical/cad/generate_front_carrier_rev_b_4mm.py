import cadquery as cq
import math
import json

OUT = "AP22_FRONT_CARRIER_REV_B_4MM_DMU.step"

xmin, xmax, ymin, ymax = 0.8, 319.2, 0.8, 399.2
W, H = xmax-xmin, ymax-ymin
ring = 10.0
base_t = 1.8
station_t = 3.2
pocket_d = 4.4
pocket_r = pocket_d/2
pocket_depth = 2.2

outer = cq.Workplane("XY").rect(W,H).extrude(base_t).translate(((xmin+xmax)/2,(ymin+ymax)/2,0))
inner = cq.Workplane("XY").rect(W-2*ring,H-2*ring).extrude(base_t+1).translate(((xmin+xmax)/2,(ymin+ymax)/2,-0.5))
part = outer.cut(inner)

stations = [
 ("M1D",70,394,"top"), ("M2D",250,394,"top"),
 ("M3D",70,6,"bottom"), ("M4D",250,6,"bottom"),
 ("M5D",6,135,"left"), ("M6D",6,275,"left"),
 ("M7D",314,135,"right"), ("M8D",314,315,"right")
]

outer_clip = cq.Workplane("XY").rect(W,H).extrude(station_t+2).translate(((xmin+xmax)/2,(ymin+ymax)/2,-1))
legal = {
 "top": cq.Workplane("XY").box(400,20,station_t+2,centered=(True,False,False)).translate((160,390.5,-1)),
 "bottom": cq.Workplane("XY").box(400,9.5,station_t+2,centered=(True,False,False)).translate((160,0,-1)),
 "left": cq.Workplane("XY").box(9.5,500,station_t+2,centered=(False,True,False)).translate((0,200,-1)),
 "right": cq.Workplane("XY").box(20,500,station_t+2,centered=(False,True,False)).translate((310.5,200,-1)),
}

for _,x,y,side in stations:
    stock = cq.Workplane("XY").center(x,y).circle(6.0).extrude(station_t-base_t).translate((0,0,base_t))
    part = part.union(stock.intersect(legal[side]).intersect(outer_clip))

for _,x,y,_ in stations:
    bore = cq.Workplane("XY").center(x,y).circle(pocket_r).extrude(pocket_depth).translate((0,0,station_t-pocket_depth))
    part = part.cut(bore)

# Diagnostic capture seeds only; not production-frozen.
for _,x,y,_ in stations:
    for ang in (0,120,240):
        a = math.radians(ang)
        rr = pocket_r-0.15
        nx, ny = x+rr*math.cos(a), y+rr*math.sin(a)
        nub = cq.Workplane("XY").center(nx,ny).circle(0.45).extrude(0.45).translate((0,0,station_t-0.45))
        part = part.union(nub)

peel = cq.Workplane("XY").box(28,5,station_t+2,centered=(True,False,False)).translate((160,0,-1))
part = part.cut(peel).clean()

shape = part.val()
solids = part.solids().vals()
bb = shape.BoundingBox()
vol = sum(s.Volume() for s in solids)

dml_rear = cq.Workplane("XY").box(300,380,station_t-base_t+0.2,centered=(False,False,False)).translate((10,10,base_t))
inter = part.intersect(dml_rear)
inter_vol = sum(s.Volume() for s in inter.solids().vals()) if inter.solids().size() else 0.0

clearances=[]
outerwalls=[]
for name,x,y,side in stations:
    if side=="top":
        dmlc=(y-pocket_r)-390; ow=399.2-(y+pocket_r)
    elif side=="bottom":
        dmlc=10-(y+pocket_r); ow=(y-pocket_r)-0.8
    elif side=="left":
        dmlc=10-(x+pocket_r); ow=(x-pocket_r)-0.8
    else:
        dmlc=(x-pocket_r)-310; ow=319.2-(x+pocket_r)
    clearances.append((name,dmlc)); outerwalls.append((name,ow))

cq.exporters.export(part, OUT)

print(json.dumps({
 "valid": shape.isValid(),
 "solid_count": len(solids),
 "volume_mm3": vol,
 "bbox_mm": [bb.xlen,bb.ylen,bb.zlen],
 "dml_station_z_intersection_mm3": inter_vol,
 "min_pocket_to_dml_mm": min(v for _,v in clearances),
 "min_dml_side_ligament_after_0p5_keepout_mm": min(v for _,v in clearances)-0.5,
 "min_outer_wall_mm": min(v for _,v in outerwalls),
 "step": OUT
}, indent=2))
