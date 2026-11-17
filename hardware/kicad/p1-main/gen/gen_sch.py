"""Generate p1-main.kicad_sch from circuit.py (label-per-pin style, one sheet, functional blocks)."""
import os
import uuid

import kilib
import circuit

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.join(HERE, "..")
kilib.LOCAL_SYM["AudioPicture_P1"] = os.path.join(PRJ, "lib", "AudioPicture_P1.kicad_sym")
kilib.LOCAL_SYM["AudioPicture_ENV"] = os.path.join(PRJ, "..", "environment", "lib", "AudioPicture_ENV.kicad_sym")

NS = uuid.UUID("6b3c2f0e-3a51-4e43-9a0f-5d0a1b7c9e21")
ROOT = str(uuid.uuid5(NS, "root"))
G = 2.54

BLOCKS = [
    ("PIN", "POWER ENTRY  DC 24 V / PoE secondary / OR-ing / USB-C / telemetry"),
    ("PRI", "PoE PRIMARY (isolated)  RJ45 line side, bridges, Bob Smith"),
    ("BUCK", "5 V BUCK  TPSM53603"),
    ("PWR", "3V3 BUCK  TPS62823"),
    ("ESP", "MCU  ESP32-S3-WROOM-1-N16R8"),
    ("ETH", "ETHERNET  W5500 + magnetics"),
    ("AMP", "AMPLIFIER  TAS5825M, LC filter, speaker connector"),
    ("UI", "PRIVACY MUTE, BUTTONS, LEDs, FLEX HEADER, RADAR"),
    ("ENV", "ENVIRONMENT ISLAND  SHT45, OPT3004"),
    ("TP", "TEST POINTS, MOUNTING, FIDUCIALS"),
]
FLAGS = ["GND", "3V3", "VBUS24", "3V3A", "LED_5V", "DC_F", "POE_VP", "POE_VN"]


def uid(*k):
    return str(uuid.uuid5(NS, "/".join(map(str, k))))


def snap(v):
    return round(round(v / G) * G, 4)


def text_len(s):
    return 1.27 * 0.8 * len(s) + 2.0


def block_of(p):
    if p["grp"]:
        return p["grp"]
    r = p["ref"]
    if r in ("J1",):
        return "PIN"
    if r in ("J2", "T1", "U2"):
        return "PRI" if r != "U2" else "PIN"
    if r in ("C21",):
        return "PIN"
    if r == "U8":
        return "ESP"
    if r == "J3":
        return "PIN"
    if r == "U10":
        return "ETH"
    if r in ("U11", "J4"):
        return "AMP"
    if r in ("SW1", "SW2", "D3", "D4", "J5", "J6"):
        return "UI"
    if r in ("U14", "U15"):
        return "ENV"
    return "TP"


def sym_bbox(lib_id, pins_used):
    pins = kilib.pins(lib_id)
    if not pins:
        return (-2.54, -2.54, 2.54, 2.54), 0, 0
    xs = [p[3] for p in pins]; ys = [p[4] for p in pins]
    lmax = rmax = 0.0
    for p in pins:
        n = pins_used.get(p[0], "")
        L = text_len(n) if n else 2.0
        if p[5] == 0:
            lmax = max(lmax, L)
        elif p[5] == 180:
            rmax = max(rmax, L)
    vy = max([text_len(pins_used.get(p[0], "")) for p in pins if p[5] in (90, 270)] + [0])
    return (min(xs) - lmax, min(ys) - vy - 2.54, max(xs) + rmax, max(ys) + vy + 2.54), lmax, rmax


def label(net, x, y, pin_ang):
    ang = {0: 180, 180: 0, 90: 270, 270: 90}[int(pin_ang) % 360]
    just = {0: "left", 180: "right", 90: "left", 270: "right"}[ang]
    return (f'\t(global_label "{net}" (shape passive) (at {x:.2f} {y:.2f} {ang}) (fields_autoplaced yes)\n'
            f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))\n'
            f'\t\t(uuid "{uid("lbl", net, x, y)}")\n'
            f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes))))\n')


def instance(p, x, y):
    lib = p["sym"]
    ds = kilib.prop(lib, "Datasheet") or "~"
    props = [("Reference", p["ref"], 0, -3.81, False), ("Value", p["value"], 0, 3.81, False),
             ("Footprint", p["fp"], 0, 0, True), ("Datasheet", ds, 0, 0, True), ("MPN", p["mpn"], 0, 0, True)]
    if p["note"]:
        props.append(("Note", p["note"], 0, 0, True))
    s = (f'\t(symbol (lib_id "{lib}") (at {x:.2f} {y:.2f} 0) (unit 1) (exclude_from_sim no) (in_bom {"no" if p["ref"].startswith(("H", "FID", "TP")) else "yes"}) '
         f'(on_board yes) (dnp {"yes" if p["dnp"] else "no"}) (uuid "{uid("sym", p["ref"])}")\n')
    for k, v, dx, dy, hid in props:
        v = str(v).replace('"', "'")
        s += (f'\t\t(property "{k}" "{v}" (at {x + dx:.2f} {y + dy:.2f} 0) '
              f'(effects (font (size 1.27 1.27)){" (hide yes)" if hid else ""}))\n')
    for pin in kilib.pins(lib):
        s += f'\t\t(pin "{pin[0]}" (uuid "{uid("pin", p["ref"], pin[0], pin[3], pin[4])}"))\n'
    s += (f'\t\t(instances (project "p1-main" (path "/{ROOT}" (reference "{p["ref"]}") (unit 1))))\n\t)\n')
    return s


