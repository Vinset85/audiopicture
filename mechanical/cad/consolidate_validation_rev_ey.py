"""Consolidate executed evidence. Never derive a product release from solver exit codes."""
from pathlib import Path
import json,hashlib,ast,subprocess,re
import numpy as np
root=Path(__file__).resolve().parents[2];out=root/'mechanical/validation/rev-et-ey';out.mkdir(exist_ok=True)
def read(p):return json.loads((root/p).read_text())
def dump(name,v):(out/name).write_text(json.dumps(v,indent=2,ensure_ascii=False))
base=read('mechanical/validation/rev-en-es/gate-register.json');base['revision']='Rev.EY';base['status']='PARTIAL_DIGITAL_VALIDATION_WITH_CONFIRMED_FAILURES_NOT_PRODUCTION_RELEASE';gates=base['gates'];byid={g['id']:g for g in gates}
byid['G20'].update(status='PASS',scope='Elmer official NaturalConvection reference converges at three relaxation factors',evidence={'coupled_warnings':0,'relaxation_factors':[.1,.2,.35],'scope':'water reference only; not product CFD'})
byid['G17']['evidence']='Full candidate frame screens now executed. Exact cleat/contact geometry, qualified allowables, temperature/orientation cases, full LC7 locations and physical correlation remain OPEN.'
byid['G23']['evidence']='Portable governor core host-tested; full ESP-IDF drivers/app, networking, Home Assistant, OTA and hardware tests OPEN.'
byid['G22']['evidence']='74 BOM rows, 26 active rows lack exact orderable MPN, 5 optional/removed; native schemas/boards and ERC/DRC still absent.'
byid['G07']['scope']='Rev.EQ with Rev.ES coarse frame only: BREP/export/reimport and clearance (does not apply to Rev.EU)'
new=[]
def gate(i,status,scope,evidence):new.append(dict(id=f'G{i:02}',status=status,scope=scope,evidence=evidence))
frames={v:read(f'evidence/rev-eu{v}/execution.json') for v in [4,5,6,7,8,9,10] if (root/f'evidence/rev-eu{v}/execution.json').exists()}
for v,r in frames.items():r['catalog_density_g_per_cm3']=1.22;r['calculated_homogeneous_mass_g']=r['volume_mm3']*.00122;r['frame_250g_target_status']='PASS' if r['calculated_homogeneous_mass_g']<=250 else 'FAIL'
dump('frame-candidates.json',frames)
gate(27,'FAIL','Rev.EU.4 homogeneous frame catalog-density mass <=250 g',{'mass_g':frames[4]['calculated_homogeneous_mass_g'],'source':'Prusament PC-CF TDS, density 1.22 g/cm3','measured':False})
nonlinear=read('evidence/rev-ev4/M0-contactK100k-MAT-B/metrics.json');lc4=next(x for x in nonlinear if x['case']=='LC4')
gate(28,'FAIL','Rev.EU.4 normalized nonlinear LC4 lower-right corner displacement <=1 mm',{'normal_displacement_mm':lc4['corner_max_abs_UZ_mm']['CORNER_LR'],'load_N':30,'exact_wall_hardware_model':False})
gate(29,'FAIL','Rev.EU.4 to Rev.EQ baffle clearance >=1 mm target',{'clearance_mm':frames[4]['shell_clearance_mm'],'collision_volume_mm3':frames[4]['collision_volume_mm3']['shell_EQ']})
gate(30,'OPEN','Complete enclosure closure, DML seal, service/ENV/cable openings',read('evidence/rev-ex/enclosure-completion.json'))
gate(31,'PASS','Rev.EU.4 valid/reimported single solid, zero listed coarse keepout intersections',{'valid':frames[4]['valid'],'solid_count':frames[4]['solid_count'],'collision_volume_mm3':frames[4]['collision_volume_mm3'],'exact_RF_DMU':False})
sens=read('mechanical/validation/rev-et-ex/frame-material-cg-sensitivities.json');assert len(sens['cases'])==31 and all(x['solver_execution_pass'] and x['force_balance_pass'] for x in sens['cases'])
material=[x for x in sens['cases'] if x['id'].startswith('EZ')];cg=[x for x in sens['cases'] if x['id'].startswith('CG')]
gate(32,'PASS','Full candidate LC1 normalized material/CG execution only',{'material_cases':len(material),'additional_cg_cases':len(cg),'material_displacement_range_mm':[min(x['displacement_mm'] for x in material),max(x['displacement_mm'] for x in material)],'cg_displacement_range_mm':[min(x['displacement_mm'] for x in cg),max(x['displacement_mm'] for x in cg)]})
meshes=[]
for m,path in [('M0','material-cg-sensitivities/EZ0.35-GX0.4-GY0.4'),('M1','M1-linear-MAT-B'),('M2','M2-linear-MAT-B')]:
 r=read(f'evidence/rev-ev4/{path}/LC1/metrics.json');mesh=read(f'evidence/rev-ev4/{m}/mesh-report.json');meshes.append({'id':m,**mesh,'Umax_mm':r['max_displacement_mm'],'raw_nodal_von_mises_MPa':r['nodal_extrapolated_stress_diagnostic']['von_mises_max_MPa'],'raw_peak_xyz_mm':r['nodal_extrapolated_stress_diagnostic']['xyz_mm']})
