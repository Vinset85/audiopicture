"""Gmsh C3D10 M1D debug deck, not LC1-LC7 or material release.

Material seed explicitly permitted by material-evidence Rev.L.
Remote cut faces fixed; 5 N normal load distributed over front tab nodes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import gmsh
import numpy as np

p=argparse.ArgumentParser()
p.add_argument('--step',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--size',type=float,required=True)
p.add_argument('--nu',type=float,default=.35)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
gmsh.initialize()
gmsh.model.add('M1D_debug')
volumes=gmsh.model.occ.importShapes(str(a.step))
gmsh.model.occ.synchronize()
assert len(gmsh.model.getEntities(3))==1
g=gmsh.model.addPhysicalGroup(3,[t for d,t in volumes if d==3])
gmsh.model.setPhysicalName(3,g,'EALL')
gmsh.option.setNumber('Mesh.MeshSizeMin',a.size/2)
gmsh.option.setNumber('Mesh.MeshSizeMax',a.size)
gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',12)
gmsh.option.setNumber('Mesh.Algorithm3D',1)
gmsh.model.mesh.generate(3)
gmsh.model.mesh.setOrder(2)
gmsh.model.mesh.optimize('HighOrder')
tags,coords,_=gmsh.model.mesh.getNodes()
coords=np.asarray(coords).reshape(-1,3)
fixed=[int(t) for t,c in zip(tags,coords) if abs(c[0]-30)<1e-6 or abs(c[0]-110)<1e-6]
target=[int(t) for t,c in zip(tags,coords) if abs(c[2]-5.1)<1e-6]
assert fixed and target
_,element_tags,_=gmsh.model.mesh.getElements(3)
elements=np.concatenate(element_tags)
quality=gmsh.model.mesh.getElementQualities(elements,'minSICN')
assert min(quality)>0
mesh=a.out/'mesh.inp'
gmsh.write(str(mesh))
gmsh.write(str(a.out/'mesh.msh'))
text=mesh.read_text()
assert '*ELSET,ELSET=EALL' in text.upper().replace(' ','')
def nset(name,nodes):
    return '*NSET,NSET='+name+'\n'+'\n'.join(','.join(str(n) for n in nodes[i:i+16]) for i in range(0,len(nodes),16))+'\n'
deck=text+nset('FIXED',fixed)+nset('TARGET',target)
deck+='*MATERIAL,NAME=PC_CF_ISOTROPIC_DEBUG\n*ELASTIC\n1900,'+str(a.nu)+'\n'
deck+='*SOLID SECTION,ELSET=EALL,MATERIAL=PC_CF_ISOTROPIC_DEBUG\n'
deck+='*BOUNDARY\nFIXED,1,3,0\n*STEP\n*STATIC,SOLVER=ITERATIVE CHOLESKY\n*CLOAD\n'
deck+=''.join(f'{n},3,{-5/len(target):.12g}\n' for n in target)
deck+='*NODE PRINT,NSET=TARGET\nU\n*NODE PRINT,NSET=FIXED,TOTALS=YES\nRF\n*EL PRINT,ELSET=EALL\nS\n*NODE FILE\nU,RF\n*EL FILE\nS\n*END STEP\n'
(a.out/'screen.inp').write_text(deck)
result={'classification':'ISOTROPIC_LOCAL_DEBUG_NOT_RELEASE_NOT_LC1_LC7',
        'gmsh_version':gmsh.__version__,'mesh_size_mm':a.size,'node_count':len(tags),
        'element_count':len(elements),'element_type':'C3D10',
        'min_SICN':float(min(quality)),'fixed_nodes':len(fixed),'target_nodes':len(target),
        'load_N':5,'applied_load_sum_N':-5.,'E_MPa':1900,'nu_assumption':a.nu,
        'source_sha256':hashlib.sha256(a.step.read_bytes()).hexdigest(),
        'limitations':['Nodal equal-force distribution is a debug load abstraction.',
                       'Remote fixed cut faces are local boundary assumption.',
                       'No orthotropic/temperature/contact/strength release claim.']}
(a.out/'mesh-report.json').write_text(json.dumps(result,indent=2)+'\n')
gmsh.finalize()
print(json.dumps(result,indent=2))
