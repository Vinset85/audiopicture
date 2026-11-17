"""KiCad Python: apply the hand layout of amp_hand.py (and the fixed parts of circuit.py) to the board.

Moves the listed parts, removes the copper they invalidate, adds the hand tracks/vias as locked items
(exported to Specctra as protected wiring) and reshapes the VBUS24 strip.  Safe to run more than once.
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import amp_hand  # noqa: E402
import circuit  # noqa: E402
import layout  # noqa: E402
import build_board  # noqa: E402
from build_board import G, MM, PCB, V, make_fp, place_fixed  # noqa: E402

PLANE = set(layout.PLANE_NETS)
REFIX = ("J5",)          # parts with circuit.py positions that may have moved since the board was routed


def in_rect(x, y, r, m=0.0):
    return r[0] - m <= x <= r[2] + m and r[1] - m <= y <= r[3] + m


def item_points(t):
    if t.GetClass() == "PCB_VIA":
        return [G(t.GetPosition())]
    return [G(t.GetStart()), G(t.GetEnd())]


def main():
    board = pcbnew.LoadBoard(PCB)
    nets = board.GetNetsByName()
    fps = {f.GetReference(): f for f in board.GetFootprints()}
    # footprints changed in circuit.py since the board was built
    for r, p in circuit.PARTS.items():
        f = fps[r]
        if f.GetFPIDAsString() != p["fp"]:
            pos, rot = f.GetPosition(), f.GetOrientationDegrees()
            board.Remove(f)
            f = make_fp(board, {n: nets[n] for n in set(build_board.PADNET.values())}, p)
            f.SetPosition(pos); f.SetOrientationDegrees(rot)
            fps[r] = f
            print("footprint replaced:", r, p["fp"])
    moved = list(amp_hand.PLACE) + ["U11"] + list(REFIX)

    rip_nets = set(sys.argv[1:])     # extra nets to reroute
    old_pads = []
    for r in moved:
        for q in fps[r].Pads():
            n = q.GetNetname()
            if n in PLANE:
                old_pads.append((q, n))
            elif n and not n.startswith("unconnected"):
                rip_nets.add(n)

    tracks = list(board.GetTracks())
    kill = {}

    def uid(t):
        return t.m_Uuid.AsString()
    # plane-net fan-out attached to the old pads of moved parts
    for t in tracks:
        if t.GetClass() == "PCB_TRACK" and t.GetNetname() in PLANE:
            for q, n in old_pads:
                if n == t.GetNetname() and (q.HitTest(t.GetStart()) or q.HitTest(t.GetEnd())):
                    kill[uid(t)] = t
    ends = {}
    for t in tracks:
        if t.GetClass() == "PCB_TRACK" and uid(t) not in kill:
            for p in (t.GetStart(), t.GetEnd()):
                ends.setdefault(t.GetNetname(), []).append(p)
    for t in tracks:
        if t.GetClass() == "PCB_VIA" and t.GetNetname() in PLANE:
            attached = any(q.HitTest(t.GetPosition()) for q, n in old_pads if n == t.GetNetname())
            fed = any(t.HitTest(p) for p in ends.get(t.GetNetname(), []))
            near_old = any((q.GetPosition() - t.GetPosition()).EuclideanNorm() < MM(3.0) for q, n in old_pads)
            if near_old and not fed and not attached:
                kill[uid(t)] = t
    # everything inside the hand windows, and whole nets that touch them
    for t in tracks:
        if any(in_rect(x, y, r) for x, y in item_points(t) for r in amp_hand.CLEAR):
            kill[uid(t)] = t
            if t.GetNetname() not in PLANE:
                rip_nets.add(t.GetNetname())

    # move parts
    for r, (x, y, rot) in amp_hand.PLACE.items():
        f = fps[r]
        f.SetOrientationDegrees(rot)
        f.SetPosition(V(x, y))
    for r in REFIX:
        if fps[r].IsFlipped():
            fps[r].Flip(fps[r].GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        place_fixed(fps[r], circuit.PARTS[r])

    # other copper hit by the new pads
    newpads = [q for r in moved for q in fps[r].Pads()]
    for t in tracks:
        if uid(t) in kill:
            continue
        for q in newpads:
            if q.GetNetname() == t.GetNetname() and q.GetNetname():
                continue
            lays = [l for l in (pcbnew.F_Cu, pcbnew.B_Cu) if q.IsOnLayer(l) and t.IsOnLayer(l)]
            if any(q.GetEffectiveShape(l).Collide(t.GetEffectiveShape(l), MM(0.2)) for l in lays):
                kill[uid(t)] = t
                if t.GetNetname() not in PLANE:
                    rip_nets.add(t.GetNetname())
                break
    for t in tracks:
        if t.GetNetname() in rip_nets and not t.GetNetname() in PLANE:
            kill[uid(t)] = t
    for t in kill.values():
        board.Remove(t)

    # hand copper
    def pt(p):
        if isinstance(p, tuple) and p and p[0] == "pad":
            _, r, n = p
            q = next(q for q in fps[r].Pads() if q.GetNumber() == n)
            return q.GetPosition()
        return V(*p)

    nt = nv = 0
    for net, w, pts in amp_hand.TRACKS:
        vs = [pt(p) for p in pts]
        for a, b in zip(vs, vs[1:]):
            if a == b:
                continue
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(a); t.SetEnd(b); t.SetWidth(MM(w)); t.SetLayer(pcbnew.F_Cu); t.SetNet(nets[net])
            t.SetLocked(True)
            board.Add(t); nt += 1
    for net, x, y, d, dr in amp_hand.VIAS:
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(V(x, y)); v.SetWidth(MM(d)); v.SetDrill(MM(dr)); v.SetNet(nets[net])
        v.SetLocked(True)
        board.Add(v); nv += 1

    # VBUS24 strip outline
    for z in board.Zones():
        if z.GetZoneName() == "VBUS24 strip":
            ol = z.Outline()
            ol.RemoveAllContours()
            ol.NewOutline()
            for x, y in layout.STRIP:
                p = V(x, y)
                ol.Append(p.x, p.y)

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(PCB)
    print("removed %d items, ripped %d nets, added %d tracks %d vias" % (len(kill), len(rip_nets), nt, nv))
    print("ripped:", " ".join(sorted(rip_nets)))


if __name__ == "__main__":
    main()
