"""22 parallel stepped cells, each with opposing upper/lower openings.

Rev.BK real apertures preserved. Full cell depth is a design candidate, not
qualified production dimensions. Area and LOS gates are geometric only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq

p=argparse.ArgumentParser()
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--frame',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):
 return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
solid=cq.importers.importStep(str(a.baseline))
for x0,x1,y0,y1,z0 in [(14.9,51.1,13.9,62.1,33.9),(268.9,305.1,13.9,62.1,33.9),
                       (14.9,51.1,314.9,363.1,35),(268.9,305.1,314.9,363.1,35)]:
 solid=solid.cut(box(x0,x1,y0,y1,z0,37.8))
lower=[('V',x,x+3,y,y+40) for y in (14,62,110) for x in (17,24)]
upper=[('H',17,62,y,y+3) for y in (315,322,329,336,343)]
vents=lower+upper
vents +=[(o,320-x1,320-x0,y0,y1) for o,x0,x1,y0,y1 in vents]
cells=[];reports=[]
for i,(o,x0,x1,y0,y1) in enumerate(vents):
 # u is short aperture direction; v is long direction.
 # inlet u0..u0+3; middle baffle u0-3..u0+2; bottom outlet u0-2..u0.
 u0,u1,v0,v1=(x0,x1,y0,y1) if o=='V' else (y0,y1,x0,x1)
 def b(ua,ub,va,vb,za,zb):
  return box(ua,ub,va,vb,za,zb) if o=='V' else box(va,vb,ua,ub,za,zb)
 parts=[b(u0,u0+5,v0-1,v1+1,29,30),
        b(u0-3,u0+2,v0-1,v1+1,33,34),
        b(u0-3,u0-2,v0-1,v1+1,29,37.81),
        b(u0+4,u0+5,v0-1,v1+1,29,37.81),
        b(u0-3,u0+5,v0-1,v0,29,37.81),
        b(u0-3,u0+5,v1,v1+1,29,37.81)]
 cell=parts[0]
 for s in parts[1:]:cell=cell.union(s)
 cell=cell.clean();cells.append(cell)
 solid=solid.union(cell)
 # Minimum cross sections: 2 mm upper turn gap and 2 mm bottom outlet;
 # top/bottom horizontal channels have heights 3.8/3.0 mm respectively.
 length=v1-v0
 reports.append({'id':i+1,'orientation':o,'aperture_xy':[x0,x1,y0,y1],
                 'minimum_geometric_cross_section_mm2':2*length,
                 'cell_valid':cell.val().isValid()})
solid=solid.clean()
frame=cq.importers.importStep(str(a.frame))
chambers=cells[0]
for c in cells[1:]:chambers=chambers.union(c)
chambers=chambers.clean()
q=chambers.intersect(frame)
overlap=sum(s.Volume() for s in q.solids().vals())
clearance=min(s.distance(frame.val()) for s in chambers.solids().vals())
fluid=box(.01,319.99,.01,399.99,9.31,40.25).cut(solid).cut(frame).clean()
vent_reclosure=[];vent_connected=[]
for o,x0,x1,y0,y1 in vents:
 length=(y1-y0) if o=='V' else (x1-x0)
 probe=cq.Workplane('XY',origin=((x0+x1)/2,(y0+y1)/2,37.8)).slot2D(length,3,90 if o=='V' else 0).extrude(2.4)
 vent_reclosure.append(sum(s.Volume() for s in solid.intersect(probe).solids().vals()))
 vent_connected.append(sum(s.Volume() for s in fluid.intersect(probe).solids().vals())>1e-8)
# Aperture samples to cavity and directly to the bottom outlet of every cell.
# Dense finite test supplements the 2D collinearity bound below.
open_rays=0;total=0;examples=[]
for o,x0,x1,y0,y1 in vents:
 u0=x0 if o=='V' else y0
 v0,v1=(y0,y1) if o=='V' else (x0,x1)
 for fu in (.1,.5,.9):
  for fv in (.05,.5,.95):
   x,y=(x0+3*fu,y0+(y1-y0)*fv) if o=='V' else (x0+(x1-x0)*fv,y0+3*fu)
   destinations=[(x,y,28.5),(160,200,28.5),(80,y,28.5),(240,y,28.5)]
   for gu in (.1,.5,.9):
    for gv in (.05,.5,.95):
     u=u0-2+2*gu;v=v0+(v1-v0)*gv
     destinations.append((u,v,28.5) if o=='V' else (v,u,28.5))
   for dest in destinations:
    e=cq.Edge.makeLine(cq.Vector(x,y,40.25),cq.Vector(*dest))
    if solid.val().distance(e)>1e-7:
     open_rays+=1
     if len(examples)<10:examples.append({'source':[x,y,40.25],'dest':dest})
    total+=1
# Any straight path must cross shell-inner plane (z37.8) inside inlet u=[0,3]
# and floor-top plane (z30) inside outlet u=[-2,0]. At baffle top z34,
# interpolation puts it in [-0.97436,1.53846], strictly inside baffle [-3,2].
# Side walls prevent escaping to a different cell or around long-axis ends.
f=(37.8-34)/(37.8-30)
lower_area=sum(r['minimum_geometric_cross_section_mm2'] for r in reports if r['orientation']=='V')
upper_area=sum(r['minimum_geometric_cross_section_mm2'] for r in reports if r['orientation']=='H')
result={'revision':'Rev.EQ','classification':'CALCULATED_CAD_CANDIDATE_NOT_PRODUCTION',
        'solid_valid':solid.val().isValid(),'solid_components':solid.solids().size(),
        'solid_volume_mm3':sum(s.Volume() for s in solid.solids().vals()),
        'fluid_valid':fluid.val().isValid(),'fluid_components':fluid.solids().size(),
        'fluid_volume_mm3':sum(s.Volume() for s in fluid.solids().vals()),
        'full_coverage_vents':22,'parallel_cells':22,'cells':reports,
        'max_nominal_vent_reclosure_mm3':max(vent_reclosure),
        'connected_vents_count':sum(vent_connected),
        'coarse_frame_overlap_mm3':overlap,'coarse_frame_clearance_mm':clearance,
        'sampled_rays':total,'open_rays':open_rays,'open_examples':examples,
        'analytic_straight_ray_baffle_coordinate_bounds_mm':[-2*f,3*(1-f)],
        'baffle_coordinate_interval_mm':[-3,2],
        'aggregate_lower_min_cross_section_mm2':lower_area,
        'aggregate_upper_min_cross_section_mm2':upper_area,
        'area_geometry_gate':'PASS' if lower_area>=600 and upper_area>=750 else 'FAIL',
        'release':'OPEN',
        'limitations':['Geometric cross sections are not measured effective flow areas.',
                       'CFD, acoustic attenuation, tolerance/print qualification open.',
                       'Coarse frame only; exact component, RF, cleat, cable DMU absent.',
                       'Floors z29..30, baffles z33..34: new candidate dimensions.',
                       'Internal audit complement excludes electronics/harnesses and room/wall gap.']}
coupon_reports={}
for label,indices in [('LOWER_PAIR',[0,1]),('UPPER_PAIR',[6,7])]:
 coupon=cells[indices[0]].union(cells[indices[1]])
 bb=coupon.val().BoundingBox()
 coupon=coupon.union(box(bb.xmin,bb.xmax,bb.ymin,bb.ymax,37.8,40))
 for i in indices:
  o,x0,x1,y0,y1=vents[i]
  length=(y1-y0) if o=='V' else (x1-x0)
  cut=cq.Workplane('XY',origin=((x0+x1)/2,(y0+y1)/2,37.8)).slot2D(length,3,90 if o=='V' else 0).extrude(2.3)
  coupon=coupon.cut(cut)
 coupon=coupon.clean();bb=coupon.val().BoundingBox()
 coupon=coupon.translate((-bb.xmin,-bb.ymin,-bb.zmin))
 coupon_reports[label]={'valid':coupon.val().isValid(),'solids':coupon.solids().size(),
                        'bbox_mm':[bb.xlen,bb.ylen,bb.zlen],
                        'purpose':'ASA print/metrology/flow coupon, not qualified part'}
 for ext in ('step','stl'):cq.exporters.export(coupon,str(a.out/f'AP22_REV_EQ_{label}_COUPON.{ext}'))
 assert coupon.val().isValid() and coupon.solids().size()==1
result['physical_process_coupons']=coupon_reports
for name,obj in [('solid',solid),('fluid',fluid)]:
 if obj.val().isValid():
  path=a.out/f'AP22_REV_EQ_{name.upper()}.step';cq.exporters.export(obj,str(path))
  imported=cq.importers.importStep(str(path))
  result[name+'_reimport_valid']=imported.val().isValid()
  result[name+'_reimport_components']=imported.solids().size()
  result[name+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
(a.out/'execution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='cells'},indent=2))
if not(solid.val().isValid() and solid.solids().size()==1 and fluid.val().isValid() and fluid.solids().size()==1 and overlap<1e-8 and clearance>1e-7 and open_rays==0 and max(vent_reclosure)<1e-8 and all(vent_connected)):raise SystemExit(1)
