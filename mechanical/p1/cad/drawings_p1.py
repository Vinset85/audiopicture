#!/usr/bin/env python3
"""AudioPicture P1 2D drawings: three hidden-line views per manufactured part, overall dimensions,
feature tables from p1_params.json and a title block. STEP files stay the master geometry.

    ~/.venvs/ap-cad/bin/python mechanical/p1/cad/drawings_p1.py      (after build_p1.py)
"""
from __future__ import annotations
import json
import math
import re
from pathlib import Path

import cadquery as cq
from cadquery.occ_impl.exporters.svg import getSVG
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[3]
P = json.loads((ROOT / "mechanical/p1/p1_params.json").read_text())
OUT = ROOT / "mechanical/p1/cad/out"
DWG = ROOT / "mechanical/p1/drawings"
GATES = json.loads((ROOT / "evidence/p1/cad-gates.json").read_text())
EP, DRV, BF = P["electronics_pocket"], P["drivers"], P["baffle"]

SLS = "PA12 SLS (EOS PA 2200 / HP 3D HR PA12), 100 % dense, natural; bead-blast, dye black"
PARTS = {
    "TUB": ("Tub (rear shell, partition, ribs, tie columns, connector bay)", SLS, 1,
            "Heat-set inserts: Ruthex RX-M3x5.7 (ledge, partition, MAIN/Flex standoffs), RX-M4x8.1 (ties, cleat).\n"
            "Seal the driver chamber: 2 coats of PU varnish inside, silicone the wire pass-throughs."),
    "BAFFLE": ("Baffle (driver rebates, mic and radar pockets, light-pipe bores)", SLS, 1,
               "Flatness of the gasket land 0.3 mm. Driver rebates are machined datum faces: verify depth +/-0.1."),
    "FRAME": ("Front frame (magnetic, holds the acoustic fabric)", SLS, 1,
              "Magnets N52 8x3 mm pressed and bonded (Loctite 435). Fabric wrapped and stapled/taped on the back."),
    "MIC_RETAINER": ("Microphone array retainer", SLS, 1, "Screws M3x8 ISO 7380 A2 into the baffle inserts."),
    "RADAR_RETAINER": ("Radar retainer (HLK-LD6004)", SLS, 1, "Screws M3x8 ISO 7380 A2 into the baffle inserts."),
    "BUTTON_ROD_MUTE": ("Button push rod (MUTE and ACTION, same part)", SLS, 2,
                        "Insert from inside before the MAIN board. Outer face flush with the tub bottom face."),
    "PICTURE_CLEAT": ("Picture cleat (French cleat, frame side)", "EN AW-6082 T6 extrusion, anodised", 1,
                      "4x M4x10 ISO 10642 A2 countersunk into the tub inserts."),
    "WALL_RAIL": ("Wall rail (French cleat, wall side)", "EN AW-6082 T6 extrusion, anodised", 1,
                  "3x countersunk 5 mm holes for wall plugs; installer chooses the anchor for the wall type."),
}
VIEWS = (("front (from the room, -Z)", (0, 0, 1)), ("bottom (-Y)", (0, -1, 0)), ("right side (+X)", (1, 0, 0)))


def polylines(shape, direction):
    svg = getSVG(shape, {"projectionDir": direction, "showAxes": False, "showHidden": True,
                         "width": 800, "height": 600})
    vis, hid = [], []
    blocks = re.split(r"<!--\s*(hidden|solid) lines\s*-->", svg)
    for kind, body in zip(blocks[1::2], blocks[2::2]):
        for d in re.findall(r'd="([^"]+)"', body):
            pts = [tuple(map(float, p.split(","))) for p in re.findall(r"-?[\d.e+-]+,-?[\d.e+-]+", d)]
            if len(pts) >= 2:
                (hid if kind == "hidden" else vis).append(pts)
    return vis, hid


def dim(ax, a, b, off, text=None, vertical=False):
    (x0, y0), (x1, y1) = a, b
    if vertical:
        x = max(x0, x1) + off
        ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.5))
        ax.plot([x0, x + off * 0.1], [y0, y0], lw=0.3, color="k"); ax.plot([x1, x + off * 0.1], [y1, y1], lw=0.3, color="k")
        ax.text(x + off * 0.15, (y0 + y1) / 2, text or f"{abs(y1 - y0):.1f}", rotation=90, va="center", fontsize=6)
    else:
        y = min(y0, y1) - off
        ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.5))
        ax.plot([x0, x0], [y0, y - off * 0.1], lw=0.3, color="k"); ax.plot([x1, x1], [y1, y - off * 0.1], lw=0.3, color="k")
        ax.text((x0 + x1) / 2, y - off * 0.35, text or f"{abs(x1 - x0):.1f}", ha="center", va="top", fontsize=6)


