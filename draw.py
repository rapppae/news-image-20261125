#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper poster summing up world news of
Wednesday 25 November 2026. Original artwork drawn from scratch with PIL:
no copied images, no photos, no external assets. Run: python3 draw.py
Writes entry.png (1024x1024) next to this file."""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 24, 34)
NAVY = (18, 36, 62)
NAVY2 = (28, 54, 92)
RED = (178, 34, 34)
TEAL = (13, 110, 102)
AMBER = (176, 112, 8)
SLATE = (84, 92, 106)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None, max_lines=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y, len(lines)


def kicker(draw, x, y, label, color):
    f = font(SANS_B, 20)
    draw.text((x, y), label.upper(), font=f, fill=color)
    return y + 28


# ---------- simple icons, drawn with shapes only ----------

def icon_ship(d, cx, cy, s, col):
    # hull
    d.polygon([(cx - 52 * s, cy + 6 * s), (cx + 52 * s, cy + 6 * s),
               (cx + 36 * s, cy + 30 * s), (cx - 36 * s, cy + 30 * s)], fill=col)
    d.rectangle([cx - 26 * s, cy - 18 * s, cx + 26 * s, cy + 6 * s], fill=col)
    d.rectangle([cx - 3 * s, cy - 52 * s, cx + 3 * s, cy - 18 * s], fill=col)
    d.polygon([(cx + 3 * s, cy - 50 * s), (cx + 30 * s, cy - 30 * s),
               (cx + 3 * s, cy - 30 * s)], fill=col)
    for wx in (-58, -18, 22, 58):
        d.arc([cx + wx * s - 16 * s, cy + 38 * s, cx + wx * s + 16 * s, cy + 52 * s],
              200, 340, fill=col, width=4)


def icon_globe_leaf(d, cx, cy, s, col):
    d.ellipse([cx - 46 * s, cy - 46 * s, cx + 46 * s, cy + 46 * s], outline=col, width=6)
    d.ellipse([cx - 18 * s, cy - 46 * s, cx + 18 * s, cy + 46 * s], outline=col, width=4)
    d.line([cx - 46 * s, cy, cx + 46 * s, cy], fill=col, width=4)
    # leaf
    d.pieslice([cx + 2 * s, cy - 34 * s, cx + 44 * s, cy + 8 * s], 270, 90, fill=col)
    d.line([cx + 6 * s, cy - 30 * s, cx + 40 * s, cy + 4 * s], fill=PAPER, width=3)


def icon_chip(d, cx, cy, s, col):
    d.rectangle([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s], fill=col)
    d.rectangle([cx - 18 * s, cy - 18 * s, cx + 18 * s, cy + 18 * s], fill=PAPER)
    d.rectangle([cx - 10 * s, cy - 10 * s, cx + 10 * s, cy + 10 * s], fill=col)
    for dx in (-22, 0, 22):
        d.line([cx + dx * s, cy - 48 * s, cx + dx * s, cy - 34 * s], fill=col, width=5)
        d.line([cx + dx * s, cy + 34 * s, cx + dx * s, cy + 48 * s], fill=col, width=5)
        d.line([cx - 48 * s, cy + dx * s, cx - 34 * s, cy + dx * s], fill=col, width=5)
        d.line([cx + 34 * s, cy + dx * s, cx + 48 * s, cy + dx * s], fill=col, width=5)


def icon_tower(d, cx, cy, s, col):
    # plain skyscraper: tapered shaft, antenna, windows, base
    d.polygon([(cx - 16 * s, cy + 48 * s), (cx - 9 * s, cy - 30 * s),
               (cx + 9 * s, cy - 30 * s), (cx + 16 * s, cy + 48 * s)], fill=col)
    d.line([cx, cy - 54 * s, cx, cy - 30 * s], fill=col, width=5)
    d.ellipse([cx - 5 * s, cy - 60 * s, cx + 5 * s, cy - 50 * s], fill=col)
    for wy in (-18, -2, 14, 30):
        d.rectangle([cx - 5 * s, cy + wy * s, cx + 5 * s, cy + (wy + 7) * s],
                    fill=PAPER)
    d.rectangle([cx - 30 * s, cy + 44 * s, cx + 30 * s, cy + 52 * s], fill=col)


def icon_handshake_map(d, cx, cy, s, col):
    # two overlapping shields = pact; star on top
    d.rounded_rectangle([cx - 48 * s, cy - 26 * s, cx + 2 * s, cy + 34 * s],
                        radius=10, outline=col, width=6)
    d.rounded_rectangle([cx - 2 * s, cy - 26 * s, cx + 48 * s, cy + 34 * s],
                        radius=10, fill=col)
    d.text((cx + 10 * s, cy - 12 * s), "AU", font=font(SANS_B, int(20 * s)), fill=WHITE)
    d.text((cx - 38 * s, cy - 12 * s), "SB", font=font(SANS_B, int(20 * s)), fill=col)
    d.polygon([(cx, cy - 52 * s), (cx + 6 * s, cy - 38 * s), (cx - 6 * s, cy - 38 * s)],
              fill=col)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-176) ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 176], fill=RED)
    d.text((36, 22), "THE WORLD  •  IN ONE PAGE", font=font(SANS_B, 24), fill=(180, 200, 225))
    d.text((36, 52), "WORLD NEWS", font=font(SERIF_B, 64), fill=WHITE)
    d.text((36, 122), "Wednesday 25 November 2026", font=font(SERIF_B, 34), fill=(255, 214, 130))
    d.text((W - 36, 30), "FIVE STORIES\nTHAT MATTERED", font=font(SANS_B, 22),
           fill=(180, 200, 225), anchor="ra", align="right")

    # ---- hero: Ukraine (196-448) ----
    hx, hy, hw, hh = 28, 196, W - 56, 252
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=14, fill=NAVY2)
    d.rectangle([hx, hy, hx + 10, hy + hh], fill=RED)
    icon_ship(d, hx + 92, hy + 128, 1.0, (255, 214, 130))
    kicker(d, hx + 190, hy + 18, "War in Europe — the Baltic & Libya", (255, 120, 120))
    d.text((hx + 190, hy + 48), "Ukraine strikes Russian ships",
           font=font(SERIF_B, 38), fill=WHITE)
    text_block(d, (hx + 190, hy + 102),
               "Zelenskiy confirms a drone strike on a Russian cargo ship in the "
               "Gulf of Finland. Kyiv also says it sank a Russian warship off "
               "Libya; Moscow calls the attacks terrorism.",
               font(SANS, 24), (225, 232, 242), hw - 220, leading=31, max_lines=3)
    d.text((hx + 190, hy + 212), "KYIV  •  MOSCOW  •  BENGHAZI",
           font=font(SANS_B, 19), fill=(180, 200, 225))

    # ---- 2x2 grid (464-880) ----
    cards = [
        ("Climate — Antalya", TEAL, "COP31 ends with no deal",
         "UN climate summit in Turkey collapses: oil and gas producers block "
         "fossil-fuel phase-out.", icon_globe_leaf),
        ("Tech & markets", AMBER, "Huang back at Nvidia",
         "Nvidia reinstates Jensen Huang as CEO after Trump intervened; "
         "AI shares slide in Asia.", icon_chip),
        ("Middle East", RED, "Houthis hit Riyadh tower",
         "Strike on Riyadh's tallest tower wounds 11; Houthi forces advance "
         "to 60 km from Aden.", icon_tower),
        ("Pacific security", NAVY2, "Australia–Solomon pact",
         "Security deal names Australia the Solomons' primary partner, "
         "ruling out foreign bases.", icon_handshake_map),
    ]
    gx, gy = 28, 464
    cw, ch, gap = (W - 56 - 16) // 2, 200, 16
    for i, (kick, col, head, body, icon) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=CARD,
                            outline=(210, 205, 190), width=2)
        d.rectangle([x, y, x + cw, y + 8], fill=col)
        icon(d, x + 62, y + 72, 0.68, col)
        kicker(d, x + 126, y + 16, kick, col)
        head_f = font(SERIF_B, 26)
        _, n_head = text_block(d, (x + 126, y + 44), head, head_f, INK,
                               cw - 146, leading=31, max_lines=2)
        body_y = y + 44 + n_head * 31 + 6
        text_block(d, (x + 126, body_y), body, font(SANS, 20), (52, 58, 70),
                   cw - 146, leading=25, max_lines=3)

    # ---- ticker strip (896-972) ----
    ty = 896
    d.rounded_rectangle([28, ty, W - 28, ty + 76], radius=10, fill=INK)
    d.text((52, ty + 24), "ALSO TODAY", font=font(SANS_B, 22), fill=(255, 214, 130))
    text_block(d, (52 + 168, ty + 10),
               "Gaza toll reported at 74,746  •  NATO warns over a Russian "
               "nuclear satellite  •  S. Korea minister quits over exam scandal",
               font(SANS, 20), WHITE, W - 56 - 220, leading=26, max_lines=2)

    # ---- footer (986-1014) ----
    d.text((28, 984), "Drawn from events reported on 25 November 2026 — Reuters, AP and other wire reports.",
           font=font(SANS, 18), fill=SLATE)
    d.text((28, 1008), "One day, five stories.  •  make.fun news-image-20261125",
           font=font(SANS, 18), fill=SLATE)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
