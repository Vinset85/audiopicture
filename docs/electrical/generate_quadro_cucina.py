#!/usr/bin/env python3
"""Genera lo schema elettrico corretto del quadro cucina (SVG + PNG)."""

from pathlib import Path

import cairosvg

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 1680, 1180
INK = "#111111"
ACCENT = "#1a4f8b"
N_COL = "#1a5c2e"
L_COL = "#9a1f1f"
ETH = "#444444"
BG = "#ffffff"
BOX = "#f5f5f5"
STROKE = 2.2

# Mappatura funzionale: canale Shelly On = circuito n
# Terminali fisici Shelly Pro 4PM (alto, sx→dx): O4, O3, L, O2, O1
SHELLY1 = {
    "O1": (1, "LAVASTOVIGLIE"),
    "O2": (2, "MICROONDE"),
    "O3": (3, "FORNO"),
    "O4": (4, "FRIGORIFERO"),
}
SHELLY2 = {
    "O1": (5, "PIANO COTTURA"),
    "O2": (6, "PRESE PIANO COTTURA"),
    "O3": (7, "PRESE PIANO LAVORO"),
    "O4": (8, "PRESE INTERNO MOBILE"),
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
  <rect width="100%" height="100%" fill="{BG}"/>
  <defs>
    <style><![CDATA[
      .title {{ font: 700 30px DejaVu Sans, Arial, sans-serif; fill: {INK}; }}
      .sub {{ font: 400 13px DejaVu Sans, Arial, sans-serif; fill: #444; }}
      .lab {{ font: 700 12px DejaVu Sans, Arial, sans-serif; fill: {INK}; }}
      .lab-sm {{ font: 500 11px DejaVu Sans, Arial, sans-serif; fill: {INK}; }}
      .term {{ font: 700 11px DejaVu Sans, Arial, sans-serif; fill: {INK}; }}
      .n {{ font: 700 13px DejaVu Sans, Arial, sans-serif; fill: {N_COL}; }}
      .l {{ font: 700 13px DejaVu Sans, Arial, sans-serif; fill: {L_COL}; }}
      .note {{ font: 400 12px DejaVu Sans, Arial, sans-serif; fill: #222; }}
      .dev {{ font: 700 13px DejaVu Sans, Arial, sans-serif; fill: {INK}; }}
      .dev2 {{ font: 500 11px DejaVu Sans, Arial, sans-serif; fill: #333; }}
      .warn {{ font: 500 11px DejaVu Sans, Arial, sans-serif; fill: #663c00; }}
    ]]></style>
  </defs>
'''
    )

    a(f'<text x="{W/2}" y="40" text-anchor="middle" class="title">QUADRO ELETTRICO CUCINA</text>')
    a(
        f'<text x="{W/2}" y="62" text-anchor="middle" class="sub">'
        "Schema di cablaggio corretto — Magnetotermico differenziale + 2× Shelly Pro 4PM "
        "(alimentazione L/N, uscite O1–O4, Ethernet)</text>"
    )

    # Coordinate principali
    top_n_y = 100
    l_bus_y = 560
    n_bus_y = 860
    mx, my, mw, mh = 50, 170, 190, 300

    # Alimentazione entrante
    a(f'<text x="85" y="120" class="l">L rete</text>')
    a(f'<text x="145" y="120" class="n">N rete</text>')
    a(f'<line x1="90" y1="128" x2="90" y2="{my}" stroke="{L_COL}" stroke-width="{STROKE}"/>')
    a(f'<line x1="150" y1="128" x2="150" y2="{my}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
    a(f'<circle cx="90" cy="{my}" r="3.8" fill="{L_COL}"/>')
    a(f'<circle cx="150" cy="{my}" r="3.8" fill="{N_COL}"/>')
    a(f'<text x="90" y="{my-8}" text-anchor="middle" class="term">L</text>')
    a(f'<text x="150" y="{my-8}" text-anchor="middle" class="term">N</text>')

    # Magnetotermico differenziale
    a(
        f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="{BOX}" '
        f'stroke="{INK}" stroke-width="{STROKE}" rx="4"/>'
    )
    a(f'<text x="{mx+mw/2}" y="{my+32}" text-anchor="middle" class="dev">MAGNETOTERMICO</text>')
    a(f'<text x="{mx+mw/2}" y="{my+52}" text-anchor="middle" class="dev">DIFFERENZIALE</text>')
    a(f'<text x="{mx+mw/2}" y="{my+72}" text-anchor="middle" class="dev2">RCBO · protezione L+N</text>')
    a(
        f'<rect x="{mx+55}" y="{my+100}" width="80" height="100" fill="#fff" '
        f'stroke="{INK}" stroke-width="1.6"/>'
    )
    a(f'<text x="{mx+95}" y="{my+130}" text-anchor="middle" class="lab-sm">IΔn</text>')
    a(f'<line x1="{mx+70}" y1="{my+150}" x2="{mx+120}" y2="{my+150}" stroke="{INK}" stroke-width="1.6"/>')
    a(f'<circle cx="{mx+95}" cy="{my+168}" r="9" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    a(f'<text x="{mx+95}" y="{my+220}" text-anchor="middle" class="lab-sm">MT + Diff</text>')

    # Uscite magnetotermico
    a(f'<line x1="90" y1="{my}" x2="90" y2="{my+mh}" stroke="{L_COL}" stroke-width="{STROKE}"/>')
    a(f'<line x1="150" y1="{my}" x2="150" y2="{my+mh}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
    a(f'<circle cx="90" cy="{my+mh}" r="3.8" fill="{L_COL}"/>')
    a(f'<circle cx="150" cy="{my+mh}" r="3.8" fill="{N_COL}"/>')
    a(f'<text x="70" y="{my+mh+18}" text-anchor="middle" class="l">L</text>')
    a(f'<text x="170" y="{my+mh+18}" text-anchor="middle" class="n">N</text>')

    # BUS L
    a(f'<line x1="90" y1="{my+mh}" x2="90" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="{STROKE}"/>')
    a(f'<line x1="90" y1="{l_bus_y}" x2="1500" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="{STROKE}"/>')
    a(f'<text x="1515" y="{l_bus_y+4}" class="l">BUS L</text>')

    # BUS N basso + N carichi alto collegati a destra
    a(f'<line x1="150" y1="{my+mh}" x2="150" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
    a(f'<line x1="150" y1="{n_bus_y}" x2="1560" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
    a(f'<text x="1575" y="{n_bus_y+4}" class="n">BUS N</text>')
    a(f'<line x1="300" y1="{top_n_y}" x2="1560" y2="{top_n_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
    a(f'<text x="1575" y="{top_n_y+4}" class="n">N carichi</text>')
    a(f'<line x1="1560" y1="{top_n_y}" x2="1560" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')

    def draw_shelly(x: float, y: float, w: float, h: float, title: str, eth: str, mapping: dict):
        a(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BOX}" '
            f'stroke="{INK}" stroke-width="{STROKE}" rx="4"/>'
        )
        # Display
        sx, sy, sw, sh = x + w * 0.20, y + 48, w * 0.60, 78
        a(
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#e8eef5" '
            f'stroke="{ACCENT}" stroke-width="1.5" rx="3"/>'
        )
        a(f'<text x="{sx+sw/2}" y="{sy+30}" text-anchor="middle" class="dev">{title}</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+50}" text-anchor="middle" class="dev2">Shelly Pro 4PM</text>')
        a(f'<text x="{sx+sw/2}" y="{sy+68}" text-anchor="middle" class="dev2">16 A / canale</text>')

        by = sy + sh + 12
        for i, lab in enumerate(["▲", "▼", "OK"]):
            bx = sx + 28 + i * 55
            a(f'<rect x="{bx}" y="{by}" width="40" height="18" fill="#fff" stroke="{INK}" stroke-width="1" rx="2"/>')
            a(f'<text x="{bx+20}" y="{by+13}" text-anchor="middle" class="lab-sm">{lab}</text>')

        # Terminali alti: O4 O3 L O2 O1
        term_x = {
            "O4": x + 40,
            "O3": x + 95,
            "L": x + w / 2,
            "O2": x + w - 95,
            "O1": x + w - 40,
        }
        for label, tx in term_x.items():
            color = L_COL if label == "L" else INK
            a(f'<circle cx="{tx}" cy="{y}" r="4.2" fill="{color}"/>')
            a(f'<text x="{tx}" y="{y+18}" text-anchor="middle" class="term">{label}</text>')
            if label == "L":
                a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{l_bus_y}" stroke="{L_COL}" stroke-width="{STROKE}"/>')
                a(f'<circle cx="{tx}" cy="{l_bus_y}" r="3.5" fill="{L_COL}"/>')

        # LAN + N in basso (ingressi S non usati in questo quadro)
        lan_x = x + 48
        n_x = x + 110
        a(f'<rect x="{lan_x-20}" y="{y+h-10}" width="40" height="18" fill="#222" rx="2"/>')
        a(f'<text x="{lan_x}" y="{y+h+28}" text-anchor="middle" class="lab-sm">LAN</text>')
        eth_y = y + h + 58
        a(
            f'<line x1="{lan_x}" y1="{y+h+8}" x2="{lan_x}" y2="{eth_y}" '
            f'stroke="{ETH}" stroke-width="2" stroke-dasharray="5 3"/>'
        )
        a(
            f'<line x1="{lan_x}" y1="{eth_y}" x2="{lan_x+80}" y2="{eth_y}" '
            f'stroke="{ETH}" stroke-width="2" stroke-dasharray="5 3"/>'
        )
        a(f'<text x="{lan_x+90}" y="{eth_y+4}" class="lab">{eth}</text>')

        a(f'<circle cx="{n_x}" cy="{y+h}" r="4.2" fill="{N_COL}"/>')
        a(f'<text x="{n_x}" y="{y+h-12}" text-anchor="middle" class="term">N</text>')
        a(f'<line x1="{n_x}" y1="{y+h}" x2="{n_x}" y2="{n_bus_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
        a(f'<circle cx="{n_x}" cy="{n_bus_y}" r="3.5" fill="{N_COL}"/>')

        # Marcatura S non collegati
        a(f'<text x="{x+w-20}" y="{y+h+16}" text-anchor="end" class="dev2">S1–S4 non usati</text>')

        # Uscite verso carichi
        for out in ("O4", "O3", "O2", "O1"):
            num, name = mapping[out]
            tx = term_x[out]
            fuse_bottom = y - 22
            fuse_top = y - 42
            a(f'<line x1="{tx}" y1="{y}" x2="{tx}" y2="{fuse_bottom}" stroke="{INK}" stroke-width="{STROKE}"/>')
            a(
                f'<rect x="{tx-8}" y="{fuse_top}" width="16" height="20" fill="#fff" '
                f'stroke="{INK}" stroke-width="1.5"/>'
            )
            load_y = top_n_y + 36
            a(f'<line x1="{tx}" y1="{fuse_top}" x2="{tx}" y2="{load_y+10}" stroke="{INK}" stroke-width="{STROKE}"/>')
            a(f'<circle cx="{tx}" cy="{load_y}" r="11" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
            a(f'<line x1="{tx-7}" y1="{load_y-7}" x2="{tx+7}" y2="{load_y+7}" stroke="{INK}" stroke-width="1.3"/>')
            a(f'<line x1="{tx+7}" y1="{load_y-7}" x2="{tx-7}" y2="{load_y+7}" stroke="{INK}" stroke-width="1.3"/>')
            a(f'<line x1="{tx}" y1="{load_y-11}" x2="{tx}" y2="{top_n_y}" stroke="{N_COL}" stroke-width="{STROKE}"/>')
            a(f'<circle cx="{tx}" cy="{top_n_y}" r="3.2" fill="{N_COL}"/>')
            a(f'<text x="{tx}" y="{load_y+28}" text-anchor="middle" class="lab">{num} · {out}</text>')
            words = name.split()
            if len(name) > 16 and len(words) > 1:
                mid = max(1, len(words) // 2)
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                a(f'<text x="{tx}" y="{top_n_y-28}" text-anchor="middle" class="lab-sm">{esc(line1)}</text>')
                a(f'<text x="{tx}" y="{top_n_y-14}" text-anchor="middle" class="lab-sm">{esc(line2)}</text>')
            else:
                a(f'<text x="{tx}" y="{top_n_y-16}" text-anchor="middle" class="lab-sm">{esc(name)}</text>')

    draw_shelly(310, 250, 460, 230, "SHELLY #1", "ETH 1", SHELLY1)
    draw_shelly(900, 250, 460, 230, "SHELLY #2", "ETH 2", SHELLY2)

    # Legenda
    lx, ly, lw, lh = 310, 940, 1050, 200
    a(
        f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{BOX}" '
        f'stroke="{INK}" stroke-width="1.6" rx="4"/>'
    )
    a(f'<text x="{lx+18}" y="{ly+28}" class="dev">LEGENDA CARICHI E COLLEGAMENTI</text>')

    legend = [
        (1, "LAVASTOVIGLIE", "Shelly #1 → O1"),
        (2, "MICROONDE", "Shelly #1 → O2"),
        (3, "FORNO", "Shelly #1 → O3"),
        (4, "FRIGORIFERO", "Shelly #1 → O4"),
        (5, "PIANO COTTURA", "Shelly #2 → O1"),
        (6, "PRESE PIANO COTTURA", "Shelly #2 → O2"),
        (7, "PRESE PIANO LAVORO", "Shelly #2 → O3"),
        (8, "PRESE INTERNO MOBILE", "Shelly #2 → O4"),
    ]
    for i, (num, name, path) in enumerate(legend):
        col = 0 if i < 4 else 1
        row = i % 4
        x = lx + 30 + col * 520
        y = ly + 58 + row * 24
        a(f'<text x="{x}" y="{y}" class="note">{num}. {esc(name)}  —  {esc(path)}</text>')

    a(
        f'<text x="{lx+18}" y="{ly+175}" class="warn">'
        "Nota: ogni carico riceve la fase commutata da Ox e il neutro dal BUS N. "
        "Verificare correnti (max 16 A/canale, 40 A totali per Pro 4PM) e sezioni cavo.</text>"
    )

    # Chiave colori
    a(f'<text x="50" y="980" class="dev">Convenzioni</text>')
    a(f'<line x1="50" y1="1000" x2="110" y2="1000" stroke="{L_COL}" stroke-width="3"/>')
    a(f'<text x="120" y="1004" class="note">Fase L</text>')
    a(f'<line x1="50" y1="1025" x2="110" y2="1025" stroke="{N_COL}" stroke-width="3"/>')
    a(f'<text x="120" y="1029" class="note">Neutro N</text>')
    a(f'<line x1="50" y1="1050" x2="110" y2="1050" stroke="{ETH}" stroke-width="2" stroke-dasharray="5 3"/>')
    a(f'<text x="120" y="1054" class="note">Ethernet</text>')
    a(f'<rect x="50" y="1068" width="16" height="20" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    a(f'<text x="78" y="1083" class="note">Protezione / fusibile canale</text>')

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
    print(f"Wrote {svg_path}")
    print(f"Wrote {png_path}")
    print(f"Wrote {art_png}")


if __name__ == "__main__":
    main()
