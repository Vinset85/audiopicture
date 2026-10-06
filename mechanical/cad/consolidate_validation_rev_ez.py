"""Consolidate actual Rev.EZ evidence, never promote the product to release."""
import json, hashlib, shutil, subprocess, datetime
import xml.etree.ElementTree as ET
from pathlib import Path

repo=Path(__file__).resolve().parents[2]
workspace=repo.parent.parent
e=repo/'evidence/rev-ez'; dst=repo/'mechanical/validation/rev-ez'
dst.mkdir(parents=True,exist_ok=True)
def read(path):return json.loads((repo/path).read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
assert head=='19a436701211b5135ecb1b672eae44f177894629'
cad=read('evidence/rev-eu11/execution.json')
lc1=read('evidence/rev-ev11/M0-linear-MAT-B/LC1/metrics.json')
lc4=read('evidence/rev-ev11/M0-contactK100k-MAT-B/LC4/metrics.json')
mesh=read('evidence/rev-ev11/M0/mesh-report.json')
assert cad['valid'] and cad['reimport_valid'] and cad['solid_count']==cad['reimport_solids']==1
assert max(cad['collision_volume_mm3'].values())<1e-6
assert mesh['source_sha256']==cad['sha256']
assert lc1['solver_execution_pass'] and lc4['solver_execution_pass']
assert lc1['force_balance_within_0_1_percent_or_0_001N'] and lc4['force_balance_within_0_1_percent_or_0_001N']
env=read('evidence/rev-ez/env-electrical-check.json')
assert env['erc_errors_warnings_exclusions']==0
for name,sha in env['source_hashes'].items():assert digest(e/name)==sha
fp=read('evidence/rev-ez/opt3004-footprint.json')
assert digest(repo/'hardware/kicad/environment/lib/AudioPicture_ENV.pretty/TI_DNP0006A_OPT3004.kicad_mod')==fp['sha256']
optical=read('evidence/rev-ez/env-optical-path-audit.json')
bom=read('evidence/rev-ez/bom-audit.json')
assert digest(repo/'hardware/bom/audiopicture-v2.2-rev-a.csv')==bom['sha256']
host=ET.parse(e/'firmware-host-tests.xml').getroot()
ha=ET.parse(e/'home-assistant-tests.xml').getroot().find('testsuite')
assert host.get('tests')=='3' and host.get('failures')=='0'
assert ha.get('tests')=='32' and ha.get('failures')==ha.get('errors')=='0'
coverage=read('evidence/rev-ez/home-assistant-coverage.json')['totals']
assert coverage['covered_lines']==coverage['num_statements']==181
buildlog=workspace/'work/idf-build-rev-ez-status.log'
assert 'Project build complete.' in buildlog.read_text()
build=workspace/'work/firmware-idf-build'
files=['audiopicture.bin','bootloader/bootloader.bin','partition_table/partition-table.bin','ota_data_initial.bin','flasher_args.json']
for name in files:
    target=e/'firmware-bin'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(build/name,target)
assert (e/'firmware-bin/audiopicture.bin').stat().st_size==851936
for source,name in [(buildlog,'firmware-idf-build.log'),(workspace/'work/ha-tests.log','home-assistant-tests.log'),
                    (workspace/'work/env-erc.log','env-erc.log'),(workspace/'work/env-netlist.log','env-netlist.log')]:
    if source.exists():shutil.copy2(source,e/name)
tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=repo).decode().split('\0')
software=[repo/p for p in tracked if p.startswith(('firmware/','home-assistant/','hardware/kicad/environment/')) and (repo/p).is_file()]
provenance={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_head':head,
 'classification':'EXECUTED_DIGITAL_DIAGNOSTIC_AND_CANDIDATE_EVIDENCE_NOT_PRODUCT_RELEASE',
 'versions':{'ESP_IDF':'v5.5.3 / 2c211b236707889e8400c4dc5644dd5c4ee071e0','KiCad':'9.0.8','kicad_skip':'0.2.5','Home_Assistant':'2026.9.4'},
 'firmware_app_bytes':851936,'physical_tests_executed':False,
 'source_hashes':{str(p.relative_to(repo)):digest(p) for p in sorted(software)},
 'binary_hashes':{name:digest(e/'firmware-bin'/name) for name in files},
 'test_dates':{'host':host.get('timestamp'),'home_assistant':ha.get('timestamp')},
 'limits':['Source snapshot at consolidation; hash collection is not itself a new test run.',
           'ESP image compiled but not flashed; transport mocks do not validate PCB/hardware.',
           'Home Assistant tests unchanged since 2026-10-01; 100% line coverage is not branch coverage.']}
