"""KiCad Python helpers for the routing loop.

  kicad_io.py export <dsn>          Specctra DSN of the current board
  kicad_io.py import <ses>          import a session, keeping every pre-existing track/via
  kicad_io.py fill                  refill all zones and save
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.normpath(os.path.join(HERE, "..", "p1-main.kicad_pcb"))


def key(t):
    if t.GetClass() == "PCB_VIA":
        return ("via", t.GetNetname(), t.GetPosition().x, t.GetPosition().y, t.GetWidth(pcbnew.F_Cu), t.GetDrill())
    if t.GetClass() == "PCB_TRACK":
        return ("track", t.GetNetname(), t.GetStart().x, t.GetStart().y, t.GetEnd().x, t.GetEnd().y,
                t.GetWidth(), t.GetLayer())
    return None


def snapshot(board):
    """(key, locked) for every track and via."""
    return [(key(t), t.IsLocked()) for t in board.GetTracks() if key(t)]


def restore(board, items):
    have = {key(t): t for t in board.GetTracks() if key(t)}
    nets = board.GetNetsByName()
    added = 0
    for it, locked in items:
        if it in have:
            if locked:
                have[it].SetLocked(True)
            continue
        if it[0] == "via":
            t = pcbnew.PCB_VIA(board)
            t.SetPosition(pcbnew.VECTOR2I(it[2], it[3])); t.SetWidth(it[4]); t.SetDrill(it[5])
        else:
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pcbnew.VECTOR2I(it[2], it[3])); t.SetEnd(pcbnew.VECTOR2I(it[4], it[5]))
            t.SetWidth(it[6]); t.SetLayer(it[7])
        t.SetNet(nets[it[1]]); t.SetLocked(locked); board.Add(t)
        added += 1
    return added


def main():
    op = sys.argv[1]
    board = pcbnew.LoadBoard(PCB)
    if op == "export":
        ok = pcbnew.ExportSpecctraDSN(board, sys.argv[2])
        print("export", ok)
        return
    if op == "import":
        import re
        ses = open(sys.argv[2]).read()
        routed = set(m.group(1) or m.group(2) for m in
                     re.finditer(r'\(net\s+(?:"([^"]+)"|([^\s()"]+))', ses[ses.find("(network_out"):]))
        before = [(it, lk) for it, lk in snapshot(board) if it[1] not in routed or lk]
        ok = pcbnew.ImportSpecctraSES(board, sys.argv[2])
        n = restore(board, before)
        print("import", ok, "restored", n, "items; tracks now", len(board.GetTracks()))
    if op in ("import", "fill"):
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(PCB)
    print("saved")


if __name__ == "__main__":
    main()
