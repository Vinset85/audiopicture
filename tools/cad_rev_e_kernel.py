#!/usr/bin/env python3
"""Generate Rev.E parametric CAD kernel: frame, panel blank, service rail, cleat.

Requires the ap-cad venv (cadquery). Exports STEP + STL under mechanical/rev-e/cad/.
"""
from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = ROOT / "mechanical/rev-e/rev_e_params.json"
OUT = ROOT / "mechanical/rev-e/cad"


def main() -> int:
    try:
        import cadquery as cq
    except ImportError:
        print("cadquery missing; use ~/.venvs/ap-cad/bin/python", file=sys.stderr)
        return 2
    p = json.loads(PARAMS.read_text())
    W, H, D = p["body"]["width_mm"], p["body"]["height_mm"], p["body"]["depth_mm"]
    lip = p["frame"]["lip_mm"]
    wall = p["frame"]["wall_mm"]
    rail_h = p["frame"]["service_rail_height_mm"]
    pt = p["panel"]["thickness_mm"]
    aw, ah = p["panel"]["aperture_width_mm"], p["panel"]["aperture_height_mm"]

    OUT.mkdir(parents=True, exist_ok=True)

    # Outer shell envelope
    outer = cq.Workplane("XY").box(W, H, D, centered=(True, True, False))
    # Inner cavity
    inner_w, inner_h = W - 2 * wall, H - 2 * wall
    cavity = cq.Workplane("XY").box(inner_w, inner_h, D - wall, centered=(True, True, False)).translate((0, 0, wall))
    frame = outer.cut(cavity)

    # Service rail solid (bottom) — keeps electronics volume
    rail = (
        cq.Workplane("XY")
        .box(inner_w - 1, rail_h, D - wall - 0.5, centered=(True, True, False))
        .translate((0, -H / 2 + wall + rail_h / 2, wall))
    )
    assembly_frame = frame.union(rail)

    # Panel blank in aperture
    panel = (
        cq.Workplane("XY")
        .box(aw, ah, pt, centered=(True, True, False))
        .translate((0, rail_h / 4, D - 1.5 - pt))
    )

    # French cleat (picture side): wedge along top rear
    cleat = (
        cq.Workplane("XY")
        .box(W - 40, 24, 8, centered=(True, True, False))
        .translate((0, H / 2 - 40, 0))
    )

    def export(name: str, solid) -> None:
        step = OUT / f"{name}.step"
        stl = OUT / f"{name}.stl"
        cq.exporters.export(solid, str(step))
        cq.exporters.export(solid, str(stl))
        print("wrote", step.name, stl.name)

    export("AP-E-FRAME", assembly_frame)
    export("AP-E-PANEL", panel)
    export("AP-E-CLEAT", cleat)

    meta = {
        "generator": "tools/cad_rev_e_kernel.py",
        "params": str(PARAMS.relative_to(ROOT)),
        "parts": ["AP-E-FRAME", "AP-E-PANEL", "AP-E-CLEAT"],
        "envelope_mm": [W, H, D],
        "note": "Kernel only — not tooling-ready; exciters and PCB are keep-outs in DMU.",
    }
    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
