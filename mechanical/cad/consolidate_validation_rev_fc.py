"""Verify actual CAD/solver artifacts before consolidating the Rev.FC checkpoint."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

repo = Path(__file__).resolve().parents[2]
parent = '7a61afc609072f81a5ce00683a7f3da2161ec81d'
subprocess.run(['git', 'merge-base', '--is-ancestor', parent, 'HEAD'], cwd=repo, check=True)

def read(path):
    return json.loads((repo / path).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_sources(record, key):
    for path, digest in record[key].items():
        assert sha(repo / path) == digest, path

gates = read('mechanical/validation/rev-fb/gate-register.json')
summary = read('mechanical/validation/rev-fb/summary.json')
frames = {}

def gate(status, scope, evidence):
    gates['gates'].append({'id': f'G{len(gates["gates"])+1:02d}',
                          'status': status, 'scope': scope, 'evidence': evidence})

for rev in [15, 16, 17, 18]:
    path = f'evidence/rev-eu{rev}'
    cad = read(path + '/execution.json')
    verify_sources(cad, 'input_sha256')
    assert cad['sha256'] == sha(repo / path / 'AP22_FRAME_CANDIDATE_REV_EU.step')
    assert cad['valid'] and cad['reimport_valid'] and cad['solid_count'] == cad['reimport_solids'] == 1
    assert len(cad['collision_volume_mm3']) == 22 and max(cad['collision_volume_mm3'].values()) < 1e-6
    assert cad['shell_clearance_mm'] >= 1 - 1e-6 and cad['front_carrier_clearance_mm'] >= .5 - 1e-6
    frames[f'EU{rev}'] = {'CAD': cad, 'executed_cases': {}}
    gate('PASS', f'EU.{rev} nominal BREP/reimport and 22 coarse collision checks only',
         {'volume_mm3': cad['volume_mm3'], 'production_clearances_qualified': False})
    mass = cad['volume_mm3'] * .00122
    gate('PASS' if mass <= 250 else 'FAIL', f'EU.{rev} homogeneous candidate mass at catalog density only',
         {'mass_g': mass, 'density_catalog_g_cm3': 1.22, 'limit_g': 250,
          'unfinished_interfaces_and_inserts_included': False})

failed = read('evidence/rev-ev17/mesh-failures.json')
for attempt in failed['attempts']:
    assert sha(repo / attempt['log']) == attempt['log_sha256']
    assert 'Error' in (repo / attempt['log']).read_text()
gate('FAIL', 'EU.17 meshing, two actual attempts, no FEA executed', failed)

for rev, mesh, run, case in [
    (15, 'M0', 'M0-contactK100k-MAT-B', 'LC4'),
    (18, 'M0', 'M0-linear-MAT-B', 'LC1'),
    (18, 'M0', 'M0-pull-contactK100k-MAT-B', 'LC3'),
    (18, 'M0', 'M0-contactK100k-MAT-B', 'LC4'),
    (18, 'M1', 'M1-contactK100k-MAT-B', 'LC4'),
]:
    base = f'evidence/rev-ev{rev}'
    mesh_report = read(f'{base}/{mesh}/mesh-report.json')
    folder = repo / base / run / case
    executed = json.loads((folder / 'execution.json').read_text())
    metric = json.loads((folder / 'metrics.json').read_text())
    assert mesh_report['source_sha256'] == frames[f'EU{rev}']['CAD']['sha256']
    assert executed['mesh_report'] == mesh_report
    assert executed['input_sha256'] == sha(folder / 'frame.inp')
    assert executed['solver_execution_pass'] and 'Job finished' in (folder / 'solver.log').read_text()
    assert metric['solver_execution_pass'] and metric['final_step_time'] == 1
    assert metric['force_balance_within_0_1_percent_or_0_001N']
    key = f'{mesh}-{case}'
    frames[f'EU{rev}']['executed_cases'][key] = {'execution': executed, 'metrics': metric}
    if case == 'LC4':
        assert executed.get('loaded_corner', 'LR') == 'LR'
        value = max(metric['corner_max_abs_UZ_mm'].values())
        gate('PASS' if value <= 1 else 'FAIL', f'EU.{rev} {mesh} LC4 lower-right 30 N normalized nonlinear screen only',
             {'max_corner_normal_mm': value, 'limit_mm': 1, 'all_corners_swept': False,
              'qualified_material_or_strength': False})
    elif case == 'LC1':
        gate('PASS', 'EU.18 LC1 linear screen execution and equilibrium only',
             {'max_displacement_mm': metric['max_displacement_mm'], 'mount_compliance_qualified': False})
    else:
        audit = json.loads((folder / 'deformed-clearance.json').read_text())
        verify_sources(audit, 'source_sha256')
        hit = audit['nodes_predicted_inside_DML'] + audit['nodes_predicted_frontward_of_DML_within_projection']
        frames[f'EU{rev}']['LC3_deformed_node_audit'] = audit
        gate('FAIL' if hit else 'PASS', 'EU.18 LC3 sampled deformed-node DML interference diagnostic only',
             {'max_displacement_mm': metric['max_displacement_mm'], 'node_interference_count': hit,
              'continuous_deformed_element_clearance_verified': False})

for mesh in ['M0', 'M1']:
    quality = read(f'evidence/rev-ev18/{mesh}/quality-audit.json')
    verify_sources(quality, 'source_sha256')
    assert quality['nonpositive_Jacobian_elements'] == 0
    frames['EU18'][mesh + '_mesh_quality'] = quality

cases = frames['EU18']['executed_cases']
coarse = max(cases['M0-LC4']['metrics']['corner_max_abs_UZ_mm'].values())
fine = max(cases['M1-LC4']['metrics']['corner_max_abs_UZ_mm'].values())
change = abs(fine - coarse) / abs(fine) * 100
comparison = {'coarse_corner_UZ_mm': coarse, 'fine_corner_UZ_mm': fine,
              'relative_change_percent_fine_reference': change,
              'displacement_pair_below_5_percent': change < 5,
              'full_contract_mesh_convergence_verified': False,
              'limits': ['Two meshes only; mesh density and Netgen optimization change together.',
                         'Pad/anti-lift/corner sampling changes; loads remain normalized force distributions.',
                         'Unfilleted stress peaks remain unclassified and are not converged allowables.']}
frames['EU18']['LC4_mesh_comparison'] = comparison
gate('PASS' if change < 5 else 'FAIL', 'EU.18 two-mesh LC4 displacement comparison only, not full convergence', comparison)
gate('OPEN', 'EU.18 full current-revision structural qualification',
     {'all_LC1_LC7_material_CG_temperature_contact_buckling_cases_complete': False,
      'all_four_corner_load_positions_swept': False, 'qualified_allowables_available': False,
      'production_interfaces_and_fillets_complete': False})

mass_review = read('evidence/rev-fc/mass-budget-review.json')
verify_sources(mass_review, 'source_sha256')
gate('OPEN', 'Current complete-assembly mass and CG budget; historical 1.55 kg allocation is stale',
     {'actual_assembled_mass_g': None, 'frame_250g_target_revised': False,
      'evidence': 'evidence/rev-fc/mass-budget-review.json',
      'conditional_scenarios_are_not_product_mass_predictions': True})

timestamp = datetime.now(timezone.utc).isoformat()
gates.update(revision='Rev.FC', recorded_utc=timestamp, checkpoint_parent_head=parent)
gates['dependency_order'].append('EU.15-EU.18 actual diagnostics -> current load-path/interface/fillet redesign -> current-revision structural matrix and convergence -> physical correlation')
summary.update(revision='Rev.FC', recorded_utc=timestamp, checkpoint_parent_head=parent,
               gate_counts={s: sum(g['status'] == s for g in gates['gates']) for s in ['PASS', 'FAIL', 'OPEN']},
               frames_rev_fc=frames, production_ready=False, all_remaining_digital_work_complete=False)
summary['mass_budget_review_rev_fc'] = mass_review
out = repo / 'mechanical/validation/rev-fc'
out.mkdir(parents=True, exist_ok=True)
(out / 'gate-register.json').write_text(json.dumps(gates, indent=2) + '\n')
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
sources = [p for p in (repo / 'mechanical/cad').glob('*rev_fc.py')]
sources += [repo / f'mechanical/cad/generate_frame_candidate_rev_eu{n}.py' for n in [15, 16, 17, 18]]
sources += [repo / 'mechanical/cad/summarize_frame_results_rev_ev.py', repo / 'mechanical/cad/audit_loaded_frame_envelope_rev_fb.py']
evidence_files = [p for name in ['rev-eu15', 'rev-eu16', 'rev-eu17', 'rev-eu18', 'rev-ev15', 'rev-ev17', 'rev-ev18']
                  for p in (repo / 'evidence' / name).rglob('*') if p.is_file()]
evidence_files += [repo / 'evidence/rev-ev14/M0-contactK100k-MAT-B/LC4/lower-crossmember-diagnostic.json',
                   repo / 'evidence/rev-fc/EU14-EU15-boundary-comparison.json',
                   repo / 'evidence/rev-fc/EU14-EU18-boundary-comparison.json',
                   repo / 'evidence/rev-fc/mass-budget-review.json']
for rev in [15, 18]:
    verify_sources(read(f'evidence/rev-fc/EU14-EU{rev}-boundary-comparison.json'), 'sha256')
provenance = {'revision': 'Rev.FC', 'recorded_utc': timestamp, 'checkpoint_parent_head': parent,
              'source_hashes': {str(p.relative_to(repo)): sha(p) for p in sources},
              'evidence_hashes': {str(p.relative_to(repo)): sha(p) for p in evidence_files},
              'physical_tests_executed': False, 'full_product_CFD_executed': False,
              'material_properties_qualified': False}
(repo / 'evidence/rev-fc/provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(json.dumps({'counts': summary['gate_counts'], 'EU18_LC4_mesh_comparison': comparison}, indent=2))
