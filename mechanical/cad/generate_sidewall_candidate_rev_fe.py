"""Add real ASA sidewalls to EQ while preserving all 22 labyrinth cells.

This closes the previously empty lateral wall samples, not the full enclosure:
front/DML seals, service cable geometry, mounting penetrations and ENV chamber
remain separate unresolved interfaces. No fluid/thermal qualification is claimed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import cadquery as cq
import trimesh

p=argparse.ArgumentParser()
p.add_argument('--shell',type=Path,required=True)
p.add_argument('--frame',type=Path,required=True)
p.add_argument('--front',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
repo=Path(__file__).resolve().parents[2]
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
def vol(s):
    return sum(q.Volume() for q in s.solids().vals())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
old=cq.importers.importStep(str(a.shell))
frame=cq.importers.importStep(str(a.frame))
front=cq.importers.importStep(str(a.front))
wall_t,front_z,outer_radius=2.2,4.2,2.0
walls=box(0,320,0,400,front_z,40).cut(box(wall_t,320-wall_t,wall_t,400-wall_t,front_z-.1,40.1))
shell=old.union(walls).clean()
# Four outer vertical corner edges and four outer rear edges, no vent edge.
edges=[]
for e in shell.val().Edges():
    b=e.BoundingBox()
    if e.geomType()!='LINE': continue
    corner=(b.xlen<1e-6 and b.ylen<1e-6 and b.zlen>30
            and min(abs(b.xmin),abs(b.xmin-320))<1e-6
            and min(abs(b.ymin),abs(b.ymin-400))<1e-6)
    rear=(abs(b.zmin-40)<1e-6 and b.zlen<1e-6
          and ((b.xlen<1e-6 and min(abs(b.xmin),abs(b.xmin-320))<1e-6)
               or (b.ylen<1e-6 and min(abs(b.ymin),abs(b.ymin-400))<1e-6)))
    if corner or rear: edges.append(e)
assert len(edges)==8, len(edges)
shell=shell.newObject(edges).fillet(outer_radius).clean()
assert shell.val().isValid() and shell.solids().size()==1
b=shell.val().BoundingBox()
assert b.xmin>=-1e-6 and b.xmax<=320+1e-6 and b.ymin>=-1e-6 and b.ymax<=400+1e-6
assert b.zmin>=front_z-1e-6 and abs(b.zmax-40)<1e-6
frame_overlap=vol(shell.intersect(frame)); front_overlap=vol(shell.intersect(front))
frame_gap=shell.val().distance(frame.val()); front_gap=shell.val().distance(front.val())
assert max(frame_overlap,front_overlap)<1e-6
assert frame_gap>=1-1e-6 and front_gap>=.5-1e-6

# Compare both directions of the Boolean difference within a box enclosing
# every EQ cell, aperture and 0.2 mm of cavity. The wall change is outside it.
protected=box(12,308,12,350,28.8,40.25)
added_inside=vol(shell.cut(old).intersect(protected))
removed_inside=vol(old.cut(shell).intersect(protected))
assert max(added_inside,removed_inside)<1e-6
eq_path=repo/'evidence/rev-eq/execution.json'; eq=json.loads(eq_path.read_text())
assert sha(a.shell)==eq['solid_sha256']
vents=[]
for cell in eq['cells']:
    x0,x1,y0,y1=cell['aperture_xy']; o=cell['orientation']
    length=y1-y0 if o=='V' else x1-x0
    probe=cq.Workplane('XY',origin=((x0+x1)/2,(y0+y1)/2,37.8)).slot2D(length,3,90 if o=='V' else 0).extrude(2.4)
    overlap=vol(shell.intersect(probe))
    assert overlap<1e-6
    vents.append({'id':cell['id'],'aperture_obstruction_mm3':overlap})
samples=[]
for side in ['left','right','bottom','top']:
    for t in [.25,.5,.75]:
        for z in [12,20,26]:
            xyz=([1,400*t,z] if side=='left' else [319,400*t,z] if side=='right' else [320*t,1,z] if side=='bottom' else [320*t,399,z])
            occupied=shell.val().isInside(cq.Vector(*xyz)); assert occupied
            samples.append({'side':side,'xyz_mm':xyz,'ASA_material_present':occupied})
step=a.out/'AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step'
stl=a.out/'AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.stl'
cq.exporters.export(shell,str(step)); cq.exporters.export(shell,str(stl),tolerance=.05,angularTolerance=.1)
back=cq.importers.importStep(str(step))
assert back.val().isValid() and back.solids().size()==1
assert abs(vol(back)-vol(shell))<1e-4
mesh=trimesh.load_mesh(stl)
initial_watertight=bool(mesh.is_watertight)
# OCC emits four collapsed pole facets at the R2 spherical corners. Remove
# only faces with repeated vertex indices after exact STL vertex merging;
# do not fill holes, move vertices or remove finite-area geometry.
f=mesh.faces
keep=(f[:,0]!=f[:,1]) & (f[:,1]!=f[:,2]) & (f[:,2]!=f[:,0])
collapsed_count=int((~keep).sum())
if collapsed_count:
    mesh.update_faces(keep)
    mesh.remove_unreferenced_vertices()
    mesh.export(stl)
    mesh=trimesh.load_mesh(stl)
assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
stl_error=abs(mesh.volume-vol(shell))/vol(shell); assert stl_error<.005
report={'revision':'Rev.FE','classification':'CALCULATED_PARTIAL_ENCLOSURE_CANDIDATE_NOT_RELEASE',
        'valid':True,'solid_count':1,'STEP_reimport_valid':True,'volume_mm3':vol(shell),
        'added_volume_mm3':vol(shell)-vol(old),'sidewall_thickness_mm':wall_t,
        'sidewall_front_z_mm':front_z,'outer_edge_radius_mm':outer_radius,
        'frame_overlap_mm3':frame_overlap,'front_overlap_mm3':front_overlap,
        'frame_clearance_mm':frame_gap,'front_clearance_mm':front_gap,
        'labyrinth_protected_box_mm':[12,308,12,350,28.8,40.25],
        'added_within_labyrinth_box_mm3':added_inside,'removed_within_labyrinth_box_mm3':removed_inside,
        'unchanged_labyrinth_cells':len(vents),'vent_probes':vents,'sidewall_samples':samples,
        'STL_watertight':True,'STL_volume_relative_error':stl_error,
        'initial_STL_watertight':initial_watertight,'collapsed_zero_area_facets_removed':collapsed_count,
        'STL_cleanup':'Repeated-index zero-area facets only; no moved vertices or filled holes.',
        'full_enclosure_closed':False,'full_product_CFD_executed':False,
        'source_sha256':{str(q.resolve().relative_to(repo)):sha(q) for q in [a.shell,a.frame,a.front,eq_path,Path(__file__)]},
        'artifact_sha256':{step.name:sha(step),stl.name:sha(stl)},
        'limitations':['4.2 mm front edge is a design seed providing 0.5 mm to the front magnetic stock.',
                      'Front seam and DML acoustic seal remain open; no enclosure leakage qualification.',
                      'Service/cable and actual wall-mount penetrations are not yet designed.',
                      'ENV chamber and full PCB/cable DMU remain incomplete.',
                      'Unchanged cells preserve geometry only, not a thermal/flow/acoustic attenuation result.',
                      'ASA material, tolerances, shrink, warpage and production process require physical qualification.']}
(a.out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['sidewall_samples','vent_probes']},indent=2))
