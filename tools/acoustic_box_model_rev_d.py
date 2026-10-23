#!/usr/bin/env python3
"""Lumped box model for the AudioPicture Rev.D mono two-way.

One Dayton ND91-4 and two ND90-PR in one sealed volume, wall-mounted
(half-space radiation), small-signal, manufacturer Thiele-Small data.
This is a model, not a measurement and not an in-room response.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np

RHO = 1.204
C_AIR = 343.2
P_REF = 20e-6
SQRT2 = math.sqrt(2.0)

WOOFER = {
    "name": "Dayton Audio ND91-4",
    "re": 4.3, "le": 0.83e-3, "bl": 4.59, "mms": 4.8e-3, "cms": 0.96e-3,
    "qms": 4.24, "fs": 74.0, "sd": 30.4e-4, "xmax": 4.6e-3,
    "p_rated_w": 30.0, "z_nominal": 4.0,
}
PASSIVE = {
    "name": "Dayton Audio ND90-PR",
    "mmp": 8.1e-3, "cmp": 1.09e-3, "rmp": 0.44, "sd": 31.2e-4,
    "xmax": 9.0e-3, "supplied_disk_kg": 7.3e-3, "supplied_disks": 2,
    "count": 2,
}
# Box losses: leakage Q referred to 50 Hz. Stuffing is not credited with extra volume.
QL = 7.0
QL_REFERENCE_HZ = 50.0


def net_volume() -> dict:
    """Net driver air from the Rev.D 84 mm stack. All values in mm / litres."""
    outer = (320.0, 400.0, 84.0)
    side_wall = 10.0
    baffle_face_z = 1.5 + 12.2
    baffle = 12.0
    rear_wall = 5.0
    inner_w = outer[0] - 2 * side_wall
    inner_h = outer[1] - 2 * side_wall
    inner_d = outer[2] - rear_wall - (baffle_face_z + baffle)
    gross = inner_w * inner_h * inner_d * 1e-6
    deductions = {
        "sealed_electronics_pocket_300x70": inner_w * 70.0 * inner_d * 1e-6,
        "two_vertical_braces_10x360": 2 * 10.0 * 360.0 * inner_d * 1e-6,
        "hanger_and_cable_recess": 0.20,
        "driver_bodies_inside_box": 0.25,
    }
    net = gross - sum(deductions.values())
    return {
        "inner_mm": [inner_w, inner_h, round(inner_d, 2)],
        "gross_l": round(gross, 3),
        "deductions_l": {k: round(v, 3) for k, v in deductions.items()},
        "net_l": round(net, 3),
        "magnet_to_rear_wall_mm": round(outer[2] - rear_wall - (baffle_face_z + 61.0), 2),
    }


def solve(f: np.ndarray, vb_l: float, m_add_kg: float, volts: float = 1.0) -> dict:
    w = 2 * math.pi * f
    s = 1j * w
    wf, pr = WOOFER, PASSIVE
    rms = 2 * math.pi * wf["fs"] * wf["mms"] / wf["qms"]
    zmd = s * wf["mms"] + rms + 1 / (s * wf["cms"])
    ze = wf["re"] + s * wf["le"]
    zmp = s * (pr["mmp"] + m_add_kg) + pr["rmp"] + 1 / (s * pr["cmp"])
    cab = vb_l * 1e-3 / (RHO * C_AIR ** 2)
    ral = QL / (2 * math.pi * QL_REFERENCE_HZ * cab)
    yt = s * cab + 1 / ral + pr["count"] * pr["sd"] ** 2 / zmp
    zm_total = zmd + wf["sd"] ** 2 / yt
    i = volts / (ze + wf["bl"] ** 2 / zm_total)
    vd = wf["bl"] * i / zm_total
    p_box = -wf["sd"] * vd / yt
    vp = p_box * pr["sd"] / zmp
    u_total = -s * cab * p_box
    p_far = s * RHO * u_total / (2 * math.pi * 1.0)
    return {
        "spl": 20 * np.log10(np.abs(p_far) / P_REF),
        "x_woofer_peak": np.abs(vd) / w * SQRT2,
        "x_passive_peak": np.abs(vp) / w * SQRT2,
        "z": np.abs(volts / i),
    }


REFERENCE_BAND_HZ = (150.0, 400.0)
EQ_BAND_HZ = (55.0, 300.0)
MAX_DSP_BOOST_DB = 6.0


def reference(f: np.ndarray, spl: np.ndarray) -> float:
    band = (f >= REFERENCE_BAND_HZ[0]) & (f <= REFERENCE_BAND_HZ[1])
    return float(np.mean(spl[band]))


def metrics(f: np.ndarray, r: dict) -> dict:
    ref = reference(f, r["spl"])
    below = np.where(f <= 300)[0]

    def corner(drop: float):
        for k in below[::-1]:
            if r["spl"][k] <= ref - drop:
                return round(float(f[k]), 1)
        return None

    low = (f >= 20) & (f <= 300)
    return {
        "reference_spl_db_2v83": round(ref + 20 * math.log10(2.83), 2),
        "f3_hz": corner(3.0),
        "f6_hz": corner(6.0),
        "f10_hz": corner(10.0),
        "ripple_above_reference_db": round(float(np.max(r["spl"][low]) - ref), 2),
    }


def max_spl(f: np.ndarray, r: dict) -> np.ndarray:
    v_rated = math.sqrt(WOOFER["p_rated_w"] * WOOFER["z_nominal"])
    v_lim = np.minimum.reduce([
        np.full_like(f, v_rated),
        WOOFER["xmax"] / r["x_woofer_peak"],
        PASSIVE["xmax"] / r["x_passive_peak"],
    ])
    return r["spl"] + 20 * np.log10(v_lim), v_lim


def at(f: np.ndarray, values: np.ndarray, hz: float) -> float:
    return float(np.interp(hz, f, values))


def equalized(f: np.ndarray, r: dict) -> tuple[float, float]:
    """Flat level reachable across EQ_BAND_HZ and the boost that flatness needs."""
    band = (f >= EQ_BAND_HZ[0]) & (f <= EQ_BAND_HZ[1])
    spl_max, _ = max_spl(f, r)
    ref_1v = reference(f, r["spl"])
    boost = float(np.max(ref_1v - r["spl"][band]))
    return float(np.min(spl_max[band])), boost


FS = 48000.0
CROSSOVER_HZ = 3000.0
SUBSONIC_HZ = 45.0
BUTTERWORTH4_Q = (0.5411961, 1.3065630)
TWEETER_SENSITIVITY_2V83 = 90.0
EQ_STAGES = 3
EQ_GAIN_LIMIT_DB = 6.0
# A lossless Le overstates the ND91 treble droop; above this the bench curve has authority.
MODEL_VALID_TO_HZ = 500.0


def rbj(kind: str, f0: float, q: float, gain_db: float = 0.0) -> tuple[list[float], list[float]]:
    """RBJ cookbook biquad normalized by a0; must match ap_biquad_* in firmware."""
    w0 = 2 * math.pi * f0 / FS
    cw, alpha = math.cos(w0), math.sin(w0) / (2 * q)
    if kind == "lowpass":
        b, a = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2], [1 + alpha, -2 * cw, 1 - alpha]
    elif kind == "highpass":
        b, a = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2], [1 + alpha, -2 * cw, 1 - alpha]
    elif kind == "peaking":
        amp = 10 ** (gain_db / 40)
        b = [1 + alpha * amp, -2 * cw, 1 - alpha * amp]
        a = [1 + alpha / amp, -2 * cw, 1 - alpha / amp]
    else:
        raise ValueError(kind)
    return [x / a[0] for x in b], [1.0, a[1] / a[0], a[2] / a[0]]


def biquad_db(coeffs: tuple[list[float], list[float]], f: np.ndarray) -> np.ndarray:
    b, a = coeffs
    z = np.exp(-1j * 2 * math.pi * f / FS)
    h = (b[0] + b[1] * z + b[2] * z ** 2) / (a[0] + a[1] * z + a[2] * z ** 2)
    return 20 * np.log10(np.abs(h))


def subsonic_db(f: np.ndarray) -> np.ndarray:
    return sum(biquad_db(rbj("highpass", SUBSONIC_HZ, q), f) for q in BUTTERWORTH4_Q)


def woofer_lowpass_db(f: np.ndarray) -> np.ndarray:
    return 2 * biquad_db(rbj("lowpass", CROSSOVER_HZ, math.sqrt(0.5)), f)


def fit_eq(f: np.ndarray, deviation: np.ndarray) -> list[dict]:
    """Greedy minimax fit of peaking filters to a dB deviation curve."""
    centres = np.geomspace(40, 300, 48)
    qs = np.geomspace(0.4, 4.0, 14)
    gains = np.arange(-EQ_GAIN_LIMIT_DB, EQ_GAIN_LIMIT_DB + 0.01, 0.25)
    residual = deviation.copy()
    total = np.zeros_like(f)
    chosen = []
    for _ in range(EQ_STAGES):
        start = float(np.max(np.abs(residual)))
        best = (start, None, None)
        for f0 in centres:
            for q in qs:
                for g in gains:
                    if g == 0:
                        continue
                    shape = biquad_db(rbj("peaking", f0, q, g), f)
                    if float(np.max(total + shape)) > EQ_GAIN_LIMIT_DB:
                        continue
                    err = float(np.max(np.abs(residual - shape)))
                    if err < best[0]:
                        best = (err, {"hz": round(float(f0), 2), "q": round(float(q), 4),
                                      "gain_db": round(float(g), 2)}, shape)
        if best[1] is None or start - best[0] < 0.2:
            break
        chosen.append(best[1])
        residual = residual - best[2]
        total = total + best[2]
    return chosen


def low_band_design(f: np.ndarray, r: dict) -> dict:
    ref_1v = reference(f, r["spl"])
    band = (f >= EQ_BAND_HZ[0]) & (f <= EQ_BAND_HZ[1])
    pre_eq = r["spl"] + subsonic_db(f)
    eq = fit_eq(f[band], ref_1v - pre_eq[band])
    eq_db = sum((biquad_db(rbj("peaking", e["hz"], e["q"], e["gain_db"]), f) for e in eq),
                np.zeros_like(f))
    filters = subsonic_db(f) + eq_db + woofer_lowpass_db(f)
    response = r["spl"] + filters
    _, v_lim = max_spl(f, r)
    span = (f >= 20) & (f <= 1500)
    # Largest digital gain G (dB re 1 V) that keeps every frequency inside Xmax and rating.
    g_max = float(np.min(20 * np.log10(v_lim[span]) - filters[span]))
    level = float(np.mean((response + g_max)[(f >= REFERENCE_BAND_HZ[0]) & (f <= REFERENCE_BAND_HZ[1])]))
    window = (f >= 55) & (f <= MODEL_VALID_TO_HZ)
    dev = response[window] - ref_1v
    limiting_hz = float(f[span][np.argmin(20 * np.log10(v_lim[span]) - filters[span])])
    tweeter_pad = (ref_1v + 20 * math.log10(2.83)) - TWEETER_SENSITIVITY_2V83
    f3 = None
    for k in np.where(f <= 300)[0][::-1]:
        if response[k] <= ref_1v - 3:
            f3 = round(float(f[k]), 1)
            break
    return {
        "sample_rate_hz": FS,
        "subsonic": {"type": "butterworth4", "hz": SUBSONIC_HZ, "q": list(BUTTERWORTH4_Q)},
        "crossover": {"type": "linkwitz_riley4", "hz": CROSSOVER_HZ},
        "eq": eq,
        "max_eq_boost_db": round(float(np.max(eq_db[band])), 2),
        "woofer_response_55_500hz_db": [round(float(dev.min()), 2), round(float(dev.max()), 2)],
        "model_valid_to_hz": MODEL_VALID_TO_HZ,
        "f3_after_dsp_hz": f3,
        "max_level_1m_db_reference_band": round(level, 1),
        "max_level_limited_at_hz": round(limiting_hz, 1),
        "tweeter_pad_db": round(tweeter_pad, 2),
        "tweeter_not_modeled": True,
    }


def c_header(design: dict) -> str:
    lines = [
        "/* Generated by tools/acoustic_box_model_rev_d.py. Model-derived starting curve:",
        " * not a factory measurement. The bench curve replaces it. */",
        "#ifndef AP_MODEL_CURVE_REV_D_H",
        "#define AP_MODEL_CURVE_REV_D_H",
        f"#define AP_MODEL_SAMPLE_RATE_HZ {design['sample_rate_hz']:.1f}",
        f"#define AP_MODEL_CROSSOVER_HZ {design['crossover']['hz']:.1f}",
        f"#define AP_MODEL_SUBSONIC_HZ {design['subsonic']['hz']:.1f}",
        f"#define AP_MODEL_TWEETER_PAD_DB ({design['tweeter_pad_db']:.2f})",
        f"#define AP_MODEL_EQ_COUNT {len(design['eq'])}u",
        "static const struct { double hz, q, gain_db; } ap_model_eq_rev_d[] = {",
    ]
    lines += [f"    {{{e['hz']:.2f}, {e['q']:.4f}, {e['gain_db']:.2f}}}," for e in design["eq"]]
    lines += ["};", "#endif", ""]
    return "\n".join(lines)


def run(vb_l: float) -> dict:
    f = np.geomspace(15, 3000, 4000)
    candidates = []
    for m_add_g in np.arange(0.0, 40.01, 0.1):
        r = solve(f, vb_l, m_add_g * 1e-3)
        flat_max, boost = equalized(f, r)
        if boost <= MAX_DSP_BOOST_DB:
            candidates.append((flat_max, round(float(m_add_g), 1), boost))
    flat_max, m_best, boost = max(candidates)
    r = solve(f, vb_l, m_best * 1e-3)
    k_best = metrics(f, r)
    spl_max, v_lim = max_spl(f, r)
    probe = [40, 45, 50, 55, 60, 70, 80, 100, 150, 200, 500, 1000]
    raw_1v = r["spl"]
    woofer_band = (f >= 100) & (f <= 1500)
    unloaded = solve(f, vb_l, 0.0)
    one_disk = solve(f, vb_l, PASSIVE["supplied_disk_kg"])
    one_disk_flat, one_disk_boost = equalized(f, one_disk)
    return {
        "net_volume_l": vb_l,
        "passive_added_mass_g_each": m_best,
        "passive_added_mass_vs_supplied_disks_g": round(
            m_best - PASSIVE["supplied_disk_kg"] * PASSIVE["supplied_disks"] * 1e3, 1),
        "raw_alignment": k_best,
        "raw_alignment_without_added_mass": metrics(f, unloaded),
        "min_impedance_ohm_20_3000hz": round(float(np.min(r["z"][f >= 20])), 2),
        "eq_band_hz": list(EQ_BAND_HZ),
        "dsp_boost_needed_db": round(boost, 2),
        "flat_max_spl_1m_db_over_eq_band": round(flat_max, 1),
        "max_spl_1m_db": {str(h): round(at(f, spl_max, h), 1) for h in probe},
        "max_spl_limit": {
            str(h): ("voltage" if at(f, v_lim, h) >= math.sqrt(30 * 4) - 1e-6 else "excursion")
            for h in probe
        },
        "woofer_band_min_max_spl_100_1500hz_db": round(float(np.min(spl_max[woofer_band])), 1),
        "voltage_rms_for_90db_at_100hz": round(10 ** ((90 - at(f, raw_1v, 100.0)) / 20), 2),
        "build_option_one_supplied_disk_each": {
            "added_mass_g": PASSIVE["supplied_disk_kg"] * 1e3,
            "flat_max_spl_1m_db_over_eq_band": round(one_disk_flat, 1),
            "dsp_boost_needed_db": round(one_disk_boost, 2),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parents[1] / "evidence/rev-d/box-model.json")
    parser.add_argument("--header", type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parents[1]
                        / "firmware/components/room_audio/include/ap_model_curve_rev_d.h")
    args = parser.parse_args()
    geometry = net_volume()
    nominal = run(geometry["net_l"])
    f = np.geomspace(15, 3000, 4000)
    build = solve(f, geometry["net_l"], PASSIVE["supplied_disk_kg"])
    design = low_band_design(f, build)
    design["passive_added_mass_g_each"] = PASSIVE["supplied_disk_kg"] * 1e3
    nominal["dsp_design_one_supplied_disk"] = design
    args.header.parent.mkdir(parents=True, exist_ok=True)
    args.header.write_text(c_header(design))
    sensitivity = {f"{v:.1f}": run(v) for v in (2.5, 3.0, 3.5, 4.5)}
    result = {
        "model": "lumped sealed box + two passive radiators, half-space 2pi at 1 m, small signal",
        "not_a_measurement": True,
        "woofer": WOOFER, "passive": PASSIVE,
        "box_losses": {"ql": QL, "referred_to_hz": QL_REFERENCE_HZ},
        "selection": {
            "reference_band_hz": list(REFERENCE_BAND_HZ),
            "rule": "maximize the flat SPL reachable over the EQ band, limited by woofer Xmax, "
                    "passive Xmax and the 30 W rated voltage, with DSP boost <= 6 dB",
        },
        "geometry": geometry,
        "nominal": nominal,
        "volume_sensitivity": sensitivity,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"geometry": geometry, "dsp_design": design,
                      "sensitivity": {k: {"mass_g": v["passive_added_mass_g_each"],
                                          "flat_max_db": v["flat_max_spl_1m_db_over_eq_band"],
                                          "boost_db": v["dsp_boost_needed_db"]}
                                      for k, v in sensitivity.items()}},
                     indent=2))


if __name__ == "__main__":
    main()
