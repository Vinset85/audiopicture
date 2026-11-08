#!/usr/bin/env python3
"""Genera lo schema elettrico quadro cucina con icone e rendering dispositivi."""

from pathlib import Path

import cairosvg

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 2000, 1420
BG = "#e8eef3"
PANEL = "#ffffff"
PANEL_EDGE = "#b8c4d0"
INK = "#1a2332"
MUTED = "#5a6b7d"
L_COL = "#c0392b"
L_SOFT = "#fdecea"
N_COL = "#0f766e"
N_SOFT = "#e6f4f2"
ETH = "#334155"
ACCENT = "#0f4c81"
ACCENT_SOFT = "#e8f1f8"
DIN = "#9aa6b2"
SHELLY_BODY = "#2b3340"
SHELLY_FACE = "#3a4454"
SCREEN = "#0a1624"
FUSE = "#94a3b8"

SHELLY1 = {
    "O4": (4, "Frigorifero", "fridge"),
    "O3": (3, "Forno", "oven"),
    "O2": (2, "Microonde", "microwave"),
    "O1": (1, "Lavastoviglie", "dishwasher"),
}
SHELLY2 = {
    "O4": (8, "Prese interno mobile", "socket"),
    "O3": (7, "Prese piano lavoro", "socket"),
    "O2": (6, "Prese piano cottura", "socket"),
    "O1": (5, "Piano cottura", "cooktop"),
}


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def icon_dishwasher(a, cx, cy, s=1.0):
    x, y = cx - 16 * s, cy - 18 * s
    a(f'<rect x="{x}" y="{y}" width="{32*s}" height="{36*s}" rx="{3*s}" fill="#dbe7f3" stroke="{ACCENT}" stroke-width="1.6"/>')
    a(f'<rect x="{x+3*s}" y="{y+3*s}" width="{26*s}" height="{6*s}" rx="{1.5*s}" fill="{ACCENT}"/>')
    a(f'<circle cx="{cx+8*s}" cy="{y+6*s}" r="{1.6*s}" fill="#9fd0ff"/>')
    a(f'<rect x="{x+5*s}" y="{y+13*s}" width="{22*s}" height="{16*s}" rx="{2*s}" fill="#fff" stroke="{ACCENT}" stroke-width="1.2"/>')
    a(f'<path d="M {x+8*s} {y+20*s} q {8*s} {8*s} {16*s} 0" fill="none" stroke="{ACCENT}" stroke-width="1.4"/>')


def icon_microwave(a, cx, cy, s=1.0):
    x, y = cx - 18 * s, cy - 14 * s
    a(f'<rect x="{x}" y="{y}" width="{36*s}" height="{28*s}" rx="{3*s}" fill="#dbe7f3" stroke="{ACCENT}" stroke-width="1.6"/>')
    a(f'<rect x="{x+3*s}" y="{y+4*s}" width="{20*s}" height="{20*s}" rx="{2*s}" fill="#0b1f33"/>')
    a(f'<rect x="{x+25*s}" y="{y+4*s}" width="{8*s}" height="{20*s}" rx="{1.5*s}" fill="#fff" stroke="{ACCENT}" stroke-width="1"/>')
    a(f'<circle cx="{x+29*s}" cy="{y+10*s}" r="{1.8*s}" fill="{ACCENT}"/>')
    a(f'<circle cx="{x+29*s}" cy="{y+18*s}" r="{1.8*s}" fill="{ACCENT}"/>')


def icon_oven(a, cx, cy, s=1.0):
    x, y = cx - 16 * s, cy - 18 * s
    a(f'<rect x="{x}" y="{y}" width="{32*s}" height="{36*s}" rx="{3*s}" fill="#dbe7f3" stroke="{ACCENT}" stroke-width="1.6"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{24*s}" height="{5*s}" rx="{1.5*s}" fill="{ACCENT}"/>')
    a(f'<rect x="{x+5*s}" y="{y+13*s}" width="{22*s}" height="{16*s}" rx="{2*s}" fill="#0b1f33"/>')
    a(f'<line x1="{x+8*s}" y1="{y+21*s}" x2="{x+24*s}" y2="{y+21*s}" stroke="#9fd0ff" stroke-width="1.3"/>')
    a(f'<circle cx="{cx}" cy="{y+6.5*s}" r="{1.4*s}" fill="#9fd0ff"/>')


