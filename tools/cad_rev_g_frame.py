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
    by = -H / 2 + wall + bay_clear / 2
    hat_cx = -W / 2 + wall + 4 + hat[0] / 2
    outer = box(W, H, D, 0, 0, 0)
    behind = box(W - 2 * wall, cavity_h, panel_z - rear, 0, cy, rear)
    pocket = box(pw + 1.0, ph + 1.0, pt, 0, cy, panel_z)
    opening = box(pw - 16, ph - 16, lip + 1, 0, cy, D - lip)
    bay = box(W - 2 * wall, bay_clear, D - rear - lip, 0, by, rear)
    frame = outer.cut(behind).cut(pocket).cut(opening).cut(bay)
    frame = frame.cut(box(14, wall + 2, 8, 0, -H / 2 + wall / 2, 8))  # mains lead, clamped
    frame = frame.cut(box(16, 46, lip + 2, hat_cx, by, D - lip))
    pocket_depth = p["volume_touch"]["pocket_depth_mm"]
    if pocket_depth <= 0 or pocket_depth >= lip:
        print("touch pocket would open the front skin", file=sys.stderr)
        return 1
    for zone in p["volume_touch"]["zones"]:
        zw, zh = zone["size_mm"]
        zx, zy = zone["center_mm"]
        frame = frame.cut(box(zw, zh, pocket_depth, zx, zy, D - lip))
    for dx in (-30, -10, 10, 30):
        frame = frame.cut(box(6, 3, lip + 2, hat_cx + dx, bay_top - 6, D - lip))
    for sign in (-1, 1):
        bx = sign * (W / 2 - wall - 8)
        by_ = H / 2 - wall - 10
        frame = frame.union(box(20, 24, 8, bx, by_, 0))
        head = cq.Workplane("XY").circle(4.0).extrude(6.5).translate((bx, by_ - 4, -0.2))
        slot = box(4.2, 12, 6.5, bx, by_ + 2, -0.2)
        frame = frame.cut(head).cut(slot)
    panel = box(pw, ph, pt, 0, cy, panel_z)

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
        "panel_origin_mm": [round(-pw / 2, 3), round(cy - ph / 2, 3), panel_z],
        "hat_center_mm": [round(hat_cx, 3), round(by, 3)],
        "top_wall_mm": wall,
        "volume_touch_mm": [
            {"id": zone["id"], "center_mm": zone["center_mm"], "size_mm": zone["size_mm"]}
            for zone in p["volume_touch"]["zones"]
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta))
    return 0 if depth <= 30.01 else 1


if __name__ == "__main__":
    raise SystemExit(main())
