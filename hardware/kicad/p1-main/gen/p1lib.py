"""Writes the project library AudioPicture_P1 (symbols + footprints) for parts KiCad does not ship.

Ag53024  : Silvertel Ag53000 family datasheet V1.1 (2026-06-22), Fig. 12 package, Fig. 13 land pattern.
PT61020EL: Bourns PT61020EL datasheet REV. 03/20, product dimensions and recommended layout.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "lib")
UUID0 = "a9e0c3a2-0000-4000-8000-"


def _pin(num, name, typ, x, y, ang, length=2.54):
    return (f'\t\t\t(pin {typ} line (at {x:.2f} {y:.2f} {ang}) (length {length})\n'
            f'\t\t\t\t(name "{name}" (effects (font (size 1.27 1.27))))\n'
            f'\t\t\t\t(number "{num}" (effects (font (size 1.27 1.27)))))\n')


def _symbol(name, ref, value, fp, ds, desc, w, h, left, right):
    """left/right: lists of (num, name, type) from top to bottom; None leaves a gap."""
    s = (f'\t(symbol "{name}" (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
         f'\t\t(property "Reference" "{ref}" (at 0 {h / 2 + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))\n'
         f'\t\t(property "Value" "{value}" (at 0 {-h / 2 - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))\n'
         f'\t\t(property "Footprint" "{fp}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
         f'\t\t(property "Datasheet" "{ds}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
         f'\t\t(property "Description" "{desc}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
         f'\t\t(symbol "{name}_0_1"\n'
         f'\t\t\t(rectangle (start {-w / 2:.2f} {h / 2:.2f}) (end {w / 2:.2f} {-h / 2:.2f})\n'
         f'\t\t\t\t(stroke (width 0.254) (type default)) (fill (type background))))\n'
         f'\t\t(symbol "{name}_1_1"\n')
    for side, pins, x, ang in (("L", left, -w / 2 - 2.54, 0), ("R", right, w / 2 + 2.54, 180)):
        y = h / 2 - 2.54
        for p in pins:
            if p is not None:
                s += _pin(p[0], p[1], p[2], x, y, ang)
            y -= 2.54
    s += '\t\t)\n\t)\n'
    return s


def symbols():
    ag = _symbol("Ag53024", "U", "Ag53024", "AudioPicture_P1:Silvertel_Ag53000_SIL10",
                 "https://silvertel.com/images/datasheets/Ag53000-Datasheet.pdf",
                 "IEEE 802.3at PoE+ PD module, 24 V 25.5 W, 1500 V isolation",
                 15.24, 17.78,
                 [("1", "VIN+", "power_in"), ("2", "VIN-", "power_in"), None, ("3", "NC3", "no_connect"),
                  ("4", "NC4", "no_connect"), ("5", "NC5", "no_connect"), ("6", "NC6", "no_connect")],
                 [("8", "VOUT+", "power_out"), ("9", "ADJ", "passive"), None, None,
                  ("7", "VOUT-", "passive"), ("10", "VOUT-", "passive")])
    pt = _symbol("PT61020EL", "T", "PT61020EL", "AudioPicture_P1:Bourns_PT61020EL_SMD24",
                 "https://www.bourns.com/docs/product-datasheets/pt61020el.pdf",
                 "4-pair 1CT:1 LAN transformer, PoE+ 650 mA, 1500 Vac", 15.24, 33.02,
                 [("1", "TCT1", "passive"), ("2", "TD1+", "passive"), ("3", "TD1-", "passive"),
                  ("4", "TCT2", "passive"), ("5", "TD2+", "passive"), ("6", "TD2-", "passive"),
                  ("7", "TCT3", "passive"), ("8", "TD3+", "passive"), ("9", "TD3-", "passive"),
                  ("10", "TCT4", "passive"), ("11", "TD4+", "passive"), ("12", "TD4-", "passive")],
                 [("24", "MCT1", "passive"), ("23", "MX1+", "passive"), ("22", "MX1-", "passive"),
                  ("21", "MCT2", "passive"), ("20", "MX2+", "passive"), ("19", "MX2-", "passive"),
                  ("18", "MCT3", "passive"), ("17", "MX3+", "passive"), ("16", "MX3-", "passive"),
                  ("15", "MCT4", "passive"), ("14", "MX4+", "passive"), ("13", "MX4-", "passive")])
    return ('(kicad_symbol_lib (version 20241209) (generator "audiopicture_p1lib") (generator_version "1.0")\n'
            + ag + pt + ')\n')


def _line(layer, x0, y0, x1, y1, w):
    return f'\t(fp_line (start {x0:.3f} {y0:.3f}) (end {x1:.3f} {y1:.3f}) (stroke (width {w}) (type solid)) (layer "{layer}"))\n'


def _rect(layer, x0, y0, x1, y1, w):
    return (_line(layer, x0, y0, x1, y0, w) + _line(layer, x1, y0, x1, y1, w)
            + _line(layer, x1, y1, x0, y1, w) + _line(layer, x0, y1, x0, y0, w))


def _keepout(x0, y0, x1, y1, name):
    return (f'\t(zone (net 0) (net_name "") (layers "*.Cu") (name "{name}") (hatch edge 0.5)\n'
            f'\t\t(connect_pads (clearance 0))\n\t\t(min_thickness 0.25)\n'
            f'\t\t(keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed))\n'
            f'\t\t(fill (thermal_gap 0.5) (thermal_bridge_width 0.5))\n'
            f'\t\t(polygon (pts (xy {x0} {y0}) (xy {x1} {y0}) (xy {x1} {y1}) (xy {x0} {y1}))))\n')


def _fp_head(name, descr, tags, attr):
    return (f'(footprint "{name}" (version 20241229) (generator "audiopicture_p1lib") (generator_version "1.0")\n'
            f'\t(layer "F.Cu")\n\t(descr "{descr}")\n\t(tags "{tags}")\n'
            f'\t(property "Reference" "REF**" (at 0 -3 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
            f'\t(property "Value" "{name}" (at 0 3 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))\n'
            f'\t(attr {attr})\n')


def ag53000_fp():
    """Pin 1 at origin, pins along +x. Module components on the -y side (dimension C, max 13.0;
    pins sit ~2.9 mm from the module PCB face). Copper keep-out between the isolation barriers:
    x 13.97..34.29, y -8.46 (b) .. +6.0 (d >= 1.27 and the hatched area below the pins)."""
    xs = [i * 2.54 for i in range(6)] + [35.56, 38.10, 40.64, 43.18]
    s = _fp_head("Silvertel_Ag53000_SIL10", "Silvertel Ag53000 PoE PD module, SIL 10 pins, 2.54 mm, hole 1.12 (datasheet Fig. 13)",
                 "PoE PD Ag53024 Ag53012", "through_hole")
    for i, x in enumerate(xs):
        shape = "rect" if i == 0 else "circle"
        s += (f'\t(pad "{i + 1}" thru_hole {shape} (at {x:.2f} 0) (size 1.8 1.8) (drill 1.12) '
              f'(layers "*.Cu" "*.Mask") (remove_unused_layers no))\n')
    x0, x1 = -5.36, -5.36 + 58.28
    s += _rect("F.Fab", -5.11, -10.14, -5.11 + 57.28, 2.9, 0.1)
    s += _rect("F.CrtYd", x0 - 0.25, -10.4, x1 + 0.25, 3.2, 0.05)
    s += _rect("F.SilkS", x0 - 0.1, -10.25, x1 + 0.1, 3.05, 0.12)
    s += _line("F.SilkS", 13.97, -10.25, 13.97, 3.05, 0.12) + _line("F.SilkS", 34.29, -10.25, 34.29, 3.05, 0.12)
    s += _line("Dwgs.User", 13.97, -12, 13.97, 7, 0.1) + _line("Dwgs.User", 34.29, -12, 34.29, 7, 0.1)
    s += (f'\t(fp_text user "ISOLATION BARRIER" (at 24.13 -5 0) (layer "Dwgs.User") '
          f'(effects (font (size 1 1) (thickness 0.15))))\n')
    s += _keepout(13.97, -8.46, 34.29, 6.0, "Ag53000 isolation keep-out")
    s += ')\n'
    return s


def pt61020_fp():
    """Top view, pin 1 bottom-left. Rows 1-12 (PHY side, +y) and 24-13 (line side, -y), pitch 1.27.
    Recommended layout: pads 0.76 x 1.91, row outer span 16.51 -> pad centres at +-7.30."""
    s = _fp_head("Bourns_PT61020EL_SMD24", "Bourns PT61020EL LAN transformer, 24-pin SMD, 1.27 mm (datasheet recommended layout)",
                 "LAN magnetics PoE", "smd")
    yc = 16.51 / 2 - 1.91 / 2
    for i in range(12):
        x = -6.985 + i * 1.27
        s += f'\t(pad "{i + 1}" smd rect (at {x:.3f} {yc:.3f}) (size 0.76 1.91) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
        s += f'\t(pad "{24 - i}" smd rect (at {x:.3f} {-yc:.3f}) (size 0.76 1.91) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
    s += _rect("F.Fab", -6.98, -6.1, 6.98, 6.1, 0.1)
    s += _rect("F.CrtYd", -8.85, -8.6, 8.85, 8.6, 0.05)
    s += _line("F.SilkS", -7.1, -6.2, 7.1, -6.2, 0.12) + _line("F.SilkS", -7.1, 6.2, 7.1, 6.2, 0.12)
    s += f'\t(fp_circle (center -7.8 8.0) (end -7.55 8.0) (stroke (width 0.25) (type solid)) (fill solid) (layer "F.SilkS"))\n'
    s += ')\n'
    return s


def write():
    os.makedirs(os.path.join(LIB, "AudioPicture_P1.pretty"), exist_ok=True)
    open(os.path.join(LIB, "AudioPicture_P1.kicad_sym"), "w").write(symbols())
    open(os.path.join(LIB, "AudioPicture_P1.pretty", "Silvertel_Ag53000_SIL10.kicad_mod"), "w").write(ag53000_fp())
    open(os.path.join(LIB, "AudioPicture_P1.pretty", "Bourns_PT61020EL_SMD24.kicad_mod"), "w").write(pt61020_fp())


if __name__ == "__main__":
    write()
    print("written", LIB)
