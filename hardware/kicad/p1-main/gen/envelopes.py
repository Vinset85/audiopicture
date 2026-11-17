"""Component envelopes of the routed MAIN board in global CAD coordinates (KiCad Python).

Each part: side, courtyard box [x0, y0, x1, y1] (mm, front view, Y up) and height above its board face.
"""
import json
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import circuit  # noqa: E402
import layout  # noqa: E402
from build_board import PCB, bbox_g  # noqa: E402

DEFAULT_H = (("DNP0006", 0.65), ("EVQP7A", 1.35), ("B3QFN", 4.0), ("R_Shunt", 0.9), ("Crystal", 0.8),
             ("Fuse", 2.6), ("PMFI", 1.0), ("LED", 0.85), ("0402", 0.6), ("0603", 0.9), ("0805", 1.35), ("1206", 1.8),
             ("1210", 2.7), ("1808", 2.2), ("SOT-23", 1.2), ("SOT", 1.1), ("SOIC", 1.75), ("VSSOP", 1.0),
             ("TSSOP", 1.2), ("LQFP", 1.6), ("VQFN", 1.0), ("QFN", 1.0), ("VSON", 1.0), ("TDSON", 1.1), ("DFN", 0.8),
             ("LGA", 1.0), ("SOD", 1.1), ("D_SMA", 2.4), ("D_SMB", 2.4), ("DRT", 0.6), ("TestPoint", 0.1),
             ("Fiducial", 0.05), ("MountingHole", 0.0))


def height(p):
    if p["h"] is not None:
        return p["h"], "circuit"
    for key, h in DEFAULT_H:
        if key in p["fp"]:
            return h, "package"
    return 3.0, "default"


def main():
    board = pcbnew.LoadBoard(PCB)
    parts = []
    for fp in board.GetFootprints():
        p = circuit.PARTS[fp.GetReference()]
        side = "B" if fp.IsFlipped() else "F"
        cy = fp.GetCourtyard(pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd)
        crt = bbox_g(cy.BBox()) if cy.OutlineCount() else bbox_g(fp.GetBoundingBox(False))
        fab = pcbnew.B_Fab if fp.IsFlipped() else pcbnew.F_Fab
        bodies = [bbox_g(it.GetBoundingBox()) for it in fp.GraphicalItems()
                  if it.GetLayer() == fab and it.GetClass() == "PCB_SHAPE"]
        body = ([min(b[0] for b in bodies), min(b[1] for b in bodies), max(b[2] for b in bodies),
                 max(b[3] for b in bodies)] if bodies else crt)
        h, src = height(p)
        parts.append({"ref": p["ref"], "value": p["value"], "side": side, "body": [round(v, 3) for v in body],
                      "courtyard": [round(v, 3) for v in crt], "h": h, "h_src": src})
    holes = [{"ref": p["ref"], "at": p["at"]} for p in circuit.PARTS.values() if p["ref"].startswith("H")]
    out = {"board": {"outline": [layout.X0, layout.Y0, layout.X1, layout.Y1], "slots": layout.SLOTS,
                     "thickness": 1.6, "front_face": "F.Cu faces the room (+Z)"},
           "holes": holes, "parts": sorted(parts, key=lambda d: d["ref"])}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print("envelopes", len(parts))


if __name__ == "__main__":
    main()
