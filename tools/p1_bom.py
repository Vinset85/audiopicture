#!/usr/bin/env python3
"""AudioPicture P1 complete bill of materials (one unit): printed and machined parts, drivers, modules,
MAIN PCBA (from hardware/kicad/p1-main/gen/circuit.py), fasteners, inserts, gaskets, damping, cables.

    ~/.venvs/ap-cad/bin/python tools/p1_bom.py   ->  manufacturing/p1/AP-P1-BOM.csv
"""
import csv
import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hardware/kicad/p1-main/gen"))
import circuit  # noqa: E402

P = json.loads((ROOT / "mechanical/p1/p1_params.json").read_text())
G = json.loads((ROOT / "evidence/p1/cad-gates.json").read_text())
OUT = ROOT / "manufacturing/p1/AP-P1-BOM.csv"
N_EDGE, N_MAG, N_TIE = G["edge_screws"], G["magnets"], len(P["ties"])
PIPE_L = round(P["z_stack"]["baffle_front"] - 0.2 - (P["electronics_pocket"]["main_pcb"]["z_bottom"] + 1.6 + 1.2), 1)

# section, item, qty, description, manufacturer / MPN, source, status
MECH = [
    ("A Printed", "AP-P1-TUB", 1, "Tub: rear skin, side walls, partition, ribs, tie columns, connector bay, ENV wall",
     "SLS PA12 (EOS PA 2200 / HP 3D HR PA12), dyed black", "mechanical/p1/cad/out/AP-P1-TUB.step", "MAKE"),
    ("A Printed", "AP-P1-BAFFLE", 1, "Baffle 316x396x12 with rebates, pockets, bores, ENV wall rib",
     "SLS PA12, dyed black", "AP-P1-BAFFLE.step", "MAKE"),
    ("A Printed", "AP-P1-FRAME", 1, "Magnetic front frame", "SLS PA12, dyed to finish", "AP-P1-FRAME.step", "MAKE"),
    ("A Printed", "AP-P1-MIC_RETAINER", 1, "Mic array retainer", "SLS PA12", "AP-P1-MIC_RETAINER.step", "MAKE"),
    ("A Printed", "AP-P1-RADAR_RETAINER", 1, "Radar retainer", "SLS PA12", "AP-P1-RADAR_RETAINER.step", "MAKE"),
    ("A Printed", "AP-P1-BUTTON_ROD", 2, "Push rod MUTE / ACTION", "SLS PA12", "AP-P1-BUTTON_ROD_MUTE.step", "MAKE"),
    ("B Machined", "AP-P1-PICTURE_CLEAT", 1, "French cleat, frame side 130x24x8", "EN AW-6082 T6, anodised",
     "AP-P1-PICTURE_CLEAT.step", "MAKE"),
    ("B Machined", "AP-P1-WALL_RAIL", 1, "French cleat, wall rail 150x24x8", "EN AW-6082 T6, anodised",
     "AP-P1-WALL_RAIL.step", "MAKE"),
    ("C Drivers", "WF1", 1, "Woofer 3.5 in, 4 ohm", "Dayton Audio ND91-4", "Parts Express (SKU to confirm at order)", "BUY"),
    ("C Drivers", "TW1", 1, "Tweeter 3/4 in dome, rear mount, 4 ohm", "Dayton Audio ND20FB-4", "Parts Express (SKU to confirm at order)", "BUY"),
    ("C Drivers", "PR1 PR2", 2, "Passive radiator 3.5 in, one supplied 7.3 g disk fitted each", "Dayton Audio ND90-PR",
     "Parts Express (SKU to confirm at order)", "BUY"),
    ("D Modules", "MAIN PCBA", 1, "P1-MAIN rev A, 292x58 mm, 4 layers 1.6 mm, see section E", "Cinetyk P1-MAIN",
     "hardware/kicad/p1-main/fab", "MAKE"),
    ("D Modules", "FLEX", 1, "XVF3800 voice processor core, without XIAO", "Seeed reSpeaker Flex XVF3800",
     "Seeed Studio", "BUY"),
    ("D Modules", "MIC", 1, "Linear 4-mic array with FPC", "Seeed reSpeaker Flex Linear-4", "Seeed Studio", "BUY"),
    ("D Modules", "RADAR", 1, "60 GHz presence radar", "Hi-Link HLK-LD6004", "Hi-Link", "BUY / VERIFY pinout"),
    ("F Cables", "W1", 1, "IDC ribbon 20-way 1.27 mm, 80 mm, two 2x10 IDC sockets", "Amphenol T812120A101CEU x2 + 3M 3365/20",
     "MAIN J5 -> Flex header", "BUY / VERIFY Flex header pitch"),
    ("F Cables", "W2", 1, "Radar harness GH 1.25 6-way, 120 mm", "JST GHR-06V-S x2 + SSHL-002T-P0.2 x12, 28 AWG",
     "MAIN J6 -> LD6004", "MAKE"),
    ("F Cables", "W3", 1, "Speaker harness VH 3.96 4-way, 200 mm, 18 AWG twisted pairs", "JST VHR-4N + SVH-21T-P1.1 x4",
     "MAIN J4 -> WF1/TW1", "MAKE"),
    ("F Cables", "W3-T", 4, "Driver terminals", "TE 2.8 mm and 4.8 mm FASTON receptacles (VERIFY on driver tabs)",
     "WF1 / TW1", "BUY"),
    ("G Fasteners", "S1", N_EDGE + 2, "Baffle to tub ledge and partition bosses", "M3x16 ISO 10642 A2", "", "BUY"),
    ("G Fasteners", "S2", N_TIE, "Baffle to tie columns", "M4x16 ISO 10642 A2", "", "BUY"),
    ("G Fasteners", "S3", 16, "Drivers to baffle (4 each WF1, TW1, PR1, PR2)", "M3x8 ISO 7380 A2", "", "BUY"),
    ("G Fasteners", "S4", 10, "MAIN (6) and Flex core (4) to standoffs", "M3x6 ISO 7380 A2 + nylon washer M3", "", "BUY"),
    ("G Fasteners", "S5", 4, "Mic and radar retainers", "M3x8 ISO 7380 A2", "", "BUY"),
    ("G Fasteners", "S6", 4, "Picture cleat to tub", "M4x10 ISO 10642 A2", "", "BUY"),
    ("G Fasteners", "S7", 2, "Mic array to retainer fingers (through the board M3 holes)", "M3x6 ISO 7380 A2 nylon", "", "BUY"),
    ("H Inserts", "I1", N_EDGE + 2 + 16 + 10 + 4, "Heat-set insert M3, bore 4.0 x 6", "Ruthex RX-M3x5.7", "", "BUY"),
    ("H Inserts", "I2", N_TIE + 4, "Heat-set insert M4, bore 5.6 x 9", "Ruthex RX-M4x8.1", "", "BUY"),
    ("J Magnetic", "M1", N_MAG, "Frame magnets 8x3 mm axial, bonded", "N52 NdFeB 8x3 Ni-Cu-Ni", "", "BUY"),
    ("J Magnetic", "M2", N_MAG, "Steel discs 8x1 mm in the baffle", "DC01 / 1.0330 zinc plated 8x1", "", "BUY"),
    ("K Seals", "G1", 4, "Driver flange gasket ring, 1.0 mm before compression", "Rogers PORON 4701-30-20040 die-cut",
     "WF1, PR1, PR2 square flange; TW1 39x39", "MAKE (die-cut)"),
    ("K Seals", "G2", 1.45, "Baffle perimeter gasket, metre, 6x2 mm closed cell", "EPDM foam tape 6x2 mm, adhesive one side",
     "", "BUY"),
    ("K Seals", "G3", 4, "Mic port gasket ring 7x3x0.5 mm", "Rogers PORON 4701-30 0.5 mm die-cut", "", "MAKE (die-cut)"),
    ("K Seals", "G4", 1, "Wire pass-through seal, cartridge share", "Neutral-cure silicone (e.g. Dow 3145 RTV)", "", "BUY"),
    ("L Damping", "D1", 40, "Polyester fibre fill in the driver chamber, grams", "Dayton Audio / Acousta-Stuf polyester",
     "VERIFY amount on impedance sweep", "BUY"),
    ("L Damping", "D2", 1, "Butyl CLD sheet 2 mm, 250x300 mm on the rear skin interior", "Silent Coat 2 mm or equal",
     "fit only if the accelerometer scan asks", "OPTIONAL"),
    ("M Front", "F1", 1, "Acoustic fabric 340x420 mm, printed", "ShowTex Speaker Mesh Print 3838", "", "BUY / VERIFY transfer"),
    ("M Front", "F2", 3, f"Light pipe, PMMA rod d3.0 x {PIPE_L} mm, polished ends", "PMMA optical rod 3 mm", "", "MAKE"),
    ("N Misc", "B1", 2, "Rear bumpers", "3M Bumpon SJ5302", "", "BUY"),
    ("N Misc", "L1", 1, "Rating and compliance label 40x20 mm", "polyester label, laser print", "", "MAKE"),
    ("P Power", "PSU", 1, "24 V 2.5 A external adapter, 5.5/2.1 centre positive (alternative to PoE)",
     "Mean Well GST60A24-P1J", "", "BUY / OPTIONAL"),
]


