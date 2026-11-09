#!/usr/bin/env python3
"""Quadro cucina — schema ad alta fedeltà (armadio, DIN, RCBO, Shelly Pro 4PM)."""

from pathlib import Path

import cairosvg

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 2300, 1750
L = "#7A3E1D"      # marrone IEC
N = "#1E40AF"      # blu IEC
PE = "#A16207"
INK = "#0F172A"
ACC = "#0F4C81"

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


def screw(a, cx, cy, r=3.6):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r+1.2}" fill="#4B5563"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#steel)"/>')
    a(f'<line x1="{cx-r*0.55}" y1="{cy}" x2="{cx+r*0.55}" y2="{cy}" stroke="#1F2937" stroke-width="1.2"/>')
    a(f'<line x1="{cx}" y1="{cy-r*0.55}" x2="{cx}" y2="{cy+r*0.55}" stroke="#1F2937" stroke-width="1.2"/>')
    a(f'<circle cx="{cx-r*0.25}" cy="{cy-r*0.25}" r="{r*0.2}" fill="#F9FAFB" opacity="0.55"/>')


def ferrule(a, x, y, color):
    """Puntale ferrula rame + guaina."""
    a(f'<rect x="{x-4}" y="{y-7}" width="8" height="10" rx="1" fill="{color}"/>')
    a(f'<rect x="{x-3}" y="{y+2}" width="6" height="7" rx="0.8" fill="#D97706"/>')
    a(f'<rect x="{x-2.2}" y="{y+3}" width="4.4" height="2" fill="#FBBF24" opacity="0.7"/>')


def wire_tag(a, x, y, text):
    a(f'<rect x="{x-12}" y="{y-9}" width="24" height="18" rx="2" fill="#F8FAFC" stroke="#64748B"/>')
    a(f'<text x="{x}" y="{y+4}" text-anchor="middle" style="font:700 10px DejaVu Sans,Arial;fill:#0F172A">{text}</text>')


def cable_tie(a, x, y):
    a(f'<rect x="{x-7}" y="{y-3}" width="14" height="6" rx="2" fill="#111827"/>')
    a(f'<rect x="{x-5}" y="{y-1.5}" width="10" height="3" rx="1" fill="#374151"/>')


# ---- icone prodotto ----
def icon_dishwasher(a, cx, cy, s=1.0):
    x, y = cx - 20 * s, cy - 24 * s
    a(f'<rect x="{x}" y="{y}" width="{40*s}" height="{48*s}" rx="{4*s}" fill="url(#applWhite)" stroke="#374151" stroke-width="1.4"/>')
    a(f'<rect x="{x+3*s}" y="{y+3*s}" width="{34*s}" height="{9*s}" rx="{2*s}" fill="#6B7280"/>')
    a(f'<circle cx="{cx+11*s}" cy="{y+7.5*s}" r="{2.1*s}" fill="#93C5FD"/>')
    a(f'<rect x="{x+6*s}" y="{y+16*s}" width="{28*s}" height="{24*s}" rx="{2*s}" fill="#F8FAFC" stroke="#9CA3AF"/>')
    a(f'<path d="M{x+10*s} {y+28*s} q {10*s} {11*s} {20*s} 0" fill="none" stroke="#2563EB" stroke-width="{1.7*s}"/>')
    a(f'<path d="M{x+13*s} {y+25*s} q {7*s} {7*s} {14*s} 0" fill="none" stroke="#93C5FD" stroke-width="{1.3*s}"/>')


def icon_microwave(a, cx, cy, s=1.0):
    x, y = cx - 24 * s, cy - 17 * s
    a(f'<rect x="{x}" y="{y}" width="{48*s}" height="{34*s}" rx="{3*s}" fill="url(#applWhite)" stroke="#374151" stroke-width="1.4"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{26*s}" height="{26*s}" rx="{2*s}" fill="#0F172A"/>')
    a(f'<rect x="{x+8*s}" y="{y+8*s}" width="{18*s}" height="{18*s}" rx="{1*s}" fill="#1E293B" stroke="#475569"/>')
    a(f'<rect x="{x+33*s}" y="{y+4*s}" width="{11*s}" height="{26*s}" rx="{2*s}" fill="#F8FAFC" stroke="#9CA3AF"/>')
    a(f'<circle cx="{x+38.5*s}" cy="{y+12*s}" r="{2.3*s}" fill="#374151"/>')
    a(f'<circle cx="{x+38.5*s}" cy="{y+21*s}" r="{2.3*s}" fill="#374151"/>')


