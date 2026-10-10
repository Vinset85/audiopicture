"""Execute candidate-frame normalized load screens, never a production PASS.

Rev.FE adds explicit material/print axes; the weak direction is not always global Z.
Vertical loads remain at least the frozen 70 N minimum.
Orthotropic seeds and volume-based substitute loads are explicit. Boressurfaces
are perfectly bonded rigid insert/cleat surrogates. Lower supports may use
unilateral GAPUNI penalty contacts with zero friction and zero initial gap.
"""
import argparse,json,re,os,subprocess,hashlib
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--mesh',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--ccx',type=Path,required=True);p.add_argument('--cases',nargs='+',default=['LC1']);p.add_argument('--ez',type=float,default=.35);p.add_argument('--gx',type=float,default=.4);p.add_argument('--gy',type=float,default=.4);p.add_argument('--cg',nargs=2,type=float,default=[160,200]);p.add_argument('--gap',action='store_true');p.add_argument('--pad-penalty',type=float,default=100000.);p.add_argument('--gap-force-floor',type=float,default=1e-12);p.add_argument('--contact-iterations',action='store_true');p.add_argument('--anti-normal',action='store_true');p.add_argument('--execute',action='store_true');p.add_argument('--warp',type=float,default=.5);p.add_argument('--corner',choices=['LL','LR','UL','UR'],default='LR');p.add_argument('--vertical-load',type=float,default=70.);p.add_argument('--weak-axis',choices=['X','Y','Z'],default='Z');a=p.parse_args();assert np.isfinite(a.vertical_load) and a.vertical_load>=70, 'Vertical load must be finite and at least 70 N';a.out.mkdir(parents=True,exist_ok=True)
mesh=(a.mesh/'mesh.inp').read_text();sets=json.loads((a.mesh/'sets.json').read_text());data=np.load(a.mesh/'mesh-data.npz');tags=data['tags'].astype(int);xyz=data['coords'];weight=data['weights'];index={t:i for i,t in enumerate(tags)}
# Adjust positive distributed body-load weights to an explicit XY CG seed.
mu=weight@xyz[:,:2];centered=xyz[:,:2]-mu;cov=centered.T@(weight[:,None]*centered);coef=np.linalg.solve(cov,np.array(a.cg)-mu);w=weight*(1+centered@coef);assert min(w)>0;w=w/w.sum();assert np.max(abs(w@xyz[:,:2]-a.cg))<1e-6
E=1900.;nu=.35;g=E/(2*(1+nu));constants=[E,E,E*a.ez,nu,nu,nu,g,g*a.gx,g*a.gy]
compliance=np.diag([1/E,1/E,1/(E*a.ez),1/(g*a.gy),1/(g*a.gx),1/g]);compliance[0,1]=compliance[1,0]=-nu/E;compliance[0,2]=compliance[2,0]=-nu/E;compliance[1,2]=compliance[2,1]=-nu/E;assert min(np.linalg.eigvalsh(compliance))>0
axes={'Z':[[1,0,0],[0,1,0],[0,0,1]],
      'X':[[0,1,0],[0,0,1],[1,0,0]],
      'Y':[[1,0,0],[0,0,-1],[0,1,0]]}[a.weak_axis]
R=np.array(axes).T
assert np.allclose(R.T@R,np.eye(3)) and np.isclose(np.linalg.det(R),1)
mat='*ORIENTATION,NAME=PRINT_AXES,SYSTEM=RECTANGULAR\n'+','.join(map(str,axes[0]+axes[1]))+'\n'
mat+='*MATERIAL,NAME=PC_CF_NORMALIZED_SEED\n*ELASTIC,TYPE=ENGINEERING CONSTANTS\n'+','.join(map(str,constants[:8]))+'\n'+str(constants[8])+'\n*SOLID SECTION,ELSET=EALL,MATERIAL=PC_CF_NORMALIZED_SEED,ORIENTATION=PRINT_AXES\n'

