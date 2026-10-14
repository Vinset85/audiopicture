"""Upper product/wall cleats, recessed shell pockets and explicit screw stack.

All alloy sections, clearances and seal grooves are design candidates. The
thread/head limits are sourced separately. No bolt preload, heat-set pullout,
friction, machining tolerance or wall-anchor capacity is assumed qualified.
"""
import argparse, hashlib, json, math
from pathlib import Path
import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
for manifest in ['execution.json','frame-geometry.json']:(a.out/manifest).unlink(missing_ok=True)
def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False)).translate((x0,y0,z0))
def cylinder(x,y,r,z0,z1):
    return cq.Workplane('XY').center(x,y).circle(r).extrude(z1-z0).translate((0,0,z0))
def cone(x,y,r0,r1,z0,z1):
    return cq.Workplane(obj=cq.Solid.makeCone(r0,r1,z1-z0,cq.Vector(x,y,z0)))
def volume(w):
    total=0.
    for s in w.solids().vals():
        prop=GProp_GProps();BRepGProp.VolumeProperties_s(s.wrapped,prop,1e-10,True,False);total+=prop.Mass()
    return total
paths={
 'frame':'evidence/rev-fg/fixed-seals/AP22_FRAME_SEAL_LAND_REV_FG.step',
 'shell':'evidence/rev-fe/sidewalls-eu22/AP22_SHELL_SIDEWALL_CANDIDATE_REV_FE.step',
 'DML':'evidence/rev-fg/fixed-seals/AP22_DML_NOMINAL_REV_FG.step',
 'DML_seal':'evidence/rev-fg/fixed-seals/AP22_DML_GASKET_COMPRESSED_REV_FG.step',
 'frame_shell_seal':'evidence/rev-fg/fixed-seals/AP22_FRAME_SHELL_GASKET_COMPRESSED_REV_FG.step',
}
parts={n:cq.importers.importStep(str(ROOT/v)) for n,v in paths.items()}
frame,shell=parts['frame'],parts['shell'];parts_new={};motion=[];stacks=[];alternatives={}
mount_top=31.; cleat_back=33.5; bore_bottom=21.9; base_bottom=19.4
product_profile=[(369,mount_top),(394,mount_top),(394,40),(384,40),(390.5,cleat_back),(369,cleat_back)]
wall_profile=[(369,40.5),(369,43),(389,43),(389,40),(384,40),(390.5,cleat_back),(381,cleat_back),(381,40.5)]
for side,x0 in [('L',27.5),('R',242.5)]:
    # Move the entire threaded interface forward, retaining the catalog bore
    # depth and base thickness, to provide a 6.5-mm nominal hook profile.
    module=box(x0,x0+50,366.8,383.2,base_bottom,bore_bottom)
    for x in [x0+10,x0+40]:module=module.union(cylinder(x,375,6,bore_bottom,mount_top))
    roots=[e for e in module.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().z-bore_bottom)<1e-6 and abs(e.radius()-6)<1e-6]
    assert len(roots)==2
    module=module.newObject(roots).fillet(2).clean();frame=frame.union(module)
    for x in [x0+10,x0+40]:
        frame=frame.union(cylinder(x,375,3.01,bore_bottom-.1,35))
        frame=frame.cut(cylinder(x,375,2.8,bore_bottom,35.1))
    product=cq.Workplane('YZ').polyline(product_profile).close().extrude(50).translate((x0,0,0))
    wall=cq.Workplane('YZ').polyline(wall_profile).close().extrude(50).translate((x0,0,0))
    # Radius 0.5 on the re-entrant product transition; the rest of the mating
    # bevel is left as a flat CAD contact surface for the nonlinear model.
    edges=[e for e in product.val().Edges() if e.geomType()=='LINE' and abs(e.Length()-50)<1e-6
           and abs(e.Center().y-390.5)<1e-6 and abs(e.Center().z-cleat_back)<1e-6]
    assert len(edges)==1
    product=product.newObject(edges).fillet(.5)
    tip=[e for e in wall.val().Edges() if e.geomType()=='LINE' and abs(e.Length()-50)<1e-6
         and abs(e.Center().y-390.5)<1e-6 and abs(e.Center().z-cleat_back)<1e-6]
    assert len(tip)==1
    wall=wall.newObject(tip).fillet(.75)
    for x in [x0+10,x0+40]:
        # Clearance is a design interface, not a universal anchor selection.
        wall=wall.cut(cylinder(x,375,2.25,40.4,43.1))
        head=cone(x,375,4.48,2,40.5,42.98)
        wall=wall.cut(head)
        parts_new[f'WALL_HEAD_{side}_{x:g}_SPACE_ENVELOPE']=head
    for thick in [1,2]:
        spacer=box(x0,x0+50,369,389,43,43+thick)
        for x in [x0+10,x0+40]:spacer=spacer.cut(cylinder(x,375,2.25,42.9,43.1+thick))
        assert spacer.val().isValid() and volume(spacer.intersect(wall))<1e-6
        alternatives[f'WALL_SPACER_{thick}MM_{side}']=spacer
    # Recessed ASA pocket keeps product-side metal at Z<=40. The shell floor
    # clears the metal by 0.2 mm; PC-CF bosses contact the cleat at Z31.
    outer=box(x0-2.7,x0+52.7,366.3,396.7,28.6,40)
    opening=box(x0-.5,x0+50.5,368.5,394.5,30.8,40.1)
    pocket=outer.cut(opening)
    # Remove inherited structural stock from the pocket with 0.5 mm clearance.
    # Original bosses remain, so no primary load is credited to ASA.
    clearance=box(x0-3.2,x0+53.2,365.8,397.2,28.1,40.1)
    for x in [x0+10,x0+40]:
        clearance=clearance.cut(cylinder(x,375,6,bore_bottom-.1,mount_top))
    frame=frame.cut(clearance).clean()
    for j,x in enumerate([x0+10,x0+40],1):
        pocket=pocket.cut(cylinder(x,375,7.2,28.5,31.0))
        product=product.cut(cylinder(x,375,2.25,mount_top-.1,40.1))
        # ISO10642 length includes the head. The maximum 90-degree head
        # envelope is flush with the metal, allowing the complete lift path.
        head=cone(x,375,2,4.48,31.02,33.5)
        product=product.cut(head)
        screw=cylinder(x,375,2,23.5,31.02).union(head)
        parts_new[f'SCREW_{side}{j}_BOUNDING']=screw
        # Axial die-cut gasket on a dedicated polymer collar. Its bore clears
        # the boss radially; sealing occurs on planar lands, not at a circular
        # line contact. The 1.57 mm / 320 kg/m3 PORON family is a catalog seed,
        # not a measured compression or air-permeability law.
        seal_free=1.57; seal_installed=.8*seal_free
        seal_top=28.6; seal_bottom=seal_top-seal_installed
        collar=cylinder(x,375,8.4,seal_bottom-1.2,seal_bottom)
        collar=collar.cut(cylinder(x,375,2.8,seal_bottom-1.3,seal_bottom+.1))
        frame=frame.union(collar).clean()
        seal=cylinder(x,375,8.1,seal_bottom,seal_top).cut(cylinder(x,375,6.2,seal_bottom-.1,seal_top+.1))
        frame=frame.cut(seal).clean()
        parts_new[f'BOSS_SEAL_{side}{j}_COMPRESSED']=seal
        stacks.append({'name':f'{side}{j}','center_xy_mm':[x,375],'cleat_thickness_mm':2.5,
                       'countersunk_screw_overall_length_mm':10,'nominal_engagement_mm':7.5,
                       'nominal_insert_bottom_reserve_mm':.6,'nominal_bore_floor_reserve_mm':1.6,
                       'maximum_head_back_Z_mm':33.5,'ASA_floor_gap_mm':.2,
                       'boss_seal_free_mm':seal_free,'boss_seal_installed_mm':seal_installed,
                       'boss_seal_ID_OD_mm':[12.4,16.2],'boss_seal_ASA_contact_radial_width_mm':.9,
                       'boss_seal_PC_land_top_Z_mm':seal_bottom,'boss_seal_PC_land_OD_mm':16.8})
    shell=shell.cut(box(x0-.5,x0+50.5,368.5,394.5,30.8,40.1)).union(pocket).clean()
    assert volume(product.intersect(wall))<1e-6,volume(product.intersect(wall))
    trials=[]
    for label,dy,dz in [('downward',-.1,0),('outward',0,-.1),('release_up',7,0),('retained_after_5mm_lift',5,-5.5)]:
        overlap=volume(product.translate((0,dy,dz)).intersect(wall))
        trials.append({'motion':label,'dY_mm':dy,'dZ_mm':dz,'interference_mm3':overlap})
        assert overlap>1e-4 if label!='release_up' else overlap<1e-6,(label,overlap)
    motion.append({'side':side,'rigid_motion_tests':trials})
    parts_new[f'PRODUCT_CLEAT_{side}']=product
    parts_new[f'WALL_CLEAT_{side}']=wall
