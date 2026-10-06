"""Complete native ENV seed through kicad-skip; validate with actual KiCad 9.

ENV's native-capture-contract explicitly permits validated automation. Symbol
instances originate in the native GUI seed / official KiCad 9.0.8 demo; library
definitions come from the installed KiCad libraries. No handwritten schematic
text is emitted. A successful script is not an ERC or production PASS.
"""
import argparse, copy, uuid
from pathlib import Path
import skip
from types import SimpleNamespace
from skip.sexp.sourcefile import SourceFile

p=argparse.ArgumentParser()
p.add_argument('--seed',type=Path,required=True)
p.add_argument('--demo',type=Path,required=True)
p.add_argument('--libraries',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
s=skip.Schematic(str(a.seed)); demo=skip.Schematic(str(a.demo))
project=a.out.stem

def library(name):
    family,part=name.split(':')
    lib=SourceFile(str(a.libraries/f'{family}.kicad_sym'))
    raw=copy.deepcopy(next(x.raw for x in lib.symbol if x.value==part))
    raw[1]=name
    # Import the exact official library node, preserving all electrical fields.
    s.lib_symbols._pv.raw.append(raw)

for name in ['power:PWR_FLAG','Connector:TestPoint']:library(name)
s.write(str(a.out)); s=skip.Schematic(str(a.out))
def annotate(sym,ref):
    sym.property.Reference.value=ref
    sym.instances.project.value=project
    sym.instances.project.path.value='/'+s.uuid.value
    sym.instances.project.path.reference.value=ref

c=s.symbol.C301
annotate(c,'C301');c.move(139.7,63.5)
for ref,value,xy,dnp in [('C302','100nF X7R',(228.6,63.5),False),
                         ('C303','1uF X7R',(76.2,101.6),True)]:
    x=c.clone(); annotate(x,ref);x.property.Value.value=value;x.dnp.value=dnp;x.move(*xy)
s.symbol.J301.move(50.8,63.5)
s.symbol.U301.move(114.3,63.5)
s.symbol.U301.property.Datasheet.value='https://sensirion.com/resource/datasheet/sht4x'
s.symbol.U301.property.Description.value='Sensirion SHT45-AD1F-R2 / article 3.000.886; integrated polyimide membrane per datasheet v7.3.'
s.symbol.U302.move(198.12,63.5)
s.symbol.U302.property.Footprint.value='AudioPicture_ENV:TI_DNP0006A_OPT3004'
for ref,mpn in [('C301','C1608X7R1H104K080AA'),('C302','C1608X7R1H104K080AA'),('C303','C1608X7R1C105K080AC')]:
    sym=next(x for x in s.symbol if x.property.Reference.value==ref)
    sym.property.Datasheet.value='https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no='+mpn
    sym.property.Description.value='TDK '+mpn+'; catalog selection. PCB placement/assembly qualification open.'

flag=next(x for x in demo.symbol if 'PWR_FLAG' in x.lib_id.value)
for ref,lib,xy,value,footprint in [
    ('#FLG0301','power:PWR_FLAG',(35.56,96.52),'PWR_FLAG',''),
    ('#FLG0302','power:PWR_FLAG',(55.88,96.52),'PWR_FLAG',''),
    ('TP301','Connector:TestPoint',(111.76,101.6),'TP_3V3','TestPoint:TestPoint_Pad_D1.0mm'),
    ('TP302','Connector:TestPoint',(137.16,101.6),'TP_GND','TestPoint:TestPoint_Pad_D1.0mm'),
    ('TP303','Connector:TestPoint',(170.18,101.6),'TP_SDA','TestPoint:TestPoint_Pad_D1.0mm'),
    ('TP304','Connector:TestPoint',(203.2,101.6),'TP_SCL','TestPoint:TestPoint_Pad_D1.0mm'),
]:
    obj=s.wrap(s.new_from_list(flag.raw))
    for u in obj.getElementsByEntityType('uuid'):u.value=str(uuid.uuid4())
    obj.lib_id.value=lib; annotate(obj,ref);obj.move(*xy)
    obj.property.Value.value=value;obj.property.Footprint.value=footprint
    obj.property.Reference.effects.hide.value=ref.startswith('#')
    if ref.startswith('TP'):
        for prop,y in [('Reference',xy[1]-7.62),('Value',xy[1]-5.08)]:
            field=getattr(obj.property,prop)
            field.at.value=[xy[0],y,0]
            field.effects.font.size.value=[1.0,1.0]

s.write(str(a.out));s=skip.Schematic(str(a.out))
pins={}
for x in s.symbol:
    ref=x.property.Reference.value
    if ref.startswith('#') or ref.startswith('TP'):
        # kicad-skip's pin collection assumes multiple pins. For these two
        # official one-pin symbols, verify the library anchor explicitly.
        lp=x.lib_symbol.getElementsByEntityType('pin')
        assert len(lp)==1 and lp[0].number.value=='1' and lp[0].at.value[:2]==[0,0]
        assert x.at.value[2]==0
        pins[ref]={'1':SimpleNamespace(location=SimpleNamespace(value=x.at.value[:2]+[0]))}
    else:
        pins[ref]={v.number:v for v in x.pin}
def attach(ref,number,name,dx=None,dy=None):
    pin=pins[ref][str(number)]
    pos=pin.location.value[:2];angle=pin.location.value[2]
    if dx is None:
        dx,dy={0:(-15.24,0),180:(7.62,0),90:(0,5.08),270:(0,-5.08)}[angle]
    end=[round(pos[0]+dx,5),round(pos[1]+dy,5)]
    w=s.wire.new(); w.start_at(pos);w.end_at(end)
    label=s.label.new();label.value=name;label.move(*end)
    label.effects.font.size.value=[1.0,1.0]

nets={
 'J301':{'1':'+3V3_SYS','2':'+3V3_SYS','3':'GND','4':'GND','5':'I2C_SDA','6':'I2C_SCL'},
 'U301':{'1':'I2C_SDA','2':'I2C_SCL','3':'+3V3_SYS','4':'GND'},
 'U302':{'1':'+3V3_SYS','2':'+3V3_SYS','3':'GND','4':'I2C_SCL','6':'I2C_SDA','7':'GND'},
 'C301':{'1':'+3V3_SYS','2':'GND'},'C302':{'1':'+3V3_SYS','2':'GND'},'C303':{'1':'+3V3_SYS','2':'GND'},
 '#FLG0301':{'1':'+3V3_SYS'},'#FLG0302':{'1':'GND'},
 'TP301':{'1':'+3V3_SYS'},'TP302':{'1':'GND'},'TP303':{'1':'I2C_SDA'},'TP304':{'1':'I2C_SCL'},
}
for ref,mapping in nets.items():
    for pin,net in mapping.items():
        if ref.startswith('#') or ref.startswith('TP'):attach(ref,pin,net,0,5.08)
        elif ref=='U302' and pin=='7':attach(ref,pin,net,0,8.89)
        else:attach(ref,pin,net)
for ref,pin in [('J301','7'),('J301','8'),('U302','5')]:
    nc=s.new_from_list(demo.no_connect[0].raw)
    nc.uuid.value=str(uuid.uuid4());nc.move(*pins[ref][pin].location.value[:2])

for xy,value,size in [
 ((139.7,25.4),'AudioPicture V2.2 - ENV Rev.EZ',2.54),
 ((139.7,33.02),'Electrical capture candidate - PCB and calibration NOT RELEASED',1.27),
 ((139.7,124.46),'MAIN owns I2C pull-ups. 100 kHz baseline. No local regulator.',1.27),
 ((139.7,130.81),'ADDR = VDD: OPT3004 0x45. SHT45 0x44. INT / BOARD_ID reserved NC.',1.27),
 ((139.7,137.16),'PWR_FLAG marks incoming MAIN supply and return at J301; no other power source.',1.27),
 ((139.7,143.51),'C301/C302 local bypass; C303 DNP bulk. MPNs selected; PCB qualification OPEN.',1.27),
 ((139.7,149.86),'SHT45 central die pad: no copper / no solder. OPT3004 EP: GND.',1.27),
 ((139.7,156.21),'FPC contact side / pin-1 mating orientation and sensor chamber placement OPEN.',1.27),
]:
    t=s.text.new();t.value=value;t.move(40.64,xy[1]);t.effects.font.size.value=[size,size]
s.generator.value='audiopicture_validated_automation'
s.write(str(a.out))
print(f'Generated {a.out}; native ERC and netlist verification required.')
