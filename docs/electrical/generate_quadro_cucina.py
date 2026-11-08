#!/usr/bin/env python3
"""Schema quadro cucina realistico: armadio, DIN, RCBO, Shelly Pro 4PM, icone."""

from pathlib import Path

import cairosvg

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 2200, 1680

# IEC-ish colors (Italia)
L_COL = "#8B4513"  # marrone fase
L_BRIGHT = "#A0522D"
N_COL = "#1D4ED8"  # blu neutro
PE_COL = "#CA8A04"
ETH = "#111827"
INK = "#111827"
MUTED = "#4B5563"
BG = "#9CA3AF"
CABINET = "#D1D5DB"
CABINET_IN = "#E5E7EB"
PLASTIC = "#F3F4F6"
PLASTIC_EDGE = "#9CA3AF"
SHELLY_GRAY = "#E8EAED"
SHELLY_DARK = "#4B5563"
SCREEN_BG = "#1a2332"
ACCENT = "#0F4C81"

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


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ----- Icons (more detailed) -----
def icon_dishwasher(a, cx, cy, s=1.0):
    x, y, w, h = cx - 18 * s, cy - 22 * s, 36 * s, 44 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{4*s}" fill="#E5E7EB" stroke="#374151" stroke-width="1.5"/>')
    a(f'<rect x="{x+3*s}" y="{y+3*s}" width="{w-6*s}" height="{8*s}" rx="{2*s}" fill="#6B7280"/>')
    a(f'<circle cx="{cx+10*s}" cy="{y+7*s}" r="{2*s}" fill="#93C5FD"/>')
    a(f'<rect x="{x+5*s}" y="{y+14*s}" width="{w-10*s}" height="{22*s}" rx="{2*s}" fill="#F9FAFB" stroke="#6B7280"/>')
    a(f'<path d="M{x+9*s} {y+26*s} q {9*s} {10*s} {18*s} 0" fill="none" stroke="#3B82F6" stroke-width="{1.6*s}"/>')
    a(f'<path d="M{x+11*s} {y+23*s} q {7*s} {7*s} {14*s} 0" fill="none" stroke="#93C5FD" stroke-width="{1.2*s}"/>')


def icon_microwave(a, cx, cy, s=1.0):
    x, y, w, h = cx - 22 * s, cy - 16 * s, 44 * s, 32 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{3*s}" fill="#E5E7EB" stroke="#374151" stroke-width="1.5"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{24*s}" height="{24*s}" rx="{2*s}" fill="#111827"/>')
    a(f'<rect x="{x+8*s}" y="{y+8*s}" width="{16*s}" height="{16*s}" rx="{1*s}" fill="#1F2937" stroke="#4B5563"/>')
    a(f'<rect x="{x+30*s}" y="{y+4*s}" width="{10*s}" height="{24*s}" rx="{2*s}" fill="#F9FAFB" stroke="#6B7280"/>')
    a(f'<circle cx="{x+35*s}" cy="{y+11*s}" r="{2.2*s}" fill="#374151"/>')
    a(f'<circle cx="{x+35*s}" cy="{y+20*s}" r="{2.2*s}" fill="#374151"/>')
    a(f'<rect x="{x+32*s}" y="{y+25*s}" width="{6*s}" height="{1.5*s}" fill="#9CA3AF"/>')


def icon_oven(a, cx, cy, s=1.0):
    x, y, w, h = cx - 18 * s, cy - 22 * s, 36 * s, 44 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{3*s}" fill="#E5E7EB" stroke="#374151" stroke-width="1.5"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{w-8*s}" height="{7*s}" rx="{2*s}" fill="#4B5563"/>')
    a(f'<circle cx="{cx-6*s}" cy="{y+7.5*s}" r="{1.8*s}" fill="#D1D5DB"/>')
    a(f'<circle cx="{cx+6*s}" cy="{y+7.5*s}" r="{1.8*s}" fill="#D1D5DB"/>')
    a(f'<rect x="{x+5*s}" y="{y+15*s}" width="{w-10*s}" height="{22*s}" rx="{2*s}" fill="#111827"/>')
    a(f'<rect x="{x+8*s}" y="{y+19*s}" width="{w-16*s}" height="{14*s}" rx="{1*s}" fill="#1F2937" stroke="#F59E0B" stroke-width="1"/>')
    a(f'<line x1="{x+10*s}" y1="{y+26*s}" x2="{x+w-10*s}" y2="{y+26*s}" stroke="#FBBF24" stroke-width="1.2"/>')