frame=frame.clean();parts.update(frame=frame,shell=shell);parts.update(parts_new)
for n,w in parts.items():assert w.val().isValid() and w.solids().size()==1,n
overlaps={}
names=list(parts)
for i,n in enumerate(names):
    for m in names[i+1:]:
        overlap=volume(parts[n].intersect(parts[m]))
        if overlap>1e-5:overlaps[n+'/'+m]=overlap
assert not overlaps,overlaps
RF=box(64,119.5,318.5,366.5,0,50)
for n,w in parts.items():
    if n.startswith(('PRODUCT_CLEAT','WALL_CLEAT','SCREW','WALL_HEAD')) or n=='frame':
        assert volume(w.intersect(RF))<1e-6,n

# Assemble without the diagnostic screw envelopes when checking the material
# barrier: blind polymer bores alone already close each screw penetration.
eq=json.loads((ROOT/'evidence/rev-eq/execution.json').read_text());caps=None
for cell in eq['cells']:
    x0,x1,y0,y1=cell['aperture_xy'];v=box(x0-.1,x1+.1,y0-.1,y1+.1,39.9,40.1)
    caps=v if caps is None else caps.union(v)
barrier_names=['shell','frame','DML','DML_seal','frame_shell_seal']+[n for n in parts if n.startswith('BOSS_SEAL')]
envelope=box(0,320,0,400,0,40)
# Incremental volume conservation catches OCC results which report a valid
# BREP but have incorrectly discarded a whole connected air component.
air=envelope; boolean_checks=[]
for n,w in [(n,parts[n]) for n in barrier_names]+[('audit_caps',caps)]:
    before=volume(air); removed=volume(air.intersect(w))
    updated=air.cut(w).clean();after=volume(updated)
    residual=after-(before-removed)
    assert updated.val().isValid(),('Air BREP',n)
    assert abs(residual)<.05,('Air volume conservation',n,residual)
    boolean_checks.append({'part':n,'before_mm3':before,'removed_mm3':removed,'after_mm3':after,'residual_mm3':residual})
    air=updated