for i in range(1,len(meshes)):
 for metric in ['Umax_mm','raw_nodal_von_mises_MPa']:meshes[i][metric+'_change_percent']=abs(meshes[i][metric]-meshes[i-1][metric])/abs(meshes[i][metric])*100
dump('frame-mesh-convergence.json',{'classification':'NORMALIZED_LINEAR_LC1_ONLY','levels':meshes,'non_singular_stress_status':'OPEN: raw nodal peak moved; notch/mesh classification and local mesh contract not closed; no release margin'})
gate(33,'PASS','Normalized full-candidate linear LC1 displacement mesh convergence only',{'M1_M2_change_percent':meshes[-1]['Umax_mm_change_percent'],'non_singular_stress_release':'OPEN'})
buck=next(x for x in read('evidence/rev-ev4/M1-linear-MAT-B/metrics.json') if x['case']=='BUCKLE');assert buck['solver_execution_pass'] and len(buck['buckling_factors'])==3
gate(34,'PASS','Eigenvalue buckling execution, seed 70 N load and bonded interfaces',{'factors':buck['buckling_factors'],'imperfection_nonlinear_release':False})
fw=read('mechanical/validation/rev-et-ex/firmware-host-tests.json');assert '200000 deterministic events' in fw['result_log']
for p,digest in fw['source_sha256'].items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest
gate(35,'PASS','Portable governor host tests with address/undefined behavior sanitizers',{'events':200000,'input_combinations':320,'hardware_tested':False,'calibration_is_test_fixture':True})
gate(36,'OPEN','Ag53024 output capacitance/startup/stability with downstream audio bulk',{'catalog_Cout_uF':[180,220,330],'local_proposed_uF':220,'audio_bulk_proposed_uF':470,'connected_capacitance_requires_native_circuit_review':True,'measured_instability_claimed':False})
cavity=read('evidence/rev-ey/summary.json');last=cavity['results'][-1];assert len(cavity['results'])==3 and all(x['solver_execution']['exit_code']==0 and x['solver_execution']['coupled_warnings']==0 and not x['solver_execution']['nan'] for x in cavity['results'])
assert last['relative_Nu_error_percent']<1 and last['hot_cold_balance_percent']<.1 and last['previous_mesh_Nu_change_percent']<5
gate(37,'PASS','de Vahl Davis Ra1000 Pr0.71 numerical Boussinesq benchmark',{'meshes':[x['n'] for x in cavity['results']],'Nu_hot':last['Nu_hot'],'reference_Nu':1.118,'error_percent':last['relative_Nu_error_percent'],'hot_cold_balance_percent':last['hot_cold_balance_percent'],'mesh_change_percent':last['previous_mesh_Nu_change_percent'],'product_CFD':False})
gate(38,'FAIL','Rev.EU.5 lighter geometry candidate rejected',{'mass_g':frames[5]['calculated_homogeneous_mass_g'],'target_mass_g':250,'shell_clearance_mm':frames[5]['shell_clearance_mm'],'target_clearance_mm':1,'full_FEA_claimed':False})
retry=root/'evidence/rev-ev4/M0-contactK10k-retry/metrics.json'
if retry.exists():dump('frame-contact-retry.json',json.loads(retry.read_text()))
warp=[]
for path in ['M0-warp0.25','M0-contactK100k-MAT-B','M0-warp1']:
 entry=read(f'evidence/rev-ev4/{path}/LC7/execution.json');r=read(f'evidence/rev-ev4/{path}/LC7/metrics.json')
 warp.append({'imposed_corner_warp_mm':entry['corner_warp_mm'],**r})
