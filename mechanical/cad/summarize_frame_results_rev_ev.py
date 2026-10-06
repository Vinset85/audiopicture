"""Summarize completed CalculiX screens, with constrained-DOF reaction accounting.
Nodal extrapolated stress extrema are diagnostics, never orthotropic allowables.
"""
import argparse,json,re
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--mesh',type=Path,required=True);p.add_argument('--run',type=Path,required=True);a=p.parse_args()
data=np.load(a.mesh/'mesh-data.npz');tags=data['tags'].astype(int);xyz=data['coords'];idx={n:i for i,n in enumerate(tags)};sets=json.loads((a.mesh/'sets.json').read_text())

def read_frd(path):
 result={};active=None
 with path.open() as f:
  for line in f:
   if line.startswith(' -4'):
    name=line.split()[1];active=name if name in ['DISP','FORC','STRESS'] else None
    if active:result[active]={}
   elif line.startswith(' -3'):active=None
   elif active and line.startswith(' -1'):
    result[active][int(line[3:13])]=[float(line[j:j+12]) for j in range(13,len(line.rstrip()),12)]
 return result

def dat_vectors(path,label):
 results={};active=False
 for line in path.read_text().splitlines():
  if label in line:active=True;results={};continue
  if active:
   parts=line.split()
   if len(parts)==4:
    try:results[int(parts[0])]=[float(x) for x in parts[1:]]
    except ValueError:active=False
   elif results:active=False
 return results