solids=air.solids().vals();rear=[i for i,s in enumerate(solids) if s.isInside(cq.Vector(160,200,25))]
front=[i for i,s in enumerate(solids) if s.isInside(cq.Vector(160,200,1))]
assert len(rear)==len(front)==1 and rear[0]!=front[0]
# The externally accessible pocket must remain disconnected from the cavity.
pockets={side:[i for i,s in enumerate(solids) if s.isInside(cq.Vector(x,380,36))] for side,x in [('L',52.5),('R',267.5)]}
assert all(len(v)==1 and v[0]!=rear[0] for v in pockets.values())
vent_components=[]
for cell in eq['cells']:
    x0,x1,y0,y1=cell['aperture_xy'];point=cq.Vector((x0+x1)/2,(y0+y1)/2,39.8)
    found=[i for i,s in enumerate(solids) if s.isInside(point)]
    assert found==rear,('Vent cavity disconnected',cell['aperture_xy'],found,rear)
    vent_components.append({'aperture_xy_mm':cell['aperture_xy'],'capped_cavity_component':found[0]})
artifacts={}
for n,w in {**parts,**alternatives}.items():
    f=a.out/f'AP22_{n.upper()}_REV_FG.step';cq.exporters.export(w,str(f))
    back=cq.importers.importStep(str(f));assert back.val().isValid() and back.solids().size()==1
    err=abs(volume(back)-volume(w))/max(volume(w),1);assert err<1e-6,(n,err)
    artifacts[n]={'file':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'volume_mm3':volume(w),'STEP_relative_volume_error':err}