dump('frame-warp-sensitivity.json',{'classification':'ONE_CORNER_NORMALIZED_SCREEN_NOT_ALL_LC7_LOCATIONS','cases':warp})
if 8 in frames:
 f=frames[8]
 gate(39,'PASS' if f['shell_clearance_mm']>=.999999 else 'FAIL','Rev.EU.8 BREP and coarse geometry clearance only',{'valid':f['valid'],'solid_count':f['solid_count'],'reimport_valid':f['reimport_valid'],'reimport_solids':f['reimport_solids'],'clearance_mm':f['shell_clearance_mm'],'overlaps_mm3':f['collision_volume_mm3'],'exact_DMU':False})
 gate(40,f['frame_250g_target_status'],'Rev.EU.8 homogeneous catalog-density frame mass <=250 g',{'mass_g':f['calculated_homogeneous_mass_g'],'includes_inserts_or_future_fillets':False,'measured':False})
 result=root/'evidence/rev-ev8/M0-contactK100k-MAT-B/metrics.json'
 if result.exists():
  newframe=json.loads(result.read_text());dump('frame-EU8-screen.json',newframe)
  torsion=next((r for r in newframe if r['case']=='LC4'),None)
  if torsion and torsion['solver_execution_pass']:
   gate(41,'PASS' if max(torsion['corner_max_abs_UZ_mm'].values())<=1 else 'FAIL','Rev.EU.8 normalized single-corner LC4 only',{'corner_abs_UZ_mm':torsion['corner_max_abs_UZ_mm'],'all_corners_tested':False,'qualified_material':False})
  else:gate(41,'OPEN','Rev.EU.8 normalized LC4','Solver completion or results missing; no pass claimed')
for v,number in [(9,42),(10,43)]:
 if v not in frames:continue
 f=frames[v];result=root/f'evidence/rev-ev{v}/M0-contactK100k-MAT-B/metrics.json'
 if not result.exists():continue
 records=json.loads(result.read_text());dump(f'frame-EU{v}-screen.json',records)
 r=next((r for r in records if r['case']=='LC4'),None)
 linear=root/f'evidence/rev-ev{v}/M0-linear-MAT-B/metrics.json'
 if linear.exists():dump(f'frame-EU{v}-linear.json',json.loads(linear.read_text()))
 passed=bool(r and r['solver_execution_pass'] and r['force_balance_within_0_1_percent_or_0_001N'] and max(r['corner_max_abs_UZ_mm'].values())<=1 and f['calculated_homogeneous_mass_g']<=250 and f['shell_clearance_mm']>=.999999)
 gate(number,'PASS' if passed else 'FAIL' if r and r['solver_execution_pass'] else 'OPEN',f'Rev.EU.{v} combined catalog-mass/coarse-clearance/normalized one-corner LC4 screen only',{'mass_g':f['calculated_homogeneous_mass_g'],'clearance_mm':f['shell_clearance_mm'],'LC4_corner_abs_UZ_mm':r.get('corner_max_abs_UZ_mm') if r else None,'qualified_material':False,'full_mesh_material_CG_matrix_on_this_geometry':False})
dump('perimeter-coupons.json',read('evidence/rev-ey/perimeter-coupons/execution.json'))
dump('bom-reconciliation.json',read('evidence/rev-ex/bom-reconciliation.json'))
dump('toolchain-current.json',read('mechanical/validation/rev-et-ex/toolchain-current.json'))
dump('frame-contact-K100k.json',nonlinear);dump('frame-material-cg-sensitivities.json',sens);dump('cavity-benchmark.json',cavity)
for src,dst in [('mechanical/validation/rev-et-ex/convection-benchmark.json','convection-benchmark.json'),('mechanical/validation/rev-et-ex/firmware-host-tests.json','firmware-host-tests.json'),('evidence/rev-ex/bom-audit.json','bom-audit.json'),('evidence/rev-ex/enclosure-completion.json','enclosure-completion.json')]:dump(dst,read(src))
base['gates']=gates+new;base['dependency_order']+=['Frame mass/torsion/clearance redesign -> exact mounts/DMU -> qualified FEA','Complete shell/service/front-seal geometry -> full CHT CFD01-CFD05','Native circuit/output-capacitance analysis -> PCB -> hardware power-governor validation'];dump('gate-register.json',base)
syntax=[]
for p in root.rglob('*.py'):
 if 'evidence' in p.parts or '.git' in p.parts:continue
 ast.parse(p.read_text());syntax.append(str(p.relative_to(root)))
dump('syntax-validation.json',{'parsed_python_files':len(syntax),'files':syntax,'scope':'syntax only, not an execution claim'})
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();assert head==base['base_head']
dump('integrity.json',{'head':head,'files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='integrity.json'}})
print(json.dumps({'gates':len(base['gates']),'counts':{s:sum(g['status']==s for g in base['gates']) for s in ['PASS','FAIL','OPEN']},'syntax_files':len(syntax)},indent=2))
