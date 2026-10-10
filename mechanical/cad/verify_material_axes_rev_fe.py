"""Independent analytic versus executed CCX cube test of three print axes.

Uniform stress traction on a unit C3D8 cube, minimal rigid-body constraints.
Nine axial and nine shear cases check both modulus and orientation mapping.
This verifies numerical implementation only, never printed material properties.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import numpy as np

p=argparse.ArgumentParser();p.add_argument('--ccx',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
coords=np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]],dtype=float)
axes={'Z':[[1,0,0],[0,1,0],[0,0,1]],'X':[[0,1,0],[0,0,1],[1,0,0]],'Y':[[1,0,0],[0,0,-1],[0,1,0]]}
E=1900.;nu=.35;g=E/(2*(1+nu));es=np.array([E,E,.2*E]);gs=np.array([g,.25*g,.25*g])
rows=[]
for weak, basis in axes.items():
    R=np.array(basis).T
    assert np.allclose(R.T@R,np.eye(3)) and np.isclose(np.linalg.det(R),1)
    for kind,ij in [('axial',(0,0)),('axial',(1,1)),('axial',(2,2)),('shear',(0,1)),('shear',(0,2)),('shear',(1,2))]:
        stress=np.zeros((3,3));i,j=ij;stress[i,j]=stress[j,i]=1
        local=R.T@stress@R
        strain_local=np.zeros((3,3))
        # Reciprocal Poisson terms use the same 1/E cross compliances as the
        # material contract: nu12/E1=nu13/E1=nu23/E2=nu/1900.
        for k in range(3): strain_local[k,k]=local[k,k]/es[k]-sum(nu/E*local[l,l] for l in range(3) if l!=k)
        for (k,l),shear in zip([(0,1),(0,2),(1,2)],gs): strain_local[k,l]=strain_local[l,k]=local[k,l]/(2*shear)
        expected=R@strain_local@R.T
        loads=np.zeros((8,3))
        for normal_axis in range(3):
            for face_value,sign in [(0,-1),(1,1)]:
                ns=np.flatnonzero(coords[:,normal_axis]==face_value)
                loads[ns]+=sign*stress[:,normal_axis]/4
        assert np.allclose(loads.sum(axis=0),0)
        assert np.allclose(np.cross(coords,loads).sum(axis=0),0)
        name=f'{weak}-{kind}-'+''.join('XYZ'[v] for v in ij);folder=a.out/name;folder.mkdir(exist_ok=True)
        deck='*NODE,NSET=ALL\n'+''.join(f'{n+1},'+','.join(map(str,c))+'\n' for n,c in enumerate(coords))
        deck+='*ELEMENT,TYPE=C3D8,ELSET=EALL\n1,1,2,3,4,5,6,7,8\n'
        deck+='*ORIENTATION,NAME=PRINT_AXES,SYSTEM=RECTANGULAR\n'+','.join(map(str,basis[0]+basis[1]))+'\n'
        deck+='*MATERIAL,NAME=SEED\n*ELASTIC,TYPE=ENGINEERING CONSTANTS\n'+','.join(map(str,[*es,nu,nu,nu,gs[0],gs[1]]))+'\n'+str(gs[2])+'\n'
        deck+='*SOLID SECTION,ELSET=EALL,MATERIAL=SEED,ORIENTATION=PRINT_AXES\n'
        deck+='*BOUNDARY\n1,1,3,0\n2,2,3,0\n4,3,3,0\n*STEP\n*STATIC,SOLVER=SPOOLES\n*CLOAD\n'
        for n,load in enumerate(loads,1):
            for d,v in enumerate(load,1):
                if v: deck+=f'{n},{d},{v}\n'
        deck+='*NODE PRINT,NSET=ALL\nU,RF\n*END STEP\n'
        (folder/'cube.inp').write_text(deck)
        with (folder/'solver.log').open('w') as log:
            proc=subprocess.run([str(a.ccx.resolve()),'cube'],cwd=folder,stdout=log,stderr=subprocess.STDOUT,
                                env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'},timeout=60)
        log=(folder/'solver.log').read_text(); assert proc.returncode==0 and 'Job finished' in log and '*ERROR' not in log
        vectors={};active=False
        for line in (folder/'cube.dat').read_text().splitlines():
            if 'displacements (vx,vy,vz) for set ALL' in line:active=True;continue
            if active:
                parts=line.split()
                if len(parts)==4:
                    try:vectors[int(parts[0])]=list(map(float,parts[1:]))
                    except ValueError:active=False
                elif vectors:active=False
        assert len(vectors)==8
        U=np.array([vectors[n] for n in range(1,9)])
        # Affine gradient inferred from all eight solved nodes, not an imposed
        # displacement field. Symmetric part removes the rigid rotation gauge.
        fit=np.linalg.lstsq(np.column_stack([np.ones(8),coords]),U,rcond=None)[0]
        gradient=fit[1:].T;actual=(gradient+gradient.T)/2
        residual=float(np.max(abs(np.column_stack([np.ones(8),coords])@fit-U)))
        error=float(np.max(abs(actual-expected))/np.max(abs(expected)))
        assert error<2e-6 and residual<1e-8,(name,error,residual)
        rows.append({'name':name,'weak_global_axis':weak,'stress_global_MPa':stress.tolist(),
                     'expected_strain':expected.tolist(),'computed_strain':actual.tolist(),
                     'relative_max_strain_error':error,'affine_fit_residual_mm':residual,
                     'solver_exit_code':proc.returncode,'solver_finished':True,
                     'input_sha256':hashlib.sha256(deck.encode()).hexdigest()})
report={'classification':'SIMULATED_SOLVER_ORIENTATION_PATCH_TEST_NOT_MATERIAL_QUALIFICATION',
        'status':'PASS','cases':rows,'case_count':len(rows),'maximum_relative_strain_error':max(r['relative_max_strain_error'] for r in rows),
        'solver_sha256':hashlib.sha256(a.ccx.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(a.out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