def pcb_rows():
    groups = OrderedDict()
    for p in circuit.PARTS.values():
        if p["ref"].startswith(("H", "FID", "TP")):
            continue
        key = (p["mpn"] or p["value"], p["fp"].split(":")[-1], bool(p["dnp"]))
        groups.setdefault(key, []).append(p)
    rows = []
    for (mpn, fp, dnp), ps in groups.items():
        refs = sorted((q["ref"] for q in ps), key=lambda s: (s.rstrip("0123456789"), int("0" + s[len(s.rstrip("0123456789")):])))
        status = "VERIFY" if "VERIFY" in mpn or any("VERIFY" in (q["note"] or "") for q in ps) else "BUY"
        rows.append(("E MAIN PCBA", " ".join(refs), len(ps), f"{ps[0]['value']} {fp}", mpn, ps[0]["note"] or "",
                     "DNP" if dnp else status))
    return sorted(rows, key=lambda r: r[1])


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Section", "Item / designators", "Qty", "Description", "Manufacturer part / material", "Source / note",
                    "Status"])
        for r in MECH + pcb_rows():
            w.writerow(r)
    n_pcb = sum(1 for p in circuit.PARTS.values() if not p["ref"].startswith(("H", "FID", "TP")))
    print(OUT, "lines", len(MECH) + len(pcb_rows()), "PCB placements", n_pcb)


if __name__ == "__main__":
    main()
