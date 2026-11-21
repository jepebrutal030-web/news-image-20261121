#!/usr/bin/env python3
"""Draw the 21 November 2026 world news image.

Flat vector style, six stories, one 1024x1024 PNG. Run it with:
    python3 draw.py
It writes entry.png next to this script. Only the standard library
plus Pillow is used, and the output is deterministic.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
NAVY = (20, 33, 61)
GOLD = (233, 180, 76)
WHITE = (255, 255, 255)
INK = (20, 33, 61)
GREY = (74, 74, 68)
CARD_BORDER = (227, 220, 203)
FOOTER_GREY = (110, 105, 92)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_missile(d, cx, cy, s, color):
    """Stylised missile pointing up right, with a flame."""
    body = [
        (cx - 0.16 * s, cy + 0.28 * s),
        (cx - 0.30 * s, cy + 0.05 * s),
        (cx - 0.10 * s, cy - 0.34 * s),
        (cx + 0.10 * s, cy - 0.34 * s),
        (cx + 0.30 * s, cy + 0.05 * s),
        (cx + 0.16 * s, cy + 0.28 * s),
    ]
    d.polygon(body, fill=color)
    d.polygon(
        [(cx - 0.30 * s, cy + 0.05 * s), (cx - 0.48 * s, cy + 0.30 * s),
         (cx - 0.16 * s, cy + 0.22 * s)],
        fill=color,
    )
    d.polygon(
        [(cx + 0.30 * s, cy + 0.05 * s), (cx + 0.48 * s, cy + 0.30 * s),
         (cx + 0.16 * s, cy + 0.22 * s)],
        fill=color,
    )
    d.polygon(
        [(cx - 0.10 * s, cy + 0.30 * s), (cx + 0.10 * s, cy + 0.30 * s),
         (cx, cy + 0.52 * s)],
        fill=(255, 176, 32),
    )


def draw_chart(d, cx, cy, s, color):
    """Falling market chart with axes and an arrowhead."""
    d.line([(cx - 0.42 * s, cy + 0.40 * s), (cx + 0.44 * s, cy + 0.40 * s)],
           fill=color, width=max(3, int(s * 0.07)))
    d.line([(cx - 0.42 * s, cy + 0.40 * s), (cx - 0.42 * s, cy - 0.44 * s)],
           fill=color, width=max(3, int(s * 0.07)))
    pts = [
        (cx - 0.36 * s, cy - 0.28 * s),
        (cx - 0.12 * s, cy - 0.12 * s),
        (cx + 0.10 * s, cy - 0.22 * s),
        (cx + 0.36 * s, cy + 0.28 * s),
    ]
    d.line(pts, fill=color, width=max(4, int(s * 0.09)), joint="curve")
    d.polygon(
        [(cx + 0.36 * s, cy + 0.28 * s), (cx + 0.14 * s, cy + 0.24 * s),
         (cx + 0.32 * s, cy + 0.06 * s)],
        fill=color,
    )


def draw_scales(d, cx, cy, s, color):
    """Scales of justice."""
    d.line([(cx, cy - 0.42 * s), (cx, cy + 0.40 * s)],
           fill=color, width=max(3, int(s * 0.07)))
    d.line([(cx - 0.42 * s, cy - 0.30 * s), (cx + 0.42 * s, cy - 0.30 * s)],
           fill=color, width=max(3, int(s * 0.07)))
    d.ellipse([cx - 0.08 * s, cy - 0.50 * s, cx + 0.08 * s, cy - 0.34 * s],
              fill=color)
    for sx in (-0.42 * s, 0.42 * s):
        d.line([(cx + sx, cy - 0.30 * s), (cx + sx - 0.16 * s, cy + 0.06 * s)],
               fill=color, width=max(2, int(s * 0.04)))
        d.line([(cx + sx, cy - 0.30 * s), (cx + sx + 0.16 * s, cy + 0.06 * s)],
               fill=color, width=max(2, int(s * 0.04)))
        d.pieslice([cx + sx - 0.18 * s, cy - 0.02 * s,
                    cx + sx + 0.18 * s, cy + 0.34 * s],
                   start=0, end=180, fill=color)
    d.rectangle([cx - 0.20 * s, cy + 0.40 * s, cx + 0.20 * s, cy + 0.48 * s],
                fill=color)


def draw_flags(d, cx, cy, s, color):
    """Two flags on poles."""
    d.line([(cx - 0.30 * s, cy - 0.42 * s), (cx - 0.30 * s, cy + 0.44 * s)],
           fill=color, width=max(3, int(s * 0.06)))
    d.line([(cx + 0.18 * s, cy - 0.42 * s), (cx + 0.18 * s, cy + 0.44 * s)],
           fill=color, width=max(3, int(s * 0.06)))
    d.polygon(
        [(cx - 0.30 * s, cy - 0.42 * s), (cx + 0.06 * s, cy - 0.42 * s),
         (cx - 0.06 * s, cy - 0.18 * s), (cx - 0.30 * s, cy - 0.18 * s)],
        fill=color,
    )
    d.polygon(
        [(cx + 0.18 * s, cy - 0.42 * s), (cx + 0.50 * s, cy - 0.42 * s),
         (cx + 0.38 * s, cy - 0.18 * s), (cx + 0.18 * s, cy - 0.18 * s)],
        fill=(255, 176, 32),
    )


def draw_globe(d, cx, cy, s, color):
    """Globe with a small sun above it."""
    d.ellipse([cx - 0.34 * s, cy - 0.22 * s, cx + 0.34 * s, cy + 0.46 * s],
              outline=color, width=max(3, int(s * 0.07)))
    d.ellipse([cx - 0.34 * s, cy - 0.22 * s, cx + 0.34 * s, cy + 0.46 * s],
              fill=None)
    d.arc([cx - 0.34 * s, cy - 0.22 * s, cx + 0.34 * s, cy + 0.46 * s],
          start=90, end=270, fill=color, width=max(2, int(s * 0.04)))
    d.line([(cx - 0.34 * s, cy + 0.12 * s), (cx + 0.34 * s, cy + 0.12 * s)],
           fill=color, width=max(2, int(s * 0.04)))
    d.ellipse([cx + 0.17 * s, cy - 0.43 * s, cx + 0.39 * s, cy - 0.21 * s],
              fill=(255, 176, 32))
    for ang in (0, 45, 90, 135, 180, 225, 270, 315):
        import math
        r1 = 0.14 * s
        r2 = 0.20 * s
        x1 = cx + 0.28 * s + r1 * math.cos(math.radians(ang))
        y1 = cy - 0.32 * s + r1 * math.sin(math.radians(ang))
        x2 = cx + 0.28 * s + r2 * math.cos(math.radians(ang))
        y2 = cy - 0.32 * s + r2 * math.sin(math.radians(ang))
        d.line([(x1, y1), (x2, y2)], fill=(255, 176, 32),
               width=max(2, int(s * 0.04)))


def draw_pill(d, cx, cy, s, color):
    """Capsule pill, tilted, two halves."""
    pill = Image.new("RGBA", (int(s), int(s)), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    x0, y0, x1, y1 = 0.10 * s, 0.32 * s, 0.90 * s, 0.68 * s
    r = (y1 - y0) / 2
    w = max(2, int(s * 0.04))
    pd.ellipse([x0, y0, x0 + 2 * r, y1], fill=color)
    pd.rectangle([x0 + r, y0, 0.50 * s, y1], fill=color)
    pd.ellipse([x1 - 2 * r, y0, x1, y1], fill=WHITE)
    pd.rectangle([0.50 * s, y0, x1 - r, y1], fill=WHITE)
    pd.ellipse([x0, y0, x0 + 2 * r, y1], outline=color, width=w)
    pd.ellipse([x1 - 2 * r, y0, x1, y1], outline=color, width=w)
    pd.line([(x0 + r, y0), (x1 - r, y0)], fill=color, width=w)
    pd.line([(x0 + r, y1), (x1 - r, y1)], fill=color, width=w)
    pill = pill.rotate(38, resample=Image.BICUBIC, center=(s / 2, s / 2))
    d._image.paste(pill, (int(cx - s / 2), int(cy - s / 2)), pill)


STORIES = [
    {
        "tag": "CONFLICT",
        "accent": (192, 57, 43),
        "icon": draw_missile,
        "headline": "RUSSIA STRIKES KYIV, MISSILES LAND IN POLAND",
        "caption": "400 drones and 110 missiles hit Ukraine. Warsaw calls it a deliberate provocation.",
    },
    {
        "tag": "MARKETS",
        "accent": (211, 84, 0),
        "icon": draw_chart,
        "headline": "AI SELL-OFF DRAGS S&P INTO CORRECTION",
        "caption": "US stocks fell 3.7 percent. The Nasdaq erased all its 2026 gains.",
    },
    {
        "tag": "JUSTICE",
        "accent": (20, 122, 138),
        "icon": draw_scales,
        "headline": "ICJ: MYANMAR GUILTY OF ROHINGYA GENOCIDE",
        "caption": "The Hague court finds Myanmar responsible for genocide against the Rohingya.",
    },
    {
        "tag": "POLITICS",
        "accent": (46, 90, 172),
        "icon": draw_flags,
        "headline": "UK AND EU SIGN BIGGEST POST-BREXIT DEALS",
        "caption": "Three deals in Brussels: food trade, carbon markets and youth mobility.",
    },
    {
        "tag": "CLIMATE",
        "accent": (46, 125, 50),
        "icon": draw_globe,
        "headline": "COP31 CLIMATE TALKS RUN PAST DEADLINE",
        "caption": "The Antalya summit stalls as nearly 200 nations fail to agree on fossil fuels.",
    },
    {
        "tag": "HEALTH",
        "accent": (108, 52, 131),
        "icon": draw_pill,
        "headline": "PANCREATIC CANCER PILL BREAKTHROUGH",
        "caption": "Trial pill daraxonrasib made tumours undetectable in 1 in 12 patients.",
    },
]


def draw_panel(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14,
                        fill=WHITE, outline=CARD_BORDER, width=2)
    accent = story["accent"]
    chip = 92
    cx0, cy0 = x + 18, y + 18
    d.rounded_rectangle([cx0, cy0, cx0 + chip, cy0 + chip], radius=14,
                        fill=accent)
    story["icon"](d, cx0 + chip / 2, cy0 + chip / 2, 84, WHITE)
    tx = cx0 + chip + 16
    tw = x + w - 18 - tx
    tag_f = font(FONT_BOLD, 18)
    d.text((tx, y + 20), story["tag"], font=tag_f, fill=accent)
    head_f = font(FONT_BOLD, 27)
    lines = wrap(d, story["headline"], head_f, tw)
    ly = y + 48
    for line in lines[:3]:
        d.text((tx, ly), line, font=head_f, fill=INK)
        ly += 34
    cap_f = font(FONT_REG, 21)
    cap_lines = wrap(d, story["caption"], cap_f, w - 36)
    cy = y + h - 18 - len(cap_lines[:2]) * 27
    for line in cap_lines[:2]:
        d.text((x + 18, cy), line, font=cap_f, fill=GREY)
        cy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 130], fill=NAVY)
    d.rectangle([0, 130, W, 136], fill=GOLD)
    kick_f = font(FONT_BOLD, 22)
    d.text((36, 22), "THE WORLD IN ONE IMAGE", font=kick_f, fill=GOLD)
    title_f = font(FONT_BOLD, 52)
    d.text((34, 52), "SATURDAY 21 NOVEMBER 2026", font=title_f, fill=WHITE)
    px, py = 14, 150
    pw, ph = 490, 258
    gap = 16
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = px + col * (pw + gap)
        y = py + row * (ph + 12)
        draw_panel(d, x, y, pw, ph, story)
    foot_f = font(FONT_REG, 18)
    sources = "Sources: BBC, Reuters, AP, Al Jazeera, Financial Times, The Guardian."
    d.text((W / 2, 962), sources, font=foot_f, fill=FOOTER_GREY, anchor="ma")
    d.text((W / 2, 988), "Reported 21 November 2026",
           font=foot_f, fill=FOOTER_GREY, anchor="ma")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
