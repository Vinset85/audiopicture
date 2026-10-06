"""Quadratic tetra mesh, independent cleat bores and volume-based load weights.
See ../digital-validation-rev-et-ey.md for boundary/material scope and limits.
"""
import argparse,json,hashlib
from pathlib import Path
import gmsh,numpy as np
p=argparse.ArgumentParser();p.add_argument('--step',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--size',type=float,default=4);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
gmsh.initialize();gmsh.model.add('frame_rev_eu');gmsh.model.occ.importShapes(str(a.step));gmsh.model.occ.synchronize()
vols=gmsh.model.getEntities(3);assert len(vols)==1
g=gmsh.model.addPhysicalGroup(3,[t for d,t in vols]);gmsh.model.setPhysicalName(3,g,'EALL')
gmsh.option.setNumber('Mesh.MeshSizeMin',min(1.,a.size/3));gmsh.option.setNumber('Mesh.MeshSizeMax',a.size);gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',16)
for d,t in gmsh.model.getEntities(0):
 x,y,z=gmsh.model.getValue(0,t,[])
 if 367<=y<=384 and any(abs(x-c)<7 for c in [37.5,67.5,252.5,282.5]):gmsh.model.mesh.setSize([(d,t)],min(1.5,a.size/2))
gmsh.model.mesh.generate(3);gmsh.model.mesh.setOrder(2);gmsh.model.mesh.optimize('HighOrder')
tags,c,_=gmsh.model.mesh.getNodes();c=np.asarray(c).reshape(-1,3);index={int(t):i for i,t in enumerate(tags)};sets={}
for name,x in [('UL1',37.5),('UL2',67.5),('UR1',252.5),('UR2',282.5)]:
 sel=(abs(np.hypot(c[:,0]-x,c[:,1]-375)-3)<1e-5)&(c[:,2]>=28-1e-7)&(c[:,2]<=35+1e-7);sets[name]=tags[sel].astype(int).tolist();assert len(sets[name])>=10
for name,x in [('PAD_L',45),('PAD_R',275)]:
 sel=(abs(c[:,2]-35)<1e-6)&(abs(c[:,0]-x)<9.001)&(c[:,1]>21.999)&(c[:,1]<34.001);sets[name]=tags[sel].astype(int).tolist();assert sets[name]
sets['ANTILIFT']=tags[(abs(c[:,2]-35)<1e-6)&(abs(c[:,0]-160)<9.001)&(c[:,1]>=10)&(c[:,1]<=20)].astype(int).tolist()
for name,x,y in [('CORNER_LL',7,7),('CORNER_LR',313,7),('CORNER_UL',7,393),('CORNER_UR',313,393)]:
 sets[name]=tags[(abs(c[:,0]-x)<=5.001)&(abs(c[:,1]-y)<=5.001)&(abs(c[:,2]-35)<1e-6)].astype(int).tolist();assert sets[name]
types,els,conn=gmsh.model.mesh.getElements(3);assert list(types)==[11]
etags=els[0];elems=np.asarray(conn[0]).reshape(-1,10);coords=c[np.array([[index[int(t)] for t in e[:4]] for e in elems])]
v=np.abs(np.linalg.det(coords[:,1:]-coords[:,:1]))/6
weight=np.zeros(len(tags))
for e,ev in zip(elems,v):
 for n in e:weight[index[int(n)]]+=ev/10
weights=weight/weight.sum();quality=gmsh.model.mesh.getElementQualities(etags,'minSICN');assert min(quality)>0
gmsh.write(str(a.out/'mesh.inp'));gmsh.write(str(a.out/'mesh.msh'))
np.savez_compressed(a.out/'mesh-data.npz',tags=tags,coords=c,elements=elems,element_tags=etags,element_volumes=v,weights=weights)
(a.out/'sets.json').write_text(json.dumps(sets))
report={'source_sha256':hashlib.sha256(a.step.read_bytes()).hexdigest(),'size_mm':a.size,'nodes':len(tags),'elements':len(etags),'type':'C3D10','min_SICN':float(min(quality)),'corner_tet_volume_mm3':float(v.sum()),'volume_weighted_seed_cg_mm':(weights@c).tolist(),'node_sets':{k:len(v) for k,v in sets.items()},'load_scope':'volume-lumped structural-body load, not actual assembled product mass distribution'}
(a.out/'mesh-report.json').write_text(json.dumps(report,indent=2));gmsh.finalize();print(json.dumps(report,indent=2))