def build():
    libs, body = {}, []
    y0 = 20.0
    xmax_all = 0.0
    for key, title in BLOCKS:
        members = [p for p in circuit.PARTS.values() if block_of(p) == key]
        if not members:
            continue
        body.append(f'\t(text "{title}" (exclude_from_sim no) (at 15.24 {y0:.2f} 0) '
                    f'(effects (font (size 2.54 2.54) (bold yes)) (justify left bottom)) (uuid "{uid("t", key)}"))\n')
        x, y, rowh = 15.24, y0 + 8.0, 0.0
        for p in members:
            libs[p["sym"]] = True
            (bx0, by0, bx1, by1), _, _ = sym_bbox(p["sym"], p["pins"])
            w, h = bx1 - bx0 + 5.08, by1 - by0 + 5.08
            if x + w > 560.0:
                x, y, rowh = 15.24, y + rowh, 0.0
            sx, sy = snap(x - bx0), snap(y + by1)
            body.append(instance(p, sx, sy))
            for pin in kilib.pins(p["sym"]):
                px, py = round(sx + pin[3], 2), round(sy - pin[4], 2)
                net = p["pins"].get(pin[0])
                if net:
                    body.append(label(net, px, py, pin[5]))
                elif pin[2] != "no_connect" or True:
                    body.append(f'\t(no_connect (at {px:.2f} {py:.2f}) (uuid "{uid("nc", p["ref"], pin[0], px, py)}"))\n')
            x += w
            rowh = max(rowh, h)
            xmax_all = max(xmax_all, x)
        y0 = y + rowh + 10.0
    # power flags
    libs["power:PWR_FLAG"] = True
    x = 15.24
    body.append(f'\t(text "PWR_FLAG" (exclude_from_sim no) (at 15.24 {y0:.2f} 0) (effects (font (size 2.54 2.54) (bold yes)) '
                f'(justify left bottom)) (uuid "{uid("t", "flags")}"))\n')
    for i, n in enumerate(FLAGS):
        fx, fy = snap(x + 10 + i * 25.4), snap(y0 + 12)
        body.append(f'\t(symbol (lib_id "power:PWR_FLAG") (at {fx:.2f} {fy:.2f} 0) (unit 1) (exclude_from_sim no) (in_bom yes) '
                    f'(on_board yes) (dnp no) (uuid "{uid("flag", n)}")\n'
                    f'\t\t(property "Reference" "#FLG{i + 1:02d}" (at {fx:.2f} {fy - 3.81:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
                    f'\t\t(property "Value" "PWR_FLAG" (at {fx:.2f} {fy - 3.81:.2f} 0) (effects (font (size 1.27 1.27))))\n'
                    f'\t\t(property "Footprint" "" (at {fx:.2f} {fy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
                    f'\t\t(property "Datasheet" "~" (at {fx:.2f} {fy:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
                    f'\t\t(pin "1" (uuid "{uid("flagpin", n)}"))\n'
                    f'\t\t(instances (project "p1-main" (path "/{ROOT}" (reference "#FLG{i + 1:02d}") (unit 1))))\n\t)\n')
        body.append(label(n, fx, fy, 90))
    y0 += 30
    W = max(841.0, xmax_all + 20); H = max(594.0, y0 + 20)
    libtxt = "".join("\t\t" + kilib.dump(kilib.symbol(l), 2) + "\n" for l in sorted(libs))
    head = (f'(kicad_sch (version 20250114) (generator "audiopicture_gen_sch") (generator_version "1.0")\n'
            f'\t(uuid "{ROOT}")\n\t(paper "User" {W:.0f} {H:.0f})\n'
            f'\t(title_block (title "AudioPicture P1 MAIN") (date "2026-10-23") (rev "P1.0") (company "Cinetyk")\n'
            f'\t\t(comment 1 "Generated from hardware/kicad/p1-main/gen/circuit.py - do not edit by hand"))\n'
            f'\t(lib_symbols\n{libtxt}\t)\n')
    tail = (f'\t(sheet_instances (path "/" (page "1")))\n)\n')
    out = os.path.join(PRJ, "p1-main.kicad_sch")
    open(out, "w").write(head + "".join(body) + tail)
    return out, W, H


if __name__ == "__main__":
    print(build())
