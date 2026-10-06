"""Check the nominal straight optical path against the frozen DML volume.

This is geometric interference, not an optical transmission simulation.
No sensor XY position within the current ENV region is assumed frozen.
"""
import argparse, json
from pathlib import Path
import cadquery as cq

p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
dml=box(10,310,10,390,3.3,9.3)
path=box(252,294,35,59,.5,12)
v=path.intersect(dml).val().Volume()
probes=[]
for x in [252,262.5,273,283.5,294]:
    for y in [35,41,47,53,59]:
        edge=cq.Edge.makeLine(cq.Vector(x,y,.5),cq.Vector(x,y,12))
        length=sum(e.Length() for e in edge.intersect(dml.val()).Edges())
        probes.append({'xy_mm':[x,y],'path_inside_DML_mm':length})
assert abs(v-6048)<1e-7
assert all(abs(q['path_inside_DML_mm']-6)<1e-7 for q in probes)
result={'classification':'CALCULATED_GEOMETRIC_PATH_AUDIT_NOT_OPTICAL_SIMULATION',
        'status':'FAIL_STRAIGHT_UNOBSTRUCTED_FRONT_PATH_FOR_CURRENT_ENV_SEED',
        'DML_volume_mm':[10,310,10,390,3.3,9.3],
        'ENV_XY_seed_mm':[252,294,35,59],'ENV_PCB_front_Z_seed_mm':12,
        'swept_path_DML_overlap_mm3':v,'projected_ENV_coverage_percent':100,
        'tested_normal_rays':len(probes),'rays_intersecting_DML':len(probes),'probes':probes,
        'analytical_scope':'Entire ENV XY rectangle is a subset of the hard DML projection; changing ENV Z from 12 to 13 cannot remove the intervening DML band.',
        'does_not_establish':['DML/fabric optical transmittance, scattering, lux accuracy or attenuation',
                            'A reflective or lateral optical path','A released relocation of the sensor'],
        'required_resolution':'Define and verify an actual perimeter/front optical path or relocate the light sensor; preserve DML, RF and removable-front requirements. Do not release the current normal-facing placement.',
        'sources':['mechanical/master-global-z-map-rev-a.md sections 3 and 9',
                   'mechanical/g1-dimensional-packaging-model-rev-a.md ENV XY seed',
                   'hardware/environment/sht45-opt3004-rev-a.md optical tunnel contract']}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='probes'},indent=2))