frame_info=json.loads((ROOT/'evidence/rev-fg/fixed-seals/frame-geometry.json').read_text())
frame_file=Path(artifacts['frame']['file'])
frame_info.update(revision='Rev.FG recessed upper mount candidate',bore_z_mm=[bore_bottom,mount_top],
                  volume_mm3=volume(frame),mass_g_at_catalog_density_1p22=volume(frame)*.00122,
                  artifacts={frame_file.name:{'sha256':artifacts['frame']['sha256']}},
                  parent_geometry_sha256=hashlib.sha256((ROOT/'evidence/rev-fg/fixed-seals/frame-geometry.json').read_bytes()).hexdigest())
(a.out/'frame-geometry.json').write_text(json.dumps(frame_info,indent=2)+'\n')
report={'classification':'CALCULATED_NOMINAL_UPPER_MOUNT_ASSEMBLY_NOT_STRUCTURAL_RELEASE',
        'status':'PASS_SCOPED_CAD_AND_RIGID_ENGAGEMENT_CHECKS', 'product_part_max_Z_mm':40,
        'wall_plane_seed_Z_mm':43,'wall_gap_seed_mm':3,'wall_gap_4_5_requires_spacers':True,
        'alternative_spacer_thickness_mm':[1,2],'spacers_are_mutually_exclusive':True,
        'wall_fastener_clearance_hole_diameter_mm':4.5,'wall_head_space_envelope_diameter_height_mm':[8.96,2.48],
        'wall_head_requirement':'M4 90-degree countersunk interface, flush or below Z40.5; shaft length and anchor must be qualified for substrate.',
        'wall_anchor_MPN_and_substrate_qualification':None,'nominal_hook_profile_depth_mm':6.5,
        'product_profile_YZ_mm':product_profile,'wall_profile_YZ_mm':wall_profile,
        'screw_catalog_candidate':'PTS A79910410, A2 stainless, M4x10 ISO10642',
        'screw_model':'Maximum 90-degree countersunk head and external-thread envelopes; no hex recess or original detailed screw CAD',
        'stacks':stacks,'rigid_engagement':motion,'unexpected_overlaps_mm3':overlaps,
        'air_partition_boolean_checks':boolean_checks,'capped_air_components':len(solids),'rear_component':rear[0],'front_component':front[0],
        'mount_pocket_components':pockets,'capped_air_component_volumes_mm3':[volume(cq.Workplane(obj=s)) for s in solids],
        'vent_cavity_checks':vent_components,'artifacts':artifacts,
        'source_sha256':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths.values()},
        'limits':['No installed heat-set plastic-flow geometry, clamp torque or pullout strength.',
                  'Cleat shape and seal grooves are nominal design choices; nonlinear/contact FEA and tolerance sweeps remain required.',
                  'Wall-anchor holes and head space are design interfaces; exact anchors, substrate, preload and bearing/edge strength are unqualified.',
                  'Rigid interference tests establish kinematic engagement only, not stiffness or retention strength.',
                  'Normal contact of ASA pocket is excluded from the intended structural load path.',
                  'Seal domains are impermeable geometric assumptions, not measured leakage or seal force.']}
report['source_sha256'][str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(a.out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','capped_air_components','rigid_engagement','unexpected_overlaps_mm3']},indent=2))
