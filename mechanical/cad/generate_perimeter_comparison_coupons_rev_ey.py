"""Real section coupons for comparing C and X-braced PC-CF print/process behavior.
End grips are test-fixture seeds; no material or force acceptance is invented.
"""
import argparse,json,hashlib
from pathlib import Path
import cadquery as cq
import trimesh
p=argparse.ArgumentParser();p.add_argument('--c-frame',type=Path,required=True);p.add_argument('--x-frame',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
reports=[]
for name,src in [('C_SECTION_EU8',a.c_frame),('X_BRACED_EU9',a.x_frame)]:
 frame=cq.importers.importStep(str(src))
 # Left perimeter avoids all internal rails and component interfaces.
 part=frame.intersect(box(3.2,11.2,158,242,6,35))
 for y in [158,238.8]:part=part.union(box(3.2,11.2,y,y+3.2,6,35))
 part=part.clean().translate((-3.2,-158,-6))
 assert part.val().isValid() and part.solids().size()==1
 files={}
 for ext in ['step','stl']:
  dest=a.out/f'AP22_PERIMETER_{name}_COUPON.{ext}';cq.exporters.export(part,str(dest));files[ext]={'path':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 imported=cq.importers.importStep(str(a.out/files['step']['path']))
 stl=trimesh.load_mesh(str(a.out/files['stl']['path']))
 assert imported.val().isValid() and imported.solids().size()==1 and stl.is_watertight and stl.is_winding_consistent
 bb=part.val().BoundingBox()
 reports.append({'name':name,'classification':'CALCULATED_PROCESS_AND_STIFFNESS_COMPARISON_COUPON_NOT_PRODUCTION','valid':True,'single_solid':True,'reimport_valid':True,'stl_watertight':True,'stl_winding_consistent':True,'bbox_mm':[bb.xlen,bb.ylen,bb.zlen],'volume_mm3':part.val().Volume(),'end_grip_length_mm':3.2,'nominal_clear_test_span_mm':77.6,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'files':files,'fixture_compliance_correction':'REQUIRED','load_protocol_and_acceptance':'OPEN: laboratory to define before qualification; compare same process/orientation and linear force-displacement/torque-angle slopes'})
(a.out/'execution.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
