#!/usr/bin/env python3
"""Render fotorealistico del quadro cucina con cablaggio corretto (PIL)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

OUT_DIR = Path(__file__).resolve().parent
ART_DIR = Path("/opt/cursor/artifacts")

W, H = 2200, 1500
L = (122, 62, 29)       # marrone fase
N = (30, 64, 175)       # blu neutro
PE = (161, 98, 7)
ETH = (30, 58, 138)
METAL = (100, 116, 139)
INK = (15, 23, 42)

SHELLY1 = [("O4", 4, "Frigorifero"), ("O3", 3, "Forno"), ("O2", 2, "Microonde"), ("O1", 1, "Lavastoviglie")]
SHELLY2 = [("O4", 8, "Prese int. mobile"), ("O3", 7, "Prese piano lavoro"), ("O2", 6, "Prese piano cottura"), ("O1", 5, "Piano cottura")]


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = f"/usr/share/fonts/truetype/dejavu/{name}"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def rr(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient_rect(img, box, c1, c2, vertical=True):
    x0, y0, x1, y1 = box
    crop = img.crop((x0, y0, x1, y1))
    w, h = crop.size
    for i in range(h if vertical else w):
        t = i / max((h if vertical else w) - 1, 1)
        col = tuple(int(c1[j] * (1 - t) + c2[j] * t) for j in range(3))
        line = Image.new("RGB", (w, 1) if vertical else (1, h), col)
        if vertical:
            crop.paste(line, (0, i))
        else:
            crop.paste(line, (i, 0))
    img.paste(crop, (x0, y0))


def screw(draw, cx, cy, r=6):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(75, 85, 99), outline=(31, 41, 55))
    draw.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=(203, 213, 225))
    draw.line([cx - r + 3, cy, cx + r - 3, cy], fill=(51, 65, 85), width=2)
    draw.line([cx, cy - r + 3, cx, cy + r - 3], fill=(51, 65, 85), width=2)


def wire(draw, pts, color, width=5):
    draw.line(pts, fill=color, width=width, joint="curve")
    # highlight
    hi = tuple(min(255, c + 40) for c in color)
    draw.line(pts, fill=hi + (0,), width=max(1, width // 4))  # ignored alpha on RGB; ok
    draw.line([(x, y - 1) for x, y in pts], fill=hi, width=max(1, width // 5))


def label_chip(draw, xy, text, bg, fg=(255, 255, 255)):
    x, y = xy
    f = font(16, True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    rr(draw, [x, y, x + tw + 16, y + th + 10], 8, bg, outline=(255, 255, 255), width=1)
    draw.text((x + 8, y + 4), text, fill=fg, font=f)


def draw_rcbo(img, draw, x, y, w, h):
    gradient_rect(img, (x, y, x + w, y + h), (255, 255, 255), (210, 215, 222))
    rr(draw, [x, y, x + w, y + h], 8, None, outline=(100, 116, 139), width=2)
    rr(draw, [x + 10, y + 12, x + w - 10, y + 58], 6, (248, 250, 252), (203, 213, 225))
    draw.text((x + w // 2, y + 28), "RCBO", fill=INK, font=font(18, True), anchor="mm")
    draw.text((x + w // 2, y + 48), "2P 40A 30mA", fill=(100, 116, 139), font=font(12), anchor="mm")
    # TEST
    rr(draw, [x + 28, y + 75, x + w - 28, y + 105], 6, (220, 38, 38))
    draw.text((x + w // 2, y + 90), "TEST", fill=(255, 255, 255), font=font(14, True), anchor="mm")
    # lever
    rr(draw, [x + w // 2 - 22, y + 120, x + w // 2 + 22, y + 210], 8, (226, 232, 240), (51, 65, 85), 2)
    rr(draw, [x + w // 2 - 18, y + 126, x + w // 2 + 18, y + 168], 6, (34, 197, 94))
    draw.text((x + w // 2, y + 195), "ON", fill=(22, 101, 52), font=font(14, True), anchor="mm")
    # terminals
    for i, lab in enumerate(["L", "N"]):
        tx = x + 40 + i * 70
        rr(draw, [tx - 16, y - 8, tx + 16, y + 14], 3, (107, 114, 128))
        screw(draw, tx, y + 3, 5)
        col = L if lab == "L" else N
        draw.text((tx, y + 28), lab, fill=col, font=font(14, True), anchor="mm")
        rr(draw, [tx - 16, y + h - 14, tx + 16, y + h + 8], 3, (107, 114, 128))
        screw(draw, tx, y + h - 3, 5)
    return {"L_top": (x + 40, y), "N_top": (x + 110, y), "L_bot": (x + 40, y + h), "N_bot": (x + 110, y + h)}


def draw_shelly(img, draw, x, y, w, h, title, eth):
    gradient_rect(img, (x, y, x + w, y + h), (250, 251, 252), (180, 186, 194))
    rr(draw, [x, y, x + w, y + h], 10, None, outline=(100, 116, 139), width=2)
    # side brand
    gradient_rect(img, (x, y, x + 34, y + h), (209, 213, 219), (156, 163, 175), vertical=True)
    for i, ch in enumerate("Shelly"):
        draw.text((x + 17, y + 70 + i * 28), ch, fill=(51, 65, 85), font=font(14, True), anchor="mm")
    # face
    rr(draw, [x + 48, y + 48, x + w - 18, y + 210], 10, (233, 237, 241), (203, 213, 225))
    # LCD
    rr(draw, [x + 110, y + 62, x + 360, y + 155], 8, (11, 18, 32))
    for i in range(0, 90, 3):
        draw.line([x + 112, y + 64 + i, x + 358, y + 64 + i], fill=(30, 41, 59), width=1)
    draw.text((x + 235, y + 95), title, fill=(125, 211, 252), font=font(18, True), anchor="mm")
    draw.text((x + 235, y + 120), "Pro 4PM · 4×16A", fill=(148, 163, 184), font=font(12), anchor="mm")
    draw.text((x + 130, y + 142), "● online", fill=(74, 222, 128), font=font(12))
    draw.text((x + 340, y + 142), eth, fill=(56, 189, 248), font=font(12), anchor="rm")
    # buttons
    for i, lab in enumerate(["▲", "▼", "OK"]):
        bx = x + 140 + i * 70
        rr(draw, [bx, y + 168, bx + 55, y + 198], 6, (229, 231, 235), (100, 116, 139))
        draw.text((bx + 27, y + 183), lab, fill=(51, 65, 85), font=font(13, True), anchor="mm")
    # top terminals O4 O3 L O2 O1
    labels = ["O4", "O3", "L", "O2", "O1"]
    xs = {}
    span = w - 70
    x0 = x + 50
    for i, lab in enumerate(labels):
        tx = int(x0 + span * (i + 0.5) / 5)
        xs[lab] = tx
        rr(draw, [tx - 15, y - 10, tx + 15, y + 12], 3, (107, 114, 128))
        screw(draw, tx, y + 1, 5)
        col = L if lab == "L" else INK
        draw.text((tx, y + 26), lab, fill=col, font=font(13, True), anchor="mm")
    # bottom LAN N S
    lan = (x + 75, y + h)
    rr(draw, [lan[0] - 22, lan[1] - 18, lan[0] + 22, lan[1] + 6], 3, (15, 23, 42))
    for i in range(8):
        draw.rectangle([lan[0] - 14 + i * 4, lan[1] - 12, lan[0] - 12 + i * 4, lan[1] - 2], fill=(203, 213, 225))
    draw.text((lan[0], lan[1] + 18), "LAN", fill=(100, 116, 139), font=font(11), anchor="mm")
    nx = x + 140
    rr(draw, [nx - 15, y + h - 10, nx + 15, y + h + 10], 3, (107, 114, 128))
    screw(draw, nx, y + h, 5)
    draw.text((nx, y + h - 18), "N", fill=N, font=font(13, True), anchor="mm")
    for i, lab in enumerate(["S4", "S3", "S2", "S1"]):
        sx = x + 210 + i * 55
        rr(draw, [sx - 12, y + h - 8, sx + 12, y + h + 8], 3, (148, 163, 184))
        screw(draw, sx, y + h, 4)
        draw.text((sx, y + h + 20), lab, fill=(148, 163, 184), font=font(10), anchor="mm")
    draw.text((x + w - 12, y + h + 38), "S1–S4 non collegati", fill=(148, 163, 184), font=font(11), anchor="rm")
    return {"terms": xs, "N": (nx, y + h), "LAN": lan, "top": y, "bottom": y + h}


def draw_mcb(img, draw, cx, cy):
    gradient_rect(img, (cx - 16, cy - 34, cx + 16, cy + 34), (255, 255, 255), (220, 220, 220))
    rr(draw, [cx - 16, cy - 34, cx + 16, cy + 34], 4, None, (107, 114, 128), 1)
    rr(draw, [cx - 12, cy - 28, cx + 12, cy - 14], 3, (254, 226, 226), (239, 68, 68))
    draw.text((cx, cy - 21), "16A", fill=(185, 28, 28), font=font(9, True), anchor="mm")
    rr(draw, [cx - 6, cy - 8, cx + 6, cy + 18], 3, (226, 232, 240), (51, 65, 85))
    rr(draw, [cx - 5, cy - 6, cx + 5, cy + 6], 2, (34, 197, 94))
    screw(draw, cx, cy - 30, 3)
    screw(draw, cx, cy + 26, 3)


def draw_load_card(draw, cx, cy, num, name, out):
    rr(draw, [cx - 58, cy, cx + 58, cy + 78], 10, (255, 255, 255), (148, 163, 184), 2)
    draw.ellipse([cx - 56, cy + 8, cx - 32, cy + 32], fill=(15, 76, 129))
    draw.text((cx - 44, cy + 20), str(num), fill=(255, 255, 255), font=font(14, True), anchor="mm")
    draw.text((cx + 12, cy + 20), out, fill=(100, 116, 139), font=font(12, True), anchor="mm")
    # simple appliance glyph
    draw.rounded_rectangle([cx - 22, cy + 38, cx + 22, cy + 68], 4, outline=(51, 65, 85), width=2)
    draw.text((cx, cy + 53), {1: "LV", 2: "MO", 3: "FO", 4: "FR", 5: "PC", 6: "PR", 7: "PL", 8: "PM"}.get(num, "·"),
              fill=(15, 76, 129), font=font(11, True), anchor="mm")
    words = name.split()
    if len(name) > 14 and len(words) > 1:
        mid = max(1, len(words) // 2)
        draw.text((cx, cy + 90), " ".join(words[:mid]), fill=INK, font=font(12, True), anchor="mm")
        draw.text((cx, cy + 106), " ".join(words[mid:]), fill=INK, font=font(12, True), anchor="mm")
    else:
        draw.text((cx, cy + 94), name, fill=INK, font=font(12, True), anchor="mm")


def build() -> Image.Image:
    img = Image.new("RGB", (W, H), (71, 85, 105))
    draw = ImageDraw.Draw(img)

    # cabinet shell
    gradient_rect(img, (40, 40, W - 40, H - 40), (229, 231, 235), (100, 116, 139))
    rr(draw, [40, 40, W - 40, H - 40], 16, None, (51, 65, 85), 4)
    # inner
    rr(draw, [70, 90, W - 70, H - 70], 8, (203, 213, 225), (148, 163, 184), 2)
    # perforated plate
    for yy in range(120, H - 100, 16):
        for xx in range(100, W - 100, 16):
            draw.ellipse([xx, yy, xx + 3, yy + 3], fill=(148, 163, 184))

    # title plate
    rr(draw, [90, 55, 820, 100], 8, (248, 250, 252), (255, 255, 255), 1)
    draw.text((110, 67), "Quadro elettrico cucina", fill=INK, font=font(28, True))
    draw.text((110, 100), "Render · cablaggio corretto da schema tecnico", fill=(71, 85, 105), font=font(14))

    # legend colors
    for i, (c, t) in enumerate([(L, "L fase"), (N, "N neutro"), (ETH, "ETH"), (PE, "PE")]):
        x = 1600 + i * 120
        rr(draw, [x, 65, x + 18, 83], 4, c)
        draw.text((x + 26, 67), t, fill=(248, 250, 252), font=font(13, True))

    # DIN rail
    din_y = 820
    gradient_rect(img, (110, din_y, W - 110, din_y + 36), (248, 250, 252), (71, 85, 105))
    draw.rectangle([110, din_y + 10, W - 110, din_y + 16], fill=(255, 255, 255))
    draw.text((120, din_y + 48), "Guida DIN 35 mm", fill=(51, 65, 85), font=font(12))

    # N bar top
    n_y = 150
    draw.rectangle([140, n_y - 8, W - 220, n_y + 8], fill=N)
    for i in range(16):
        screw(draw, 180 + i * 70, n_y, 4)
    label_chip(draw, (W - 300, n_y - 18), "MORSETTIERA N", (219, 234, 254), N)

    # buses
    l_bus_y = 980
    n_bus_y = 1080
    draw.line([(160, l_bus_y), (W - 160, l_bus_y)], fill=L, width=8)
    draw.line([(160, n_bus_y), (W - 160, n_bus_y)], fill=N, width=8)
    label_chip(draw, (W - 280, l_bus_y - 16), "BUS L", (254, 243, 199), L)
    label_chip(draw, (W - 280, n_bus_y - 16), "BUS N", (219, 234, 254), N)
    # PE
    draw.rectangle([140, 1160, 420, 1178], fill=PE)
    for i in range(0, 280, 14):
        draw.rectangle([140 + i, 1160, 147 + i, 1178], fill=(22, 101, 52))
    draw.text((280, 1195), "BARRA PE", fill=PE, font=font(13, True), anchor="mm")

    # RCBO
    rcbo = draw_rcbo(img, draw, 120, din_y - 290, 150, 300)

    # supply into top of RCBO
    wire(draw, [(100, 1120), (100, 480), (rcbo["L_top"][0], 480), rcbo["L_top"]], L, 6)
    wire(draw, [(250, 1120), (250, 480), (rcbo["N_top"][0], 480), rcbo["N_top"]], N, 6)
    label_chip(draw, (70, 1125), "L rete", (254, 243, 199), L)
    label_chip(draw, (220, 1125), "N rete", (219, 234, 254), N)

    # RCBO out to buses
    wire(draw, [rcbo["L_bot"], (rcbo["L_bot"][0], l_bus_y), (W - 200, l_bus_y)], L, 7)
    wire(draw, [rcbo["N_bot"], (rcbo["N_bot"][0], n_bus_y), (W - 200, n_bus_y)], N, 7)
    wire(draw, [(W - 250, n_y), (W - 250, n_bus_y)], N, 6)

    # Shellys
    s1 = draw_shelly(img, draw, 340, din_y - 290, 520, 310, "SHELLY #1", "ETH 1")
    s2 = draw_shelly(img, draw, 980, din_y - 290, 520, 310, "SHELLY #2", "ETH 2")

    # power to Shellys
    for s in (s1, s2):
        wire(draw, [(s["terms"]["L"], s["top"]), (s["terms"]["L"], l_bus_y)], L, 5)
        wire(draw, [s["N"], (s["N"][0], n_bus_y)], N, 5)

    # ETH only to LAN, exit right as data (NOT to PE)
    for s, label, xoff in ((s1, "ETH 1", 0), (s2, "ETH 2", 80)):
        lx, ly = s["LAN"]
        wire(draw, [(lx, ly + 8), (lx, 1140), (1700 + xoff, 1140), (1700 + xoff, 1220)], ETH, 5)
        label_chip(draw, (1660 + xoff, 1225), label, (30, 58, 138), (248, 250, 252))

    # loads + MCB
    def loads_for(s, mapping):
        for idx, (out, num, name) in enumerate(mapping):
            tx = s["terms"][out]
            mcb_y = 430
            wire(draw, [(tx, s["top"]), (tx, mcb_y + 34)], INK, 4)
            draw_mcb(img, draw, tx, mcb_y)
            stagger = (idx % 2) * 55
            card_y = 175 + stagger
            wire(draw, [(tx, mcb_y - 34), (tx, card_y + 78)], INK, 4)
            wire(draw, [(tx, n_y), (tx, card_y)], N, 3)
            draw_load_card(draw, tx, card_y, num, name, out)

    loads_for(s1, SHELLY1)
    loads_for(s2, SHELLY2)

    # footer rules
    rr(draw, [90, 1240, W - 90, 1430], 12, (248, 250, 252), (203, 213, 225), 2)
    draw.text((110, 1260), "Cablaggio corretto (questo render)", fill=INK, font=font(18, True))
    rules = [
        "1. L/N rete → morsetti ALTI del RCBO",
        "2. Uscite RCBO → BUS L (marrone) e BUS N (blu)",
        "3. Shelly: L sul morsetto alto centrale · N sul morsetto basso",
        "4. Ox → MCB 16A → carico · neutro carico → MORSETTIERA N",
        "5. ETH1/ETH2 SOLO porte LAN (non PE, non S, non L/N)",
        "6. S1–S4 non collegati · barra PE separata",
    ]
    for i, r in enumerate(rules):
        col = i % 2
        row = i // 2
        draw.text((110 + col * 980, 1300 + row * 28), r, fill=(51, 65, 85), font=font(15))

    # photographic finish
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    blur = img.filter(ImageFilter.GaussianBlur(0.8))
    img = Image.blend(img, blur, 0.12)
    noise = Image.effect_noise((W, H), 10).convert("RGB")
    img = Image.blend(img, noise, 0.035)
    return img


def main():
    img = build()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    for path in (
        OUT_DIR / "quadro-elettrico-cucina-foto.jpg",
        ART_DIR / "quadro-elettrico-cucina-foto.jpg",
    ):
        img.save(path, quality=93, optimize=True)
        print("wrote", path)


if __name__ == "__main__":
    main()
