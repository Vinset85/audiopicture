"""Rebuild the P1 MAIN board from circuit.py end to end.

  make_main.py [sch] [place] [route] [post] [drc] [fab]     (no argument = everything)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.normpath(os.path.join(HERE, ".."))
VPY = sys.executable
KPY = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3")
KCLI = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
NOISE = ("Fontconfig", "assert \"\"traits\"\"")


def run(cmd, cwd=HERE):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if not any(n in l for n in NOISE))
    if out.strip():
        print(out.strip())
    if r.returncode:
        raise SystemExit("FAILED: " + " ".join(cmd))


def main():
    steps = sys.argv[1:] or ["sch", "place", "route", "post", "drc", "fab"]
    if "sch" in steps:
        run([VPY, "p1lib.py"]); run([VPY, "gen_pro.py"]); run([VPY, "gen_sch.py"])
        run([KCLI, "sch", "erc", "--severity-all", "--exit-code-violations", "-o", "build/erc.rpt",
             os.path.join(PRJ, "p1-main.kicad_sch")])
        run([KCLI, "sch", "export", "netlist", "-o", "build/p1.net", os.path.join(PRJ, "p1-main.kicad_sch")])
        run([VPY, "check_netlist.py", "build/p1.net"])
    if "place" in steps:
        run([KPY, "fpdump.py"]); run([KPY, "build_board.py", "fixed"]); run([VPY, "placer.py"])
        run([KPY, "build_board.py", "full"])
    if "route" in steps:
        run([VPY, "route.py", "1", "2"])
    if "post" in steps:
        run([KPY, "post.py"])
    if "drc" in steps:
        run([KCLI, "pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity", "-o", "build/drc.json",
             os.path.join(PRJ, "p1-main.kicad_pcb")])
        run([VPY, "drc_summary.py", "build/drc.json"])
    if "fab" in steps:
        run([VPY, "fab.py"])


if __name__ == "__main__":
    main()