def features(name):
    rows = []
    if name == "BAFFLE":
        for k, d in DRV.items():
            if "center" in d:
                cut = d.get("cutout_d") or d.get("hole_d")
                rows.append((k, f"{d['part']}", f"({d['center'][0]:.1f}, {d['center'][1]:.1f})", f"cut-out {cut} mm",
                             f"rebate {d.get('rebate_depth', '-')} mm"))
        ma = EP["mic_array"]
        rows.append(("MIC", "Linear-4 pocket", f"({ma['center'][0]:.1f}, {ma['center'][1]:.1f})",
                     f"{ma['outline'][0]}x{ma['outline'][1]} mm", f"ports d{ma['port_d']} at x {ma['mic_x_from_left']}"))
        ra = EP["radar"]
        rows.append(("RADAR", "LD6004 radome pocket", f"({ra['center'][0]:.1f}, {ra['center'][1]:.1f})",
                     f"{ra['outline'][0]}x{ra['outline'][1]} mm", f"radome {ra['radome_t']} mm"))
        for k in ("light_pipe", "status_led_pipe", "mute_led_pipe"):
            lp = EP[k]
            rows.append((k.upper(), lp.get("_doc", ""), f"({lp['center'][0]:.1f}, {lp['center'][1]:.1f})",
                         f"bore d{lp['d'] + 0.2:.1f}", "through"))
        rows.append(("SCREWS", BF["edge_screw"], f"{GATES['edge_screws']} on the perimeter", "csk d6.8 / 3.4", "flush"))
    elif name == "TUB":
        for i, (x, y) in enumerate(EP["main_pcb"]["mount_holes"]):
            rows.append((f"MAIN-{i + 1}", "MAIN standoff d8, insert RX-M3x5.7", f"({x:.1f}, {y:.1f})",
                         f"top z {EP['main_pcb']['z_bottom']:.1f}", "bore d4.0 x 6"))
        for i, (x, y) in enumerate(P["ties"]):
            rows.append((f"TIE-{i + 1}", "tie column d16, insert RX-M4x8.1", f"({x:.1f}, {y:.1f})",
                         f"top z {P['z_stack']['baffle_back']:.1f}", "bore d5.6 x 9"))
        rb = EP["rear_bay"]
        rows.append(("BAY", "rear connector bay", f"x {rb['x']} y {rb['y']}", f"z {rb['z']}", "open to wall and floor"))
        for nm, (bx, by) in ((k, v) for k, v in EP["buttons"].items() if k in ("MUTE", "ACTION")):
            rows.append((f"BTN-{nm}", "push-rod bore d6.0 through the bottom wall", f"x {bx:.1f}", "axis z 39.3", "rod d5.6"))
        ec = EP["env_chamber"]
        rows.append(("ENV", "ENV chamber wall", f"x {ec['wall_x']}", f"y {ec['y']}", "bottom vents x 287-304"))
    return rows


def sheet(pdf, name):
    title, material, qty, notes = PARTS[name]
    shape = cq.importers.importStep(str(OUT / f"AP-P1-{name}.step")).val()
    bb = shape.BoundingBox()
    fig = plt.figure(figsize=(16.54, 11.69))   # A3 landscape
    gs = fig.add_gridspec(2, 3, height_ratios=[3, 1.25], hspace=0.12, wspace=0.12, left=0.03, right=0.97, top=0.95, bottom=0.04)
    for i, (label, direction) in enumerate(VIEWS):
        ax = fig.add_subplot(gs[0, i])
        vis, hid = polylines(shape, direction)
        for pl in hid:
            ax.plot(*zip(*pl), lw=0.25, color="0.65", ls=(0, (2, 2)))
        for pl in vis:
            ax.plot(*zip(*pl), lw=0.5, color="k")
        xs = [p[0] for pl in vis for p in pl]; ys = [p[1] for pl in vis for p in pl]
        if xs:
            x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
            span = max(x1 - x0, y1 - y0)
            dim(ax, (x0, y0), (x1, y0), 0.06 * span)
            dim(ax, (x1, y0), (x1, y1), 0.05 * span, vertical=True)
            ax.set_xlim(x0 - 0.12 * span, x1 + 0.15 * span); ax.set_ylim(y0 - 0.15 * span, y1 + 0.08 * span)
        ax.set_aspect("equal"); ax.axis("off"); ax.set_title(label, fontsize=8)
    ax = fig.add_subplot(gs[1, :2]); ax.axis("off")
    rows = features(name)
    if rows:
        t = ax.table(cellText=[list(r) for r in rows[:22]], colLabels=["id", "feature", "position (X,Y) mm", "size", "note"],
                     loc="upper left", cellLoc="left", colWidths=[0.08, 0.36, 0.2, 0.16, 0.2])
        t.auto_set_font_size(False); t.set_fontsize(5.5); t.scale(1, 0.9)
    ax = fig.add_subplot(gs[1, 2]); ax.axis("off")
    mass = GATES["printed_and_machined_mass_g"].get(name, "-")
    tb = [("Part", f"AP-P1-{name}"), ("Title", title), ("Qty / unit", str(qty)), ("Material", material),
          ("Envelope mm", f"{bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}"), ("Mass g (CAD)", str(mass)),
          ("Tolerance", "ISO 2768-m unless noted; SLS +/-0.3 % (min +/-0.3 mm)"),
          ("Coordinates", "X right, Y up seen from the room, Z wall(0) -> front"),
          ("Master", f"mechanical/p1/cad/out/AP-P1-{name}.step"), ("Rev", "P1 rev A  2026-10  Cinetyk")]
    for i, (k, v) in enumerate(tb):
        ax.text(0.0, 1 - i * 0.085, k, fontsize=7, weight="bold", va="top")
        ax.text(0.26, 1 - i * 0.085, v, fontsize=7, va="top", wrap=True)
    ax.text(0.0, 1 - len(tb) * 0.085 - 0.02, "Notes: " + notes, fontsize=6.5, va="top", wrap=True)
    fig.suptitle(f"AudioPicture P1 - {title}", fontsize=11, x=0.03, ha="left")
    pdf.savefig(fig)
    fig.savefig(DWG / f"AP-P1-{name}.png", dpi=110)
    plt.close(fig)


def main():
    DWG.mkdir(parents=True, exist_ok=True)
    with PdfPages(DWG / "AP-P1-drawings.pdf") as pdf:
        for name in PARTS:
            sheet(pdf, name)
            print("sheet", name)


if __name__ == "__main__":
    main()
