"""Build TI DNP0006A land pattern using KiCad's native pcbnew API.

Source: OPT3004 SBOS929A, package drawing 4221434/C (01/2018),
land pattern and stencil examples. Dimensions in mm; mask/courtyard are
documented design choices, not manufacturer tolerances. No PCB release.
Run with the Python interpreter bundled with KiCad 9.0.8.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pcbnew as k

p = argparse.ArgumentParser()
p.add_argument('--library', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
a = p.parse_args()
a.library.mkdir(parents=True, exist_ok=True)
name = 'TI_DNP0006A_OPT3004'
fp = k.FOOTPRINT(None)
fp.SetFPID(k.LIB_ID('AudioPicture_ENV', name))
fp.SetAttributes(k.FP_SMD)
fp.SetLibDescription('OPT3004 DNP0006A; TI 4221434/C. EP GND. Fabrication process/vias OPEN.')
fp.SetValue('OPT3004DNPR')
fp.SetReference('REF**')

def xy(x, y): return k.VECTOR2I(k.FromMM(x), k.FromMM(y))

def layers(*items):
    result = k.LSET()
    for item in items: result.AddLayer(item)
    return result

def pad(number, x, y, w, h, shape, ls):
    item = k.PAD(fp)
    item.SetNumber(number)
    item.SetAttribute(k.PAD_ATTRIB_SMD)
    item.SetShape(shape)
    item.SetPosition(xy(x, y))
    item.SetSize(xy(w, h))
    item.SetLayerSet(layers(*ls))
    item.SetLocalSolderMaskMargin(k.FromMM(.05))
    item.SetLocalSolderPasteMargin(0)
    item.SetLocalSolderPasteMarginRatio(0.0)
    fp.Add(item)

for num, x, y in [(1,-.95,-.65),(2,-.95,0),(3,-.95,.65),
                  (4,.95,.65),(5,.95,0),(6,.95,-.65)]:
    pad(str(num), x, y, .5, .25, k.PAD_SHAPE_OVAL, [k.F_Cu,k.F_Mask,k.F_Paste])
pad('7', 0, 0, .65, 1.35, k.PAD_SHAPE_RECT, [k.F_Cu,k.F_Mask])
# The stencil opening has unequal X/Y reductions. A separate native paste
# aperture preserves TI's 0.62 x 1.25 example without distorting the copper EP.
pad('', 0, 0, .62, 1.25, k.PAD_SHAPE_RECT, [k.F_Paste])

def line(x1, y1, x2, y2, layer, width):
    item = k.PCB_SHAPE(fp)
    item.SetShape(k.SHAPE_T_SEGMENT)
    item.SetStart(xy(x1,y1)); item.SetEnd(xy(x2,y2))
    item.SetLayer(layer); item.SetWidth(k.FromMM(width)); fp.Add(item)

fab = [(-1,-.6),(-.6,-1),(1,-1),(1,1),(-1,1),(-1,-.6)]
for p1,p2 in zip(fab,fab[1:]): line(*p1,*p2,k.F_Fab,.1)
ct = [(-1.45,-1.3),(1.45,-1.3),(1.45,1.3),(-1.45,1.3),(-1.45,-1.3)]
for p1,p2 in zip(ct,ct[1:]): line(*p1,*p2,k.F_CrtYd,.05)
# Only external silkscreen: nothing over the sensor's optical window.
line(-1.2,-1.15,-.8,-1.15,k.F_SilkS,.12)
for item,y in [(fp.Reference(),-1.95),(fp.Value(),1.95)]:
    item.SetPosition(xy(0,y)); item.SetTextSize(xy(.8,.8)); item.SetTextThickness(k.FromMM(.12))
fp.Value().SetLayer(k.F_Fab)
plugin = k.PCB_IO_KICAD_SEXPR()
plugin.FootprintSave(str(a.library.resolve()),fp)
loaded = plugin.FootprintLoad(str(a.library.resolve()),name)
assert loaded is not None
rows=[]
for item in loaded.Pads():
    pos=item.GetPosition(); size=item.GetSize()
    rows.append({'number':item.GetNumber(), 'xy_mm':[k.ToMM(pos.x),k.ToMM(pos.y)],
                 'size_mm':[k.ToMM(size.x),k.ToMM(size.y)],
                 'layers':[k.LayerName(n) for n in item.GetLayerSet().Seq()]})
expected={str(n):(x,y,.5,.25) for n,x,y in [(1,-.95,-.65),(2,-.95,0),(3,-.95,.65),(4,.95,.65),(5,.95,0),(6,.95,-.65)]}
expected['7']=(0,0,.65,1.35);expected['']=(0,0,.62,1.25)
assert len(rows)==8
for row in rows:
    assert max(abs(x-y) for x,y in zip(row['xy_mm']+row['size_mm'],expected[row['number']]))<1e-9
    assert ('F.Cu' in row['layers']) == (row['number']!='')
    assert ('F.Paste' in row['layers']) == (row['number']!='7')
path=a.library/(name+'.kicad_mod')
report={'status':'PASS_LAND_PATTERN_GEOMETRY_SCOPE_ONLY','kicad_version':k.GetBuildVersion(),
        'source':'https://www.ti.com/lit/ds/symlink/opt3004.pdf',
        'drawing':'4221434/C 01/2018, DNP0006A', 'pads':rows,
        'EP_paste_coverage_percent':100*(.62*1.25)/(.65*1.35),
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'design_seeds':{'mask_expansion_mm':.05,'courtyard_half_width_mm':1.45,'courtyard_half_height_mm':1.3},
        'open':['Stencil thickness/process qualification; TI example 125 micrometres.',
                'Thermal via implementation/filled-tented process: TI example diameter 0.2 at (0,+/-0.4); no vias embedded in footprint.',
                'Optical tunnel and board placement; complete PCB DRC and assembly verification.']}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
