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
    cavity_h = H - bay_h - wall
    bay_clear = bay_h - wall
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
    gates.append(gate("frame STEP and STL exist", stl.is_file() and step.is_file() and stl.stat().st_size > 1000, f"stl={stl.stat().st_size if stl.is_file() else 0}"))

    # Published Satellite1 firmware (speaker.yaml, 2026-11): I2S dout is GPIO9
    # into the on-board DAC proxy. External audio is the PCM5122 line-out.
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
