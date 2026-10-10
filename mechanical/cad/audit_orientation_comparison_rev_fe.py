"""Verify an orientation experiment changes no load, geometry or support."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--oriented',type=Path,required=True);a=p.parse_args()
repo=Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
left=(a.baseline/'frame.inp').read_text(); right=(a.oriented/'frame.inp').read_text()
match=re.search(r'^\*ORIENTATION,NAME=PRINT_AXES,SYSTEM=RECTANGULAR\n([^\n]+)\n',right,re.M)
assert match
values=np.array(list(map(float,match[1].split(',')))).reshape(2,3)
stripped=right[:match.start()]+right[match.end():]
stripped=stripped.replace(',ORIENTATION=PRINT_AXES','')
assert stripped==left, 'Changes beyond material orientation detected'
l=json.loads((a.baseline/'execution.json').read_text());r=json.loads((a.oriented/'execution.json').read_text())
assert l['input_sha256']==sha(a.baseline/'frame.inp') and r['input_sha256']==sha(a.oriented/'frame.inp')
for key in ['constitutive_assumptions','load_sum_N','mesh_report','lower_unilateral_gap_contacts',
            'anti_lift_normal_support_assumption','bonded_insert_cleat_surrogate_nodes','loaded_corner']:
    assert l[key]==r[key],key
axes=np.array(r['material_axes_global']);assert np.array_equal(values,axes[:2])
assert np.allclose(np.cross(axes[0],axes[1]),axes[2]) and np.isclose(np.linalg.det(axes),1)
check=repo/'evidence/rev-fe/material-axes-check/verification.json'
q=json.loads(check.read_text());assert q['status']=='PASS' and q['case_count']==18
paths=[a.baseline/'frame.inp',a.baseline/'execution.json',a.oriented/'frame.inp',a.oriented/'execution.json',check,Path(__file__)]
result={'classification':'CALCULATED_CONTROLLED_EXPERIMENT_AUDIT','status':'PASS',
        'only_changed_input':'Material orientation card and its solid-section reference',
        'weak_global_axis':r['weak_global_axis'],'material_axes_global':r['material_axes_global'],
        'identical_geometry_loads_contacts_constraints_and_material_values':True,
        'physical_print_orientation_qualified':False,
        'source_sha256':{str(x.resolve().relative_to(repo)):sha(x) for x in paths}}
(a.oriented/'orientation-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
