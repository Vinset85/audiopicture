"""Minimal KiCad .kicad_sym reader: S-expression parse, `extends` flattening, pin geometry."""
from __future__ import annotations
import os
import re
from functools import lru_cache
from pathlib import Path

KICAD = Path(os.path.expanduser("~/Applications/KiCad/KiCad.app/Contents/SharedSupport"))
SYMDIR = KICAD / "symbols"
FPDIR = KICAD / "footprints"
LOCAL_SYM = {}


def tokenize(s: str):
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in " \t\r\n":
            i += 1
        elif c in "()":
            yield c; i += 1
        elif c == '"':
            j = i + 1; buf = []
            while s[j] != '"':
                if s[j] == "\\":
                    buf.append(s[j + 1]); j += 2
                else:
                    buf.append(s[j]); j += 1
            yield ('"', "".join(buf)); i = j + 1
        else:
            j = i
            while j < n and s[j] not in " \t\r\n()":
                j += 1
            yield s[i:j]; i = j


def parse(s: str):
    stack, cur = [], []
    for t in tokenize(s):
        if t == "(":
            stack.append(cur); cur = []
        elif t == ")":
            done = cur; cur = stack.pop(); cur.append(done)
        else:
            cur.append(t)
    return cur[0]


def dump(x, ind=0) -> str:
    if isinstance(x, tuple):
        return '"' + x[1].replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(x, str):
        return x
    inner = [dump(e, ind + 1) for e in x]
    one = "(" + " ".join(inner) + ")"
    if len(one) < 100 and not any(isinstance(e, list) and len(e) > 3 for e in x):
        return one
    pad = "\t" * (ind + 1)
    return "(" + inner[0] + "".join("\n" + pad + e for e in inner[1:]) + ")"


def sval(x):
    return x[1] if isinstance(x, tuple) else x


def find(node, key):
    return [e for e in node if isinstance(e, list) and e and e[0] == key]


def first(node, key):
    r = find(node, key)
    return r[0] if r else None


@lru_cache(maxsize=None)
def load_lib(lib: str):
    path = LOCAL_SYM.get(lib) or (SYMDIR / f"{lib}.kicad_sym")
    tree = parse(Path(path).read_text())
    return {sval(s[1]): s for s in find(tree, "symbol")}


def symbol(lib_id: str):
    """Return a flattened symbol S-expression named lib_id (extends resolved)."""
    lib, name = lib_id.split(":")
    syms = load_lib(lib)
    s = [list(e) if isinstance(e, list) else e for e in syms[name]]
    ext = first(s, "extends")
    if ext is not None:
        parent = symbol(f"{lib}:{sval(ext[1])}")
        pname = sval(parent[1]).split(":")[-1]
        props = {sval(p[1]): p for p in find(s, "property")}
        out = [parent[0], ('"', name)]
        for e in parent[2:]:
            if isinstance(e, list) and e[0] == "property" and sval(e[1]) in props:
                out.append(props.pop(sval(e[1])))
            elif isinstance(e, list) and e[0] == "symbol":
                sub = list(e); sub[1] = ('"', sval(e[1]).replace(pname, name, 1)); out.append(sub)
            else:
                out.append(e)
        out[2:2] = []
        for p in props.values():
            out.append(p)
        s = out
    s = list(s); s[1] = ('"', lib_id)
    return s


def pins(lib_id: str):
    """[(number, name, etype, x, y, angle, length, unit)] in symbol coordinates (y up)."""
    s = symbol(lib_id)
    out = []
    for sub in find(s, "symbol"):
        m = re.search(r"_(\d+)_(\d+)$", sval(sub[1]))
        unit = int(m.group(1)) if m else 0
        for p in find(sub, "pin"):
            at = first(p, "at"); ln = first(p, "length")
            out.append((sval(first(p, "number")[1]), sval(first(p, "name")[1]), p[1],
                        float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0,
                        float(ln[1]), unit))
    return out


def prop(lib_id: str, key: str):
    for p in find(symbol(lib_id), "property"):
        if sval(p[1]) == key:
            return sval(p[2])
    return None
