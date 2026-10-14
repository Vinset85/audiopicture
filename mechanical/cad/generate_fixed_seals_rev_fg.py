"""Nominal fixed-frame/DML sealing land, isolated from magnetic front retention.

The compressed gasket shapes are geometric domains, not measured porous-media
or compression laws. Preload retention and the actual manufactured stack still
require independent verification. Rear vent caps exist only in the leak audit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
def ring(x0,x1,y0,y1,xi0,xi1,yi0,yi1,z0,z1):
    return box(x0,x1,y0,y1,z0,z1).cut(box(xi0,xi1,yi0,yi1,z0-.1,z1+.1))
def volume(w):
    value=0.
    for s in w.solids().vals():
        props=GProp_GProps();BRepGProp.VolumeProperties_s(s.wrapped,props,1e-10,True,False);value+=props.Mass()
    return value
paths={
    'frame':'evidence/rev-fg/frame/AP22_FRAME_INTERFACE_CANDIDATE_REV_FG.step',
    'shell':'evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step',
    'front':'evidence/rev-fa/AP22_FRONT_CARRIER_OPTICAL_CANDIDATE_REV_FA.step',
}
parts={n:cq.importers.importStep(str(ROOT/path)) for n,path in paths.items()}
frame=parts['frame']
# The six-mm DML edge land follows the existing mounting contract. A 2 mm
# foam is represented at 20% nominal compression; no force is assigned here.
ledge=ring(3.2,316.8,3.2,396.8,16,304,16,384,10.9,13.3)
frame=frame.union(ledge)
# Radial seal: 1.57 mm nominal sheet at 20% geometric compression. This
# requires a prepared land, rather than forcing it into the original 1 mm gap.
radial_gap=1.57*.8;edge=2.2+radial_gap
relief=ring(0,320,0,400,edge,320-edge,edge,400-edge,10.9,13.3)
frame=frame.cut(relief).clean()
dml=box(10,310,10,390,3.3,9.3)
dml_seal=ring(10,310,10,390,16,304,16,384,9.3,10.9)
radial_seal=ring(2.2,317.8,2.2,397.8,edge,320-edge,edge,400-edge,10.9,13.3)
# Remove inherited stock from the foam seat; the land begins at Z10.9.
frame=frame.cut(dml_seal).clean()
parts.update(frame=frame,DML=dml,DML_seal=dml_seal,frame_shell_seal=radial_seal)
for n,w in parts.items():
    assert w.val().isValid() and w.solids().size()==1,n
overlaps={}
names=list(parts)
for i,n in enumerate(names):
    for m in names[i+1:]:
        overlaps[n+'/'+m]=volume(parts[n].intersect(parts[m]))
assert max(overlaps.values())<1e-5,overlaps
keepouts={
    'EX_L1':[37,99,50,110,9.3,36.3],'EX_L2':[83,145,166,226,9.3,36.3],
    'EX_R1':[175,237,238,298,9.3,36.3],'EX_R2':[223,285,88,148,9.3,36.3],
    'MAIN_C':[85,235,315,370,16,36.6],'MAIN_P':[105,220,112,157,17,33],
    'VOICE':[119,201,20,102,11,18],'RADAR':[249,287,184,216,0,18],
    'ENV':[252,294,35,59,11,18],'SERVICE':[100,220,20,48,20,40],
    'ESP32_RF':[64,119.5,318.5,366.5,0,40],
}
for n,v in keepouts.items():
    for part in ['frame','DML_seal','frame_shell_seal']:
        assert volume(parts[part].intersect(box(*v)))<1e-5,(part,n)

# Prove separation of front air and rear cavity with the specified rear vents
# temporarily capped. This tests the complete nominal BREP partition, not a
# selection of rays. Removing each seal must restore an unintended path.
material=parts['shell'].union(frame).union(dml).union(dml_seal).union(radial_seal).clean()
eq=json.loads((ROOT/'evidence/rev-eq/execution.json').read_text())
cap=None
for cell in eq['cells']:
    x0,x1,y0,y1=cell['aperture_xy'];v=box(x0-.1,x1+.1,y0-.1,y1+.1,39.9,40.1)
    cap=v if cap is None else cap.union(v)
envelope=box(0,320,0,400,0,40)
rear_point=cq.Vector(160,200,25);front_point=cq.Vector(160,200,1)
def partition(material):
    air=envelope.cut(material.union(cap)).clean()
    assert air.val().isValid()
    solids=air.solids().vals()
    rear=[i for i,s in enumerate(solids) if s.isInside(rear_point)]
    front=[i for i,s in enumerate(solids) if s.isInside(front_point)]
    assert len(rear)==len(front)==1
    return air,{'components':len(solids),'rear_component':rear[0],'front_component':front[0],
                'rear_front_connected':rear[0]==front[0], 'volumes_mm3':[s.Volume() for s in solids]}
air,closed=partition(material)
assert not closed['rear_front_connected'],closed
_,without_radial=partition(parts['shell'].union(frame).union(dml).union(dml_seal))
_,without_dml=partition(parts['shell'].union(frame).union(dml).union(radial_seal))
assert without_radial['rear_front_connected'] and without_dml['rear_front_connected']
rear_air=air.solids().vals()[closed['rear_component']]

# The former witness polylines now encounter the radial seal.
paths_blocked=[]
for y in [180,250,300]:
    edge_path=cq.Edge.makeLine(cq.Vector(2.7,y,3),cq.Vector(2.7,y,36.5))
    distance=radial_seal.val().distance(edge_path)
    assert distance<1e-7
    paths_blocked.append({'Y_mm':y,'seal_distance_mm':distance})

exports={'FRAME_SEAL_LAND':frame,'DML_GASKET_COMPRESSED':dml_seal,
         'FRAME_SHELL_GASKET_COMPRESSED':radial_seal,'DML_NOMINAL':dml,
         'CAPPED_REAR_AIR_AUDIT_ONLY':cq.Workplane(obj=rear_air)}
artifacts={}
for n,w in exports.items():
    f=a.out/f'AP22_{n}_REV_FG.step';cq.exporters.export(w,str(f))
    back=cq.importers.importStep(str(f));assert back.val().isValid() and back.solids().size()==1
    err=abs(volume(back)-volume(w))/max(volume(w),1);assert err<1e-6,(n,err)
    artifacts[n]={'file':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'STEP_relative_volume_error':err}
original=json.loads((ROOT/'evidence/rev-fg/frame/execution.json').read_text())
base={k:original[k] for k in ['mount_centers_xy_mm','bore_radius_mm','bore_z_mm','boss_outer_diameter_mm','floor_mm','root_fillet_mm','limitations']}
base['parent_geometry_sha256']=hashlib.sha256((ROOT/'evidence/rev-fg/frame/execution.json').read_bytes()).hexdigest()
base['BREP_valid']=True
base['solid_count']=1
base['STEP_reimport_valid']=True
framefile=a.out/'AP22_FRAME_SEAL_LAND_REV_FG.step'
base.update(revision='Rev.FG seal-land candidate',volume_mm3=volume(frame),mass_g_at_catalog_density_1p22=volume(frame)*.00122,
            artifacts={framefile.name:{'sha256':hashlib.sha256(framefile.read_bytes()).hexdigest()}},
            limitations=base['limitations']+['DML preload retention, gasket properties and installed seal compression are unqualified.'])
(a.out/'frame-geometry.json').write_text(json.dumps(base,indent=2)+'\n')
report={'classification':'CALCULATED_NOMINAL_BREP_PARTITION_WITH_IMPERMEABLE_GASKET_ASSUMPTION',
        'status':'PASS_NOMINAL_FRONT_REAR_PARTITION_WITH_22_AUDIT_CAPS',
        'frame_volume_mm3':volume(frame),'frame_mass_g_at_catalog_density_1p22':volume(frame)*.00122,
        'DML_foam_nominal_free_mm':2,'DML_foam_installed_mm':1.6,'DML_foam_land_width_mm':6,
        'radial_foam_nominal_free_mm':1.57,'radial_foam_installed_mm':radial_gap,
        'nominal_compression_fraction':.2,'part_overlap_mm3':overlaps,
        'capped_partition':closed,'without_radial_seal':without_radial,'without_DML_seal':without_dml,
        'former_path_segments_intercepted':paths_blocked,'audit_caps_count':len(eq['cells']),
        'artifacts':artifacts,'source_sha256':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths.values()},
        'limits':['Audit caps must never be included in production CAD or the real-aperture CFD model.',
                  'Gaskets are assumed impermeable in this topology calculation; their air permeability and leak rate are not measured.',
                  'Magnetic front provides no modeled gasket preload; a separate fixed DML retainer and hard stops remain required.',
                  'This nominal partition excludes future service, mount, microphone and environmental penetrations.',
                  'No thermal CFD, acoustic attenuation, tolerance closure or physical seal qualification is implied.']}
report['source_sha256'][str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(a.out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','frame_volume_mm3','frame_mass_g_at_catalog_density_1p22','capped_partition','without_radial_seal','without_DML_seal']},indent=2))
