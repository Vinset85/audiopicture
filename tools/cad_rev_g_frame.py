#!/usr/bin/env python3
"""Printable Rev.G frame: 320 x 400 x 30 mm, Satellite1 bay, radar window, panel.

One solid. Front face is Z = 30. Print with the front on the bed.
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

    def box(w, h, d, x, y, z):
        return cq.Workplane("XY").box(w, h, d, centered=(True, True, False)).translate((x, y, z))

    outer = box(W, H, D, 0, 0, 0)
    # Acoustic cavity: above the bay, open through the front lip except a 8 mm picture rebate.
    cavity_h = H - bay_h - wall
    cavity = box(W - 2 * wall, cavity_h, D - rear, 0, -H / 2 + wall + bay_h + cavity_h / 2, rear)
    # Front opening slightly smaller than the panel so the panel sits on a rebate.
    opening = box(pw - 16, ph - 16, lip + 1, 0, -H / 2 + wall + bay_h + cavity_h / 2, D - lip)
    # Electronics bay, open at the back for the boards (covers screw on later if needed).
    bay = box(W - 2 * wall, bay_h - wall, D - rear - 2, 0, -H / 2 + wall + (bay_h - wall) / 2, rear)
    frame = outer.cut(cavity).cut(opening).cut(bay)

    # USB-C slot, bottom edge, centred.
    usb = box(14, wall + 2, 8, 0, -H / 2 + wall / 2, 8)
    # Radar window in the front of the bay, right side. Plastic remains the bay floor.
    radar = box(16, 46, lip + 2, W / 2 - 36, -H / 2 + bay_h / 2, D - lip)
    # Four mic slots above the HAT seat, through the front lip of the bay.
    mics = None
    for i, x in enumerate((-30, -10, 10, 30)):
        slot = box(6, 3, lip + 2, x, -H / 2 + bay_h - 8, D - lip)
        mics = slot if mics is None else mics.union(slot)
    frame = frame.cut(usb).cut(radar).cut(mics)

    # Cleat rib on the rear, inside the top edge. Stays within 30 mm.
    cleat = box(W - 48, 18, 6, 0, H / 2 - 28, 0)
    frame = frame.union(cleat)

    panel = box(pw, ph, pt, 0, -H / 2 + wall + bay_h + cavity_h / 2, D - lip - pt)

    OUT.mkdir(parents=True, exist_ok=True)
    for name, solid in (("AP-G-FRAME", frame), ("AP-G-PANEL", panel)):
        cq.exporters.export(solid, str(OUT / f"{name}.step"))
        cq.exporters.export(solid, str(OUT / f"{name}.stl"))
        print("wrote", name)
    bb = frame.val().BoundingBox()
    depth = round(bb.zmax - bb.zmin, 2)
    if depth > 30.01:
        print("FAIL depth", depth)
        return 1
    meta = {
        "parts": ["AP-G-FRAME", "AP-G-PANEL"],
        "envelope_mm": [round(bb.xmax - bb.xmin, 2), round(bb.ymax - bb.ymin, 2), depth],
        "print": p["print"],
        "note": "Prototype frame. Mic slots are a pitch, not a measured HAT footprint.",
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("envelope", meta["envelope_mm"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
