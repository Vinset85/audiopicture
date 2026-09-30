# AudioPicture V2.2 frame-aware vent candidate Rev.BI
# Candidate replacing Rev.AD/Rev.V only after full master B-rep gate.
import math,json
R=1.5
lowerL=[("V",17,20,14,54),("V",24,27,14,54),("V",17,20,62,102),("V",24,27,62,102),("V",17,20,110,150),("V",24,27,110,150)]
upperL=[("H",17,62,315,318),("H",17,62,322,325),("H",17,62,329,332),("H",17,62,336,339),("H",17,62,343,346)]
def mirror(c):
 o,x0,x1,y0,y1=c;return(o,320-x1,320-x0,y0,y1)
lowerR=[mirror(c) for c in lowerL];upperR=[mirror(c) for c in upperL]
ain=(40-3)*3+math.pi*R*R;aout=(45-3)*3+math.pi*R*R
print(json.dumps({"lower_left":lowerL,"lower_right":lowerR,"upper_left":upperL,"upper_right":upperR,
"real_area_mm2":{"inlet":12*ain,"outlet":10*aout},
"effective_seed_mm2":{"inlet_at_0p75":12*ain*.75,"outlet_at_0p80":10*aout*.80},
"validated_before_source_creation":["lower Rev.BH: projected-frame clear and >=4mm web","upper: projected-frame clear at 1mm seed; MAIN-C and coarse ESP32 mask clear at 2mm screen"],
"open":["exact 3D shell master boolean","retention-seat and edge-return interaction","exact RF/radar","CFD"]},indent=2))
