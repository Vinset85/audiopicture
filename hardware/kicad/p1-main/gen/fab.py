"""Manufacturing outputs for P1-MAIN: Gerber X2, Excellon, CPL, BOM, schematic PDF, assembly PDF, STEP, CAD envelopes."""
import csv
import glob
import json
import os
import shutil
import subprocess
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(PRJ, "fab")
KCLI = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
KPY = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3")
PCB = os.path.join(PRJ, "p1-main.kicad_pcb")
SCH = os.path.join(PRJ, "p1-main.kicad_sch")
LAYERS = "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"


def cli(*a):
    r = subprocess.run([KCLI, *a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stdout + r.stderr)


def main():
    import circuit
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    g = os.path.join(OUT, "gerber")
    os.makedirs(g)
    cli("pcb", "export", "gerbers", "-o", g + "/", "-l", LAYERS, "--subtract-soldermask", "--use-drill-file-origin", PCB)
    cli("pcb", "export", "drill", "-o", g + "/", "--format", "excellon", "--excellon-units", "mm",
        "--excellon-separate-th", "--generate-map", "--map-format", "pdf", "--drill-origin", "plot", PCB)
    with zipfile.ZipFile(os.path.join(OUT, "P1-MAIN_revA_gerber.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(glob.glob(g + "/*")):
            z.write(f, os.path.basename(f))
    cli("pcb", "export", "pos", "-o", os.path.join(OUT, "P1-MAIN_revA_cpl.csv"), "--format", "csv", "--units", "mm",
        "--side", "both", "--exclude-dnp", PCB)
    cli("sch", "export", "pdf", "-o", os.path.join(OUT, "P1-MAIN_revA_schematic.pdf"), SCH)
    cli("pcb", "export", "pdf", "-o", os.path.join(OUT, "P1-MAIN_revA_assembly_top.pdf"),
        "-l", "F.Fab,Edge.Cuts,F.SilkS", "--mode-single", PCB)
    cli("pcb", "export", "pdf", "-o", os.path.join(OUT, "P1-MAIN_revA_assembly_bottom.pdf"),
        "-l", "B.Fab,Edge.Cuts,B.SilkS", "--mode-single", "--mirror", PCB)
    cli("pcb", "export", "step", "-o", os.path.join(OUT, "P1-MAIN_revA.step"), "--subst-models", "--force",
        "--no-dnp", PCB)
    # BOM grouped by MPN
    rows = {}
    for p in circuit.PARTS.values():
        if p["ref"].startswith(("H", "FID", "TP")):
            continue
        key = (p["mpn"] or p["value"], p["fp"], bool(p.get("dnp")))
        rows.setdefault(key, {"value": p["value"], "refs": [], "note": p.get("note", "")})["refs"].append(p["ref"])
    with open(os.path.join(OUT, "P1-MAIN_revA_bom.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Qty", "Designators", "Value", "MPN", "Footprint", "DNP", "Note"])
        for (mpn, fp, dnp), r in sorted(rows.items(), key=lambda kv: (kv[1]["refs"][0][0], kv[1]["refs"][0])):
            w.writerow([len(r["refs"]), " ".join(sorted(r["refs"], key=lambda s: (s.rstrip("0123456789"), int("0" + s[len(s.rstrip("0123456789")):])))),
                        r["value"], mpn, fp.split(":")[-1], "DNP" if dnp else "", r["note"]])
    # component envelopes for the mechanical CAD
    subprocess.run([KPY, os.path.join(HERE, "envelopes.py"), os.path.join(OUT, "P1-MAIN_revA_envelopes.json")],
                   check=True, capture_output=True)
    print("fab outputs:", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
