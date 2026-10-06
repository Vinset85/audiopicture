"""Audit omitted enclosure boundaries with real BREP point membership, not a CFD run."""
import argparse,json
from pathlib import Path
import cadquery as cq
p=argparse.ArgumentParser();p.add_argument('--shell',type=Path,required=True);p.add_argument('--frame',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
shell=cq.importers.importStep(str(a.shell)).val();frame=cq.importers.importStep(str(a.frame)).val()
# Probe material on lateral enclosure boundary below all rear edge returns.
probes=[]
for side in ['left','right','bottom','top']:
 for t in [.25,.5,.75]:
  for z in [12,20,26]:
   pos=([1,400*t,z] if side=='left' else [319,400*t,z] if side=='right' else [320*t,1,z] if side=='bottom' else [320*t,399,z])
   probes.append({'side':side,'xyz_mm':pos,'ASA_shell_material':shell.isInside(cq.Vector(*pos)),'PC_CF_frame_material':frame.isInside(cq.Vector(*pos))})
# Rear service port remains a solid rear sheet at a representative proposed access location.
service={'xyz_mm':[160,34,39],'shell_material_present':shell.isInside(cq.Vector(160,34,39))}
clearance=frame.distance(shell)
r={'classification':'CALCULATED_BREP_AUDIT_NOT_CFD','sidewall_sample_count':len(probes),'unoccupied_sidewall_samples':sum(not x['ASA_shell_material'] and not x['PC_CF_frame_material'] for x in probes),'probes':probes,'service_probe':service,'shell_frame_min_clearance_mm':clearance,'clearance_1mm_target_status':'PASS' if clearance>=1.-1e-6 else 'FAIL','closure_status':'OPEN: no full sidewalls/front seal/service-cable penetrations in these two BREP files. 22 vent cells do not certify all openings of a complete enclosure.','CFD01_to_CFD05_status':'OPEN: exterior room, 3/4/5 mm wall gap, full obstruction volumes, CHT material properties and radiation boundary surfaces still required.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='probes'},indent=2))
