"""Flag predicted DML interference from the executed unconstrained LC3 screen.

The solver does not include DML contact. These are model-predicted positions,
not physically realizable panel penetration or a material failure prediction.
"""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
repo=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--mesh',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--revision',required=True);a=p.parse_args()
folder=a.run.resolve();mesh=a.mesh.resolve()
m=json.loads((folder/'metrics.json').read_text())
assert m['solver_execution_pass'] and m['final_step_time']==1
d=np.load(mesh/'mesh-data.npz');tags=d['tags'].astype(int);xyz=d['coords']
vectors={};active=False
for line in (folder/'frame.dat').read_text().splitlines():
    if 'displacements (vx,vy,vz) for set ALL' in line:active=True;vectors={};continue
    if active:
        cols=line.split()
        if len(cols)==4:
            try:vectors[int(cols[0])]=list(map(float,cols[1:]))
            except ValueError:active=False
        elif vectors:active=False
assert len(vectors)==len(tags)
u=np.array([vectors[n] for n in tags]);deformed=xyz+u
def inside(v):return (v[:,0]>10)&(v[:,0]<310)&(v[:,1]>10)&(v[:,1]<390)&(v[:,2]>3.3)&(v[:,2]<9.3)
before=inside(xyz);after=inside(deformed)
assert before.sum()==0
forward=((deformed[:,0]>10)&(deformed[:,0]<310)&(deformed[:,1]>10)&(deformed[:,1]<390)&(deformed[:,2]<3.3))
imax=int(np.linalg.norm(u,axis=1).argmax())
r={'classification':'CALCULATED_COLLISION_SCREEN_OF_SIMULATED_UNCONSTRAINED_DISPLACEMENTS',
   'status':'FAIL_PREDICTED_DML_INTERFERENCE' if after.any() or forward.any() else 'NO_SAMPLED_NODE_INTERFERENCE',
   'load_case':a.revision+' LC3 50 N outward; normalized MAT-B and surrogate supports',
   'nodes_initially_inside_DML':int(before.sum()),'nodes_predicted_inside_DML':int(after.sum()),
   'nodes_predicted_frontward_of_DML_within_projection':int(forward.sum()),
   'max_displacement_node':int(tags[imax]),'max_node_original_xyz_mm':xyz[imax].tolist(),
   'max_node_displacement_xyz_mm':u[imax].tolist(),'max_node_predicted_xyz_mm':deformed[imax].tolist(),
   'sample_predicted_DML_nodes':[{'node':int(tags[i]),'xyz_mm':deformed[i].tolist()} for i in np.flatnonzero(after)[:10]],
   'source_sha256':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [folder/'frame.dat',folder/'metrics.json',mesh/'mesh-data.npz',Path(__file__)]},
   'limits':['DML contact is absent from this screening FEA; post-contact response is not a physical displacement prediction.',
             'No impact, panel strength, allowable load, contact onset load, or material failure margin is inferred.',
             'Node membership detects interference but is not a complete deformed-element intersection algorithm. A detected collision is sufficient to reject this clearance screen.',
             'The true assembly/contact/load distribution and deformed elements need validation even if no sampled node intersects.']}
(folder/'deformed-clearance.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
