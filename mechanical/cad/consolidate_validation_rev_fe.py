"""Consolidate executed FE work; failed criteria stay failed, pending jobs block publication."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess

repo=Path(__file__).resolve().parents[2]
parent='1922eb1667b5027569bc569c6152589ecaa66f82'
subprocess.run(['git','merge-base','--is-ancestor',parent,'HEAD'],cwd=repo,check=True)
def read(path):return json.loads((repo/path).read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def source_path(path):
    p=Path(path)
    if p.is_absolute():
        # Older reports used absolute paths. Resolve only their repository
        # suffix, so an extracted checkpoint cannot read arbitrary host paths.
        marker='/audiopicture/'
        assert str(p).count(marker)==1,path
        p=Path(str(p).split(marker,1)[1])
    result=(repo/p).resolve();assert result.is_relative_to(repo)
    return result
def verify(d,key='source_sha256'):
    for path,digest in d[key].items():assert sha(source_path(path))==digest,path
gates=read('mechanical/validation/rev-fd/gate-register.json')
def gate(status,scope,evidence):
    gates['gates'].append({'id':f'G{len(gates["gates"])+1:02d}','status':status,'scope':scope,'evidence':evidence})

frames={}
for n,levels in [(20,['M0','M1']),(21,['M0']),(22,['M0','M1'])]:
    cad=read(f'evidence/rev-eu{n}/execution.json');verify(cad,'input_sha256')
    assert sha(repo/f'evidence/rev-eu{n}/AP22_FRAME_CANDIDATE_REV_EU.step')==cad['sha256']
    assert cad['valid'] and cad['reimport_valid'] and cad['solid_count']==cad['reimport_solids']==1
    assert len(cad['collision_volume_mm3'])==22 and max(cad['collision_volume_mm3'].values())<1e-6
    meshes={}
    for level in levels:
        mr=read(f'evidence/rev-ev{n}/{level}/mesh-report.json');q=read(f'evidence/rev-ev{n}/{level}/quality-audit.json');verify(q)
        assert mr['source_sha256']==cad['sha256'] and q['nonpositive_Jacobian_elements']==0
        meshes[level]={'report':mr,'quality':q}
    frames[f'EU{n}']={'CAD':cad,'meshes':meshes,'cases':{}}
    if n!=20:
        gate('PASS',f'EU.{n} BREP/reimport, 22 coarse overlap checks and positive mesh Jacobians only',
             {'mass_catalog_density_g':cad['mass_g_at_catalog_density_1p22'],
              'shell_gap_mm':cad['shell_clearance_mm'],'production_qualified':False})
        assert cad['mass_acceptance_ceiling_g'] is None

executions=[]
for inp in sorted((repo/'evidence/rev-fe').glob('EU*/*/*/frame.inp')):
    folder=inp.parent; frame_name=folder.parents[1].name;run=folder.parent.name;level=run.split('-')[0]
    # Every generated full-frame deck must have completed output and metrics.
    e=json.loads((folder/'execution.json').read_text());m=json.loads((folder/'metrics.json').read_text())
    assert e['input_sha256']==sha(inp)
    assert e['mesh_report']==frames[frame_name]['meshes'][level]['report']
    assert e['solver_execution_pass'] and m['solver_execution_pass'] and m['final_step_time']==1
    assert 'Job finished' in (folder/'solver.log').read_text() and '*ERROR' not in (folder/'solver.log').read_text()
    assert m['force_balance_within_0_1_percent_or_0_001N']
    row={'execution':e,'metrics':m,'path':str(folder.relative_to(repo))}
    frames[frame_name]['cases'][run+'/'+e['case']]=row; executions.append(row)
    if e['case']=='LC4':
        value=max(m['corner_max_abs_UZ_mm'].values());axis=e.get('weak_global_axis','Z')
        gate('PASS' if value<=1 else 'FAIL',f'{frame_name} {level} LC4 {e["loaded_corner"]}, weak {axis}, normalized displacement only',
             {'max_corner_UZ_mm':value,'limit_mm':1,'qualified_strength_and_process':False,'path':row['path']})
        if axis!='Z':
            comparison=json.loads((folder/'orientation-comparison.json').read_text());verify(comparison)
            assert comparison['status']=='PASS';row['controlled_orientation_comparison']=comparison
    else:
        gate('PASS',f'{frame_name} {run} {e["case"]}: solver execution and force equilibrium only',
             {'max_displacement_mm':m['max_displacement_mm'],'actual_mount_compliance_and_strength_qualified':False,'path':row['path']})
    for name in ['lower-crossmember-diagnostic.json','quadratic-dml-clearance.json','deformed-clearance.json','refined-quadratic-clearance.json']:
        if (folder/name).exists():
            d=json.loads((folder/name).read_text());verify(d);row[name]=d
            if name=='deformed-clearance.json':
                failed=d['nodes_predicted_inside_DML']>0 or d['nodes_predicted_frontward_of_DML_within_projection']>0
                gate('FAIL' if failed else 'PASS',f'{frame_name} {run} {e["case"]}: sampled-node DML clearance only',
                     {'nodes_inside_DML':d['nodes_predicted_inside_DML'],
                      'nodes_frontward_of_DML':d['nodes_predicted_frontward_of_DML_within_projection'],
                      'DML_contact_modeled':False,'path':row['path']})
            elif name=='quadratic-dml-clearance.json':
                gate('PASS' if d['final']['all_element_bounds_separated_from_DML_and_frontward_region'] else 'OPEN',
                     f'{frame_name} {run} {e["case"]}: full quadratic element bounds versus fixed DML only',
                     {'status':d['status'],'final':d['final'],'path':row['path']})
            elif name=='refined-quadratic-clearance.json':
                status='FAIL' if d['witnesses_beyond_0p0001_mm_numerical_margin'] else ('PASS' if d['status'].startswith('PASS') else 'OPEN')
                gate(status,f'{frame_name} {run} {e["case"]}: refined full-element DML clearance',
                     {'status':d['status'],'robust_witnesses':d['witnesses_beyond_0p0001_mm_numerical_margin'],
                      'largest_witness_boundary_margin_mm':d['largest_witness_boundary_margin_mm'],'path':row['path']})
                final_id=gates['gates'][-1]['id']
                for old_gate in gates['gates'][:-1]:
                    old_evidence=old_gate.get('evidence',{})
                    if isinstance(old_evidence,dict) and old_evidence.get('path')==row['path'] and 'full quadratic element bounds' in old_gate['scope']:
                        old_gate['refined_by_gate']=final_id
assert len(executions)>=10, 'Expected at least the completed baseline and orientation work'
coarse=frames['EU22']['cases']['M0-LC4-LR-Ez020-G025/LC4']['metrics']['max_abs_UZ_mm']
fine=frames['EU22']['cases']['M1-LC4-LR-Ez020-G025/LC4']['metrics']['max_abs_UZ_mm']
mesh_comparison={'coarse_mm':coarse,'fine_mm':fine,'relative_change_percent_fine_reference':abs(fine-coarse)/fine*100,
                 'full_stress_mesh_convergence_verified':False,'criterion_mm':1}
gate('PASS' if mesh_comparison['relative_change_percent_fine_reference']<5 else 'FAIL',
     'EU.22 two-mesh weak-Z lower-right LC4 displacement comparison only',mesh_comparison)

axes=read('evidence/rev-fe/material-axes-check/verification.json')
assert axes['status']=='PASS' and axes['case_count']==18
assert axes['script_sha256']==sha(repo/'mechanical/cad/verify_material_axes_rev_fe.py')
for row in axes['cases']:
    folder=repo/'evidence/rev-fe/material-axes-check'/row['name']
    assert row['input_sha256']==sha(folder/'cube.inp')
    assert 'Job finished' in (folder/'solver.log').read_text()
gate('PASS','18 executed independent axial/shear cube checks of material rotation only',
     {'maximum_relative_strain_error':axes['maximum_relative_strain_error'],'material_qualified':False})
shells={}
for name in ['sidewalls','sidewalls-eu22']:
    s=read(f'evidence/rev-fe/{name}/execution.json');verify(s)
    for file,digest in s['artifact_sha256'].items():assert sha(repo/f'evidence/rev-fe/{name}'/file)==digest
    assert s['valid'] and s['STEP_reimport_valid'] and s['STL_watertight'] and s['solid_count']==1
    assert s['unchanged_labyrinth_cells']==22 and s['added_within_labyrinth_box_mm3']<1e-6 and s['removed_within_labyrinth_box_mm3']<1e-6
    assert all(p['ASA_material_present'] for p in s['sidewall_samples']) and len(s['sidewall_samples'])==36
    assert s['frame_clearance_mm']>=1-1e-6 and s['front_clearance_mm']>=.5-1e-6
    shells[name]=s
gate('PASS','ASA sidewall candidate: BREP/STEP/STL, 36 side samples, 22 unchanged labyrinth cells and nominal clearances only',
     {'volume_mm3':shells['sidewalls-eu22']['volume_mm3'],'full_enclosure_closed':False})
joint=read('evidence/rev-fe/front-joint-audit.json');verify(joint)
assert joint['continuous_path_count']>0 and joint['all_product_apertures_treatment_verified'] is False
gate('FAIL','Current front joint permits unmanaged geometric paths to the cavity',
     {'continuous_paths_demonstrated':joint['continuous_path_count'],'direct_LOS_or_attenuation_claimed':False})
insert=read('evidence/rev-fe/insert-source/cad-audit.json');verify(insert)
gate('FAIL','The temporary frame bores are not a valid installation specification for RX-M4x8.1',
     {'hole_depth_shortfall_mm':insert['surrogate_depth_shortfall_mm'],'nominal_diameter_difference_mm':insert['surrogate_hole_diameter_difference_mm']})
coupon=read('evidence/rev-fe/insert-coupon/execution.json');verify(coupon)
for file,digest in coupon['artifact_sha256'].items():assert sha(repo/'evidence/rev-fe/insert-coupon'/file)==digest
assert coupon['BREP_valid'] and coupon['STEP_reimport_valid'] and coupon['STL_watertight']
gate('PASS','Catalog-sized M4 installation coupon CAD/STEP/STL only',{'root_fillet_mm':coupon['root_fillet_mm'],'printed_or_measured':False})
mass=read('evidence/rev-fe/mass-load-review.json');verify(mass)
verify(read('evidence/rev-fe/geometry-figure.json'))
figure=read('evidence/rev-fe/orientation-figure.json');verify(figure)
for path,digest in figure['artifact_sha256'].items():assert sha(repo/path)==digest
gate('OPEN','Production selection, qualified print/material and complete real mounting/sealing interfaces',
     {'final_geometry_selected':False,'full_LC1_LC7_current_matrix_complete':False,
      'full_product_CFD_executed':False,'physical_qualification_executed':False})

timestamp=datetime.now(timezone.utc).isoformat()
gates.update(revision='Rev.FE',recorded_utc=timestamp,checkpoint_parent_head=parent)
gates['dependency_order'].append('Weak-seed and orientation results -> exact mount/insert plus process calibration and seal design -> current complete FEA/CFD and product integration')
counts={s:sum(g['status']==s for g in gates['gates']) for s in ['PASS','FAIL','OPEN']}
summary={'revision':'Rev.FE','recorded_utc':timestamp,'checkpoint_parent_head':parent,
         'previous_checkpoint':'mechanical/validation/rev-fd/summary.json','gate_counts_including_history':counts,
         'counts_are_not_completion_percentages':True,'executed_full_frame_runs':len(executions),'executed_material_axis_cube_tests':18,
         'frames':frames,'EU22_weak_Z_mesh_comparison':mesh_comparison,'sidewall_candidates':shells,
         'front_joint_audit':joint,'insert_audit':insert,'installation_coupon':coupon,'mass_load_review':mass,
         'production_ready':False,'final_frame_and_print_orientation_selected':False,
         'all_remaining_digital_work_complete':False,'physical_tests_executed':False,'full_product_CFD_executed':False}
out=repo/'mechanical/validation/rev-fe';out.mkdir(parents=True,exist_ok=True)
(out/'gate-register.json').write_text(json.dumps(gates,indent=2)+'\n')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
evidence=[p for d in ['rev-fe','rev-eu21','rev-ev21','rev-eu22','rev-ev22'] for p in (repo/'evidence'/d).rglob('*')
          if p.is_file() and p.name not in ['provenance.json','raw-artifact-index.json','github-publication.json']]
sources=list((repo/'mechanical/cad').glob('*rev_fe.py'))+[repo/f'mechanical/cad/generate_frame_candidate_rev_eu{n}.py' for n in [21,22]]
sources += [repo/'mechanical/components/ruthex-m4-insert-candidate-rev-fe.json',repo/'mechanical/test/insert-installation-pilot-rev-fe.md',repo/'mechanical/print-orientation-study-rev-fe.md',repo/'mechanical/test/physical-qualification-addendum-rev-fe.json',repo/'mechanical/test/measurement-record-template-rev-fe.json',repo/'manufacturing/real-data-required-rev-fe.md']
provenance={'revision':'Rev.FE','checkpoint_parent_head':parent,
            'source_hashes':{str(p.relative_to(repo)):sha(p) for p in sources},
            'evidence_hashes':{str(p.relative_to(repo)):sha(p) for p in evidence},
            'solver_sha256':sha(repo.parent/'solvers/CalculiX/ccx_2.23/src/ccx_2.23'),'solver_version':'CalculiX 2.23',
            'production_qualified':False}
(repo/'evidence/rev-fe/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'full_frame_runs':len(executions),'cube_tests':18,'gate_counts':counts,'EU22_mesh_comparison':mesh_comparison},indent=2))
