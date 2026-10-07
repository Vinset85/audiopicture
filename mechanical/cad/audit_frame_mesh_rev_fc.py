"""Audit quadratic element Jacobians and identify poor-quality regions.

Positive Jacobians are necessary; they do not establish mesh convergence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import gmsh
import numpy as np

p = argparse.ArgumentParser()
p.add_argument('--mesh', type=Path, required=True)
a = p.parse_args()
gmsh.initialize()
gmsh.open(str(a.mesh / 'mesh.msh'))
d = np.load(a.mesh / 'mesh-data.npz')
tags = d['element_tags']
quality = np.asarray(gmsh.model.mesh.getElementQualities(tags, 'minSICN'))
jac = np.asarray(gmsh.model.mesh.getElementQualities(tags, 'minDetJac'))
index = {int(t): i for i, t in enumerate(d['tags'])}
coords = d['coords']
elements = d['elements']
worst = np.argsort(quality)[:10]
r = {
    'classification': 'CALCULATED_MESH_INTEGRITY_NOT_CONVERGENCE',
    'elements': len(tags), 'min_SICN': float(quality.min()),
    'min_adaptive_Jacobian_determinant_mm3': float(jac.min()),
    'nonpositive_Jacobian_elements': int((jac <= 0).sum()),
    'SICN_below_0p01_count': int((quality < .01).sum()),
    'SICN_percentiles': dict(zip(['0', '1', '5', '50', '100'], np.percentile(quality, [0, 1, 5, 50, 100]).tolist())),
    'worst_elements': [
        {'element': int(tags[i]), 'SICN': float(quality[i]),
         'min_Jacobian_mm3': float(jac[i]),
         'corner_centroid_xyz_mm': np.mean([coords[index[int(n)]] for n in elements[i][:4]], axis=0).tolist()}
        for i in worst
    ],
    'mesh_convergence_verified': False,
    'source_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in [a.mesh / 'mesh.msh', a.mesh / 'mesh-data.npz', Path(__file__)]},
}
gmsh.finalize()
(a.mesh / 'quality-audit.json').write_text(json.dumps(r, indent=2) + '\n')
print(json.dumps(r, indent=2))
assert r['nonpositive_Jacobian_elements'] == 0