def icon_oven(a, cx, cy, s=1.0):
    x, y = cx - 20 * s, cy - 24 * s
    a(f'<rect x="{x}" y="{y}" width="{40*s}" height="{48*s}" rx="{3*s}" fill="url(#applWhite)" stroke="#374151" stroke-width="1.4"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{32*s}" height="{8*s}" rx="{2*s}" fill="#4B5563"/>')
    a(f'<circle cx="{cx-7*s}" cy="{y+8*s}" r="{2*s}" fill="#E5E7EB"/>')
    a(f'<circle cx="{cx+7*s}" cy="{y+8*s}" r="{2*s}" fill="#E5E7EB"/>')
    a(f'<rect x="{x+5*s}" y="{y+16*s}" width="{30*s}" height="{25*s}" rx="{2*s}" fill="#0F172A"/>')
    a(f'<rect x="{x+9*s}" y="{y+20*s}" width="{22*s}" height="{14*s}" rx="{1*s}" fill="#1E293B" stroke="#F59E0B"/>')
    a(f'<line x1="{x+11*s}" y1="{y+27*s}" x2="{x+29*s}" y2="{y+27*s}" stroke="#FBBF24" stroke-width="1.3"/>')


def icon_fridge(a, cx, cy, s=1.0):
    x, y = cx - 16 * s, cy - 26 * s
    a(f'<rect x="{x}" y="{y}" width="{32*s}" height="{52*s}" rx="{3*s}" fill="url(#applWhite)" stroke="#374151" stroke-width="1.4"/>')
    a(f'<line x1="{x}" y1="{y+17*s}" x2="{x+32*s}" y2="{y+17*s}" stroke="#6B7280" stroke-width="1.4"/>')
    a(f'<rect x="{x+25*s}" y="{y+5*s}" width="{3*s}" height="{8*s}" rx="{1*s}" fill="#374151"/>')
    a(f'<rect x="{x+25*s}" y="{y+24*s}" width="{3*s}" height="{14*s}" rx="{1*s}" fill="#374151"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{10*s}" height="{3*s}" rx="{1*s}" fill="#93C5FD" opacity="0.75"/>')


