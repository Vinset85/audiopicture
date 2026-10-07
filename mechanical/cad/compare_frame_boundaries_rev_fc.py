"""Compare sampled load/support coordinates without reclassifying physical BCs."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from scipy.spatial import cKDTree
p=argparse.ArgumentParser();p.add_argument('--baseline',type=int,required=True);p.add_argument('--candidate',type=int,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True)
models={};sources=[Path(__file__)]
for revision in [a.baseline,a.candidate]:
 root=Path(f'evidence/rev-ev{revision}/M0');data=np.load(root/'mesh-data.npz');xyz=data['coords'];tags=data['tags'];idx={int(n):i for i,n in enumerate(tags)};sets=json.loads((root/'sets.json').read_text())
 models[revision]={name:sorted(tuple(float(x) for x in np.round(xyz[idx[n]],8)) for n in ns) for name,ns in sets.items()};sources.extend([root/'mesh-data.npz',root/'sets.json'])
comparison={name:{'baseline_nodes':len(points),'candidate_nodes':len(models[a.candidate][name]),'coordinates_identical_to_1e_minus8_mm':points==models[a.candidate][name]} for name,points in models[a.baseline].items()}
for name,row in comparison.items():
 left=np.array(models[a.baseline][name]);right=np.array(models[a.candidate][name]);distance=max(float(cKDTree(left).query(right)[0].max()),float(cKDTree(right).query(left)[0].max()));row['symmetric_nearest_node_distance_mm']=distance
result={'classification':'CALCULATED_BOUNDARY_NODE_COMPARISON','models':[f'EU.{a.baseline}',f'EU.{a.candidate}'],'comparison':comparison,'all_sets_match':all(x['coordinates_identical_to_1e_minus8_mm'] for x in comparison.values()),'note':'Checks unchanged mesh boundary/load sampling, not validity of physical support assumptions.','sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
