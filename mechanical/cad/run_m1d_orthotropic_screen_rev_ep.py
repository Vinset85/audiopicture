"""Normalized M1D sensitivity; explicitly assumed constitutive matrices.

This is not frame LC1-LC7, material characterization, or allowable stress.
"""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import numpy as np

p=argparse.ArgumentParser()
p.add_argument('--ccx',type=Path,required=True)
p.add_argument('--base',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
base=a.base.read_text()
tasks=[]
for name,ez_fraction in [('MAT-A',.2),('MAT-B',.35),('MAT-C',.5)]:
 for gx in (.25,.4,.6):
  for gy in (.25,.4,.6):
   folder=a.out/f'{name}_G13_{gx}_G23_{gy}';folder.mkdir(exist_ok=True)
   E1=E2=1900.;E3=E1*ez_fraction;nu=.35
   G12=E1/(2*(1+nu));G13=G12*gx;G23=G12*gy
   compliance=np.diag([1/E1,1/E2,1/E3,1/G23,1/G13,1/G12])
   compliance[0,1]=compliance[1,0]=-nu/E1
   compliance[0,2]=compliance[2,0]=-nu/E1
   compliance[1,2]=compliance[2,1]=-nu/E2
   assert np.linalg.eigvalsh(compliance).min()>0
   seed=f'*ELASTIC,TYPE=ENGINEERING CONSTANTS\n{E1},{E2},{E3},{nu},{nu},{nu},{G12},{G13}\n{G23}\n'
   deck=base.replace('*ELASTIC\n1900,0.35\n',seed)
   assert deck!=base
   (folder/'normalized.inp').write_text(deck)
   tasks.append((folder,{'material_label':name,'E3_over_E1':ez_fraction,'G13_over_G12':gx,'G23_over_G12':gy,
                        'assumptions':{'E1_MPa':E1,'E2_MPa':E2,'E3_MPa':E3,'nu12_nu13_nu23':nu,
                                       'G12_MPa':G12,'G13_MPa':G13,'G23_MPa':G23}}))
def run(task):
 folder,report=task
 with (folder/'solver.log').open('w') as stdout,(folder/'solver.stderr').open('w') as stderr:
  r=subprocess.run([str(a.ccx.resolve()),'normalized'],cwd=folder,stdout=stdout,stderr=stderr,timeout=180)
 report.update({'folder':str(folder),'return_code':r.returncode,
                'job_finished':'Job finished' in (folder/'solver.log').read_text(),
                'classification':'NORMALIZED_LOCAL_SIMULATION_ASSUMED_MATERIAL_NOT_RELEASE'})
 print(json.dumps(report),flush=True)
 return report
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 reports=list(pool.map(run,tasks))
(a.out/'executions.json').write_text(json.dumps(reports,indent=2)+'\n')
assert all(r['return_code']==0 and r['job_finished'] for r in reports)
