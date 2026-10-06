"""Consolidate executed EU.13/EU.14 diagnostic screens; never infer product PASS."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

repo = Path(__file__).resolve().parents[2]
parent = '1fa4e20bd5b269b2e426532804c44618d667d176'
subprocess.run(['git', 'merge-base', '--is-ancestor', parent, 'HEAD'], cwd=repo, check=True)

def read(path):
    return json.loads((repo / path).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

gates = read('mechanical/validation/rev-fa/gate-register.json')
summary = read('mechanical/validation/rev-fa/summary.json')
frames = {}
next_gate = 61

def gate(status, scope, evidence):
    global next_gate
    gates['gates'].append({'id': f'G{next_gate:02d}', 'status': status,
                          'scope': scope, 'evidence': evidence})
    next_gate += 1

for revision in [13, 14]:
    cad_path = f'evidence/rev-eu{revision}'
    solver_path = f'evidence/rev-ev{revision}'
    cad = read(cad_path + '/execution.json')
    mesh = read(solver_path + '/M0/mesh-report.json')
    for source, digest in cad['input_sha256'].items():
        assert sha(repo / source) == digest, source
    assert mesh['source_sha256'] == cad['sha256'] == sha(repo / cad_path / 'AP22_FRAME_CANDIDATE_REV_EU.step')
    assert cad['valid'] and cad['reimport_valid'] and cad['solid_count'] == cad['reimport_solids'] == 1
    assert max(cad['collision_volume_mm3'].values()) < 1e-6
    assert cad['shell_clearance_mm'] >= 1 - 1e-6
    cases = {}
    for case in ['LC1', 'LC3', 'LC4']:
        run = 'M0-linear-MAT-B' if case == 'LC1' else 'M0-contactK100k-MAT-B'
        folder = repo / solver_path / run / case
        executed = json.loads((folder / 'execution.json').read_text())
        metric = json.loads((folder / 'metrics.json').read_text())
        assert executed['input_sha256'] == sha(folder / 'frame.inp')
        assert executed['mesh_report'] == mesh
        assert executed['solver_execution_pass'] and 'Job finished' in (folder / 'solver.log').read_text()
        assert metric['solver_execution_pass'] and metric['final_step_time'] == 1
        assert metric['force_balance_within_0_1_percent_or_0_001N']
        cases[case] = metric
    loaded = read(solver_path + '/M0-contactK100k-MAT-B/LC3/deformed-clearance.json')
    for source, digest in loaded['source_sha256'].items():
        assert sha(repo / source) == digest, source
    mass = cad['volume_mm3'] * .00122
    frames[f'EU{revision}'] = {'CAD': cad, 'mesh': mesh, 'cases': cases, 'LC3_deformed_node_audit': loaded}
    gate('PASS', f'EU.{revision} nominal CAD and 22 coarse collision checks only',
         {'volume_mm3': cad['volume_mm3'], 'shell_clearance_mm': cad['shell_clearance_mm'],
          'front_carrier_clearance_mm': cad['front_carrier_clearance_mm'],
          'exact_assembly_fillets_and_production_tolerances_qualified': False})
    gate('PASS' if mass <= 250 else 'FAIL', f'EU.{revision} homogeneous frame mass at catalog density, 250 g objective only',
         {'mass_g': mass, 'density_catalog_g_cm3': 1.22, 'limit_g': 250,
          'incomplete_interfaces_and_inserts_included': False})
    gate('PASS', f'EU.{revision} LC1 execution and force equilibrium only',
         {'max_displacement_mm': cases['LC1']['max_displacement_mm'],
          'mount_compliance_qualified': False, 'qualified_strength_margin': None})
    hit = loaded['nodes_predicted_inside_DML'] + loaded['nodes_predicted_frontward_of_DML_within_projection']
    gate('FAIL' if hit else 'PASS', f'EU.{revision} sampled deformed-node DML interference diagnostic under LC3 only',
         {'max_displacement_mm': cases['LC3']['max_displacement_mm'],
          'predicted_node_interference_count': hit, 'exact_deformed_element_clearance_verified': False,
          'DML_contact_or_strength_qualified': False})
    corner = max(cases['LC4']['corner_max_abs_UZ_mm'].values())
    gate('PASS' if corner <= 1 else 'FAIL', f'EU.{revision} LC4 lower-right applied 30 N, normalized nonlinear contact screen, 1 mm limit',
         {'max_corner_normal_mm': corner, 'all_corner_load_positions_swept': False,
          'current_mesh_convergence_and_qualified_strength_complete': False})

timestamp = datetime.now(timezone.utc).isoformat()
gates.update(revision='Rev.FB', recorded_utc=timestamp, checkpoint_parent_head=parent)
gates['dependency_order'].append('EU.13/EU.14 diagnostic results -> stiffness/mass and real interface redesign -> current-revision full LC1-LC7, mesh, material and contact qualification')
summary.update(revision='Rev.FB', recorded_utc=timestamp, checkpoint_parent_head=parent,
               gate_counts={s: sum(g['status'] == s for g in gates['gates']) for s in ['PASS', 'FAIL', 'OPEN']},
               frames_rev_fb=frames, production_ready=False, all_remaining_digital_work_complete=False)
out = repo / 'mechanical/validation/rev-fb'
out.mkdir(parents=True, exist_ok=True)
(out / 'gate-register.json').write_text(json.dumps(gates, indent=2) + '\n')
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
evidence = repo / 'evidence/rev-fb'
evidence.mkdir(parents=True, exist_ok=True)
sources = ['mechanical/cad/' + p for p in ['generate_frame_candidate_rev_eu13.py', 'generate_frame_candidate_rev_eu14.py',
           'mesh_frame_screen_rev_ev.py', 'run_frame_screen_rev_ev.py', 'summarize_frame_results_rev_ev.py',
           'audit_loaded_frame_envelope_rev_fb.py', 'consolidate_validation_rev_fb.py', 'plot_frame_diagnostics_rev_fb.py']]
provenance = {'revision': 'Rev.FB', 'recorded_utc': timestamp, 'checkpoint_parent_head': parent,
              'source_hashes': {p: sha(repo / p) for p in sources},
              'evidence_hashes': {str(p.relative_to(repo)): sha(p)
                                  for base in ['rev-eu13', 'rev-ev13', 'rev-eu14', 'rev-ev14']
                                  for p in (repo / 'evidence' / base).rglob('*') if p.is_file()},
              'material_properties_qualified': False, 'physical_tests_executed': False,
              'full_product_CFD_executed': False}
(evidence / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(json.dumps({'gate_counts': summary['gate_counts'], 'frames': {
    name: {'mass_g': value['CAD']['mass_g_at_catalog_density_1p22'],
           'LC1_U_mm': value['cases']['LC1']['max_displacement_mm'],
           'LC3_U_mm': value['cases']['LC3']['max_displacement_mm'],
           'LC4_corner_UZ_mm': max(value['cases']['LC4']['corner_max_abs_UZ_mm'].values()),
           'LC3_DML_node_audit': value['LC3_deformed_node_audit']['status']}
    for name, value in frames.items()}, 'production_ready': False}, indent=2))
