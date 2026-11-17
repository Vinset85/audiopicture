#!/usr/bin/env python3
"""Rev.G assembly without the cloth. Parts sit where the spec puts them.

The PD source and the line filter have no frozen outline, so those two
bodies are fit-check blocks. Wires follow the routes the cavities allow.
"""
from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = ROOT / "mechanical/rev-g/rev_g_params.json"
CAD = ROOT / "mechanical/rev-g/cad"
FRAME = CAD / "AP-G-FRAME.step"


def box(cq, w, h, d, x, y, z):
    # (x, y, z) is the minimum corner. CadQuery otherwise centres X and Y.
    return cq.Workplane("XY").box(w, h, d, centered=(False, False, False)).translate((x, y, z))


def tube(cq, a, b, radius):
    start = cq.Vector(*a)
    end = cq.Vector(*b)
    axis = end - start
    length = axis.Length
    if length < 0.2:
        return None
    solid = cq.Solid.makeCylinder(radius, length, start, axis.normalized())
    return cq.Workplane(obj=solid)


def samples_box(x0, y0, z0, x1, y1, z1):
    def axis(a, b):
        inset = min(0.4, abs(b - a) * 0.25)
        return (a + inset, (a + b) / 2, b - inset)
    return [(x, y, z) for x in axis(x0, x1) for y in axis(y0, y1) for z in axis(z0, z1)]


