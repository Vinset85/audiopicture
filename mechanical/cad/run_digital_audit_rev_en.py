"""Repository evidence inventory; executes selected unchanged baseline scripts.

Historical STATUS strings are indexed as claims, never promoted to verified PASS.
"""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root=Path(__file__).resolve().parents[2]
out=root/'evidence'/'rev-en'
out.mkdir(parents=True,exist_ok=True)
tracked=subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines()
inventory=[];claims=[]
for name in tracked:
    path=root/name
    data=path.read_bytes()
    inventory.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    if path.suffix in ('.md','.json','.csv','.py'):
        for n,line in enumerate(data.decode('utf-8').splitlines(),1):
            if any(s in line.upper() for s in ('OPEN','FAIL','VALIDATE','PENDING','NOT YET','NOT_A_')):
                claims.append({'file':name,'line':n,'text':line})
bom=list(csv.DictReader((root/'hardware/bom/audiopicture-v2.2-rev-a.csv').open()))
unresolved=[r for r in bom if any(t in r['Status'] for t in ('VALIDATE','VERIFY','PLACEHOLDER','OPEN','DNP'))]
index={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
       'tracked_files':inventory,'historical_unresolved_claims':claims,
       'bom_rows':len(bom),'bom_unresolved_rows':unresolved,
       'native_kicad_files':[n for n in tracked if n.endswith(('.kicad_sch','.kicad_pcb'))],
       'firmware_source_files':[n for n in tracked if n.startswith('firmware/') and n.endswith(('.c','.h','.cpp','.py'))],
       'home_assistant_source_files':[n for n in tracked if n.startswith('home-assistant/') and n.endswith('.py')],
       'interpretation':'Text inventory is traceability, not verification of historical claims.'}
(out/'repository-inventory.json').write_text(json.dumps(index,indent=2)+'\n')
# Executed scripts only; every result gets stdout, stderr, exit code and source hash.
selected=['generate_rear_frame_g2_rev_c.py','generate_rear_frame_retention_rev_ap.py',
          'generate_structural_spine_rev_j.py','generate_m1d_fea_submodel_rev_k.py',
          'generate_rear_shell_frame_aware_master_rev_bk.py',
          'spatial_heat_allocation_rev_ci.py','thermal_source_matrix_rev_cg.py',
          'retention_hard_stack_tolerance_rev_aw.py',
          'sculpted_terminal_chamber_height_map_rev_ds.py',
          'check_distributed_frame_aware_vents_rev_bh.py']
runs=[]
for name in selected:
    script=root/'mechanical/cad'/name
    target=out/'runs'/script.stem
    target.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    with (target/'stdout.log').open('w') as stdout,(target/'stderr.log').open('w') as stderr:
        try:
            result=subprocess.run([sys.executable,str(script)],cwd=target,stdout=stdout,stderr=stderr,timeout=180)
            code=result.returncode
        except subprocess.TimeoutExpired:
            code='TIMEOUT'
    run={'script':str(script.relative_to(root)),'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
         'exit_code':code,'elapsed_s':time.monotonic()-start,
         'evidence_dir':str(target.relative_to(root))}
    runs.append(run)
    print(json.dumps(run),flush=True)
(out/'executed-scripts.json').write_text(json.dumps(runs,indent=2)+'\n')
