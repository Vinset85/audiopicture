"""Complete structural screening candidate. Engineering seeds, NOT production CAD.

EU.22 adds solid side/top perimeter sections after EU.21 weak-seed LC4 failed.
Restores legal rails/lower pads/anti-lift and independent insert interfaces.
RF mask forces mount Y366->375. A 6 mm blind bore is a sensitivity geometry,
not an installation-hole specification. No catalog strength is assumed.
"""
import argparse,json,hashlib,math
from pathlib import Path
import cadquery as cq
p=argparse.ArgumentParser();p.add_argument('--frame',type=Path,required=True);p.add_argument('--shell',type=Path,required=True);p.add_argument('--front-carrier',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
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
# Rev.EU.22: replace the massive original 8 mm plate by a 2.4 mm rear skin.
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
 'pad_L_ring':[(45,28),(45,7)],'pad_R_ring':[(275,28),(275,7)],
 'tie_L125':[(8.4,125),(32,125)],'tie_L235':[(8.4,235),(32,235)],
 'tie_L350':[(8.4,350),(34,350)],'tie_R155':[(311.6,155),(305,155)],
 'tie_R225':[(311.6,225),(303,225)],'tie_R350':[(311.6,350),(300,350)]}
# Mass-cap removal: use 3.2 mm primary width and 8 mm depth, with ties to the deep perimeter
# at three intermediate levels per side. Posts anchor ties to both flanges
# so a tie does not simply end inside a void between diagonal members.
for name,points in paths.items():frame=frame.union(rib(points,3.2,20,28))
# New deep lower paths bypass the SERVICE rectangle on its two sides and
# join each lower pad to its corner in front of the labyrinth. Replace the
# old shallow lower routing; no additional support or ASA stiffness is used.
for points in [[(95,15),(95,28),(45,28)],[(225,15),(225,28),(275,28)]]:
 frame=frame.union(rib(points,8.0,10.3,35))
for points in [[(45,28),(7,7)],[(275,28),(313,7)]]:
 # EU.17's 1.4 mm end radius was exactly tangent to the tube wall Y5.6.
 # EU.22 increases corner-girder width to 12.8 mm to test the lower load path.
 # This is a physical geometry change, not a CAD-only tolerance.
 frame=frame.union(rib(points,12.8,10.3,28))
for x,ys in [(8.4,[125,235,350]),(311.6,[155,225,350])]:
 for y in ys:frame=frame.union(box(x-1.2,x+1.2,y-1.4,y+1.4,6,35))
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
# EU.19 uses continuous inner/outer PC-CF webs instead of the mass-limited
# diagonal lattice. Both webs remain outside the DML hard projection.
# No metal or ASA stiffness, additional supports or altered material is credited.
inner_web=box(7.2,312.8,7.2,392.8,6,35).cut(box(9.6,310.4,9.6,390.4,5,36))
outer_web=box(3.2,316.8,3.2,396.8,6,35).cut(box(5.6,314.4,5.6,394.4,5,36))
frame=frame.union(inner_web).union(outer_web)
# EU.22: full side/top sections above the DML back-plane + 1 mm.
# No lower cell is encroached: side inner edge X12.6 versus cell edge X14.
frame=frame.union(box(3.2,12.6,3.2,396.8,10.3,35))
frame=frame.union(box(307.4,316.8,3.2,396.8,10.3,35))
frame=frame.union(box(3.2,316.8,387.4,396.8,10.3,35))
# Trim protruding ends to the intended depth and ring envelope.
frame=frame.intersect(box(3.2,316.8,3.2,396.8,6,35))
# Hollow upper/lower cross-members strengthen single-cleat and torsion paths.
top=box(3.2,316.8,371.2,396.8,20,35).cut(box(2,318,373.6,394.4,19,32.6))
# The central extra top carrier is not a qualified MAIN-C attachment. Preserve
# only the rear perimeter skin here, reducing redundant cross-member volume.
top=top.cut(box(85,235,370,388,19,36))
bottom=box(3.2,316.8,3.2,12,10.5,35).cut(box(2,318,5.6,9.6,12.9,32.6))
# EU.22 fills the bottom crossmember through both outer corners.
# Outside the central span Y is limited to 12 mm, 1 mm before lower cells.
# Stepped front face stays outside the DML hard projection and gives
# the central cross-member more section depth. Leave 1.0 mm behind the
# DML where the section overlaps its XY projection. A 1.0 mm shell gap
# limits the rear face to Z36.8. Retain the original anti-lift surface Z35.
outer_center=box(32,288,3.2,19,6,36.8).union(box(3.2,316.8,3.2,12,6,36.8))
outer_center=outer_center.cut(box(2,318,9.6,20,5,10.3))
# Solid section seed; production process and mass optimization remain open.

