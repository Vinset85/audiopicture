"""Conditional gasket stack arithmetic, not a qualified seal or preload model.

Manufacturer ranges are transcribed from the locally archived Rogers sheet.
The only force calculation is explicitly at the sheet's 25% compression point.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'evidence/rev-fg/gasket-stack'
OUT.mkdir(parents=True, exist_ok=True)
source = ROOT / 'evidence/rev-fg/sources/poron-4701-30.pdf'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '9567c83b0d8d9e97e5477a4ccbef6c966d849ac3209b0aff4d1a9204922c4b68'

def stack(name, thickness, tolerance, gap):
    tmin, tmax = thickness*(1-tolerance), thickness*(1+tolerance)
    low, high = .7*tmax, .9*tmin
    cmin, cmax = 1-gap/tmin, 1-gap/tmax
    feasible = low <= high
    row = dict(name=name, nominal_free_thickness_mm=thickness,
               catalog_fractional_thickness_tolerance=tolerance,
               nominal_installed_gap_mm=gap,
               compression_extremes_with_exact_gap=[cmin,cmax],
               allowed_gap_for_10_to_30_percent_mm=[low,high],
               any_fixed_gap_can_cover_stock_tolerance=feasible,
               rigid_and_adhesive_stack_budget_below_nominal_mm=gap-low if feasible else None,
               rigid_and_adhesive_stack_budget_above_nominal_mm=high-gap if feasible else None,
               maximum_symmetric_gap_budget_at_current_nominal_mm=min(gap-low,high-gap) if feasible else None,
               optimal_gap_for_symmetric_budget_mm=(low+high)/2 if feasible else None,
               best_possible_symmetric_gap_budget_mm=(high-low)/2 if feasible else None,
               status='PASS_CONDITIONAL_EXACT_GAP_ARITHMETIC' if .1 <= cmin <= cmax <= .3 else 'FAIL_STOCK_TOLERANCE_WITH_FIXED_GAP')
    if feasible:
        assert math.isclose(1-low/tmax,.3,abs_tol=1e-12)
        assert math.isclose(1-high/tmin,.1,abs_tol=1e-12)
    return row

rows=[stack('DML rear, 320 kg/m3 catalog family',2,.10,1.6),
      stack('Frame-shell radial, 320 kg/m3 catalog family',1.57,.10,1.256),
      stack('Upper mount axial washers, 320 kg/m3 catalog family',1.57,.10,1.256),
      stack('Rejected 0.79 mm / 400 kg/m3 fixed-gap option',.79,.15,.632)]
assert [r['status'].startswith('PASS') for r in rows] == [True,True,True,False]
dml_area=300*380-288*368
washer_area=math.pi*(8.1**2-6.2**2)
forces=[]
for name,area,count in [('DML rear gasket',dml_area,1),('Mount washer',washer_area,4)]:
    forces.append({'part':name,'geometric_area_mm2_each':area,'count':count,
                   'catalog_25_percent_stress_range_kPa':[21,55],
                   'catalog_25_percent_typical_stress_kPa':35,
                   'reference_force_at_25_percent_N_each':[area*.021,area*.055],
                   'reference_typical_force_at_25_percent_N_each':area*.035,
                   'classification':'CATALOG_POINT_REFERENCE_ONLY_NOT_20_PERCENT_PRELOAD'})
report={'classification':'CALCULATED_CONDITIONAL_STACK_FROM_CATALOG_THICKNESS_BANDS',
        'status':'OPEN_MANUFACTURED_GAP_PRELOAD_AND_LEAKAGE_QUALIFICATION',
        'rows':rows,'force_references':forces,
        'production_tolerances_assigned':False,'force_at_20_percent_N':None,
        'required_digital_work':['Independent fixed DML retainer and over-travel capture; magnetic front is not the preload mechanism.',
                                 'Include adhesive and land-flatness contributions, and provide adjustable stops/shim selection and an inspection gauge.'],
        'required_measurements':['Actual gasket stock thickness, force-compression curves at operating temperatures and compression set.',
                                 'Installed gaps around the whole perimeter and each mounting washer, including shell clamping and print warp.',
                                 'Pressure-flow leakage and dynamic stiffness; a solid CAD gasket does not establish airtightness.'],
        'limits':['Rogers data are catalog references, not certified specification limits or AudioPicture material allowables.',
                  'No modulus is inferred from one 25% compression point; no force is interpolated to 20%.',
                  'The calculated gap budgets are requirements on the combined stack, not demonstrated FDM capabilities.',
                  'Sheet family ranges do not establish availability, adhesive option or qualification of a specific purchased MPN.'],
        'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,Path(__file__)]}}
(OUT/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
