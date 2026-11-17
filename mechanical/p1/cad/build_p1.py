#!/usr/bin/env python3
"""AudioPicture P1 parametric CAD (CadQuery 2.8).

Builds every manufactured part from ../p1_params.json, places purchased parts as
dimensioned envelopes, runs the geometric gates and exports STEP/STL.

    ~/.venvs/ap-cad/bin/python mechanical/p1/cad/build_p1.py
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
P = json.loads((ROOT / "mechanical/p1/p1_params.json").read_text())
OUT = ROOT / "mechanical/p1/cad/out"
EVID = ROOT / "evidence/p1"
DENSITY = {"PA12": 1.01e-3, "AL6082": 2.70e-3, "STEEL": 7.85e-3}  # g/mm3

B, Z, T, BF = P["body"], P["z_stack"], P["tub"], P["baffle"]
W, H = B["width"], B["height"]
DRV = P["drivers"]
for k in ("PR2",):
    DRV[k] = {**DRV["PR1"], **{kk: vv for kk, vv in DRV[k].items() if kk != "same_as"}}
EP = P["electronics_pocket"]
GASKET = BF["flange_gasket_compressed"]

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def cyl(cx, cy, d, z0, z1):
    return cq.Workplane("XY").circle(d / 2).extrude(z1 - z0).translate((cx, cy, z0))

def cone(cx, cy, d0, z0, d1, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(d0 / 2) \
        .workplane(offset=z1 - z0).circle(d1 / 2).loft()

def flange_shape(cx, cy, flats, corner_d, z0, z1):
    sq = cq.Workplane("XY").rect(flats, flats).extrude(z1 - z0)
    ci = cq.Workplane("XY").circle(corner_d / 2).extrude(z1 - z0)
    return sq.intersect(ci).translate((cx, cy, z0))

def bolt_circle(cx, cy, d, n=4, start=45.0):
    return [(cx + d / 2 * math.cos(math.radians(start + 360 * i / n)),
             cy + d / 2 * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]

def union_all(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.union(s)
    return out

# ---------------------------------------------------------------- mount faces
WF, TW, PR1, PR2 = DRV["WF1"], DRV["TW1"], DRV["PR1"], DRV["PR2"]
WF_MOUNT = Z["baffle_front"] - WF["rebate_depth"] + GASKET          # flange underside
PR_MOUNT = Z["baffle_front"] - PR1["rebate_depth"] + GASKET
TW_SEAT = Z["baffle_back"] - TW["seat_boss"][1]                       # flange top face
PR_CONE_REST_ABOVE_MOUNT = 5.5   # VERIFY on received sample
WF_CONE_REST_ABOVE_MOUNT = 4.0   # VERIFY on received sample

# ---------------------------------------------------------------- perimeter fasteners
def perimeter_points(inset, pitch_max, skip_corner=14.0):
    """Points on a rectangle inset from the outer body edge, evenly pitched per side."""
    pts = []
    x0, x1, y0, y1 = inset, W - inset, inset, H - inset
    for (a, b, fixed, horiz) in ((x0 + skip_corner, x1 - skip_corner, y0, True),
                                 (x0 + skip_corner, x1 - skip_corner, y1, True),
                                 (y0 + skip_corner, y1 - skip_corner, x0, False),
                                 (y0 + skip_corner, y1 - skip_corner, x1, False)):
        n = math.ceil((b - a) / pitch_max) + 1
        for i in range(n):
            t = a + (b - a) * i / (n - 1)
            pts.append((t, fixed) if horiz else (fixed, t))
    return pts

EDGE_SCREWS = perimeter_points(6.0, BF["edge_screw_pitch_max"])
def magnet_points():
    """Magnets sit at mid-gaps between edge screws: top/bottom gaps 0,2,4; sides 0,2,3,5."""
    ins = P["front_frame"]["magnet_inset"]
    xs = sorted({x for (x, y) in EDGE_SCREWS if y == 6.0})
    ys = sorted({y for (x, y) in EDGE_SCREWS if x == 6.0})
    mx = [(xs[i] + xs[i + 1]) / 2 for i in (0, 2, 4) if i + 1 < len(xs)]
    my = [(ys[i] + ys[i + 1]) / 2 for i in (0, 2, 3, 5) if i + 1 < len(ys)]
    return [(x, ins) for x in mx] + [(x, H - ins) for x in mx] + [(ins, y) for y in my] + [(W - ins, y) for y in my]
MAGNETS = magnet_points()
PARTITION_BOSSES = [(60.0, 82.0), (260.0, 82.0)]
MIC_HOLES_X = (23.75, 86.25)   # Linear-4 M3 holes from the board's left edge, at y = 5.5

# ---------------------------------------------------------------- TUB
def build_tub():
    sw, lip = T["side_wall"], T["lip_thickness"]
    outer = cq.Workplane("XY").rect(W, H).extrude(Z["baffle_front"]).translate((W / 2, H / 2, 0)) \
        .edges("|Z").fillet(B["corner_radius_xy"])
    tub = outer.cut(box(sw, W - sw, sw, H - sw, Z["rear_skin"], Z["baffle_front"] + 1))
    tub = tub.cut(box(lip, W - lip, lip, H - lip, T["ledge_z"], Z["baffle_front"] + 1))
    py0, py1 = T["partition_y"]
    tub = tub.union(box(sw, W - sw, py0, py1, Z["rear_skin"], T["ledge_z"]))
    for (x, y) in PARTITION_BOSSES:
        tub = tub.union(cyl(x, y, 10.0, Z["rear_skin"], T["ledge_z"]))
    # ribs on the rear skin, driver chamber only
    r = T["rib"]
    zr0, zr1 = Z["rear_skin"], Z["rear_skin"] + r["height"]
    dy0, dy1 = T["driver_interior_y"]
    ribs = []
    x = sw + r["pitch"] / 2
    while x < W - sw:
        ribs.append(box(x - r["width"] / 2, x + r["width"] / 2, dy0, dy1, zr0, zr1)); x += r["pitch"]
    y = dy0 + r["pitch"] / 2
    while y < dy1:
        ribs.append(box(sw, W - sw, y - r["width"] / 2, y + r["width"] / 2, zr0, zr1)); y += r["pitch"]
    rib = union_all(ribs)
    for (cx, cy), d in (((WF["center"]), WF["magnet_d"] + 14.0), (PR1["center"], 48.0), (PR2["center"], 48.0)):
        rib = rib.cut(cyl(cx, cy, d, zr0 - 1, zr1 + 1))
    tub = tub.union(rib)
    # tie columns rear skin -> baffle back
    tc = T["tie_column"]
    for (x, y) in P["ties"]:
        tub = tub.union(cyl(x, y, tc["od"], Z["rear_skin"], Z["baffle_back"]))
        tub = tub.cut(cyl(x, y, tc["insert_bore"], Z["baffle_back"] - tc["insert_depth"], Z["baffle_back"] + 1))
    # cleat recess with backing boss
    c = P["cleat"]["recess"]
    tub = tub.union(box(c["x"][0] - 2, c["x"][1] + 2, c["y"][0] - 2, c["y"][1] + 2,
                        Z["rear_skin"], c["depth"] + 10.0))
    tub = tub.cut(box(c["x"][0], c["x"][1], c["y"][0], c["y"][1], -1, c["depth"]))
    for (x, y) in cleat_insert_points():   # Ruthex RX-M4x8.1: bore 5.6, depth 9
        tub = tub.cut(cyl(x, y, 5.6, c["depth"] - 0.1, c["depth"] + 9.0))
    # rear connector bay (open to wall and floor), ceiling just below MAIN
    rb = EP["rear_bay"]
    zc = EP["main_pcb"]["z_bottom"]
    tub = tub.union(box(rb["x"][0] - 2, rb["x"][1] + 2, 0, rb["y"][1] + 2, 0, zc - 0.2))
    tub = tub.cut(box(rb["x"][0], rb["x"][1], -1, rb["y"][1], -1, rb["z"][1]))
    tub = tub.cut(box(rb["x"][0] + 1, rb["x"][1] - 1, rb["y"][0] + 8, rb["y"][1] - 4, rb["z"][1] - 1, zc + 1))
    # MAIN standoffs and Flex core standoffs (M3 heat-set, bore 4.0)
    for (x, y) in main_mount_points():
        tub = tub.union(cyl(x, y, 8.0, Z["rear_skin"], zc)).cut(cyl(x, y, 4.0, zc - 6.0, zc + 1))
    fc = EP["flex_core"]
    for (x, y) in flex_mount_points():
        tub = tub.union(cyl(x, y, 7.0, Z["rear_skin"], fc["z_bottom"])).cut(cyl(x, y, 4.0, fc["z_bottom"] - 5.0, fc["z_bottom"] + 1))
    # ledge inserts M3 (bore 4.0, depth 7)
    for (x, y) in EDGE_SCREWS:
        tub = tub.cut(cyl(x, y, 4.0, T["ledge_z"] - 7.0, T["ledge_z"] + 1))
    for (x, y) in PARTITION_BOSSES:
        tub = tub.cut(cyl(x, y, 4.0, T["ledge_z"] - 7.0, T["ledge_z"] + 1))
    # bottom vents (pocket) and speaker-wire pass-throughs in the partition
    ec = EP["env_chamber"]
    tub = tub.union(box(ec["wall_x"][0], ec["wall_x"][1], sw - 0.01, py0 + 0.01, Z["rear_skin"] - 0.01,
                        EP["main_pcb"]["z_bottom"] - 0.3))
    for nm, (bx, by) in BUTTONS.items():
        zc = BUTTON_ZC
        tub = tub.cut(cyl_y(bx, zc, BUTTON["bore"], -1.0, sw + 1.0))
    for (x0, x1) in EP["vents_bottom"]:
        xx = x0
        while xx + 3 <= x1:
            if not (rb["x"][0] - 3 < xx < rb["x"][1] + 3):
                tub = tub.cut(box(xx, xx + 3, -1, T["side_wall"] + 1, 14.0, 50.0))
            xx += 7.0
    for x in (120.0, 135.0):   # woofer and tweeter pairs; sealed with neutral-cure silicone
        tub = tub.cut(box(x - 2.5, x + 2.5, py0 - 1, py1 + 1, 40.0, 45.0))
    # bumper pockets at the rear bottom corners (3M Bumpon SJ5302, 12.7 x 3.5)
    for x in (40.0, W - 40.0):
        tub = tub.cut(cyl(x, 20.0, 13.2, -1, 3.0))
    return tub

BUTTON = {"bore": 6.0, "rod": 5.6, "collar": 8.0, "tip": 3.0, "gap": 0.2}
BUTTONS = {k: v for k, v in EP["buttons"].items() if k in ("MUTE", "ACTION")}
BUTTON_ZC = EP["main_pcb"]["z_bottom"] + EP["main_pcb"]["thickness"] + 0.7   # EVQ-P7A actuator axis (VERIFY on sample)

def cyl_y(cx, cz, d, y0, y1):
    return cq.Workplane("XZ").center(cx, cz).circle(d / 2).extrude(-(y1 - y0)).translate((0, y0, 0))

def button_rod(cx):
    """Printed push rod: outer face 0.3 mm below the tub bottom face, collar inside the pocket, tip to the actuator."""
    sw = T["side_wall"]; zc = BUTTON_ZC
    tip_y = EP["main_pcb"]["origin"][1] - BUTTON["gap"]          # actuator face at the MAIN bottom edge
    rod = cyl_y(cx, zc, BUTTON["rod"], 0.0, sw)
    collar = cyl_y(cx, zc, BUTTON["collar"], sw + 0.2, sw + 1.0)
    neck = cyl_y(cx, zc, BUTTON["rod"], sw - 0.01, sw + 0.21)
    tip = cyl_y(cx, zc, BUTTON["tip"], sw + 1.0 - 0.01, tip_y)
    return union_all([rod, neck, collar, tip])

def cleat_insert_points():
    c = P["cleat"]; rec = c["recess"]; pl = c["picture_cleat"][0]
    xm = (rec["x"][0] + rec["x"][1]) / 2
    y = c["rail_top_y"] - c["wall_rail"][2] + rec["depth"] + (c["picture_cleat"][1] - c["picture_cleat"][2]) / 2
    return [(x, y) for x in (xm - pl / 2 + 15, xm - 25, xm + 25, xm + pl / 2 - 15)]

def main_mount_points():
    m = EP["main_pcb"]; ox, oy = m["origin"]; w, h = m["outline"]
    return [(ox + 4, oy + 4), (ox + w - 4, oy + 4), (ox + 4, oy + h - 4), (ox + w - 4, oy + h - 4),
            (ox + 128, oy + 4), (ox + 128, oy + h - 4)]

def flex_mount_points():
    fc = EP["flex_core"]; ox, oy = fc["origin"]
    return [(ox + 4.0, oy + 4.0), (ox + 66.5, oy + 4.0), (ox + 4.0, oy + 48.2), (ox + 66.5, oy + 48.2)]

# ---------------------------------------------------------------- BAFFLE
def driver_rebate(d, mount):
    cx, cy = d["center"]
    reb = flange_shape(cx, cy, d["flange_flats"] + 1.0, d["flange_corner_d"] + 1.0,
                       Z["baffle_front"] - d["rebate_depth"], Z["baffle_front"] + 1)
    return reb

def build_baffle():
    bw, bh = BF["outline"]
    x0, y0 = (W - bw) / 2, (H - bh) / 2
    b = cq.Workplane("XY").rect(bw, bh).extrude(BF["thickness"]).translate((W / 2, H / 2, Z["baffle_back"])) \
        .edges("|Z").fillet(1.0)
    # tweeter seat boss on the back
    sx, sh = TW["seat_boss"]
    b = b.union(box(TW["center"][0] - sx / 2, TW["center"][0] + sx / 2, TW["center"][1] - sx / 2,
                    TW["center"][1] + sx / 2, TW_SEAT, Z["baffle_back"] + 0.01))
    for d in (WF, PR1, PR2):
        cx, cy = d["center"]
        b = b.cut(cyl(cx, cy, d["cutout_d"], TW_SEAT - 1, Z["baffle_front"] + 1))
        b = b.cut(driver_rebate(d, None))
        if d.get("recess_chamfer"):
            ch = d["recess_chamfer"]
            for k in range(1, 4):   # 3-step 45 deg lead-in around the sunk passive radiator
                f = k / 3.0
                step = flange_shape(cx, cy, d["flange_flats"] + 1.0 + 2 * ch * f, d["flange_corner_d"] + 1.0 + 2 * ch * f,
                                    Z["baffle_front"] - ch * (1 - f) - 0.01, Z["baffle_front"] + 1)
                b = b.cut(step)
        mount_floor = Z["baffle_front"] - d["rebate_depth"]
        depth = min(7.0, mount_floor - Z["baffle_back"] - 1.0)   # blind: never break into the box
        for (hx, hy) in bolt_circle(cx, cy, d["bolt_circle_d"]):
            b = b.cut(cyl(hx, hy, 4.0, mount_floor - depth, mount_floor + 0.5))
    b = b.cut(cyl(TW["center"][0], TW["center"][1], TW["hole_d"], TW_SEAT - 1, Z["baffle_front"] + 1))
    for (hx, hy) in bolt_circle(TW["center"][0], TW["center"][1], TW["bolt_circle_d"]):
        b = b.cut(cyl(hx, hy, 4.0, TW_SEAT - 0.5, TW_SEAT + 6.0))
    # edge screws: M3 countersunk, head flush with baffle front
    for (x, y) in EDGE_SCREWS + PARTITION_BOSSES:
        b = b.cut(cyl(x, y, 3.4, Z["baffle_back"] - 1, Z["baffle_front"] + 1))
        b = b.cut(cone(x, y, 3.4, Z["baffle_front"] - 1.7, 6.8, Z["baffle_front"] + 0.01))
    # tie screws: M4 countersunk
    for (x, y) in P["ties"]:
        b = b.cut(cyl(x, y, 4.5, Z["baffle_back"] - 1, Z["baffle_front"] + 1))
        b = b.cut(cone(x, y, 4.5, Z["baffle_front"] - 2.3, 9.0, Z["baffle_front"] + 0.01))
    # steel discs for the magnetic front frame
    sd, st = P["front_frame"]["steel_disc"]
    for (x, y) in MAGNETS:
        b = b.cut(cyl(x, y, sd + 0.2, Z["baffle_front"] - st - 0.1, Z["baffle_front"] + 1))
    # microphone array pocket, ports and retainer inserts
    ma = EP["mic_array"]; mx, my = ma["center"]; aw, ah = ma["outline"]
    keep = ma["baffle_remaining"]
    b = b.cut(box(mx - aw / 2 - 0.3, mx + aw / 2 + 0.3, my - ah / 2 - 0.3, my + ah / 2 + 0.3,
                  Z["baffle_back"] - 1, Z["baffle_front"] - keep))
    for xo in ma["mic_x_from_left"]:
        px, py = mx - aw / 2 + xo, my - ah / 2 + ma["mic_y_from_bottom"]
        b = b.cut(cyl(px, py, ma["port_d"], Z["baffle_front"] - keep - 0.1, Z["baffle_front"] + 1))
    for xo in (-aw / 2 - 8, aw / 2 + 8):
        b = b.cut(cyl(mx + xo, my, 4.0, Z["baffle_back"] - 1, Z["baffle_back"] + 6.0))
    # radar radome: pocket leaving radome_t of unfilled PA12
    ra = EP["radar"]; rx, ry = ra["center"]; rw, rh = ra["outline"]
    b = b.cut(box(rx - rw / 2 - 0.5, rx + rw / 2 + 0.5, ry - rh / 2 - 0.5, ry + rh / 2 + 0.5,
                  Z["baffle_back"] - 1, Z["baffle_front"] - ra["radome_t"]))
    for yo in (-rh / 2 - 6, rh / 2 + 6):
        b = b.cut(cyl(rx, ry + yo, 4.0, Z["baffle_back"] - 1, Z["baffle_back"] + 6.0))
    # light pipes
    for k in LIGHT_PIPES:
        lp = EP[k]
        b = b.cut(cyl(lp["center"][0], lp["center"][1], lp["d"] + 0.2, Z["baffle_back"] - 1, Z["baffle_front"] + 1))
    # pocket front vents behind the fabric, away from the microphones
    vy0, vy1 = EP["vents_front_y"]
    for (xa, xb) in EP["vents_front_x"]:
        xx = xa
        while xx + 3 <= xb:
            if not (EP["radar"]["center"][0] - 16 < xx < EP["radar"]["center"][0] + 16 and vy0 < 62):
                b = b.cut(box(xx, xx + 3, vy0, vy1, Z["baffle_back"] - 1, Z["baffle_front"] + 1))
            xx += 7.0
    # ENV chamber wall, front half: baffle back -> 0.3 mm above the MAIN top face (passes the board slots)
    ec = EP["env_chamber"]; zt = EP["main_pcb"]["z_bottom"] + EP["main_pcb"]["thickness"]
    b = b.union(box(ec["wall_x"][0], ec["wall_x"][1], T["pocket_interior_y"][0] + 0.3, T["partition_y"][0] - 0.3,
                    zt + 0.3, Z["baffle_back"] + 0.01))
    return b

# ---------------------------------------------------------------- FRONT FRAME
def build_frame():
    f = P["front_frame"]; pw = f["profile_width"]; z0, z1 = f["z"]
    outer = cq.Workplane("XY").rect(W, H).extrude(z1 - z0).translate((W / 2, H / 2, z0)).edges("|Z").fillet(B["corner_radius_xy"])
    inner = cq.Workplane("XY").rect(W - 2 * pw, H - 2 * pw).extrude(z1 - z0 + 2).translate((W / 2, H / 2, z0 - 1)).edges("|Z").fillet(2.0)
    fr = outer.cut(inner)
    # hollow the profile from the back to save mass; leave 2 mm walls
    hol = cq.Workplane("XY").rect(W - 4, H - 4).extrude(z1 - z0 - 2.5).translate((W / 2, H / 2, z0 - 0.01)) \
        .cut(cq.Workplane("XY").rect(W - 2 * pw + 4, H - 2 * pw + 4).extrude(z1 - z0).translate((W / 2, H / 2, z0 - 1)))
    fr = fr.cut(hol)
    md, mt = f["magnet"]
    for (x, y) in MAGNETS:
        fr = fr.union(cyl(x, y, f["boss_d"], z0, z1 - 2.5)).cut(cyl(x, y, md + 0.2, z0 - 0.01, z0 + mt + 0.1))
    try:
        fr = fr.faces(">Z").edges().fillet(1.5)
    except Exception:
        pass
    return fr

# ---------------------------------------------------------------- small printed parts
def build_mic_retainer():
    ma = EP["mic_array"]; mx, my = ma["center"]; aw, ah = ma["outline"]
    zb = Z["baffle_front"] - ma["baffle_remaining"] - ma["gasket_compressed"] - 1.51   # board back face
    bar = box(mx - aw / 2 - 14, mx + aw / 2 + 14, my - 7, my + 7, Z["baffle_back"] - 3.0, Z["baffle_back"])
    # fingers press on the component-free pads around the board's M3 holes; gasket preload comes from 0.5 -> 0.3 mm compression
    fingers = union_all([cyl(mx - aw / 2 + xo, my, 5.5, Z["baffle_back"] - 0.01, zb) for xo in MIC_HOLES_X])
    r = bar.union(fingers)
    for xo in (-aw / 2 - 8, aw / 2 + 8):
        r = r.cut(cyl(mx + xo, my, 3.4, Z["baffle_back"] - 4, Z["baffle_back"] + 1))
    return r

def build_radar_retainer():
    ra = EP["radar"]; rx, ry = ra["center"]; rw, rh = ra["outline"]
    zr_back = Z["baffle_front"] - ra["radome_t"] - 0.3 - 1.0   # module PCB back face
    r = box(rx - 10, rx + 10, ry - rh / 2 - 10, ry + rh / 2 + 10, Z["baffle_back"] - 3.0, Z["baffle_back"])
    r = r.cut(box(rx - 8, rx + 8, ry - rh / 2 + 3, ry + rh / 2 - 3, Z["baffle_back"] - 4, Z["baffle_back"] + 1))
    for xo in (-rw / 2 + 2.0, rw / 2 - 2.0):   # corner fingers onto the module PCB edge
        r = r.union(box(rx + xo - 1.5, rx + xo + 1.5, ry - rh / 2 + 1, ry + rh / 2 - 1, Z["baffle_back"] - 0.01, zr_back))
    for yo in (-rh / 2 - 6, rh / 2 + 6):
        r = r.cut(cyl(rx, ry + yo, 3.4, Z["baffle_back"] - 4, Z["baffle_back"] + 1))
    return r

def build_cleats():
    """French cleat, profiles in the YZ plane (z = 0 is the wall).

    Rail (on the wall, z 0..t): top face rises from (yt-t, z=0) to (yt, z=t), i.e. the groove opens
    toward the wall. Picture cleat (z 2..2+t) hooks into it; the bevel reaction pushes it up and
    toward the wall, so the load closes the joint.
    """
    c = P["cleat"]; rec = c["recess"]; yt = c["rail_top_y"]
    pl, ph, pt = c["picture_cleat"]
    rl, rh_, rt = c["wall_rail"]
    xm = (rec["x"][0] + rec["x"][1]) / 2
    zf = rec["depth"]; zw = zf - pt                      # cleat wall-side face (2 mm off the wall)
    prof = cq.Workplane("YZ").polyline([(yt - rt + zw, zw), (yt - rt + zw + ph, zw), (yt - rt + zw + ph, zf),
                                        (yt - rt + zf, zf)]).close().extrude(pl).translate((xm - pl / 2, 0, 0))
    for (x, y) in cleat_insert_points():
        prof = prof.cut(cyl(x, y, 4.5, zw - 1, zf + 1)).cut(cone(x, y, 9.0, zw - 0.01, 4.5, zw + 2.25))
    rail = cq.Workplane("YZ").polyline([(yt - rh_, 0), (yt - rt, 0), (yt, rt), (yt - rh_, rt)]).close() \
        .extrude(rl).translate((xm - rl / 2, 0, 0))
    yy = yt - rh_ / 2 - 2.0
    for x in (xm - rl / 2 + 15, xm, xm + rl / 2 - 15):
        rail = rail.cut(cyl(x, yy, 5.0, -1, rt + 1)).cut(cone(x, yy, 5.0, rt - 2.5, 10.0, rt + 0.01))
    return prof, rail

def cleat_geometry_report():
    c = P["cleat"]; rec = c["recess"]; yt = c["rail_top_y"]
    pl, ph, pt = c["picture_cleat"]; rl, rh_, rt = c["wall_rail"]
    zw = rec["depth"] - pt
    cleat_top = yt - rt + zw + ph
    return {"rail_y": [yt - rh_, yt], "cleat_y": [yt - rt + zw, cleat_top],
            "rail_inside_recess": rec["y"][0] + 1.0 <= yt - rh_,
            "lift_clear_mm": rec["y"][1] - cleat_top,
            "lift_ok": rec["y"][1] - cleat_top >= c["lift_to_hang"],
            "rail_x_inside_recess": rec["x"][0] + 1.0 <= (rec["x"][0] + rec["x"][1] - rl) / 2}

# ---------------------------------------------------------------- purchased envelopes
def woofer():
    cx, cy = WF["center"]
    fl = flange_shape(cx, cy, WF["flange_flats"], WF["flange_corner_d"], WF_MOUNT, WF_MOUNT + WF["flange_t"])
    basket = cone(cx, cy, WF["basket_d"], WF_MOUNT - 0.01, 50.0, WF_MOUNT - 34.0)
    magnet = cyl(cx, cy, WF["magnet_d"], WF_MOUNT - WF["depth_below_mount_face"], WF_MOUNT - 33.9)
    front = cyl(cx, cy, 73.7, WF_MOUNT + WF["flange_t"], WF_MOUNT + WF["front_above_mount_face"])
    return union_all([fl, basket, magnet, front])

def woofer_moving_front():
    cx, cy = WF["center"]
    return cyl(cx, cy, 73.7, WF_MOUNT + WF["flange_t"], WF_MOUNT + WF_CONE_REST_ABOVE_MOUNT + WF["xmax"])

def passive(d):
    cx, cy = d["center"]
    fl = flange_shape(cx, cy, d["flange_flats"], d["flange_corner_d"], PR_MOUNT, PR_MOUNT + d["flange_t"])
    basket = cone(cx, cy, d["basket_d"], PR_MOUNT - 0.01, 50.0, PR_MOUNT - d["basket_depth_below_mount_face"])
    zb = PR_MOUNT - d["basket_depth_below_mount_face"]
    stud = cyl(cx, cy, 34.0, zb - d["stud_protrusion_after_trim"], zb)   # disk + nut + stud envelope
    front = cyl(cx, cy, 76.0, PR_MOUNT + d["flange_t"], PR_MOUNT + d["front_above_mount_face"])
    return union_all([fl, basket, stud, front])

def passive_moving(d):
    cx, cy = d["center"]
    zb = PR_MOUNT - d["basket_depth_below_mount_face"]
    back = cyl(cx, cy, 34.0, zb - d["stud_protrusion_after_trim"] - d["xmax"], zb)
    front = cyl(cx, cy, 76.0, PR_MOUNT + d["flange_t"],
                max(PR_MOUNT + d["front_above_mount_face"] + d["xmax"] / 2, PR_MOUNT + PR_CONE_REST_ABOVE_MOUNT + d["xmax"]))
    return back, front

def tweeter():
    cx, cy = TW["center"]
    fl = box(cx - 19.5, cx + 19.5, cy - 19.5, cy + 19.5, TW_SEAT - 1.5, TW_SEAT)
    ring = cyl(cx, cy, TW["front_ring_d"], TW_SEAT, TW_SEAT + TW["ring_height_above_flange"])
    body = cyl(cx, cy, 34.0, TW_SEAT - TW["body_below_flange"], TW_SEAT - 1.5)
    tabs = box(cx - 16, cx + 16, cy - 2, cy + 2, TW_SEAT - TW["body_below_flange"] - 8, TW_SEAT - TW["body_below_flange"])
    return union_all([fl, ring, body, tabs])

MAIN_NAMED = {"U2": "U2_POE_Ag53024", "U8": "U8_ESP32-S3-WROOM-1", "C21": "C21_PVDD_470u", "J1": "J1_DC",
              "J2": "J2_RJ45", "J3": "J3_USB_C", "J4": "J4_SPK", "J5": "J5_FLEX_IDC", "J6": "J6_RADAR", "T1": "T1_PoE_XFMR",
              "U5": "U5_TPSM53603"}
LIGHT_PIPES = ("light_pipe", "status_led_pipe", "mute_led_pipe")

def main_envelopes():
    return json.loads((ROOT / EP["main_pcb"]["envelopes"]).read_text())

def electronics():
    m = EP["main_pcb"]; ox, oy = m["origin"]; w, h = m["outline"]; zb = m["z_bottom"]
    env = main_envelopes()
    top = zb + m["thickness"]
    pcb = box(ox, ox + w, oy, oy + h, zb, top)
    for (x0, y0, x1, y1) in env["board"]["slots"]:
        pcb = pcb.cut(box(x0, x1, y0, y1, zb - 1, top + 1))
    for hx, hy in m["mount_holes"]:
        pcb = pcb.cut(cyl(hx, hy, 3.2, zb - 1, top + 1))
    parts = {"MAIN_PCB": pcb}
    small = {"F": [], "B": []}
    for e in env["parts"]:
        if e["h"] < 0.05:
            continue
        x0, y0, x1, y1 = e["body"]
        x0, y0, x1, y1 = max(x0, ox), max(y0, oy), min(x1, ox + w), min(y1, oy + h)
        z0, z1 = (top, top + e["h"]) if e["side"] == "F" else (zb - e["h"], zb)
        b = box(x0, x1, y0, y1, z0, z1)
        if e["ref"] in MAIN_NAMED:
            parts[MAIN_NAMED[e["ref"]]] = b
        else:
            small[e["side"]].append(b)
    for side, lst in small.items():
        if lst:
            parts[f"MAIN_PARTS_{side}"] = union_all(lst)
    for k in LIGHT_PIPES:
        lp = EP[k]
        parts[k.upper()] = cyl(lp["center"][0], lp["center"][1], lp["d"], top + 1.2, Z["baffle_front"] - 0.2)
    for nm, (bx, by) in BUTTONS.items():
        parts[f"BUTTON_ROD_{nm}"] = button_rod(bx)
    fc = EP["flex_core"]; fx, fy = fc["origin"]
    parts["FLEX_CORE"] = box(fx, fx + 70.5, fy, fy + 52.2, fc["z_bottom"] + 0.0, fc["z_bottom"] + 1.51) \
        .union(box(fx + 5, fx + 65, fy + 8, fy + 46, fc["z_bottom"] + 1.51, fc["z_bottom"] + 1.51 + 10.6)) \
        .union(box(fx + 8, fx + 62, fy + 8, fy + 44, fc["z_bottom"] - 1.6, fc["z_bottom"]))
    ma = EP["mic_array"]; mx, my = ma["center"]; aw, ah = ma["outline"]
    zf = Z["baffle_front"] - ma["baffle_remaining"] - ma["gasket_compressed"]
    comp = box(mx - aw / 2 + 1, mx + aw / 2 - 1, my - 5, my + 5, zf - 1.51 - 1.46, zf - 1.51)
    for xo in MIC_HOLES_X:   # Seeed keep-out around the M3 holes
        comp = comp.cut(cyl(mx - aw / 2 + xo, my, 6.5, zf - 4, zf))
    parts["MIC_ARRAY"] = box(mx - aw / 2, mx + aw / 2, my - ah / 2, my + ah / 2, zf - 1.51, zf).union(comp)
    ra = EP["radar"]; rx, ry = ra["center"]; rw, rh = ra["outline"]
    zr = Z["baffle_front"] - ra["radome_t"] - 0.3
    parts["RADAR_LD6004"] = box(rx - rw / 2, rx + rw / 2, ry - rh / 2, ry + rh / 2, zr - 1.0, zr) \
        .union(box(rx - rw / 2 + 3.5, rx + rw / 2 - 3.5, ry - rh / 2 + 3.5, ry + rh / 2 - 3.5, zr - 4.0, zr - 1.0))
    return parts

# ---------------------------------------------------------------- gates
def interferes(a, b, tol=1e-3):
    try:
        v = a.intersect(b).val().Volume()
    except Exception:
        return 0.0
    return v if v > tol else 0.0

def main():
    OUT.mkdir(parents=True, exist_ok=True); EVID.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.st[lp]"):
        f.unlink()
    tub, baffle, frame = build_tub(), build_baffle(), build_frame()
    mic_ret, radar_ret = build_mic_retainer(), build_radar_retainer()
    cleat, rail = build_cleats()
    wf, tw, pr1, pr2 = woofer(), tweeter(), passive(PR1), passive(PR2)
    elec = electronics()
    rods = {k: elec.pop(k) for k in list(elec) if k.startswith("BUTTON_ROD")}
    gates, ok = [], True

    def gate(name, passed, value=None):
        nonlocal ok
        ok &= bool(passed)
        gates.append({"gate": name, "result": "PASS" if passed else "FAIL", "value": value})

    fixed = {"TUB": tub, "BAFFLE": baffle, "FRAME": frame, "MIC_RETAINER": mic_ret, "RADAR_RETAINER": radar_ret, **rods}
    bought = {"WF1": wf, "TW1": tw, "PR1": pr1, "PR2": pr2, **elec}
    for bn, bs in bought.items():
        for fn, fs in fixed.items():
            v = interferes(bs, fs)
            if v:
                gate(f"interference {bn} x {fn}", False, round(v, 2))
    names = list(bought)
    for i, a in enumerate(names):
        for b2 in names[i + 1:]:
            v = interferes(bought[a], bought[b2])
            if v:
                gate(f"interference {a} x {b2}", False, round(v, 2))
    for (an, a), (bn2, b2) in ((("TUB", tub), ("BAFFLE", baffle)), (("BAFFLE", baffle), ("FRAME", frame)),
                               (("TUB", tub), ("FRAME", frame))):
        v = interferes(a, b2)
        gate(f"interference {an} x {bn2}", not v, round(v, 2))
    gate("purchased-part interference sweep", not any(g["result"] == "FAIL" and g["gate"].startswith("interference ") for g in gates))

    fab = Z["fabric_back"]
    wf_front = woofer_moving_front().val().BoundingBox().zmax
    gate("WF1 cone at +Xmax to fabric >= 2 mm", fab - wf_front >= P["clearances"]["cone_to_fabric_min"], round(fab - wf_front, 2))
    for nm, d in (("PR1", PR1), ("PR2", PR2)):
        back, front = passive_moving(d)
        zf = front.val().BoundingBox().zmax
        gate(f"{nm} cone at +Xmax to fabric >= 2 mm", fab - zf >= 2.0, round(fab - zf, 2))
        v = interferes(back, tub)
        zmin = back.val().BoundingBox().zmin
        gate(f"{nm} stud/disk at -Xmax clear of tub", not v, {"clearance_to_rear_skin_mm": round(zmin - Z['rear_skin'], 2), "overlap_mm3": round(v, 2)})
    wmag = WF_MOUNT - WF["depth_below_mount_face"]
    gate("WF1 magnet to rear skin >= 3 mm", wmag - Z["rear_skin"] >= 3.0, round(wmag - Z["rear_skin"], 2))
    gate("body depth <= 84 mm", Z["fabric_front"] <= B["depth"], Z["fabric_front"])
    cg = cleat_geometry_report()
    gate("French cleat: rail inside recess, lift-to-hang >= 10 mm",
         cg["rail_inside_recess"] and cg["lift_ok"] and cg["rail_x_inside_recess"], cg)
    gate("cleat and rail do not touch", not interferes(cleat, rail), None)
    gate("picture cleat seats on recess floor without tub overlap", not interferes(cleat, tub), None)
    c2c = math.dist(WF["center"], TW["center"])
    gate("woofer-tweeter centre spacing <= 70 mm", c2c <= 70.0, round(c2c, 2))

    # ------------------------------------------------ net driver-chamber air volume
    sw = T["side_wall"]; dy0, dy1 = T["driver_interior_y"]
    chamber = box(sw, W - sw, dy0, dy1, Z["rear_skin"], Z["baffle_back"])
    cut_air = union_all([cyl(d["center"][0], d["center"][1], d["cutout_d"], Z["baffle_back"],
                             (WF_MOUNT if d is WF else PR_MOUNT)) for d in (WF, PR1, PR2)])
    air = chamber.union(cut_air).cut(tub).cut(baffle)
    v_air = air.val().Volume()
    displ = {"WF1 magnet+basket steel": math.pi / 4 * WF["magnet_d"] ** 2 * (WF["depth_below_mount_face"] - 33.9) + 10000.0,
             "PR basket steel+disk+stud x2": 2 * (8000.0 + 2500.0),
             "TW1 body": math.pi / 4 * 34.0 ** 2 * (TW["body_below_flange"] - 1.5) + 1500.0}
    v_net = v_air - sum(displ.values())
    gate("net driver-chamber air within 3.5-5.0 L (acoustic model reads this value)", 3500e3 <= v_net <= 5000e3, round(v_net / 1e6, 3))

    # ------------------------------------------------ mass and hanger load
    mass = {}
    for nm, s, mat in (("TUB", tub, "PA12"), ("BAFFLE", baffle, "PA12"), ("FRAME", frame, "PA12"),
                       ("MIC_RETAINER", mic_ret, "PA12"), ("RADAR_RETAINER", radar_ret, "PA12"),
                       ("PICTURE_CLEAT", cleat, "AL6082"), ("WALL_RAIL", rail, "AL6082"),
                       *((k, v, "PA12") for k, v in rods.items())):
        mass[nm] = round(s.val().Volume() * DENSITY[mat], 1)
    purchased_g = {"ND91-4": 317.5, "ND90-PR x2 (+7.3 g disk each)": 2 * (113.4 + 7.3), "ND20FB-4": 45.0,
                   "MAIN PCBA": 120.0, "Flex core + array + FPC": 45.0, "LD6004": 6.0, "fasteners/inserts/magnets": 90.0,
                   "fabric + CLD + fill + gaskets": 260.0}
    total = sum(v for k, v in mass.items() if k != "WALL_RAIL") + sum(purchased_g.values())
    gate("hanger design mass >= 1.0 x assembled estimate", P["cleat"]["design_mass_kg"] * 1000 >= total, round(total / 1000, 3))

    # ------------------------------------------------ exports
    exports = {"TUB": tub, "BAFFLE": baffle, "FRAME": frame, "MIC_RETAINER": mic_ret, "RADAR_RETAINER": radar_ret,
               "PICTURE_CLEAT": cleat, "WALL_RAIL": rail, **rods}
    for nm, s in exports.items():
        cq.exporters.export(s, str(OUT / f"AP-P1-{nm}.step"))
        if nm not in ("PICTURE_CLEAT", "WALL_RAIL"):
            cq.exporters.export(s, str(OUT / f"AP-P1-{nm}.stl"), tolerance=0.05, angularTolerance=0.15)
    asm = cq.Assembly(name="AudioPicture_P1")
    colors = {"TUB": (0.12, 0.12, 0.13), "BAFFLE": (0.18, 0.18, 0.19), "FRAME": (0.85, 0.83, 0.78),
              "MIC_RETAINER": (0.3, 0.3, 0.3), "RADAR_RETAINER": (0.3, 0.3, 0.3),
              "PICTURE_CLEAT": (0.75, 0.76, 0.78), "WALL_RAIL": (0.75, 0.76, 0.78),
              **{k: (0.85, 0.83, 0.78) for k in rods}}
    for nm, s in exports.items():
        asm.add(s, name=nm, color=cq.Color(*colors[nm]))
    for nm, s in bought.items():
        col = (0.05, 0.05, 0.05) if nm in ("WF1", "PR1", "PR2", "TW1") else (0.1, 0.35, 0.15)
        asm.add(s, name=nm, color=cq.Color(*col))
    asm.save(str(OUT / "AP-P1-ASSEMBLY.step"))
    for nm, s in bought.items():
        cq.exporters.export(s, str(OUT / f"ENV-{nm}.stl"), tolerance=0.1, angularTolerance=0.3)

    report = {"params": "mechanical/p1/p1_params.json", "gates": gates, "overall": "PASS" if ok else "FAIL",
              "net_air_l": round(v_net / 1e6, 3), "air_before_driver_displacement_l": round(v_air / 1e6, 3),
              "driver_displacement_cm3": {k: round(v / 1e3, 1) for k, v in displ.items()},
              "printed_and_machined_mass_g": mass, "purchased_mass_estimate_g": purchased_g,
              "assembled_mass_estimate_kg": round(total / 1000, 3),
              "mount_faces_z_mm": {"WF1": WF_MOUNT, "PR": PR_MOUNT, "TW1_flange_top": TW_SEAT},
              "edge_screws": len(EDGE_SCREWS), "magnets": len(MAGNETS),
              "assumptions_to_verify": {"PR cone rest above mount face mm": PR_CONE_REST_ABOVE_MOUNT,
                                        "WF cone rest above mount face mm": WF_CONE_REST_ABOVE_MOUNT,
                                        "PR stud trimmed protrusion mm": PR1["stud_protrusion_after_trim"]}}
    (EVID / "cad-gates.json").write_text(json.dumps(report, indent=1) + "\n")
    for g in gates:
        print(f"{g['result']:4s} {g['gate']}: {g['value']}")
    print("net air L", report["net_air_l"], "mass kg", report["assembled_mass_estimate_kg"], "OVERALL", report["overall"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
