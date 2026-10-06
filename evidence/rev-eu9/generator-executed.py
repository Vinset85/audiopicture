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
# Rev.EU.9: replace the massive original 8 mm plate by a 2.4 mm rear skin.
# The perimeter web restores connectivity; four explicit boss cylinders retain 7 mm bore engagement.
frame=frame.cut(box(0,320,0,400,27,32.6))
for x in [37.5,67.5,252.5,282.5]:frame=frame.union(cq.Workplane('XY').center(x,375).circle(6).extrude(8).translate((0,0,27)))
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
for name,points in paths.items():frame=frame.union(rib(points,2.4,20,26.4))
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
flange=box(3.2,316.8,3.2,396.8,6,8.4).cut(box(9.6,310.4,9.6,390.4,5,9))
frame=frame.union(flange)
# Two opposed X-braced webs make a perimeter space truss. All member
# thicknesses 2.4 mm and in-plane widths 3.2 mm are geometric candidates.
# Front and rear flange rings join the two webs. No ASA stiffness is credited.
def diagonal_web(orientation, fixed, a0,a1,z0,z1):
 dx,dz=a1-a0,z1-z0;length=math.hypot(dx,dz);na,nz=-dz/length*1.6,dx/length*1.6
 polygon=[(a0+na,z0+nz),(a1+na,z1+nz),(a1-na,z1-nz),(a0-na,z0-nz)]
 if orientation=='Y':return cq.Workplane('YZ').polyline(polygon).close().extrude(2.4).translate((fixed,0,0))
 return cq.Workplane('XZ').polyline(polygon).close().extrude(2.4).translate((0,fixed+2.4,0))
for orientation,start,end,positions in [('Y',7.2,392.8,[3.2,7.2,310.4,314.4]),('X',7.2,312.8,[3.2,7.2,390.4,394.4])]:
 count=math.ceil((end-start)/34)
 for fixed in positions:
  for i in range(count):
   q0=start+(end-start)*i/count;q1=start+(end-start)*(i+1)/count
   for za,zb in [(7.2,33.8),(33.8,7.2)]:frame=frame.union(diagonal_web(orientation,fixed,q0,q1,za,zb))
# Trim protruding ends to the intended depth and ring envelope.
frame=frame.intersect(box(3.2,316.8,3.2,396.8,6,35))
# Hollow upper/lower cross-members strengthen single-cleat and torsion paths.
top=box(3.2,316.8,371.2,396.8,20,35).cut(box(2,318,373.6,394.4,19,32.6))
# The central extra top carrier is not a qualified MAIN-C attachment. Preserve
# only the rear perimeter skin here, reducing redundant cross-member volume.
top=top.cut(box(85,235,370,388,19,36))
bottom=box(3.2,316.8,3.2,12,10.5,35).cut(box(2,318,5.6,9.6,12.9,32.6))
frame=frame.union(top).union(bottom)
# Reserve room for future 2.2 mm ASA side walls, with 1 mm lateral gap.
frame=frame.intersect(box(3.2,316.8,3.2,396.8,0,40))
# Remove the unused rear membrane below the relocated bore group; existing
# side/upper ribs retain independent mount connections.
for x0,x1 in [(25.5,79.5),(240.5,294.5)]:
 frame=frame.cut(box(x0,x1,352,369,28.01,35.01))
# Trim the rear perimeter to 8 mm minimum width away from mount islands.
for coords in [(11.2,12,20,350),(308,308.8,20,350)]:
 frame=frame.cut(box(*coords,32.6,35.01))
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
report={'revision':'Rev.EU.9','classification':'CALCULATED_SCREENING_CANDIDATE_NOT_FABRICATION_RELEASE','valid':shape.isValid(),'solid_count':frame.solids().size(),'volume_mm3':sum(s.Volume() for s in frame.solids().vals()),'reimport_valid':reimport.val().isValid(),'reimport_solids':reimport.solids().size(),'collision_volume_mm3':collisions,'shell_clearance_mm':shape.distance(shell.val()),'mount_centers_xy_mm':mounts,'bore_radius_seed_mm':3,'bore_z_mm':[28,35],'pad_centers_xy_mm':[[45,28],[275,28]],'anti_lift_load_interface_xy_mm':[160,15],'rail_paths_xy_mm':paths,'primary_rib_mm':2.4,'primary_rib_z_mm':[20,26.4],'front_flange_width_mm':6.4,'perimeter_web_topology':'two opposed 2.4 mm thick X-braced webs; brace width 3.2 mm','perimeter_web_mm':2.4,'closed_bottom_tube_y_mm':[3.2,12],'sha256':hashlib.sha256(step.read_bytes()).hexdigest(),'limitations':['Mount shift Y366->375 required by conservative RF mask; requires mating cleat redesign.','6 mm insert surrogate bore, no exact insert installation-hole claim.','Fillets, exact radar mask, cables, board carrier interfaces and fasteners remain incomplete.','Lower support/anti-lift surrogate load interfaces; actual wall hardware absent.','Volume density/strength unqualified; no product release.']}
(a.out/'execution.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert report['valid'] and report['solid_count']==1 and report['reimport_valid'] and report['reimport_solids']==1
assert max(collisions.values())<1e-6
