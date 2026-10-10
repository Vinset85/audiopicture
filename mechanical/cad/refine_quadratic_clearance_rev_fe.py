"""Subdivide quadratic tetrahedra to resolve conservative DML-bound overlaps.

An overlap alone stays OPEN. An evaluated interior point in the forbidden
region is a model-interference witness. Disjoint Bernstein boxes prove only
the final interpolated FEA geometry, not real assembly clearance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import gmsh
import numpy as np

p=argparse.ArgumentParser();p.add_argument('--mesh',type=Path,required=True)
p.add_argument('--run',type=Path,required=True);p.add_argument('--max-depth',type=int,default=8)
a=p.parse_args();repo=Path(__file__).resolve().parents[2];mesh=a.mesh.resolve();run=a.run.resolve()
old=json.loads((run/'quadratic-dml-clearance.json').read_text())
assert old['classification']=='CALCULATED_CONSERVATIVE_FULL_QUADRATIC_ELEMENT_BOUND_ON_SIMULATED_FINAL_STATE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for source,digest in old['source_sha256'].items():assert sha(repo/source)==digest
data=np.load(mesh/'mesh-data.npz');tags=data['tags'].astype(int);xyz=data['coords']
index={int(n):i for i,n in enumerate(tags)}
gmsh.initialize();_,dim,order,n,local,primary=gmsh.model.mesh.getElementProperties(11);gmsh.finalize()
assert (dim,order,n,primary)==(3,2,10,4)
local=np.asarray(local).reshape(10,3);Lnodes=np.column_stack([1-local.sum(axis=1),local])
assert np.allclose(Lnodes[:4],np.eye(4))
edges=[tuple(np.flatnonzero(abs(row-.5)<1e-14)) for row in Lnodes[4:]]
def weights(L):return np.column_stack([L*(2*L-1),np.array([4*L[:,i]*L[:,j] for i,j in edges]).T])
def evaluate(nodes,L):return weights(L)@nodes
def controls(nodes):
 c=nodes.copy()
 for k,(i,j) in enumerate(edges,4):c[k]=2*nodes[k]-.5*(nodes[i]+nodes[j])
 return c
v=np.eye(4);m01=(v[0]+v[1])/2;m02=(v[0]+v[2])/2;m03=(v[0]+v[3])/2
m12=(v[1]+v[2])/2;m13=(v[1]+v[3])/2;m23=(v[2]+v[3])/2
children=np.array([[v[0],m01,m02,m03],[m01,v[1],m12,m13],[m02,m12,v[2],m23],
 [m03,m13,m23,v[3]],[m01,m02,m03,m23],[m01,m02,m12,m23],
 [m01,m12,m13,m23],[m01,m03,m13,m23]])
volumes=np.array([abs(np.linalg.det((c[1:,1:]-c[0,1:]).T)) for c in children])
assert np.allclose(volumes,1/8) and np.isclose(volumes.sum(),1)
rng=np.random.default_rng(20261009);points=rng.dirichlet(np.ones(4),size=512)
memberships=np.array([(points@np.linalg.inv(c)>=-1e-12).all(axis=1) for c in children]).sum(axis=0)
assert (memberships==1).all()
test=rng.normal(size=(10,3));error=0.
for child in children:
 sub=evaluate(test,Lnodes@child)
 error=max(error,float(abs(evaluate(sub,points)-evaluate(test,points@child)).max()))
assert error<1e-12
vectors={};active=False
for line in (run/'frame.dat').read_text().splitlines():
 if 'displacements (vx,vy,vz) for set ALL' in line:active=True;vectors={};continue
 if active:
  fields=line.split()
  if len(fields)==4:
   try:vectors[int(fields[0])]=list(map(float,fields[1:]))
   except ValueError:active=False
  elif vectors:active=False
assert set(vectors)==set(tags)
deformed=xyz+np.array([vectors[int(n)] for n in tags])
conn=np.asarray([[index[int(n)] for n in e] for e in data['elements']])
guard=1e-7;tested=0;deepest=0;unresolved=[];witnesses=[];lower=float('inf');refined_elements=0
def gap(nodes):
 c=controls(nodes);lo=c.min(axis=0)-guard;hi=c.max(axis=0)+guard
 # Union of DML box and the region forward of it within its XY projection.
 ds=np.array([max(10-hi[0],lo[0]-310,0),max(10-hi[1],lo[1]-390,0),max(lo[2]-9.3,0)])
 return float(np.linalg.norm(ds))
for tag,indices in zip(data['element_tags'],conn):
 nodes=deformed[indices];original_nodes=nodes.copy();initial_gap=gap(nodes)
 if initial_gap>0:lower=min(lower,initial_gap);continue
 refined_elements+=1;stack=[(nodes,0,np.eye(4))]
 while stack:
  nodes,depth,reference=stack.pop();tested+=1;deepest=max(deepest,depth)
  g=gap(nodes)
  if g>0:lower=min(lower,g);continue
  center=evaluate(nodes,np.full((1,4),.25))[0]
  if 10+guard<center[0]<310-guard and 10+guard<center[1]<390-guard and center[2]<9.3-guard:
   parent_L=np.full(4,.25)@reference
   assert abs(evaluate(original_nodes,parent_L[None,:])[0]-center).max()<1e-11
   margin=float(min(center[0]-10,310-center[0],center[1]-10,390-center[1],9.3-center[2]))
   witnesses.append({'element_tag':int(tag),'xyz_mm':center.tolist(),
                     'parent_barycentric_coordinates':parent_L.tolist(),
                     'forbidden_region_boundary_margin_mm':margin,
                     'inside_DML_box':bool(center[2]>3.3+guard),'depth':depth})
   break
  if depth==a.max_depth or tested>200000:
   unresolved.append({'element_tag':int(tag),'depth':depth});continue
  stack.extend((evaluate(nodes,Lnodes@c),depth+1,c@reference) for c in children)
robust=[w for w in witnesses if w['forbidden_region_boundary_margin_mm']>1e-4]
status='FAIL_WITNESSED_MODEL_INTERFERENCE' if robust else ('OPEN_UNRESOLVED_BOUNDS' if unresolved or witnesses else 'PASS_SCOPED_SUBDIVIDED_FEA_SEPARATION')
report={'classification':'CALCULATED_SUBDIVIDED_BERNSTEIN_BOUND_ON_SIMULATED_FINAL_STATE',
 'status':status,'elements':len(conn),'elements_requiring_refinement':refined_elements,
 'subdomains_examined':tested,'maximum_depth_reached':deepest,'maximum_depth_allowed':a.max_depth,
 'numerical_guard_mm':guard,'witness_count':len(witnesses),'witnesses':witnesses,
 'witnesses_beyond_0p0001_mm_numerical_margin':len(robust),
 'largest_witness_boundary_margin_mm':max((w['forbidden_region_boundary_margin_mm'] for w in witnesses),default=0.),
 'unresolved_subdomains':len(unresolved),'unresolved_examples':unresolved[:20],
 'separation_lower_bound_mm':lower if not witnesses and not unresolved else 0.,
 'self_checks':{'eight_equal_volume_subtetrahedra':True,'reference_partition_samples':512,
                'quadratic_subdivision_max_reconstruction_error':error},
 'limits':['Final interpolated FEA geometry only; fixed DML box and its forward XY projection.',
           '0.0001 mm witness margin is a numerical guard against output rounding, not a production tolerance.',
           'No real DML contact, tolerance, measured material or hardware qualification.',
           'A witness rejects the clearance screen; an overlapping bound alone stays OPEN.'],
 'source_sha256':{str(p.relative_to(repo)):sha(p) for p in [Path(__file__),mesh/'mesh-data.npz',run/'frame.dat',run/'quadratic-dml-clearance.json']}}
(run/'refined-quadratic-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['witnesses','source_sha256']},indent=2))