def icon_fridge(a, cx, cy, s=1.0):
    x, y, w, h = cx - 15 * s, cy - 24 * s, 30 * s, 48 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{3*s}" fill="#E5E7EB" stroke="#374151" stroke-width="1.5"/>')
    a(f'<line x1="{x}" y1="{y+16*s}" x2="{x+w}" y2="{y+16*s}" stroke="#6B7280" stroke-width="1.4"/>')
    a(f'<rect x="{x+w-6*s}" y="{y+5*s}" width="{2.5*s}" height="{7*s}" rx="{1*s}" fill="#374151"/>')
    a(f'<rect x="{x+w-6*s}" y="{y+22*s}" width="{2.5*s}" height="{12*s}" rx="{1*s}" fill="#374151"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{8*s}" height="{3*s}" rx="{1*s}" fill="#93C5FD" opacity="0.7"/>')


def icon_cooktop(a, cx, cy, s=1.0):
    x, y, w, h = cx - 22 * s, cy - 16 * s, 44 * s, 32 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{3*s}" fill="#1F2937" stroke="#111827" stroke-width="1.5"/>')
    for dx, dy, r in ((-8, -4, 6), (8, -4, 5), (-8, 7, 5), (8, 7, 6)):
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{r*s}" fill="none" stroke="#F59E0B" stroke-width="1.7"/>')
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{(r-2.5)*s}" fill="#F59E0B" opacity="0.25"/>')


def icon_socket(a, cx, cy, s=1.0):
    x, y, w, h = cx - 16 * s, cy - 16 * s, 32 * s, 32 * s
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{4*s}" fill="#F3F4F6" stroke="#374151" stroke-width="1.5"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{w-8*s}" height="{h-8*s}" rx="{3*s}" fill="#E5E7EB" stroke="#9CA3AF"/>')
    a(f'<circle cx="{cx-5*s}" cy="{cy-1*s}" r="{2.6*s}" fill="#111827"/>')
    a(f'<circle cx="{cx+5*s}" cy="{cy-1*s}" r="{2.6*s}" fill="#111827"/>')
    a(f'<path d="M{cx-5*s} {cy+8*s} a 5 {5*s} 0 0 0 {10*s} 0" fill="none" stroke="#111827" stroke-width="1.6"/>')


ICONS = {
    "dishwasher": icon_dishwasher,
    "microwave": icon_microwave,
    "oven": icon_oven,
    "fridge": icon_fridge,
    "cooktop": icon_cooktop,
    "socket": icon_socket,
}


def screw(a, cx, cy, r=3.4):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#9CA3AF" stroke="#4B5563" stroke-width="0.8"/>')
    a(f'<line x1="{cx-r*0.6}" y1="{cy}" x2="{cx+r*0.6}" y2="{cy}" stroke="#374151" stroke-width="1"/>')
    a(f'<line x1="{cx}" y1="{cy-r*0.6}" x2="{cx}" y2="{cy+r*0.6}" stroke="#374151" stroke-width="1"/>')


def terminal_block(a, x, y, labels, width):
    n = len(labels)
    slot = width / n
    a(f'<rect x="{x}" y="{y}" width="{width}" height="18" rx="2" fill="#6B7280" stroke="#374151"/>')
    for i, lab in enumerate(labels):
        tx = x + slot * (i + 0.5)
        a(f'<rect x="{tx-11}" y="{y+1}" width="22" height="16" rx="1.5" fill="#9CA3AF"/>')
        screw(a, tx, y + 9, 3.0)
        a(f'<text x="{tx}" y="{y+32}" text-anchor="middle" style="font:700 10px DejaVu Sans,Arial;fill:#111827">{lab}</text>')


