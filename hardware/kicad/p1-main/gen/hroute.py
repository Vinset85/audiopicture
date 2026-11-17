"""Hand routes outside the TAS5825M cluster (CAD frame, mm).

  hroute.py check            clearance of hand_routes against board_geo.json (venv python)
  hroute.py near X0 Y0 X1 Y1 list copper in a window (venv python)
  hroute.py apply            add hand_routes as locked copper to the board (KiCad python)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hand_routes  # noqa: E402

GEO = os.path.join(HERE, "build", "board_geo.json")
CL = 0.2


def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def seg_seg(a, b, c, d):
    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) - (q[1] - p[1]) * (r[0] - p[0])
    if (ccw(a, b, c) * ccw(a, b, d) < 0) and (ccw(c, d, a) * ccw(c, d, b) < 0):
        return 0.0
    return min(seg_dist(a, c, d), seg_dist(b, c, d), seg_dist(c, a, b), seg_dist(d, a, b))


def seg_rect(a, b, r):
    x0, y0, x1, y1 = r
    if x0 <= a[0] <= x1 and y0 <= a[1] <= y1 or x0 <= b[0] <= x1 and y0 <= b[1] <= y1:
        return 0.0
    edges = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    return min(seg_seg(a, b, c, d) for c, d in edges)


def segments():
    out = []
    for net, layer, w, pts in hand_routes.ROUTES:
        for a, b in zip(pts, pts[1:]):
            out.append((net, layer, w, a, b))
    return out


def removed(kind, net, pts):
    return any(k == kind and n == net and any(math.hypot(px - x, py - y) < 0.02 for px, py in pts)
               for k, n, x, y in hand_routes.REMOVE)


def check():
    import layout
    d = json.load(open(GEO))
    d["tracks"] = [t for t in d["tracks"] if not removed("trk", t[6], [(t[0], t[1]), (t[2], t[3])])]
    d["vias"] = [v for v in d["vias"] if not removed("via", v[3], [(v[0], v[1])])]
    bad = 0
    pad_layer = {"F": "F.Cu", "B": "B.Cu"}
    hv = [(x, y, dd, net) for net, x, y, dd, _ in hand_routes.VIAS]
    for net, layer, w, a, b in segments() + [(n, "*", dd, (x, y), (x, y)) for x, y, dd, n in hv]:
        hw = w / 2
        for t in d["tracks"]:
            if t[6] == net or (layer != "*" and t[5] != layer):
                continue
            g = seg_seg(a, b, (t[0], t[1]), (t[2], t[3])) - hw - t[4] / 2
            if g < CL:
                bad += 1; print("%-8s %s %s-%s  track %s %s gap %.2f" % (net, layer, a, b, t[6], t[5], g))
        for v in d["vias"] + [[x, y, dd, n] for x, y, dd, n in hv]:
            if v[3] == net:
                continue
            g = seg_dist((v[0], v[1]), a, b) - hw - v[2] / 2
            if g < CL:
                bad += 1; print("%-8s %s %s-%s  via %s @%.2f,%.2f gap %.2f" % (net, layer, a, b, v[3], v[0], v[1], g))
        for p in d["pads"]:
            if p[5] == net or (layer != "*" and p[4] != "T" and pad_layer[p[4]] != layer):
                continue
            g = seg_rect(a, b, p[:4]) - hw
            if g < CL:
                bad += 1; print("%-8s %s %s-%s  pad %s @%.2f,%.2f gap %.2f" % (net, layer, a, b, p[5], (p[0] + p[2]) / 2,
                                                                                (p[1] + p[3]) / 2, g))
        if net != "VBUS24" and layer in ("B.Cu", "*"):
            for (x0, y0), (x1, y1) in zip(layout.STRIP, layout.STRIP[1:] + layout.STRIP[:1]):
                g = seg_seg(a, b, (x0, y0), (x1, y1)) - hw
                if g < CL:
                    bad += 1; print("%-8s %s %s-%s  strip edge gap %.2f" % (net, layer, a, b, g))
        for r in layout.PRIMARY:
            if seg_rect(a, b, r) - hw < 0.3:
                bad += 1; print("%-8s %s %s-%s  PRIMARY %s" % (net, layer, a, b, r))
    print("conflicts:", bad)


def near(x0, y0, x1, y1):
    d = json.load(open(GEO))
    def inside(x, y):
        return x0 <= x <= x1 and y0 <= y <= y1
    for t in d["tracks"]:
        if inside(t[0], t[1]) or inside(t[2], t[3]):
            print("trk %-10s %s w%.2f (%.2f,%.2f)-(%.2f,%.2f)" % (t[6], t[5], t[4], *t[:4]))
    for v in d["vias"]:
        if inside(v[0], v[1]):
            print("via %-10s d%.2f (%.2f,%.2f)" % (v[3], v[2], v[0], v[1]))
    for p in d["pads"]:
        if inside((p[0] + p[2]) / 2, (p[1] + p[3]) / 2):
            print("pad %-10s %s [%.2f,%.2f,%.2f,%.2f]" % (p[5], p[4], *p[:4]))
    for r, s, b in d["fps"]:
        if b[0] < x1 and b[2] > x0 and b[1] < y1 and b[3] > y0:
            print("fp  %-6s %s [%.2f,%.2f,%.2f,%.2f]" % (r, s, *b))


def apply():
    import pcbnew
    from build_board import PCB
    board = pcbnew.LoadBoard(PCB)
    nets = board.GetNetsByName()

    def V(x, y):
        return pcbnew.VECTOR2I(pcbnew.FromMM(x + 6), pcbnew.FromMM(94 - y))

    import circuit
    from build_board import G
    for ref, ((x, y), rot) in hand_routes.MOVE.items():
        fp = board.FindFootprintByReference(ref)
        if (circuit.PARTS[ref]["side"] == "B") != fp.IsFlipped():
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        fp.SetOrientationDegrees(rot)
        fp.SetPosition(V(x, y))
        print(ref, "B" if fp.IsFlipped() else "F", ["%s@%.2f,%.2f" % (p.GetNumber(), *G(p.GetPosition())) for p in fp.Pads()])

    kill = []
    for t in board.GetTracks():
        via = t.GetClass() == "PCB_VIA"
        pts = [G(t.GetPosition())] if via else [G(t.GetStart()), G(t.GetEnd())]
        if removed("via" if via else "trk", t.GetNetname(), pts):
            kill.append(t)
    for t in kill:
        board.Remove(t)
    if kill:
        board.Save(PCB)
        board = pcbnew.LoadBoard(PCB)
        nets = board.GetNetsByName()

    layers = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
    have = set()
    for t in board.GetTracks():
        if t.GetClass() == "PCB_VIA":
            have.add(("v", t.GetNetname(), t.GetPosition().x, t.GetPosition().y))
        else:
            have.add(("t", t.GetNetname(), t.GetLayer(), t.GetStart().x, t.GetStart().y, t.GetEnd().x, t.GetEnd().y))
    nt = nv = 0
    for net, layer, w, a, b in segments():
        s, e = V(*a), V(*b)
        if ("t", net, layers[layer], s.x, s.y, e.x, e.y) in have:
            continue
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(s); t.SetEnd(e); t.SetWidth(pcbnew.FromMM(w)); t.SetLayer(layers[layer]); t.SetNet(nets[net])
        t.SetLocked(True)
        board.Add(t); nt += 1
    for net, x, y, dd, dr in hand_routes.VIAS:
        p = V(x, y)
        if ("v", net, p.x, p.y) in have:
            continue
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(p); v.SetWidth(pcbnew.FromMM(dd)); v.SetDrill(pcbnew.FromMM(dr)); v.SetNet(nets[net])
        v.SetLocked(True)
        board.Add(v); nv += 1
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(PCB)
    print("removed %d, added %d tracks %d vias" % (len(kill), nt, nv))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        check()
    elif cmd == "near":
        near(*map(float, sys.argv[2:6]))
    elif cmd == "apply":
        apply()
