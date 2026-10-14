"""Integrate catalog-size installation bosses and a larger DML edge clearance.

This is uninstalled, nominal CAD. Heat-set material flow, installed-insert
interface stiffness and printer compensation are not determined by this model.
The original EU.20 load interfaces remain identifiable for a controlled study.
"""
import argparse
import hashlib
import json
from pathlib import Path

import cadquery as cq
import trimesh
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
sources = {
    'frame': ROOT / 'evidence/rev-eu20/AP22_FRAME_CANDIDATE_REV_EU.step',
    'shell': ROOT / 'evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step',
    'front': ROOT / 'evidence/rev-fa/AP22_FRONT_CARRIER_OPTICAL_CANDIDATE_REV_FA.step',
    'catalog': ROOT / 'mechanical/components/ruthex-m4-insert-candidate-rev-fe.json',
}

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane('XY').box(x1-x0, y1-y0, z1-z0, centered=(False, False, False)).translate((x0, y0, z0))

def volume(w):
    total = 0.0
    for s in w.solids().vals():
        props = GProp_GProps()
        BRepGProp.VolumeProperties_s(s.wrapped, props, 1e-10, True, False)
        total += props.Mass()
    return total

def cylinder(x, y, r, z0, z1):
    return cq.Workplane('XY').center(x, y).circle(r).extrude(z1-z0).translate((0, 0, z0))

frame = cq.importers.importStep(str(sources['frame']))
mounts = {name: [x, 375.] for name, x in [('UL1', 37.5), ('UL2', 67.5), ('UR1', 252.5), ('UR2', 282.5)]}
modules = []
for x0 in [27.5, 242.5]:
    module = box(x0, x0+50, 366.8, 383.2, 23.4, 25.9)
    for x in [x0+10, x0+40]:
        module = module.union(cylinder(x, 375, 6, 25.9, 35))
    roots = [e for e in module.val().Edges() if e.geomType() == 'CIRCLE'
             and abs(e.Center().z-25.9) < 1e-6 and abs(e.radius()-6) < 1e-6]
    assert len(roots) == 2
    module = module.newObject(roots).fillet(2).clean()
    assert module.val().isValid() and module.solids().size() == 1
    frame = frame.union(module)
    modules.append({'base_xy_mm': [x0, x0+50, 366.8, 383.2], 'base_z_mm': [23.4, 25.9], 'root_fillet_mm': 2})

# Fill the former radius-3 bores before cutting the smaller installation hole.
for x, y in mounts.values():
    frame = frame.union(cylinder(x, y, 3.01, 25.8, 35))
    frame = frame.cut(cylinder(x, y, 2.8, 25.9, 35.1))

# Move the front structural band away from the DML rather than merely clipping
# it into a thin web. A solid 5.3 mm band replaces both front webs locally.
band = box(3.2, 316.8, 3.2, 396.8, 6, 10.3).cut(box(8.5, 311.5, 8.5, 391.5, 5.9, 10.4))
frame = frame.union(band).cut(box(8.5, 311.5, 8.5, 391.5, 3.3, 10.3)).clean()

keepouts = {
    'EX_L1': [37,99,50,110,9.3,36.3], 'EX_L2': [83,145,166,226,9.3,36.3],
    'EX_R1': [175,237,238,298,9.3,36.3], 'EX_R2': [223,285,88,148,9.3,36.3],
    'MAIN_C': [85,235,315,370,16,36.6], 'MAIN_P': [105,220,112,157,17,33],
    'VOICE': [119,201,20,102,11,18], 'RADAR': [249,287,184,216,0,18],
    'ENV': [252,294,35,59,11,18], 'SERVICE': [100,220,20,48,20,40],
    'ESP32_RF': [64,119.5,318.5,366.5,0,40], 'DML': [10,310,10,390,3.3,9.3],
}
collisions = {n: volume(frame.intersect(box(*v))) for n, v in keepouts.items()}
parts = {n: cq.importers.importStep(str(sources[n])) for n in ['shell', 'front']}
for n, part in parts.items():
    collisions[n] = volume(frame.intersect(part))