out=[]
for folder in sorted(a.run.iterdir()):
 if not folder.is_dir() or not (folder/'execution.json').exists():continue
 report=json.loads((folder/'execution.json').read_text());case=report['case'];r={'case':case,'solver_execution_pass':report.get('solver_execution_pass',False),'classification':'SIMULATED_NORMALIZED_SCREEN_NOT_RELEASE'}
 sta=(folder/'frame.sta').read_text().splitlines() if (folder/'frame.sta').exists() else []
 rows=[x.split() for x in sta[2:] if x.strip()]
 r['final_step_time']=float(rows[-1][5]) if rows and len(rows[-1])>=7 else None
 if case=='BUCKLE':
  txt=(folder/'frame.dat').read_text();match=re.search(r'MODE NO\s+BUCKLING\s+FACTOR\s+((?:\s*\d+\s+[-+0-9.E]+\s*)+)',txt);r['buckling_factors']=[float(line.split()[1]) for line in match.group(1).strip().splitlines()] if match else [];r['buckling_scope']='Linear eigenvalue screen under 70 N seed; does not establish nonlinear imperfection or material margin.';out.append(r);continue
 if not r['solver_execution_pass'] or r['final_step_time']!=1.:
  r['status']='OPEN_SOLVER_NOT_COMPLETED';out.append(r);continue
 fields=read_frd(folder/'frame.frd');u=dat_vectors(folder/'frame.dat','displacements (vx,vy,vz) for set ALL');rf=dat_vectors(folder/'frame.dat','forces (fx,fy,fz) for set REACTION')
 assert len(u)==len(tags)
 U=np.array([u[n] for n in tags]);norm=np.linalg.norm(U,axis=1);imax=int(norm.argmax())
 r.update(max_displacement_mm=float(norm[imax]),max_displacement_node=int(tags[imax]),max_displacement_xyz_mm=xyz[imax].tolist(),max_abs_UZ_mm=float(abs(U[:,2]).max()))
 r['corner_max_abs_UZ_mm']={name:max(abs(u[n][2]) for n in ns) for name,ns in sets.items() if name.startswith('CORNER')}
 r['bore_boundary_displacement_note']='Bore displacements are prescribed zero; cannot validate <=0.5 mm mount movement with these supports.'
 r['adjacent_mount_max_displacement_mm']={name:max((norm[i] for i,(x,y,z) in enumerate(xyz) if 3.01<=np.hypot(x-x0,y-375)<=10 and z>=27),default=None) for name,x0 in [('UL1',37.5),('UL2',67.5),('UR1',252.5),('UR2',282.5)]}
 fixed=sum([sets[n] for n in (['UL1','UL2'] if case=='LC2L' else ['UR1','UR2'] if case=='LC2R' else ['UL1','UL2','UR1','UR2'])],[])
 # Only fixed DOFs contribute support reactions. RF of free DOFs can equal applied loads.
 bcs={n:[0,1,2] for n in fixed};coords={int(n):xyz[i] for i,n in enumerate(tags)}
 if report.get('lower_unilateral_gap_contacts'):
  for i,n in enumerate(sets['PAD_L']+sets['PAD_R']):bcs[int(tags.max())+1+i]=[0,1,2];coords[int(tags.max())+1+i]=xyz[idx[n]]
 if report.get('anti_lift_normal_support_assumption'):
  for n in sets['ANTILIFT']:bcs[n]=sorted(set(bcs.get(n,[])+[2]))
 if case=='LC7':
  for n in sets['CORNER_LL']:bcs[n]=sorted(set(bcs.get(n,[])+[2]))
 reactions={n:np.array([rf.get(n,fields['FORC'].get(n,[0,0,0]))[d] if d in ds else 0 for d in range(3)]) for n,ds in bcs.items()}
 r['support_reaction_sum_N']=np.sum(list(reactions.values()),axis=0).tolist();loads=np.array(report['load_sum_N']);r['force_balance_residual_N']=(np.sum(list(reactions.values()),axis=0)+loads).tolist()
 r['force_balance_within_0_1_percent_or_0_001N']=bool(max(abs(np.array(r['force_balance_residual_N'])))<=max(.001,float(np.linalg.norm(loads))*.001))
 r['cleat_bore_reactions_N']={name:sum((reactions.get(n,np.zeros(3)) for n in sets[name]),np.zeros(3)).tolist() for name in ['UL1','UL2','UR1','UR2']}
 r['anti_lift_normal_reaction_N']=sum(reactions.get(n,np.zeros(3))[2] for n in sets['ANTILIFT'])
 r['warp_normal_reaction_N']=sum(reactions.get(n,np.zeros(3))[2] for n in sets['CORNER_LL']) if case=='LC7' else None
 # Moment closure uses deformed application points for NLGEOM. A planar
 # frictionless wall contact reacts at the slave's current tangential position.
 current={n:coords[n]+(np.array(u.get(n,[0,0,0])) if report.get('nonlinear_geometry') else np.zeros(3)) for n in coords}
 if report.get('lower_unilateral_gap_contacts'):
  for i,n in enumerate(sets['PAD_L']+sets['PAD_R']):
   ground=int(tags.max())+1+i;current[ground]=current[n].copy();current[ground][2]=35.
  r['pad_max_numerical_penetration_mm']=max(0.,max(u[n][2] for n in sets['PAD_L']+sets['PAD_R']))
  r['pad_max_opening_mm']=max(0.,max(-u[n][2] for n in sets['PAD_L']+sets['PAD_R']))
 origin=np.array([160,200,0]);moment=sum((np.cross(current[n]-origin,f) for n,f in reactions.items()),np.zeros(3))
 loading=False
 for line in (folder/'frame.inp').read_text().splitlines():
  if line.upper().startswith('*CLOAD'):loading=True;continue
  if line.startswith('*'):loading=False
  if loading and line.strip():
   n,d,f=line.split(',');n=int(n);force=np.zeros(3);force[int(d)-1]=float(f);moment+=np.cross(current[n]-origin,force)
 r['moment_balance_residual_Nmm']=moment.tolist()
 r['moment_balance_note']='About (160,200,0); wall reaction uses deformed slave tangential location. Diagnostic, not qualification of the contact model.'
 S=np.array([fields['STRESS'][n] for n in tags]);xx,yy,zz,xy,yz,zx=S.T
 vm=np.sqrt(.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3*(xy*xy+yz*yz+zx*zx));si=int(vm.argmax())
 T=np.zeros((len(tags),3,3));T[:,0,0]=xx;T[:,1,1]=yy;T[:,2,2]=zz;T[:,0,1]=T[:,1,0]=xy;T[:,1,2]=T[:,2,1]=yz;T[:,0,2]=T[:,2,0]=zx;principal=np.linalg.eigvalsh(T)
 r['nodal_extrapolated_stress_diagnostic']={'von_mises_max_MPa':float(vm[si]),'node':int(tags[si]),'xyz_mm':xyz[si].tolist(),'principal_max_MPa':float(principal[:,-1].max()),'principal_min_MPa':float(principal[:,0].min()),'hotspot_classification':'UNRESOLVED: unfilleted corners and bonded constraints; no non-singular peak or failure index claimed'}
 r['qualified_strength_margin']=None
 if case=='LC4':r['corner_displacement_screen_status']='PASS_SCOPE_ONLY' if max(r['corner_max_abs_UZ_mm'].values())<=1 else 'FAIL'
 (folder/'metrics.json').write_text(json.dumps(r,indent=2));out.append(r)
(a.run/'metrics.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
