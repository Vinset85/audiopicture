#!/usr/bin/env python3
"""Render realistico quadro cucina con foto componenti reali + cablaggio corretto."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

OUT_DIR = Path(__file__).resolve().parent
COMP = OUT_DIR / "components"
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 2400, 1600
L = (122, 62, 29)
N = (30, 64, 175)
PE = (161, 98, 7)
ETH = (30, 58, 138)
INK = (15, 23, 42)

SHELLY1 = [("O4", 4, "Frigorifero"), ("O3", 3, "Forno"), ("O2", 2, "Microonde"), ("O1", 1, "Lavastoviglie")]
SHELLY2 = [("O4", 8, "Prese int. mobile"), ("O3", 7, "Prese p. lavoro"), ("O2", 6, "Prese p. cottura"), ("O1", 5, "Piano cottura")]


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except OSError:
        return ImageFont.load_default()


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def chip(d, xy, text, bg, fg=(255, 255, 255)):
    x, y = xy
    f = font(15, True)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    rr(d, [x, y, x + tw + 16, y + th + 10], 8, bg, (255, 255, 255), 1)
    d.text((x + 8, y + 4), text, fill=fg, font=f)


def wire(d, pts, color, width=6):
    d.line(pts, fill=color, width=width, joint="curve")
    hi = tuple(min(255, c + 50) for c in color)
    d.line([(x, y - max(1, width // 4)) for x, y in pts], fill=hi, width=max(1, width // 4))


def load_cutout(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    return im


def fit_height(im: Image.Image, height: int) -> Image.Image:
    ratio = height / im.height
    return im.resize((max(1, int(im.width * ratio)), height), Image.Resampling.LANCZOS)


def paste(base: Image.Image, sprite: Image.Image, xy: tuple[int, int]):
    base.alpha_composite(sprite, dest=xy)


def prepare_components():
    """Assicura cutout Shelly ufficiale e RCBO pronti."""
    COMP.mkdir(parents=True, exist_ok=True)
    shelly_src = COMP / "shelly-pro-4pm-official.png"
    shelly_out = COMP / "shelly-pro-4pm-cutout.png"
    rcbo_src = COMP / "component-rcbo-magnetotermico.jpg"
    rcbo_out = COMP / "rcbo-cutout.png"

    if shelly_src.exists():
        im = Image.open(shelly_src).convert("RGBA")
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if r < 35 and g < 35 and b < 35:
                    px[x, y] = (r, g, b, 0)
        # rimuovi anche cavo ethernet bianco in basso se presente: lascia corpo
        bbox = im.split()[-1].getbbox()
        im = im.crop(bbox)
        # ritaglia un po' il cavo in basso: tieni ~88% altezza dal top
        im = im.crop((0, 0, im.width, int(im.height * 0.90)))
        bbox = im.split()[-1].getbbox()
        im = im.crop(bbox)
        im.save(shelly_out)

    if rcbo_src.exists():
        im = Image.open(rcbo_src).convert("RGBA")
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if r > 245 and g > 245 and b > 245:
                    px[x, y] = (r, g, b, 0)
        bbox = im.split()[-1].getbbox()
        im = im.crop(bbox)
        im.save(rcbo_out)

    return shelly_out, rcbo_out


def draw_cabinet(img: Image.Image, d: ImageDraw.ImageDraw):
    # metal cabinet
    for y in range(H):
        t = y / H
        col = (
            int(120 + 40 * (1 - t)),
            int(130 + 35 * (1 - t)),
            int(145 + 30 * (1 - t)),
        )
        d.line([(0, y), (W, y)], fill=col)
    rr(d, [36, 36, W - 36, H - 36], 18, (90, 100, 115), (40, 45, 55), 5)
    # hinges
    for hy in (160, H // 2, H - 200):
        rr(d, [28, hy, 52, hy + 48], 4, (180, 190, 200), (60, 70, 80), 2)
    # inner tray
    rr(d, [70, 100, W - 70, H - 80], 10, (210, 218, 226), (140, 150, 160), 2)
    # perforated plate
    for yy in range(130, H - 110, 18):
        for xx in range(100, W - 100, 18):
            d.ellipse([xx, yy, xx + 3, yy + 3], fill=(160, 170, 180))


def draw_din(d, y):
    d.rectangle([110, y, W - 110, y + 40], fill=(190, 198, 206), outline=(90, 100, 110))
    d.rectangle([110, y + 12, W - 110, y + 18], fill=(245, 248, 250))
    d.rectangle([110, y + 26, W - 110, y + 30], fill=(70, 80, 90))
    d.text((120, y + 52), "Guida DIN EN 60715 · 35 mm", fill=(60, 70, 80), font=font(13))


def build() -> Image.Image:
    shelly_path, rcbo_path = prepare_components()
    shelly = load_cutout(shelly_path)
    rcbo = load_cutout(rcbo_path)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    draw_cabinet(img, d)

    # header plate
    rr(d, [95, 55, 980, 115], 10, (248, 250, 252), (255, 255, 255), 1)
    d.text((115, 68), "Quadro elettrico cucina", fill=INK, font=font(30, True))
    d.text((115, 100), "Render con foto reali · Shelly Pro 4PM ufficiale + RCBO · cablaggio corretto", fill=(71, 85, 105), font=font(14))
    for i, (c, t) in enumerate([(L, "L fase"), (N, "N neutro"), (ETH, "ETH"), (PE, "PE")]):
        x = 1680 + i * 140
        rr(d, [x, 70, x + 18, 88], 4, c)
        d.text((x + 26, 72), t, fill=(248, 250, 252), font=font(14, True))

    # N bar
    n_y = 155
    d.rectangle([150, n_y - 9, W - 240, n_y + 9], fill=N)
    chip(d, (W - 330, n_y - 18), "MORSETTIERA N", (219, 234, 254), N)

    din_y = 860
    draw_din(d, din_y)

    l_bus_y = 1040
    n_bus_y = 1140
    d.line([(160, l_bus_y), (W - 170, l_bus_y)], fill=L, width=9)
    d.line([(160, n_bus_y), (W - 170, n_bus_y)], fill=N, width=9)
    chip(d, (W - 300, l_bus_y - 16), "BUS L", (254, 243, 199), L)
    chip(d, (W - 300, n_bus_y - 16), "BUS N", (219, 234, 254), N)
    d.rectangle([150, 1230, 430, 1248], fill=PE)
    for i in range(0, 280, 14):
        d.rectangle([150 + i, 1230, 157 + i, 1248], fill=(22, 101, 52))
    d.text((290, 1268), "BARRA PE", fill=PE, font=font(13, True), anchor="mm")

    # Place RCBO photo
    rcbo_h = 340
    rcbo_s = fit_height(rcbo, rcbo_h)
    rcbo_x, rcbo_y = 120, din_y - rcbo_h + 20
    paste(img, rcbo_s, (rcbo_x, rcbo_y))
    # terminal anchors on photo (approximate fractions of device)
    rcx = rcbo_x + rcbo_s.width // 2
    rc_L_top = (rcbo_x + int(rcbo_s.width * 0.32), rcbo_y + 8)
    rc_N_top = (rcbo_x + int(rcbo_s.width * 0.68), rcbo_y + 8)
    rc_L_bot = (rcbo_x + int(rcbo_s.width * 0.32), rcbo_y + rcbo_h - 8)
    rc_N_bot = (rcbo_x + int(rcbo_s.width * 0.68), rcbo_y + rcbo_h - 8)
    d.text((rcx, rcbo_y - 18), "Magnetotermico differenziale (RCBO)", fill=INK, font=font(14, True), anchor="mm")

    # Place two Shelly official photos
    shelly_h = 360
    s_img = fit_height(shelly, shelly_h)
    s1x, s1y = 380, din_y - shelly_h + 25
    s2x, s2y = 980, din_y - shelly_h + 25
    paste(img, s_img, (s1x, s1y))
    paste(img, s_img, (s2x, s2y))
    d.text((s1x + s_img.width // 2, s1y - 18), "SHELLY #1 · Pro 4PM", fill=INK, font=font(14, True), anchor="mm")
    d.text((s2x + s_img.width // 2, s2y - 18), "SHELLY #2 · Pro 4PM", fill=INK, font=font(14, True), anchor="mm")

    def shelly_terms(sx, sy, sw, sh):
        # top O4 O3 L O2 O1 across upper terminal strip
        labels = ["O4", "O3", "L", "O2", "O1"]
        xs = {}
        for i, lab in enumerate(labels):
            xs[lab] = sx + int(sw * (0.18 + i * 0.16))
        return {
            "terms": xs,
            "top_y": sy + 18,
            "N": (sx + int(sw * 0.38), sy + sh - 12),
            "LAN": (sx + int(sw * 0.22), sy + sh - 8),
            "bottom_y": sy + sh,
        }

    s1 = shelly_terms(s1x, s1y, s_img.width, shelly_h)
    s2 = shelly_terms(s2x, s2y, s_img.width, shelly_h)

    # redraw draw context after alpha paste (PIL draw stays valid)
    d = ImageDraw.Draw(img)

    # Supply L/N to RCBO top
    wire(d, [(100, 1200), (100, rc_L_top[1] - 40), (rc_L_top[0], rc_L_top[1] - 40), rc_L_top], L, 7)
    wire(d, [(250, 1200), (250, rc_N_top[1] - 40), (rc_N_top[0], rc_N_top[1] - 40), rc_N_top], N, 7)
    chip(d, (70, 1205), "L rete", (254, 243, 199), L)
    chip(d, (220, 1205), "N rete", (219, 234, 254), N)

    # RCBO out to buses
    wire(d, [rc_L_bot, (rc_L_bot[0], l_bus_y), (W - 200, l_bus_y)], L, 8)
    wire(d, [rc_N_bot, (rc_N_bot[0], n_bus_y), (W - 200, n_bus_y)], N, 8)
    wire(d, [(W - 260, n_y), (W - 260, n_bus_y)], N, 6)

    # Power Shellys
    for s in (s1, s2):
        wire(d, [(s["terms"]["L"], s["top_y"]), (s["terms"]["L"], l_bus_y)], L, 6)
        wire(d, [s["N"], (s["N"][0], n_bus_y)], N, 6)
        # label terminals lightly
        for lab, tx in s["terms"].items():
            col = L if lab == "L" else (248, 250, 252)
            d.text((tx, s["top_y"] - 14), lab, fill=col if lab == "L" else INK, font=font(11, True), anchor="mm")

    # ETH only LAN
    for s, label, xo in ((s1, "ETH 1", 0), (s2, "ETH 2", 100)):
        lx, ly = s["LAN"]
        wire(d, [(lx, ly), (lx, 1210), (1750 + xo, 1210), (1750 + xo, 1280)], ETH, 5)
        chip(d, (1710 + xo, 1285), label, ETH, (248, 250, 252))

    # Loads via MCB
    def place_loads(s, mapping):
        for idx, (out, num, name) in enumerate(mapping):
            tx = s["terms"][out]
            mcb_y = 430
            wire(d, [(tx, s["top_y"]), (tx, mcb_y + 30)], INK, 4)
            # mini MCB drawing
            rr(d, [tx - 14, mcb_y - 28, tx + 14, mcb_y + 28], 4, (250, 250, 250), (100, 110, 120), 1)
            rr(d, [tx - 10, mcb_y - 22, tx + 10, mcb_y - 10], 2, (254, 226, 226), (220, 38, 38))
            d.text((tx, mcb_y - 16), "16A", fill=(185, 28, 28), font=font(9, True), anchor="mm")
            rr(d, [tx - 5, mcb_y - 4, tx + 5, mcb_y + 14], 2, (34, 197, 94))
            stagger = (idx % 2) * 58
            card_y = 175 + stagger
            wire(d, [(tx, mcb_y - 28), (tx, card_y + 70)], INK, 4)
            wire(d, [(tx, n_y), (tx, card_y)], N, 3)
            rr(d, [tx - 56, card_y, tx + 56, card_y + 70], 10, (255, 255, 255), (120, 130, 140), 2)
            d.ellipse([tx - 52, card_y + 8, tx - 28, card_y + 32], fill=(15, 76, 129))
            d.text((tx - 40, card_y + 20), str(num), fill=(255, 255, 255), font=font(13, True), anchor="mm")
            d.text((tx + 14, card_y + 20), out, fill=(80, 90, 100), font=font(12, True), anchor="mm")
            d.text((tx, card_y + 48), name.split()[0], fill=INK, font=font(12, True), anchor="mm")
            if len(name.split()) > 1:
                d.text((tx, card_y + 64), " ".join(name.split()[1:]), fill=INK, font=font(11, True), anchor="mm")

    place_loads(s1, SHELLY1)
    place_loads(s2, SHELLY2)

    # Source credit
    rr(d, [90, 1320, W - 90, 1520], 12, (248, 250, 252), (200, 210, 220), 2)
    d.text((110, 1340), "Componenti reali nel render", fill=INK, font=font(18, True))
    d.text((110, 1372), "• Shelly Pro 4PM: foto ufficiale shelly.com (cutout)", fill=(51, 65, 85), font=font(14))
    d.text((110, 1396), "• Magnetotermico differenziale: cutout RCBO 2P 40A 30mA Tipo A", fill=(51, 65, 85), font=font(14))
    d.text((110, 1420), "Cablaggio (corretto): L/N → alto RCBO → BUS → Shelly (L alto, N basso); Ox → MCB → carico; ETH solo LAN; PE separata.", fill=(51, 65, 85), font=font(14))
    d.text((110, 1450), "S1–S4 non collegati. Limiti Pro 4PM: 16 A/canale, 40 A totali.", fill=(146, 64, 14), font=font(14, True))
    d.text((110, 1485), "Fonte Shelly: https://www.shelly.com/products/shelly-pro-4pm", fill=(100, 116, 139), font=font(12))

    # finish
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.15)
    rgb = Image.blend(rgb, rgb.filter(ImageFilter.GaussianBlur(0.7)), 0.1)
    noise = Image.effect_noise((W, H), 8).convert("RGB")
    rgb = Image.blend(rgb, noise, 0.03)
    return rgb


def main():
    img = build()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    for path in (OUT_DIR / "quadro-elettrico-cucina-foto.jpg", ART_DIR / "quadro-elettrico-cucina-foto.jpg"):
        img.save(path, quality=93, optimize=True)
        print("wrote", path)


if __name__ == "__main__":
    main()
