"""Conditional mass/load update with actual new frame and sidewall volumes."""
import hashlib
import json
from pathlib import Path
repo=Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[repo/'evidence/rev-fd/mass-load-review.json',
       repo/'evidence/rev-eq/execution.json', repo/'evidence/rev-eu22/execution.json',
       repo/'evidence/rev-fe/sidewalls-eu22/execution.json',Path(__file__)]
prior,old_shell,frame,shell=[json.loads(p.read_text()) for p in paths[:4]]
for name,digest in prior['source_sha256'].items(): assert sha(repo/name)==digest
assert frame['valid'] and shell['valid'] and shell['STEP_reimport_valid']
rows=[]
for old in prior['scenarios']:
    if old['candidate']!='EU.20':continue
    rho=old['ASA_density_assumption_g_cm3']
    added_shell_g=(shell['volume_mm3']-old_shell['solid_volume_mm3'])*rho/1000
    total=old['conditional_total_with_other_old_reserves_g']-old['frame_calculated_g']+frame['mass_g_at_catalog_density_1p22']+added_shell_g
    rows.append({'frame':'EU.22','shell':'Rev.FE sidewalls candidate',
                 'frame_calculated_g_at_catalog_density':frame['mass_g_at_catalog_density_1p22'],
                 'ASA_density_assumption_g_cm3':rho,'shell_calculated_g_at_assumed_density':shell['volume_mm3']*rho/1000,
                 'conditional_total_with_other_old_reserves_g':total,
                 'conditional_vertical_load_4g_min70_N':max(70,4*total/1000*9.80665),
                 'actual_assembly_mass_or_load_qualification':False})
report={'revision':'Rev.FE','classification':'CALCULATED_CONDITIONAL_RECONCILIATION_NOT_ASSEMBLED_MASS',
        'frame_mass_ceiling_g':None,'scenarios':rows,'actual_assembled_mass_g':None,
        'actual_assembled_CG_mm':None,'final_vertical_load_N':None,
        'limits':['Sidewalls are now present, but service/mount interfaces, seals and ENV chamber remain incomplete.',
                  'Other old reserves are retained as explicitly conditional bookkeeping, not verified component masses.',
                  'ASA 1.05/1.10 g/cm3 are assumptions, not measured properties; frame 1.22 is the existing catalog density.',
                  'No new mass ceiling is imposed. Final loads follow actual assembly mass/CG and installation conditions.',
                  'A 100 N screening load, if executed, is a sensitivity and does not qualify wall anchors or product capacity.'],
        'source_sha256':{str(p.relative_to(repo)):sha(p) for p in paths}}
(repo/'evidence/rev-fe/mass-load-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