def icon_cooktop(a, cx, cy, s=1.0):
    x, y = cx - 24 * s, cy - 17 * s
    a(f'<rect x="{x}" y="{y}" width="{48*s}" height="{34*s}" rx="{3*s}" fill="#111827" stroke="#020617" stroke-width="1.4"/>')
    for dx, dy, r in ((-9, -4, 6.5), (9, -4, 5.5), (-9, 8, 5.5), (9, 8, 6.5)):
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{r*s}" fill="none" stroke="#F59E0B" stroke-width="1.8"/>')
        a(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{(r-2.8)*s}" fill="#F59E0B" opacity="0.28"/>')


def icon_socket(a, cx, cy, s=1.0):
    x, y = cx - 17 * s, cy - 17 * s
    a(f'<rect x="{x}" y="{y}" width="{34*s}" height="{34*s}" rx="{4*s}" fill="url(#applWhite)" stroke="#374151" stroke-width="1.4"/>')
    a(f'<rect x="{x+4*s}" y="{y+4*s}" width="{26*s}" height="{26*s}" rx="{3*s}" fill="#E5E7EB" stroke="#9CA3AF"/>')
    a(f'<circle cx="{cx-5*s}" cy="{cy-1*s}" r="{2.8*s}" fill="#0F172A"/>')
    a(f'<circle cx="{cx+5*s}" cy="{cy-1*s}" r="{2.8*s}" fill="#0F172A"/>')
    a(f'<path d="M{cx-5*s} {cy+9*s} a 5 {5*s} 0 0 0 {10*s} 0" fill="none" stroke="#0F172A" stroke-width="1.7"/>')


ICONS = {
    "dishwasher": icon_dishwasher,
    "microwave": icon_microwave,
    "oven": icon_oven,
    "fridge": icon_fridge,
    "cooktop": icon_cooktop,
    "socket": icon_socket,
}


def draw_mcb(a, cx, cy):
    """MCB monofase 16A realistico."""
    a(f'<rect x="{cx-16}" y="{cy-32}" width="32" height="64" rx="3" fill="url(#plastic)" stroke="#6B7280" stroke-width="1.2" filter="url(#soft)"/>')
    a(f'<rect x="{cx-12}" y="{cy-28}" width="24" height="12" rx="2" fill="#FEF2F2" stroke="#EF4444"/>')
    a(f'<text x="{cx}" y="{cy-19}" text-anchor="middle" style="font:700 8px DejaVu Sans,Arial;fill:#B91C1C">16A</text>')
    a(f'<rect x="{cx-6}" y="{cy-10}" width="12" height="28" rx="2.5" fill="#E5E7EB" stroke="#374151"/>')
    a(f'<rect x="{cx-5}" y="{cy-8}" width="10" height="12" rx="2" fill="#22C55E"/>')
    a(f'<text x="{cx}" y="{cy+26}" text-anchor="middle" style="font:700 8px DejaVu Sans,Arial;fill:#166534">I</text>')
    screw(a, cx, cy - 30, 2.3)
    screw(a, cx, cy + 26, 2.3)


def draw_rj45(a, x, y):
    a(f'<rect x="{x}" y="{y}" width="44" height="28" rx="2" fill="#0F172A" stroke="#020617"/>')
    a(f'<rect x="{x+4}" y="{y+4}" width="36" height="17" rx="1" fill="#334155"/>')
    for i in range(8):
        a(f'<rect x="{x+7+i*4}" y="{y+6}" width="2.4" height="11" fill="#CBD5E1"/>')
    a(f'<rect x="{x+15}" y="{y+21}" width="14" height="5" fill="#475569"/>')


def draw_eth(a, x1, y1, x2, y2, label):
    a(f'<rect x="{x1-10}" y="{y1}" width="20" height="12" rx="2" fill="#1E3A8A"/>')
    a(f'<rect x="{x1-7}" y="{y1+2}" width="14" height="6" fill="#60A5FA"/>')
    a(f'<path d="M{x1} {y1+12} C {x1} {y1+40}, {x1+20} {y2}, {x2} {y2}" fill="none" stroke="#1E3A8A" stroke-width="5" stroke-linecap="round"/>')
    a(f'<path d="M{x1} {y1+12} C {x1} {y1+40}, {x1+20} {y2}, {x2} {y2}" fill="none" stroke="#93C5FD" stroke-width="1.4" stroke-dasharray="3 4"/>')
    a(f'<rect x="{x2}" y="{y2-14}" width="58" height="28" rx="4" fill="#0F172A"/>')
    a(f'<text x="{x2+29}" y="{y2+5}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:#F8FAFC">{label}</text>')


def build_svg() -> str:
    p: list[str] = []
    a = p.append

    a(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="perf" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="7" cy="7" r="1.6" fill="#94A3B8" opacity="0.45"/>
    </pattern>
    <pattern id="brush" width="6" height="40" patternUnits="userSpaceOnUse">
      <rect width="6" height="40" fill="#9CA3AF"/>
      <rect x="0" y="0" width="1" height="40" fill="#D1D5DB" opacity="0.35"/>
      <rect x="3" y="0" width="1" height="40" fill="#6B7280" opacity="0.25"/>
    </pattern>
    <linearGradient id="cab" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E5E7EB"/><stop offset="100%" stop-color="#6B7280"/>
    </linearGradient>
    <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F3F4F6"/><stop offset="55%" stop-color="#9CA3AF"/><stop offset="100%" stop-color="#6B7280"/>
    </linearGradient>
    <linearGradient id="plastic" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/><stop offset="55%" stop-color="#F3F4F6"/><stop offset="100%" stop-color="#D1D5DB"/>
    </linearGradient>
    <linearGradient id="shelly" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAFBFC"/><stop offset="45%" stop-color="#E8EAED"/><stop offset="100%" stop-color="#C5CAD3"/>
    </linearGradient>
    <linearGradient id="din" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/><stop offset="40%" stop-color="#CBD5E1"/>
      <stop offset="55%" stop-color="#64748B"/><stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <linearGradient id="applWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <filter id="soft" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.2" flood-color="#0F172A" flood-opacity="0.28"/>
    </filter>
    <filter id="glow">
      <feDropShadow dx="0" dy="0" stdDeviation="1.2" flood-color="#38BDF8" flood-opacity="0.55"/>
    </filter>
    <style><![CDATA[
      .title {{ font:700 36px DejaVu Sans,Arial; fill:#0F172A; }}
      .sub {{ font:400 13px DejaVu Sans,Arial; fill:#475569; }}
      .h {{ font:700 13px DejaVu Sans,Arial; fill:#0F172A; }}
      .h2 {{ font:600 10px DejaVu Sans,Arial; fill:#64748B; }}
      .name {{ font:700 11px DejaVu Sans,Arial; fill:#0F172A; }}
      .note {{ font:400 12px DejaVu Sans,Arial; fill:#475569; }}
      .leg {{ font:600 12px DejaVu Sans,Arial; fill:#0F172A; }}
      .legm {{ font:400 11px DejaVu Sans,Arial; fill:#64748B; }}
      .warn {{ font:500 12px DejaVu Sans,Arial; fill:#92400E; }}
      .chip {{ font:700 11px DejaVu Sans,Arial; fill:#fff; }}
      .scr {{ font:700 13px DejaVu Sans,Arial; fill:#7DD3FC; }}
      .scr2 {{ font:500 10px DejaVu Sans,Arial; fill:#94A3B8; }}
      .l {{ font:700 11px DejaVu Sans,Arial; fill:{L}; }}
      .n {{ font:700 11px DejaVu Sans,Arial; fill:{N}; }}
      .vert {{ font:700 13px DejaVu Sans,Arial; fill:#334155; }}
    ]]></style>
  </defs>
  <rect width="100%" height="100%" fill="#64748B"/>
''')

    # Header
    a(f'<rect x="40" y="36" width="{W-80}" height="82" rx="8" fill="#F8FAFC" filter="url(#soft)"/>')
    a(f'<text x="64" y="74" class="title">Quadro elettrico cucina</text>')
    a(f'<text x="64" y="98" class="sub">Vista frontale ad alta fedeltà · armadio DIN · RCBO · 2× Shelly Pro 4PM · cavi IEC con ferrule</text>')
    for x, col, lab in ((1750, L, "L fase"), (1860, N, "N neutro"), (1980, "#1E3A8A", "ETH"), (2085, PE, "PE")):
        a(f'<rect x="{x}" y="58" width="14" height="14" rx="3" fill="{col}"/>')
        a(f'<text x="{x+22}" y="70" class="note">{lab}</text>')

    # Armadio
    cx0, cy0, cw, ch = 40, 135, W - 80, 1380
    a(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="12" fill="url(#cab)" stroke="#334155" stroke-width="4" filter="url(#soft)"/>')
    # cerniere
    for hy in (cy0 + 90, cy0 + ch / 2, cy0 + ch - 110):
        a(f'<rect x="{cx0-8}" y="{hy}" width="16" height="42" rx="3" fill="url(#steel)" stroke="#1F2937"/>')
        screw(a, cx0, hy + 12, 2.4)
        screw(a, cx0, hy + 30, 2.4)
    # maniglia
    a(f'<rect x="{cx0+cw-18}" y="{cy0+ch/2-50}" width="12" height="100" rx="4" fill="url(#steel)" stroke="#1F2937"/>')

    # vasca interna + piastra forata
    ix, iy, iw, ih = cx0 + 26, cy0 + 26, cw - 52, ch - 52
    a(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="5" fill="#CBD5E1" stroke="#64748B"/>')
    a(f'<rect x="{ix+10}" y="{iy+10}" width="{iw-20}" height="{ih-20}" fill="#E2E8F0"/>')
    a(f'<rect x="{ix+10}" y="{iy+10}" width="{iw-20}" height="{ih-20}" fill="url(#perf)"/>')

    # Feritoie aerazione
    for i in range(16):
        a(f'<rect x="{ix+50+i*55}" y="{iy+16}" width="32" height="5" rx="1.5" fill="#94A3B8"/>')

    top_n = iy + 58
    # Morsettiera N blu realistica
    a(f'<rect x="{ix+50}" y="{top_n-10}" width="{iw-220}" height="20" rx="3" fill="{N}" stroke="#1E3A8A"/>')
    for i in range(18):
        screw(a, ix + 70 + i * 55, top_n, 2.5)
    a(f'<rect x="{ix+iw-155}" y="{top_n-16}" width="110" height="32" rx="5" fill="#DBEAFE" stroke="{N}" stroke-width="1.5"/>')
    a(f'<text x="{ix+iw-100}" y="{top_n+5}" text-anchor="middle" class="n">MORSETTIERA N</text>')

    # Canalina intermedia (aperta)
    duct_y = iy + 265
    a(f'<rect x="{ix+30}" y="{duct_y}" width="{iw-60}" height="40" rx="3" fill="#78716C" stroke="#57534E"/>')
    a(f'<rect x="{ix+34}" y="{duct_y+4}" width="{iw-68}" height="22" rx="2" fill="#A8A29E"/>')
    # coperchio sollevato
    a(f'<rect x="{ix+34}" y="{duct_y-16}" width="{iw-68}" height="14" rx="2" fill="#D6D3D1" stroke="#78716C" transform="rotate(-4 {ix+34} {duct_y})"/>')
    a(f'<text x="{ix+50}" y="{duct_y+20}" class="h2" style="fill:#44403C">Canalina porta-cavi · MCB 16A di canale</text>')

    # DIN rail profilo Omega
    din_y = iy + 600
    a(f'<rect x="{ix+35}" y="{din_y}" width="{iw-70}" height="38" rx="2" fill="url(#din)" stroke="#334155"/>')
    a(f'<rect x="{ix+35}" y="{din_y+8}" width="{iw-70}" height="6" fill="#F8FAFC" opacity="0.55"/>')
    a(f'<rect x="{ix+35}" y="{din_y+24}" width="{iw-70}" height="5" fill="#1E293B" opacity="0.35"/>')
    a(f'<text x="{ix+50}" y="{din_y+62}" class="h2">Guida DIN EN 60715 · 35 mm (profilo a Ω)</text>')

    # Canalina inferiore
    a(f'<rect x="{ix+30}" y="{iy+ih-100}" width="{iw-60}" height="40" rx="3" fill="#78716C" stroke="#57534E"/>')
    a(f'<rect x="{ix+34}" y="{iy+ih-96}" width="{iw-68}" height="22" rx="2" fill="#A8A29E"/>')
    a(f'<text x="{ix+50}" y="{iy+ih-80}" class="h2" style="fill:#44403C">Canalina inferiore · L/N rete + Ethernet</text>')

    # ===== RCBO =====
    mx, my, mw, mh = ix + 45, din_y - 300, 170, 320
    a(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="4" fill="url(#plastic)" stroke="#64748B" stroke-width="1.4" filter="url(#soft)"/>')
    # highlight bordo
    a(f'<rect x="{mx+3}" y="{my+3}" width="4" height="{mh-6}" rx="1" fill="#FFFFFF" opacity="0.7"/>')
    a(f'<rect x="{mx+12}" y="{my+10}" width="{mw-24}" height="48" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>')
    a(f'<text x="{mx+mw/2}" y="{my+30}" text-anchor="middle" class="h">RCBO</text>')
    a(f'<text x="{mx+mw/2}" y="{my+48}" text-anchor="middle" class="h2">2P · 40A · 30mA · Tipo A</text>')

    # morsetti alto
    for i, lab in enumerate(["L", "N"]):
        tx = mx + 45 + i * 80
        a(f'<rect x="{tx-16}" y="{my-8}" width="32" height="20" rx="2" fill="#6B7280"/>')
        screw(a, tx, my + 2, 3.4)
        a(f'<text x="{tx}" y="{my+28}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:{"#7A3E1D" if lab=="L" else "#1E40AF"}">{lab}</text>')

    a(f'<rect x="{mx+22}" y="{my+70}" width="{mw-44}" height="175" rx="5" fill="#FFFFFF" stroke="#CBD5E1"/>')
    a(f'<rect x="{mx+40}" y="{my+82}" width="{mw-80}" height="26" rx="4" fill="#DC2626"/>')
    a(f'<text x="{mx+mw/2}" y="{my+100}" text-anchor="middle" class="chip">TEST</text>')
    # leva
    a(f'<rect x="{mx+60}" y="{my+125}" width="50" height="95" rx="6" fill="#E2E8F0" stroke="#334155" stroke-width="1.3"/>')
    a(f'<rect x="{mx+64}" y="{my+130}" width="42" height="42" rx="5" fill="#22C55E"/>')
    a(f'<circle cx="{mx+85}" cy="{my+145}" r="4" fill="#BBF7D0"/>')
    a(f'<text x="{mx+mw/2}" y="{my+195}" text-anchor="middle" style="font:700 14px DejaVu Sans,Arial;fill:#166534">I</text>')
    a(f'<text x="{mx+mw/2}" y="{my+225}" text-anchor="middle" class="h2">ON</text>')
    a(f'<text x="{mx+mw/2}" y="{my+255}" text-anchor="middle" class="h2">Icn 6 kA</text>')

    for i, lab in enumerate(["L", "N"]):
        tx = mx + 45 + i * 80
        a(f'<rect x="{tx-16}" y="{my+mh-14}" width="32" height="20" rx="2" fill="#6B7280"/>')
        screw(a, tx, my + mh - 4, 3.4)

    # clip DIN
    a(f'<rect x="{mx+25}" y="{din_y-5}" width="{mw-50}" height="14" rx="2" fill="#94A3B8"/>')
    a(f'<path d="M{mx+40} {din_y+9} h {mw-80}" stroke="#64748B" stroke-width="2"/>')

    l_bus = din_y + 95
    n_bus = iy + ih - 145
    lx, nx = mx + 45, mx + 125

    # Ingresso rete: dal basso, laterale, entra in alto RCBO
    a(f'<path d="M{lx-40} {iy+ih-80} V {my-55} H {lx} V {my}" fill="none" stroke="{L}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    a(f'<path d="M{nx+40} {iy+ih-80} V {my-55} H {nx} V {my}" fill="none" stroke="{N}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    ferrule(a, lx, my - 2, L)
    ferrule(a, nx, my - 2, N)
    wire_tag(a, lx - 40, iy + ih - 55, "L")
    wire_tag(a, nx + 40, iy + ih - 55, "N")
    a(f'<rect x="{lx-65}" y="{iy+ih-105}" width="50" height="18" rx="3" fill="#FEF3C7" stroke="{L}"/>')
    a(f'<text x="{lx-40}" y="{iy+ih-92}" text-anchor="middle" class="l">L rete</text>')
    a(f'<rect x="{nx+15}" y="{iy+ih-105}" width="50" height="18" rx="3" fill="#DBEAFE" stroke="{N}"/>')
    a(f'<text x="{nx+40}" y="{iy+ih-92}" text-anchor="middle" class="n">N rete</text>')
    cable_tie(a, lx - 40, my + 40)
    cable_tie(a, nx + 40, my + 40)

    # Uscite → bus
    a(f'<path d="M{lx} {my+mh} V {l_bus} H {ix+iw-90}" fill="none" stroke="{L}" stroke-width="5.5" stroke-linecap="round"/>')
    a(f'<path d="M{nx} {my+mh} V {n_bus} H {ix+iw-90}" fill="none" stroke="{N}" stroke-width="5.5" stroke-linecap="round"/>')
    ferrule(a, lx, my + mh + 2, L)
    ferrule(a, nx, my + mh + 2, N)
    a(f'<rect x="{ix+iw-175}" y="{l_bus-14}" width="78" height="28" rx="5" fill="#FEF3C7" stroke="{L}"/>')
    a(f'<text x="{ix+iw-136}" y="{l_bus+5}" text-anchor="middle" class="l">BUS L</text>')
    a(f'<rect x="{ix+iw-175}" y="{n_bus-14}" width="78" height="28" rx="5" fill="#DBEAFE" stroke="{N}"/>')
    a(f'<text x="{ix+iw-136}" y="{n_bus+5}" text-anchor="middle" class="n">BUS N</text>')
    a(f'<path d="M{ix+iw-110} {top_n} V {n_bus}" fill="none" stroke="{N}" stroke-width="4.5"/>')

    def draw_shelly(x, title, eth_label, mapping):
        y, w, h = din_y - 300, 490, 320
        # corpo
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#shelly)" stroke="#64748B" stroke-width="1.5" filter="url(#soft)"/>')
        a(f'<rect x="{x+4}" y="{y+4}" width="5" height="{h-8}" rx="1.5" fill="#FFFFFF" opacity="0.65"/>')
        # fascia Shelly verticale
        a(f'<rect x="{x}" y="{y}" width="32" height="{h}" fill="#D1D5DB" stroke="#9CA3AF"/>')
        for i, ch in enumerate("Shelly"):
            a(f'<text x="{x+16}" y="{y+80+i*26}" text-anchor="middle" class="vert">{ch}</text>')
        for sx_, sy_ in ((x + 48, y + 22), (x + w - 18, y + 22), (x + 48, y + h - 48), (x + w - 18, y + h - 48)):
            screw(a, sx_, sy_, 2.5)

        # recess frontale
        a(f'<rect x="{x+46}" y="{y+46}" width="{w-62}" height="165" rx="7" fill="#E9EDF1" stroke="#CBD5E1"/>')
        # LCD con alone
        sx, sy, sw, sh = x + 110, y + 58, 250, 88
        a(f'<rect x="{sx-5}" y="{sy-5}" width="{sw+10}" height="{sh+10}" rx="6" fill="#94A3B8"/>')
        a(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="#0B1220" filter="url(#glow)"/>')
        for i in range(0, int(sh), 3):
            a(f'<line x1="{sx}" y1="{sy+i}" x2="{sx+sw}" y2="{sy+i}" stroke="#1E293B" stroke-width="1" opacity="0.4"/>')
        a(f'<text x="{sx+sw/2}" y="{sy+28}" text-anchor="middle" class="scr">{title}</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+48}" text-anchor="middle" class="scr2">Pro 4PM · 4×16A · metering</text>')
        a(f'<text x="{sx+16}" y="{sy+72}" class="scr2" style="fill:#4ADE80">● online</text>')
        a(f'<text x="{sx+sw-16}" y="{sy+72}" text-anchor="end" class="scr2" style="fill:#38BDF8">{eth_label}</text>')

        for i, lab in enumerate(["▲", "▼", "OK"]):
            bx = sx + 45 + i * 62
            by = sy + sh + 16
            a(f'<rect x="{bx}" y="{by}" width="52" height="30" rx="5" fill="#E5E7EB" stroke="#64748B"/>')
            a(f'<rect x="{bx+2}" y="{by+2}" width="48" height="12" rx="2" fill="#F8FAFC"/>')
            a(f'<text x="{bx+26}" y="{by+22}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:#334155">{lab}</text>')

        # LED canali
        for i in range(4):
            a(f'<circle cx="{x+55+i*16}" cy="{y+70}" r="4" fill="#22C55E"/>')
            a(f'<circle cx="{x+55+i*16}" cy="{y+70}" r="2" fill="#BBF7D0"/>')

        # Morsetti top O4 O3 L O2 O1
        labels = ["O4", "O3", "L", "O2", "O1"]
        term_x0, term_w = x + 48, w - 66
        slot = term_w / 5
        a(f'<rect x="{term_x0}" y="{y-10}" width="{term_w}" height="24" rx="2" fill="#475569"/>')
        txs = {}
        for i, lab in enumerate(labels):
            tx = term_x0 + slot * (i + 0.5)
            txs[lab] = tx
            a(f'<rect x="{tx-16}" y="{y-9}" width="32" height="22" rx="2" fill="#9CA3AF"/>')
            screw(a, tx, y + 2, 3.5)
            col = L if lab == "L" else "#0F172A"
            a(f'<text x="{tx}" y="{y+32}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:{col}">{lab}</text>')

        # Bottom LAN N S4..S1
        by = y + h - 18
        draw_rj45(a, x + 48, by - 12)
        a(f'<text x="{x+70}" y="{by+32}" text-anchor="middle" class="h2">LAN</text>')
        nx_ = x + 130
        a(f'<rect x="{nx_-15}" y="{by-8}" width="30" height="20" rx="2" fill="#9CA3AF"/>')
        screw(a, nx_, by + 2, 3.3)
        a(f'<text x="{nx_}" y="{by-14}" text-anchor="middle" class="n">N</text>')
        for i, lab in enumerate(["S4", "S3", "S2", "S1"]):
            sx_ = x + 200 + i * 60
            a(f'<rect x="{sx_-13}" y="{by-8}" width="26" height="18" rx="2" fill="#9CA3AF" opacity="0.45"/>')
            screw(a, sx_, by + 1, 2.7)
            a(f'<text x="{sx_}" y="{by+30}" text-anchor="middle" class="h2">{lab}</text>')
        a(f'<text x="{x+w-14}" y="{by+46}" text-anchor="end" class="h2">S1–S4 non collegati</text>')

        # clip DIN
        a(f'<rect x="{x+50}" y="{din_y-5}" width="{w-70}" height="14" rx="2" fill="#94A3B8"/>')

        # Alimentazione
        a(f'<path d="M{txs["L"]} {y} V {l_bus}" fill="none" stroke="{L}" stroke-width="4"/>')
        a(f'<circle cx="{txs["L"]}" cy="{l_bus}" r="5" fill="{L}"/>')
        ferrule(a, txs["L"], y + 2, L)
        a(f'<path d="M{nx_} {y+h} V {n_bus}" fill="none" stroke="{N}" stroke-width="4"/>')
        a(f'<circle cx="{nx_}" cy="{n_bus}" r="5" fill="{N}"/>')
        ferrule(a, nx_, y + h - 2, N)
        draw_eth(a, x + 70, y + h + 22, x + 145, y + h + 85, eth_label)

        # Uscite + MCB + card
        for idx, out in enumerate(("O4", "O3", "O2", "O1")):
            num, name, icon = mapping[out]
            tx = txs[out]
            mcb_y = duct_y + 18
            a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{mcb_y+32}" stroke="#0F172A" stroke-width="3"/>')
            ferrule(a, tx, y + 2, "#0F172A")
            draw_mcb(a, tx, mcb_y)
            stagger = (idx % 2) * 62
            card_y = top_n + 30 + stagger
            a(f'<line x1="{tx}" y1="{mcb_y-32}" x2="{tx}" y2="{card_y+108}" stroke="#0F172A" stroke-width="3"/>')
            a(f'<line x1="{tx}" y1="{top_n}" x2="{tx}" y2="{card_y}" stroke="{N}" stroke-width="2.8"/>')
            a(f'<circle cx="{tx}" cy="{top_n}" r="4" fill="{N}"/>')
            wire_tag(a, tx + 18, (mcb_y + card_y) / 2, str(num))

            cw, chh = 124, 108
            a(f'<rect x="{tx-cw/2}" y="{card_y}" width="{cw}" height="{chh}" rx="10" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.3" filter="url(#soft)"/>')
            a(f'<circle cx="{tx-cw/2+18}" cy="{card_y+18}" r="12" fill="{ACC}"/>')
            a(f'<text x="{tx-cw/2+18}" y="{card_y+22}" text-anchor="middle" class="chip">{num}</text>')
            a(f'<text x="{tx+18}" y="{card_y+22}" text-anchor="middle" class="h2">{out}</text>')
            ICONS[icon](a, tx, card_y + 58, 1.05)
            words = name.split()
            if len(name) > 13 and len(words) > 1:
                mid = max(1, len(words) // 2)
                a(f'<text x="{tx}" y="{card_y+chh+15}" text-anchor="middle" class="name">{esc(" ".join(words[:mid]))}</text>')
                a(f'<text x="{tx}" y="{card_y+chh+30}" text-anchor="middle" class="name">{esc(" ".join(words[mid:]))}</text>')
            else:
                a(f'<text x="{tx}" y="{card_y+chh+17}" text-anchor="middle" class="name">{esc(name)}</text>')

    draw_shelly(ix + 260, "SHELLY #1", "ETH 1", SHELLY1)
    draw_shelly(ix + 820, "SHELLY #2", "ETH 2", SHELLY2)

    # Barra PE
    a(f'<rect x="{ix+50}" y="{n_bus+36}" width="280" height="16" rx="3" fill="{PE}" stroke="#854D0E"/>')
    for i in range(8):
        screw(a, ix + 70 + i * 32, n_bus + 44, 2.3)
    # stripes hint
    for i in range(0, 280, 16):
        a(f'<rect x="{ix+50+i}" y="{n_bus+36}" width="8" height="16" fill="#166534" opacity="0.35"/>')
    a(f'<text x="{ix+190}" y="{n_bus+72}" text-anchor="middle" style="font:700 12px DejaVu Sans,Arial;fill:#854D0E">BARRA PE (giallo/verde)</text>')

    # Legenda
    ly = cy0 + ch + 18
    a(f'<rect x="40" y="{ly}" width="{W-80}" height="140" rx="8" fill="#F8FAFC" filter="url(#soft)"/>')
    a(f'<text x="60" y="{ly+28}" class="h">Legenda carichi</text>')
    legend = [
        (1, "Lavastoviglie", "#1 O1", "dishwasher"),
        (2, "Microonde", "#1 O2", "microwave"),
        (3, "Forno", "#1 O3", "oven"),
        (4, "Frigorifero", "#1 O4", "fridge"),
        (5, "Piano cottura", "#2 O1", "cooktop"),
        (6, "Prese piano cottura", "#2 O2", "socket"),
        (7, "Prese piano lavoro", "#2 O3", "socket"),
        (8, "Prese interno mobile", "#2 O4", "socket"),
    ]
    for i, (num, name, path, icon) in enumerate(legend):
        x = 60 + i * 265
        y = ly + 48
        a(f'<rect x="{x}" y="{y}" width="250" height="58" rx="8" fill="#F1F5F9" stroke="#CBD5E1"/>')
        a(f'<circle cx="{x+18}" cy="{y+29}" r="12" fill="{ACC}"/>')
        a(f'<text x="{x+18}" y="{y+33}" text-anchor="middle" class="chip">{num}</text>')
        ICONS[icon](a, x + 52, y + 29, 0.58)
        a(f'<text x="{x+80}" y="{y+24}" class="leg">{esc(name)}</text>')
        a(f'<text x="{x+80}" y="{y+42}" class="legm">Shelly {esc(path)}</text>')
    a(f'<text x="60" y="{ly+128}" class="warn">Limiti Pro 4PM: 16 A/canale, 40 A totali — verificare forno e piano cottura in opera.</text>')

    a("</svg>")
    return "\n".join(p)


def main() -> None:
    svg = build_svg()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    for path in (OUT_DIR / "quadro-elettrico-cucina.svg", ART_DIR / "quadro-elettrico-cucina.svg"):
        path.write_text(svg, encoding="utf-8")
    for path in (OUT_DIR / "quadro-elettrico-cucina.png", ART_DIR / "quadro-elettrico-cucina.png"):
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), scale=1.15)
    # copia anche il render foto se presente
    src = Path("/opt/cursor/artifacts/assets/quadro-cucina-foto-realistico.jpg")
    alt = Path("/opt/cursor/artifacts/assets/quadro-cucina-foto-realistico.png")
    for candidate in (src, alt):
        if candidate.exists():
            dest = OUT_DIR / "quadro-elettrico-cucina-foto.jpg"
            dest.write_bytes(candidate.read_bytes())
            (ART_DIR / candidate.name).write_bytes(candidate.read_bytes())
            print("foto", dest)
            break
    print("OK", ART_DIR / "quadro-elettrico-cucina.png")


if __name__ == "__main__":
    main()
