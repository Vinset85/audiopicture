#!/usr/bin/env python3
"""P1 printed-cabinet acoustic screen: wall modes, wall compliance and leakage.

Analytical plate models (Kirchhoff, clamped bays, smeared-rib orthotropic plate).
They rank wall constructions; they do not replace FEA or an accelerometer scan.
Writes evidence/p1/printed-cabinet-acoustics.json.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

RHO_AIR, C_AIR = 1.204, 343.0
MATERIALS = {
    # E [Pa], density [kg/m3], Poisson, loss factor; printed-part values, conservative
    "PA12_SLS": {"E": 1.65e9, "rho": 1000.0, "nu": 0.40, "eta": 0.03,
                 "source": "EOS PA 2200 / HP PA12 datasheets, tensile modulus 1.65-1.8 GPa"},
    "ASA_FDM_100pct": {"E": 1.9e9, "rho": 1070.0, "nu": 0.35, "eta": 0.02,
                       "source": "Polymaker ASA XY modulus 2.38 GPa derated 20 percent for Z/raster"},
    "MDF_reference": {"E": 3.5e9, "rho": 750.0, "nu": 0.25, "eta": 0.04,
                      "source": "typical loudspeaker MDF"},
}
# Clamped rectangular plate fundamental: lambda^2 coefficients (Leissa) by aspect ratio a/b.
CLAMPED = [(1.0, 35.99), (1.5, 27.01), (2.0, 24.57), (2.5, 23.77), (3.0, 23.18)]

def lam2_clamped(a: float, b: float) -> float:
    r = max(a, b) / min(a, b)
    for (r0, l0), (r1, l1) in zip(CLAMPED, CLAMPED[1:]):
        if r <= r1:
            return l0 + (l1 - l0) * (r - r0) / (r1 - r0)
    return CLAMPED[-1][1]

def plate_D(E, nu, h):
    return E * h ** 3 / (12 * (1 - nu ** 2))

def clamped_f1(D, m_area, a, b):
    short = min(a, b)
    return lam2_clamped(a, b) / (2 * math.pi * short ** 2) * math.sqrt(D / m_area)

def clamped_volume_compliance(D, a, b):
    """dV/dp of a clamped plate, uniform pressure. Square: w_max = 0.00126 p a^4/D,
    mean/max deflection about 0.28. Long bays use the short span."""
    short = min(a, b)
    w_max = 0.00126 * short ** 4 / D
    return 0.28 * w_max * a * b

def ribbed_plate(mat, skin, rib_w, rib_h, pitch):
    """Smeared T-section stiffness per unit width, ribs both directions."""
    E, nu = mat["E"], mat["nu"]
    # section per pitch: skin pitch x skin + rib rib_w x rib_h below
    A1, y1 = pitch * skin, skin / 2
    A2, y2 = rib_w * rib_h, skin + rib_h / 2
    yc = (A1 * y1 + A2 * y2) / (A1 + A2)
    I = (pitch * skin ** 3 / 12 + A1 * (y1 - yc) ** 2 + rib_w * rib_h ** 3 / 12 + A2 * (y2 - yc) ** 2)
    D = E * I / pitch / (1 - nu ** 2)
    m_area = mat["rho"] * (skin + 2 * rib_w * rib_h / pitch)
    return D, m_area

def wall_report(name, mat, a, b, skin, rib_w, rib_h, pitch, ties=(1, 1)):
    """ties=(nx, ny): rear-to-baffle tie columns split the wall into nx*ny clamped panels."""
    a, b = a / ties[0], b / ties[1]
    D_skin = plate_D(mat["E"], mat["nu"], skin)
    m_skin = mat["rho"] * skin
    if rib_h > 0:
        D_glob, m_glob = ribbed_plate(mat, skin, rib_w, rib_h, pitch)
        bay = pitch - rib_w
        nx, ny = max(1, round(a / pitch)), max(1, round(b / pitch))
        f_bay = clamped_f1(D_skin, m_skin, bay, bay)
        c_bays = nx * ny * clamped_volume_compliance(D_skin, bay, bay)
    else:
        D_glob, m_glob, f_bay, c_bays = D_skin, m_skin, None, 0.0
    f_glob = clamped_f1(D_glob, m_glob, a, b)
    c_glob = ties[0] * ties[1] * clamped_volume_compliance(D_glob, a, b)
    c_bays *= ties[0] * ties[1]
    return {"wall": name, "ties": list(ties), "span_mm": [round(a * 1e3, 1), round(b * 1e3, 1)], "skin_mm": skin * 1e3,
            "rib_mm": [rib_w * 1e3, rib_h * 1e3, pitch * 1e3] if rib_h else None,
            "f1_global_hz": round(f_glob), "f1_bay_hz": round(f_bay) if f_bay else None,
            "volume_compliance_m3_per_pa": c_glob + c_bays,
            "mass_kg_per_m2": round(m_glob, 2)}

def main():
    vb = 4.0e-3
    c_box = vb / (RHO_AIR * C_AIR ** 2)
    a, b = 0.300, 0.380  # rear wall / baffle interior spans
    side = (0.380, 0.0533)
    cases = []
    for mat_name, skin, rib, ties, baffle_h in [
        ("MDF_reference", 0.012, (0, 0, 0), (1, 1), 0.012),
        ("PA12_SLS", 0.005, (0, 0, 0), (1, 1), 0.012),
        ("PA12_SLS", 0.006, (0.004, 0.010, 0.060), (1, 1), 0.012),
        ("PA12_SLS", 0.006, (0.004, 0.010, 0.060), (2, 3), 0.012),
        ("PA12_SLS", 0.006, (0.004, 0.010, 0.060), (3, 3), 0.012),
        ("ASA_FDM_100pct", 0.006, (0.004, 0.010, 0.060), (3, 3), 0.012),
    ]:
        mat = MATERIALS[mat_name]
        rear = wall_report("rear", mat, a, b, skin, *rib, ties=ties)
        baffle = wall_report("baffle", mat, a, b, baffle_h, 0, 0, 0, ties=ties)
        sidew = wall_report("side", mat, side[0], side[1], 0.010, 0, 0, 0)
        total_c = (rear["volume_compliance_m3_per_pa"] + baffle["volume_compliance_m3_per_pa"]
                   + 4 * sidew["volume_compliance_m3_per_pa"])
        cases.append({"material": mat_name, "rear_and_baffle": rear, "baffle_solid": baffle, "side_10mm": sidew,
                      "wall_to_air_compliance_percent": round(100 * total_c / c_box, 3),
                      "loss_factor": mat["eta"]})
    for c in cases:
        for k in ("rear_and_baffle", "baffle_solid", "side_10mm"):
            c[k]["volume_compliance_m3_per_pa"] = float(f"{c[k]['volume_compliance_m3_per_pa']:.3e}")
    # Leakage: QL from equivalent hole; QL = 1/(w Rl Cbox) with an orifice of area A
    leaks = []
    fb = 50.0
    for d_mm in (0.3, 0.5, 1.0, 2.0):
        area = math.pi * (d_mm * 1e-3 / 2) ** 2
        # linearised orifice resistance at 1 m/s particle velocity (turbulent-limit screen)
        r_acoustic = RHO_AIR * 1.0 / (2 * 0.6 ** 2 * area)  # Pa s/m3 per unit velocity scale
        ql = 1 / (2 * math.pi * fb * r_acoustic * c_box)
        leaks.append({"equivalent_hole_mm": d_mm, "ql_at_50hz_screen": round(ql, 1)})
    out = {
        "model": "analytical Kirchhoff plates; clamped bays; smeared ribs; screening only",
        "box_air_compliance_m3_per_pa": float(f"{c_box:.3e}"),
        "net_volume_l": vb * 1e3,
        "materials": MATERIALS,
        "cases": cases,
        "leak_screen": leaks,
        "acceptance": {
            "global_wall_f1_hz_min": 500,
            "bay_f1_hz_min": 2500,
            "wall_to_air_compliance_percent_max": 1.0,
            "pressure_decay_test": "box at +500 Pa, drivers sealed: <=10 percent decay in 10 s",
        },
    }
    path = Path("evidence/p1/printed-cabinet-acoustics.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1) + "\n")
    for c in cases:
        r = c["rear_and_baffle"]
        print(f"{c['material']:16s} skin {r['skin_mm']:.0f} rib {r['rib_mm']} ties {r['ties']}: rear f1 {r['f1_global_hz']} Hz,"
              f" bay {r['f1_bay_hz']} Hz, baffle f1 {c['baffle_solid']['f1_global_hz']} Hz, side {c['side_10mm']['f1_global_hz']} Hz,"
              f" wall/air compliance {c['wall_to_air_compliance_percent']} %, {r['mass_kg_per_m2']} kg/m2")

if __name__ == "__main__":
    main()
