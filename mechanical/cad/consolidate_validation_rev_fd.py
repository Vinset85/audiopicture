"""Verify Rev.FD executions while preserving superseded mass gates as history."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

repo = Path(__file__).resolve().parents[2]
parent = 'dfe1c09d39ed9c9d843f3c43f73ca6556a68587a'
subprocess.run(['git', 'merge-base', '--is-ancestor', parent, 'HEAD'], cwd=repo, check=True)

def read(p):
    return json.loads((repo / p).read_text())

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def verify_sources(d, key):
    for path, digest in d[key].items():
        assert sha(repo / path) == digest, path

gates = read('mechanical/validation/rev-fc/gate-register.json')
mass_ids = ['G27','G40','G62','G67','G72','G74','G76','G78']
for gate in gates['gates']:
    if gate['id'] in mass_ids:
        gate['current_acceptance_applicability'] = 'HISTORICAL_MASS_TARGET_SUPERSEDED_BY_USER_REV_FD'
        gate['current_rejection_criterion'] = False

def gate(status, scope, evidence):
    gates['gates'].append({'id': f'G{len(gates["gates"])+1:02d}',
                          'status': status, 'scope': scope, 'evidence': evidence})

guard = read('evidence/rev-fd/vertical-load-input-guard.json')
assert guard['script_sha256'] == sha(repo/'mechanical/cad/run_frame_screen_rev_fd.py')
assert all(c['rejected_before_output_or_mesh_read'] for c in guard['cases'])
policy = read('mechanical/fea/rear-frame-solver-manifest-rev-fd.json')['mass_policy']
assert policy['frame_250g_is_rejection_gate'] is False
assert policy['replacement_frame_ceiling_g'] is None
def validate_candidate(number, expected):
    cad = read(f'evidence/rev-eu{number}/execution.json')
    verify_sources(cad, 'input_sha256')
    assert cad['sha256'] == sha(repo/f'evidence/rev-eu{number}/AP22_FRAME_CANDIDATE_REV_EU.step')
    assert cad['valid'] and cad['reimport_valid'] and cad['solid_count'] == cad['reimport_solids'] == 1
    assert len(cad['collision_volume_mm3']) == 22 and max(cad['collision_volume_mm3'].values()) < 1e-6
    assert cad['shell_clearance_mm'] >= 1-1e-6 and cad['front_carrier_clearance_mm'] >= .5-1e-6
    assert cad['mass_acceptance_ceiling_g'] is None
    gate('PASS', f'EU.{number} nominal BREP/reimport and 22 coarse collision checks only',
         {'volume_mm3':cad['volume_mm3'], 'mass_catalog_density_g':cad['mass_g_at_catalog_density_1p22'],
          'mass_is_tracked_without_a_250g_acceptance_gate':True, 'exact_assembly_and_fillets_complete':False})
    meshes = {}
    for mesh in ['M0','M1']:
        report = read(f'evidence/rev-ev{number}/{mesh}/mesh-report.json')
        quality = read(f'evidence/rev-ev{number}/{mesh}/quality-audit.json')
        verify_sources(quality, 'source_sha256')
        assert report['source_sha256'] == cad['sha256']
        assert quality['nonpositive_Jacobian_elements'] == 0
        meshes[mesh] = {'report':report, 'quality':quality}
    cases = {}
    for run, case, mesh in expected:
        folder = repo / f'evidence/rev-ev{number}' / run / case
        execution = json.loads((folder/'execution.json').read_text())
        metric = json.loads((folder/'metrics.json').read_text())
        assert execution['input_sha256'] == sha(folder/'frame.inp')
        assert execution['mesh_report'] == meshes[mesh]['report']
        assert execution['solver_execution_pass'] and 'Job finished' in (folder/'solver.log').read_text()
        assert metric['solver_execution_pass'] and metric['final_step_time'] == 1
        assert metric['force_balance_within_0_1_percent_or_0_001N']
        cases[run] = {'execution':execution, 'metrics':metric}
        if case == 'LC4':
            assert execution['loaded_corner'] == run.rsplit('-',1)[1]
            value = max(metric['corner_max_abs_UZ_mm'].values())
            gate('PASS' if value <= 1 else 'FAIL', f'EU.{number} {mesh} LC4 {execution["loaded_corner"]} normalized 30 N corner screen only',
                 {'max_corner_UZ_mm':value, 'limit_mm':1, 'qualified_material_and_strength':False})
        elif case == 'LC1':
            n = execution['vertical_load_seed_N']
            assert n >= 70 and abs(execution['load_sum_N'][1]+n) < 1e-6
            gate('PASS', f'EU.{number} LC1 {n:g} N linear execution and force equilibrium only',
                 {'max_displacement_mm':metric['max_displacement_mm'],
                  'actual_assembly_mass_load_adequacy_and_mount_compliance_verified':False})
        else:
            audit = json.loads((folder/'deformed-clearance.json').read_text())
            verify_sources(audit, 'source_sha256')
            cases[run]['deformed_node_audit'] = audit
            quadratic = json.loads((folder/'quadratic-dml-clearance.json').read_text())
            verify_sources(quadratic, 'source_sha256')
            cases[run]['quadratic_clearance_audit'] = quadratic
            gate('PASS' if quadratic['final']['all_element_bounds_separated_from_DML_and_frontward_region'] else 'OPEN',
                 f'EU.{number} LC3 full quadratic FEA element enclosure versus fixed DML at final load only',
                 {'bound':quadratic['final'], 'exact_deformed_CAD_and_physical_clearance_qualified':False})
            hit = audit['nodes_predicted_inside_DML'] + audit['nodes_predicted_frontward_of_DML_within_projection']
            gate('FAIL' if hit else 'PASS', f'EU.{number} LC3 sampled deformed-node DML interference diagnostic only',
                 {'node_interference_count':hit, 'exact_deformed_CAD_and_physical_clearance_verified':False,
                  'max_displacement_mm':metric['max_displacement_mm']})
    coarse = max(cases['M0-contactK100k-MAT-B-LR']['metrics']['corner_max_abs_UZ_mm'].values())
    fine = max(cases['M1-contactK100k-MAT-B-LR']['metrics']['corner_max_abs_UZ_mm'].values())
    change = abs(fine-coarse)/abs(fine)*100
    comparison = {'coarse_mm':coarse, 'fine_mm':fine, 'relative_change_percent_fine_reference':change,
                  'two_mesh_displacement_change_below_5_percent':change<5,
                  'full_contract_mesh_convergence_verified':False,
                  'limits':['No converged non-singular stress or qualified allowable.',
                            'Nodal load/contact sampling changes with refinement.',
                            'No general transfer to other load/material/geometry cases.']}
    gate('PASS' if change<5 else 'FAIL', f'EU.{number} two-mesh lower-right LC4 displacement comparison only', comparison)
    return {'CAD':cad, 'meshes':meshes, 'cases':cases, 'LC4_mesh_comparison':comparison}

common = [('M0-linear70-MAT-B','LC1','M0'), ('M0-linear90-MAT-B','LC1','M0'),
          ('M0-pull-contactK100k-MAT-B','LC3','M0'),
          ('M0-contactK100k-MAT-B-LR','LC4','M0'), ('M1-contactK100k-MAT-B-LR','LC4','M1')]
frames = {'EU19':validate_candidate(19, common)}
frames['EU20'] = validate_candidate(20, common+[(f'M0-contactK100k-MAT-B-{c}','LC4','M0') for c in ['LL','UL','UR']])
gate('OPEN', 'EU.20 full current-revision structural and assembly qualification',
     {'coupon_materials':False, 'actual_load_mass_CG':False, 'real_cleat_insert_contact_geometry':False,
      'fillets_hotspot_stress_convergence':False, 'full_LC1_LC7_sensitivity_buckling_matrix':False})
verify_sources(read('evidence/rev-fd/frame-comparison.json'), 'source_sha256')
mass_review = read('evidence/rev-fd/mass-load-review.json')
verify_sources(mass_review, 'source_sha256')
for name in ['EU18-EU19','EU19-EU20']:
    verify_sources(read(f'evidence/rev-fd/{name}-boundary-comparison.json'), 'sha256')
timestamp = datetime.now(timezone.utc).isoformat()
gates.update(revision='Rev.FD',recorded_utc=timestamp,checkpoint_parent_head=parent,mass_policy=policy,
             historical_mass_only_gates_superseded=mass_ids)
gates['dependency_order'].append('Mass ceiling removed by user -> EU.19/EU.20 actual stiffness checks -> real interfaces/fillets/current full matrix -> physical calibration and final assembly mass/CG loads')
counts = {s:sum(g['status']==s for g in gates['gates']) for s in ['PASS','FAIL','OPEN']}
active_counts = {s:sum(g['status']==s and g['id'] not in mass_ids for g in gates['gates']) for s in ['PASS','FAIL','OPEN']}
summary = {'revision':'Rev.FD','recorded_utc':timestamp,'checkpoint_parent_head':parent,
           'previous_checkpoint':'mechanical/validation/rev-fc/summary.json',
           'gate_counts_including_history':counts,'counts_excluding_superseded_mass_only_gates':active_counts,
           'counts_are_not_completion_percentages':True,'mass_policy':policy,
           'frames':frames,'conditional_mass_load_review':mass_review,'executed_structural_runs':sum(len(f['cases']) for f in frames.values()),
           'production_ready':False,'all_remaining_digital_work_complete':False,
           'physical_tests_executed':False,'full_product_CFD_executed':False}
out = repo/'mechanical/validation/rev-fd';out.mkdir(parents=True,exist_ok=True)
(out/'gate-register.json').write_text(json.dumps(gates,indent=2)+'\n')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
sources = list((repo/'mechanical/cad').glob('*rev_fd.py'))
sources += [repo/'mechanical/cad/generate_frame_candidate_rev_eu19.py',repo/'mechanical/cad/generate_frame_candidate_rev_eu20.py',
            repo/'mechanical/cad/mesh_frame_screen_optimized_rev_fc.py',
            repo/'mechanical/cad/audit_frame_mesh_rev_fc.py',
            repo/'mechanical/cad/summarize_frame_results_rev_ev.py',
            repo/'mechanical/cad/audit_loaded_frame_envelope_rev_fb.py',
            repo/'mechanical/mass-policy-rev-fd.md',repo/'mechanical/fea/rear-frame-solver-manifest-rev-fd.json']
evidence = [p for name in ['rev-eu19','rev-ev19','rev-eu20','rev-ev20'] for p in (repo/'evidence'/name).rglob('*') if p.is_file()]
evidence += [repo/'evidence/rev-fd/frame-comparison.json',repo/'evidence/rev-fd/frame-comparison.png',repo/'evidence/rev-fd/vertical-load-input-guard.json',repo/'evidence/rev-fd/mass-load-review.json',repo/'evidence/rev-fd/EU19-EU20-boundary-comparison.json',repo/'evidence/rev-fd/EU18-EU19-boundary-comparison.json',repo/'evidence/rev-fd/geometry-figure.json',repo/'evidence/rev-fd/frame-candidate.png']
provenance = {'revision':'Rev.FD','recorded_utc':timestamp,'checkpoint_parent_head':parent,
              'source_hashes':{str(p.relative_to(repo)):sha(p) for p in sources},
              'evidence_hashes':{str(p.relative_to(repo)):sha(p) for p in evidence},
              'solver_executable_sha256':sha(repo.parent/'solvers/CalculiX/ccx_2.23/src/ccx_2.23'),
              'solver_version':'CalculiX 2.23','mass_ceiling_removed_by_user':True,
              'material_properties_and_assembly_not_qualified':True}
(repo/'evidence/rev-fd/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'counts_including_history':counts,'counts_excluding_old_mass_gates':active_counts,
                  'frames':{k:{'mass_g':v['CAD']['mass_g_at_catalog_density_1p22'],'LC4_mesh_comparison':v['LC4_mesh_comparison']} for k,v in frames.items()}},indent=2))
