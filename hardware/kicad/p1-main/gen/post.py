"""Post-route pass (KiCad Python): widen power/speaker tracks where clearance allows, add silkscreen, refill zones."""
import collections
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import circuit  # noqa: E402
import layout  # noqa: E402
from build_board import MM, NETCLASSES, PCB, V, G, bbox_g  # noqa: E402

CLASS_OF = {n: c for c, ns in circuit.NETCLASS.items() for n in ns}
WIDE = {   # net: widths to try (mm), widest first
    "DC_RAW": (1.5, 1.0, 0.8), "DC_F": (1.5, 1.0, 0.8), "POE_24V": (1.0, 0.8, 0.6), "VBUS_OR": (1.5, 1.0, 0.8),
    "5V": (1.0, 0.8, 0.6), "FLEX_5V": (0.8, 0.6), "LED_5V": (0.6,), "3V3A": (0.4,), "VBUS_USB": (0.8, 0.6),
    "SW_3V3": (1.0, 0.8, 0.6), "SH_P": (1.5, 1.0, 0.8), "SH_N": (1.5, 1.0, 0.8),
    "POE_VP": (0.8, 0.6), "POE_VN": (0.8, 0.6), "BS_NODE": (0.6,),
    "OUTAP": (1.0, 0.8, 0.6), "OUTAN": (1.0, 0.8, 0.6), "OUTBP": (1.0, 0.8, 0.6), "OUTBN": (1.0, 0.8, 0.6),
    "SPK_WFP": (1.2, 1.0, 0.8), "SPK_WFN": (1.2, 1.0, 0.8), "SPK_TWA": (0.8, 0.6), "SPK_TWP": (0.8, 0.6),
    "SPK_TWN": (0.8, 0.6),
}
CELL = 2.0


def clearance(a, b):
    ca, cb = CLASS_OF.get(a, "Default"), CLASS_OF.get(b, "Default")
    c = max(NETCLASSES[ca][0], NETCLASSES[cb][0])
    if (ca == "PRI") != (cb == "PRI") and b and a:
        c = max(c, 2.0)
    return c + 0.02