(e/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
sources={}
for name,url in [('OPT3004','https://www.ti.com/lit/ds/symlink/opt3004.pdf'),('SHT4x','https://sensirion.com/resource/datasheet/sht4x'),('INA228','https://www.ti.com/lit/ds/symlink/ina228.pdf'),('TCA9534','https://www.ti.com/lit/ds/symlink/tca9534.pdf'),('Ag53000-Datasheet','https://silvertel.com/images/datasheets/Ag53000-Datasheet.pdf')]:
    p=workspace/'work/vendor-sources'/f'{name}.pdf';sources[name]={'url':url,'sha256':digest(p),'bytes':p.stat().st_size}
(e/'manufacturer-source-hashes.json').write_text(json.dumps(sources,indent=2)+'\n')
g=read('mechanical/validation/rev-et-ey/gate-register.json');g['revision']='Rev.EZ'
g['recorded_utc']=provenance['recorded_utc']
for gate in g['gates']:
    if gate['id']=='G22':gate['evidence']={'BOM_rows':bom['rows'],'active_rows_not_fully_orderable':bom['active_rows_without_exact_mpn'],'optional_or_removed':bom['optional_or_removed'],'ENV_schematic_ERC_and_netlist':'PASS_SCOPE_ONLY','MAIN_VOICE_RADAR_schematics_and_all_PCBS':'OPEN','note':bom['audit_note']}
    if gate['id']=='G23':gate['evidence']='Diagnostic ESP32-S3 image compiled, three host suites pass, Home Assistant diagnostic integration 32 tests pass. Complete audio/voice/radar, commissioning, OTA, integrated governor and hardware validation remain OPEN.'
def gate(i,status,scope,evidence):g['gates'].append({'id':f'G{i:02d}','status':status,'scope':scope,'evidence':evidence})
gate(44,'PASS','Rev.EU.11 BREP/export/reimport, coarse collision/clearance and catalog-density mass only',{'volume_mm3':cad['volume_mm3'],'catalog_density_g_cm3':1.22,'calculated_mass_g':cad['volume_mm3']*.00122,'clearance_mm':cad['shell_clearance_mm'],'overlaps_mm3':cad['collision_volume_mm3'],'fillets_inserts_exact_DMU_included':False})
gate(45,'FAIL','Rev.EU.11 normalized lower-right 30 N LC4, limit 1 mm',{'corner_displacement_mm':lc4['corner_max_abs_UZ_mm']['CORNER_LR'],'mesh_elements':mesh['elements'],'mesh_nodes':mesh['nodes'],'force_balance_pass':True,'material_and_contacts_qualified':False,'convergence_on_this_revision':False})
gate(46,'PASS','Rev.EU.11 LC1 solver execution and equilibrium only',{'max_displacement_mm':lc1['max_displacement_mm'],'max_displacement_xyz_mm':lc1['max_displacement_xyz_mm'],'force_balance_pass':True,'mechanical_acceptance_claimed':False})
gate(47,'PASS','Portable firmware host protocol/governor/input-expander tests with ASan and UBSan',{'suites':3,'governor_events':200000,'governor_combinations':320,'CRC_single_bit_corruptions':48,'status_patterns':256,'invalid_status_configs':510,'hardware_test':False})
gate(48,'PASS','ESP32-S3 diagnostic image actual compilation only',{'bytes':851936,'ESP_IDF':'5.5.3','audio_voice_radar_enabled':False,'flashed':False})
gate(49,'PASS','Home Assistant diagnostic integration automated host tests only',{'tests':32,'line_statements_covered':181,'line_statements_total':181,'branch_coverage_claimed':False,'installed_on_user_HA':False})
gate(50,'PASS','ENV native KiCad electrical capture and independent pin-netlist check only',env)
gate(51,'PASS','OPT3004 manufacturer land-pattern copper/paste geometry, native save/reload only',fp)
gate(52,'FAIL','Unobstructed straight optical path from current ENV seed',optical)
gate(53,'OPEN','ENV PCB/chamber/optical path and FPC integration','Complete placement/routing/DRC and a verified optical route are required; existing ENV Z sweep alone does not solve G52.')
gate(54,'OPEN','MAIN status conditioning and isolated PoE classification','TCA9534 digital contract/driver implemented. Analog thresholds/conditioners, isolator implementation and Type-2 negotiation remain unqualified. Raw input never sets type2_verified.')
g['dependency_order']+=['G52 -> actual optical route/ENV outline -> G53 -> P15 sensor characterization','G54 + native MAIN + calibrated monitor -> integrated governor -> P14 electrical tests']
(dst/'gate-register.json').write_text(json.dumps(g,indent=2)+'\n')
summary={'revision':'Rev.EZ','base_head':head,'gate_counts':{s:sum(x['status']==s for x in g['gates']) for s in ['PASS','FAIL','OPEN']},'counts_are_completion_percentage':False,'frame_EU11':{'CAD':cad,'mesh':mesh,'LC1':lc1,'LC4':lc4},'ENV':env,'optical_path':optical,'software':{'host_suites':3,'ha_tests':32,'ha_line_coverage':coverage,'firmware_bytes':851936},'BOM':{k:v for k,v in bom.items() if k!='items'},'production_ready':False,'all_remaining_digital_work_complete':False}
(dst/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'consolidated':True,'gate_counts':summary['gate_counts'],'production_ready':False},indent=2))
