#!/usr/bin/env python3
"""Genera lo schema elettrico corretto del quadro cucina (SVG + PNG)."""

from pathlib import Path

import cairosvg

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 1920, 1280

# Palette tecnica, sobria
BG = "#eef2f5"
PANEL = "#ffffff"
PANEL_EDGE = "#c5ced8"
INK = "#1c2430"
MUTED = "#5b6b7c"
L_COL = "#c0392b"
L_SOFT = "#fdecea"
N_COL = "#0f766e"
N_SOFT = "#e6f4f2"
ETH = "#334155"
ACCENT = "#0f4c81"
ACCENT_SOFT = "#e8f1f8"
FUSE = "#94a3b8"
STROKE = 2.4

SHELLY1 = {
    "O4": (4, "Frigorifero"),
    "O3": (3, "Forno"),
    "O2": (2, "Microonde"),
    "O1": (1, "Lavastoviglie"),
}
SHELLY2 = {
    "O4": (8, "Prese interno mobile"),
    "O3": (7, "Prese piano lavoro"),
    "O2": (6, "Prese piano cottura"),
    "O1": (5, "Piano cottura"),
}


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_svg() -> str:
    p: list[str] = []
    a = p.append

    a(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#d7dee6" stroke-width="1"/>
    </pattern>
    <filter id="soft" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#1c2430" flood-opacity="0.08"/>
    </filter>
    <style><![CDATA[
      .title {{ font: 700 34px "DejaVu Sans", Arial, sans-serif; fill: {INK}; letter-spacing: 0.5px; }}
      .sub {{ font: 400 14px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .h {{ font: 700 14px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .h2 {{ font: 600 12px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .chip {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: #fff; }}
      .name {{ font: 600 12px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .term {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .term-l {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {L_COL}; }}
      .term-n {{ font: 700 11px "DejaVu Sans", Arial, sans-serif; fill: {N_COL}; }}
      .bus {{ font: 700 12px "DejaVu Sans", Arial, sans-serif; }}
      .note {{ font: 400 12px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .leg {{ font: 500 12px "DejaVu Sans", Arial, sans-serif; fill: {INK}; }}
      .leg-m {{ font: 400 11px "DejaVu Sans", Arial, sans-serif; fill: {MUTED}; }}
      .warn {{ font: 500 12px "DejaVu Sans", Arial, sans-serif; fill: #8a5a00; }}
    ]]></style>
  </defs>
  <rect width="100%" height="100%" fill="{BG}"/>
  <rect width="100%" height="100%" fill="url(#grid)" opacity="0.45"/>
'''
    )

    # Header
    a(f'<rect x="0" y="0" width="{W}" height="88" fill="{PANEL}"/>')
    a(f'<rect x="0" y="86" width="{W}" height="2" fill="{ACCENT}"/>')
    a(f'<text x="48" y="42" class="title">Quadro elettrico cucina</text>')
    a(
        f'<text x="48" y="66" class="sub">'
        "Magnetotermico differenziale · 2× Shelly Pro 4PM · 8 circuiti · Ethernet</text>"
    )
    # Color key in header
    a(f'<rect x="1380" y="28" width="14" height="14" rx="2" fill="{L_COL}"/>')
    a(f'<text x="1402" y="40" class="note">Fase L</text>')
    a(f'<rect x="1485" y="28" width="14" height="14" rx="2" fill="{N_COL}"/>')
    a(f'<text x="1507" y="40" class="note">Neutro N</text>')
    a(f'<rect x="1600" y="28" width="14" height="14" rx="2" fill="{ETH}"/>')
    a(f'<text x="1622" y="40" class="note">Ethernet</text>')
    a(f'<rect x="1725" y="28" width="14" height="14" rx="2" fill="{FUSE}"/>')
    a(f'<text x="1747" y="40" class="note">Fusibile</text>')

    top_n_y = 155
    device_y = 360
    device_h = 260
    l_bus_y = 710
    n_bus_y = 960

    # N carichi rail
    a(f'<line x1="300" y1="{top_n_y}" x2="1780" y2="{top_n_y}" stroke="{N_COL}" stroke-width="3"/>')
    a(
        f'<rect x="1790" y="{top_n_y-14}" width="86" height="28" rx="14" fill="{N_SOFT}" '
        f'stroke="{N_COL}" stroke-width="1.5"/>'
    )
    a(f'<text x="1833" y="{top_n_y+5}" text-anchor="middle" class="term-n">N carichi</text>')

    # Magnetotermico
    mx, my, mw, mh = 48, 330, 210, 310
    a(
        f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="{PANEL}" '
        f'stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>'
    )
    a(f'<rect x="{mx}" y="{my}" width="8" height="{mh}" rx="4" fill="{ACCENT}"/>')
    a(f'<text x="{mx+mw/2+4}" y="{my+36}" text-anchor="middle" class="h">Magnetotermico</text>')
    a(f'<text x="{mx+mw/2+4}" y="{my+56}" text-anchor="middle" class="h">differenziale</text>')
    a(
        f'<rect x="{mx+42}" y="{my+78}" width="{mw-84}" height="28" rx="14" fill="{ACCENT_SOFT}"/>'
    )
    a(f'<text x="{mx+mw/2+4}" y="{my+97}" text-anchor="middle" class="h2">RCBO · L + N</text>')

    # Symbol block
    a(
        f'<rect x="{mx+48}" y="{my+125}" width="{mw-96}" height="110" rx="10" fill="#f8fafc" '
        f'stroke="{PANEL_EDGE}"/>'
    )
    a(f'<text x="{mx+mw/2+4}" y="{my+155}" text-anchor="middle" class="h2">protezione</text>')
    a(f'<circle cx="{mx+mw/2+4}" cy="{my+185}" r="16" fill="none" stroke="{ACCENT}" stroke-width="2.2"/>')
    a(f'<path d="M {mx+mw/2-6} {my+185} h 12" stroke="{ACCENT}" stroke-width="2.2"/>')
    a(f'<text x="{mx+mw/2+4}" y="{my+218}" text-anchor="middle" class="h2">IΔn</text>')

    # Supply in
    a(f'<line x1="98" y1="120" x2="98" y2="{my}" stroke="{L_COL}" stroke-width="3"/>')
    a(f'<line x1="158" y1="120" x2="158" y2="{my}" stroke="{N_COL}" stroke-width="3"/>')
    a(f'<circle cx="98" cy="{my}" r="5" fill="{L_COL}"/>')
    a(f'<circle cx="158" cy="{my}" r="5" fill="{N_COL}"/>')
    a(
        f'<rect x="74" y="96" width="48" height="22" rx="11" fill="{L_SOFT}" '
        f'stroke="{L_COL}" stroke-width="1.3"/>'
    )
    a(f'<text x="98" y="111" text-anchor="middle" class="term-l">L rete</text>')
    a(
        f'<rect x="134" y="96" width="48" height="22" rx="11" fill="{N_SOFT}" '
        f'stroke="{N_COL}" stroke-width="1.3"/>'
    )
    a(f'<text x="158" y="111" text-anchor="middle" class="term-n">N rete</text>')

    # Internal + out
    a(f'<line x1="98" y1="{my}" x2="98" y2="{my+mh}" stroke="{L_COL}" stroke-width="3"/>')
    a(f'<line x1="158" y1="{my}" x2="158" y2="{my+mh}" stroke="{N_COL}" stroke-width="3"/>')
    a(f'<circle cx="98" cy="{my+mh}" r="5" fill="{L_COL}"/>')
    a(f'<circle cx="158" cy="{my+mh}" r="5" fill="{N_COL}"/>')

    # BUS L / BUS N
    a(f'<line x1="98" y1="{my+mh}" x2="98" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3"/>')
    a(f'<line x1="98" y1="{l_bus_y}" x2="1780" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3"/>')
    a(
        f'<rect x="1790" y="{l_bus_y-14}" width="70" height="28" rx="14" fill="{L_SOFT}" '
        f'stroke="{L_COL}" stroke-width="1.5"/>'
    )
    a(f'<text x="1825" y="{l_bus_y+5}" text-anchor="middle" class="term-l">BUS L</text>')

    a(f'<line x1="158" y1="{my+mh}" x2="158" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3"/>')
    a(f'<line x1="158" y1="{n_bus_y}" x2="1780" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3"/>')
    a(
        f'<rect x="1790" y="{n_bus_y-14}" width="70" height="28" rx="14" fill="{N_SOFT}" '
        f'stroke="{N_COL}" stroke-width="1.5"/>'
    )
    a(f'<text x="1825" y="{n_bus_y+5}" text-anchor="middle" class="term-n">BUS N</text>')
    a(f'<line x1="1780" y1="{top_n_y}" x2="1780" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3"/>')

    def draw_shelly(x: float, title: str, eth: str, mapping: dict[str, tuple[int, str]]):
        y, w, h = device_y, 580, device_h
        a(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{PANEL}" '
            f'stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>'
        )
        a(f'<rect x="{x}" y="{y}" width="{w}" height="44" rx="16" fill="{ACCENT}"/>')
        a(f'<rect x="{x}" y="{y+28}" width="{w}" height="16" fill="{ACCENT}"/>')
        a(f'<text x="{x+22}" y="{y+28}" class="chip" style="font-size:15px">{title}</text>')
        a(f'<text x="{x+w-22}" y="{y+28}" text-anchor="end" class="chip">Shelly Pro 4PM</text>')

        # Screen
        sx, sy, sw, sh = x + 180, y + 74, 220, 72
        a(
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" fill="#0b1f33" '
            f'stroke="#16324d" stroke-width="1.5"/>'
        )
        a(f'<text x="{sx+sw/2}" y="{sy+32}" text-anchor="middle" fill="#9fd0ff" '
          f'style="font:600 13px DejaVu Sans, Arial, sans-serif">16 A / canale</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+52}" text-anchor="middle" fill="#6b8eab" '
          f'style="font:500 11px DejaVu Sans, Arial, sans-serif">misura energia · LAN</text>')

        for i, lab in enumerate(["▲", "▼", "OK"]):
            bx = sx + 28 + i * 58
            by = sy + sh + 14
            a(f'<rect x="{bx}" y="{by}" width="42" height="22" rx="6" fill="#f1f5f9" stroke="{PANEL_EDGE}"/>')
            a(f'<text x="{bx+21}" y="{by+15}" text-anchor="middle" class="h2">{lab}</text>')

        # Terminali più distanziati per etichette leggibili
        term_x = {
            "O4": x + 70,
            "O3": x + 175,
            "L": x + w / 2,
            "O2": x + w - 175,
            "O1": x + w - 70,
        }

        for label, tx in term_x.items():
            if label == "L":
                a(f'<circle cx="{tx}" cy="{y}" r="6" fill="{L_COL}"/>')
                a(
                    f'<rect x="{tx-14}" y="{y+10}" width="28" height="18" rx="9" fill="{L_SOFT}" '
                    f'stroke="{L_COL}" stroke-width="1.2"/>'
                )
                a(f'<text x="{tx}" y="{y+23}" text-anchor="middle" class="term-l">L</text>')
                a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="3"/>')
                a(f'<circle cx="{tx}" cy="{l_bus_y}" r="4.5" fill="{L_COL}"/>')
            else:
                a(f'<circle cx="{tx}" cy="{y}" r="6" fill="{INK}"/>')
                a(f'<text x="{tx}" y="{y+22}" text-anchor="middle" class="term">{label}</text>')

        # Bottom LAN + N
        lan_x = x + 78
        n_x = x + 168
        a(f'<rect x="{lan_x-22}" y="{y+h-12}" width="44" height="20" rx="4" fill="#0f172a"/>')
        a(f'<text x="{lan_x}" y="{y+h+28}" text-anchor="middle" class="h2">LAN</text>')
        eth_y = y + h + 58
        a(
            f'<path d="M {lan_x} {y+h+8} V {eth_y} H {lan_x+90}" fill="none" stroke="{ETH}" '
            f'stroke-width="2.2" stroke-dasharray="6 4" stroke-linecap="round"/>'
        )
        a(
            f'<rect x="{lan_x+98}" y="{eth_y-13}" width="58" height="26" rx="13" fill="#e2e8f0" '
            f'stroke="{ETH}" stroke-width="1.3"/>'
        )
        a(f'<text x="{lan_x+127}" y="{eth_y+4}" text-anchor="middle" class="term">{eth}</text>')

        a(f'<circle cx="{n_x}" cy="{y+h}" r="6" fill="{N_COL}"/>')
        a(
            f'<rect x="{n_x-14}" y="{y+h-30}" width="28" height="18" rx="9" fill="{N_SOFT}" '
            f'stroke="{N_COL}" stroke-width="1.2"/>'
        )
        a(f'<text x="{n_x}" y="{y+h-17}" text-anchor="middle" class="term-n">N</text>')
        a(f'<line x1="{n_x}" y1="{y+h}" x2="{n_x}" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="3"/>')
        a(f'<circle cx="{n_x}" cy="{n_bus_y}" r="4.5" fill="{N_COL}"/>')
        a(f'<text x="{x+w-24}" y="{y+h+20}" text-anchor="end" class="note">S1–S4 non usati</text>')

        # Outputs / loads — etichette alternate in altezza per evitare overlap
        for idx, out in enumerate(("O4", "O3", "O2", "O1")):
            num, name = mapping[out]
            tx = term_x[out]
            fuse_y = y - 38
            a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{fuse_y+18}" stroke="{INK}" stroke-width="2.4"/>')
            a(
                f'<rect x="{tx-9}" y="{fuse_y}" width="18" height="22" rx="3" fill="#fff" '
                f'stroke="{FUSE}" stroke-width="1.8"/>'
            )
            load_y = top_n_y + 52
            a(f'<line x1="{tx}" y1="{fuse_y}" x2="{tx}" y2="{load_y+14}" stroke="{INK}" stroke-width="2.4"/>')
            a(f'<circle cx="{tx}" cy="{load_y}" r="13" fill="{PANEL}" stroke="{ACCENT}" stroke-width="2"/>')
            a(f'<circle cx="{tx}" cy="{load_y}" r="4" fill="{ACCENT}"/>')
            a(f'<line x1="{tx}" y1="{load_y-13}" x2="{tx}" y2="{top_n_y}" stroke="{N_COL}" stroke-width="2.4"/>')
            a(f'<circle cx="{tx}" cy="{top_n_y}" r="4" fill="{N_COL}"/>')

            stagger = 0 if idx % 2 == 0 else 42
            badge_y = top_n_y - 78 - stagger
            card_y = top_n_y - 58 - stagger
            card_w = 112
            a(f'<circle cx="{tx}" cy="{badge_y}" r="14" fill="{ACCENT}"/>')
            a(f'<text x="{tx}" y="{badge_y+5}" text-anchor="middle" class="chip" style="font-size:13px">{num}</text>')
            a(
                f'<rect x="{tx-card_w/2}" y="{card_y}" width="{card_w}" height="36" rx="8" '
                f'fill="{PANEL}" stroke="{PANEL_EDGE}" stroke-width="1.3"/>'
            )
            words = name.split()
            if len(name) > 13 and len(words) > 1:
                mid = max(1, len(words) // 2)
                a(
                    f'<text x="{tx}" y="{card_y+15}" text-anchor="middle" class="name" '
                    f'style="font-size:11px">{esc(" ".join(words[:mid]))}</text>'
                )
                a(
                    f'<text x="{tx}" y="{card_y+29}" text-anchor="middle" class="name" '
                    f'style="font-size:11px">{esc(" ".join(words[mid:]))}</text>'
                )
            else:
                a(f'<text x="{tx}" y="{card_y+22}" text-anchor="middle" class="name">{esc(name)}</text>')
            a(f'<text x="{tx}" y="{load_y+34}" text-anchor="middle" class="h2">{out}</text>')

    draw_shelly(300, "SHELLY #1", "ETH 1", SHELLY1)
    draw_shelly(980, "SHELLY #2", "ETH 2", SHELLY2)

    # Legend panel
    lx, ly, lw, lh = 300, 1020, 1220, 210
    a(
        f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="16" fill="{PANEL}" '
        f'stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>'
    )
    a(f'<text x="{lx+24}" y="{ly+34}" class="h">Legenda carichi</text>')
    a(
        f'<text x="{lx+24}" y="{ly+54}" class="note">'
        "Canale Shelly = numero circuito · fase commutata da Ox · neutro da N carichi</text>"
    )

    legend = [
        (1, "Lavastoviglie", "Shelly #1 · O1"),
        (2, "Microonde", "Shelly #1 · O2"),
        (3, "Forno", "Shelly #1 · O3"),
        (4, "Frigorifero", "Shelly #1 · O4"),
        (5, "Piano cottura", "Shelly #2 · O1"),
        (6, "Prese piano cottura", "Shelly #2 · O2"),
        (7, "Prese piano lavoro", "Shelly #2 · O3"),
        (8, "Prese interno mobile", "Shelly #2 · O4"),
    ]
    for i, (num, name, path) in enumerate(legend):
        col = i % 4
        row = i // 4
        x = lx + 24 + col * 295
        y = ly + 78 + row * 52
        a(f'<rect x="{x}" y="{y}" width="275" height="40" rx="10" fill="#f8fafc" stroke="{PANEL_EDGE}"/>')
        a(f'<circle cx="{x+22}" cy="{y+20}" r="12" fill="{ACCENT}"/>')
        a(f'<text x="{x+22}" y="{y+24}" text-anchor="middle" class="chip">{num}</text>')
        a(f'<text x="{x+44}" y="{y+17}" class="leg">{esc(name)}</text>')
        a(f'<text x="{x+44}" y="{y+32}" class="leg-m">{esc(path)}</text>')

    a(
        f'<text x="{lx+24}" y="{ly+190}" class="warn">'
        "Verificare correnti in opera: max 16 A/canale e 40 A totali per Pro 4PM "
        "(attenzione a forno e piano cottura).</text>"
    )

    # Side note card
    a(
        f'<rect x="48" y="1020" width="220" height="210" rx="16" fill="{PANEL}" '
        f'stroke="{PANEL_EDGE}" stroke-width="1.5" filter="url(#soft)"/>'
    )
    a(f'<text x="68" y="1055" class="h">Flusso</text>')
    steps = [
        "1. L/N da rete",
        "2. Protezione RCBO",
        "3. BUS L / BUS N",
        "4. Shelly #1 e #2",
        "5. Ox → carico",
        "6. Neutro comune",
    ]
    for i, step in enumerate(steps):
        a(f'<text x="68" y="{1085 + i*22}" class="note">{step}</text>')

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
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png_path), scale=1.35)
    art_svg.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(art_png), scale=1.35)
    print(f"Wrote {png_path}")
    print(f"Wrote {art_png}")


if __name__ == "__main__":
    main()