class Index:
    def __init__(self, board):
        self.grid = collections.defaultdict(list)
        self.items = []
        for fp in board.GetFootprints():
            for p in fp.Pads():
                self.add(p)
        for t in board.GetTracks():
            self.add(t)

    def add(self, it):
        bb = it.GetBoundingBox()
        x0, y0 = pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY())
        x1, y1 = x0 + pcbnew.ToMM(bb.GetWidth()), y0 + pcbnew.ToMM(bb.GetHeight())
        for i in range(int(x0 // CELL), int(x1 // CELL) + 1):
            for j in range(int(y0 // CELL), int(y1 // CELL) + 1):
                self.grid[(i, j)].append(it)

    def near(self, it, margin):
        bb = it.GetBoundingBox()
        x0, y0 = pcbnew.ToMM(bb.GetX()) - margin, pcbnew.ToMM(bb.GetY()) - margin
        x1, y1 = x0 + pcbnew.ToMM(bb.GetWidth()) + 2 * margin, y0 + pcbnew.ToMM(bb.GetHeight()) + 2 * margin
        seen = set()
        for i in range(int(x0 // CELL), int(x1 // CELL) + 1):
            for j in range(int(y0 // CELL), int(y1 // CELL) + 1):
                for q in self.grid.get((i, j), ()):
                    if id(q) not in seen:
                        seen.add(id(q))
                        yield q


def edge_ok(board, t, margin):
    shape = t.GetEffectiveShape(t.GetLayer())
    for d in board.GetDrawings():
        if d.GetLayer() == pcbnew.Edge_Cuts and d.GetEffectiveShape().Collide(shape, MM(margin)):
            return False
    for fp in board.GetFootprints():
        for z in fp.Zones():
            if z.GetDoNotAllowTracks() and z.IsOnLayer(t.GetLayer()) and z.Outline().Collide(
                    pcbnew.SEG(t.GetStart(), t.GetEnd()), t.GetWidth() // 2):
                return False
    for z in board.Zones():
        if z.GetIsRuleArea() and z.GetDoNotAllowTracks() and z.IsOnLayer(t.GetLayer()) and z.Outline().Collide(
                pcbnew.SEG(t.GetStart(), t.GetEnd()), t.GetWidth() // 2):
            return False
    return True


def fits(board, idx, t):
    net = t.GetNetname()
    if not edge_ok(board, t, 0.3 if CLASS_OF.get(net) != "PRI" else 1.0):
        return False
    shape = t.GetEffectiveShape(t.GetLayer())
    for q in idx.near(t, 2.2):
        qn = q.GetNetname()
        if q is t or (qn == net and qn) or not q.IsOnLayer(t.GetLayer()):
            continue
        if q.GetEffectiveShape(t.GetLayer()).Collide(shape, MM(clearance(net, qn))):
            return False
    return True


def widen(board):
    idx = Index(board)
    stats = collections.Counter()
    narrow = []
    for t in list(board.GetTracks()):
        if t.GetClass() != "PCB_TRACK":
            continue
        net = t.GetNetname()
        w0 = t.GetWidth()
        tries = [w for w in WIDE.get(net, ()) if MM(w) > w0]
        if w0 < MM(0.15):
            tries.append(0.15)
        for w in tries:
            t.SetWidth(MM(w))
            if fits(board, idx, t):
                stats[net] += 1
                break
            t.SetWidth(w0)
        if t.GetWidth() < MM(0.15):
            narrow.append((net, pcbnew.ToMM(t.GetWidth()), G(t.GetStart())))
    if narrow:
        print("tracks still below 0.15 mm:", narrow)
    return stats


def text(board, s, x, y, layer=pcbnew.F_SilkS, size=1.2, angle=0, bold=False):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s); t.SetPosition(V(x, y)); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size))); t.SetTextThickness(MM(size * (0.2 if bold else 0.15)))
    t.SetTextAngleDegrees(angle)
    if layer == pcbnew.B_SilkS:
        t.SetMirrored(True)
    board.Add(t)


def silk(board):
    for d in list(board.GetDrawings()):
        if d.GetClass() == "PCB_TEXT" and d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            board.Remove(d)
    text(board, "AudioPicture P1-MAIN  rev A  2026-10", 230.0, 20.0, size=1.5, bold=True)
    text(board, "Cinetyk", 230.0, 17.8, size=1.0)
    text(board, "PoE PRIMARY - 1500 Vac ISOLATION BARRIER", 232.0, 71.7, size=0.9, bold=True)
    labels = {"J1": "24V DC", "J2": "ETH / PoE", "J3": "USB-C", "J4": "SPK", "J5": "FLEX XVF3800", "J6": "RADAR",
              "SW1": "MUTE", "SW2": "ACT", "U14": "SHT45", "U15": "OPT3004"}
    for fp in board.GetFootprints():
        r = fp.GetReference()
        if r in labels:
            bb = fp.GetCourtyard(pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd).BBox()
            x, y = G(pcbnew.VECTOR2I(bb.Centre().x, bb.GetBottom()))
            layer = pcbnew.B_SilkS if fp.IsFlipped() else pcbnew.F_SilkS
            yy = y - 0.9 if y - 0.9 > layout.Y0 + 0.8 else G(pcbnew.VECTOR2I(0, bb.GetTop()))[1] + 0.9
            text(board, labels[r], x, yy, layer=layer, size=0.9)
    text(board, "AudioPicture P1-MAIN rev A", 230.0, 20.0, layer=pcbnew.B_SilkS, size=1.5, bold=True)


def sync_fields(board):
    for fp in board.GetFootprints():
        p = circuit.PARTS[fp.GetReference()]
        fp.SetValue(p["value"])
        for key in ("MPN", "Note"):
            if p.get(key.lower()) or fp.HasField(key):
                fp.SetField(key, p.get(key.lower()) or "")


def ident(t):
    return (t.GetClass(), t.GetStart().x, t.GetStart().y, t.GetEnd().x, t.GetEnd().y, t.GetLayer(), t.GetNetname())


def cleanup(board):
    """Drop vias joined on fewer than two items and track stubs with a free end (signal nets only)."""
    plane = set(layout.PLANE_NETS)
    removed = collections.Counter()
    pads = collections.defaultdict(list)
    for fp in board.GetFootprints():
        for q in fp.Pads():
            pads[q.GetNetname()].append(q)
    # footprint silkscreen beyond the board outline (U8 antenna marking)
    silk_kill = []
    for fp in board.GetFootprints():
        for it in fp.GraphicalItems():
            if it.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                x0, y0, x1, y1 = bbox_g(it.GetBoundingBox())
                if x0 < layout.X0 + 0.2 or x1 > layout.X1 - 0.2 or y0 < layout.Y0 + 0.2 or y1 > layout.Y1 - 0.2:
                    silk_kill.append((fp, it))
    by_net = collections.defaultdict(list)
    for t in board.GetTracks():
        if t.GetNetname() not in plane:
            by_net[t.GetNetname()].append(t)
    dead = {}
    while True:
        kill = []
        for net, items in by_net.items():
            items = [t for t in items if ident(t) not in dead]
            vias = [t for t in items if t.GetClass() == "PCB_VIA"]
            segs = [t for t in items if t.GetClass() == "PCB_TRACK"]
            for v in vias:
                if v.IsLocked():
                    continue
                ends = [(s.GetLayer(), p) for s in segs for p in (s.GetStart(), s.GetEnd()) if v.HitTest(p)]
                onpad = [q for q in pads[net] if q.HitTest(v.GetPosition())]
                layers = {l for l, _ in ends} | {l for q in onpad for l in (pcbnew.F_Cu, pcbnew.B_Cu) if q.IsOnLayer(l)}
                if len(layers) < 2:
                    pts = {(p.x, p.y) for _, p in ends}
                    if (len(ends) <= 1 and not onpad) or (len(pts) == 1 and not onpad):
                        kill.append(v)   # unused, or joins tracks of one layer that meet at its centre
            for s in segs:
                if s.IsLocked():
                    continue
                for p in (s.GetStart(), s.GetEnd()):
                    hit = any(q.HitTest(p) and q.IsOnLayer(s.GetLayer()) for q in pads[net])
                    hit = hit or any(v.HitTest(p) for v in vias)
                    hit = hit or any(o.GetLayer() == s.GetLayer() and o.HitTest(p, 1)
                                     for o in segs if ident(o) != ident(s))
                    if not hit:
                        kill.append(s)
                        break
        if not kill:
            break
        for t in kill:
            dead[ident(t)] = t
    # removals last: the SWIG proxies are unreliable once items have been removed
    for t in dead.values():
        removed[t.GetClass()] += 1
        board.Remove(t)
    for fp, it in silk_kill:
        fp.Remove(it)
        removed["silk"] += 1
    return dict(removed)


def main():
    board = pcbnew.LoadBoard(PCB)
    print("cleanup", cleanup(board))
    board.Save(PCB)
    board = pcbnew.LoadBoard(PCB)
    sync_fields(board)
    stats = widen(board)
    print("widened", sum(stats.values()), "segments:", dict(stats))
    silk(board)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(PCB)
    print("saved")


if __name__ == "__main__":
    main()
