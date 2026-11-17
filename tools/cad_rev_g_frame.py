#!/usr/bin/env python3
"""Printable Rev.G frame. Front face is Z = 30. Print with the front on the bed.

The acoustic cavity stops at the back of the panel. A 1.5 mm lip keeps the
panel in. The bottom bay is tall enough for the 88 mm Satellite1 HAT.
"""
from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = ROOT / "mechanical/rev-g/rev_g_params.json"
OUT = ROOT / "mechanical/rev-g/cad"


def main() -> int:
    try:
        import cadquery as cq
    except ImportError:
        print("cadquery missing; use ~/.venvs/ap-cad/bin/python", file=sys.stderr)
        return 2
    p = json.loads(PARAMS.read_text())
    W, H, D = p["body_mm"]
    wall, rear, lip = p["wall_mm"], p["rear_skin_mm"], p["front_lip_mm"]
    bay_h = p["bay_height_mm"]
    pw, ph, pt = p["panel_mm"]
    panel_z = p["panel_z_mm"]
    hat = p["electronics"]["hat_mm"]
    # bay_h includes the bottom wall. The cavity used to be H-bay_h-wall and
    # ran through the top skin; the top wall is reserved explicitly.
    bay_clear = bay_h - wall
    bay_top = -H / 2 + wall + bay_clear
    cavity_bottom = bay_top + wall
    cavity_top = H / 2 - wall
    cavity_h = cavity_top - cavity_bottom
    if ph + 1.0 > cavity_h or pw + 1.0 > W - 2 * wall:
        print("panel pocket does not fit the closed cavity", file=sys.stderr)
        return 1

    def box(w, h, d, x, y, z):
        return cq.Workplane("XY").box(w, h, d, centered=(True, True, False)).translate((x, y, z))

    cy = (cavity_bottom + cavity_top) / 2
    panel_y0 = -92.0
    py = panel_y0 + ph / 2
    by = -H / 2 + wall + bay_clear / 2
    hat_cx = -W / 2 + wall + 4 + hat[0] / 2
    if panel_y0 < cavity_bottom or panel_y0 + ph > H / 2 - 14:
        print("panel meets the front rabbet", file=sys.stderr)
        return 1
    outer = box(W, H, D, 0, 0, 0)
    behind = box(W - 2 * wall, cavity_h, panel_z - rear, 0, cy, rear)
    pocket = box(pw + 1.0, ph + 1.0, pt, 0, py, panel_z)
    opening = box(pw - 16, ph - 16, lip + 1, 0, py, D - lip)
    bay = box(W - 2 * wall, bay_clear, D - rear - lip, 0, by, rear)
    frame = outer.cut(behind).cut(pocket).cut(opening).cut(bay)
    # Mains inlet is on the rear skin, beside the IRM-30 AC pins. The bottom edge stays closed.
    inlet = p["electronics"]["mains_inlet"]
    ix, iy = inlet["center_mm"]
    iw, ih = inlet["size_mm"]
    frame = frame.cut(box(iw, ih, rear + 0.4, ix, iy, -0.2))
    frame = frame.cut(box(16, 46, lip + 2, hat_cx, by, D - lip))
    touch = p["volume_touch"]
    pocket_depth = touch["pocket_depth_mm"]
    if pocket_depth <= 0 or pocket_depth >= wall - 1.0:
        print("volume pocket would open the bottom wall", file=sys.stderr)
        return 1
    for zone in touch["zones"]:
        zx, zz = zone["center_xz_mm"]
        zw, zd = zone["size_mm"]
        cut_h = pocket_depth + 0.2
        frame = frame.cut(box(zw, cut_h, zd, zx, -H / 2 - 0.2 + cut_h / 2, zz - zd / 2))
        lead = cq.Solid.makeCylinder(
            touch["lead_hole_mm"] / 2,
            2.4,
            cq.Vector(zx, -H / 2 + pocket_depth - 0.4, zz),
            cq.Vector(0, 1, 0),
        )
        frame = frame.cut(cq.Workplane(obj=lead))
    mute = p["mic_mute"]
    mx, mz = mute["center_xz_mm"]
    mute_hole = cq.Solid.makeCylinder(
        mute["hole_diameter_mm"] / 2,
        wall + 0.6,
        cq.Vector(mx, -H / 2 - 0.2, mz),
        cq.Vector(0, 1, 0),
    )
    frame = frame.cut(cq.Workplane(obj=mute_hole))
    for dx in (-30, -10, 10, 30):
        frame = frame.cut(box(6, 3, lip + 2, hat_cx + dx, bay_top - 6, D - lip))
    lamps = p["status_leds"]["lamps"]
    led_r = p["status_leds"]["hole_diameter_mm"] / 2
    if not 0.8 <= led_r <= 1.5 or len(lamps) > 4:
        print("status LEDs must be four or fewer, hole 1.6 to 3 mm", file=sys.stderr)
        return 1
    for lamp in lamps:
        lx, ly = lamp["center_mm"]
        port = cq.Workplane("XY").center(lx, ly).circle(led_r).extrude(lip + 0.4)
        frame = frame.cut(port.translate((0, 0, D - lip - 0.2)))
    for sign in (-1, 1):
        bx = sign * (W / 2 - wall - 8)
        by_ = H / 2 - wall - 10
        frame = frame.union(box(20, 24, 8, bx, by_, 0))
        head = cq.Workplane("XY").circle(4.0).extrude(6.5).translate((bx, by_ - 4, -0.2))
        slot = box(4.2, 12, 6.5, bx, by_ + 2, -0.2)
        frame = frame.cut(head).cut(slot)
    cloth = p["cloth_fastening"]
    magnet = cloth["magnet"]
    rabbet = cloth["rabbet"]
    radius = magnet["pocket_diameter_mm"] / 2
    depth = magnet["pocket_depth_mm"]
    rim, recess, shelf = rabbet["rim_mm"], rabbet["depth_mm"], rabbet["shelf_mm"]
    bleed = 0.2
    inset = rim + (shelf - rim) / 2
    if depth <= 0 or shelf < rim + 2 * radius + 1.0 or inset - radius <= rim:
        print("front rabbet is too narrow for the magnet", file=sys.stderr)
        return 1
    floor_z = D - recess - depth
    ledge_z = floor_z - 1.5
    frame = frame.union(box(shelf, H, D - ledge_z, -W / 2 + shelf / 2, 0, ledge_z))
    frame = frame.union(box(shelf, H, D - ledge_z, W / 2 - shelf / 2, 0, ledge_z))
    frame = frame.union(box(W - 2 * shelf, shelf, D - ledge_z, 0, H / 2 - shelf / 2, ledge_z))
    frame = frame.union(box(W - 2 * shelf, shelf, D - ledge_z, 0, -H / 2 + shelf / 2, ledge_z))
    frame = frame.cut(box(W - 2 * rim, H - 2 * rim, recess + 0.4, 0, 0, D - recess))
    seats = []

    def front_seat(x, y):
        length = depth + bleed
        base = cq.Vector(x, y, D - recess + bleed)
        pocket = cq.Solid.makeCylinder(radius, length, base, cq.Vector(0, 0, -1))
        return cq.Workplane(obj=pocket)

    for y in cloth["long_side_y_mm"]:
        for x in (-W / 2 + inset, W / 2 - inset):
            frame = frame.cut(front_seat(x, y))
            seats.append([round(x, 3), round(y, 3), round(D - recess, 3)])
    for x in cloth["short_side_x_mm"]:
        for y in (-H / 2 + inset, H / 2 - inset):
            frame = frame.cut(front_seat(x, y))
            seats.append([round(x, 3), round(y, 3), round(D - recess, 3)])
    for lamp in lamps:
        lx, ly = lamp["center_mm"]
        port = cq.Workplane("XY").center(lx, ly).circle(led_r).extrude(D - ledge_z + 0.4)
        frame = frame.cut(port.translate((0, 0, ledge_z - 0.2)))
    passage = p["electronics"]["cable_pass"]
    cx, cz = passage["center_xz_mm"]
    cw, cd = passage["size_mm"]
    divider_y = bay_top + wall / 2
    if cz - cd / 2 < rear + 1 or cz + cd / 2 > panel_z - 1:
        print("cable pass leaves the space behind the panel", file=sys.stderr)
        return 1
    frame = frame.cut(box(cw, wall + 0.4, cd, cx, divider_y, cz - cd / 2))
    panel = box(pw, ph, pt, 0, py, panel_z)

    OUT.mkdir(parents=True, exist_ok=True)
    for name, solid in (("AP-G-FRAME", frame), ("AP-G-PANEL", panel)):
        cq.exporters.export(solid, str(OUT / f"{name}.step"))
        cq.exporters.export(solid, str(OUT / f"{name}.stl"))
    bb = frame.val().BoundingBox()

    def span(a, b):
        value = b - a
        return round(value, 2) if abs(value - round(value)) < 0.02 else round(value, 3)

    depth = span(bb.zmin, bb.zmax)
    meta = {
        "envelope_mm": [span(bb.xmin, bb.xmax), span(bb.ymin, bb.ymax), depth],
        "bay_interior_mm": [round(W - 2 * wall, 3), round(bay_clear, 3)],
        "cavity_mm": [round(W - 2 * wall, 3), round(cavity_h, 3)],
        "cavity_y_mm": [round(cavity_bottom, 3), round(cavity_top, 3)],
        "panel_origin_mm": [round(-pw / 2, 3), round(panel_y0, 3), panel_z],
        "hat_center_mm": [round(hat_cx, 3), round(by, 3)],
        "top_wall_mm": wall,
        "volume_touch_mm": [
            {"id": zone["id"], "center_xz_mm": zone["center_xz_mm"], "size_mm": zone["size_mm"]}
            for zone in p["volume_touch"]["zones"]
        ],
        "cloth_magnet_count": len(seats),
        "cloth_magnet_center_mm": seats,
        "status_led_mm": [
            {"id": lamp["id"], "center_mm": lamp["center_mm"]}
            for lamp in p["status_leds"]["lamps"]
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta))
    return 0 if depth <= 30.01 else 1


if __name__ == "__main__":
    raise SystemExit(main())