def draw_mcb_fuse(a, cx, cy):
    """Mini magnetotermico / portafusibile canale — aspetto plastica."""
    a(f'<rect x="{cx-14}" y="{cy-28}" width="28" height="56" rx="3" fill="#F9FAFB" stroke="#6B7280" stroke-width="1.3"/>')
    a(f'<rect x="{cx-10}" y="{cy-22}" width="20" height="10" rx="1.5" fill="#FEE2E2" stroke="#EF4444" stroke-width="0.8"/>')
    a(f'<text x="{cx}" y="{cy-14}" text-anchor="middle" style="font:700 7px DejaVu Sans,Arial;fill:#B91C1C">16A</text>')
    a(f'<rect x="{cx-5}" y="{cy-6}" width="10" height="22" rx="2" fill="#E5E7EB" stroke="#374151"/>')
    a(f'<rect x="{cx-4}" y="{cy-4}" width="8" height="10" rx="1.5" fill="#22C55E"/>')
    screw(a, cx, cy - 24, 2.2)
    screw(a, cx, cy + 22, 2.2)


def draw_rj45(a, x, y):
    a(f'<rect x="{x}" y="{y}" width="40" height="26" rx="2" fill="#111827" stroke="#000"/>')
    a(f'<rect x="{x+4}" y="{y+4}" width="32" height="16" rx="1" fill="#374151"/>')
    for i in range(8):
        a(f'<rect x="{x+6+i*3.5}" y="{y+6}" width="2.2" height="10" fill="#D1D5DB"/>')
    a(f'<rect x="{x+14}" y="{y+20}" width="12" height="4" fill="#4B5563"/>')


def draw_eth_cable(a, x1, y1, x2, y2, label):
    # jack plug
    a(f'<rect x="{x1-8}" y="{y1}" width="16" height="10" rx="1" fill="#1F2937"/>')
    a(f'<path d="M{x1} {y1+10} V {y2} H {x2}" fill="none" stroke="#111827" stroke-width="3.5" stroke-linecap="round"/>')
    a(f'<path d="M{x1} {y1+10} V {y2} H {x2}" fill="none" stroke="#6B7280" stroke-width="1.6" stroke-dasharray="2 3"/>')
    a(f'<rect x="{x2}" y="{y2-12}" width="54" height="24" rx="4" fill="#111827"/>')
    a(f'<text x="{x2+27}" y="{y2+4}" text-anchor="middle" style="font:700 11px DejaVu Sans,Arial;fill:#F9FAFB">{label}</text>')


