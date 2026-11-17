#!/usr/bin/env python3
"""Digital production checks for the frozen Rev.G configuration.

Writes evidence/rev-g/production-verification.json. A PASS here is not a
license to ship: acoustic, I2S-or-jack, and pilot gates stay external.
"""
from __future__ import annotations
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARAMS = ROOT / "mechanical/rev-g/rev_g_params.json"
OUT = ROOT / "evidence/rev-g/production-verification.json"


def gate(name: str, ok: bool, detail: str) -> dict:
    return {"gate": name, "result": "PASS" if ok else "FAIL", "detail": detail}


def main() -> int:
    p = json.loads(PARAMS.read_text())
    W, H, D = p["body_mm"]
    wall, rear, lip = p["wall_mm"], p["rear_skin_mm"], p["front_lip_mm"]
    bay_h = p["bay_height_mm"]
    pw, ph, pt = p["panel_mm"]
    panel_z = p["panel_z_mm"]
    stack = p["stack_mm"]
    lf, wb = p["exciters"]["lf"], p["exciters"]["wb"]
    hat = p["electronics"]["hat_mm"]
    core = p["electronics"]["core_mm"]
    gates = []

    total = round(sum(stack[k] for k in ("rear_skin", "clearance_behind_teax", "teax_depth", "panel", "cloth")), 3)
    gates.append(gate("stack sums to 30.0 mm", abs(total - 30.0) < 0.05 and D == 30, f"sum={total}"))
    gates.append(gate(
        "TEAX clears the rear skin",
        panel_z - lf["depth_mm"] > rear and abs((panel_z - wb["depth_mm"]) - (rear + stack["clearance_behind_teax"])) < 0.05,
        f"TEAX back face Z={panel_z - wb['depth_mm']}, skin inner Z={rear}",
    ))
    bay_clear = bay_h - wall
    cavity_bottom = -H / 2 + wall + bay_clear + wall
    cavity_top_design = H / 2 - wall
    cavity_h = cavity_top_design - cavity_bottom
    bay_w = W - 2 * wall
    gates.append(gate(
        "panel fits the acoustic cavity",
        pw < bay_w and ph < cavity_h and panel_z + pt <= D - lip + 0.01,
        f"panel {pw}x{ph} cavity {bay_w}x{cavity_h} front Z={panel_z + pt}",
    ))
    gates.append(gate(
        "HAT and Core fit the bay side by side",
        hat[0] <= bay_clear - 4 and hat[1] <= bay_w and core[0] + hat[0] + 6 <= bay_w and core[1] <= bay_clear,
        f"bay interior {bay_w:.0f}x{bay_clear:.0f}, HAT {hat[0]}x{hat[1]}, Core {core[0]}x{core[1]}",
    ))
    gates.append(gate(
        "boards are thinner than the bay",
        hat[2] < (D - rear - lip) and core[2] < (D - rear - lip),
        f"bay depth {D - rear - lip:.1f} mm",
    ))

    def inside(part, half_x, half_y, margin=3.0):
        x, y = part["on_panel_mm_from_lower_left"]
        return margin + half_x <= x <= pw - half_x - margin and margin + half_y <= y <= ph - half_y - margin

    lf_r = lf["diameter_mm"] / 2
    wb_hx, wb_hy = wb["footprint_mm"][0] / 2, wb["footprint_mm"][1] / 2
    gates.append(gate("bass exciter footprint inside the panel", inside(lf, lf_r, lf_r), str(lf["on_panel_mm_from_lower_left"])))
    gates.append(gate("TEAX footprint inside the panel", inside(wb, wb_hx, wb_hy), str(wb["on_panel_mm_from_lower_left"])))
    dx = lf["on_panel_mm_from_lower_left"][0] - wb["on_panel_mm_from_lower_left"][0]
    dy = lf["on_panel_mm_from_lower_left"][1] - wb["on_panel_mm_from_lower_left"][1]
    dist = math.hypot(dx, dy)
    gates.append(gate("exciters do not overlap", dist > lf_r + max(wb_hx, wb_hy) + 5, f"centre distance {dist:.1f} mm"))
    gates.append(gate(
        "bass exciter is the shallower motor",
        lf["depth_mm"] <= 16 and wb["depth_mm"] == 19 and lf["impedance_ohm"] == 4 and wb["impedance_ohm"] == 8,
        f"LF {lf['depth_mm']} mm {lf['impedance_ohm']} ohm, WB {wb['depth_mm']} mm {wb['impedance_ohm']} ohm",
    ))

    stl = ROOT / "mechanical/rev-g/cad/AP-G-FRAME.stl"
    step = ROOT / "mechanical/rev-g/cad/AP-G-FRAME.step"
    manifest = ROOT / "mechanical/rev-g/cad/manifest.json"
    gates.append(gate("frame STEP and STL exist", stl.is_file() and step.is_file() and stl.stat().st_size > 1000, f"stl={stl.stat().st_size if stl.is_file() else 0}"))
    meta = json.loads(manifest.read_text()) if manifest.is_file() else {}
    cavity_top = (meta.get("cavity_y_mm") or [None, None])[1]
    envelope = meta.get("envelope_mm") or [0, 0, 0]
    gates.append(gate(
        "top wall stays inside the outline",
        cavity_top is not None and abs(cavity_top - cavity_top_design) < 0.05 and all(abs(a - b) < 0.05 for a, b in zip(envelope, (W, H, D))),
        f"cavity top Y={cavity_top}, envelope={envelope}",
    ))
    power = p["electronics"].get("power", "")
    gates.append(gate(
        "power text names the analog amplifier",
        "TAS5825M" not in power and p["amplifier"]["part"].startswith("stereo analog"),
        power,
    ))
    try:
        import cadquery as cq
        frame = cq.importers.importStep(str(step))
        shape = frame.val()
        skin = [(x, y, z) for x in (-120, 0, 120) for y in (196.8, 198.8) for z in (0.5, 8, 16, 24, 29)]
        closed = all(shape.isInside(pt) for pt in skin) and not shape.isInside((0, 190, 10))
        throat = not shape.isInside((148, 182, 2)) and not shape.isInside((-148, 182, 2))
        gates.append(gate("top wall is closed", closed and throat, f"sampled {len(skin)} points in the top skin; both keyholes open"))
        shape_probe = shape
    except Exception as exc:
        shape_probe = None
        gates.append(gate("top wall is closed", False, f"STEP probe failed: {exc}"))

    # Published Satellite1 firmware (speaker.yaml, 2026-11): I2S dout is GPIO9
    # into the on-board DAC proxy. External audio is the PCM5122 line-out.
    touch = p.get("volume_touch") or {}
    zones = touch.get("zones") or []
    bay_top = -H / 2 + wall + bay_clear
    bay_bottom = -H / 2 + wall
    hat_cx = -W / 2 + wall + 4 + hat[0] / 2
    by = -H / 2 + wall + bay_clear / 2
    radar = (hat_cx, by, 16, 46)
    mics = [(hat_cx + dx, bay_top - 6, 6, 3) for dx in (-30, -10, 10, 30)]

    def overlaps(a, b, gap=3.0):
        ax, ay, aw, ah = a
        bx, by_, bw, bh = b
        return abs(ax - bx) < (aw + bw) / 2 + gap and abs(ay - by_) < (ah + bh) / 2 + gap

    pads_ok = (
        len(zones) == 2
        and zones[0]["id"] == "vol_down" and zones[0]["center_mm"][0] < 0
        and zones[1]["id"] == "vol_up" and zones[1]["center_mm"][1] == zones[0]["center_mm"][1]
        and zones[1]["center_mm"][0] == -zones[0]["center_mm"][0]
        and 0 < touch.get("pocket_depth_mm", 0) < lip
    )
    for zone in zones:
        zx, zy = zone["center_mm"]
        zw, zh = zone["size_mm"]
        pads_ok = pads_ok and bay_bottom + 2 + zh / 2 <= zy <= bay_top - 2 - zh / 2
        pads_ok = pads_ok and -W / 2 + wall + 2 + zw / 2 <= zx <= W / 2 - wall - 2 - zw / 2
        pads_ok = pads_ok and not overlaps((zx, zy, zw, zh), radar)
        pads_ok = pads_ok and not any(overlaps((zx, zy, zw, zh), mic) for mic in mics)
    gates.append(gate(
        "volume pads sit under the cloth on the bay",
        pads_ok,
        "left tap lowers, right tap raises, clear of radar, mics and the sounding panel",
    ))
    if shape_probe is None:
        gates.append(gate("volume pockets do not pierce the front skin", False, "no STEP shape"))
    else:
        recess_ok = True
        for zone in zones:
            zx, zy = zone["center_mm"]
            recess_ok = recess_ok and shape_probe.isInside((zx, zy, D - lip + touch["pocket_depth_mm"] + 0.4))
            recess_ok = recess_ok and not shape_probe.isInside((zx, zy, D - lip + touch["pocket_depth_mm"] / 2))
        gates.append(gate(
            "volume pockets do not pierce the front skin",
            recess_ok,
            f"remaining skin {lip - touch.get('pocket_depth_mm', 0):.1f} mm",
        ))

    psu = p["electronics"]["psu"]["size_mm"]
    amp = p["electronics"]["amp_max_mm"]
    bay_depth = D - rear - lip
    core_right = hat_cx + hat[0] / 2 + 6 + core[0]
    psu_left = core_right + 4
    psu_right = psu_left + psu[0]
    amp_left = psu_right + 4
    amp_right = amp_left + amp[0]
    bay_left = -W / 2 + wall
    bay_right = W / 2 - wall
    supply_ok = (
        psu[2] < bay_depth and amp[2] < bay_depth
        and psu[1] < bay_clear - 4 and amp[1] < bay_clear - 4
        and bay_left + 2 <= psu_left and amp_right <= bay_right - 2
        and "IRM-30-24" in p["electronics"]["psu"]["part"]
    )
    gates.append(gate(
        "one 24 V supply fits beside the Core",
        supply_ok,
        f"IRM-30-24 ends at X={psu_right:.0f}, amplifier ends at X={amp_right:.0f}, bay edge X={bay_right:.0f}",
    ))

    audio = p.get("audio_path")
    gates.append(gate(
        "audio path matches the published kit firmware",
        audio == "pcm5122-line-out",
        "GPIO9 I2S feeds the onboard TAS2780/PCM5122. An external TAS5825M I2S tap is not a documented port.",
    ))

    failed = [g for g in gates if g["result"] != "PASS"]
    report = {
        "configuration": "Rev.G",
        "digital_result": "PASS" if not failed else "FAIL",
        "production_release": "BLOCKED",
        "blocked_by": [
            "First-article acoustic measurement against the pass bars in the frozen spec",
            "Line-out level and channel assignment confirmed on a real Dev Kit",
            "Pilot of at least one assembled frame, not a released lot",
            "Volume-button contact confirmed active-low to ground before the touch output shares it",
        ],
        "gates": gates,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    for g in gates:
        print(f"{g['result']:4} {g['gate']}: {g['detail']}")
    print("digital", report["digital_result"], "release", report["production_release"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
