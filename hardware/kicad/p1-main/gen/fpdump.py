"""Stage A (KiCad Python): dump footprint geometry used by the placer.

Output build/fpgeo.json: per footprint id -> courtyard bbox (local, rot 0, front), pads
[(number, x, y, sx, sy, drill, smd, shape)], through-hole flag.
"""
import json
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import circuit  # noqa: E402

FPDIR = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
LOCAL = {"AudioPicture_P1": os.path.join(HERE, "..", "lib", "AudioPicture_P1.pretty"),
         "AudioPicture_ENV": os.path.join(HERE, "..", "..", "environment", "lib", "AudioPicture_ENV.pretty")}


def libpath(lib):
    return LOCAL.get(lib) or os.path.join(FPDIR, lib + ".pretty")


def load(fpid):
    lib, name = fpid.split(":")
    fp = pcbnew.FootprintLoad(libpath(lib), name)
    if fp is None:
        raise RuntimeError("footprint not found: " + fpid)
    return fp


def mm(v):
    return round(pcbnew.ToMM(v), 4)


def geo(fp):
    cy = fp.GetCourtyard(pcbnew.F_CrtYd)
    if cy.OutlineCount():
        bb = cy.BBox()
        box = [mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())]
    else:
        bb = fp.GetBoundingBox(False)
        box = [mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())]
    pads = []
    tht = False
    for p in fp.Pads():
        pos = p.GetPosition(); s = p.GetSize(pcbnew.F_Cu) if hasattr(p, "GetSize") else p.GetSize()
        drill = mm(p.GetDrillSize().x)
        smd = p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD
        if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH,):
            tht = True
        pads.append([p.GetNumber(), mm(pos.x), mm(pos.y), mm(s.x), mm(s.y), drill, smd,
                     p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH, round(p.GetOrientationDegrees(), 1)])
    return {"box": box, "pads": pads, "tht": tht}


def main():
    out = {}
    for p in circuit.PARTS.values():
        if p["fp"] not in out:
            out[p["fp"]] = geo(load(p["fp"]))
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "build", "fpgeo.json"), "w"), indent=1)
    print(len(out), "footprints")


if __name__ == "__main__":
    main()
