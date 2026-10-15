"""Consolidate the three completed FG-frame weak-Y follow-up screens."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '069621b970e5b8b130c754e29dd4dac697ac8674'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def verify(data):
    for name, digest in data['source_sha256'].items():
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and sha(path) == digest, name


subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=ROOT, check=True)
mesh = read('evidence/rev-fg/mesh-upper/M0/mesh-report.json')
assembly = read('evidence/rev-fg/upper-mounts-chamfer/execution.json')
assert mesh['source_sha256'] == assembly['artifacts']['frame']['sha256']
assert sha(ROOT / assembly['artifacts']['frame']['file']) == mesh['source_sha256']
registry = read('mechanical/validation/rev-fg/gate-register.json')
added = []


def gate(status, scope, evidence):
    row = {'id': f'G{len(registry["gates"]) + 1:02d}', 'status': status, 'scope': scope, 'evidence': evidence}
    registry['gates'].append(row)
    added.append(row)


runs = []
for name, case in [('M0-LC4-LR-weakY', 'LC4'), ('M0-LC4-LL-weakY', 'LC4'), ('M0-LC3-weakY', 'LC3')]:
    path = f'evidence/rev-fh/{name}/{case}'
    e = read(path + '/execution.json')
    m = read(path + '/metrics.json')
    q = read(path + '/quadratic-dml-clearance.json')
    n = read(path + '/deformed-clearance.json')
    assert e['solver_execution_pass'] and e['exit_code'] == 0 and e['job_finished'] and not e['errors']
    assert e['input_sha256'] == sha(ROOT / path / 'frame.inp')
    assert e['runner_sha256'] == sha(ROOT / 'mechanical/cad/run_frame_screen_rev_fe.py')
    assert e['mesh_report'] == mesh and e['weak_global_axis'] == 'Y' and e['nonlinear_geometry']
    assert e['constitutive_assumptions']['E3'] == 380 and e['qualified_allowables'] is None
    log = (ROOT / path / 'solver.log').read_text()
    assert 'Job finished' in log and '*ERROR' not in log
    for data in [m, q, n]:
        verify(data)
    assert m['solver_execution_pass'] and m['final_step_time'] == 1
    assert m['force_balance_within_0_1_percent_or_0_001N'] and m['qualified_strength_margin'] is None
    assert q['final']['elements'] == mesh['elements']
    gate('PASS', f'FH {name}: actual solver completion and prescribed force-balance tolerance only',
         {'path': path + '/metrics.json', 'max_force_residual_N': max(map(abs, m['force_balance_residual_N'])),
          'allowable_force_residual_N': max(.001, .001 * sum(x*x for x in e['load_sum_N'])**.5)})
    if case == 'LC4':
        corner = max(m['corner_max_abs_UZ_mm'].values())
        gate('PASS' if corner <= 1 else 'FAIL', f'FH {name}: normalized 30 N corner displacement only',
             {'path': path + '/metrics.json', 'corner_UZ_mm': corner, 'limit_mm': 1})
    separated = q['final']['all_element_bounds_separated_from_DML_and_frontward_region']
    gate('PASS' if separated else 'OPEN', f'FH {name}: final full quadratic-element enclosure versus fixed DML only',
         {'path': path + '/quadratic-dml-clearance.json',
          'separation_lower_bound_mm': q['final']['conservative_DML_separation_lower_bound_mm'],
          'actual_deformable_assembly_contact_qualified': False})
    runs.append({'path': path, 'execution': e, 'metrics': m, 'quadratic_clearance': q, 'nodal_clearance': n})

registry.update(revision='Rev.FH', client_checkpoint_date='2026-10-15', checkpoint_parent_head=BASE)
counts = {s: sum(g['status'] == s for g in registry['gates']) for s in ['PASS', 'FAIL', 'OPEN']}
summary = {'revision': 'Rev.FH', 'client_checkpoint_date': '2026-10-15', 'checkpoint_parent_head': BASE,
           'executed_followup_runs': len(runs), 'same_geometry_and_mesh_as_FG': True,
           'gate_counts_including_history': counts, 'counts_are_not_completion_percentages': True,
           'new_gates': added, 'runs': runs, 'future_execution_policy': 'One verification at a time, validate and preserve before starting the next, per user request 2026-10-15.',
           'production_ready': False, 'full_assembly_FEA_complete': False, 'mesh_convergence_current_frame_verified': False,
           'print_orientation_selected_for_production': False, 'full_product_CFD_executed': False, 'physical_tests_executed': False}
out = ROOT / 'mechanical/validation/rev-fh'
out.mkdir(parents=True, exist_ok=True)
(out / 'gate-register.json').write_text(json.dumps(registry, indent=2) + '\n')
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
sources = [Path(__file__), ROOT / 'mechanical/digital-validation-rev-fh.md', ROOT / 'tools/package_rev_fh.py',
           ROOT / 'mechanical/cad/run_frame_screen_rev_fe.py', ROOT / 'mechanical/cad/summarize_frame_results_rev_fg.py',
           ROOT / 'mechanical/cad/audit_loaded_frame_envelope_rev_fe.py', ROOT / 'mechanical/cad/audit_quadratic_dml_clearance_rev_fd.py']
evidence = [p for p in (ROOT / 'evidence/rev-fh').rglob('*') if p.is_file() and p.name not in
            ['provenance.json', 'raw-artifact-index.json', 'github-publication.json', 'archive-tree-verification.json']]
provenance = {'revision': 'Rev.FH', 'checkpoint_parent_head': BASE,
              'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sources},
              'evidence_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(evidence)},
              'solver_version': 'CalculiX 2.23', 'solver_sha256': sha(ROOT.parent / 'solvers/CalculiX/ccx_2.23/src/ccx_2.23'),
              'mesh_sha256': sha(ROOT / 'evidence/rev-fg/mesh-upper/M0/mesh-data.npz'),
              'geometry_sha256': mesh['source_sha256'], 'qualified_material_or_process': False}
(ROOT / 'evidence/rev-fh/provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(json.dumps({'actual_runs': len(runs), 'new_gates': len(added), 'counts_with_history': counts}, indent=2))
