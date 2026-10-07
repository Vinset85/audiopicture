"""Reconcile historical allocations against actual CAD; no assembled mass claim."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

repo = Path(__file__).resolve().parents[2]
def read(path):
    return json.loads((repo / path).read_text())

frame = read('evidence/rev-eu18/execution.json')
shell = read('evidence/rev-eq/execution.json')
front = read('evidence/rev-fa/independent-artifact-check.json')
old = {'DML_exciters_bonding': 718., 'front_system': 125., 'electronics_harness': 250.,
       'frame': 220., 'shell': 150., 'product_hardware': 85.}
assert sum(old.values()) == 1548.
exciter = {'classification': 'CATALOG_NOT_MEASURED', 'part': 'DAEX25FHE-4',
           'unit_net_mass_g': 110.9, 'quantity': 4, 'total_net_mass_g': 4*110.9,
           'historical_budget_g': 452.,
           'source': 'https://www.audiophonics.fr/images2/8713/295-224-dayton-audio-daex25fhe-4-spec-sheet.pdf',
           'source_author': 'Dayton Audio', 'sheet_revision_as_printed': '2/5/2014',
           'source_host_note': 'Manufacturer-authored datasheet retained by distributor; net weight, not shipping weight or moving mass.',
           'physical_units_not_weighed': True}
scenarios = []
for fm in [frame['mass_g_at_catalog_density_1p22'], 275., 300.]:
    for rho in [1.05, 1.10]:
        sm = shell['solid_volume_mm3'] * rho / 1000
        # Keep all other OLD reserves unchanged. This is a what-if subtotal,
        # not a sum of complete/current manufactured component masses.
        conditional = sum(old.values()) - old['frame'] - old['shell'] - 452 + fm + sm + exciter['total_net_mass_g']
        scenarios.append({'frame_g': fm, 'frame_classification': 'CALCULATED_CAD_AT_CATALOG_DENSITY' if fm == frame['mass_g_at_catalog_density_1p22'] else 'HYPOTHETICAL_TRADEOFF_NOT_A_CAD_RESULT',
                          'ASA_density_sensitivity_g_cm3': rho, 'shell_candidate_g': sm,
                          'conditional_total_with_other_old_reserves_g': conditional,
                          'difference_from_1700g_target_g': conditional-1700})
paths = ['mechanical/system-mass-cg-budget-rev-a.md',
         'mechanical/rear-structural-frame-rev-b.md',
         'mechanical/rear-frame-parametric-fea-rev-b.md',
         'mechanical/front-frame-carrier-cad-kernel-generation-rev-a.md',
         'evidence/rev-eu18/execution.json', 'evidence/rev-eq/execution.json',
         'evidence/rev-fa/independent-artifact-check.json',
         'mechanical/cad/review_mass_budget_rev_fc.py']
r = {'revision': 'Rev.FC', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
     'classification': 'CALCULATED_RECONCILIATION_WITH_EXPLICIT_CATALOG_DATA_AND_ASSUMPTIONS',
     'historical_allocations_g': old, 'historical_total_g': sum(old.values()),
     'frame_target_g': 250, 'frame_target_excludes_inserts_and_metal_cleats': True,
     'target_origin': 'Rear structural frame Rev.B section 24; topology review required before accepting an increase.',
     'target_is_physical_material_limit': False,
     'original_frame_working_range_g': [170, 280], 'product_mass_target_g': 1700,
     'vertical_design_load_baseline_N': 70, 'selected_exciter_catalog': exciter,
     'ASA_density_classification': 'ASSUMED_SENSITIVITY_ALREADY_USED_IN_REPOSITORY_NOT_QUALIFIED_PRINT_DENSITY',
     'shell_EQ_volume_mm3': shell['solid_volume_mm3'], 'scenarios': scenarios,
     'actual_assembled_mass_g': None, 'numeric_assembled_CG_mm': None,
     'budget_headroom_released_g': None, 'frame_target_revised': False,
     'limits': ['EQ shell/labyrinth is incomplete: sidewalls, service, seals and connections are not fully modeled.',
                'Old front reserve contains polymer/magnets/adhesive. The FA carrier alone cannot replace that complete reserve.',
                'Electronics, cables, fasteners and printed densities are unqualified; exact DMU mass distribution is absent.',
                '275/300 g scenarios illustrate budget effects only; they are not simulated or accepted frame designs.',
                '70 N remains the minimum seed, not proof of actual product/anchor capacity. Recompute loads/CG when assembly masses are known.'],
     'source_sha256': {p: hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in paths}}
(repo/'evidence/rev-fc/mass-budget-review.json').write_text(json.dumps(r, indent=2)+'\n')
print(json.dumps({'historical_total_g': r['historical_total_g'], 'scenarios': scenarios, 'actual_assembled_mass_g': None}, indent=2))
