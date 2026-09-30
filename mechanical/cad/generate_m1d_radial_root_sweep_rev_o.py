import cadquery as cq
import json, math

E=1900.0
P=5.0
x=70.0
L=17.7 # screen from just behind DML to rear-ring onset

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane("XY").box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))

rear=box(30,110,388,398,27,35)
tab=box(65,75,390.5,392.5,5.1,9.2)
dml=box(10,310,10,390,3.3,9.3)

results=[]
for idx,hroot in enumerate([2.4,3.2,4.0,5.0]):
    # Front blade remains 2.4 mm radial. Behind DML, add only outward material
    # (toward +Y at top station), linearly approximated by 0.5 mm Z slices.
    m=rear.union(box(65,75,390.4,392.8,6,29)).union(tab)
    dz=0.5
    z=9.3
    while z < 27.0-1e-9:
        z1=min(z+dz,27.0)
        f=((z+z1)/2-9.3)/(27.0-9.3)
        h=2.4+(hroot-2.4)*max(0,min(1,f))
        # growth outward only: inner DML-facing edge fixed at Y390.4
        m=m.union(box(65,75,390.4,390.4+h,z,z1))
        z=z1
    # full root depth continues through overlap into rear ring
    m=m.union(box(65,75,390.4,390.4+hroot,27,29)).clean()

    iv=m.intersect(dml)
    solids=m.solids().vals()
    vol=sum(s.Volume() for s in solids)

    # Variable-section cantilever screening, h grows linearly 2.4 -> hroot.
    # x=0 front end just behind DML, x=L root.
    n=50000; dx=L/n; integ=0.0
    b=10.0
    for i in range(n):
        xx=(i+0.5)*dx
        h=2.4+(hroot-2.4)*(xx/L)
        I=b*h**3/12.0
        # unit-load / curvature integration for end-load deflection
        integ += ((L-xx)**2)/(E*I)*dx
    delta=P*integ
    bb=m.val().BoundingBox()
    name=f"R{idx}"
    cq.exporters.export(m,f"AP22_M1D_RADIAL_ROOT_{name}.step")
    results.append({
      "variant":name,"root_radial_depth_mm":hroot,
      "valid":m.val().isValid(),"solid_count":len(solids),
      "volume_mm3":vol,
      "added_volume_vs_R0_mm3":None,
      "dml_intersection_mm3":sum(s.Volume() for s in iv.solids().vals()) if iv.solids().size() else 0,
      "delta_5N_variable_section_screen_mm":delta,
      "bbox_mm":[bb.xlen,bb.ylen,bb.zlen]
    })
v0=results[0]["volume_mm3"]
for r in results:r["added_volume_vs_R0_mm3"]=r["volume_mm3"]-v0
print(json.dumps(results,indent=2))
