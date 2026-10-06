from pathlib import Path
import shutil,subprocess,concurrent.futures,json,re,os
root=Path.cwd(); source=root/'work/elmer-natural-convection'; base=(source/'case.sif').read_text()
bin=root/'work/solvers/elmer-install/bin/ElmerSolver'
out=root/'work/audiopicture/evidence/rev-et/convection';out.mkdir(parents=True,exist_ok=True)
def run(relax):
 d=out/str(relax);d.mkdir(exist_ok=True);shutil.copytree(source/'square',d/'square',dirs_exist_ok=True)
 s=base.replace('Steady State Max Iterations = 20','Steady State Max Iterations = 500').replace('Steady State Convergence Tolerance = 1.0e-5',f'Steady State Convergence Tolerance = 1.0e-7\n  Steady State Relaxation Factor = {relax}').replace('Solver 2 :: Reference Norm = Real 0.27503667E-03','').replace('!  Post File = case.vtu','  Post File = case.vtu')
 s=s.replace('Linear System Symmetric = True','Linear System Symmetric = False')
 (d/'case.sif').write_text(s)
 with (d/'solver.log').open('w') as f:p=subprocess.run([str(bin),'case.sif'],cwd=d,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
 log=(d/'solver.log').read_text();result={'relaxation':relax,'exit_code':p.returncode,'coupled_warnings':log.count('Coupled system did not converge'),'nan':bool(re.search(r'\bNaN\b',log)),'last_changes':re.findall(r'ComputeChange: SS .*',log)[-2:]}
 (d/'result.json').write_text(json.dumps(result,indent=2));return result
with concurrent.futures.ThreadPoolExecutor(3) as e:print(json.dumps(list(e.map(run,[.1,.2,.35])),indent=2))
