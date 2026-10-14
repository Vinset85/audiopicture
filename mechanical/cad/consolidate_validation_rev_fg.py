"""Verify Rev.FG artifacts and record scoped outcomes without closing release gates."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE='08def92a06e8a09cc321664966e159ea339dc8b5'
subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def resolve(p):
    p=Path(p)
    if p.is_absolute():
        marker='/audiopicture/';assert str(p).count(marker)==1
        p=Path(str(p).split(marker,1)[1])
    q=(ROOT/p).resolve();assert q.is_relative_to(ROOT);return q
def verify(d):
    for p,h in d['source_sha256'].items():assert sha(resolve(p))==h,p
gates=read('mechanical/validation/rev-fe/gate-register.json');added=[]
def gate(status,scope,evidence):
    g=dict(id=f'G{len(gates["gates"])+1:02d}',status=status,scope=scope,evidence=evidence)
    gates['gates'].append(g);added.append(g)

frame=read('evidence/rev-fg/frame/execution.json');verify(frame)
assert frame['BREP_valid'] and frame['STEP_reimport_valid'] and frame['solid_count']==1 and frame['STL_watertight']
assert max(frame['collision_volume_mm3'].values())<1e-6
for name,a in frame['artifacts'].items():assert sha(ROOT/'evidence/rev-fg/frame'/name)==a['sha256']
gate('PASS','FG installation-bore and enlarged DML-clearance candidate: nominal BREP/STEP/STL and overlap checks only',
     {'path':'evidence/rev-fg/frame/execution.json','volume_mm3':frame['volume_mm3'],'production_qualified':False})
seals=read('evidence/rev-fg/fixed-seals/execution.json');verify(seals)
assert not seals['capped_partition']['rear_front_connected']
assert seals['without_radial_seal']['rear_front_connected'] and seals['without_DML_seal']['rear_front_connected']
for a in seals['artifacts'].values():assert sha(ROOT/a['file'])==a['sha256']
gate('PASS','FG fixed DML/radial seal candidate: nominal capped air partition and omitted-seal controls only',
     {'path':'evidence/rev-fg/fixed-seals/execution.json','impermeable_gaskets_assumed':True,'preload_and_leakage_qualified':False})
mounts=read('evidence/rev-fg/upper-mounts-chamfer/execution.json');verify(mounts)
parent_mounts=read('evidence/rev-fg/upper-mounts-deep/execution.json');verify(parent_mounts)
for data in [mounts,parent_mounts]:
    for a in data['artifacts'].values():assert sha(ROOT/a['file'])==a['sha256']
audit=read('evidence/rev-fg/upper-mounts-chamfer/independent-audit.json');verify(audit)
assert audit['status'].startswith('PASS') and len(audit['each_mount_seal_removal_controls'])==4
assert len(audit['coarse_keepout_checks'])==187 and len(mounts['vent_cavity_checks'])==22
assert max(audit['unchanged_22_cell_region_material'].values())<1e-4
gate('PASS','FG upper mount CAD: STEP reimport, 187 coarse keepouts, 22 unchanged labyrinth cells and capped pocket separation only',
     {'path':'evidence/rev-fg/upper-mounts-chamfer/independent-audit.json',
      'capped_air_components':audit['closed_partition']['components'],'all_product_apertures_treatment_qualified':False})
gate('PASS','FG represented upper assembly: continuous rigid 7 mm lift and outward extraction sweep only',
     {'path':'evidence/rev-fg/upper-mounts-chamfer/independent-audit.json','tolerances_deformation_and_lower_hardware_included':False})
gate('PASS','FG alternate wall spacer CAD for nominal 3/4/5 mm gaps only',
     {'path':'evidence/rev-fg/upper-mounts-chamfer/execution.json','exact_wall_anchor_and_substrate':None})

meshes={}
for name,geom,step in [
 ('mesh','frame/execution.json','frame/AP22_FRAME_INTERFACE_CANDIDATE_REV_FG.step'),
 ('mesh-seals','fixed-seals/frame-geometry.json','fixed-seals/AP22_FRAME_SEAL_LAND_REV_FG.step'),
 ('mesh-upper','upper-mounts-deep/frame-geometry.json','upper-mounts-deep/AP22_FRAME_REV_FG.step')]:
    path=f'evidence/rev-fg/{name}/M0';m=read(path+'/mesh-report.json');q=read(path+'/quality-audit.json');verify(q)
    assert m['source_sha256']==sha(ROOT/'evidence/rev-fg'/step)
    assert m['interface_geometry_sha256']==sha(ROOT/'evidence/rev-fg'/geom)
    assert q['nonpositive_Jacobian_elements']==0 and m['type']=='C3D10'
    meshes[name]=m
    gate('PASS',f'FG {name} M0: positive quadratic-element Jacobians only',
         {'path':path+'/quality-audit.json','nodes':m['nodes'],'elements':m['elements'],'min_SICN':m['min_SICN'],'mesh_convergence_verified':False})

runs=[]
for inp in sorted((ROOT/'evidence/rev-fg').glob('*-runs/*/*/frame.inp')):
    folder=inp.parent;relative=str(folder.relative_to(ROOT));m=json.loads((folder/'metrics.json').read_text());verify(m)
    e=json.loads((folder/'execution.json').read_text());assert e['input_sha256']==sha(inp)
    assert e['runner_sha256']==sha(ROOT/'mechanical/cad/run_frame_screen_rev_fe.py')
    assert e['solver_execution_pass'] and m['final_step_time']==1 and m['force_balance_within_0_1_percent_or_0_001N']
    assert e['mesh_report'] in list(meshes.values())
    log=(folder/'solver.log').read_text();assert 'Job finished' in log and '*ERROR' not in log
    gate('PASS',f'FG {relative}: actual solver completion and force equilibrium only',
         {'path':relative+'/metrics.json','max_displacement_mm':m['max_displacement_mm'],
          'qualified_material_mount_or_strength_margin':None})
    if e['case']=='LC4':
        u=max(m['corner_max_abs_UZ_mm'].values())
        gate('PASS' if u<=1 else 'FAIL',f'FG {relative}: normalized corner displacement screen',
             {'path':relative+'/metrics.json','corner_UZ_mm':u,'limit_mm':1.})
    q=json.loads((folder/'quadratic-dml-clearance.json').read_text());verify(q)
    d=json.loads((folder/'deformed-clearance.json').read_text());verify(d)
    f=folder/'refined-quadratic-clearance.json'
    if q['final']['all_element_bounds_separated_from_DML_and_frontward_region']:
        gate('PASS',f'FG {relative}: final-state full quadratic FEA geometry versus fixed DML only',
             {'path':relative+'/quadratic-dml-clearance.json','separation_lower_bound_mm':q['final']['conservative_DML_separation_lower_bound_mm']})
    else:
        refinement=json.loads(f.read_text());verify(refinement)
        robust=refinement['witnesses_beyond_0p0001_mm_numerical_margin']
        gate('FAIL' if robust else 'OPEN',f'FG {relative}: refined deformed-element DML clearance',
             {'path':relative+'/refined-quadratic-clearance.json','robust_interference_witnesses':robust,
              'largest_witness_boundary_margin_mm':refinement['largest_witness_boundary_margin_mm'],'DML_contact_modeled':False})
    runs.append({'path':relative,'execution':e,'metrics':m,'quadratic_clearance':q})
assert len(runs)==4
assert mounts['artifacts']['frame']['sha256']==parent_mounts['artifacts']['frame']['sha256']

stack=read('evidence/rev-fg/gasket-stack/execution.json');verify(stack)
assert stack['force_at_20_percent_N'] is None and not stack['production_tolerances_assigned']
gate('PASS','FG catalog gasket arithmetic: conditional compression budgets and 25% reference force only',
     {'path':'evidence/rev-fg/gasket-stack/execution.json','measured_leakage_or_compression_law':False})
gate('OPEN','FG real stack tolerance, seal preload, fixed DML retainer and leakage qualification',
     {'path':'evidence/rev-fg/gasket-stack/execution.json','DML_gap_symmetric_budget_at_nominal_mm':stack['rows'][0]['maximum_symmetric_gap_budget_at_current_nominal_mm']})
gate('OPEN','FG complete deformable assembly LC1-LC7, lower capture, orthotropic strength, convergence and buckling',
     {'current_frame_only_runs':2,'actual_cleat_contact_FEA_executed':False,'qualified_strength_margin':None})
gate('OPEN','FG full product thermal CFD, complete electronics/PCB, production firmware and prototype release',
     {'full_product_CFD_executed':False,'native_MAIN_VOICE_RADAR_complete':False,'production_ready':False})

figure=read('evidence/rev-fg/mount-sections-figure.json');verify(figure)
for p,h in figure['artifact_sha256'].items():assert sha(ROOT/p)==h
for entry in read('evidence/rev-fg/sources/index.json'):
    assert sha(ROOT/entry['file'])==entry['sha256']
gates.update(revision='Rev.FG',client_checkpoint_date='2026-10-14',checkpoint_parent_head=BASE)
gates['dependency_order'].append('FG verified upper-mount and sealing CAD -> lower capture and fixed DML preload design -> complete assembly/contact FEA and full product CFD -> material/process and prototype qualification')
counts={s:sum(g['status']==s for g in gates['gates']) for s in ['PASS','FAIL','OPEN']}
summary={'revision':'Rev.FG','client_checkpoint_date':'2026-10-14','checkpoint_parent_head':BASE,
         'gate_counts_including_history':counts,'counts_are_not_completion_percentages':True,
         'new_gates':added,'executed_full_frame_runs':len(runs),'runs':runs,'meshes':meshes,
         'selected_mount_geometry':'evidence/rev-fg/upper-mounts-chamfer/execution.json',
         'frame_volume_mm3':read('evidence/rev-fg/upper-mounts-deep/frame-geometry.json')['volume_mm3'],
         'frame_calculated_mass_at_catalog_density_g':read('evidence/rev-fg/upper-mounts-deep/frame-geometry.json')['mass_g_at_catalog_density_1p22'],
         'mass_ceiling_g':None,'all_remaining_digital_work_complete':False,'production_ready':False,
         'full_product_CFD_executed':False,'physical_tests_executed':False,
         'prior_report_correction':{'revision':'FE','case':'EU20 LC1 100N weakY nonlinear','actual_sampled_DML_nodes':57,
                                    'earlier_zero_node_claim_was_incorrect':True}}
out=ROOT/'mechanical/validation/rev-fg';out.mkdir(parents=True,exist_ok=True)
(out/'gate-register.json').write_text(json.dumps(gates,indent=2)+'\n')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
sources=sorted((ROOT/'mechanical/cad').glob('*rev_fg.py'))
sources.append(ROOT/'tools/package_rev_fg.py')
sources+=[ROOT/'mechanical/digital-validation-rev-fg.md',ROOT/'manufacturing/real-data-addendum-rev-fg.md',ROOT/'mechanical/components/upper-mount-candidates-rev-fg.json']
evidence=sorted(p for p in (ROOT/'evidence/rev-fg').rglob('*') if p.is_file() and p.name not in ['provenance.json','raw-artifact-index.json','github-publication.json','archive-tree-verification.json'])
provenance={'revision':'Rev.FG','checkpoint_parent_head':BASE,'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},
            'evidence_hashes':{str(p.relative_to(ROOT)):sha(p) for p in evidence},
            'solver_sha256':sha(ROOT.parent/'solvers/CalculiX/ccx_2.23/src/ccx_2.23'),'solver_version':'CalculiX 2.23',
            'production_qualified':False}
(ROOT/'evidence/rev-fg/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'executed_frame_runs':len(runs),'gate_counts_including_history':counts,'new_gates':len(added)},indent=2))
