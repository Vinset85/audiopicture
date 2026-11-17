"""Board preview PNG.  KiCad Python: plot_board.py dump   |   venv: plot_board.py png [x0 y0 x1 y1] [out.png]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "build", "board_geo.json")


def dump():
    import pcbnew
    sys.path.insert(0, HERE)
    from build_board import PCB, G, bbox_g
    b = pcbnew.LoadBoard(PCB)
    out = {"tracks": [], "vias": [], "pads": [], "fps": [], "rats": []}
    for t in b.GetTracks():
        if t.GetClass() == "PCB_VIA":
            out["vias"].append([*G(t.GetPosition()), pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)), t.GetNetname()])
        else:
            out["tracks"].append([*G(t.GetStart()), *G(t.GetEnd()), pcbnew.ToMM(t.GetWidth()),
                                  b.GetLayerName(t.GetLayer()), t.GetNetname()])
    for fp in b.GetFootprints():
        side = "B" if fp.IsFlipped() else "F"
        cy = fp.GetCourtyard(pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd)
        box = bbox_g(cy.BBox()) if cy.OutlineCount() else bbox_g(fp.GetBoundingBox(False))
        out["fps"].append([fp.GetReference(), side, box])
        for p in fp.Pads():
            out["pads"].append([*bbox_g(p.GetBoundingBox()), side if p.GetAttribute() != pcbnew.PAD_ATTRIB_PTH else "T",
                                p.GetNetname()])
    json.dump(out, open(GEO, "w"))
    print("dumped", {k: len(v) for k, v in out.items()})


def png(view, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    d = json.load(open(GEO))
    drc = os.path.join(HERE, "build", "drc.json")
    if os.path.exists(drc):
        for v in json.load(open(drc)).get("unconnected_items", []):
            it = v["items"]
            if len(it) == 2:
                d["rats"].append([it[0]["pos"]["x"] - 6, 94 - it[0]["pos"]["y"], it[1]["pos"]["x"] - 6,
                                  94 - it[1]["pos"]["y"], it[0]["description"]])
    x0, y0, x1, y1 = view
    fig, ax = plt.subplots(figsize=(max(8, (x1 - x0) / 6), max(3, (y1 - y0) / 6)), dpi=150)
    for xa, ya, xb, yb, side in [(*p[:4], p[4]) for p in d["pads"]]:
        ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fc={"F": "#d4a017", "B": "#4a90d9", "T": "#999"}[side],
                               ec="none", alpha=0.8))
    for ref, side, (a, b_, c, e) in d["fps"]:
        ax.add_patch(Rectangle((a, b_), c - a, e - b_, fill=False, lw=0.3, ec="#c33" if side == "F" else "#36c"))
        if x0 <= a <= x1 and y0 <= b_ <= y1:
            ax.text((a + c) / 2, (b_ + e) / 2, ref, fontsize=3, ha="center", va="center")
    zoom = (x1 - x0) < 45
    if zoom:
        fig.set_size_inches((x1 - x0) / 2.5, (y1 - y0) / 2.5)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal")
    fig.tight_layout()
    fig.canvas.draw()
    pt_per_mm = ax.get_window_extent().width / fig.dpi * 72 / (x1 - x0)
    if zoom:
        import layout
        ax.add_patch(plt.Polygon(layout.STRIP, fc="#2471a3", alpha=0.08, ec="#2471a3", lw=0.3))
        for xa, ya, xb, yb, side, net in [(*p[:4], p[4], p[5]) for p in d["pads"]]:
            if x0 <= xa <= x1 and y0 <= ya <= y1 and net and not net.startswith("unconnected"):
                ax.text((xa + xb) / 2, (ya + yb) / 2, net, fontsize=1.6, ha="center", va="center", rotation=45)
    for xa, ya, xb, yb, w, lay, net in d["tracks"]:
        ax.plot([xa, xb], [ya, yb], lw=w * pt_per_mm if zoom else max(0.3, w * 2.2),
                color="#c0392b" if lay == "F.Cu" else "#2471a3", alpha=0.6 if zoom else 0.85, solid_capstyle="round")
    for x, y, dd, net in d["vias"]:
        ax.add_patch(plt.Circle((x, y), dd / 2, color="#555"))
        if zoom and x0 <= x <= x1 and y0 <= y <= y1:
            ax.text(x, y, net, fontsize=1.4, ha="center", va="center", color="w")
    for xa, ya, xb, yb, net in d["rats"]:
        ax.plot([xa, xb], [ya, yb], lw=0.5, color="#0a0", ls=":")
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_title("ratsnest open: %d" % len(d["rats"]), fontsize=7)
    fig.savefig(path)
    print(path)


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        dump()
    else:
        v = [float(a) for a in sys.argv[2:6]] if len(sys.argv) >= 6 else [14, 16, 306, 74]
        png(v, sys.argv[6] if len(sys.argv) > 6 else os.path.join(HERE, "build", "board.png"))
