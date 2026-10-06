"""Independently check KiCad-exported ENV XML against the pin contract.

Do not read the schematic generator's mapping: an ERC-clean wrong address
strap, swapped bus pin, or omitted power connection must still fail here.
"""
import argparse, hashlib, json
from pathlib import Path
import xml.etree.ElementTree as ET

p=argparse.ArgumentParser()
p.add_argument('--netlist',type=Path,required=True)
p.add_argument('--erc',type=Path,required=True)
p.add_argument('--report',type=Path,required=True)
a=p.parse_args()
root=ET.parse(a.netlist).getroot()
erc=json.loads(a.erc.read_text())
violations=[v for s in erc['sheets'] for v in s['violations']]
assert not violations, violations
expected={
 '+3V3_SYS':{'J301.1','J301.2','U301.3','U302.1','U302.2','C301.1','C302.1','C303.1','TP301.1'},
 'GND':{'J301.3','J301.4','U301.4','U302.3','U302.7','C301.2','C302.2','C303.2','TP302.1'},
 'I2C_SDA':{'J301.5','U301.1','U302.6','TP303.1'},
 'I2C_SCL':{'J301.6','U301.2','U302.4','TP304.1'},
}
actual={};nc=set()
for net in root.findall('nets/net'):
    nodes={n.get('ref')+'.'+n.get('pin') for n in net.findall('node')}
    if net.get('name').startswith('unconnected-'):
        assert len(nodes)==1 and '+no_connect' in net.find('node').get('pintype')
        nc.update(nodes)
    else:actual[net.get('name').lstrip('/')]=nodes
assert actual==expected, {'actual':actual,'expected':expected}
assert nc=={'J301.7','J301.8','U302.5'}, nc
components={c.get('ref'):c for c in root.findall('components/comp')}
assert set(components)=={'J301','U301','U302','C301','C302','C303','TP301','TP302','TP303','TP304'}
assert components['U302'].findtext('footprint')=='AudioPicture_ENV:TI_DNP0006A_OPT3004'
assert components['U301'].findtext('footprint').endswith('SHT4x_NoCentralPad')
assert components['J301'].findtext('value')=='FH12-8S-0.5SH(55)'
assert any(q.get('name')=='dnp' for q in components['C303'].findall('property'))
assert not any(q.get('name')=='dnp' for ref in ['C301','C302','U301','U302','J301'] for q in components[ref].findall('property'))
report={'status':'PASS_ELECTRICAL_CAPTURE_SCOPE_ONLY','kicad_version':erc['kicad_version'],
        'erc_errors_warnings_exclusions':len(violations),'components_without_power_flags':len(components),
        'connected_pin_count':sum(map(len,actual.values())),'explicit_no_connect_pin_count':len(nc),
        'nets':{k:sorted(v) for k,v in actual.items()},'no_connect':sorted(nc),
        'checks':['Exact pin memberships from independent KiCad XML','OPT3004 ADDR tied VDD (0x45)',
                  'No ENV pull-up resistor components','C303 DNP; bypass capacitors populated',
                  'SHT45 no-central-pad and OPT3004 dedicated EP footprints'],
        'source_hashes':{str(x.name):hashlib.sha256(x.read_bytes()).hexdigest() for x in [a.netlist,a.erc]},
        'not_closed':['PCB placement/routing/DRC','Mating FPC orientation','Thermal chamber and optical tunnel',
                      'Hardware bus, sensor and assembly tests','Capacitor placement and assembly qualification']}
a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
