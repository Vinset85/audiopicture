"""Complete structural screening candidate. Engineering seeds, NOT production CAD.

Restores legal rails/lower pads/anti-lift and independent insert interfaces.
RF mask forces mount Y366->375. A 6 mm blind bore is a sensitivity geometry,
not an installation-hole specification. No catalog strength is assumed.
"""
import argparse,json,hashlib,math
from pathlib import Path
import cadquery as cq
p=argparse.ArgumentParser();p.add_argument('--frame',type=Path,required=True);p.add_argument('--shell',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def box(x0,x1,y0,y1,z0,z1):return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
def rib(points,width,z0,z1):
 result=None
 for (x0,y0),(x1,y1) in zip(points,points[1:]):
  dx,dy=x1-x0,y1-y0;l=math.hypot(dx,dy);nx,ny=-dy/l*width/2,dx/l*width/2
  q=cq.Workplane('XY').polyline([(x0+nx,y0+ny),(x1+nx,y1+ny),(x1-nx,y1-ny),(x0-nx,y0-ny)]).close().extrude(z1-z0).translate((0,0,z0))
  result=q if result is None else result.union(q)
 for x,y in points:
  result=result.union(cq.Workplane('XY').center(x,y).circle(width/2).extrude(z1-z0).translate((0,0,z0)))
 return result
frame=cq.importers.importStep(str(a.frame));shell=cq.importers.importStep(str(a.shell))
# Rails dive in front of the labyrinth (max Z28, cells start Z29), outside exciters.
paths={
 'rail_L':[(34,378),(34,350),(33,300),(32,235),(32,125),(33,112),(33,45),(45,28)],
 'rail_R':[(286,378),(300,350),(300,300),(303,225),(305,155),(306,75),(300,62),(296,30),(275,28)],
 'mid_B1_B2':[(32,235),(155,230),(303,225)],
 'mid_B3':[(155,230),(205,165),(305,155)],
 'mid_B4':[(32,125),(70,161),(155,161),(155,230)],
 'lower_L':[(33,45),(95,45),(95,14),(160,14)],
 'lower_R':[(300,62),(296,60),(225,55),(225,14),(160,14)],
 'pad_L_ring':[(45,28),(45,7)],'pad_R_ring':[(275,28),(275,7)]}
for name,points in paths.items():frame=frame.union(rib(points,2.8,20,28))
# Two paths from each mount island, tied separately to top and side perimeters.
for points in [[(38,375),(25,384),(7,384)],[(67,375),(67,393)],[(252,375),(252,393)],[(282,375),(300,384),(313,384)]]:
 frame=frame.union(rib(points,3.2,27,35))
# Integrate front/rear depth at rail ends and lower-pad connections.
for x,y in [(34,378),(286,378),(45,7),(275,7)]:frame=frame.union(box(x-3,x+3,y-3,y+3,20,35))
for x in [45,275]:
 frame=frame.union(box(x-9,x+9,22,34,20,35))
frame=frame.union(box(151,169,10,20,20,35))
frame=frame.union(rib([(160,14),(160,7)],3.2,20,35))
# Shell-retention top tabs from Rev.AP, absent from Rev.J/ES.
for x in [145,175]:frame=frame.union(box(x-6,x+6,378,390,27,35))
# Continuous 2.4 mm perimeter return + 2.4 mm front flange outside DML.
# Candidate deep section; no continuous metal ring is introduced.
web=box(7.2,312.8,7.2,392.8,6,29).cut(box(9.6,310.4,9.6,390.4,5,30))
flange=box(2,318,2,398,6,8.4).cut(box(9.6,310.4,9.6,390.4,5,9))
frame=frame.union(web).union(flange)
# Hollow upper/lower cross-members strengthen single-cleat and torsion paths.
top=box(2,318,371.2,398,20,35).cut(box(1,319,373.6,395.6,22.4,32.6))
bottom=box(2,318,2,18,10.5,28).cut(box(1,319,4.4,15.6,12.9,25.6))
frame=frame.union(top).union(bottom)
# All full-depth coarse forbidden volumes from the authoritative packaging contract.
keepouts={
 'EX_L1':[37,99,50,110,9.3,36.3],'EX_L2':[83,145,166,226,9.3,36.3],
 'EX_R1':[175,237,238,298,9.3,36.3],'EX_R2':[223,285,88,148,9.3,36.3],
 'MAIN_C':[85,235,315,370,16,36.6],'MAIN_P':[105,220,112,157,17,33],
 'VOICE':[119,201,20,102,11,18],'RADAR':[249,287,184,216,0,18],
 'ENV':[252,294,35,59,11,18],'SERVICE':[100,220,20,48,20,40],
 'ESP32_RF':[64,119.5,318.5,366.5,0,40],
 'DML':[10,310,10,390,3.3,9.3]}
for name,coords in keepouts.items():frame=frame.cut(box(*coords))
frame=frame.clean()
mounts={n:(x,375) for n,x in [('UL1',37.5),('UL2',67.5),('UR1',252.5),('UR2',282.5)]}
for x,y in mounts.values():
 bore=cq.Workplane('XY').center(x,y).circle(3).extrude(7.1).translate((0,0,28))
 frame=frame.cut(bore)
frame=frame.clean()
# Fillet bore bottom circular edges: 0.5mm numerical seating radius candidate.
# Mount islands are massive solids; outer perimeter transitions remain unfilleted pending FEA.
collisions={n:sum(s.Volume() for s in frame.intersect(box(*c)).solids().vals()) for n,c in keepouts.items()}
collisions['shell_EQ']=sum(s.Volume() for s in frame.intersect(shell).solids().vals())
shape=frame.val();step=a.out/'AP22_FRAME_CANDIDATE_REV_EU.step';cq.exporters.export(frame,str(step))
reimport=cq.importers.importStep(str(step))
report={'revision':'Rev.EU.4','classification':'CALCULATED_SCREENING_CANDIDATE_NOT_FABRICATION_RELEASE','valid':shape.isValid(),'solid_count':frame.solids().size(),'volume_mm3':sum(s.Volume() for s in frame.solids().vals()),'reimport_valid':reimport.val().isValid(),'reimport_solids':reimport.solids().size(),'collision_volume_mm3':collisions,'shell_clearance_mm':shape.distance(shell.val()),'mount_centers_xy_mm':mounts,'bore_radius_seed_mm':3,'bore_z_mm':[28,35],'pad_centers_xy_mm':[[45,28],[275,28]],'anti_lift_load_interface_xy_mm':[160,15],'rail_paths_xy_mm':paths,'sha256':hashlib.sha256(step.read_bytes()).hexdigest(),'limitations':['Mount shift Y366->375 required by conservative RF mask; requires mating cleat redesign.','6 mm insert surrogate bore, no exact insert installation-hole claim.','Fillets, exact radar mask, cables, board carrier interfaces and fasteners remain incomplete.','Lower support/anti-lift surrogate load interfaces; actual wall hardware absent.','Volume density/strength unqualified; no product release.']}
(a.out/'execution.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert report['valid'] and report['solid_count']==1 and report['reimport_valid'] and report['reimport_solids']==1
assert max(collisions.values())<1e-6
