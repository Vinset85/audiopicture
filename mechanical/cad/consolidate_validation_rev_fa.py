"""Add executed optical and EU.12 evidence; preserve historical failed gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess

repo=Path(__file__).resolve().parents[2]
def read(p):return json.loads((repo/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
o=read('evidence/rev-fa/execution.json')
v=read('evidence/rev-fa/independent-artifact-check.json')
assert v['execution_sha256']==sha(repo/'evidence/rev-fa/execution.json')
for path,digest in o['input_sha256'].items():assert sha(repo/path)==digest,path
for part in o['exports'].values():
    assert sha(repo/'evidence/rev-fa'/part['step'])==part['sha256']
    if 'stl' in part:assert sha(repo/'evidence/rev-fa'/part['stl'])==part['stl_sha256']
assert o['35_deg_remaining_combined_lateral_allowance_mm']>0
assert all(x['blocked_by_carrier']==0 for x in o['angular_sweep'] if x['polar_deg']<=35)
cad=read('evidence/rev-eu12/execution.json')
for path,digest in cad['input_sha256'].items():assert sha(repo/path)==digest,path
mesh=read('evidence/rev-ev12/M0/mesh-report.json')
assert mesh['source_sha256']==cad['sha256']==sha(repo/'evidence/rev-eu12/AP22_FRAME_CANDIDATE_REV_EU.step')
assert cad['valid'] and cad['reimport_valid'] and cad['solid_count']==cad['reimport_solids']==1
assert max(cad['collision_volume_mm3'].values())<1e-6
lc1=read('evidence/rev-ev12/M0-linear-MAT-B/LC1/metrics.json')
lc4=read('evidence/rev-ev12/M0-contactK100k-MAT-B/LC4/metrics.json')
lc3=read('evidence/rev-ev12/M0-contactK100k-MAT-B-pull/LC3/metrics.json')
loaded=read('evidence/rev-ev12/M0-contactK100k-MAT-B-pull/LC3/deformed-clearance.json')
for path,digest in loaded['source_sha256'].items():assert sha(repo/path)==digest,path
for name,metric in [('M0-linear-MAT-B/LC1',lc1),('M0-contactK100k-MAT-B/LC4',lc4),('M0-contactK100k-MAT-B-pull/LC3',lc3)]:
    folder=repo/'evidence/rev-ev12'/name
    e=json.loads((folder/'execution.json').read_text())
    assert e['input_sha256']==sha(folder/'frame.inp')
    assert 'Job finished' in (folder/'solver.log').read_text()
    assert metric['solver_execution_pass'] and metric['final_step_time']==1
    assert metric['force_balance_within_0_1_percent_or_0_001N']
g=read('mechanical/validation/rev-ez/gate-register.json')
s=read('mechanical/validation/rev-ez/summary.json')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==g['base_head']
timestamp=datetime.now(timezone.utc).isoformat()
g['revision']='Rev.FA';g['recorded_utc']=timestamp
for item in g['gates']:
    if item['id']=='G52':item['historical_scope']='Rejected old ENV placement. New perimeter candidate is evaluated separately by G55; the original result is not erased.'
    if item['id']=='G53':item['evidence']='Rev.FA passes nominal perimeter optical geometry only. Physical split, wiring/FPC, retention, baffle, PCB DRC and SHT45 chamber remain OPEN; see G55/G56.'
def gate(i,status,scope,evidence):g['gates'].append({'id':f'G{i:02d}','status':status,'scope':scope,'evidence':evidence})
gate(55,'PASS','Rev.FA nominal perimeter optical geometry, independent CAD/STL artifacts and straight front removal only',
     {'ray_count_through_35_deg':1953,'blocked_through_35_deg':0,'independent_OCC_rays':153,
      'analytic_clear_half_angle_deg':o['analytical_all_azimuth_clear_half_angle_deg'],
      'remaining_geometric_allowance_mm':o['35_deg_remaining_combined_lateral_allowance_mm'],
      'optical_transmission_or_lux_accuracy_simulated':False,'evidence':'evidence/rev-fa'})
gate(56,'OPEN','Optical island mechanical/electrical split and final light sealing',
     {'unresolved':o['open_items'],'prepared_physical_test':'manufacturing/optical-coupon-rev-fa.md',
      'physical_test_executed':False,'full_enclosure_sidewall_front_joint':'OPEN'})
mass=cad['volume_mm3']*.00122
assert mass<=250 and cad['shell_clearance_mm']>=1-1e-6
gate(57,'PASS','EU.12 nominal CAD, coarse keep-outs, shell/front clearance and catalog-density mass only',
     {'mass_g_at_catalog_1p22':mass,'volume_mm3':cad['volume_mm3'],
      'shell_clearance_mm':cad['shell_clearance_mm'],'front_clearance_mm':cad['front_carrier_clearance_mm'],
      'zero_overlap_checks':len(cad['collision_volume_mm3']),'full_exact_assembly_and_fillets':'OPEN'})
u=lc4['corner_max_abs_UZ_mm']['CORNER_LR']
gate(58,'PASS' if u<=1 else 'FAIL','EU.12 lower-right LC4 30 N normalized nonlinear contact screen, 1 mm limit',
     {'corner_UZ_mm':u,'qualified_material_and_contacts':False,'mesh_convergence_this_revision':False,
      'equilibrium_pass':True,'worst_corner_across_all_product_corners_demonstrated':False})
gate(59,'PASS','EU.12 LC1 execution and equilibrium only; not upper-mount compliance acceptance',
     {'maximum_U_mm':lc1['max_displacement_mm'],'maximum_xyz_mm':lc1['max_displacement_xyz_mm'],
      'qualified_strength_margin':None,'mount_boundary_displacement_constrained':True})
assert loaded['nodes_predicted_inside_DML']>0
gate(60,'FAIL','EU.12 LC3 unconstrained outward-pull model predicts DML interference',
     {'solver_execution_and_equilibrium_pass':True,'max_U_mm':lc3['max_displacement_mm'],
      'deformed_clearance':loaded,'physical_post_contact_response_simulated':False,
      'consequence':'Reject this candidate for assembly; LC1 improvement does not compensate for lost out-of-plane stiffness.'})
g['dependency_order']+=['G55 -> actual optical retention/interconnect/baffle -> G56 + G53 -> P15 optical characterization',
                        'G57/G58/G59 -> further frame design + true interfaces -> full current-revision structural matrix']
s.update(revision='Rev.FA',recorded_utc=timestamp,
         gate_counts={st:sum(x['status']==st for x in g['gates']) for st in ['PASS','FAIL','OPEN']},
         optical_perimeter_candidate=o,
         frame_EU12={'CAD':cad,'mesh':mesh,'LC1':lc1,'LC3':lc3,'LC4':lc4,'loaded_clearance':loaded},
         production_ready=False,all_remaining_digital_work_complete=False)
out=repo/'mechanical/validation/rev-fa';out.mkdir(parents=True,exist_ok=True)
(out/'gate-register.json').write_text(json.dumps(g,indent=2)+'\n')
(out/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
sources=['mechanical/cad/generate_optical_perimeter_candidate_rev_fa.py',
         'mechanical/cad/audit_loaded_frame_envelope_rev_fa.py',
         'mechanical/cad/verify_optical_candidate_rev_fa.py',
         'mechanical/cad/generate_frame_candidate_rev_eu12.py',
         'mechanical/cad/mesh_frame_screen_rev_ev.py',
         'mechanical/cad/run_frame_screen_rev_ev.py',
         'mechanical/cad/summarize_frame_results_rev_ev.py',
         'mechanical/cad/consolidate_validation_rev_fa.py']
provenance={'revision':'Rev.FA','recorded_utc':timestamp,'base_head':g['base_head'],
    'source_hashes':{p:sha(repo/p) for p in sources},
    'evidence_hashes':{str(p.relative_to(repo)):sha(p) for base in ['evidence/rev-fa','evidence/rev-eu12','evidence/rev-ev12'] for p in (repo/base).rglob('*') if p.is_file() and p.name!='provenance.json'},
    'physical_tests_executed':False,'full_product_CFD_executed':False,
    'prior_tests':'Rev.EZ evidence remains historical; no firmware or HA source was changed by this mechanical iteration.'}
(repo/'evidence/rev-fa/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'gates':s['gate_counts'],'EU12_mass_g':mass,'EU12_LC1_U_mm':lc1['max_displacement_mm'],'EU12_LC4_LR_mm':u,'production_ready':False},indent=2))