def build_svg() -> str:
    p: list[str] = []
    a = p.append

    a(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="cabOut" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E5E7EB"/>
      <stop offset="100%" stop-color="#9CA3AF"/>
    </linearGradient>
    <linearGradient id="cabIn" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F3F4F6"/>
      <stop offset="100%" stop-color="#D1D5DB"/>
    </linearGradient>
    <linearGradient id="din" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F9FAFB"/>
      <stop offset="45%" stop-color="#E5E7EB"/>
      <stop offset="55%" stop-color="#9CA3AF"/>
      <stop offset="100%" stop-color="#6B7280"/>
    </linearGradient>
    <linearGradient id="plastic" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E5E7EB"/>
    </linearGradient>
    <linearGradient id="shellyBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8F9FA"/>
      <stop offset="40%" stop-color="#E8EAED"/>
      <stop offset="100%" stop-color="#CBD0D6"/>
    </linearGradient>
    <filter id="depth" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#111827" flood-opacity="0.22"/>
    </filter>
    <filter id="inset">
      <feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.25"/>
    </filter>
    <style><![CDATA[
      .title {{ font: 700 34px DejaVu Sans, Arial, sans-serif; fill: #111827; }}
      .sub {{ font: 400 13px DejaVu Sans, Arial, sans-serif; fill: #4B5563; }}
      .h {{ font: 700 13px DejaVu Sans, Arial, sans-serif; fill: #111827; }}
      .h2 {{ font: 600 10px DejaVu Sans, Arial, sans-serif; fill: #6B7280; }}
      .name {{ font: 700 11px DejaVu Sans, Arial, sans-serif; fill: #111827; }}
      .note {{ font: 400 12px DejaVu Sans, Arial, sans-serif; fill: #4B5563; }}
      .leg {{ font: 600 12px DejaVu Sans, Arial, sans-serif; fill: #111827; }}
      .leg-m {{ font: 400 11px DejaVu Sans, Arial, sans-serif; fill: #6B7280; }}
      .warn {{ font: 500 12px DejaVu Sans, Arial, sans-serif; fill: #92400E; }}
      .chip {{ font: 700 11px DejaVu Sans, Arial, sans-serif; fill: #fff; }}
      .scr {{ font: 700 12px DejaVu Sans, Arial, sans-serif; fill: #7DD3FC; }}
      .scr2 {{ font: 500 10px DejaVu Sans, Arial, sans-serif; fill: #64748B; }}
      .l {{ font: 700 11px DejaVu Sans, Arial, sans-serif; fill: {L_COL}; }}
      .n {{ font: 700 11px DejaVu Sans, Arial, sans-serif; fill: {N_COL}; }}
      .vert {{ font: 700 12px DejaVu Sans, Arial, sans-serif; fill: #374151; }}
    ]]></style>
  </defs>
  <rect width="100%" height="100%" fill="{BG}"/>
''')

    # Outer room / wall
    a(f'<rect x="30" y="30" width="{W-60}" height="{H-60}" rx="8" fill="#6B7280"/>')

    # Header plate
    a(f'<rect x="50" y="50" width="{W-100}" height="78" rx="6" fill="#F9FAFB" filter="url(#depth)"/>')
    a(f'<text x="74" y="88" class="title">Quadro elettrico cucina</text>')
    a(f'<text x="74" y="110" class="sub">Armadio DIN · RCBO · 2× Shelly Pro 4PM · colori IEC (L marrone / N blu) · vista frontale realistica</text>')
    a(f'<rect x="1680" y="68" width="14" height="14" rx="2" fill="{L_COL}"/>')
    a(f'<text x="1702" y="80" class="note">L fase</text>')
    a(f'<rect x="1780" y="68" width="14" height="14" rx="2" fill="{N_COL}"/>')
    a(f'<text x="1802" y="80" class="note">N neutro</text>')
    a(f'<rect x="1890" y="68" width="14" height="14" rx="2" fill="{ETH}"/>')
    a(f'<text x="1912" y="80" class="note">ETH</text>')

    # Cabinet enclosure
    cab_x, cab_y, cab_w, cab_h = 50, 145, W - 100, 1280
    a(f'<rect x="{cab_x}" y="{cab_y}" width="{cab_w}" height="{cab_h}" rx="10" fill="url(#cabOut)" stroke="#4B5563" stroke-width="3" filter="url(#depth)"/>')
    for hy in (cab_y + 80, cab_y + cab_h / 2, cab_y + cab_h - 100):
        a(f'<rect x="{cab_x-6}" y="{hy}" width="12" height="36" rx="2" fill="#374151"/>')
    ix, iy, iw, ih = cab_x + 28, cab_y + 28, cab_w - 56, cab_h - 56
    a(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="4" fill="url(#cabIn)" stroke="#9CA3AF"/>')
    for i in range(14):
        a(f'<rect x="{ix+40+i*55}" y="{iy+8}" width="30" height="4" rx="1" fill="#9CA3AF"/>')

    # Zona carichi in alto
    top_n_y = iy + 55
    a(f'<rect x="{ix+40}" y="{top_n_y-8}" width="{iw-200}" height="16" rx="3" fill="{N_COL}"/>')
    a(f'<rect x="{ix+iw-150}" y="{top_n_y-14}" width="100" height="28" rx="4" fill="#DBEAFE" stroke="{N_COL}"/>')
    a(f'<text x="{ix+iw-100}" y="{top_n_y+5}" text-anchor="middle" class="n">MORSETTIERA N</text>')

    # Canalina intermedia (tra carichi e dispositivi)
    duct_y = iy + 250
    a(f'<rect x="{ix+20}" y="{duct_y}" width="{iw-40}" height="32" rx="3" fill="#9CA3AF" stroke="#6B7280"/>')
    a(f'<rect x="{ix+24}" y="{duct_y+4}" width="{iw-48}" height="24" rx="2" fill="#D1D5DB"/>')
    a(f'<text x="{ix+40}" y="{duct_y+20}" class="h2">Canalina · fusibili/MT di canale</text>')

    # DIN rail più in basso per lasciare spazio a MCB e card
    din_y = iy + 560
    a(f'<rect x="{ix+30}" y="{din_y}" width="{iw-60}" height="34" rx="2" fill="url(#din)" stroke="#6B7280"/>')
    a(f'<rect x="{ix+30}" y="{din_y+12}" width="{iw-60}" height="4" fill="#F9FAFB" opacity="0.7"/>')
    a(f'<text x="{ix+45}" y="{din_y+58}" class="h2">Guida DIN EN 60715 · 35 mm</text>')

    a(f'<rect x="{ix+20}" y="{iy+ih-90}" width="{iw-40}" height="36" rx="3" fill="#9CA3AF" stroke="#6B7280"/>')
    a(f'<rect x="{ix+24}" y="{iy+ih-86}" width="{iw-48}" height="28" rx="2" fill="#D1D5DB"/>')
    a(f'<text x="{ix+40}" y="{iy+ih-66}" class="h2">Canalina inferiore · alimentazione e Ethernet</text>')

    # ===== RCBO realistic =====
    mx, my, mw, mh = ix + 40, din_y - 280, 160, 300
    a(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="4" fill="url(#plastic)" stroke="#6B7280" stroke-width="1.4" filter="url(#depth)"/>')
    # brand plate
    a(f'<rect x="{mx+8}" y="{my+8}" width="{mw-16}" height="42" rx="3" fill="#F9FAFB" stroke="#D1D5DB"/>')
    a(f'<text x="{mx+mw/2}" y="{my+26}" text-anchor="middle" class="h">RCBO</text>')
    a(f'<text x="{mx+mw/2}" y="{my+42}" text-anchor="middle" class="h2">2P · 40A · 30mA</text>')
    # top terminals L N
    terminal_block(a, mx + 18, my - 2, ["L", "N"], mw - 36)
    # body window
    a(f'<rect x="{mx+20}" y="{my+60}" width="{mw-40}" height="160" rx="4" fill="#FFFFFF" stroke="#9CA3AF"/>')
    a(f'<rect x="{mx+35}" y="{my+72}" width="{mw-70}" height="22" rx="3" fill="#EF4444"/>')
    a(f'<text x="{mx+mw/2}" y="{my+87}" text-anchor="middle" class="chip">TEST</text>')
    # lever
    a(f'<rect x="{mx+55}" y="{my+110}" width="40" height="85" rx="5" fill="#E5E7EB" stroke="#374151" stroke-width="1.3"/>')
    a(f'<rect x="{mx+58}" y="{my+114}" width="34" height="38" rx="4" fill="#22C55E"/>')
    a(f'<text x="{mx+mw/2}" y="{my+175}" text-anchor="middle" style="font:700 11px DejaVu Sans,Arial;fill:#166534">I</text>')
    a(f'<text x="{mx+mw/2}" y="{my+205}" text-anchor="middle" class="h2">ON</text>')
    a(f'<text x="{mx+mw/2}" y="{my+235}" text-anchor="middle" class="h2">Tipo A</text>')
    # bottom terminals
    terminal_block(a, mx + 18, my + mh - 16, ["L", "N"], mw - 36)
    # clip on DIN
    a(f'<rect x="{mx+20}" y="{din_y-4}" width="{mw-40}" height="12" rx="2" fill="#9CA3AF"/>')

    # Alimentazione: ingresso alto RCBO (lato linea), uscita basso (lato carico)
    l_bus_y = din_y + 90
    n_bus_y = iy + ih - 130
    lx_in, nx_in = mx + 45, mx + 105
    # L/N rete dalla canalina inferiore, salgono lateralmente e entrano dall'alto
    a(f'<path d="M{lx_in-35} {iy+ih-72} V {my-50} H {lx_in} V {my}" fill="none" stroke="{L_COL}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<path d="M{nx_in+35} {iy+ih-72} V {my-50} H {nx_in} V {my}" fill="none" stroke="{N_COL}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<rect x="{lx_in-60}" y="{iy+ih-95}" width="50" height="18" rx="3" fill="#FEF3C7" stroke="{L_COL}"/>')
    a(f'<text x="{lx_in-35}" y="{iy+ih-82}" text-anchor="middle" class="l">L rete</text>')
    a(f'<rect x="{nx_in+10}" y="{iy+ih-95}" width="50" height="18" rx="3" fill="#DBEAFE" stroke="{N_COL}"/>')
    a(f'<text x="{nx_in+35}" y="{iy+ih-82}" text-anchor="middle" class="n">N rete</text>')
    # Uscite protette → BUS
    a(f'<path d="M{lx_in} {my+mh} V {l_bus_y} H {ix+iw-80}" fill="none" stroke="{L_COL}" stroke-width="4.5" stroke-linecap="round"/>')
    a(f'<path d="M{nx_in} {my+mh} V {n_bus_y} H {ix+iw-80}" fill="none" stroke="{N_COL}" stroke-width="4.5" stroke-linecap="round"/>')
    a(f'<rect x="{ix+iw-160}" y="{l_bus_y-12}" width="70" height="24" rx="4" fill="#FEF3C7" stroke="{L_COL}"/>')
    a(f'<text x="{ix+iw-125}" y="{l_bus_y+5}" text-anchor="middle" class="l">BUS L</text>')
    a(f'<rect x="{ix+iw-160}" y="{n_bus_y-12}" width="70" height="24" rx="4" fill="#DBEAFE" stroke="{N_COL}"/>')
    a(f'<text x="{ix+iw-125}" y="{n_bus_y+5}" text-anchor="middle" class="n">BUS N</text>')
    a(f'<path d="M{ix+iw-100} {top_n_y} V {n_bus_y}" fill="none" stroke="{N_COL}" stroke-width="4" stroke-linecap="round"/>')

    def draw_shelly(x, title, eth_label, mapping):
        y = din_y - 280
        w, h = 460, 300
        # Corpo plastica grigio chiaro (Shelly Pro reale)
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#shellyBody)" stroke="#6B7280" stroke-width="1.5" filter="url(#depth)"/>')
        a(f'<rect x="{x+3}" y="{y+3}" width="6" height="{h-6}" rx="2" fill="#CBD5E1"/>')
        a(f'<rect x="{x}" y="{y}" width="30" height="{h}" fill="#D8DCE2" stroke="#9CA3AF"/>')
        for i, ch in enumerate("Shelly"):
            a(f'<text x="{x+15}" y="{y+75+i*24}" text-anchor="middle" class="vert">{ch}</text>')
        # Viti angolo
        screw(a, x + 42, y + 18, 2.4)
        screw(a, x + w - 14, y + 18, 2.4)
        screw(a, x + 42, y + h - 40, 2.4)
        screw(a, x + w - 14, y + h - 40, 2.4)

        a(f'<rect x="{x+42}" y="{y+40}" width="{w-56}" height="155" rx="6" fill="#EEF1F4" stroke="#C5CAD3"/>')
        sx, sy, sw, sh = x + 100, y + 52, 240, 82
        a(f'<rect x="{sx-4}" y="{sy-4}" width="{sw+8}" height="{sh+8}" rx="5" fill="#9CA3AF"/>')
        a(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="3" fill="{SCREEN_BG}"/>')
        # scanline leggera sul display
        for i in range(0, int(sh), 4):
            a(f'<line x1="{sx}" y1="{sy+i}" x2="{sx+sw}" y2="{sy+i}" stroke="#243044" stroke-width="1" opacity="0.35"/>')
        a(f'<text x="{sx+sw/2}" y="{sy+26}" text-anchor="middle" class="scr">{title}</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+46}" text-anchor="middle" class="scr2">Pro 4PM · 4×16A metering</text>')
        a(f'<text x="{sx+14}" y="{sy+68}" class="scr2" style="fill:#22C55E">● online</text>')
        a(f'<text x="{sx+sw-14}" y="{sy+68}" text-anchor="end" class="scr2" style="fill:#38BDF8">{eth_label}</text>')

        for i, lab in enumerate(["▲", "▼", "OK"]):
            bx = sx + 40 + i * 60
            by = sy + sh + 14
            a(f'<rect x="{bx}" y="{by}" width="50" height="28" rx="5" fill="#E5E7EB" stroke="#6B7280"/>')
            a(f'<rect x="{bx+2}" y="{by+2}" width="46" height="11" rx="2" fill="#F9FAFB"/>')
            a(f'<text x="{bx+25}" y="{by+20}" text-anchor="middle" style="font:700 11px DejaVu Sans,Arial;fill:#374151">{lab}</text>')

        # Morsetti superiori O4 O3 L O2 O1
        top_labels = ["O4", "O3", "L", "O2", "O1"]
        term_w = w - 55
        term_x0 = x + 42
        slot = term_w / 5
        a(f'<rect x="{term_x0}" y="{y-8}" width="{term_w}" height="22" rx="2" fill="#4B5563"/>')
        term_xs = {}
        for i, lab in enumerate(top_labels):
            tx = term_x0 + slot * (i + 0.5)
            term_xs[lab] = tx
            a(f'<rect x="{tx-15}" y="{y-7}" width="30" height="20" rx="2" fill="#9CA3AF"/>')
            screw(a, tx, y + 3, 3.4)
            color = L_COL if lab == "L" else "#111827"
            a(f'<text x="{tx}" y="{y+30}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:{color}">{lab}</text>')

        bot_y = y + h - 16
        draw_rj45(a, x + 42, bot_y - 10)
        a(f'<text x="{x+62}" y="{bot_y+30}" text-anchor="middle" class="h2">LAN</text>')
        nx = x + 120
        a(f'<rect x="{nx-14}" y="{bot_y-6}" width="28" height="18" rx="2" fill="#9CA3AF"/>')
        screw(a, nx, bot_y + 3, 3.2)
        a(f'<text x="{nx}" y="{bot_y-12}" text-anchor="middle" class="n">N</text>')
        for i, lab in enumerate(["S4", "S3", "S2", "S1"]):
            sx_ = x + 185 + i * 58
            a(f'<rect x="{sx_-12}" y="{bot_y-6}" width="24" height="16" rx="2" fill="#9CA3AF" opacity="0.5"/>')
            screw(a, sx_, bot_y + 2, 2.6)
            a(f'<text x="{sx_}" y="{bot_y+28}" text-anchor="middle" class="h2">{lab}</text>')
        a(f'<text x="{x+w-12}" y="{bot_y+44}" text-anchor="end" class="h2">S1–S4 non collegati</text>')
        a(f'<rect x="{x+42}" y="{din_y-4}" width="{w-60}" height="12" rx="2" fill="#9CA3AF"/>')

        a(f'<path d="M{term_xs["L"]} {y} V {l_bus_y}" fill="none" stroke="{L_COL}" stroke-width="3.8"/>')
        a(f'<circle cx="{term_xs["L"]}" cy="{l_bus_y}" r="4.5" fill="{L_COL}"/>')
        a(f'<path d="M{nx} {y+h} V {n_bus_y}" fill="none" stroke="{N_COL}" stroke-width="3.8"/>')
        a(f'<circle cx="{nx}" cy="{n_bus_y}" r="4.5" fill="{N_COL}"/>')
        draw_eth_cable(a, x + 62, y + h + 20, x + 130, y + h + 78, eth_label)

        # MCB canale nella fascia canalina, card carichi sopra
        for idx, out in enumerate(("O4", "O3", "O2", "O1")):
            num, name, icon = mapping[out]
            tx = term_xs[out]
            mcb_y = duct_y + 16
            a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{mcb_y+28}" stroke="#111827" stroke-width="2.8"/>')
            draw_mcb_fuse(a, tx, mcb_y)
            stagger = (idx % 2) * 58
            card_y = top_n_y + 28 + stagger
            a(f'<line x1="{tx}" y1="{mcb_y-28}" x2="{tx}" y2="{card_y+102}" stroke="#111827" stroke-width="2.8"/>')
            a(f'<line x1="{tx}" y1="{top_n_y}" x2="{tx}" y2="{card_y}" stroke="{N_COL}" stroke-width="2.6"/>')
            a(f'<circle cx="{tx}" cy="{top_n_y}" r="3.8" fill="{N_COL}"/>')

            cw, ch = 118, 102
            a(f'<rect x="{tx-cw/2}" y="{card_y}" width="{cw}" height="{ch}" rx="8" fill="#FFFFFF" stroke="#9CA3AF" stroke-width="1.3" filter="url(#depth)"/>')
            a(f'<circle cx="{tx-cw/2+17}" cy="{card_y+17}" r="12" fill="{ACCENT}"/>')
            a(f'<text x="{tx-cw/2+17}" y="{card_y+21}" text-anchor="middle" class="chip">{num}</text>')
            a(f'<text x="{tx+16}" y="{card_y+21}" text-anchor="middle" class="h2">{out}</text>')
            ICONS[icon](a, tx, card_y + 56, 1.0)
            words = name.split()
            if len(name) > 13 and len(words) > 1:
                mid = max(1, len(words) // 2)
                a(f'<text x="{tx}" y="{card_y+ch+14}" text-anchor="middle" class="name">{esc(" ".join(words[:mid]))}</text>')
                a(f'<text x="{tx}" y="{card_y+ch+28}" text-anchor="middle" class="name">{esc(" ".join(words[mid:]))}</text>')
            else:
                a(f'<text x="{tx}" y="{card_y+ch+16}" text-anchor="middle" class="name">{esc(name)}</text>')

    draw_shelly(ix + 250, "SHELLY #1", "ETH 1", SHELLY1)
    draw_shelly(ix + 780, "SHELLY #2", "ETH 2", SHELLY2)

    # PE bar optional small
    a(f'<rect x="{ix+40}" y="{n_bus_y+30}" width="220" height="14" rx="3" fill="{PE_COL}"/>')
    a(f'<text x="{ix+150}" y="{n_bus_y+55}" text-anchor="middle" style="font:700 11px DejaVu Sans,Arial;fill:#854D0E">BARRA PE (giallo/verde)</text>')

    # Legend outside cabinet bottom
    ly = cab_y + cab_h + 15
    a(f'<rect x="50" y="{ly}" width="{W-100}" height="130" rx="8" fill="#F9FAFB" filter="url(#depth)"/>')
    a(f'<text x="70" y="{ly+28}" class="h">Legenda carichi</text>')
    legend = [
        (1, "Lavastoviglie", "#1 · O1", "dishwasher"),
        (2, "Microonde", "#1 · O2", "microwave"),
        (3, "Forno", "#1 · O3", "oven"),
        (4, "Frigorifero", "#1 · O4", "fridge"),
        (5, "Piano cottura", "#2 · O1", "cooktop"),
        (6, "Prese piano cottura", "#2 · O2", "socket"),
        (7, "Prese piano lavoro", "#2 · O3", "socket"),
        (8, "Prese interno mobile", "#2 · O4", "socket"),
    ]
    for i, (num, name, path, icon) in enumerate(legend):
        x = 70 + i * 245
        y = ly + 45
        a(f'<rect x="{x}" y="{y}" width="230" height="55" rx="8" fill="#F3F4F6" stroke="#D1D5DB"/>')
        a(f'<circle cx="{x+18}" cy="{y+28}" r="12" fill="{ACCENT}"/>')
        a(f'<text x="{x+18}" y="{y+32}" text-anchor="middle" class="chip">{num}</text>')
        ICONS[icon](a, x + 48, y + 28, 0.55)
        a(f'<text x="{x+75}" y="{y+24}" class="leg">{esc(name)}</text>')
        a(f'<text x="{x+75}" y="{y+42}" class="leg-m">Shelly {esc(path)}</text>')

    a(f'<text x="70" y="{ly+120}" class="warn">Limiti Pro 4PM: 16 A/canale, 40 A totali — verificare forno e piano cottura in opera.</text>')

    a("</svg>")
    return "\n".join(p)


def main() -> None:
    svg = build_svg()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    for path in (OUT_DIR / "quadro-elettrico-cucina.svg", ART_DIR / "quadro-elettrico-cucina.svg"):
        path.write_text(svg, encoding="utf-8")
    for path in (OUT_DIR / "quadro-elettrico-cucina.png", ART_DIR / "quadro-elettrico-cucina.png"):
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), scale=1.2)
    print("OK", ART_DIR / "quadro-elettrico-cucina.png")


if __name__ == "__main__":
    main()
