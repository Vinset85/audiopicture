"""Track the heavier candidates without reinstating a mass acceptance ceiling."""
from pathlib import Path
import hashlib
import json

repo = Path(__file__).resolve().parents[2]
prior_path = repo / 'evidence/rev-fc/mass-budget-review.json'
prior = json.loads(prior_path.read_text())
for source, expected in prior['source_sha256'].items():
    assert hashlib.sha256((repo/source).read_bytes()).hexdigest() == expected, source
sources = [prior_path, Path(__file__), repo/'mechanical/mass-policy-rev-fd.md']
scenarios = []
for revision in [19, 20]:
    path = repo / f'evidence/rev-eu{revision}/execution.json'
    cad = json.loads(path.read_text())
    assert cad['valid'] and cad['reimport_valid']
    sources.append(path)
    frame_g = cad['mass_g_at_catalog_density_1p22']
    for old in prior['scenarios'][:2]:
        total_g = old['conditional_total_with_other_old_reserves_g'] - old['frame_g'] + frame_g
        scenarios.append({
            'candidate': f'EU.{revision}', 'frame_calculated_g': frame_g,
            'ASA_density_assumption_g_cm3': old['ASA_density_sensitivity_g_cm3'],
            'conditional_total_with_other_old_reserves_g': total_g,
            'conditional_vertical_load_4g_min70_N': max(70., 4*total_g/1000*9.80665),
            'actual_assembly_mass_or_load_qualification': False,
        })
report = {
    'revision': 'Rev.FD',
    'classification': 'CALCULATED_CONDITIONAL_RECONCILIATION_NOT_ASSEMBLED_MASS',
    'frame_mass_ceiling_g': None, 'old_product_1700g_is_rejection_gate': False,
    'scenarios': scenarios, 'actual_assembled_mass_g': None,
    'actual_assembled_CG_mm': None, 'final_vertical_load_N': None,
    'additional_90N_screen_is_conditional_sensitivity_only': True,
    'limits': prior['limits'][:3] + [
        'No physical property or budget allowance is created by authorizing more mass.',
        'The 70 N minimum is retained; final loads must follow actual assembly mass/CG and installation requirements.',
        'The 90 N screening seed does not certify the frame, wall anchors, insert pull-out or product mass capacity.',
    ],
    'source_sha256': {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
}
out = repo/'evidence/rev-fd/mass-load-review.json'
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