def samples_line(a, b, step=2.0):
    ax, ay, az = a
    bx, by, bz = b
    n = max(1, int(((bx - ax) ** 2 + (by - ay) ** 2 + (bz - az) ** 2) ** 0.5 // step))
    return [
        (ax + (bx - ax) * i / n, ay + (by - ay) * i / n, az + (bz - az) * i / n)
        for i in range(n + 1)
    ]


def overlaps(a, b, gap=0.2):
    return not (
        a[1][0] <= b[0][0] + gap or b[1][0] <= a[0][0] + gap
        or a[1][1] <= b[0][1] + gap or b[1][1] <= a[0][1] + gap
        or a[1][2] <= b[0][2] + gap or b[1][2] <= a[0][2] + gap
    )


def main() -> int:
    try:
        import cadquery as cq
    except ImportError:
        print("cadquery missing; use ~/.venvs/ap-cad/bin/python", file=sys.stderr)
        return 2
    if not FRAME.is_file():
        print("frame STEP missing; run tools/cad_rev_g_frame.py", file=sys.stderr)
        return 1
    p = json.loads(PARAMS.read_text())
    W, H, D = p["body_mm"]
    wall, rear = p["wall_mm"], p["rear_skin_mm"]
    bay_h = p["bay_height_mm"]
    pw, ph, pt = p["panel_mm"]
    panel_z = p["panel_z_mm"]
    panel_x0, panel_y0 = -pw / 2, -92.0
    bay_clear = bay_h - wall
    bay_top = -H / 2 + wall + bay_clear
    hat = p["electronics"]["hat_mm"]
    core = p["electronics"]["core_mm"]
    psu = p["electronics"]["psu"]["size_mm"]
    amp = p["electronics"]["amp_max_mm"]
    hat_cx = -W / 2 + wall + 4 + hat[0] / 2
    hat_cy = -H / 2 + wall + bay_clear / 2
    core_right = hat_cx + hat[0] / 2 + 6 + core[0]
    psu_left = core_right + 4
    amp_left = psu_left + psu[0] + 4

    frame = cq.importers.importStep(str(FRAME))
    shape = frame.val()
    solids = [shape]
    bounds = {}

    def add(name, solid, bound):
        bounds[name] = bound
        solids.append(solid.val() if hasattr(solid, "val") else solid)

    panel = box(cq, pw, ph, pt, panel_x0, panel_y0, panel_z)
    add("panel", panel, ((panel_x0, panel_y0, panel_z), (panel_x0 + pw, panel_y0 + ph, panel_z + pt)))

    lf = p["exciters"]["lf"]
    lx = panel_x0 + lf["on_panel_mm_from_lower_left"][0]
    ly = panel_y0 + lf["on_panel_mm_from_lower_left"][1]
    lf_r = lf["diameter_mm"] / 2
    lf_z0 = panel_z - lf["depth_mm"]
    lf_body = cq.Workplane("XY").circle(lf_r).extrude(lf["depth_mm"]).translate((lx, ly, lf_z0))
    add("xt19", lf_body, ((lx - 12, ly - 12, lf_z0 + 0.4), (lx + 12, ly + 12, panel_z - 0.4)))

    wb = p["exciters"]["wb"]
    wx = panel_x0 + wb["on_panel_mm_from_lower_left"][0] - wb["footprint_mm"][0] / 2
    wy = panel_y0 + wb["on_panel_mm_from_lower_left"][1] - wb["footprint_mm"][1] / 2
    ww, wh, wd = wb["footprint_mm"][0], wb["footprint_mm"][1], wb["depth_mm"]
    wb_z0 = panel_z - wd
    add("teax", box(cq, ww, wh, wd, wx, wy, wb_z0), ((wx, wy, wb_z0), (wx + ww, wy + wh, panel_z)))

    hat_x0 = hat_cx - hat[0] / 2
    hat_y0 = hat_cy - hat[1] / 2
    add("hat", box(cq, hat[0], hat[1], hat[2], hat_x0, hat_y0, rear), (
        (hat_x0, hat_y0, rear), (hat_x0 + hat[0], hat_y0 + hat[1], rear + hat[2])))
    core_x0 = hat_x0 + hat[0] + 6
    core_y0 = hat_cy - core[1] / 2
    add("core", box(cq, core[0], core[1], core[2], core_x0, core_y0, rear), (
        (core_x0, core_y0, rear), (core_x0 + core[0], core_y0 + core[1], rear + core[2])))
    add("radar", box(cq, 15, 44, 3, hat_cx - 7.5, hat_cy - 22, 25.2), (
        (hat_cx - 7.5, hat_cy - 22, 25.2), (hat_cx + 7.5, hat_cy + 22, 28.2)))
    add("psu", box(cq, psu[0], psu[1], psu[2], psu_left, hat_cy - psu[1] / 2, rear), (
        (psu_left, hat_cy - psu[1] / 2, rear),
        (psu_left + psu[0], hat_cy + psu[1] / 2, rear + psu[2])))
    add("amp", box(cq, amp[0], amp[1], amp[2], amp_left, hat_cy - amp[1] / 2, rear), (
        (amp_left, hat_cy - amp[1] / 2, rear),
        (amp_left + amp[0], hat_cy + amp[1] / 2, rear + amp[2])))
    # Fit-check blocks. No outline is frozen for these two.
    add("pd", box(cq, 30, 16, 10, -52, hat_cy - 8, 12), ((-52, hat_cy - 8, 12), (-22, hat_cy + 8, 22)))
    add("filter", box(cq, 28, 16, 8, 96, hat_cy - 8, 18), ((96, hat_cy - 8, 18), (124, hat_cy + 8, 26)))

    for zone in p["volume_touch"]["zones"]:
        zx, zz = zone["center_xz_mm"]
        add(zone["id"], box(cq, 24, 0.4, 10, zx - 12, -199.8, zz - 5), (
            (zx - 12, -199.8, zz - 5), (zx + 12, -199.4, zz + 5)))
        add(zone["id"] + "_ttp", box(cq, 16, 11, 3, zx - 8, -182, 13), (
            (zx - 8, -182, 13), (zx + 8, -171, 16)))
    mx, mz = p["mic_mute"]["center_xz_mm"]
    add("mute", box(cq, 8, 10, 8, mx - 4, -196, mz - 4), ((mx - 4, -196, mz - 4), (mx + 4, -186, mz + 4)))
    for lamp in p["status_leds"]["lamps"]:
        lx_, ly_ = lamp["center_mm"]
        led = cq.Workplane("XY").center(lx_, ly_).circle(1.4).extrude(5).translate((0, 0, 18))
        add(lamp["id"], led, ((lx_ - 0.7, ly_ - 0.7, 18.4), (lx_ + 0.7, ly_ + 0.7, 22.6)))

    cloth = p["cloth_fastening"]
    rabbet = cloth["rabbet"]
    inset = rabbet["rim_mm"] + (rabbet["shelf_mm"] - rabbet["rim_mm"]) / 2
    mag_z = D - rabbet["depth_mm"] - cloth["magnet"]["thickness_mm"]
    seats = [(x, y) for y in cloth["long_side_y_mm"] for x in (-W / 2 + inset, W / 2 - inset)]
    seats += [(x, y) for x in cloth["short_side_x_mm"] for y in (-H / 2 + inset, H / 2 - inset)]
    for i, (sx, sy) in enumerate(seats):
        magnet = cq.Workplane("XY").center(sx, sy).circle(4).extrude(2).translate((0, 0, mag_z))
        add(f"magnet_{i}", magnet, ((sx - 2.2, sy - 2.2, mag_z + 0.2), (sx + 2.2, sy + 2.2, mag_z + 1.8)))

    routes = {
        "mains": [(77, -180, 4), (77, -172, 4), (83, -160, 8)],
        "dc_amp": [(10, -170, 8), (10, -192, 8), (100, -192, 8)],
        "dc_pd": [(40, hat_cy, 26), (-30, hat_cy, 26), (-37, hat_cy, 22)],
        "audio": [(-70, -120, 26), (110, -120, 26), (110, hat_cy, 26)],
        "spk_lf": [(112, -104, 6), (118, -70, 6), (-36, -70, 8), (-36, -36, 8)],
        "spk_wb": [(128, -104, 6), (128, 78, 5), (40, 78, 4)],
        "touch_l": [(-40, -198, 15), (-40, -176, 14), (-40, -193, 8), (-100, -193, 8)],
        "touch_r": [(40, -198, 15), (40, -176, 14), (40, -193, 8), (100, -193, 8), (-100, -193, 6)],
        "mute_w": [(0, -184, 15), (0, -193, 12), (-90, -193, 12)],
        "leds": [(-45, -192, 18), (-45, -175, 16), (45, -175, 16), (-70, -160, 14)],
        "radar_w": [(hat_cx, hat_cy, 25), (hat_cx, hat_cy, 12)],
        "antenna": [(-25, -130, 8), (-25, -108, 8)],
        "ground": [(90, -192, 5), (-100, -192, 5)],
    }
    wire_pts = []
    for name, points in routes.items():
        radius = 1.6 if name.startswith("spk") or name in ("mains", "dc_amp", "dc_pd") else 1.0
        for a, b in zip(points, points[1:]):
            segment = tube(cq, a, b, radius)
            if segment is not None:
                solids.append(segment.val())
            wire_pts.extend(samples_line(a, b))

    problems = []
    for name, bound in bounds.items():
        hit = [pt for pt in samples_box(*bound[0], *bound[1]) if shape.isInside(pt)]
        if hit:
            problems.append(f"{name} inside the frame at {tuple(round(v, 1) for v in hit[0])}")
    names = list(bounds)
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            if overlaps(bounds[left], bounds[right]):
                problems.append(f"{left} meets {right}")
    buried = [pt for pt in wire_pts if shape.isInside(pt)]
    if buried:
        problems.append(f"a wire enters the frame at {tuple(round(v, 1) for v in buried[0])}")

    def outside(pt):
        x, y, z = pt
        return x < -W / 2 - 0.05 or x > W / 2 + 0.05 or y < -H / 2 - 0.05 or y > H / 2 + 0.05 or z < -0.05 or z > D + 0.05

    for name, bound in bounds.items():
        corners = [
            (x, y, z)
            for x in bound[0][0:1] + bound[1][0:1]
            for y in (bound[0][1], bound[1][1])
            for z in (bound[0][2], bound[1][2])
        ]
        hit = [pt for pt in corners if outside(pt)]
        if hit:
            problems.append(f"{name} leaves the outline at {tuple(round(v, 1) for v in hit[0])}")
    stray = [pt for pt in wire_pts if outside(pt)]
    if stray:
        problems.append(f"a wire leaves the outline at {tuple(round(v, 1) for v in stray[0])}")

    compound = cq.Compound.makeCompound(solids)
    out = CAD / "AP-G-ASSEMBLY.stl"
    cq.exporters.export(cq.Workplane(obj=compound), str(out))
    print(json.dumps({
        "stl": str(out.relative_to(ROOT)),
        "bytes": out.stat().st_size,
        "parts": len(bounds),
        "wires": len(routes),
        "problems": problems,
    }, indent=2))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
