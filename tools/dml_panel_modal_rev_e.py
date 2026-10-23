#!/usr/bin/env python3
"""Analytical modal screening for the Rev.E DML panel (simply-supported plate).

Not a full FEA and not a measurement. Used to seed exciter placement and to
reject panels whose first mode sits inside the listening band without damping.
"""
from __future__ import annotations
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = ROOT / "mechanical/rev-e/rev_e_params.json"
OUT = ROOT / "evidence/rev-e/panel-modal-screen.json"


def plate_modes(a_m: float, b_m: float, h_m: float, E: float, nu: float, rho: float, nmax: int = 5):
    D = E * h_m**3 / (12.0 * (1.0 - nu**2))
    mu = rho * h_m
    modes = []
    for m in range(1, nmax + 1):
        for n in range(1, nmax + 1):
            k = (m * math.pi / a_m) ** 2 + (n * math.pi / b_m) ** 2
            w = math.sqrt(D / mu) * k
            f = w / (2.0 * math.pi)
            # Prefer drive near antinode of (m,n): a/(2m) offsets, avoid edges
            x = a_m * (0.5 / m)
            y = b_m * (0.5 / n)
            if m == 1 and n == 1:
                x, y = 0.5 * a_m, 0.35 * b_m  # LF seed: lower third
            if m == 2 and n == 1:
                x, y = 0.55 * a_m, 0.68 * b_m  # WB seed
            modes.append({
                "m": m, "n": n, "f_hz": round(f, 2),
                "antinode_seed_xy_mm": [round(x * 1000, 1), round(y * 1000, 1)],
            })
    modes.sort(key=lambda z: z["f_hz"])
    return modes, D, mu


def main() -> None:
    p = json.loads(PARAMS.read_text())
    panel = p["panel"]
    a = panel["aperture_width_mm"] / 1000.0
    b = panel["aperture_height_mm"] / 1000.0
    h = panel["thickness_mm"] / 1000.0
    E = panel["young_gpa_nominal"] * 1e9
    nu = panel["poisson"]
    rho = panel["areal_density_kg_m2_nominal"] / h
    modes, D, mu = plate_modes(a, b, h, E, nu, rho)
    f1 = modes[0]["f_hz"]
    # Gate: first mode should not sit as an undamped peak in 80–400 Hz without plan
    warnings = []
    if f1 < 40:
        warnings.append("f1 very low — check hanging/compliance model")
    if 80 <= f1 <= 400:
        warnings.append("f1 in mid-bass — damping and DSP peaking EQ mandatory")
    lf = next(m for m in modes if m["m"] == 1 and m["n"] == 1)
    wb = next(m for m in modes if m["m"] == 2 and m["n"] == 1)
    report = {
        "model": "Kirchhoff thin plate, simply supported, uniform orthotropy approximated as isotropic",
        "not_a_measurement": True,
        "not_full_fea": True,
        "inputs": {
            "aperture_mm": [panel["aperture_width_mm"], panel["aperture_height_mm"]],
            "thickness_mm": panel["thickness_mm"],
            "E_gpa": panel["young_gpa_nominal"],
            "nu": nu,
            "areal_density_kg_m2": panel["areal_density_kg_m2_nominal"],
            "derived_bulk_density_kg_m3": round(rho, 1),
            "flexural_rigidity_N_m": D,
        },
        "modes_hz": modes[:12],
        "exciter_seeds_mm": {
            "EX_LF": lf["antinode_seed_xy_mm"],
            "EX_WB": wb["antinode_seed_xy_mm"],
        },
        "gates": {
            "f1_hz": f1,
            "warnings": warnings,
            "damping_loss_factor_required": panel["damping_loss_factor"],
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    # Sync seeds into params if still TBD-style
    p["exciters"]["lf"]["target_xy_mm"] = report["exciter_seeds_mm"]["EX_LF"]
    p["exciters"]["wb"]["target_xy_mm"] = report["exciter_seeds_mm"]["EX_WB"]
    p["exciters"]["seed_source"] = "tools/dml_panel_modal_rev_e.py"
    PARAMS.write_text(json.dumps(p, indent=2) + "\n")
    print(f"wrote {OUT}")
    print(f"f1={f1} Hz; LF seed={report['exciter_seeds_mm']['EX_LF']}; WB seed={report['exciter_seeds_mm']['EX_WB']}")
    for w in warnings:
        print("WARN:", w)


if __name__ == "__main__":
    main()
