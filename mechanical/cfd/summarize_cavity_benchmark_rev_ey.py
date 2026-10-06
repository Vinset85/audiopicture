import argparse,json
from pathlib import Path
import vtk,numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from scipy.integrate import simpson
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();results=[]
for path in sorted(a.root.glob('N*'),key=lambda p:int(p.name[1:])):
 if not (path/'execution.json').exists():continue
 ex=json.loads((path/'execution.json').read_text());n=ex['n'];last=sorted((path/'square').glob('*.vtu'))[-1]
 rd=vtk.vtkXMLUnstructuredGridReader();rd.SetFileName(str(last));rd.Update();grid=rd.GetOutput();points=vtk_to_numpy(grid.GetPoints().GetData());temp=vtk_to_numpy(grid.GetPointData().GetArray('temperature'));vel=vtk_to_numpy(grid.GetPointData().GetArray('velocity'))
 assert len(points)==(n+1)**2
 T=np.zeros((n+1,n+1));U=np.zeros((n+1,n+1,3));indices=np.rint(points[:,:2]*n).astype(int)
 for i,(x,y) in enumerate(indices):T[y,x]=temp[i];U[y,x]=vel[i]
 assert np.max(abs(T[:,0]-300.5))<1e-8 and np.max(abs(T[:,-1]-299.5))<1e-8
 y=np.linspace(0,1,n+1)
 hot=(3*T[:,0]-4*T[:,1]+T[:,2])*n/2
 cold=(-3*T[:,-1]+4*T[:,-2]-T[:,-3])*n/2
 nuh=float(simpson(hot,x=y));nuc=float(simpson(cold,x=y));u=float(abs(U[:,n//2,0]).max());v=float(abs(U[n//2,:,1]).max())
 r={'n':n,'solver_execution':ex,'vtu_last':str(last.relative_to(a.root)),'Nu_hot':nuh,'Nu_cold':nuc,'reference_Nu':1.118,'relative_Nu_error_percent':abs(nuh/1.118-1)*100,'hot_cold_balance_percent':abs(nuh-nuc)/((abs(nuh)+abs(nuc))/2)*100,'centerline_abs_u_max':u,'centerline_abs_v_max':v,'reference_u_max':3.649,'reference_v_max':3.697,'flux_evaluation':'second-order one-sided boundary derivative and Simpson integration of nodal temperature; not a component-temperature model','classification':'SIMULATED_BOUSSINESQ_REFERENCE_NOT_PRODUCT_CFD'}
 results.append(r)
for i,r in enumerate(results):
 if i:r['previous_mesh_Nu_change_percent']=abs(r['Nu_hot']-results[i-1]['Nu_hot'])/abs(r['Nu_hot'])*100
(a.root/'summary.json').write_text(json.dumps({'reference':'https://doi.org/10.1002/fld.1650030305','reference_conditions':'Pr=0.71 Ra=1000, no-slip all walls, hot/cold vertical walls, insulated horizontal walls','constructed_coefficients':'L=1, rho=1, cp=1, k=1, mu=0.71, beta=.01, deltaT=1, g=71000; a mathematical benchmark, not real product air','results':results},indent=2));print(json.dumps(results,indent=2))