def nset(name,nodes):return '*NSET,NSET='+name+'\n'+'\n'.join(','.join(map(str,nodes[i:i+16])) for i in range(0,len(nodes),16))+'\n'
node_sets=''.join(nset(name,n) for name,n in sets.items())+nset('ALL',tags.tolist())
results=[]
for case in a.cases:
 folder=a.out/case;folder.mkdir(exist_ok=True)
 fixed=sets['UL1']+sets['UL2']+sets['UR1']+sets['UR2']
 if case=='LC2L':fixed=sets['UL1']+sets['UL2']
 if case=='LC2R':fixed=sets['UR1']+sets['UR2']
 # Apply distributed forces only to unconstrained structural nodes.
 wf=weight.copy();wf[[index[n] for n in fixed]]=0;wf/=wf.sum()
 muf=wf@xyz[:,:2];dc=xyz[:,:2]-muf;cf=dc.T@(wf[:,None]*dc);co=np.linalg.solve(cf,np.array(a.cg)-muf);w=wf*(1+dc@co);assert min(w)>=0;w/=w.sum()
 bodyloads=np.zeros((len(tags),3))
 if case in ['LC1','LC2L','LC2R','BUCKLE']:bodyloads[:,1]=-a.vertical_load*w
 elif case=='LC3':bodyloads[:,2]=-50*w
 elif case=='LC4':
  for n in sets['CORNER_'+a.corner]:bodyloads[index[n],2]=-30/len(sets['CORNER_'+a.corner])
 elif case=='LC5':bodyloads[:,1]=-100*w
 elif case=='LC6':
  for n in sets['ANTILIFT']:bodyloads[index[n],1]=50/len(sets['ANTILIFT'])
 elif case=='LC7':pass
 else:raise ValueError(case)
 nonlinear=case in ['LC2L','LC2R','LC4','LC5','LC6','LC7'] or a.gap
 gapused=a.gap and case!='BUCKLE'
 contacts='';grounds=[]
 if gapused:
  pad=sets['PAD_L']+sets['PAD_R'];nextnode=int(max(tags))+1;nextelem=int(max(data['element_tags']))+1
  contacts='*NODE\n'
  for i,n in enumerate(pad):
   grounds.append(nextnode+i);contacts+=f'{nextnode+i},'+','.join(map(str,xyz[index[n]]))+'\n'
  contacts+='*ELEMENT,TYPE=GAPUNI,ELSET=LOWER_GAPS\n'
  for i,n in enumerate(pad):contacts+=f'{nextelem+i},{n},{grounds[i]}\n'
  # Numerical contact penalty, mesh independent total stiffness; NOT a measured pad property.
  assert a.pad_penalty>0
  contacts+='*GAP,ELSET=LOWER_GAPS\n0,0,0,1,,'+str(a.pad_penalty/len(pad))+','+str(a.gap_force_floor)+'\n'+nset('GROUND',grounds)
 reaction_nodes=sorted(set(fixed+grounds+(sets['ANTILIFT'] if a.anti_normal else [])+(sets['CORNER_LL'] if case=='LC7' else [])))
 bc=nset('FIXED',fixed)+nset('REACTION',reaction_nodes)+'*BOUNDARY\nFIXED,1,3,0\n'
 if gapused:bc+='GROUND,1,3,0\n'
 if a.anti_normal:bc+='ANTILIFT,3,3,0\n'
 step='*STEP'+(',NLGEOM,INC=200' if nonlinear else '')+'\n'
 if case=='BUCKLE':step+='*BUCKLE,SOLVER=SPOOLES\n3,0.01\n'
 elif nonlinear:step+='*STATIC,SOLVER=SPOOLES\n0.1,1,0.00001,0.2\n'
 else:step+='*STATIC,SOLVER=SPOOLES\n'
 if a.contact_iterations and nonlinear:step+='*CONTROLS,PARAMETERS=TIME INCREMENTATION\n12,20,99,40,12,4,,10\n0.25,0.5,0.75,0.85,,,1.5\n'
 if case=='LC7':step+='*BOUNDARY\nCORNER_LL,3,3,'+str(-a.warp)+'\n'
 if case!='LC7':
  step+='*CLOAD\n'
  for n,load in zip(tags,bodyloads):
   for j,f in enumerate(load):
    if abs(f)>1e-15:step+=f'{n},{j+1},{f:.12g}\n'
 # Final-only output to bound archive size; convergence history remains .sta/.cvg.
 step+='*NODE PRINT,NSET=ALL,FREQUENCY=999999\nU\n*NODE PRINT,NSET=REACTION,TOTALS=YES,FREQUENCY=999999\nRF\n*NODE FILE,FREQUENCY=999999\nU,RF\n*EL FILE,FREQUENCY=999999\nS\n*END STEP\n'
 deck=mesh+node_sets+contacts+mat+bc+step;(folder/'frame.inp').write_text(deck)
 report={'case':case,'material_axes_global':axes,'weak_global_axis':a.weak_axis,'properties_are_in_local_material_axes':True,'print_process_and_axes_qualified':False,'vertical_load_seed_N':a.vertical_load,'assembled_mass_load_adequacy_verified':False,'loaded_corner':a.corner if case=='LC4' else None,'classification':'SIMULATED_NORMALIZED_FULL_CANDIDATE_FRAME_SCREEN_NOT_RELEASE','constitutive_assumptions':dict(zip(['E1','E2','E3','nu12','nu13','nu23','G12','G13','G23'],constants)),'load_sum_N':bodyloads.sum(axis=0).tolist(),'load_cg_seed_mm':(w@xyz).tolist(),'nonlinear_geometry':nonlinear,'lower_unilateral_gap_contacts':len(grounds),'total_pad_penalty_N_per_mm':a.pad_penalty if gapused else None,'gap_force_floor_N':a.gap_force_floor if gapused else None,'contact_iteration_controls':a.contact_iterations,'anti_lift_normal_support_assumption':a.anti_normal,'bonded_insert_cleat_surrogate_nodes':len(fixed),'corner_warp_mm':a.warp if case=='LC7' else None,'input_sha256':hashlib.sha256(deck.encode()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'mesh_report':json.loads((a.mesh/'mesh-report.json').read_text()),'qualified_allowables':None,'release_margin':None}
 if a.execute:
  with (folder/'solver.log').open('w') as log:
   try:proc=subprocess.run([str(a.ccx.resolve()),'frame'],cwd=folder,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','CCX_NPROC_RESULTS':'2'},timeout=1800);report['exit_code']=proc.returncode
   except subprocess.TimeoutExpired:report['exit_code']='TIMEOUT_1800S'
  s=(folder/'solver.log').read_text();report['job_finished']='Job finished' in s;report['errors']=[line for line in s.splitlines() if '*ERROR' in line or 'too many cutbacks' in line.lower()]
  report['solver_execution_pass']=report['exit_code']==0 and report['job_finished'] and not report['errors']
 (folder/'execution.json').write_text(json.dumps(report,indent=2));results.append(report);print(json.dumps({k:v for k,v in report.items() if k not in ['mesh_report','constitutive_assumptions']}),flush=True)
(a.out/'executions.json').write_text(json.dumps(results,indent=2))
if a.execute:assert all(r['solver_execution_pass'] for r in results)
