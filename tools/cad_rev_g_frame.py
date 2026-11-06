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
    cavity_h = H - bay_h - wall
    bay_clear = bay_h - wall

    def box(w, h, d, x, y, z):
        return cq.Workplane("XY").box(w, h, d, centered=(True, True, False)).translate((x, y, z))

    cy = -H / 2 + wall + bay_h + cavity_h / 2
    by = -H / 2 + wall + bay_clear / 2
    outer = box(W, H, D, 0, 0, 0)
    behind = box(W - 2 * wall, cavity_h, panel_z - rear, 0, cy, rear)
    pocket = box(pw + 1.0, ph + 1.0, pt, 0, cy, panel_z)
    opening = box(pw - 16, ph - 16, lip + 1, 0, cy, D - lip)
    bay = box(W - 2 * wall, bay_clear, D - rear - lip, 0, by, rear)
    frame = outer.cut(behind).cut(pocket).cut(opening).cut(bay)
    frame = frame.cut(box(14, wall + 2, 8, 0, -H / 2 + wall / 2, 8))
    frame = frame.cut(box(16, 46, lip + 2, W / 2 - 36, by, D - lip))
    for x in (-30, -10, 10, 30):
        frame = frame.cut(box(6, 3, lip + 2, x, -H / 2 + bay_h - 6, D - lip))
    frame = frame.union(box(W - 48, 14, 4, 0, H / 2 - 22, 0))
    panel = box(pw, ph, pt, 0, cy, panel_z)

    OUT.mkdir(parents=True, exist_ok=True)
    for name, solid in (("AP-G-FRAME", frame), ("AP-G-PANEL", panel)):
        cq.exporters.export(solid, str(OUT / f"{name}.step"))
        cq.exporters.export(solid, str(OUT / f"{name}.stl"))
    bb = frame.val().BoundingBox()
    depth = bb.zmax - bb.zmin
    meta = {
        "envelope_mm": [round(bb.xmax - bb.xmin, 3), round(bb.ymax - bb.ymin, 3), round(depth, 3)],
        "bay_interior_mm": [round(W - 2 * wall, 3), round(bay_clear, 3)],
        "cavity_mm": [round(W - 2 * wall, 3), round(cavity_h, 3)],
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta))
    return 0 if depth <= 30.01 else 1


if __name__ == "__main__":
    raise SystemExit(main())