# Add an outward-DML front lip, maintaining 0.8 mm to the carrier base.
# Relieve complete magnetic-station stock +0.5 mm nominal XY clearance.
lip=box(32,288,3.2,9.6,3.1,6.1)
for x in [70,250]:lip=lip.cut(box(x-6.5,x+6.5,0,10,2.5,6.2))
outer_center=outer_center.union(lip)
# Fill the old hollow central crossmember to assess its stiffness limitation.
# Keep the stepped DML clearance, rear retention reliefs and anti-lift surface.
# This is a heavier physical cross-section, not a qualified production choice.
bottom=bottom.union(outer_center)
bottom=bottom.cut(box(151,169,10,20,35,37))
# Rear-shell retention bosses occupy X75..85 and235..245, Y12.., Z36..
# Preserve a 1.0 mm gap by lowering the tube rear face locally.
for x0,x1 in [(74,86),(234,246)]:bottom=bottom.cut(box(x0,x1,11,20,35,37))
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
# Bore-bottom and outer-transition fillets are not implemented yet.
# These candidates do not close the contractual fillet/mesh qualification gates.
collisions={n:sum(s.Volume() for s in frame.intersect(box(*c)).solids().vals()) for n,c in keepouts.items()}
front_carrier=cq.importers.importStep(str(a.front_carrier))
collisions['front_carrier_FA']=sum(s.Volume() for s in frame.intersect(front_carrier).solids().vals())
for i,(x,y) in enumerate([(70,394),(250,394),(70,6),(250,6),(6,135),(6,275),(314,135),(314,315)]):
 collisions[f'metal_target_{i+1}']=sum(s.Volume() for s in frame.intersect(box(x-3.5,x+3.5,y-3.5,y+3.5,4.1,5.1)).solids().vals())
collisions['shell_EQ']=sum(s.Volume() for s in frame.intersect(shell).solids().vals())
shape=frame.val();step=a.out/'AP22_FRAME_CANDIDATE_REV_EU.step';cq.exporters.export(frame,str(step))
reimport=cq.importers.importStep(str(step))
report={'revision':'Rev.EU.22','classification':'CALCULATED_SCREENING_CANDIDATE_NOT_FABRICATION_RELEASE','valid':shape.isValid(),'solid_count':frame.solids().size(),'volume_mm3':sum(s.Volume() for s in frame.solids().vals()),'reimport_valid':reimport.val().isValid(),'reimport_solids':reimport.solids().size(),'collision_volume_mm3':collisions,'shell_clearance_mm':shape.distance(shell.val()),'front_carrier_clearance_mm':shape.distance(front_carrier.val()),'input_sha256':{str(v.resolve().relative_to(Path.cwd())):hashlib.sha256(v.read_bytes()).hexdigest() for v in [a.frame,a.shell,a.front_carrier,Path(__file__)]},'mount_centers_xy_mm':mounts,'bore_radius_seed_mm':3,'bore_z_mm':[28,35],'pad_centers_xy_mm':[[45,28],[275,28]],'anti_lift_load_interface_xy_mm':[160,15],'rail_paths_xy_mm':paths,'primary_rib_mm':3.2,'deep_lower_girders':{'side_paths':[[[95,15],[95,28],[45,28]],[[225,15],[225,28],[275,28]]],'side_z_mm':[10.3,35],'corner_paths':[[[45,28],[7,7]],[[275,28],[313,7]]],'corner_z_mm':[10.3,28],'side_width_mm':8.0,'corner_width_mm':12.8},'intermediate_ties':{'count':6,'post_xy_section_mm':[2.4,2.8],'post_z_mm':[6,35]},'central_bottom_tube_xy_mm':[32,288,3.2,19],'central_crossmember_section':'solid section extended to both outer corners within Y3.2..12; side girders 8.0 mm and corner girders 12.8 mm','central_tube_z_mm':[3.1,36.8],'dml_notch_yz_mm':[9.6,19,6,10.3],'anti_lift_surface_z_mm':35,'primary_rib_z_mm':[20,28],'front_flange_width_mm':6.4,'perimeter_web_topology':'solid 9.4 mm side/top sections Z10.3..35 plus original front webs; above DML with 1 mm nominal Z separation','perimeter_web_mm':2.4,'closed_bottom_tube_y_mm':[3.2,12],'sha256':hashlib.sha256(step.read_bytes()).hexdigest(),'limitations':['Mount shift Y366->375 required by conservative RF mask; requires mating cleat redesign.','6 mm insert surrogate bore, no exact insert installation-hole claim.','Fillets, exact radar mask, cables, board carrier interfaces and fasteners remain incomplete.','Lower support/anti-lift surrogate load interfaces; actual wall hardware absent.','Volume density/strength unqualified; no product release.']}
report['mass_g_at_catalog_density_1p22']=report['volume_mm3']*.00122
report['solid_perimeter_section_mm']={'side_width':9.4,'top_width':9.4,'z':[10.3,35]}
report['mass_acceptance_ceiling_g']=None
report['mass_policy']='User authorization 2026-10-07: exceed prior mass budget; no 250 g rejection criterion. Mass and assembly CG/load adequacy remain tracked.'
report['mass_change_vs_EU21_g']=report['mass_g_at_catalog_density_1p22']-473.690764329757
(a.out/'execution.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert report['valid'] and report['solid_count']==1 and report['reimport_valid'] and report['reimport_solids']==1
assert max(collisions.values())<1e-6
