"""Independently reimport mount CAD and audit air partition and rigid motion.

Gaskets remain impermeable geometric assumptions. Swept unfilleted wall
profiles conservatively enclose the actual filleted and drilled wall cleats.
"""
import hashlib
import argparse
import json
from pathlib import Path
import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=ROOT/'evidence/rev-fg/upper-mounts-chamfer');a=p.parse_args()
folder=a.folder.resolve()
source=folder/'execution.json'; info=json.loads(source.read_text())
(folder/'independent-audit.json').unlink(missing_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=False).translate((x0,y0,z0))
def volume(w):
    out=0.
    for s in w.solids().vals():
        prop=GProp_GProps();BRepGProp.VolumeProperties_s(s.wrapped,prop,1e-10,True,False);out+=prop.Mass()
    return out
parts={}
for n,a in info['artifacts'].items():
    p=ROOT/a['file'];assert digest(p)==a['sha256']
    w=cq.importers.importStep(str(p));assert w.val().isValid() and w.solids().size()==1
    assert abs(volume(w)-a['volume_mm3'])/max(a['volume_mm3'],1)<1e-6
    parts[n]=w
for path,h in info['source_sha256'].items():assert digest(ROOT/path)==h,path

eq=json.loads((ROOT/'evidence/rev-eq/execution.json').read_text())
caps=None
for cell in eq['cells']:
    x0,x1,y0,y1=cell['aperture_xy'];v=box(x0-.1,x1+.1,y0-.1,y1+.1,39.9,40.1)
    caps=v if caps is None else caps.union(v)
barriers=['shell','frame','DML','DML_seal','frame_shell_seal']+[n for n in parts if n.startswith('BOSS_SEAL')]
points={'rear':[160,200,25],'front':[160,200,1],'pocket_L':[52.5,380,36],'pocket_R':[267.5,380,36]}
def partition(skip=None):
    air=box(0,320,0,400,0,40);checks=[]
    for n,w in [(n,parts[n]) for n in barriers if n!=skip]+[('audit_caps',caps)]:
        expected=volume(air)-volume(air.intersect(w));new=air.cut(w).clean()
        assert new.val().isValid(),n
        residual=volume(new)-expected;assert abs(residual)<.05,(n,residual)
        checks.append(residual);air=new
    solids=air.solids().vals();mapping={}
    for n,p in points.items():
        inside=[i for i,s in enumerate(solids) if s.isInside(cq.Vector(*p))]
        assert len(inside)==1,(n,inside)
        mapping[n]=inside[0]
    return air,{'omitted_seal':skip,'components':len(solids),'point_components':mapping,
                'volumes_mm3':[volume(cq.Workplane(obj=s)) for s in solids],
                'max_incremental_volume_residual_mm3':max(map(abs,checks))}
air,closed=partition();m=closed['point_components']
assert all(m['rear']!=m[n] for n in ['front','pocket_L','pocket_R'])
controls=[]
for name in [n for n in barriers if n.startswith('BOSS_SEAL')]:
    _,r=partition(name);side='L' if '_L' in name else 'R'
    assert r['point_components']['rear']==r['point_components']['pocket_'+side],name
    controls.append(r)
print('Independent partition and four omitted-seal controls passed',flush=True)

# Preserve all existing parallel-cell material. This is a geometry comparison,
# independent of connectivity, and does not establish acoustic attenuation.
old_path=ROOT/'evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step'
old=cq.importers.importStep(str(old_path));cell_region=box(0,320,0,355,0,40)
before=old.intersect(cell_region);after=parts['shell'].intersect(cell_region)
differences={'added_mm3':volume(after.cut(before)),'removed_mm3':volume(before.cut(after))}
assert max(differences.values())<1e-4

def swept_profile(profile,dy,dz,x0):
    shapes=[profile,[(y+dy,z+dz) for y,z in profile]]
    for (y1,z1),(y2,z2) in zip(profile,profile[1:]+profile[:1]):
        if abs((y2-y1)*dz-(z2-z1)*dy)>1e-8:
            shapes.append([(y1,z1),(y2,z2),(y2+dy,z2+dz),(y1+dy,z1+dz)])
    result=None
    for polygon in shapes:
        s=cq.Workplane('YZ').polyline(polygon).close().extrude(50).translate((x0,0,0))
        result=s if result is None else result.union(s)
    assert result.val().isValid()
    return result

