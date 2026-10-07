"""Fit local translations/rotations to executed LC4 nodal displacement fields.

This is a small-rotation least-squares diagnostic, not strain energy, stress
qualification, or a physical measurement. No prescribed support is altered.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--mesh',type=Path,required=True);p.add_argument('--run',type=Path,required=True);a=p.parse_args()
d=np.load(a.mesh/'mesh-data.npz');tags=d['tags'].astype(int);xyz=d['coords'];u={};active=False
execution=json.loads((a.run/'execution.json').read_text());assert execution['solver_execution_pass'] and execution['case']=='LC4'
for line in (a.run/'frame.dat').read_text().splitlines():
 if 'displacements (vx,vy,vz) for set ALL' in line:active=True;u={};continue
 if active:
  c=line.split()
  if len(c)==4:
   try:u[int(c[0])]=list(map(float,c[1:]))
   except ValueError:active=False
  elif u:active=False
assert len(u)==len(tags);U=np.array([u[int(n)] for n in tags]);rows=[]
for x in [160,170,190,210,230,240,250,270,280,290,300,313]:
 sel=(abs(xyz[:,0]-x)<2)&(xyz[:,1]<19.01)
 c=xyz[sel];disp=U[sel];center=np.array([x,11,22]);q=c-center
 A=np.zeros((len(q)*3,6));A[:,0:3]=np.tile(np.eye(3),(len(q),1))
 A[0::3,4]=q[:,2];A[0::3,5]=-q[:,1];A[1::3,3]=-q[:,2];A[1::3,5]=q[:,0];A[2::3,3]=q[:,1];A[2::3,4]=-q[:,0]
 fit,residuals,rank,singular=np.linalg.lstsq(A,disp.ravel(),rcond=None);assert rank==6
 rows.append({'section_x_mm':x,'nodes':int(sel.sum()),'translation_xyz_mm':fit[:3].tolist(),'small_rotation_xyz_rad':fit[3:].tolist(),'fit_RMS_mm':float(np.sqrt(np.mean((A@fit-disp.ravel())**2)))})
report={'classification':'CALCULATED_POSTPROCESS_OF_EXECUTED_NORMALIZED_FEA',
 'method':'Least squares U = translation + small_rotation cross (X-[section_x,11,22]); equal nodal weights; original coordinates; |X-section_x|<2 mm and Y<19.01 mm',
 'sections':rows,'source_sha256':{str(v):hashlib.sha256(v.read_bytes()).hexdigest() for v in [a.mesh/'mesh-data.npz',a.run/'frame.dat',a.run/'execution.json',Path(__file__)]},
 'limits':['Not a material or support qualification.', 'A local rigid-section fit is diagnostic; its residual is not stress or energy.', 'No physical rotation, separated compliance contribution or full-field displacement decomposition is asserted.']}
(a.run/'lower-crossmember-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
