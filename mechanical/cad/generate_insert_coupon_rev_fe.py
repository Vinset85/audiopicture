"""Catalog-sized installation coupon, not a qualified product boss or fixture.

The outer cylinder/base and root fillet are engineering choices. The installation
hole follows the cited vendor nominal drawing; real printed fit remains untested.
"""
import argparse
import hashlib
import json
from pathlib import Path

import cadquery as cq
import trimesh

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
repo = Path(__file__).resolve().parents[2]
a.out.mkdir(parents=True, exist_ok=True)
catalog_path = repo/'mechanical/components/ruthex-m4-insert-candidate-rev-fe.json'
catalog = json.loads(catalog_path.read_text())
sources_path = repo/catalog['source']
sources = json.loads(sources_path.read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for source in sources['files']:
    assert sha(repo/source['file']) == source['sha256']

base_xy, floor, boss_od = 30.0, 2.5, 12.0
hole_d = catalog['manufacturer_nominal_installation_hole_diameter_mm']
depth = catalog['manufacturer_min_hole_depth_mm']
fillet = catalog['project_root_fillet_min_mm']
height = floor + depth
stock = cq.Workplane('XY').box(base_xy, base_xy, floor, centered=(True, True, False))
stock = stock.union(cq.Workplane('XY', origin=(0,0,floor)).circle(boss_od/2).extrude(depth)).clean()
roots = [e for e in stock.val().Edges() if e.geomType() == 'CIRCLE'
         and abs(e.Center().z-floor)<1e-7 and abs(e.radius()-boss_od/2)<1e-7]
assert len(roots) == 1
stock = stock.newObject(roots).fillet(fillet)
hole = cq.Workplane('XY', origin=(0,0,floor)).circle(hole_d/2).extrude(depth+.1)
coupon = stock.cut(hole).clean()
assert coupon.val().isValid() and coupon.solids().size() == 1
stem = 'AP22_INSERT_INSTALLATION_COUPON_REV_FE'
step, stl = a.out/(stem+'.step'), a.out/(stem+'.stl')
cq.exporters.export(coupon, str(step))
cq.exporters.export(coupon, str(stl), tolerance=.03, angularTolerance=.08)
back = cq.importers.importStep(str(step))
assert back.val().isValid() and back.solids().size() == 1
assert abs(back.val().Volume()-coupon.val().Volume())<1e-6
mesh = trimesh.load_mesh(stl)
assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
stl_error = abs(mesh.volume-coupon.val().Volume())/coupon.val().Volume()
assert stl_error < .005

# Check the complete nominal cylindrical void and a closed 2.5 mm floor.
probe = cq.Workplane('XY', origin=(0,0,floor+.0001)).circle(hole_d/2-.0001).extrude(depth-.0002)
void_overlap = sum(s.Volume() for s in coupon.intersect(probe).solids().vals())
floor_probe = cq.Workplane('XY').circle(hole_d/2-.0001).extrude(floor-.0001)
floor_present = sum(s.Volume() for s in coupon.intersect(floor_probe).solids().vals())
assert void_overlap < 1e-8
assert abs(floor_present-floor_probe.val().Volume())<1e-6
assert (boss_od-hole_d)/2 >= catalog['project_min_wall_from_hole_mm']
report = {
    'classification':'CALCULATED_INSTALLATION_COUPON_NOT_STRUCTURAL_QUALIFICATION',
    'catalog_part':catalog['part_number'], 'base_xy_mm':base_xy,
    'floor_mm':floor, 'boss_outer_diameter_mm':boss_od, 'overall_height_mm':height,
    'nominal_hole_diameter_mm':hole_d, 'nominal_hole_depth_mm':depth,
    'radial_wall_from_nominal_hole_mm':(boss_od-hole_d)/2,
    'root_fillet_mm':fillet, 'nominal_insert_bottom_clearance_mm':depth-catalog['nominal_length_mm'],
    'BREP_valid':True, 'solid_count':1, 'STEP_reimport_valid':True,
    'volume_mm3':coupon.val().Volume(), 'STL_watertight':True,
    'STL_volume_relative_error':stl_error, 'nominal_hole_obstruction_mm3':void_overlap,
    'floor_continuity_verified':True,
    'source_sha256':{str(q.relative_to(repo)):sha(q) for q in [catalog_path,sources_path,Path(__file__)]},
    'artifact_sha256':{step.name:sha(step),stl.name:sha(stl)},
    'printed':False, 'measured':False, 'qualified':False,
    'limits':['Not the complete frame boss/gusset or its stress boundary condition.',
              'Hole size is a manufacturer nominal; printer compensation and installation remain unqualified.',
              'The base is for handling and installation trials, not a validated pullout fixture.',
              'Strength, torque, hot performance, sample count and statistical acceptance require the P02 laboratory protocol.']
}
(a.out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
