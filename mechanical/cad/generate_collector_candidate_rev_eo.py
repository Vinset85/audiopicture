"""Full-coverage closed-floor, opposing-gate collector candidate.

Engineering candidate only. Rev.BK apertures and Z datum preserved.
Not a production release: restrictive throats, exact DMU/RF and CFD remain open.
"""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq

p=argparse.ArgumentParser()
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
# Strip the old chamber walls/roof below the shell. Keep shell, vents, returns, seats.
old=cq.importers.importStep(str(a.baseline))
shell=old.cut(box(14.9,51.1,13.9,62.1,33.9,37.8))
shell=shell.cut(box(268.9,305.1,13.9,62.1,33.9,37.8))
shell=shell.cut(box(14.9,51.1,314.9,363.1,35.0,37.8))
shell=shell.cut(box(268.9,305.1,314.9,363.1,35.0,37.8))
def collector(x0,x1,y0,y1,floor,gate1,gate2,gap1,gap2,exit_y):
    # Shell is the ceiling. Floor has no vent relief: prevents axial short circuit.
    ss=[box(x0,x1,y0,y1,floor,floor+1),
        box(x0,x0+1,y0,y1,floor+1,37.81),
        box(x0,x1,y0,y0+1,floor+1,37.81),
        box(x0,x1,y1-1,y1,floor+1,37.81)]
    for ya,yb in [(y0,exit_y[0]),(exit_y[1],y1)]:
        if yb>ya: ss.append(box(x1-1,x1,ya,yb,floor+1,37.81))
    for gx,(g0,g1) in [(gate1,gap1),(gate2,gap2)]:
        for ya,yb in [(y0+1,g0),(g1,y1-1)]:
            if yb>ya:ss.append(box(gx,gx+1,ya,yb,floor+1,37.81))
    s=ss[0]
    for q in ss[1:]:s=s.union(q)
    return s.clean()
lower=collector(15,36,12,172,34,28,32,(152,171),(13,150),(13,150))
upper=collector(15,77,313,351,35.1,64,70,(347,350),(314,317),(314,317))
collectors=[lower,lower.mirror('YZ',basePointVector=(160,0,0)),
            upper,upper.mirror('YZ',basePointVector=(160,0,0))]
solid=shell
for c in collectors:solid=solid.union(c)
solid=solid.clean()
# Exact Rev.BK vent profile: above z37.8 only, never cut floors or baffles.
lower_v=[('V',17,20,y,y+40) for y in (14,62,110)]+[('V',24,27,y,y+40) for y in (14,62,110)]
upper_v=[('H',17,62,y,y+3) for y in (315,322,329,336,343)]
vents=lower_v+upper_v
vents+= [(o,320-x1,320-x0,y0,y1) for o,x0,x1,y0,y1 in vents]
def capsule(r):
    o,x0,x1,y0,y1=r
    if o=='V':
        wire=cq.Workplane('XY',origin=(0,0,37.8)).moveTo(x0,y0+1.5).lineTo(x0,y1-1.5).threePointArc(((x0+x1)/2,y1),(x1,y1-1.5)).lineTo(x1,y0+1.5).threePointArc(((x0+x1)/2,y0),(x0,y0+1.5)).close()
    else:
        wire=cq.Workplane('XY',origin=(0,0,37.8)).moveTo(x0+1.5,y0).lineTo(x1-1.5,y0).threePointArc((x1,(y0+y1)/2),(x1-1.5,y1)).lineTo(x0+1.5,y1).threePointArc((x0,(y0+y1)/2),(x0+1.5,y0)).close()
    return wire.extrude(2.3)
reclosure=[sum(s.Volume() for s in solid.intersect(capsule(r)).solids().vals()) for r in vents]
fluid=box(.01,319.99,.01,399.99,33,40.25).cut(solid).clean()
axial=[]
for o,x0,x1,y0,y1 in vents:
    x,y=(x0+x1)/2,(y0+y1)/2
    e=cq.Edge.makeLine(cq.Vector(x,y,40.25),cq.Vector(x,y,33))
    axial.append(solid.val().distance(e)>1e-7)
# Test rays from distributed aperture samples to nearby cavity, including axial
# witnesses omitted in historical Rev.EF. This is finite screening, not proof.
opened=0;total=0;examples=[]
for o,x0,x1,y0,y1 in vents:
    for f in (.1,.5,.9):
        x=x0+(x1-x0)*f if o=='H' else (x0+x1)/2
        y=y0+(y1-y0)*f if o=='V' else (y0+y1)/2
        for dest in [(x,y,33),(80,y,33),(240,y,33),(160,200,33),
                     (x,y+25,33),(x,y-25,33),(80,y,36.5),(240,y,36.5)]:
            edge=cq.Edge.makeLine(cq.Vector(x,y,40.25),cq.Vector(*dest))
            if solid.val().distance(edge)>1e-7:
                opened+=1
                if len(examples)<12:examples.append({'source':[x,y,40.25],'destination':dest})
            total+=1
result={'revision':'Rev.EO','classification':'CAD_CANDIDATE_NOT_PRODUCTION',
        'solid_valid':solid.val().isValid(),'solid_components':solid.solids().size(),
        'solid_volume_mm3':sum(s.Volume() for s in solid.solids().vals()),
        'fluid_valid':fluid.val().isValid(),'fluid_components':fluid.solids().size(),
        'fluid_volume_mm3':sum(s.Volume() for s in fluid.solids().vals()),
        'max_vent_reclosure_mm3':max(reclosure),'open_axial_rays':sum(axial),
        'sampled_rays':total,'open_sampled_rays':opened,'examples':examples,
        'upper_air_height_mm':1.7,'lower_air_height_mm':2.8,
        'lower_gate_opening_area_mm2':19*2.8,'upper_gate_opening_area_mm2':3*1.7,
        'lower_inter_gate_cross_section_mm2':3*2.8,
        'upper_inter_gate_cross_section_mm2':5*1.7,
        'full_vent_footprint_coverage_count':22,
        'airflow_area_contract_gate':'FAIL',
        'release':'FAIL_NOT_FABRICABLE_RELEASE',
        'limitations':['Upper 5.1 mm2 gate per side is restrictive; thermal capacity unproven.',
                       'Local slab fluid is not full CFD geometry.',
                       'Exact component/harness/RF masks not present.',
                       'No acoustic attenuation or CFD/FEA result.',
                       'No process tolerance assigned; 1 mm walls are design candidate dimensions.']}
for name,obj in [('solid',solid),('fluid',fluid)]:
    if obj.val().isValid():
        path=a.out/f'AP22_REV_EO_{name.upper()}.step'
        cq.exporters.export(obj,str(path))
        result[name+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
(a.out/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
