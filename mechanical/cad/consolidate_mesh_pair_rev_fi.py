"""Audit one completed refined-mesh case against FH; no full convergence claim."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f45808a49d7e4ceba46a800b765b528b9fde5046'
RUN0 = 'evidence/rev-fh/M0-LC4-LR-weakY/LC4'
RUN1 = 'evidence/rev-fi/M1-LC4-LR-weakY/LC4'
MESH0 = 'evidence/rev-fg/mesh-upper/M0'
MESH1 = 'evidence/rev-fi/mesh/M1'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def verify_sources(data):
    for name, digest in data['source_sha256'].items():
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and sha(path) == digest, name


def load_patch(mesh, run):
    data = np.load(ROOT / mesh / 'mesh-data.npz')
    coords = dict(zip(map(int, data['tags']), data['coords']))
    load = {}
    active = False
    for line in (ROOT / run / 'frame.inp').read_text().splitlines():
        if line.upper().startswith('*CLOAD'):
            active = True
            continue
        if line.startswith('*'):
            active = False
        if active and line.strip():
            n, dof, f = line.split(',')
            assert int(dof) == 3
            load[int(n)] = load.get(int(n), 0.) + float(f)
    assert load and all(f < 0 for f in load.values())
    force = sum(load.values())
    assert abs(force + 30.) < 1e-8
    center = sum((coords[n] * f for n, f in load.items()), np.zeros(3)) / force
    points = sorted([*np.round(coords[n], 9).tolist(), round(f, 9)] for n, f in load.items())
    return {'loaded_nodes': len(load), 'force_N': force, 'original_load_centroid_mm': center.tolist(),
            'coordinate_force_samples_rounded_1e_9': points,
            'distribution': 'Equal force per node in the existing geometric corner set; not consistent surface traction.'}


subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=ROOT, check=True)
mesh0, mesh1 = read(MESH0 + '/mesh-report.json'), read(MESH1 + '/mesh-report.json')
assert mesh0['source_sha256'] == mesh1['source_sha256']
assert mesh1['source_sha256'] == sha(ROOT / 'evidence/rev-fg/upper-mounts-chamfer/AP22_FRAME_REV_FG.step')
assert mesh0['interface_geometry_sha256'] == mesh1['interface_geometry_sha256']
assert mesh0['mesher_sha256'] == mesh1['mesher_sha256'] == sha(ROOT / 'mechanical/cad/mesh_frame_interfaces_rev_fg.py')
assert mesh0['algorithm3d'] == mesh1['algorithm3d'] and mesh0['linear_mesh_optimizer'] == mesh1['linear_mesh_optimizer']
assert mesh1['size_mm'] < mesh0['size_mm'] and mesh1['elements'] > mesh0['elements']
quality = read(MESH1 + '/quality-audit.json')
verify_sources(quality)
assert quality['nonpositive_Jacobian_elements'] == 0
e0, e1 = read(RUN0 + '/execution.json'), read(RUN1 + '/execution.json')
for key in ['constitutive_assumptions', 'material_axes_global', 'weak_global_axis', 'loaded_corner',
            'nonlinear_geometry', 'anti_lift_normal_support_assumption', 'total_pad_penalty_N_per_mm',
            'gap_force_floor_N', 'contact_iteration_controls', 'runner_sha256']:
    assert e0[key] == e1[key], key
assert e1['runner_sha256'] == sha(ROOT / 'mechanical/cad/run_frame_screen_rev_fe.py')
assert e1['input_sha256'] == sha(ROOT / RUN1 / 'frame.inp')
assert e1['mesh_report'] == mesh1 and e1['solver_execution_pass'] and e1['exit_code'] == 0
assert e1['job_finished'] and not e1['errors'] and e1['qualified_allowables'] is None
assert 'Job finished' in (ROOT / RUN1 / 'solver.log').read_text()
m0, m1 = read(RUN0 + '/metrics.json'), read(RUN1 + '/metrics.json')
q0, q1 = read(RUN0 + '/quadratic-dml-clearance.json'), read(RUN1 + '/quadratic-dml-clearance.json')
for data in [m0, m1, q0, q1, read(RUN1 + '/deformed-clearance.json')]:
    verify_sources(data)
assert m1['final_step_time'] == 1 and m1['force_balance_within_0_1_percent_or_0_001N']
assert q1['final']['elements'] == mesh1['elements']
patch0, patch1 = load_patch(MESH0, RUN0), load_patch(MESH1, RUN1)
corner0 = max(m0['corner_max_abs_UZ_mm'].values())
corner1 = max(m1['corner_max_abs_UZ_mm'].values())
delta = abs(corner1 - corner0) / abs(corner1) * 100
stress0 = m0['nodal_extrapolated_stress_diagnostic']['von_mises_max_MPa']
stress1 = m1['nodal_extrapolated_stress_diagnostic']['von_mises_max_MPa']
pair = {'coarse_max_size_mm': mesh0['size_mm'], 'fine_max_size_mm': mesh1['size_mm'],
        'coarse_elements': mesh0['elements'], 'fine_elements': mesh1['elements'],
        'coarse_corner_UZ_mm': corner0, 'fine_corner_UZ_mm': corner1,
        'relative_difference_percent_of_fine': delta, 'comparison_threshold_percent': 5,
        'displacement_pair_within_5_percent': delta < 5,
        'coarse_load_patch': patch0, 'fine_load_patch': patch1,
        'same_load_points_and_forces_at_1e_9_precision': patch0['coordinate_force_samples_rounded_1e_9'] == patch1['coordinate_force_samples_rounded_1e_9'],
        'load_centroid_shift_mm': (np.array(patch1['original_load_centroid_mm']) - patch0['original_load_centroid_mm']).tolist(),
        'coarse_lower_support_nodes': e0['lower_unilateral_gap_contacts'],
        'fine_lower_support_nodes': e1['lower_unilateral_gap_contacts'],
        'coarse_nodal_von_mises_peak_MPa_diagnostic_only': stress0,
        'fine_nodal_von_mises_peak_MPa_diagnostic_only': stress1,
        'nodal_peak_difference_percent_of_fine_diagnostic_only': abs(stress1 - stress0) / stress1 * 100,
        'coarse_DML_separation_lower_bound_mm': q0['final']['conservative_DML_separation_lower_bound_mm'],
        'fine_DML_separation_lower_bound_mm': q1['final']['conservative_DML_separation_lower_bound_mm'],
        'full_mesh_convergence_verified': False,
        'limits': ['Two mesh levels and one load case only.',
                   'Load and support sets are selected on each mesh; actual load point equality is checked, while lower support discretization changes. The equal nodal load is a surrogate, not a resolved physical load footprint.',
                   'Full-element clearance bounds vary with subdivision and are not exact minimum distances.',
                   'Non-singular stress convergence and hotspot classification remain open.',
                   'Normalized material and ideal joints are not qualified physical properties or assembly contacts.']}
registry = read('mechanical/validation/rev-fh/gate-register.json')
added = []


def gate(status, scope, evidence):
    row = {'id': f'G{len(registry["gates"]) + 1:02d}', 'status': status, 'scope': scope, 'evidence': evidence}
    registry['gates'].append(row)
    added.append(row)


gate('PASS', 'FI M1: positive quadratic Jacobians only, not mesh convergence',
     {'path': MESH1 + '/quality-audit.json', 'elements': mesh1['elements'],
      'min_Jacobian_mm3': quality['min_adaptive_Jacobian_determinant_mm3']})
gate('PASS', 'FI M1 LC4 LR weakY: actual completion and prescribed force-balance tolerance only',
     {'path': RUN1 + '/metrics.json', 'residual_N': m1['force_balance_residual_N']})
gate('PASS' if corner1 <= 1 else 'FAIL', 'FI M1 LC4 LR weakY: normalized corner displacement only',
     {'path': RUN1 + '/metrics.json', 'corner_UZ_mm': corner1, 'limit_mm': 1})
gate('PASS' if q1['final']['all_element_bounds_separated_from_DML_and_frontward_region'] else 'OPEN',
     'FI M1 LC4 LR weakY: final quadratic-element bounds versus fixed DML only',
     {'path': RUN1 + '/quadratic-dml-clearance.json', 'separation_lower_bound_mm': pair['fine_DML_separation_lower_bound_mm']})
gate('PASS' if delta < 5 else 'FAIL', 'FI LC4 LR weakY: two-mesh displacement consistency only; ideal supports, not full convergence',
     {'path': 'mechanical/validation/rev-fi/mesh-pair.json', 'relative_difference_percent': delta, 'threshold_percent': 5})
registry.update(revision='Rev.FI', client_checkpoint_date='2026-10-16', checkpoint_parent_head=BASE)
counts = {s: sum(g['status'] == s for g in registry['gates']) for s in ['PASS', 'FAIL', 'OPEN']}
out = ROOT / 'mechanical/validation/rev-fi'
out.mkdir(parents=True, exist_ok=True)
summary = {'revision': 'Rev.FI', 'client_checkpoint_date': '2026-10-16', 'checkpoint_parent_head': BASE,
           'actual_new_solver_runs': 1, 'execution_policy': 'Serial: mesh, quality, one solve, result audits, preservation.',
           'gate_counts_including_history': counts, 'counts_are_not_completion_percentages': True,
           'new_gates': added, 'mesh_pair': pair, 'production_ready': False,
           'full_mesh_convergence_verified': False, 'full_assembly_FEA_complete': False,
           'full_product_CFD_executed': False, 'physical_tests_executed': False}
for name, value in [('gate-register.json', registry), ('summary.json', summary), ('mesh-pair.json', pair)]:
    (out / name).write_text(json.dumps(value, indent=2) + '\n')
sources = [Path(__file__), ROOT / 'mechanical/digital-validation-rev-fi.md', ROOT / 'tools/package_rev_fi.py',
           ROOT / 'mechanical/cad/mesh_frame_interfaces_rev_fg.py',
           ROOT / 'mechanical/cad/run_frame_screen_rev_fe.py', ROOT / 'mechanical/cad/audit_frame_mesh_rev_fc.py',
           ROOT / 'mechanical/cad/summarize_frame_results_rev_fg.py',
           ROOT / 'mechanical/cad/audit_loaded_frame_envelope_rev_fe.py',
           ROOT / 'mechanical/cad/audit_quadratic_dml_clearance_rev_fd.py']
evidence = [p for p in (ROOT / 'evidence/rev-fi').rglob('*') if p.is_file() and p.name not in
            ['provenance.json', 'raw-artifact-index.json', 'github-publication.json', 'archive-tree-verification.json']]
provenance = {'revision': 'Rev.FI', 'checkpoint_parent_head': BASE,
              'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sources},
              'evidence_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(evidence)},
              'solver_version': 'CalculiX 2.23',
              'solver_sha256': sha(ROOT.parent / 'solvers/CalculiX/ccx_2.23/src/ccx_2.23'),
              'geometry_sha256': mesh1['source_sha256'], 'qualified_material_or_process': False}
(ROOT / 'evidence/rev-fi/provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(json.dumps({'counts': counts, 'mesh_pair': pair}, indent=2))
