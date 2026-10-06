"""Restore documented conservative RF exclusion in Rev.J frame kernel.

Coarse mask from ESP32 placement Rev.A / retention Rev.AP, not exact antenna CAD.
No boss/insert/contact fabrication release.
"""
import argparse
import json
from pathlib import Path
import cadquery as cq

p=argparse.ArgumentParser();p.add_argument('--frame',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
frame=cq.importers.importStep(str(a.frame))
mask=box(64,119.5,318.5,366.5,0,40)
def overlap(s,t):return sum(v.Volume() for v in s.intersect(t).solids().vals())
before=overlap(frame,mask);clipped=frame.cut(mask).clean()
after=overlap(clipped,mask)
result={'revision':'Rev.ES','classification':'CALCULATED_COARSE_RF_CAD_CORRECTION_NOT_EXACT_RF_RELEASE',
        'mask_xy_mm':[64,119.5,318.5,366.5],'mask_z_mm':[0,40],
        'before_RF_overlap_mm3':before,'after_RF_overlap_mm3':after,
        'before_volume_mm3':sum(s.Volume() for s in frame.solids().vals()),
        'after_volume_mm3':sum(s.Volume() for s in clipped.solids().vals()),
        'valid':clipped.val().isValid(),'solid_count':clipped.solids().size(),
        'coarse_RF_gate':'PASS' if after<1e-8 else 'FAIL',
        'exact_RF_gate':'OPEN','structural_gate':'OPEN_REQUIRES_NEW_FRAME_FEA',
        'limitations':['Exact antenna mask remains absent.','Mount bosses/inserts/contacts absent.',
                       'Removed material changes structural load paths.']}
cq.exporters.export(clipped,str(a.out/'AP22_FRAME_RF_CLIPPED_REV_ES.step'))
(a.out/'execution.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
assert clipped.val().isValid() and clipped.solids().size()==1 and after<1e-8
