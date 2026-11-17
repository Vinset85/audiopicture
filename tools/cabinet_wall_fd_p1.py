#!/usr/bin/env python3
"""P1 wall check with the real tie-column layout (finite-difference Kirchhoff plate).

Rear wall: clamped to the side walls, ribbed (smeared), skin-only where ribs are cut,
solid 10 mm under the cleat recess. Baffle: simply supported on the screwed ledge and on
the partition (conservative), 12 mm solid, thinner at the driver rebates, driver cut-outs
carried as 20 % stiffness plus the full driver mass. Tie columns clamp a Ø16 patch on
both panels. Energy form U = 1/2 * sum D (lap w)^2 h^2.

Reads mechanical/p1/p1_params.json and the CAD net volume from evidence/p1/cad-gates.json.
Writes evidence/p1/wall-fd.json and evidence/p1/wall-fd-modes.png.

    ~/.venvs/ap-cad/bin/python tools/cabinet_wall_fd_p1.py
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, str(Path(__file__).resolve().parent))
from printed_cabinet_acoustics_p1 import MATERIALS, ribbed_plate, plate_D, wall_report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "mechanical/p1/p1_params.json").read_text())
for _k, _d in list(P["drivers"].items()):
    if "same_as" in _d:
        P["drivers"][_k] = {**P["drivers"][_d["same_as"]], **{k: v for k, v in _d.items() if k != "same_as"}}
CAD = json.loads((ROOT / "evidence/p1/cad-gates.json").read_text())
RHO_AIR, C_AIR = 1.204, 343.0
H_MM = 3.0
DRIVER_MASS_KG = {"WF1": 0.3175, "PR1": 0.1207, "PR2": 0.1207}


def grid():
    sw = P["tub"]["side_wall"]; y0, y1 = P["tub"]["driver_interior_y"]
    xs = np.arange(sw, P["body"]["width"] - sw + 1e-9, H_MM)
    ys = np.arange(y0, y1 + 1e-9, H_MM)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    return xs, ys, X, Y


def tie_mask(X, Y):
    r = P["tub"]["tie_column"]["od"] / 2
    m = np.zeros_like(X, dtype=bool)
    for (tx, ty) in P["ties"]:
        m |= (X - tx) ** 2 + (Y - ty) ** 2 <= r ** 2
    return m


def solve(D, m, fixed, clamped_edges):
    nx, ny = D.shape
    h = H_MM * 1e-3
    unk = -np.ones((nx, ny), dtype=int)
    free = ~fixed
    free[0, :] = free[-1, :] = free[:, 0] = free[:, -1] = False
    unk[free] = np.arange(free.sum())
    n = int(free.sum())
    rows, cols, vals, wts = [], [], [], []
    r = 0
    for i in range(nx):
        for j in range(ny):
            entries = {}
            def add(a, b, c):
                if 0 <= a < nx and 0 <= b < ny and unk[a, b] >= 0:
                    entries[unk[a, b]] = entries.get(unk[a, b], 0.0) + c
            add(i, j, -4.0)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if 0 <= a < nx and 0 <= b < ny:
                    add(a, b, 1.0)
                else:   # ghost node beyond the edge
                    add(i - di, j - dj, 1.0 if clamped_edges else -1.0)
            if entries:
                for k, v in entries.items():
                    rows.append(r); cols.append(k); vals.append(v / h ** 2)
                wts.append(D[i, j] * h ** 2)
                r += 1
    L = sp.csr_matrix((vals, (rows, cols)), shape=(r, n))
    K = (L.T @ sp.diags(wts) @ L).tocsc()
    mass = m[free] * h ** 2
    M = sp.diags(mass).tocsc()
    w2, vec = spla.eigsh(K, k=4, M=M, sigma=0.0, which="LM")
    order = np.argsort(w2)
    f = np.sqrt(np.abs(w2[order])) / (2 * math.pi)
    disp = spla.spsolve(K, np.full(n, h ** 2))         # 1 Pa uniform
    dv = float(disp.sum() * h ** 2)
    shape = np.zeros((nx, ny)); shape[free] = vec[:, order[0]]
    return [round(float(x)) for x in f], dv, shape


def rear_wall(X, Y):
    pa = MATERIALS["PA12_SLS"]
    t = P["tub"]; rib = t["rib"]
    D_rib, m_rib = ribbed_plate(pa, t_skin := P["z_stack"]["rear_skin"] * 1e-3, rib["width"] * 1e-3,
                                rib["height"] * 1e-3, rib["pitch"] * 1e-3)
    D = np.full(X.shape, D_rib); m = np.full(X.shape, m_rib)
    D_skin, m_skin = plate_D(pa["E"], pa["nu"], t_skin), pa["rho"] * t_skin
    d = P["drivers"]
    for (c, dia) in ((d["WF1"]["center"], d["WF1"]["magnet_d"] + 14.0), (d["PR1"]["center"], 48.0), (d["PR2"]["center"], 48.0)):
        k = (X - c[0]) ** 2 + (Y - c[1]) ** 2 <= (dia / 2) ** 2
        D[k], m[k] = D_skin, m_skin
    rec = P["cleat"]["recess"]
    k = (X >= rec["x"][0]) & (X <= rec["x"][1]) & (Y >= rec["y"][0]) & (Y <= rec["y"][1])
    D[k], m[k] = plate_D(pa["E"], pa["nu"], 0.010), pa["rho"] * 0.010
    return D, m


def baffle(X, Y):
    pa = MATERIALS["PA12_SLS"]
    tb = P["baffle"]["thickness"] * 1e-3
    D = np.full(X.shape, plate_D(pa["E"], pa["nu"], tb)); m = np.full(X.shape, pa["rho"] * tb)
    for key in ("WF1", "PR1", "PR2"):
        d = P["drivers"][key]; c = d["center"]
        t_reb = (P["baffle"]["thickness"] - d["rebate_depth"]) * 1e-3
        ring = (np.abs(X - c[0]) <= (d["flange_flats"] + 1) / 2) & (np.abs(Y - c[1]) <= (d["flange_flats"] + 1) / 2)
        D[ring], m[ring] = plate_D(pa["E"], pa["nu"], t_reb), pa["rho"] * t_reb
        hole = (X - c[0]) ** 2 + (Y - c[1]) ** 2 <= (d["cutout_d"] / 2) ** 2
        area = math.pi * (d["cutout_d"] * 1e-3 / 2) ** 2
        D[hole] = 0.2 * plate_D(pa["E"], pa["nu"], tb)
        m[hole] = DRIVER_MASS_KG[key] / area
    return D, m


def main():
    xs, ys, X, Y = grid()
    ties = tie_mask(X, Y)
    v_net = CAD["net_air_l"] * 1e-3
    c_box = v_net / (RHO_AIR * C_AIR ** 2)
    out = {"model": "finite-difference Kirchhoff plate, energy form; screening, confirm with accelerometer scan",
           "grid_mm": H_MM, "net_air_l": CAD["net_air_l"], "ties": P["ties"]}
    res = {}
    shapes = {}
    for name, (D, m), clamped in (("rear", rear_wall(X, Y), True), ("baffle", baffle(X, Y), False)):
        f, dv, shape = solve(D, m, ties.copy(), clamped)
        res[name] = {"modes_hz": f, "volume_compliance_m3_per_pa": float(f"{dv:.3e}"),
                     "edge_condition": "clamped" if clamped else "simply supported"}
        shapes[name] = shape
    side = wall_report("side", MATERIALS["PA12_SLS"], 0.306, 0.0523, 0.010, 0, 0, 0)
    c_walls = res["rear"]["volume_compliance_m3_per_pa"] + res["baffle"]["volume_compliance_m3_per_pa"] \
        + 4 * side["volume_compliance_m3_per_pa"]
    pct = 100 * c_walls / c_box
    gates = {"rear f1 >= 500 Hz": res["rear"]["modes_hz"][0] >= 500,
             "baffle f1 >= 500 Hz": res["baffle"]["modes_hz"][0] >= 500,
             "wall/air compliance <= 1 %": pct <= 1.0}
    out.update({"panels": res, "side_wall_f1_hz": side["f1_global_hz"],
                "wall_to_air_compliance_percent": round(pct, 3), "gates": gates,
                "overall": "PASS" if all(gates.values()) else "FAIL"})
    ev = ROOT / "evidence/p1"
    (ev / "wall-fd.json").write_text(json.dumps(out, indent=1) + "\n")
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 2, figsize=(10, 5.4))
        for ax, nm in zip(axs, ("rear", "baffle")):
            s = shapes[nm]; s = s / np.max(np.abs(s))
            ax.pcolormesh(xs, ys, s.T, cmap="RdBu_r", vmin=-1, vmax=1, shading="auto")
            for (tx, ty) in P["ties"]:
                ax.add_patch(plt.Circle((tx, ty), 8, fill=False, color="k"))
            for key in ("WF1", "PR1", "PR2", "TW1"):
                c = P["drivers"][key]["center"]
                d = P["drivers"][key].get("cutout_d", P["drivers"][key].get("hole_d", 36))
                ax.add_patch(plt.Circle(c, d / 2, fill=False, color="0.4", ls="--"))
            ax.set_aspect("equal"); ax.set_title(f"{nm}: mode 1 = {res[nm]['modes_hz'][0]} Hz")
            ax.set_xlabel("x mm"); ax.set_ylabel("y mm")
        fig.suptitle(f"AudioPicture P1 wall modes (ties {len(P['ties'])}, wall/air compliance {pct:.2f} %)")
        fig.tight_layout(); fig.savefig(ev / "wall-fd-modes.png", dpi=110)
    except Exception as e:  # plotting is evidence only
        print("plot skipped:", e)
    for nm, r in res.items():
        print(nm, r["modes_hz"], "Hz", r["volume_compliance_m3_per_pa"], "m3/Pa")
    print("wall/air compliance %", round(pct, 3), "OVERALL", out["overall"])
    return 0 if out["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
