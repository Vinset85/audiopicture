"""Executed optical packaging candidate; not a PCB or manufacturing release.

The entire maximum OPT3004 package projection and PCB-front Z are used as
conservative detector origins. This is geometrical visibility through an
ideal aperture, not radiometry, fabric transmission, or a measured tolerance.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import cadquery as cq

p = argparse.ArgumentParser()
for name in ('carrier', 'frame', 'shell', 'out'):
    p.add_argument('--' + name, type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane('XY').box(x1-x0, y1-y0, z1-z0,
        centered=(False, False, False)).translate((x0, y0, z0))


def volume(part):
    return sum(s.Volume() for s in part.solids().vals())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_export(part, name, stl=False):
    path = a.out / (name + '.step')
    cq.exporters.export(part, str(path))
    again = cq.importers.importStep(str(path))
    v0, v1 = volume(part), volume(again)
    bb = again.val().BoundingBox()
    report = {'step': path.name, 'sha256': sha(path),
              'valid': part.val().isValid(), 'solids': part.solids().size(),
              'reimport_valid': again.val().isValid(),
              'reimport_solids': again.solids().size(),
              'volume_mm3': v0, 'reimport_volume_mm3': v1,
              'bbox_mm': [bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]}
    assert report['valid'] and report['reimport_valid']
    assert report['solids'] == report['reimport_solids'] == 1
    assert abs(v0-v1) < 1e-6
    if stl:
        mesh = a.out / (name + '.stl')
        cq.exporters.export(part, str(mesh), tolerance=0.03, angularTolerance=0.1)
        report['stl'] = mesh.name
        report['stl_sha256'] = sha(mesh)
        report['stl_scope'] = 'Tessellated candidate; not manufacturing acceptance.'
    return report


# Rev.F global datum is authoritative for this front-carrier revision.
original = cq.importers.importStep(str(a.carrier)).translate((0, 0, 0.5))
frame = cq.importers.importStep(str(a.frame))
shell = cq.importers.importStep(str(a.shell))
cx, cy = 313.9, 47.0
width, height, radius = 6.6, 8.4, 1.2
window = (cq.Workplane('XY').rect(width, height).extrude(5)
          .edges('|Z').fillet(radius).translate((cx, cy, -0.5)))
carrier = original.cut(window).clean()
coupon = carrier.intersect(box(309.2, 319.2, 35, 59, 0.5, 2.3)).clean()

# PCB dimensions/thickness and mounting position are engineering design seeds.
# The 2.1 x 2.1 x 0.65 maximum package comes from TI DNP0006A.
# Using Z=PCB front for the ray origin covers any detector depth in the package.
pcb_front = 3.35
parts = {
    'OPT_head_PCB_envelope': box(cx-2.6, cx+2.6, 43, 51, pcb_front, pcb_front+0.8),
    'OPT3004_max_package_envelope': box(cx-1.05, cx+1.05, cy-1.05, cy+1.05,
                                      pcb_front-0.65, pcb_front),
    'C302_backside_envelope_seed': box(cx-0.9, cx+0.9, 49.25, 50.35,
                                      pcb_front+0.8, pcb_front+1.7),
}
keepouts = {
    'DML': box(10, 310, 10, 390, 3.3, 9.3),
    'ESP32_RF': box(64, 119.5, 318.5, 366.5, 0, 40),
    'RADAR': box(249, 287, 184, 216, 0, 18),
    'ENV_existing_seed': box(252, 294, 35, 59, 11, 18),
    # A full-height sidewall from Z0.5 overlaps the existing removable carrier.
    # Z4.1 is an integration reservation, NOT an already built/sealed sidewall.
    'future_ASA_right_wall_seed': box(317.8, 320, 0, 400, 4.1, 37.8),
    'frame_EU11': frame,
    'shell_EQ': shell,
}
stations = [(70,394), (250,394), (70,6), (250,6),
            (6,135), (6,275), (314,135), (314,315)]
targets = cq.Workplane('XY').newObject([cq.Compound.makeCompound([
    box(x-3.5, x+3.5, y-3.5, y+3.5, 4.1, 5.1).val() for x,y in stations])])
keepouts['eight_metal_target_envelopes'] = targets
collisions = {}
clearances = {}
for name, part in {'modified_carrier': carrier, **parts}.items():
    collisions[name] = {k: volume(part.intersect(v)) for k,v in keepouts.items()}
    clearances[name] = {k: part.val().distance(v.val()) for k,v in keepouts.items()}
for name, part in parts.items():
    collisions[name]['modified_carrier'] = volume(part.intersect(carrier))
    clearances[name]['modified_carrier'] = part.val().distance(carrier.val())

# No connection between the island and frame is credited; this models the
# allocated envelopes only. Check straight removal, not an arbitrary peel.
removal = []
for travel in [0, 0.5, 1, 3, 10, 40]:
    shifted = carrier.translate((0, 0, -travel))
    overlaps = {n: volume(shifted.intersect(v)) for n,v in parts.items()}
    removal.append({'frontward_travel_mm': travel, 'overlap_mm3': overlaps})

# Rounded aperture SDF: negative inside. Its convexity means that both segment
# endpoints inside imply the entire segment through the carrier is inside.
def aperture_sdf(x, y):
    qx, qy = abs(x-cx)-(width/2-radius), abs(y-cy)-(height/2-radius)
    return math.hypot(max(qx,0), max(qy,0)) + min(max(qx,qy),0) - radius

origins = [(cx+dx, cy+dy, pcb_front)
           for dx in [-1.05,0,1.05] for dy in [-1.05,0,1.05]]
angles = [0, 15, 30, 35, 40, 45, 57, 60]
angular = []
rays = []
for polar in angles:
    blocked = 0
    azimuths = [0] if polar == 0 else range(0,360,5)
    min_margin = float('inf')
    for x,y,z in origins:
        for az in azimuths:
            t = math.tan(math.radians(polar))
            dx, dy = t*math.cos(math.radians(az)), t*math.sin(math.radians(az))
            xyz = [(x+dx*(z-zz), y+dy*(z-zz), zz) for zz in [2.3,0.5]]
            margin = min(-aperture_sdf(xx,yy) for xx,yy,zz in xyz)
            blocked += margin < -1e-9
            min_margin = min(min_margin,margin)
            # An independent OCC line/material intersection validates a subset.
            if polar in [0,35,45] and az % 45 == 0:
                edge = cq.Edge.makeLine(cq.Vector(x,y,z), cq.Vector(*xyz[-1]))
                material_length = sum(e.Length() for e in edge.intersect(carrier.val()).Edges())
                dml_length = sum(e.Length() for e in edge.intersect(keepouts['DML'].val()).Edges())
                rays.append({'origin_mm':[x,y,z], 'polar_deg':polar,'azimuth_deg':az,
                             'rounded_window_clear':margin >= -1e-9,
                             'carrier_intersection_mm':material_length,
                             'DML_intersection_mm':dml_length})
                assert (material_length < 1e-7) == (margin >= -1e-9)
                assert dml_length < 1e-7
    angular.append({'polar_deg':polar,'rays':len(origins)*len(azimuths),
                    'blocked_by_carrier':blocked, 'minimum_margin_mm':min_margin})

# The source rectangle is inside the central straight part of the rounded port.
# Its minimum distance to the boundary is 3.3-1.05=2.25 mm (left/right).
# A circular cone footprint of radius d*tan(theta) is therefore contained
# for every source point and every azimuth when that radius <= 2.25 mm.
source_edge_margin = width/2-1.05
depth = pcb_front-0.5
analytic_angle = math.degrees(math.atan(source_edge_margin/depth))
allowance_35 = source_edge_margin-depth*math.tan(math.radians(35))
assert all(r['blocked_by_carrier']==0 for r in angular if r['polar_deg']<=35)
assert min(clearances['OPT_head_PCB_envelope'].values()) > 0
(a.out/'preflight-collisions.json').write_text(json.dumps(collisions,indent=2)+'\n')
print('Collision preflight: '+json.dumps({n:{k:v for k,v in group.items() if v>1e-6}
      for n,group in collisions.items()}),flush=True)
assert max(v for group in collisions.values() for v in group.values()) < 1e-6
assert max(v for row in removal for v in row['overlap_mm3'].values()) < 1e-6

exports = {'carrier': checked_export(carrier, 'AP22_FRONT_CARRIER_OPTICAL_CANDIDATE_REV_FA', True),
           'window_coupon': checked_export(coupon, 'AP22_OPTICAL_WINDOW_COUPON_REV_FA', True)}
for name, part in parts.items():
    exports[name] = checked_export(part, name + '_REV_FA')

result = {
    'revision':'Rev.FA', 'executed_at_utc':datetime.now(timezone.utc).isoformat(),
    'classification':'CALCULATED_OPTICAL_PACKAGING_CANDIDATE_NOT_RADIOMETRY_OR_PRODUCTION',
    'status':'PASS_NOMINAL_35_DEG_GEOMETRIC_FIELD_ONLY',
    'input_sha256':{str(path):sha(path) for path in [a.carrier,a.frame,a.shell,Path(__file__)]},
    'carrier_global_Z_translation_mm':0.5,
    'unmodified_carrier_volume_mm3':volume(original),
    'removed_carrier_volume_mm3':volume(original)-volume(carrier),
    'window_xyz_mm':[cx-width/2,cx+width/2,cy-height/2,cy+height/2,0.5,2.3],
    'window_corner_radius_mm':radius,
    'remaining_nominal_carrier_ligaments_mm':[cx-width/2-309.2,319.2-(cx+width/2)],
    'optical_center_xy_mm':[cx,cy],
    'PCB_front_Z_mm':pcb_front, 'PCB_thickness_seed_mm':0.8,
    'future_right_wall_seed_xyz_mm':[317.8,320,0,400,4.1,37.8],
    'future_wall_scope':'Reservation only. The earlier Z0.5 full-height hypothesis intersected the carrier by 1034.699339 mm3. The enclosure and its front seal still need design; this result does not close them.',
    'whole_package_source_rectangle_mm':[cx-1.05,cx+1.05,cy-1.05,cy+1.05],
    'conservative_source_Z_mm':pcb_front,
    'analytical_all_azimuth_clear_half_angle_deg':analytic_angle,
    '35_deg_remaining_combined_lateral_allowance_mm':allowance_35,
    'allowance_rule':'A conservative registration/depth allocation obeys norm(delta_XY) + tan(35deg)*positive_delta_Z <= remaining allowance. This is available geometric margin, NOT a measured manufacturing tolerance.',
    'aperture_proof':'Rounded port is convex; the entire source rectangle is at least 2.25 mm from its boundary. Dilating it by a disk of radius (3.35-0.5)*tan(35deg) stays inside, so every azimuth through the complete thickness is clear. Conservative source plane is behind the complete optical package.',
    'angular_sweep':angular, 'independent_OCC_rays':rays,
    'collision_volume_mm3':collisions, 'minimum_clearances_mm':clearances,
    'frontward_removal_samples':removal, 'exports':exports,
    'catalog_basis':{'package':'TI OPT3004DNPR DNP0006A maximum 2.1 x 2.1 x 0.65 mm',
                     'field_of_view':'TI SBOS929A section 9.1.2 recommends at least +/-35 degrees; 57 degrees half-power response is a typical catalog response, not a mechanical clearance requirement.',
                     'source':'https://www.ti.com/lit/ds/symlink/opt3004.pdf'},
    'open_items':['Fixed island retention/bracket and exact connector or flex routing',
                  'Native PCB layout and electrical/mechanical verification after physical split',
                  'Registration and fabrication tolerances; window ligament strength',
                  'Dark baffle, seal, LED leakage, fabric sag and optical calibration',
                  'Actual tilted/peel removal and strain relief',
                  'SHT45 isolated passive chamber remains separate and unvalidated'],
    'production_ready':False,
}
(a.out/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in
                 ['independent_OCC_rays','collision_volume_mm3','minimum_clearances_mm',
                  'frontward_removal_samples','exports']},indent=2),flush=True)
