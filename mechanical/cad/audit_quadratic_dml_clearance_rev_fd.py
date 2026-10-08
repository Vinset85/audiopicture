"""Conservative full-element bounds for the final quadratic FEA displacement.

A degree-two tetrahedron lies inside the convex hull of its Bernstein control
points: barycentric Bernstein basis functions are nonnegative and sum to one.
Disjoint enclosing boxes prove separation for the entire mapped element.
Overlapping boxes are inconclusive, never automatically called a collision.
This audits the FEA geometry at final load, not the exact deformed CAD/assembly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import gmsh
import numpy as np

p = argparse.ArgumentParser()
p.add_argument('--mesh', type=Path, required=True)
p.add_argument('--run', type=Path, required=True)
a = p.parse_args()
repo = Path(__file__).resolve().parents[2]
mesh, run = a.mesh.resolve(), a.run.resolve()
metrics = json.loads((run/'metrics.json').read_text())
assert metrics['solver_execution_pass'] and metrics['final_step_time'] == 1
data = np.load(mesh/'mesh-data.npz')
tags, xyz = data['tags'].astype(int), data['coords']
index = {int(n): i for i, n in enumerate(tags)}

# Discover the Gmsh ordering used by mesh-data.npz rather than assuming that
# the exported Abaqus/CalculiX connectivity has the same last two edge nodes.
gmsh.initialize()
name, dim, order, count, local, primary = gmsh.model.mesh.getElementProperties(11)
gmsh.finalize()
assert dim == 3 and order == 2 and count == 10 and primary == 4
local = np.asarray(local).reshape(10,3)
bary = np.column_stack([1-local.sum(axis=1), local])
assert np.allclose(bary[:4], np.eye(4), atol=1e-14)
edges = []
for row in bary[4:]:
    pair = np.flatnonzero(abs(row-.5) < 1e-14)
    assert len(pair) == 2 and np.allclose(row.sum(),1)
    edges.append(tuple(int(i) for i in pair))
assert len(set(tuple(sorted(e)) for e in edges)) == 6

def controls(nodes):
    result = nodes.copy()
    for k,(i,j) in enumerate(edges, 4):
        result[:,k] = 2*nodes[:,k] - .5*(nodes[:,i]+nodes[:,j])
    return result

def evaluate(nodes, L):
    weights = np.concatenate([L*(2*L-1), np.array([4*L[i]*L[j] for i,j in edges])])
    return np.einsum('enk,n->ek', nodes, weights)

# A curved scalar coordinate can exceed all nodal values. This case would be
# missed by a node-only exclusion test and must remain flagged by our bound.
test = np.zeros((1,10,3)); test[0,:,0] = -.01; test[0,1,0] = -1
assert test[:,:,0].max() < 0
assert evaluate(test,np.array([.75,.25,0,0]))[0,0] > 0
assert controls(test)[:,:,0].max() > 0
rng = np.random.default_rng(22020)
random_nodes = rng.normal(size=(32,10,3)); ctrl = controls(random_nodes)
for _ in range(64):
    L = rng.dirichlet(np.ones(4)); values = evaluate(random_nodes,L)
    assert np.all(values >= ctrl.min(axis=1)-1e-12)
    assert np.all(values <= ctrl.max(axis=1)+1e-12)

vectors = {}; active = False
for line in (run/'frame.dat').read_text().splitlines():
    if 'displacements (vx,vy,vz) for set ALL' in line:
        active=True; vectors={}; continue
    if active:
        cols=line.split()
        if len(cols)==4:
            try: vectors[int(cols[0])] = list(map(float,cols[1:]))
            except ValueError: active=False
        elif vectors: active=False
assert set(vectors) == set(tags)
U=np.asarray([vectors[int(t)] for t in tags])
conn=np.asarray([[index[int(n)] for n in e] for e in data['elements']])
assert conn.shape[1] == 10

def bound(nodes):
    ctrl=controls(nodes)
    # Inflation is a numerical guard only, not a manufacturing tolerance.
    lo,hi=ctrl.min(axis=1)-1e-7,ctrl.max(axis=1)+1e-7
    low=np.array([10,10,3.3]); high=np.array([310,390,9.3])
    distances=np.maximum(np.maximum(low-hi,lo-high),0)
    distance=np.linalg.norm(distances,axis=1)
    xy=(hi[:,0]>=10)&(lo[:,0]<=310)&(hi[:,1]>=10)&(lo[:,1]<=390)
    front=xy&(lo[:,2]<=3.3)
    unresolved=(distance==0)|front
    return {'elements':len(nodes),
            'potential_DML_box_overlap_elements':int((distance==0).sum()),
            'potential_frontward_within_DML_projection_elements':int(front.sum()),
            'all_element_bounds_separated_from_DML_and_frontward_region':not bool(unresolved.any()),
            'conservative_DML_separation_lower_bound_mm':float(distance.min()),
            'unresolved_element_tags_sample':data['element_tags'][unresolved][:20].astype(int).tolist()}

before=bound(xyz[conn]); after=bound((xyz+U)[conn])
report={'classification':'CALCULATED_CONSERVATIVE_FULL_QUADRATIC_ELEMENT_BOUND_ON_SIMULATED_FINAL_STATE',
        'status':'PASS_SCOPED_FEA_GEOMETRY_SEPARATION' if after['all_element_bounds_separated_from_DML_and_frontward_region'] else 'OPEN_OVERLAPPING_BOUNDS_REQUIRE_REFINEMENT',
        'method':'Quadratic tetrahedral Bernstein control-point convex enclosure; enclosing AABBs inflated 1e-7 mm. Overlap is inconclusive.',
        'gmsh_edge_node_pairs_zero_based':edges,
        'self_checks':{'curved_node_only_false_negative_detected':True,'random_elements':32,'barycentric_samples_each':64},
        'initial':before,'final':after,
        'limits':['Final load state only; not all intermediate states.',
                  'FEA interpolation geometry only; not exact deformed BREP, manufacturing tolerance or real assembly qualification.',
                  'DML is the fixed nominal hard box, not a deformable contact body.',
                  'No physical clearance is certified from unqualified material/support assumptions.'],
        'source_sha256':{str(f.relative_to(repo)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),mesh/'mesh-data.npz',run/'frame.dat',run/'metrics.json']}}
(run/'quadratic-dml-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