for i, (x, y) in enumerate([(70,394),(250,394),(70,6),(250,6),(6,135),(6,275),(314,135),(314,315)]):
    collisions[f'metal_target_{i+1}'] = volume(frame.intersect(box(x-3.5,x+3.5,y-3.5,y+3.5,4.1,5.1)))
holes = []
for name, (x, y) in mounts.items():
    hole_volume = volume(frame.intersect(cylinder(x,y,2.8,25.9,35)))
    floor = cylinder(x,y,2.8,23.4,25.9)
    missing_floor = volume(floor.cut(frame))
    holes.append({'name': name, 'hole_obstruction_mm3': hole_volume, 'missing_floor_mm3': missing_floor})
    assert hole_volume < 1e-6 and missing_floor < 1e-6
shape = frame.val()
assert shape.isValid() and frame.solids().size() == 1
assert max(collisions.values()) < 1e-6, collisions
step = a.out / 'AP22_FRAME_INTERFACE_CANDIDATE_REV_FG.step'
stl = a.out / 'AP22_FRAME_INTERFACE_CANDIDATE_REV_FG.stl'
cq.exporters.export(frame, str(step))
cq.exporters.export(frame, str(stl), tolerance=.05, angularTolerance=.1)
back = cq.importers.importStep(str(step))
mesh = trimesh.load_mesh(stl)
assert back.val().isValid() and back.solids().size() == 1
step_volume_error = abs(volume(frame)-volume(back))
print('STEP reimport volume difference mm3:', step_volume_error, flush=True)
# One part per million is an exchange-integrity check, not a part tolerance.
assert step_volume_error/max(volume(frame),1) < 1e-6
exchange_difference = {'original_minus_STEP_mm3': volume(frame.cut(back)), 'STEP_minus_original_mm3': volume(back.cut(frame))}
assert max(exchange_difference.values()) < 1e-4
assert mesh.is_watertight and mesh.is_winding_consistent
assert abs(mesh.volume-volume(frame))/volume(frame) < .005
result = {
    'revision': 'Rev.FG', 'classification': 'CALCULATED_NOMINAL_INSTALLATION_CAD_NOT_QUALIFIED_PRODUCT',
    'BREP_valid': True, 'solid_count': 1, 'STEP_reimport_valid': True, 'STL_watertight': True,
    'STEP_volume_absolute_error_mm3': step_volume_error,
    'STEP_relative_volume_limit': 1e-6, 'STEP_boolean_difference': exchange_difference,
    'volume_integration': 'OCC adaptive Gauss, per-face relative tolerance 1e-10',
    'volume_mm3': volume(frame), 'mass_g_at_catalog_density_1p22': volume(frame)*.00122,
    'mount_centers_xy_mm': mounts, 'bore_radius_mm': 2.8, 'bore_z_mm': [25.9,35],
    'boss_outer_diameter_mm': 12, 'floor_mm': 2.5, 'root_fillet_mm': 2, 'mount_modules': modules,
    'nominal_DML_front_band_XY_clearance_mm': 1.5, 'nominal_DML_rear_clearance_mm': 1,
    'front_band_solid_width_mm': 5.3, 'front_band_z_mm': [6,10.3],
    'hole_checks': holes, 'collision_volume_mm3': collisions,
    'part_clearances_mm': {n: shape.distance(v.val()) for n,v in parts.items()},
    'source_sha256': {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in [*sources.values(),Path(__file__)]},
    'artifacts': {f.name: {'bytes': f.stat().st_size, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()} for f in [step,stl]},
    'limitations': ['Nominal uninstalled holes, no print compensation or heat-set material-flow model.',
                    'Cleats, screws and actual wall contacts must be integrated before complete interface verification.',
                    'Boss root fillets are present; other inherited rib junctions remain unqualified.',
                    'Clearances are nominal, not a tolerance or deformed-assembly acceptance.',
                    'No strength, physical material property, manufacturing-process or production approval.'],
}
(a.out/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['revision','BREP_valid','solid_count','volume_mm3','mass_g_at_catalog_density_1p22','part_clearances_mm']},indent=2))
