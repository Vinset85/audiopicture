"""Locate an unresolved stress peak using existing M0/M1 fields; no new solve.

Proximity to ideal constraints is evidence for follow-up, not proof that a peak
is a mathematical singularity or permission to exclude it from acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--out', type=Path, default=ROOT / 'evidence/rev-fi/lower-capture-audit')
p.add_argument('--preview', type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
a.preview.parent.mkdir(parents=True, exist_ok=True)
sources = {Path(__file__)}


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path):
    path = ROOT / path
    sources.add(path)
    return json.loads(path.read_text())


def verify_sources(data):
    for name, digest in data['source_sha256'].items():
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and sha(path) == digest, name


step = ROOT / 'evidence/rev-fg/upper-mounts-chamfer/AP22_FRAME_REV_FG.step'
sources.add(step)
cad = cq.importers.importStep(str(step)).val()
assert cad.isValid() and len(cad.Solids()) == 1
edges, faces = cad.Edges(), cad.Faces()


def nearest(shapes, vertex, count=3):
    rows = []
    for i, shape in enumerate(shapes):
        b = shape.BoundingBox()
        rows.append({'index_in_this_STEP_import': i, 'type': shape.geomType(),
                     'distance_mm': shape.distance(vertex),
                     'bbox_mm': [b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax]})
    return sorted(rows, key=lambda r: r['distance_mm'])[:count]


runs, plot_data = [], []
for label, mesh, run in [
    ('M0', 'evidence/rev-fg/mesh-upper/M0', 'evidence/rev-fh/M0-LC4-LR-weakY/LC4'),
    ('M1', 'evidence/rev-fi/mesh/M1', 'evidence/rev-fi/M1-LC4-LR-weakY/LC4')]:
    metrics = read(run + '/metrics.json')
    verify_sources(metrics)
    report = read(mesh + '/mesh-report.json')
    assert report['source_sha256'] == sha(step)
    data_path = ROOT / mesh / 'mesh-data.npz'
    sources.add(data_path)
    data = np.load(data_path)
    tags, xyz = data['tags'].astype(int), data['coords']
    idx = {int(n): i for i, n in enumerate(tags)}
    sets = read(mesh + '/sets.json')
    stress, active = {}, False
    frd = ROOT / run / 'frame.frd'
    sources.add(frd)
    with frd.open() as f:
        for line in f:
            if line.startswith(' -4'):
                active = line.split()[1] == 'STRESS'
                if active:
                    stress = {}
            elif line.startswith(' -3'):
                active = False
            elif active and line.startswith(' -1'):
                stress[int(line[3:13])] = [float(line[j:j+12]) for j in range(13, len(line.rstrip()), 12)]
    # FRD also contains zero-stress ground nodes belonging only to GAPUNI.
    # Audit their identity explicitly, then use the solid mesh nodes only.
    assert set(tags).issubset(stress)
    ground_count = len(sets['PAD_L']) + len(sets['PAD_R'])
    ground_tags = set(range(int(tags.max()) + 1, int(tags.max()) + 1 + ground_count))
    assert set(stress) - set(tags) == ground_tags
    assert all(all(v == 0 for v in stress[n]) for n in ground_tags)
    s = np.array([stress[n] for n in tags])
    assert s.shape == (len(tags), 6) and np.isfinite(s).all()
    xx, yy, zz, xy, yz, zx = s.T
    vm = np.sqrt(.5*((xx-yy)**2 + (yy-zz)**2 + (zz-xx)**2) + 3*(xy*xy + yz*yz + zx*zx))
    peak = int(vm.argmax())
    assert np.isclose(vm[peak], metrics['nodal_extrapolated_stress_diagnostic']['von_mises_max_MPa'], rtol=1e-12)
    support = xyz[[idx[n] for n in sets['ANTILIFT']]]
    nearest_distance, nearest_index = cKDTree(support).query(xyz[peak])
    # Distance to the nominal rectangle used to select z=35 constrained nodes.
    # It is not an assertion that a physical, fully contacting rectangle exists.
    rect = xyz.copy()
    rect[:, 0] = np.clip(rect[:, 0], 151., 169.)
    rect[:, 1] = np.clip(rect[:, 1], 10., 20.)
    rect[:, 2] = 35.
    dist = np.linalg.norm(xyz - rect, axis=1)
    bins = []
    trees = {name: cKDTree(xyz[[idx[n] for n in sets[name]]])
             for name in ['UL1', 'UL2', 'UR1', 'UR2', 'PAD_L', 'PAD_R', 'ANTILIFT', 'CORNER_LR']}
    edges_mm = [0., 1., 2., 3., 5., 10., 20., float('inf')]
    for low, high in zip(edges_mm[:-1], edges_mm[1:]):
        mask = (dist >= low) & (dist < high)
        band_peak = int(np.flatnonzero(mask)[vm[mask].argmax()]) if mask.any() else None
        bins.append({'lower_mm': low, 'upper_mm': high if np.isfinite(high) else None,
                     'nodes': int(mask.sum()), 'max_nodal_von_mises_MPa': float(vm[band_peak]) if mask.any() else None,
                     'peak_xyz_mm': xyz[band_peak].tolist() if mask.any() else None,
                     'distances_to_boundary_or_load_nodes_mm': {name: float(tree.query(xyz[band_peak])[0]) for name, tree in trees.items()} if mask.any() else None})
    vertex = cq.Vertex.makeVertex(*map(float, xyz[peak]))
    remote_vertex = cq.Vertex.makeVertex(*bins[-1]['peak_xyz_mm'])
    bins[-1]['nearest_CAD_edges'] = nearest(edges, remote_vertex, count=1)
    bins[-1]['nearest_CAD_faces'] = nearest(faces, remote_vertex, count=1)
    runs.append({'mesh': label, 'source_run': run, 'peak_node': int(tags[peak]),
                 'peak_xyz_mm': xyz[peak].tolist(), 'peak_nodal_von_mises_MPa': float(vm[peak]),
                 'peak_is_prescribed_displacement_node': int(tags[peak]) in sets['ANTILIFT'],
                 'nearest_anti_normal_node_mm': support[int(nearest_index)].tolist(),
                 'distance_to_nearest_anti_normal_node_mm': float(nearest_distance),
                 'distance_to_selection_rectangle_mm': float(dist[peak]),
                 'nearest_CAD_edges': nearest(edges, vertex), 'nearest_CAD_faces': nearest(faces, vertex),
                 'normal_reaction_N': metrics['anti_lift_normal_reaction_N'], 'distance_band_diagnostics': bins})
    plot_data.append((label, xyz, vm, support, peak, bins))

reactions = []
for path in ['evidence/rev-fg/upper-frame-runs/M0-LC1-100N-weakY/LC1',
             'evidence/rev-fh/M0-LC3-weakY/LC3', 'evidence/rev-fh/M0-LC4-LL-weakY/LC4',
             'evidence/rev-fh/M0-LC4-LR-weakY/LC4', 'evidence/rev-fi/M1-LC4-LR-weakY/LC4']:
    m, e = read(path + '/metrics.json'), read(path + '/execution.json')
    verify_sources(m)
    assert e['solver_execution_pass'] and m['final_step_time'] == 1
    assert e['mesh_report']['source_sha256'] == sha(step) and e['weak_global_axis'] == 'Y'
    reactions.append({'path': path, 'case': e['case'], 'loaded_corner': e['loaded_corner'],
                      'normal_reaction_N': m['anti_lift_normal_reaction_N']})

result = {'classification': 'POSTPROCESSING_EXISTING_NORMALIZED_SCREENS_NOT_NEW_FEA_OR_STRENGTH_QUALIFICATION',
          'client_date': '2026-10-16', 'runs': runs, 'available_case_reactions': reactions,
          'maximum_absolute_normal_reaction_N_in_available_cases': max(abs(r['normal_reaction_N']) for r in reactions),
          'physical_hotspot_classification': 'OPEN: proximity to the ideal support established; cause and non-singular peak unresolved',
          'real_lower_capture_qualified': False, 'full_stress_convergence_verified': False,
          'limits': ['Nodal extrapolated stress, not integration-point stress or an orthotropic failure index.',
                     'Distance bands are diagnostic; no exclusion radius or acceptance rule is introduced.',
                     'Proximity alone cannot distinguish geometric stress concentration from a constraint singularity.',
                     'Case envelope is incomplete; reactions are model loads, not measured capacities or production design loads.'],
          'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(sources)}}
(a.out / 'audit.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')

plt.rcParams.update({'font.size': 10, 'svg.hashsalt': 'AudioPicture-FI-lower-capture'})
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), constrained_layout=True)
vmax = max(float(v.max()) for _, _, v, _, _, _ in plot_data)
for ax, (label, xyz, vm, support, peak, bins) in zip(axes[:2], plot_data):
    sel = (xyz[:, 0] >= 145) & (xyz[:, 0] <= 177) & (xyz[:, 1] >= 9.999) & (xyz[:, 1] <= 10.001) & (xyz[:, 2] >= 30)
    sc = ax.scatter(xyz[sel, 0], xyz[sel, 2], c=vm[sel], s=13, cmap='viridis', vmin=0, vmax=vmax)
    ax.plot([151, 169], [35, 35], color='crimson', lw=3, label='Selezione vincolo ideale, Z=35')
    ax.scatter([xyz[peak, 0]], [xyz[peak, 2]], marker='*', s=120, facecolor='white', edgecolor='black', zorder=5)
    ax.set(title=f'{label}: nodi sulla faccia Y=10 mm', xlabel='X [mm]', ylabel='Z [mm]', ylim=(34.7, 37.2))
    ax.legend(loc='upper left', fontsize=7)
    ax.grid(alpha=.2)
fig.colorbar(sc, ax=axes[:2], label='von Mises nodale estrapolato [MPa]')
for label, xyz, vm, support, peak, bins in plot_data:
    axes[2].plot(range(len(bins)), [b['max_nodal_von_mises_MPa'] for b in bins], marker='o', label=label)
axes[2].set_xticks(range(7), ['0–1', '1–2', '2–3', '3–5', '5–10', '10–20', '≥20'], rotation=30)
axes[2].set(xlabel='Distanza dal rettangolo di selezione [mm]', ylabel='Massimo nodale per fascia [MPa]', title='Diagnostica: nessuna esclusione del picco')
axes[2].legend()
axes[2].grid(alpha=.2)
fig.suptitle('LC4 30 N, asse debole Y — picco vicino al vincolo inferiore ideale, qualificazione OPEN')
fig.savefig(a.out / 'hotspot.svg', metadata={'Date': None})
fig.savefig(a.preview, dpi=160)
plt.close(fig)
print(json.dumps({'peaks': [{k: r[k] for k in ['mesh', 'peak_xyz_mm', 'peak_nodal_von_mises_MPa', 'distance_to_nearest_anti_normal_node_mm']} for r in runs],
                  'maximum_normal_reaction_N': result['maximum_absolute_normal_reaction_N_in_available_cases']}, indent=2))
