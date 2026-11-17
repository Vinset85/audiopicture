"""Two-pass Freerouting loop (venv Python driving KiCad Python and freerouting-cli).

pass 1: PoE primary nets only, inside the primary region.
pass 2: every other signal net, primary region (+2 mm) as keep-out; plane nets (GND, 3V3, VBUS24) are not
        routed: they reach In1/In2/B.Cu through the fan-out vias, which become obstacles.
"""
import os
import re
import subprocess
import sys

import circuit
import layout

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
KPY = os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3")
JAVA = os.path.expanduser("~/tools/jre/jdk-25.0.5+8-jre/Contents/Home/bin/java")
FR = os.path.expanduser("~/tools/freerouting/freerouting-2.5.0.jar")
PRI = set(circuit.NETCLASS["PRI"])
PLANE = set(layout.PLANE_NETS)


def kio(*args):
    r = subprocess.run([KPY, os.path.join(HERE, "kicad_io.py")] + list(args), capture_output=True, text=True)
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "assert" not in l and "Fontconfig" not in l)
    print(out.strip())
    if r.returncode:
        raise SystemExit("kicad_io failed")


def blocks(txt, start):
    """Yield (i0, i1) spans of balanced S-expressions starting at each match of `start`."""
    for m in re.finditer(start, txt):
        i = m.start(); d = 0
        for j in range(i, len(txt)):
            if txt[j] == "(":
                d += 1
            elif txt[j] == ")":
                d -= 1
                if d == 0:
                    yield i, j + 1
                    break


def section(txt, name):
    return next(blocks(txt, r"\(" + name + r"\b"))


def netname(s):
    m = re.match(r'\((?:net)\s+("([^"]*)"|(\S+))', s)
    return m.group(2) if m.group(2) is not None else m.group(3)


def primary_keepouts():
    out = []
    for (x0, y0, x1, y1) in layout.PRIMARY:
        e = layout.ISO
        out.append((round((x0 - e + 6) * 1000), round((y0 - e - 94) * 1000)))
    return out


OUTSIDE_PRIMARY = [(14.0, 16.0, 188.5, 74.0), (188.5, 16.0, 211.0, 30.0), (188.5, 37.0, 211.0, 74.0),
                   (211.0, 16.0, 251.0, 30.0), (251.0, 16.0, 306.0, 74.0)]


def rect_keepouts(rects):
    out = []
    for (x0, y0, x1, y1) in rects:
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        xy = "  ".join("%d %d" % (round((x + 6) * 1000), round((y - 94) * 1000)) for x, y in pts)
        for lay in ("F.Cu", "B.Cu"):
            out.append('(keepout "" (polygon %s 0  %s))' % (lay, xy))
    return out


