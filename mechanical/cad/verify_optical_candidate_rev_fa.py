"""Reimport candidate artifacts independently; no regeneration of geometry."""
import argparse, hashlib, json
from pathlib import Path
import cadquery as cq
import trimesh

p=argparse.ArgumentParser();p.add_argument('--evidence',required=True,type=Path);a=p.parse_args()
r=json.loads((a.evidence/'execution.json').read_text());step_checks=[];stl_checks=[]
for name,entry in r['exports'].items():
    path=a.evidence/entry['step'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
    part=cq.importers.importStep(str(path));v=sum(s.Volume() for s in part.solids().vals())
    assert part.val().isValid() and part.solids().size()==1
    assert abs(v-entry['volume_mm3'])<1e-6
    step_checks.append({'part':name,'valid':True,'solid_count':1,'volume_mm3':v})
    if 'stl' not in entry:continue
    path=a.evidence/entry['stl'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['stl_sha256']
    mesh=trimesh.load_mesh(path,process=True)
    q={'file':path.name,'watertight':bool(mesh.is_watertight),
       'winding_consistent':bool(mesh.is_winding_consistent),'body_count':int(mesh.body_count),
       'vertices':len(mesh.vertices),'faces':len(mesh.faces),'mesh_volume_mm3':float(mesh.volume),
       'relative_volume_difference_percent':abs(float(mesh.volume)-v)/v*100,
       'sha256':entry['stl_sha256']}
    assert q['watertight'] and q['winding_consistent'] and q['body_count']==1
    stl_checks.append(q)
assert sum(v['rays'] for v in r['angular_sweep'] if v['polar_deg']<=35)==1953
assert sum(v['blocked_by_carrier'] for v in r['angular_sweep'] if v['polar_deg']<=35)==0
assert len(r['independent_OCC_rays'])==153
assert all(v['DML_intersection_mm']<1e-7 for v in r['independent_OCC_rays'])
(a.evidence/'stl-check.json').write_text(json.dumps(stl_checks,indent=2)+'\n')
result={'classification':'INDEPENDENT_ARTIFACT_REIMPORT_AND_CHECKSUM_CHECK',
        'status':'PASS_SCOPE_ONLY','STEP':step_checks,'STL':stl_checks,
        'execution_sha256':hashlib.sha256((a.evidence/'execution.json').read_bytes()).hexdigest(),
        'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'manufacturing_release':False}
(a.evidence/'independent-artifact-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
