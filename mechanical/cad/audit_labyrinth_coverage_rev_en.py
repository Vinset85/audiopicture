"""Independent Rev.EM coverage and axial LOS audit. No CFD/acoustic claim.

Run from repository root with CadQuery and Shapely installed.
Reads regenerated STEP, never trusts historical pass labels.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import cadquery as cq
from shapely.geometry import LineString, box
from shapely.ops import unary_union

parser = argparse.ArgumentParser()
parser.add_argument('--step', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
solid = cq.importers.importStep(str(args.step))
lower = [(17,20,14,54),(24,27,14,54),(17,20,62,102),
         (24,27,62,102),(17,20,110,150),(24,27,110,150)]
upper = [(17,62,315,318),(17,62,322,325),(17,62,329,332),
         (17,62,336,339),(17,62,343,346)]
vents = []
for prefix, rows, orientation in [('IL',lower,'V'),('IR',lower,'V'),
                                  ('UL',upper,'H'),('UR',upper,'H')]:
    for i, r in enumerate(rows, 1):
        a,b,c,d = r
        if prefix.endswith('R'):
            a,b = 320-b,320-a
        vents.append((f'{prefix}{i}',orientation,a,b,c,d))
# Actual Rev.EM chamber footprint, including its documented mirror offset.
footprint = unary_union([box(15,14,51,62),box(269.001,14,305.001,62),
                        box(15,315,51,363),box(269.001,315,305.001,363)])
rows=[]
for name,o,a,b,c,d in vents:
    if o=='V':
        centerline=LineString([((a+b)/2,c+1.5),((a+b)/2,d-1.5)])
        exact_area=(d-c-3)*3+math.pi*1.5**2
    else:
        centerline=LineString([(a+1.5,(c+d)/2),(b-1.5,(c+d)/2)])
        exact_area=(b-a-3)*3+math.pi*1.5**2
    # Fine circular tessellation used only for area overlap; axial witness is OCC.
    aperture=centerline.buffer(1.5,quad_segs=512)
    coverage=aperture.intersection(footprint).area/aperture.area
    x,y=(a+b)/2,(c+d)/2
    edge=cq.Edge.makeLine(cq.Vector(x,y,40.25),cq.Vector(x,y,33.0))
    distance=solid.val().distance(edge)
    rows.append({'vent':name,'nominal_area_mm2':exact_area,
                 'footprint_coverage_fraction':coverage,
                 'axial_ray':[[x,y,40.25],[x,y,33.0]],
                 'axial_obstacle_distance_mm':distance,
                 'axial_LOS_open':distance>1e-7})
bb=solid.val().BoundingBox()
result={'revision':'Rev.EN','source_sha256':hashlib.sha256(args.step.read_bytes()).hexdigest(),
        'classification':'CALCULATED_GEOMETRIC_AUDIT_NOT_ACOUSTIC_SIMULATION',
        'solid_valid':solid.val().isValid(),'solid_components':solid.solids().size(),
        'solid_volume_mm3':sum(s.Volume() for s in solid.solids().vals()),
        'bbox_mm':[bb.xlen,bb.ylen,bb.zlen],
        'z_extent_mm':[bb.zmin,bb.zmax],
        'fully_footprint_covered_vents':sum(r['footprint_coverage_fraction']>1-1e-9 for r in rows),
        'area_weighted_footprint_coverage_fraction':sum(r['nominal_area_mm2']*r['footprint_coverage_fraction'] for r in rows)/sum(r['nominal_area_mm2'] for r in rows),
        'open_axial_LOS_count':sum(r['axial_LOS_open'] for r in rows),
        'labyrinth_treatment_gate':'FAIL' if any(r['axial_LOS_open'] or r['footprint_coverage_fraction']<1-1e-9 for r in rows) else 'OPEN',
        'vents':rows,
        'limitations':['Footprint overlap alone does not prove treatment.',
                      'One open ray is sufficient to falsify universal LOS blockage.',
                      'Zero sampled open rays cannot prove acoustic attenuation.',
                      'Domain z33..40.25 is a local audit slab, not the full product CFD domain.']}
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='vents'},indent=2))
