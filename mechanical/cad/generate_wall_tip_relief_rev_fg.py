"""Replace the wall-cleat tip fillet by an explicit machined flat relief.

The frame and all other parts are copied byte-for-byte, so their mesh and
frame-only simulations retain exact geometry provenance. This does not qualify
wall-cleat stress or an anchor substrate.
"""
import hashlib,json,math,shutil
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[2]
parent=ROOT/'evidence/rev-fg/upper-mounts-deep';out=ROOT/'evidence/rev-fg/upper-mounts-chamfer';out.mkdir(exist_ok=True)
(out/'execution.json').unlink(missing_ok=True)
source=parent/'execution.json';report=json.loads(source.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for path,h in report['source_sha256'].items():assert sha(ROOT/path)==h,path
parts={}
for n,a in report['artifacts'].items():
    original=ROOT/a['file'];assert sha(original)==a['sha256']
    dest=out/original.name;shutil.copyfile(original,dest);a['file']=str(dest.relative_to(ROOT))
    parts[n]=cq.importers.importStep(str(dest))
profile=report['wall_profile_YZ_mm'];assert profile[5]==[390.5,33.5]
relief=1.8
profile=profile[:5]+[[390.5-relief/math.sqrt(2),33.5+relief/math.sqrt(2)],[390.5-relief,33.5]]+profile[6:]
report['wall_profile_YZ_mm']=profile
report['wall_tip_relief_mm_along_each_adjacent_edge']=relief
report['wall_tip_relief_requires_edge_and_contact_stress_validation']=True
for side,x0 in [('L',27.5),('R',242.5)]:
    wall=cq.Workplane('YZ').polyline(profile).close().extrude(50).translate((x0,0,0))
    for x in [x0+10,x0+40]:
        bore=cq.Workplane('XY').center(x,375).circle(2.25).extrude(2.7).translate((0,0,40.4))
        wall=wall.cut(bore).cut(parts[f'WALL_HEAD_{side}_{x:g}_SPACE_ENVELOPE'])
    assert wall.val().isValid() and wall.solids().size()==1
    for n,p in parts.items():
        if n.startswith('WALL_CLEAT'):continue
        assert abs(wall.intersect(p).val().Volume())<1e-5,(side,n)
    name='WALL_CLEAT_'+side;f=ROOT/report['artifacts'][name]['file'];cq.exporters.export(wall,str(f))
    back=cq.importers.importStep(str(f));assert back.val().isValid() and back.solids().size()==1
    error=abs(back.val().Volume()-wall.val().Volume())/wall.val().Volume();assert error<1e-6
    report['artifacts'][name].update(sha256=sha(f),bytes=f.stat().st_size,volume_mm3=wall.val().Volume(),STEP_relative_volume_error=error)
    product=parts['PRODUCT_CLEAT_'+side]
    checks=[]
    for label,dy,dz in [('downward',-.1,0),('outward',0,-.1),('release_up',7,0),('retained_after_5mm_lift',5,-5.5)]:
        v=abs(product.translate((0,dy,dz)).intersect(wall).val().Volume())
        assert v>1e-4 if label!='release_up' else v<1e-6,(side,label,v)
        checks.append(dict(motion=label,dY_mm=dy,dZ_mm=dz,interference_mm3=v))
    report['rigid_engagement'][0 if side=='L' else 1]={'side':side,'rigid_motion_tests':checks}
shutil.copyfile(parent/'frame-geometry.json',out/'frame-geometry.json')
report['source_sha256'].update({str(p.relative_to(ROOT)):sha(p) for p in [source,Path(__file__),ROOT/'evidence/rev-fg/sources/pts-A79910410.html']})
report['frame_and_other_parts_changed']=False
report['status']='PASS_SCOPED_CAD_PENDING_CONTINUOUS_ASSEMBLY_MOTION_AUDIT'
(out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'rigid_engagement':report['rigid_engagement']},indent=2))
