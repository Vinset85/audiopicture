"""Elmer Boussinesq verification against the de Vahl Davis Ra=1000, Pr=.71 cavity.
Constructed coefficients define a numerical benchmark, NOT product air/material data.
"""
import argparse,json,subprocess,os,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--elmer-bin',type=Path,required=True);p.add_argument('--reference',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--n',type=int,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
grid=f'''Version = 210903
Coordinate System = Cartesian 2D
Subcell Divisions in 2D = 1 1
Subcell Sizes 1 = 1
Subcell Sizes 2 = 1
Material Structure in 2D
 1
End
Materials Interval = 1 1
Boundary Definitions
 1 -1 1 1
 2 -2 1 1
 3 -3 1 1
 4 -4 1 1
End
Numbering = Horizontal
Element Degree = 1
Element Innernodes = False
Surface Elements = {a.n*a.n}
Element Ratios 1 = 1
Element Ratios 2 = 1
Element Densities 1 = 1
Element Densities 2 = 1
'''
(a.out/'square.grd').write_text(grid)
with (a.out/'grid.log').open('w') as f:subprocess.run([str((a.elmer_bin/'ElmerGrid').resolve()),'1','2','square.grd'],cwd=a.out,stdout=f,stderr=subprocess.STDOUT,check=True)
s=a.reference.read_text().replace('Simulation Type = Transient','Simulation Type = Steady State').replace('Steady State Max Iterations = 500','Steady State Max Iterations = 1000').replace('Output Intervals(1) = 0','Output Intervals(1) = 1')
s=s.replace('Gravity(4) = 0 -1 0 9.82','Gravity(4) = 0 -1 0 71000')
s=s.replace('Name = "Water (room temperature)"','Name = "Constructed benchmark coefficients Pr0.71 Ra1000"').replace('Heat Conductivity = 0.58','Heat Conductivity = 1').replace('Reference Temperature = 293.0','Reference Temperature = 300').replace('Heat Capacity = 4183.0','Heat Capacity = 1').replace('Density = 998.3','Density = 1').replace('Viscosity = 1.002e-3','Viscosity = 0.71').replace('Heat expansion Coefficient = 0.207e-3','Heat expansion Coefficient = 0.01').replace('Temperature = 295','Temperature = 300').replace('Temperature = 297.0','Temperature = 299.5').replace('Temperature = 293.0','Temperature = 300.5')
s=s.replace('!  Velocity 1 = 0.0','  Velocity 1 = 0.0').replace('Steady State Convergence Tolerance = 1.0e-7','Steady State Convergence Tolerance = 1.0e-10').replace('Linear System Abort Not Converged = False','Linear System Abort Not Converged = True')
s=s.replace('Steady State Relaxation Factor = 0.2','Steady State Relaxation Factor = 0.35')
s=s.replace('Nonlinear System Max Iterations = 1','Nonlinear System Max Iterations = 10').replace('Nonlinear System Convergence Tolerance = 1.0e-8','Nonlinear System Convergence Tolerance = 1.0e-10')
s=s.replace('Linear System Max Iterations = 500','Linear System Max Iterations = 2000').replace('Linear System Convergence Tolerance = 1.0e-8','Linear System Convergence Tolerance = 1.0e-11').replace('Linear System Convergence Tolerance = 1.0e-10','Linear System Convergence Tolerance = 1.0e-11')
(a.out/'case.sif').write_text(s)
with (a.out/'solver.log').open('w') as f:
 try:r=subprocess.run([str((a.elmer_bin/'ElmerSolver').resolve()),'case.sif'],cwd=a.out,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'},timeout=1800);code=r.returncode
 except subprocess.TimeoutExpired:code='TIMEOUT'
log=(a.out/'solver.log').read_text();report={'n':a.n,'Ra':1000,'Pr':.71,'beta_delta_T':.01,'coefficients_classification':'CONSTRUCTED_REFERENCE_MODEL_NOT_PHYSICAL_PROPERTY_CLAIM','exit_code':code,'coupled_warnings':log.count('Coupled system did not converge'),'nan':bool(re.search(r'\bNaN\b',log)),'last_changes':re.findall(r'ComputeChange: SS .*',log)[-2:]}
(a.out/'execution.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
