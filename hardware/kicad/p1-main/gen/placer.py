"""Stage B (venv Python + numpy): place the non-fixed front-side parts inside their functional regions.

Reads build/fpgeo.json and build/fixed.json, writes build/place.json and build/placement.png.
Courtyards never overlap (0.3 mm min gap); parts stay inside their region; decoupling parts are pulled to
their pin (layout.NEAR); the rest minimise distance to the placed pads of the nets they share.
"""
import json
import math
import os

import numpy as np

import circuit
import layout

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
RES = 0.2
GAP = 0.15                    # courtyard inflation each side
NX = int(round((layout.X1 - layout.X0) / RES))
NY = int(round((layout.Y1 - layout.Y0) / RES))


def cell(x, y):
    return int(math.floor((x - layout.X0) / RES)), int(math.floor((y - layout.Y0) / RES))


def mark(grid, x0, y0, x1, y1, val=True):
    i0, j0 = cell(x0, y0); i1, j1 = cell(x1, y1)
    i0, j0 = max(i0, 0), max(j0, 0); i1, j1 = min(i1 + 1, NX), min(j1 + 1, NY)
    if i1 > i0 and j1 > j0:
        grid[j0:j1, i0:i1] = val


def xform(lx, ly, x, y, rot):
    """Front-side local footprint point -> global CAD (KiCad rotation, y-down local)."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    kx, ky = lx * c + ly * s, -lx * s + ly * c
    return x + kx, y - ky


def rbox(box, x, y, rot):
    pts = [xform(a, b, x, y, rot) for a in (box[0], box[2]) for b in (box[1], box[3])]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)]


def integral(free):
    s = np.zeros((NY + 1, NX + 1), dtype=np.int32)
    s[1:, 1:] = np.cumsum(np.cumsum(~free, axis=0), axis=1)
    return s


def rect_free(S, b):
    i0, j0 = cell(b[0], b[1]); i1, j1 = cell(b[2], b[3])
    if i0 < 0 or j0 < 0 or i1 >= NX or j1 >= NY:
        return False
    return S[j1 + 1, i1 + 1] - S[j0, i1 + 1] - S[j1 + 1, i0] + S[j0, i0] == 0


def main():
    geo = json.load(open(os.path.join(B, "fpgeo.json")))
    fixed = json.load(open(os.path.join(B, "fixed.json")))
    occ = np.zeros((NY, NX), bool)          # front occupancy
    m = 0.25
    occ[:, :] = False
    mark(occ, layout.X0 - 1, layout.Y0 - 1, layout.X0 + m, layout.Y1 + 1)
    mark(occ, layout.X1 - m, layout.Y0 - 1, layout.X1 + 1, layout.Y1 + 1)
    mark(occ, layout.X0 - 1, layout.Y0 - 1, layout.X1 + 1, layout.Y0 + m)
    mark(occ, layout.X0 - 1, layout.Y1 - m, layout.X1 + 1, layout.Y1 + 1)
    for s in layout.SLOTS:
        mark(occ, s[0] - 0.3, s[1] - 0.3, s[2] + 0.3, s[3] + 0.3)
    for b in layout.KEEPOUT_TOP:
        mark(occ, *b)
    mark(occ, *layout.ANTENNA)
    pads_at = {}                              # (ref, pin) -> (x, y)
    for ref, d in fixed.items():
        if d["side"] == "F" or ref.startswith("H"):
            mark(occ, *d["box"])
        for p in d["pads"]:
            if p["tht"]:
                b = p["box"]; mark(occ, b[0] - 0.3, b[1] - 0.3, b[2] + 0.3, b[3] + 0.3)
            if p["num"]:
                b = p["box"]; pads_at[(ref, p["num"])] = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        for b in d["keepouts"]:
            mark(occ, *b)
    prim = np.zeros_like(occ)
    for (x0, y0, x1, y1) in layout.PRIMARY:
        e = layout.ISO + 0.3
        mark(prim, x0 - e, y0 - e, x1 + e, y1 + e)
    regions = {}
    for gname, rects in layout.REGIONS.items():
        r = np.zeros_like(occ)
        for b in rects:
            mark(r, *b)
        regions[gname] = r

    net_pins = circuit.nets()
    todo = [p for p in circuit.PARTS.values() if p["at"] is None and p["ref"] not in layout.FIXED_EXTRA]

    def area(p):
        b = geo[p["fp"]]["box"]
        return (b[2] - b[0]) * (b[3] - b[1])

    def prio(p):
        r = p["ref"]
        if r in layout.NEAR:
            return (2, -area(p))
        if r.startswith(("U", "Q", "L", "Y", "T")) or area(p) > 20:
            return (0, -area(p))
        return (1, -area(p))

    todo.sort(key=prio)
    place = {}

    def net_target(net, exclude_ref):
        pts = [pads_at[(r, n)] for r, n in net_pins[net] if (r, n) in pads_at and r != exclude_ref]
        if not pts:
            return None
        return sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)

    for p in todo:
        g = geo[p["fp"]]
        gname = p["grp"]
        allowed = regions[gname] & ~occ
        if gname != "PRI":
            allowed &= ~prim
        S = integral(allowed)
        targets = []
        for pin, net in p["pins"].items():
            if net in layout.CENTROID_SKIP:
                continue
            t = net_target(net, p["ref"])
            if t:
                targets.append((pin, t))
        if p["ref"] in layout.NEAR:
            rr, pn = layout.NEAR[p["ref"]]
            anchor = pads_at.get((rr, pn))
        else:
            anchor = None
        if anchor is None and targets:
            anchor = (sum(t[0] for _, t in targets) / len(targets), sum(t[1] for _, t in targets) / len(targets))
        if anchor is None:
            xs = [(b[0] + b[2]) / 2 for b in layout.REGIONS[gname]]; ys = [(b[1] + b[3]) / 2 for b in layout.REGIONS[gname]]
            anchor = (sum(xs) / len(xs), sum(ys) / len(ys))
        best = None
        pads_local = [(q[0], q[1], q[2]) for q in g["pads"] if q[0]]
        rots = (0.0, 90.0, 180.0, 270.0)
        found = 0
        for radius in (2, 4, 7, 11, 16, 24, 35, 50, 80, 140, 300):
            step = RES * (1 if radius <= 11 else 2 if radius <= 35 else 5)
            n = int(radius / step)
            cands = []
            for i in range(-n, n + 1):
                for j in range(-n, n + 1):
                    d = math.hypot(i * step, j * step)
                    if d <= radius:
                        cands.append((d, anchor[0] + i * step, anchor[1] + j * step))
            cands.sort()
            for d, x, y in cands:
                x, y = round(x / 0.05) * 0.05, round(y / 0.05) * 0.05
                for r in rots:
                    b = rbox(g["box"], x, y, r)
                    bi = [b[0] - GAP, b[1] - GAP, b[2] + GAP, b[3] + GAP]
                    if not rect_free(S, bi):
                        continue
                    cost = 0.0
                    for pin, t in targets:
                        lp = [q for q in pads_local if q[0] == pin]
                        if lp:
                            px, py = xform(lp[0][1], lp[0][2], x, y, r)
                            cost += math.hypot(px - t[0], py - t[1])
                    if p["ref"] in layout.NEAR:
                        cost += 3.0 * d
                    else:
                        cost += 0.3 * d
                    if best is None or cost < best[0]:
                        best = (cost, x, y, r, b)
                    found += 1
                if found > 60:
                    break
            if best is not None and found > 20:
                break
        if best is None:
            raise SystemExit("no place for %s in %s" % (p["ref"], gname))
        _, x, y, r, b = best
        place[p["ref"]] = {"at": [round(x, 3), round(y, 3)], "rot": r, "box": [round(v, 3) for v in b]}
        mark(occ, b[0] - GAP, b[1] - GAP, b[2] + GAP, b[3] + GAP)
        for q in g["pads"]:
            if q[0]:
                pads_at[(p["ref"], q[0])] = xform(q[1], q[2], x, y, r)
    json.dump(place, open(os.path.join(B, "place.json"), "w"), indent=1)
    print("placed", len(place))
    draw(place, fixed)


def draw(place, fixed):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(30, 7))
    ax.add_patch(Rectangle((layout.X0, layout.Y0), layout.X1 - layout.X0, layout.Y1 - layout.Y0, fill=False, lw=1.5))
    for gname, rects in layout.REGIONS.items():
        if gname == "TP":
            continue
        for b in rects:
            ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=True, alpha=0.06))
            ax.text(b[0] + 0.5, b[3] - 2, gname, fontsize=8, alpha=0.6)
    for b in layout.PRIMARY:
        ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, ec="r", ls="--"))
    for ref, d in fixed.items():
        b = d["box"]
        ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, ec="b" if d["side"] == "F" else "m", lw=0.8))
        ax.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, ref, fontsize=6, ha="center", color="b")
    for ref, d in place.items():
        b = d["box"]
        ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fill=False, ec="k", lw=0.5))
        ax.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, ref, fontsize=4, ha="center", va="center")
    ax.set_xlim(layout.X0 - 2, layout.X1 + 16); ax.set_ylim(layout.Y0 - 2, layout.Y1 + 2); ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(os.path.join(B, "placement.png"), dpi=220)
    from PIL import Image
    im = Image.open(os.path.join(B, "placement.png")); w, h = im.size
    for i in range(3):
        im.crop((int(w * i / 3.2), 0, int(w * (i + 1.2) / 3.2), h)).save(os.path.join(B, "placement_%d.png" % i))


if __name__ == "__main__":
    main()