def edit(dsn, keep_net, drop_primary_keepouts):
    t = open(dsn).read()
    # inner layers are planes, never routed
    t = re.sub(r"\(layer (In[12]\.Cu)\s*\(type signal\)", r"(layer \1 (type power)", t)
    # SHT4x: the footprint keep-out hugs the pads; freerouting applies clearance to keep-outs, so use an equivalent set
    t = re.sub(r'(\(image "Sensor_Humidity:Sensirion_DFN-4[^\n]*\n(?:.*\n)*?)\s*\(keepout "" \(polygon F\.Cu 0[^)]*\)\)',
               lambda m: m.group(1) + "\n      " + "\n      ".join(
                   '(keepout "" (rect F.Cu %d %d %d %d))' % r for r in
                   ((-300, -750, 300, 750), (300, -100, 750, 100), (-750, -100, -300, 100),
                    (-750, 700, 750, 750), (-750, -750, 750, -700))), t, count=1)
    # network: keep only selected nets
    a, b = section(t, "network")
    net = t[a:b]
    keep = []
    for i0, i1 in list(blocks(net, r"\(net\s")):
        s = net[i0:i1]
        if keep_net(netname(s)):
            keep.append(s)
    classes = [net[i0:i1] for i0, i1 in blocks(net, r"\(class\s")]
    names = set(netname(s) for s in keep)
    fixed_classes = []
    for c in classes:
        head, _, rest = c.partition("(circuit")
        toks = head.split()
        cname = toks[1]
        members = [x for x in toks[2:] if x.strip('"') in names]
        if members:
            fixed_classes.append("(class %s %s (circuit%s" % (cname, " ".join(members), rest) if rest else "(class %s %s)" % (cname, " ".join(members)))
    t = t[:a] + "(network\n    " + "\n    ".join(keep + fixed_classes) + "\n  )" + t[b:]
    # wiring of dropped nets -> keep-outs
    a, b = section(t, "wiring")
    w = t[a:b]
    keepouts, wires = [], []
    for i0, i1 in blocks(w, r"\((wire|via)\s"):
        s = w[i0:i1]
        m = re.search(r'\(net\s+("([^"]*)"|([^\s)]+))\)', s)
        n = m.group(2) if m.group(2) is not None else m.group(3)
        if keep_net(n):
            wires.append(s)
            continue
        pm = re.search(r"\(path (\S+) ([\d.]+)\s+([-\d.\s]+)\)", s)
        if pm:
            keepouts.append('(keepout "" (path %s %s %s))' % (pm.group(1), pm.group(2), pm.group(3).strip()))
        vm = re.match(r'\(via "Via\[0-3\]_(\d+):\d+_um"\s+([-\d.]+) ([-\d.]+)', s)
        if vm:
            for lay in ("F.Cu", "B.Cu"):
                keepouts.append('(keepout "" (circle %s %s %s %s))' % (lay, vm.group(1), vm.group(2), vm.group(3)))
    t = t[:a] + "(wiring\n    " + "\n    ".join(wires) + "\n  )" + t[b:]
    # structure keep-outs
    a, b = section(t, "structure")
    st = t[a:b]
    if drop_primary_keepouts:
        corners = primary_keepouts()
        lines = []
        for i0, i1 in blocks(st, r"\(keepout\s"):
            s = st[i0:i1]
            if any(("%d %d" % c) in s for c in corners):
                lines.append((i0, i1))
        for i0, i1 in reversed(lines):
            st = st[:i0] + st[i1:]
    if drop_primary_keepouts:
        keepouts += rect_keepouts(OUTSIDE_PRIMARY + [(188.5, 72.9, 251.0, 74.0)])
    # board slots: Edge.Cuts clearance 0.3 mm plus margin; fiducials: copper-free 3.2 mm circle
    keepouts += rect_keepouts([(x0 - 0.5, y0 - 0.5, x1 + 0.5, y1 + 0.5) for x0, y0, x1, y1 in layout.SLOTS])
    for p in circuit.PARTS.values():
        if p["ref"].startswith("FID"):
            x, y = p["at"]
            keepouts.append('(keepout "" (circle F.Cu 3200 %d %d))' % (round((x + 6) * 1000), round((y - 94) * 1000)))
    st = re.sub(r"\(plane VBUS24 \(polygon B\.Cu", '(keepout "" (polygon B.Cu', st)
    st = st[:-1] + "\n    " + "\n    ".join(keepouts) + "\n  )"
    t = t[:a] + st + t[b:]
    open(dsn, "w").write(t)
    return len(keep), len(keepouts)


def freeroute(dsn, ses, passes):
    cmd = [JAVA, "-jar", FR, "--gui.enabled=false", "-de", dsn, "-do", ses, "-mp", str(passes), "-mt", "7"]
    print(" ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    log = r.stdout + r.stderr
    open(ses + ".log", "w").write(log)
    tail = [l for l in log.splitlines() if re.search(r"(stage completed|Optimiz|violation\(s\)|unfixable|<->|ERROR)", l)]
    print("\n".join(tail[-8:]))
    if not os.path.exists(ses):
        raise SystemExit("freerouting produced no session")


def main():
    which = sys.argv[1:] or ["1", "2"]
    if "1" in which:
        d = os.path.join(B, "pass1.dsn")
        kio("export", d)
        print("pass1 nets/keepouts", edit(d, lambda n: n in PRI, True))
        freeroute(d, os.path.join(B, "pass1.ses"), 40)
        kio("import", os.path.join(B, "pass1.ses"))
    if "2" in which:
        d = os.path.join(B, "pass2.dsn")
        kio("export", d)
        print("pass2 nets/keepouts", edit(d, lambda n: n not in PRI and n not in PLANE, False))
        freeroute(d, os.path.join(B, "pass2.ses"), 100)
        kio("import", os.path.join(B, "pass2.ses"))
    if "4" in which:
        # primary completion: secondary copper is now fixed, primary keeps its routes and finishes what is open
        d = os.path.join(B, "pass4.dsn")
        kio("export", d)
        print("pass4 nets/keepouts", edit(d, lambda n: n in PRI, True))
        freeroute(d, os.path.join(B, "pass4.ses"), 40)
        kio("import", os.path.join(B, "pass4.ses"))
    if "5" in which:
        # targeted pass: only the nets named after "5", everything else fixed
        only = set(which[which.index("5") + 1:])
        d = os.path.join(B, "pass5.dsn")
        kio("export", d)
        print("pass5 nets/keepouts", edit(d, lambda n: n in only, bool(only & PRI)))
        freeroute(d, os.path.join(B, "pass5.ses"), 80)
        kio("import", os.path.join(B, "pass5.ses"))
        return
    if "3" in which:
        # completion pass: starts from the routed board, rips up and reroutes around what is still open
        d = os.path.join(B, "pass3.dsn")
        kio("export", d)
        print("pass3 nets/keepouts", edit(d, lambda n: n not in PRI and n not in PLANE, False))
        freeroute(d, os.path.join(B, "pass3.ses"), 60)
        kio("import", os.path.join(B, "pass3.ses"))


if __name__ == "__main__":
    main()