def icon_fridge(a, cx, cy, s=1.0):
    x, y = cx - 14 * s, cy - 20 * s
    a(f'<rect x="{x}" y="{y}" width="{28*s}" height="{40*s}" rx="{3*s}" fill="#dbe7f3" stroke="{ACCENT}" stroke-width="1.6"/>')
    a(f'<line x1="{x}" y1="{y+14*s}" x2="{x+28*s}" y2="{y+14*s}" stroke="{ACCENT}" stroke-width="1.4"/>')
    a(f'<rect x="{x+22*s}" y="{y+5*s}" width="{2.5*s}" height="{6*s}" rx="{1*s}" fill="{ACCENT}"/>')
    a(f'<rect x="{x+22*s}" y="{y+20*s}" width="{2.5*s}" height="{10*s}" rx="{1*s}" fill="{ACCENT}"/>')


def icon_cooktop(a, cx, cy, s=1.0):
    x, y = cx - 18 * s, cy - 14 * s
    a(f'<rect x="{x}" y="{y}" width="{36*s}" height="{28*s}" rx="{3*s}" fill="#1f2937" stroke="{ACCENT}" stroke-width="1.6"/>')
    for dx, dy in ((-7, -4), (7, -4), (-7, 6), (7, 6)):
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{5*s}" fill="none" stroke="#f59e0b" stroke-width="1.6"/>')
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{2*s}" fill="#f59e0b" opacity="0.35"/>')


def icon_socket(a, cx, cy, s=1.0):
    x, y = cx - 14 * s, cy - 14 * s
    a(f'<rect x="{x}" y="{y}" width="{28*s}" height="{28*s}" rx="{4*s}" fill="#dbe7f3" stroke="{ACCENT}" stroke-width="1.6"/>')
    a(f'<circle cx="{cx-5*s}" cy="{cy-2*s}" r="{2.4*s}" fill="{ACCENT}"/>')
    a(f'<circle cx="{cx+5*s}" cy="{cy-2*s}" r="{2.4*s}" fill="{ACCENT}"/>')
    a(f'<path d="M {cx-4*s} {cy+7*s} a 4 {4*s} 0 0 0 {8*s} 0" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>')


ICONS = {
    "dishwasher": icon_dishwasher,
    "microwave": icon_microwave,
    "oven": icon_oven,
    "fridge": icon_fridge,
    "cooktop": icon_cooktop,
    "socket": icon_socket,
}


def draw_rj45(a, x, y):
    a(f'<rect x="{x}" y="{y}" width="34" height="22" rx="2" fill="#0f172a" stroke="#1e293b"/>')
    a(f'<rect x="{x+4}" y="{y+4}" width="26" height="14" rx="1" fill="#334155"/>')
    for i in range(6):
        a(f'<rect x="{x+7+i*3.5}" y="{y+7}" width="2" height="8" fill="#94a3b8"/>')


def draw_fuse(a, cx, cy):
    a(f'<rect x="{cx-10}" y="{cy-12}" width="20" height="24" rx="3" fill="#fff7ed" stroke="#d97706" stroke-width="1.6"/>')
    a(f'<line x1="{cx}" y1="{cy-7}" x2="{cx}" y2="{cy+7}" stroke="#d97706" stroke-width="2"/>')
    a(f'<circle cx="{cx}" cy="{cy-7}" r="2" fill="#d97706"/>')
    a(f'<circle cx="{cx}" cy="{cy+7}" r="2" fill="#d97706"/>')


