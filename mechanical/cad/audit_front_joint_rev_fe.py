"""Exhibit an unmanaged front-joint air path in the actual candidate assembly.

Each entire straight segment is checked against BREP, not point sampling. A
clear polyline establishes geometric continuity, not airflow or acoustic loss.
"""
from pathlib import Path
import hashlib
import json
import cadquery as cq
repo=Path(__file__).resolve().parents[2]
paths={'shell':'evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step',
       'frame':'evidence/rev-eu22/AP22_FRAME_CANDIDATE_REV_EU.step',
       'front':'evidence/rev-fa/AP22_FRONT_CARRIER_OPTICAL_CANDIDATE_REV_FA.step'}
shapes={name:cq.importers.importStep(str(repo/path)).val() for name,path in paths.items()}
shapes['DML_hard_box']=cq.Workplane('XY').box(300,380,6,centered=(False,False,False)).translate((10,10,3.3)).val()
trials=[]
for y in [120,180,250,300]:
    points=[[-1,y,3],[2.7,y,3],[2.7,y,36.5],[20,y,36.5]]
    segments=[]
    for start,end in zip(points,points[1:]):
        edge=cq.Edge.makeLine(cq.Vector(*start),cq.Vector(*end))
        gaps={name:s.distance(edge) for name,s in shapes.items()}
        segments.append({'from_mm':start,'to_mm':end,'BREP_min_distance_mm':gaps})
    clearance=min(v for s in segments for v in s['BREP_min_distance_mm'].values())
    trials.append({'Y_mm':y,'polyline_mm':points,'segments':segments,
                   'minimum_centerline_clearance_mm':clearance,
                   'continuous_positive_clearance_path':clearance>1e-6})
count=sum(t['continuous_positive_clearance_path'] for t in trials)
assert count>0, 'No demonstrated path: do not infer enclosure closure from this limited search.'
report={'classification':'CALCULATED_BREP_PATH_COUNTEREXAMPLE_NOT_FLOW_OR_ACOUSTIC_SIMULATION',
        'status':'FAIL_FULL_ENCLOSURE_SEAL_IN_CURRENT_CANDIDATE',
        'continuous_path_count':count,'trials':trials,
        'labyrinth_treated_rear_vent_count':22,
        'all_product_apertures_treatment_verified':False,
        'limitations':['Polyline includes turns; this is not a claim of direct acoustic line of sight.',
                      'Positive BREP segment clearance proves a finite geometric path only for these modeled parts.',
                      'The path stays at X<=20; no thermal/flow resistance or acoustic attenuation is calculated.',
                      'A qualified front/perimeter and DML seal design is still required; no gasket property is invented.'],
        'source_sha256':{path:hashlib.sha256((repo/path).read_bytes()).hexdigest() for path in paths.values()}}
report['source_sha256'][str(Path(__file__).relative_to(repo))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(repo/'evidence/rev-fe/front-joint-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'paths':count,'minimum_clearances_mm':[t['minimum_centerline_clearance_mm'] for t in trials]},indent=2))
