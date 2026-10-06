"""Extract executed CalculiX results; never turn debug stress into allowables."""
import argparse
import json
import math
from pathlib import Path
import re
import numpy as np

p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
def numbers(section,count):
 return [list(map(float,l.split())) for l in section.splitlines()
         if len(l.split())==count and re.match(r'^\s*[-\d]',l)]
def extract(path):
 s=path.read_text()
 u=numbers(s.split('displacements (vx,vy,vz)')[1].split('forces (fx,fy,fz)')[0],4)
 rf=numbers(s.split('total force (fx,fy,fz)')[1].split('stresses')[0],3)[0]
 stress=numbers(s.split('stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz)')[1],8)
 vm=[math.sqrt(.5*((r[2]-r[3])**2+(r[3]-r[4])**2+(r[4]-r[2])**2)+3*sum(v*v for v in r[5:])) for r in stress]
 return {'max_target_displacement_mm':max(math.sqrt(sum(v*v for v in r[1:])) for r in u),
         'max_target_normal_displacement_mm':max(abs(r[3]) for r in u),
         'reaction_sum_N':rf,'reaction_vector_residual_percent':100*math.sqrt(rf[0]**2+rf[1]**2+(rf[2]-5)**2)/5,
         'raw_max_von_mises_debug_MPa':max(vm),
         'stress_gate':'OPEN: sharp roots/constraints require hotspot classification; no allowables'}
results=[]
for m in ('M0','M1','M2'):
 r=json.loads((a.root/m/'mesh-report.json').read_text());r.update(extract(a.root/m/'direct.dat'))
 r['solver']='CalculiX 2.23 SPOOLES';results.append(r)
change=100*abs(results[2]['max_target_displacement_mm']-results[1]['max_target_displacement_mm'])/results[2]['max_target_displacement_mm']
norm=[]
for case in sorted((a.root/'normalized').glob('*/normalized.dat')):
 norm.append({'case':case.parent.name,**extract(case)})
cube=(a.root/'benchmark/cube.dat').read_text()
cu=numbers(cube.split('displacements (vx,vy,vz)')[1].split('forces (fx,fy,fz)')[0],4)
err=max(abs(r[1]-1/1900)/(1/1900) for r in cu)
result={'classification':'SIMULATED_LOCAL_DEBUG_AND_NORMALIZED_ASSUMPTIONS_NOT_FRAME_RELEASE',
        'mesh_results':results,'M1_to_M2_target_displacement_change_percent':change,
        'displacement_convergence_gate':'PASS' if change<5 else 'FAIL',
        'stress_convergence_gate':'OPEN','unit_cube_relative_displacement_error':err,
        'unit_cube_gate':'PASS' if err<1e-5 else 'FAIL','normalized_cases':norm,
        'frame_LC1_LC7_gate':'OPEN','material_qualification_gate':'OPEN',
        'limitations':['5 N front-retention subcomponent, not 70 N frame.',
                       'No nonlinear/contact, temperature or buckling release result.',
                       'Raw von Mises is only a debug scalar, not orthotropic failure index.']}
(a.root/'validated-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('mesh_results','normalized_cases')},indent=2))