def build_svg() -> str:
    p: list[str] = []
    a = p.append

    a(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#d5dde6" stroke-width="1"/>
    </pattern>
    <linearGradient id="dinGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c5ced6"/>
      <stop offset="50%" stop-color="#e8edf1"/>
      <stop offset="100%" stop-color="#b7c2cc"/>
    </linearGradient>
    <linearGradient id="rcboGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="shellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3d4758"/>
      <stop offset="100%" stop-color="#232a36"/>
    </linearGradient>
    <filter id="soft" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#1a2332" flood-opacity="0.12"/>
    </filter>
    <style><![CDATA[
      .title {{ font: 700 36px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .sub {{ font: 400 14px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .h {{ font: 700 14px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .h2 {{ font: 600 11px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .chip {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: #fff; }}
      .name {{ font: 700 12px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .term {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .term-l {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {L_COL}; }}
      .term-n {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {N_COL}; }}
      .note {{ font: 400 12px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .leg {{ font: 600 12px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .leg-m {{ font: 400 11px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .warn {{ font: 500 12px "DejaVu Sans", Arial, sans-serif; fill: #8a5a00; }}
      .dev-w {{ font: 700 13px "DejaVu Sans", Arial, sans-serif; fill: #fff; }}
      .scr {{ font: 600 12px "DejaVu Sans", Arial, sans-serif; fill: #7dd3fc; }}
      .scr2 {{ font: 500 10px "DejaVu Sans", Arial, sans-serif; fill: #64748b; }}
    ]]></style>
  </defs>
  <rect width="100%" height="100%" fill="{BG}"/>
  <rect width="100%" height="100%" fill="url(#grid)" opacity="0.5"/>
'''
    )

    # Header
    a(f'<rect x="0" y="0" width="{W}" height="92" fill="{PANEL}"/>')
    a(f'<rect x="0" y="90" width="{W}" height="3" fill="{ACCENT}"/>')
    a(f'<text x="48" y="42" class="title">Quadro elettrico cucina</text>')
    a(
        f'<text x="48" y="68" class="sub">'
        "Simulazione dispositivi DIN + schema cablaggio · RCBO · 2× Shelly Pro 4PM · 8 carichi</text>"
    )
    keys = [
        (1500, L_COL, "Fase L"),
        (1600, N_COL, "Neutro N"),
        (1710, ETH, "Ethernet"),
        (1825, "#d97706", "Fusibile"),
    ]
    for x, col, lab in keys:
        a(f'<rect x="{x}" y="34" width="14" height="14" rx="3" fill="{col}"/>')
        a(f'<text x="{x+22}" y="46" class="note">{lab}</text>')

    top_n_y = 175
    din_y = 430
    device_y = 390
    device_h = 300
    l_bus_y = 780
    n_bus_y = 1040

    # N carichi
    a(f'<line x1="310" y1="{top_n_y}" x2="1860" y2="{top_n_y}" stroke="{N_COL}" stroke-width="3.2"/>')
    a(f'<rect x="1870" y="{top_n_y-14}" width="90" height="28" rx="14" fill="{N_SOFT}" stroke="{N_COL}" stroke-width="1.5"/>')
    a(f'<text x="1915" y="{top_n_y+5}" text-anchor="middle" class="term-n">N carichi</text>')

    # DIN rail under devices
    a(f'<rect x="280" y="{din_y+250}" width="1560" height="28" rx="4" fill="url(#dinGrad)" stroke="{DIN}" stroke-width="1"/>')
    a(f'<text x="300" y="{din_y+269}" class="h2">Guida DIN 35 mm</text>')

    # ===== RCBO device simulation =====
    mx, my, mw, mh = 48, 360, 220, 340
    a(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="10" fill="url(#rcboGrad)" stroke="{PANEL_EDGE}" stroke-width="1.6" filter="url(#soft)"/>')
    # DIN clip look
    a(f'<rect x="{mx+8}" y="{my+mh-18}" width="{mw-16}" height="10" rx="2" fill="#cbd5e1"/>')
    a(f'<text x="{mx+mw/2}" y="{my+28}" text-anchor="middle" class="h">Magnetotermico</text>')
    a(f'<text x="{mx+mw/2}" y="{my+48}" text-anchor="middle" class="h">differenziale</text>')
    a(f'<rect x="{mx+40}" y="{my+62}" width="{mw-80}" height="24" rx="12" fill="{ACCENT_SOFT}"/>')
    a(f'<text x="{mx+mw/2}" y="{my+78}" text-anchor="middle" class="h2">RCBO · bipolare</text>')

    # Lever / test button simulation
    a(f'<rect x="{mx+55}" y="{my+105}" width="110" height="150" rx="8" fill="#fff" stroke="{PANEL_EDGE}"/>')
    a(f'<rect x="{mx+78}" y="{my+120}" width="64" height="18" rx="3" fill="#ef4444"/>')
    a(f'<text x="{mx+110}" y="{my+133}" text-anchor="middle" class="chip" style="font-size:10px">TEST</text>')
    # Toggle lever
    a(f'<rect x="{mx+92}" y="{my+155}" width="36" height="70" rx="6" fill="#e2e8f0" stroke="{INK}" stroke-width="1.4"/>')
    a(f'<rect x="{mx+96}" y="{my+160}" width="28" height="28" rx="4" fill="#22c55e"/>')
    a(f'<text x="{mx+110}" y="{my+250}" text-anchor="middle" class="h2">ON</text>')
    a(f'<text x="{mx+mw/2}" y="{my+290}" text-anchor="middle" class="h2">IΔn · protezione L+N</text>')

    # Supply in
    a(f'<line x1="100" y1="125" x2="100" y2="{my}" stroke="{L_COL}" stroke-width="3.2"/>')
    a(f'<line x1="170" y1="125" x2="170" y2="{my}" stroke="{N_COL}" stroke-width="3.2"/>')
    a(f'<circle cx="100" cy="{my}" r="5.5" fill="{L_COL}"/>')
    a(f'<circle cx="170" cy="{my}" r="5.5" fill="{N_COL}"/>')
    a(f'<rect x="74" y="100" width="52" height="22" rx="11" fill="{L_SOFT}" stroke="{L_COL}" stroke-width="1.3"/>')
    a(f'<text x="100" y="115" text-anchor="middle" class="term-l">L rete</text>')
    a(f'<rect x="144" y="100" width="52" height="22" rx="11" fill="{N_SOFT}" stroke="{N_COL}" stroke-width="1.3"/>')
    a(f'<text x="170" y="115" text-anchor="middle" class="term-n">N rete</text>')

    # Terminal screws on RCBO top/bottom
    for tx in (100, 170):
        a(f'<rect x="{tx-10}" y="{my-1}" width="20" height="12" rx="2" fill="#64748b"/>')
        a(f'<circle cx="{tx}" cy="{my+5}" r="3" fill="#cbd5e1"/>')
        a(f'<rect x="{tx-10}" y="{my+mh-11}" width="20" height="12" rx="2" fill="#64748b"/>')
        a(f'<circle cx="{tx}" cy="{my+mh-5}" r="3" fill="#cbd5e1"/>')

    a(f'<line x1="100" y1="{my}" x2="100" y2="{my+mh}" stroke="{L_COL}" stroke-width="3.2"/>')
    a(f'<line x1="170" y1="{my}" x2="170" y2="{my+mh}" stroke="{N_COL}" stroke-width="3.2"/>')

    # Buses
    a(f'<line x1="100" y1="{my+mh}" x2="100" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3.2"/>')
    a(f'<line x1="100" y1="{l_bus_y}" x2="1860" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3.2"/>')
    a(f'<rect x="1870" y="{l_bus_y-14}" width="72" height="28" rx="14" fill="{L_SOFT}" stroke="{L_COL}" stroke-width="1.5"/>')
    a(f'<text x="1906" y="{l_bus_y+5}" text-anchor="middle" class="term-l">BUS L</text>')

    a(f'<line x1="170" y1="{my+mh}" x2="170" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3.2"/>')
    a(f'<line x1="170" y1="{n_bus_y}" x2="1860" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3.2"/>')
    a(f'<rect x="1870" y="{n_bus_y-14}" width="72" height="28" rx="14" fill="{N_SOFT}" stroke="{N_COL}" stroke-width="1.5"/>')
    a(f'<text x="1906" y="{n_bus_y+5}" text-anchor="middle" class="term-n">BUS N</text>')
    a(f'<line x1="1860" y1="{top_n_y}" x2="1860" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3.2"/>')

    def draw_shelly(x: float, title: str, eth: str, mapping: dict):
        y, w, h = device_y, 620, device_h
        # Body — look like DIN Shelly Pro
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#shellyGrad)" stroke="#111827" stroke-width="1.4" filter="url(#soft)"/>')
        # Top bevel / label strip
        a(f'<rect x="{x+10}" y="{y+10}" width="{w-20}" height="36" rx="6" fill="#1f2937"/>')
        a(f'<text x="{x+24}" y="{y+33}" class="dev-w">{title}</text>')
        a(f'<text x="{x+w-24}" y="{y+33}" text-anchor="end" class="scr2" style="fill:#94a3b8">Pro 4PM</text>')

        # Screen simulation
        sx, sy, sw, sh = x + w / 2 - 120, y + 60, 240, 88
        a(f'<rect x="{sx-4}" y="{sy-4}" width="{sw+8}" height="{sh+8}" rx="8" fill="#0b1220"/>')
        a(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="6" fill="{SCREEN}"/>')
        a(f'<text x="{sx+sw/2}" y="{sy+28}" text-anchor="middle" class="scr">Shelly Pro 4PM</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+48}" text-anchor="middle" class="scr2">4× relè · 16 A · metering</text>')
        a(f'<text x="{sx+14}" y="{sy+72}" class="scr2" style="fill:#22c55e">● online</text>')
        a(f'<text x="{sx+sw-14}" y="{sy+72}" text-anchor="end" class="scr2" style="fill:#38bdf8">{eth}</text>')

        # Buttons under screen
        for i, lab in enumerate(["▲", "▼", "OK"]):
            bx = sx + 30 + i * 65
            by = sy + sh + 14
            a(f'<rect x="{bx}" y="{by}" width="48" height="24" rx="5" fill="#4b5563" stroke="#6b7280"/>')
            a(f'<text x="{bx+24}" y="{by+16}" text-anchor="middle" class="chip">{lab}</text>')

        # Status LEDs
        for i, col in enumerate(["#22c55e", "#22c55e", "#22c55e", "#22c55e"]):
            a(f'<circle cx="{x+40+i*18}" cy="{y+78}" r="4" fill="{col}"/>')
        a(f'<text x="{x+40}" y="{y+98}" class="scr2" style="fill:#94a3b8">O1–O4</text>')

        # Terminal positions
        term_x = {
            "O4": x + 70,
            "O3": x + 175,
            "L": x + w / 2,
            "O2": x + w - 175,
            "O1": x + w - 70,
        }

        # Top terminal block visual
        a(f'<rect x="{x+30}" y="{y-8}" width="{w-60}" height="16" rx="3" fill="#475569"/>')
        for label, tx in term_x.items():
            a(f'<rect x="{tx-12}" y="{y-10}" width="24" height="14" rx="2" fill="#64748b"/>')
            a(f'<circle cx="{tx}" cy="{y-3}" r="3.2" fill="#e2e8f0"/>')
            if label == "L":
                a(f'<rect x="{tx-14}" y="{y+14}" width="28" height="18" rx="9" fill="{L_SOFT}" stroke="{L_COL}" stroke-width="1.2"/>')
                a(f'<text x="{tx}" y="{y+27}" text-anchor="middle" class="term-l">L</text>')
                a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3.2"/>')
                a(f'<circle cx="{tx}" cy="{l_bus_y}" r="4.5" fill="{L_COL}"/>')
            else:
                a(f'<text x="{tx}" y="{y+28}" text-anchor="middle" class="chip" style="fill:#e2e8f0">{label}</text>')

        # Bottom: LAN + N + unused S silhouette
        lan_x = x + 70
        n_x = x + 165
        draw_rj45(a, lan_x - 17, y + h - 18)
        a(f'<text x="{lan_x}" y="{y+h+28}" text-anchor="middle" class="h2" style="fill:#cbd5e1">LAN</text>')
        eth_y = y + h + 62
        a(f'<path d="M {lan_x} {y+h+8} V {eth_y} H {lan_x+95}" fill="none" stroke="{ETH}" stroke-width="2.4" stroke-dasharray="6 4" stroke-linecap="round"/>')
        a(f'<rect x="{lan_x+103}" y="{eth_y-13}" width="60" height="26" rx="13" fill="#e2e8f0" stroke="{ETH}" stroke-width="1.3"/>')
        a(f'<text x="{lan_x+133}" y="{eth_y+4}" text-anchor="middle" class="term">{eth}</text>')

        a(f'<rect x="{n_x-12}" y="{y+h-10}" width="24" height="14" rx="2" fill="#64748b"/>')
        a(f'<circle cx="{n_x}" cy="{y+h-3}" r="3.2" fill="#e2e8f0"/>')
        a(f'<rect x="{n_x-14}" y="{y+h-34}" width="28" height="18" rx="9" fill="{N_SOFT}" stroke="{N_COL}" stroke-width="1.2"/>')
        a(f'<text x="{n_x}" y="{y+h-21}" text-anchor="middle" class="term-n">N</text>')
        a(f'<line x1="{n_x}" y1="{y+h}" x2="{n_x}" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3.2"/>')
        a(f'<circle cx="{n_x}" cy="{n_bus_y}" r="4.5" fill="{N_COL}"/>')

        # S terminal silhouettes (unused)
        for i, lab in enumerate(["S4", "S3", "S2", "S1"]):
            sx_ = x + w - 200 + i * 42
            a(f'<rect x="{sx_-10}" y="{y+h-10}" width="20" height="12" rx="2" fill="#374151" opacity="0.7"/>')
            a(f'<text x="{sx_}" y="{y+h+18}" text-anchor="middle" class="scr2" style="fill:#64748b">{lab}</text>')
        a(f'<text x="{x+w-24}" y="{y+h+38}" text-anchor="end" class="note" style="fill:#94a3b8">S1–S4 non usati</text>')

        # Output channels with icons
        for idx, out in enumerate(("O4", "O3", "O2", "O1")):
            num, name, icon = mapping[out]
            tx = term_x[out]
            fuse_y = y - 48
            a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{fuse_y+12}" stroke="{INK}" stroke-width="2.6"/>')
            draw_fuse(a, tx, fuse_y)
            load_y = top_n_y + 78
            a(f'<line x1="{tx}" y1="{fuse_y-12}" x2="{tx}" y2="{load_y}" stroke="{INK}" stroke-width="2.6"/>')
            a(f'<line x1="{tx}" y1="{top_n_y}" x2="{tx}" y2="{top_n_y+18}" stroke="{N_COL}" stroke-width="2.6"/>')
            a(f'<circle cx="{tx}" cy="{top_n_y}" r="4.2" fill="{N_COL}"/>')

            # Icon card
            stagger = 0 if idx % 2 == 0 else 50
            card_y = top_n_y + 18 + stagger
            card_w, card_h = 118, 86
            a(f'<rect x="{tx-card_w/2}" y="{card_y}" width="{card_w}" height="{card_h}" rx="12" fill="{PANEL}" stroke="{PANEL_EDGE}" stroke-width="1.4" filter="url(#soft)"/>')
            a(f'<circle cx="{tx-card_w/2+18}" cy="{card_y+18}" r="12" fill="{ACCENT}"/>')
            a(f'<text x="{tx-card_w/2+18}" y="{card_y+22}" text-anchor="middle" class="chip">{num}</text>')
            a(f'<text x="{tx+10}" y="{card_y+22}" text-anchor="middle" class="h2">{out}</text>')
            ICONS[icon](a, tx, card_y + 48, 1.0)
            # name below card
            words = name.split()
            if len(name) > 14 and len(words) > 1:
                mid = max(1, len(words) // 2)
                a(f'<text x="{tx}" y="{card_y+card_h+16}" text-anchor="middle" class="name" style="font-size:11px">{esc(" ".join(words[:mid]))}</text>')
                a(f'<text x="{tx}" y="{card_y+card_h+30}" text-anchor="middle" class="name" style="font-size:11px">{esc(" ".join(words[mid:]))}</text>')
            else:
                a(f'<text x="{tx}" y="{card_y+card_h+18}" text-anchor="middle" class="name">{esc(name)}</text>')

    draw_shelly(310, "SHELLY #1", "ETH 1", SHELLY1)
    draw_shelly(1020, "SHELLY #2", "ETH 2", SHELLY2)

    # Legend with mini icons
    lx, ly = 310, 1120
    a(f'<rect x="{lx}" y="{ly}" width="1300" height="250" rx="16" fill="{PANEL}" stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>')
    a(f'<text x="{lx+24}" y="{ly+32}" class="h">Legenda carichi e dispositivi</text>')
    a(f'<text x="{lx+24}" y="{ly+52}" class="note">Icone appliance · canale Shelly = numero circuito · fase da Ox · neutro da N carichi</text>')

    legend = [
        (1, "Lavastoviglie", "Shelly #1 · O1", "dishwasher"),
        (2, "Microonde", "Shelly #1 · O2", "microwave"),
        (3, "Forno", "Shelly #1 · O3", "oven"),
        (4, "Frigorifero", "Shelly #1 · O4", "fridge"),
        (5, "Piano cottura", "Shelly #2 · O1", "cooktop"),
        (6, "Prese piano cottura", "Shelly #2 · O2", "socket"),
        (7, "Prese piano lavoro", "Shelly #2 · O3", "socket"),
        (8, "Prese interno mobile", "Shelly #2 · O4", "socket"),
    ]
    for i, (num, name, path, icon) in enumerate(legend):
        col = i % 4
        row = i // 4
        x = lx + 24 + col * 315
        y = ly + 72 + row * 70
        a(f'<rect x="{x}" y="{y}" width="295" height="58" rx="12" fill="#f8fafc" stroke="{PANEL_EDGE}"/>')
        a(f'<circle cx="{x+22}" cy="{y+29}" r="13" fill="{ACCENT}"/>')
        a(f'<text x="{x+22}" y="{y+33}" text-anchor="middle" class="chip">{num}</text>')
        ICONS[icon](a, x + 58, y + 29, 0.72)
        a(f'<text x="{x+88}" y="{y+24}" class="leg">{esc(name)}</text>')
        a(f'<text x="{x+88}" y="{y+42}" class="leg-m">{esc(path)}</text>')

    a(
        f'<text x="{lx+24}" y="{ly+230}" class="warn">'
        "Verificare correnti in opera: max 16 A/canale e 40 A totali per Pro 4PM "
        "(attenzione a forno e piano cottura).</text>"
    )

    # Flow + device key
    a(f'<rect x="48" y="1120" width="230" height="250" rx="16" fill="{PANEL}" stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>')
    a(f'<text x="68" y="1154" class="h">Flusso</text>')
    for i, step in enumerate([
        "1. L/N da rete",
        "2. RCBO (leva ON)",
        "3. BUS L / BUS N",
        "4. Shelly #1 e #2",
        "5. Fusibile → Ox",
        "6. Icona carico",
        "7. Neutro comune",
        "8. ETH 1 / ETH 2",
    ]):
        a(f'<text x="68" y="{1182 + i*22}" class="note">{step}</text>')

    a("</svg>")
    return "\n".join(p)


def main() -> None:
    svg = build_svg()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OUT_DIR / "quadro-elettrico-cucina.svg"
    png_path = OUT_DIR / "quadro-elettrico-cucina.png"
    art_svg = ART_DIR / "quadro-elettrico-cucina.svg"
    art_png = ART_DIR / "quadro-elettrico-cucina.png"
    svg_path.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png_path), scale=1.25)
    art_svg.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(art_png), scale=1.25)
    print(f"Wrote {art_png}")


if __name__ == "__main__":
    main()
