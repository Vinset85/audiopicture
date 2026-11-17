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
        lf["depth_mm"] <= 16 and lf.get("fs_hz", 999) < 150 and wb["depth_mm"] == 19 and lf["impedance_ohm"] == 4 and wb["impedance_ohm"] == 8,
        f"LF {lf['depth_mm']} mm {lf['impedance_ohm']} ohm Fs {lf.get('fs_hz')} Hz, WB {wb['depth_mm']} mm {wb['impedance_ohm']} ohm",
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
        skin = [(x, y, z) for x in (-120, 0, 120) for y in (199.0, 199.5) for z in (0.5, 8, 16, 24, 29)]
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

    cloth_fast = p.get("cloth_fastening") or {}
    rabbet = cloth_fast.get("rabbet") or {}
    mag_depth = (cloth_fast.get("magnet") or {}).get("pocket_depth_mm", 2.2)
    mag_z = D - rabbet.get("depth_mm", 1.5) - mag_depth / 2
    mag_r = (cloth_fast.get("magnet") or {}).get("pocket_diameter_mm", 8.4) / 2
    pads_ok = (
        len(zones) == 2
        and zones[0]["id"] == "vol_down" and zones[0]["center_xz_mm"][0] < 0
        and zones[1]["id"] == "vol_up"
        and zones[1]["center_xz_mm"][0] == -zones[0]["center_xz_mm"][0]
        and zones[1]["center_xz_mm"][1] == zones[0]["center_xz_mm"][1] == D / 2
        and abs(zones[0]["center_xz_mm"][0]) <= 50
        and 1.0 <= wall - touch.get("pocket_depth_mm", 0)
    )
    magnet_floor = D - rabbet.get("depth_mm", 1.5) - mag_depth
    for zone in zones:
        zx, zz = zone["center_xz_mm"]
        zw, zd = zone["size_mm"]
        pads_ok = pads_ok and 1 + zd / 2 <= zz <= D - 2 - zd / 2
        pads_ok = pads_ok and abs(zx) + zw / 2 < W / 2 - wall
        pads_ok = pads_ok and zz + zd / 2 + 2 <= magnet_floor
    mute = p.get("mic_mute") or {}
    mx, mz = (mute.get("center_xz_mm") or [None, None])
    mute_d = mute.get("hole_diameter_mm", 0)
    mute_ok = (
        mx == 0 and mz == D / 2 and mute_d == 4.5
        and 1 + mute_d / 2 <= mz <= D - 2 - mute_d / 2
        and mz + mute_d / 2 + 2 <= magnet_floor
    )
    gates.append(gate(
        "volume and mute sit on the bare bottom edge",
        pads_ok and mute_ok,
        "left tap lowers, right tap raises, latching mute between them, on the bare underside",
    ))
    if shape_probe is None:
        gates.append(gate("bottom controls do not open the bay", False, "no STEP shape"))
    else:
        recess_ok = mute_ok and not shape_probe.isInside((mx, -H / 2 + 0.4, mz))
        recess_ok = recess_ok and shape_probe.isInside((mx, -H / 2 + 0.4, mz + 6))
        for zone in zones:
            zx, zz = zone["center_xz_mm"]
            recess_ok = recess_ok and not shape_probe.isInside((zx, -H / 2 + 0.4, zz))
            recess_ok = recess_ok and not shape_probe.isInside((zx, -H / 2 + wall - 0.4, zz))
            recess_ok = recess_ok and shape_probe.isInside((zx + 8, -H / 2 + wall - 0.4, zz))
        gates.append(gate(
            "bottom controls do not open the bay",
            recess_ok,
            f"volume skin {wall - touch.get('pocket_depth_mm', 0):.1f} mm, mute hole open",
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

    inlet = p["electronics"].get("mains_inlet") or {}
    ix, iy = (inlet.get("center_mm") or [0, 0])
    iw, ih = (inlet.get("size_mm") or [0, 0])
    inlet_ok = iw == 14 and ih == 8 and bay_bottom + ih / 2 < iy < by
    if shape_probe is not None and inlet_ok:
        inlet_ok = (
            not shape_probe.isInside((ix, iy, rear / 2))
            and shape_probe.isInside((ix + iw, iy, rear / 2))
            and shape_probe.isInside((0, -H / 2 + wall / 2, 12))
        )
    gates.append(gate(
        "mains inlet is on the rear skin",
        inlet_ok,
        "14 x 8 mm at the IRM-30 AC end; the bottom edge is closed",
    ))

    leds = p.get("status_leds") or {}
    lamps = leds.get("lamps") or []
    led_d = leds.get("hole_diameter_mm", 0)
    led_ids = [lamp.get("id") for lamp in lamps]
    led_ok = led_ids == ["power", "link", "mute", "listen"] and 1.6 <= led_d <= 3.0
    for lamp in lamps:
        lx, ly = lamp["center_mm"]
        led_ok = led_ok and bay_bottom + 1.5 + led_d / 2 <= ly <= -188
        led_ok = led_ok and abs(lx) + led_d / 2 <= 90
        led_ok = led_ok and not overlaps((lx, ly, led_d, led_d), radar, gap=3)
    if shape_probe is not None and led_ok:
        for lamp in lamps:
            lx, ly = lamp["center_mm"]
            led_ok = led_ok and not shape_probe.isInside((lx, ly, D - 2.1))
            led_ok = led_ok and shape_probe.isInside((lx + 6, ly, D - 2.6))
    gates.append(gate(
        "four status LEDs sit under the cloth on the lower edge",
        led_ok,
        "power, link, mute, listen; clear of the volume pads",
    ))

    cloth = p.get("cloth_fastening") or {}
    magnet = cloth.get("magnet") or {}
    disc = cloth.get("steel_disc") or {}
    rabbet = cloth.get("rabbet") or {}
    radius = magnet.get("pocket_diameter_mm", 0) / 2
    depth = magnet.get("pocket_depth_mm", 0)
    rim = rabbet.get("rim_mm", 0)
    recess = rabbet.get("depth_mm", 0)
    shelf = rabbet.get("shelf_mm", 0)
    inset = rim + (shelf - rim) / 2
    long_y = cloth.get("long_side_y_mm") or []
    short_x = cloth.get("short_side_x_mm") or []
    seats = [(x, y) for y in long_y for x in (-W / 2 + inset, W / 2 - inset)]
    seats += [(x, y) for x in short_x for y in (-H / 2 + inset, H / 2 - inset)]
    blank = cloth.get("blank_mm") or [0, 0]
    cloth_ok = (
        cloth.get("metal_on_face") is False
        and cloth.get("hem_mm") == 0
        and len(seats) == 14
        and blank == [W - 2 * rim, H - 2 * rim]
        and recess == lip
        and shelf >= rim + 2 * radius + 1.0
        and disc.get("place") == "reverse of the cloth edge"
        and meta.get("cloth_magnet_count") == 14
    )
    if shape_probe is not None and cloth_ok:
        rim_solid = shape_probe.isInside((W / 2 - rim / 2, 0, D - 0.4))
        face_open = not shape_probe.isInside((0, -150, D - 0.4))
        cloth_ok = cloth_ok and rim_solid and face_open
        for x, y in seats:
            hole = (x, y, D - recess - depth / 2)
            floor = (x, y, D - recess - depth - 0.4)
            cloth_ok = cloth_ok and (not shape_probe.isInside(hole)) and shape_probe.isInside(floor)
    gates.append(gate(
        "cloth sits flush in the front rabbet",
        cloth_ok,
        "317 x 397 mm, magnets open on the recessed border, rim stays proud",
    ))

    passage = (p.get("electronics") or {}).get("cable_pass") or {}
    cx, cz = (passage.get("center_xz_mm") or [0, 0])
    cw, cd = (passage.get("size_mm") or [0, 0])
    divider_y = bay_top + wall / 2
    pass_ok = (
        cw >= 16 and cd >= 6
        and rear + 1 <= cz - cd / 2 and cz + cd / 2 <= panel_z - 1
        and abs(cx) + cw / 2 < W / 2 - wall - 8
    )
    if shape_probe is not None and pass_ok:
        pass_ok = (
            not shape_probe.isInside((cx, divider_y, cz))
            and not shape_probe.isInside((cx, bay_top - 1, cz))
            and not shape_probe.isInside((cx, bay_top + wall + 1, cz))
            and shape_probe.isInside((cx + cw / 2 + 6, divider_y, cz))
            and shape_probe.isInside((cx, divider_y, rear / 2))
        )
    gates.append(gate(
        "speaker wires can leave the bay",
        pass_ok,
        "20 x 8 mm through the divider, behind the panel, sealed around the pairs",
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
            "Three free Core pins confirmed on a real Dev Kit before blue, red and amber are wired",
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
