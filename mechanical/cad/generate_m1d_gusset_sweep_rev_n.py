import cadquery as cq
import json, math

OUT_PREFIX="AP22_M1D_GUSSET"
E=1900.0 # N/mm2 screening only
P=5.0
x=70.0

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

def prism_xz(x0,x1,y0,y1,z_front,z_rear_front,z_rear):
    # triangular prism, extrusion in Y
    pts=[(x0,z_front),(x1,z_front),(x1,z_rear),(x0,z_rear_front)]
    return cq.Workplane("XZ").polyline(pts).close().extrude(y1-y0).translate((0,y0,0))

# M1D base
rear=box(30,110,388,398,27,35)
ret=box(65,75,390.4,392.8,6,29)
tab=box(65,75,390.5,392.5,5.1,9.2)
dml=box(10,310,10,390,3.3,9.3)

results=[]
for Lg in [0,8,12,16]:
    m=rear.union(ret).union(tab)
    # Two tangential side gussets at x edges; grow rearward from return toward ring.
    if Lg:
        # wedge in YZ concept approximated by triangular prisms along X edge strips
        # z starts at 27-Lg and grows to full ring/root at z27..29
        zf=max(9.2,27-Lg)
        g1=box(63.8,65.0,390.4,392.8,zf,27)
        g2=box(75.0,76.2,390.4,392.8,zf,27)
        # connect strips into rear ring with root overlap
        g1=g1.union(box(63.8,65.0,390.4,392.8,27,29))
        g2=g2.union(box(75.0,76.2,390.4,392.8,27,29))
        m=m.union(g1).union(g2)
    m=m.clean()
    iv=m.intersect(dml)
    bb=m.val().BoundingBox()
    vol=sum(s.Volume() for s in m.solids().vals())
    # screening effective weak-axis I: base + two side strips only over gusseted length.
    I0=10*(2.4**3)/12
    Iroot=(12.4*(2.4**3)/12) if Lg else I0
    # conservative stepped-beam integration: curvature compliance integral (L-x)^2/(E I(x)) dx
    L=17.8
    n=20000
    dx=L/n
    integ=0
    for i in range(n):
        xx=(i+0.5)*dx
        # gusset affects rear/root portion of length Lg
        I=Iroot if (Lg and xx>=max(0,L-Lg)) else I0
        integ += ((L-xx)**2)/(E*I)*dx
    delta=P*integ
    name=f"G{[0,8,12,16].index(Lg)}"
    cq.exporters.export(m,f"{OUT_PREFIX}_{name}.step")
    results.append({
      "variant":name,"gusset_length_mm":Lg,"valid":m.val().isValid(),
      "solid_count":m.solids().size(),"volume_mm3":vol,
      "delta_5N_screen_mm":delta,
      "dml_intersection_mm3":sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0,
      "bbox_mm":[bb.xlen,bb.ylen,bb.zlen]
    })
print(json.dumps(results,indent=2))
