import subprocess,itertools,json
from pathlib import Path
root=Path.cwd();repo=root/'work/audiopicture';runner=repo/'mechanical/cad/run_frame_screen_rev_ev.py';ccx=root/'work/solvers/CalculiX/ccx_2.23/src/ccx_2.23';py=root/'.venv/bin/python';mesh=repo/'evidence/rev-ev4/M0';base=repo/'evidence/rev-ev4/material-cg-sensitivities';base.mkdir(exist_ok=True)
cases=[(f'EZ{ez}-GX{gx}-GY{gy}',ez,gx,gy,[160,200]) for ez,gx,gy in itertools.product([.2,.35,.5],[.25,.4,.6],[.25,.4,.6])]
cases += [(f'CG{cg[0]}-{cg[1]}',.35,.4,.4,cg) for cg in [[140,200],[180,200],[160,185],[160,215]]]
results=[]
for name,ez,gx,gy,cg in cases:
 out=base/name
 cmd=[str(py),str(runner),'--mesh',str(mesh),'--out',str(out),'--ccx',str(ccx),'--cases','LC1','--anti-normal','--ez',str(ez),'--gx',str(gx),'--gy',str(gy),'--cg',*map(str,cg),'--execute']
 with (base/(name+'.log')).open('w') as f:ret=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 r={'id':name,'exit_code':ret.returncode};results.append(r);(base/'batch.json').write_text(json.dumps(results,indent=2));print(r,flush=True)
assert all(x['exit_code']==0 for x in results)