motions=[]
product_names=['frame','shell','DML','DML_seal','frame_shell_seal']+[n for n in parts if n.startswith(('PRODUCT_CLEAT','SCREW','BOSS_SEAL'))]
for side,x0 in [('L',27.5),('R',242.5)]:
    profile=info['wall_profile_YZ_mm']
    hull=cq.Workplane('YZ').polyline(profile).close().extrude(50).translate((x0,0,0))
    assert volume(parts['WALL_CLEAT_'+side].cut(hull))<1e-5
    # Product moves +Y7 relative to a fixed wall: equivalently sweep wall -Y7.
    lift_sweep=swept_profile(profile,-7,0,x0)
    extraction_sweep=swept_profile(profile,0,6.6,x0)
    overlaps={}
    for n in product_names:
        v=volume(parts[n].intersect(lift_sweep))
        u=volume(parts[n].translate((0,7,0)).intersect(extraction_sweep))
        assert max(v,u)<1e-5,(side,n,v,u)
        overlaps[n]={'lift_path_mm3':v,'outward_path_after_lift_mm3':u}
    # Beyond 6.6 mm outward movement, the bounding Z intervals separate.
    assert max(parts[n].val().BoundingBox().zmax for n in product_names)-6.6 < parts['WALL_CLEAT_'+side].val().BoundingBox().zmin
    motions.append({'side':side,'lift_mm':7,'outward_sweep_mm':6.6,'overlap_checks':overlaps})

for thickness in [1,2]:
    for side in ['L','R']:
        spacer=parts[f'WALL_SPACER_{thickness}MM_{side}']
        assert abs(spacer.val().BoundingBox().zmax-(43+thickness))<1e-6
        for n in product_names:assert volume(spacer.intersect(parts[n]))<1e-6

keepouts={
 'EX_L1':[37,99,50,110,9.3,36.3],'EX_L2':[83,145,166,226,9.3,36.3],
 'EX_R1':[175,237,238,298,9.3,36.3],'EX_R2':[223,285,88,148,9.3,36.3],
 'MAIN_C':[85,235,315,370,16,36.6],'MAIN_P':[105,220,112,157,17,33],
 'VOICE':[119,201,20,102,11,18],'RADAR':[249,287,184,216,0,18],
 'ENV':[252,294,35,59,11,18],'SERVICE':[100,220,20,48,20,40],
 'ESP32_RF':[64,119.5,318.5,366.5,0,50]}
checks={}
for name,b in keepouts.items():
    forbidden=box(*b)
    for n in ['frame']+[n for n in parts if n.startswith(('PRODUCT_CLEAT','WALL_CLEAT','SCREW','WALL_SPACER','WALL_HEAD'))]:
        value=volume(parts[n].intersect(forbidden));assert value<1e-5,(n,name,value)
        checks[n+'/'+name]={'overlap_mm3':value,'nominal_distance_mm':parts[n].val().distance(forbidden.val())}

report={'status':'PASS_SCOPED_REIMPORTED_PARTITION_AND_CONTINUOUS_RIGID_SWEPT_CHECKS',
 'classification':'CALCULATED_NOMINAL_CAD_NOT_CONTACT_FEA_OR_PHYSICAL_SEAL_TEST',
 'closed_partition':closed,'each_mount_seal_removal_controls':controls,
 'unchanged_22_cell_region_material':differences,'rigid_release_sweeps':motions,
 'wall_gaps_with_alternative_spacers_mm':[3,4,5],'coarse_keepout_checks':checks,
 'limits':['Six and a half mm is the nominal bevel profile depth; 5 mm retained pose and 7 mm release path are separate rigid CAD checks.',
           'Anchor shaft, wall substrate and lower anti-lift/pads are absent from this motion model.',
           'All sweeps are for the represented rigid parts at nominal dimensions; tolerances, deformation, preload and strength remain unqualified.',
           'The capped cavity is an audit construction; caps are never production or CFD boundary conditions.',
           'Impermeable gasket CAD and preserved vent material do not establish air leakage or acoustic attenuation.'],
 'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in [source,old_path,ROOT/'evidence/rev-eq/execution.json',Path(__file__)]}}
(folder/'independent-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'controls':len(controls),'coarse_keepout_checks':len(checks)},indent=2))
