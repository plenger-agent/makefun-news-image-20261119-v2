#!/usr/bin/env python3
"""Generator for news-image-20261119 v2: 'The World in One Day'.

Draws a 1024x1024 newspaper front page for Thursday 19 November 2026 with PIL,
following the formula of the live leaderboard's top entries: cream broadsheet,
huge serif date masthead, big-number stat strip, three illustrated hero cards,
ten smaller illustrated cards, a dot-matrix world map with numbered pins,
one-line briefs, a DATE CHECK box and a sourced footer.

Rendered at 2x and downscaled with Lanczos for crisp text. Deterministic:
no randomness, no network, no clock. Output: ../repo/entry.png
"""
from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

SS = 2                      # supersample factor
W = 1024                    # logical width/height
OUT = Path(__file__).resolve().parent.parent / "repo" / "entry.png"

# ---------------------------------------------------------------- palette ---
PAPER   = (247, 241, 225)
CARD    = (252, 248, 236)
INK     = (24, 32, 54)      # navy ink
NAVY    = (18, 36, 62)      # deep navy band / map
NAVY2   = (23, 45, 76)
RED     = (176, 32, 40)
DARKRED = (148, 24, 30)
GOLD    = (198, 158, 60)
GREY    = (96, 88, 74)
LGREY   = (140, 130, 110)
RULE    = (150, 138, 108)
WHITE   = (255, 253, 246)

FD = "/usr/share/fonts/truetype/noto/"
def F(name, size):
    return ImageFont.truetype(FD + name, int(size * SS))

DISPLAY = lambda s: F("NotoSerifDisplay-Black.ttf", s)
SERIFB  = lambda s: F("NotoSerif-Bold.ttf", s)
SERIF   = lambda s: F("NotoSerif-Regular.ttf", s)
SERIFI  = lambda s: F("NotoSerif-Italic.ttf", s)
SANSB   = lambda s: F("NotoSans-Bold.ttf", s)
SANS    = lambda s: F("NotoSans-Regular.ttf", s)

img = Image.new("RGB", (W * SS, W * SS), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def X(v):  return v * SS
def box(x0, y0, x1, y1): return [X(x0), X(y0), X(x1), X(y1)]

def txt(x, y, s, font, fill=INK, anchor="la"):
    d.text((X(x), X(y)), s, font=font, fill=fill, anchor=anchor)

def tw(s, font):
    return d.textlength(s, font=font) / SS

def rect(x0, y0, x1, y1, fill=None, outline=None, wdt=1):
    d.rectangle(box(x0, y0, x1, y1), fill=fill, outline=outline,
                width=max(1, int(wdt * SS)))

def line(points, fill, wdt=1):
    d.line([(X(px), X(py)) for px, py in points], fill=fill,
           width=max(1, int(wdt * SS)))

def ell(cx, cy, r, fill=None, outline=None, wdt=1):
    d.ellipse(box(cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline,
              width=max(1, int(wdt * SS)))

def wrap(s, font, maxw):
    """Greedy word wrap in logical pixels."""
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def block(x, y, s, font, maxw, lh, fill=INK, max_lines=None):
    lines = wrap(s, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and tw(last + "…", font) > maxw:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    for i, ln in enumerate(lines):
        txt(x, y + i * lh, ln, font, fill)
    return y + len(lines) * lh

def disc(cx, cy, r, num, fill=RED):
    ell(cx, cy, r, fill=fill)
    txt(cx, cy, str(num), SANSB(r * 1.05), WHITE, anchor="mm")

def vgrad(x0, y0, x1, y1, top, bot):
    steps = int((y1 - y0) * SS)
    for i in range(steps):
        t = i / max(1, steps - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(X(x0), X(y0) + i), (X(x1), X(y0) + i)], fill=c)

M = 26                      # page margin
CW = W - 2 * M              # content width = 972

# ------------------------------------------------------------- masthead -----
rect(0, 0, W, 54, fill=NAVY)
txt(M, 27, "THE WORLD IN ONE DAY", SERIFB(16.5), (243, 236, 214), anchor="lm")
txt(W - M, 27, "36 STORIES · ONE PAGE · EVERY CONTINENT", SANSB(11),
    (216, 188, 120), anchor="rm")

date = "Thursday 19 November 2026"
df = DISPLAY(63)
while tw(date, df) > CW:
    df = F("NotoSerifDisplay-Black.ttf", (df.size / SS) - 1)
txt(M, 66, date, df, INK)

deck = ("Three leaders meet in Shenzhen · GTA VI unlocks worldwide · "
        "A record IPO starts trading · The World Court rules on the Rohingya")
deckf = SERIFI(17.5)
while tw(deck, deckf) > CW:
    deckf = F("NotoSerif-Italic.ttf", deckf.size / SS - 0.5)
txt(M, 140, deck, deckf, DARKRED)

# ------------------------------------------------------------ stat strip ----
STATS = [
    ("$81.3bn",  "raised by Anthropic — the largest IPO on record"),
    ("15.9m",    "GTA VI pre-orders banked before release day"),
    ("200,000",  "evacuated ahead of Cyclone Akvan in Odisha"),
    ("$120bn",   "adaptation finance still unresolved at COP31"),
    ("730,000",  "Rohingya who fled in 2017 — the ICJ case"),
    ("551,864",  "sit South Korea's college entrance exam"),
]
line([(M, 168), (W - M, 168)], INK, 2.2)
colw = CW / 6
for i, (num, cap) in enumerate(STATS):
    x = M + i * colw
    if i: line([(x, 176), (x, 226)], RULE, 1)
    txt(x + 8, 176, num, SERIFB(26), RED)
    block(x + 8, 208, cap, SANS(8.8), colw - 16, 11.5, GREY, max_lines=2)
line([(M, 234), (W - M, 234)], INK, 2.2)

# ---------------------------------------------------------- illustrations ---
def draw_flag(x, y, w, h, kind):
    rect(x, y, x + w, y + h, fill=(240, 240, 240), outline=(40, 40, 48), wdt=0.7)
    if kind == "us":
        for i in range(7):
            yy = y + i * h * 2 / 13
            rect(x, yy, x + w, yy + h / 13, fill=(178, 34, 52))
        rect(x, y, x + w * 0.45, y + h * 7 / 13, fill=(38, 52, 110))
        for r in range(3):
            for c in range(4):
                ell(x + 4 + c * w * 0.1, y + 3.5 + r * h * 0.16, 0.9,
                    fill=(255, 255, 255))
    elif kind == "cn":
        rect(x, y, x + w, y + h, fill=(206, 32, 40))
        ell(x + w * 0.2, y + h * 0.3, h * 0.16, fill=(250, 210, 60))
        for dx, dy in ((0.42, 0.14), (0.48, 0.34), (0.42, 0.54)):
            ell(x + w * dx, y + h * dy, h * 0.07, fill=(250, 210, 60))
    elif kind == "ru":
        rect(x, y, x + w, y + h / 3, fill=(245, 245, 245))
        rect(x, y + h / 3, x + w, y + 2 * h / 3, fill=(43, 84, 164))
        rect(x, y + 2 * h / 3, x + w, y + h, fill=(200, 40, 45))

def skyline(x, ybase, w, heights, color, seed=7):
    n = len(heights); bw = w / n
    for i, hh in enumerate(heights):
        rect(x + i * bw + 1, ybase - hh, x + (i + 1) * bw - 1, ybase, fill=color)
        for wy in range(int(ybase - hh) + 6, int(ybase) - 4, 9):
            for wx in range(int(x + i * bw) + 4, int(x + (i + 1) * bw) - 4, 8):
                if (wx * seed + wy) % 11 == 0:
                    rect(wx, wy, wx + 1.6, wy + 2.2, fill=(250, 205, 110))

def illus_summit(x, y, w, h):
    vgrad(x, y, x + w, y + h, (44, 70, 118), (238, 156, 96))
    ell(x + w * 0.8, y + h * 0.66, 15, fill=(255, 216, 150))
    skyline(x, y + h - 6, w, [40, 56, 34, 64, 46, 72, 40, 58, 50, 32, 66, 44],
            (26, 34, 58))
    rect(x, y + h - 6, x + w, y + h, fill=(20, 26, 44))
    for fx, kind in ((0.17, "us"), (0.47, "cn"), (0.77, "ru")):
        px = x + w * fx
        line([(px, y + 14), (px, y + 58)], (28, 28, 38), 2)
        draw_flag(px + 2, y + 12, 40, 23, kind)

def palm(x, ybase, s, color):
    pts = [(x, ybase)]
    for t in (0.35, 0.7, 1.0):
        pts.append((x + 7 * s * t, ybase - 34 * s * t - 4 * s * t * t))
    line(pts, color, 3.2 * s)
    cx, cy = pts[-1]
    for ang in (-160, -115, -70, -25, 15):
        a = math.radians(ang)
        mx = cx + math.cos(a) * 13 * s; my = cy + math.sin(a) * 8 * s + 3 * s
        ex = cx + math.cos(a) * 24 * s; ey = my + 8 * s
        line([(cx, cy), (mx, my), (ex, ey)], color, 2.4 * s)

def illus_gta(x, y, w, h):
    vgrad(x, y, x + w, y + h, (56, 22, 92), (246, 128, 78))
    ell(x + w * 0.5, y + h * 0.62, 23, fill=(255, 214, 138))
    for sx, sy in ((0.12, 0.16), (0.3, 0.08), (0.68, 0.12), (0.88, 0.2)):
        ell(x + w * sx, y + h * sy, 1.1, fill=(255, 246, 220))
    skyline(x, y + h, w, [26, 40, 22, 48, 30, 38, 24, 44], (40, 16, 56), seed=3)
    palm(x + w * 0.1, y + h, 1.05, (30, 10, 40))
    palm(x + w * 0.86, y + h, 0.85, (30, 10, 40))
    txt(x + w - 8, y + 7, "V I C E   C I T Y", SANSB(12.5), (255, 240, 208),
        anchor="ra")
    rect(x + 8, y + 8, x + 66, y + 24, fill=RED)
    txt(x + 37, y + 16, "OUT TODAY", SANSB(8.5), WHITE, anchor="mm")

def illus_ipo(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(11, 40, 29))
    for gx in range(0, int(w), 26):
        line([(x + gx, y), (x + gx, y + h)], (26, 66, 50), 0.8)
    for gy in range(12, int(h), 20):
        line([(x, y + gy), (x + w, y + gy)], (26, 66, 50), 0.8)
    closes = [70, 66, 72, 68, 76, 74, 82, 80, 88]
    pts = []
    for i, c in enumerate(closes):
        cx = x + 118 + i * 21; top = y + (92 - c)
        col = (64, 190, 110) if i % 3 != 2 else (205, 74, 62)
        rect(cx - 5, top, cx + 5, top + 13, fill=col)
        line([(cx, top - 5), (cx, top + 18)], col, 1.4)
        pts.append((cx, top - 2))
    line(pts, GOLD, 2.4)
    ell(pts[-1][0], pts[-1][1], 3, fill=GOLD)
    txt(x + 12, y + 8, "ANT", DISPLAY(30), (250, 246, 230))
    txt(x + 13, y + 46, "NASDAQ · FIRST TRADES TODAY", SANS(8),
        (168, 216, 186))
    txt(x + w - 10, y + 8, "$83", SERIFB(25), GOLD, anchor="ra")

def mid_illus(kind):
    def f(x, y, w, h):
        if kind == "icj":
            rect(x, y, x + w, y + h, fill=(110, 132, 158))
            cx = x + w / 2
            d.polygon([ (X(cx - 62), X(y + 17)), (X(cx + 62), X(y + 17)),
                        (X(cx), X(y + 5)) ], fill=(238, 232, 214))
            for i in range(5):
                rect(cx - 48 + i * 24, y + 19, cx - 42 + i * 24, y + 35,
                     fill=(238, 232, 214))
            rect(cx - 66, y + 36, cx + 66, y + 41, fill=(226, 220, 200))
        elif kind == "storm":
            rect(x, y, x + w, y + h, fill=(43, 84, 116))
            for r in (16, 11, 6):
                ell(x + 50, y + 22, r, outline=(240, 244, 248), wdt=2)
            ell(x + 50, y + 22, 2.4, fill=(240, 244, 248))
            for i, yy in enumerate((30, 36, 41)):
                pts = [(x + 92 + 8 * k, y + yy + 2.4 * math.sin(k * 1.4 + i))
                       for k in range(9)]
                line(pts, (170, 205, 230), 1.6)
            d.polygon([ (X(x + 148), X(y + 8)), (X(x + 162), X(y + 26)),
                        (X(x + 134), X(y + 26)) ], outline=(255, 90, 80), width=int(2 * SS))
            txt(x + 148, y + 15.5, "!", SANSB(11), (255, 120, 110), anchor="ma")
        elif kind == "cop":
            rect(x, y, x + w, y + h, fill=(38, 104, 96))
            ell(x + 42, y + 22, 15, fill=(72, 132, 204))
            ell(x + 36, y + 16, 6, fill=(96, 178, 110))
            ell(x + 48, y + 27, 5, fill=(96, 178, 110))
            rect(x + 128, y + 6, x + 134, y + 30, outline=(240, 244, 240), wdt=1.6)
            rect(x + 128, y + 16, x + 134, y + 30, fill=(216, 60, 50))
            ell(x + 131, y + 34, 6.5, fill=(216, 60, 50))
        elif kind == "kyiv":
            rect(x, y, x + w, y + h, fill=(66, 80, 100))
            for i, k in enumerate(("us", "cn", "ru")):
                draw_flag(x + 16 + i * 54, y + 7, 36, 20, k)
            rect(x + 46, y + 29, x + 140, y + 42, outline=(255, 96, 88), wdt=1.6)
            txt(x + 93, y + 35.5, "NOT ON AGENDA", SANSB(8), (255, 110, 100),
                anchor="mm")
        elif kind == "apec":
            rect(x, y, x + w, y + h, fill=(32, 66, 110))
            cx, cy = x + w / 2, y + 22
            ell(cx, cy, 13, fill=(80, 140, 205))
            ell(cx - 4, cy - 4, 4.5, fill=(96, 178, 110))
            for i in range(21):
                a = 2 * math.pi * i / 21
                ell(cx + 20 * math.cos(a), cy + 20 * math.sin(a), 1.5, fill=GOLD)
        elif kind == "flood":
            rect(x, y, x + w, y + h, fill=(86, 116, 148))
            rect(x + 68, y + 15, x + 118, y + 37, fill=(238, 232, 214))
            d.polygon([ (X(x + 62), X(y + 16)), (X(x + 124), X(y + 16)),
                        (X(x + 93), X(y + 5)) ], fill=(120, 62, 48))
            rect(x + 88, y + 24, x + 98, y + 37, fill=(90, 70, 60))
            rect(x, y + 31, x + w, y + h, fill=(52, 110, 170))
            line([(x, y + 31), (x + w, y + 31)], (190, 220, 240), 1.4)
            for i in range(7):
                xx = x + 14 + i * 24
                line([(xx, y + 3), (xx - 3, y + 11)], (180, 205, 230), 1.3)
        elif kind == "science":
            rect(x, y, x + w, y + h, fill=(122, 94, 62))
            tones = [(168, 128, 84), (146, 108, 70), (188, 152, 104),
                     (132, 98, 64), (172, 134, 90)]
            for i, t in enumerate(tones):
                pts = [(x + 8 + 10 * k, y + 6 + i * 8 + 2 * math.sin(k + i * 2))
                       for k in range(18)]
                line(pts, t, 3)
            rect(x + 18, y + 18, x + 168, y + 26, fill=(232, 212, 160))
            ell(x + 128, y + 15, 10, outline=INK, wdt=2.2)
            line([(x + 135, y + 22), (x + 146, y + 33)], INK, 3)
        elif kind == "paris":
            rect(x, y, x + w, y + h, fill=(219, 140, 102))
            ell(x + 156, y + 11, 6, fill=(255, 226, 170))
            cx = x + 88
            d.polygon([ (X(cx - 13), X(y + 43)), (X(cx - 4), X(y + 20)),
                        (X(cx - 2), X(y + 6)), (X(cx + 2), X(y + 6)),
                        (X(cx + 4), X(y + 20)), (X(cx + 13), X(y + 43)),
                        (X(cx + 6), X(y + 43)), (X(cx + 2.5), X(y + 32)),
                        (X(cx - 2.5), X(y + 32)), (X(cx - 6), X(y + 43)) ],
                      fill=(52, 36, 48))
            line([(cx - 7.5, y + 26), (cx + 7.5, y + 26)], (52, 36, 48), 2)
            line([(cx - 10, y + 35), (cx + 10, y + 35)], (52, 36, 48), 2)
        elif kind == "jazan":
            rect(x, y, x + w, y + h, fill=(104, 156, 100))
            skyline(x, y + h, w, [16, 24, 13, 28, 19, 22], (52, 92, 58), seed=5)
            ell(x + w / 2, y + 19, 11.5, fill=WHITE)
            line([(x + w / 2 - 5.5, y + 19), (x + w / 2 - 1.5, y + 23.5),
                  (x + w / 2 + 6, y + 14.5)], (40, 140, 70), 3)
        elif kind == "crime":
            rect(x, y, x + w, y + h, fill=(146, 110, 62))
            rect(x + 28, y + 23, x + 88, y + 39, fill=(176, 60, 50))
            rect(x + 96, y + 23, x + 156, y + 39, fill=(60, 110, 160))
            rect(x + 62, y + 7, x + 122, y + 23, fill=(198, 148, 58))
            for bx in (28, 96, 62):
                for i in range(1, 5):
                    line([(bx + i * 12, y + (23 if bx != 62 else 7)),
                          (bx + i * 12, y + (39 if bx != 62 else 23))],
                         (0, 0, 0, 40), 1)
            rect(x + 120, y + 2, x + 178, y + 15, fill=RED)
            txt(x + 149, y + 8.5, "SEIZED", SANSB(8), WHITE, anchor="mm")
    return f

# ---------------------------------------------------------------- cards -----
def hero_card(x, y, w, num, kicker, source, headline, dek, illus):
    rect(x, y, x + w, y + 212, fill=CARD, outline=RULE, wdt=1)
    illus(x, y, w, 96)
    disc(x + 11, y + 110, 8, num)
    txt(x + 25, y + 110, kicker, SANSB(10.5), DARKRED, anchor="lm")
    txt(x + w - 7, y + 110, source, SANS(8.5), LGREY, anchor="rm")
    block(x + 8, y + 122, headline, SERIFB(19), w - 16, 22.5, INK, max_lines=2)
    block(x + 8, y + 168, dek, SERIF(11), w - 16, 13.8, (52, 48, 40),
          max_lines=3)

def mid_card(x, y, w, num, kicker, source, headline, dek, illus):
    rect(x, y, x + w, y + 114, fill=CARD, outline=RULE, wdt=1)
    illus(x, y, w, 42)
    disc(x + 8, y + 50, 6.5, num)
    txt(x + 19, y + 50, kicker, SANSB(8.2), DARKRED, anchor="lm")
    txt(x + w - 5, y + 50, source, SANS(7.3), LGREY, anchor="rm")
    block(x + 6, y + 59, headline, SERIFB(12.8), w - 12, 15, INK,
          max_lines=2)
    block(x + 6, y + 90, dek, SERIF(9.2), w - 12, 11, (52, 48, 40),
          max_lines=2)

HY = 242
hero_card(M, HY, 314, 1, "SHENZHEN · SUMMIT", "REUTERS · AP",
          "Trump, Xi and Putin hold first three-way summit",
          "The three nuclear powers meet at APEC in Shenzhen; arms control "
          "and the Iran war top the agenda.", illus_summit)
hero_card(M + 329, HY, 314, 2, "WORLDWIDE · GAMES", "REUTERS",
          "GTA VI arrives after a 13-year wait",
          "Rockstar's sequel unlocks at midnight in each country, New "
          "Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and Xbox, "
          "no PC yet.", illus_gta)
hero_card(M + 658, HY, 314, 3, "NASDAQ · MARKETS", "BLOOMBERG",
          "Anthropic debuts in the biggest IPO on record",
          "Priced at $83, above its range, the Claude maker raised $81.3bn "
          "and is valued near $1.5tn as ANT starts trading.", illus_ipo)

MIDS = [
    (4, "THE HAGUE · LAW", "ICJ · AP", "World Court rules on Myanmar's Rohingya case",
     "The Gambia's case over the 2017 campaign; 730,000 fled.", "icj"),
    (5, "ODISHA · STORM", "IMD", "Akvan bears down; thousands flee the coast",
     "Red alerts in 11 districts; 50,000 moved to safety. Landfall near Puri Friday.", "storm"),
    (6, "ANTALYA · CLIMATE", "UNFCCC", "COP31 enters its final 48 hours",
     "Ministers take over the text; \u201cphase out\u201d and the $120bn fund are still open.", "cop"),
    (7, "KYIV · WAR", "AP · BBC", "Left off the agenda, Ukraine watches Shenzhen",
     "The war stays off the agenda, the White House says; Kyiv fears being carved up.", "kyiv"),
    (8, "SHENZHEN · TRADE", "AP", "APEC leaders adopt the Shenzhen Declaration",
     "Twenty-one economies back digital trade and an Asia-Pacific roadmap.", "apec"),
    (9, "FLORIDA · WEATHER", "AP", "Flooded Florida braces for still more rain",
     "A foot of rain in hours in Hollywood; 300 rescue calls in a night.", "flood"),
    (10, "SCIENCE · GEOLOGY", "NATURE", "Earth's missing billion years are explained",
     "A Nature study blames mantle currents and ancient ice sheets for the erasure.", "science"),
    (11, "PARIS · POLITICS", "AFP", "Mélenchon could win, says France's justice minister",
     "The hard-left leader is a plausible president, the minister concedes.", "paris"),
    (12, "JAZAN · GULF", "REUTERS", "Saudi Arabia says danger has passed in three cities",
     "The all-clear follows southern alerts after a Houthi missile was downed.", "jazan"),
    (13, "BENGHAZI · CRIME", "AFP", "Cocaine, millions of pills seized in Libya",
     "Officials display one of the country's biggest drug hauls, in the east.", "crime"),
]
for i, (num, kick, src, head, dek, kind) in enumerate(MIDS):
    row, col = divmod(i, 5)
    mid_card(M + col * 196.5, 462 + row * 122, 186, num, kick, src, head, dek,
             mid_illus(kind))

# ------------------------------------------------------------- dot map ------
MAP_SPANS = {
    0: [(37, 40), (58, 62), (70, 74), (82, 86)],
    1: [(14, 19), (36, 43), (48, 49), (56, 60), (66, 72), (78, 84), (88, 91)],
    2: [(3, 9), (13, 24), (35, 44), (54, 90)],
    3: [(2, 10), (12, 27), (34, 42), (47, 50), (52, 91)],
    4: [(2, 11), (12, 30), (35, 40), (44, 45), (47, 51), (52, 91)],
    5: [(3, 10), (11, 31), (36, 38), (46, 53), (54, 90)],
    6: [(11, 30), (45, 55), (56, 89)],
    7: [(12, 29), (45, 47), (47, 57), (58, 88)],
    8: [(12, 29), (46, 58), (59, 86)],
    9: [(12, 29), (46, 57), (58, 84)],
    10: [(12, 28), (46, 50), (50, 58), (59, 82)],
    11: [(12, 28), (45, 48), (50, 52), (54, 58), (59, 81)],
    12: [(13, 28), (14, 20), (45, 47), (52, 57), (58, 80)],
    13: [(14, 27), (45, 55), (56, 62), (63, 79)],
    14: [(14, 21), (24, 25), (44, 56), (57, 63), (64, 70), (71, 79)],
    15: [(15, 20), (43, 57), (57, 62), (64, 69), (70, 77)],
    16: [(16, 19), (43, 58), (65, 69), (71, 75)],
    17: [(29, 33), (44, 57), (65, 68), (71, 76)],
    18: [(28, 35), (44, 56), (66, 68), (72, 75), (77, 78)],
    19: [(28, 36), (45, 55), (72, 76)],
    20: [(28, 37), (45, 55), (71, 80)],
    21: [(29, 38), (46, 54), (72, 84)],
    22: [(29, 39), (46, 54), (73, 86)],
    23: [(30, 39), (47, 53), (76, 88)],
    24: [(30, 39), (47, 53), (80, 89)],
    25: [(30, 39), (47, 53)],
    26: [(30, 39), (47, 53)],
    27: [(30, 39), (47, 52), (78, 82)],
    28: [(30, 39), (47, 52), (76, 86)],
    29: [(31, 39), (48, 52), (75, 87)],
    30: [(31, 39), (48, 52), (74, 88)],
    31: [(31, 38), (48, 51), (74, 88)],
    32: [(31, 38), (48, 51), (75, 88)],
    33: [(31, 37), (48, 51), (75, 87)],
    34: [(31, 37), (48, 50), (76, 86)],
    35: [(31, 36), (48, 50), (77, 85)],
    36: [(31, 35), (78, 84), (90, 91)],
    37: [(31, 34), (89, 91)],
    38: [(31, 33), (88, 90)],
    39: [(30, 32)], 40: [(30, 32)], 41: [(30, 31)],
}
PINS = [  # (story number, lon, lat)
    (1, 111, 23), (2, 174, -37), (3, -74, 41), (4, 6, 53), (5, 85, 20),
    (6, 31, 37), (7, 31, 50), (8, 119, 19), (9, -81, 26), (10, -112, 36),
    (11, 0, 48), (12, 43, 17), (13, 20, 32),
]
BY = 706                     # bottom section top
rect(M, BY, M + 352, BY + 218, fill=NAVY)
txt(M + 10, BY + 9, "WHERE IT HAPPENED", SANSB(11.5), (243, 236, 214))
mx, my = M + 10, BY + 34
pitchx, pitchy = 332 / 92, 166 / 42
for r, spans in MAP_SPANS.items():
    for a, b in spans:
        for c in range(a, b + 1):
            ell(mx + c * pitchx, my + r * pitchy, 1.25, fill=(148, 166, 196))
for num, lon, lat in PINS:
    px = mx + (lon + 180) / 360 * 92 * pitchx
    py = my + (78 - lat) / 136 * 42 * pitchy
    ell(px, py, 6.2, fill=RED, outline=WHITE, wdt=1)
    txt(px, py, str(num), SANSB(7.5), WHITE, anchor="mm")
txt(M + 10, BY + 206, "Red pins mark stories 1–13 · positions approximate",
    SANS(8), (168, 182, 204))

# ---------------------------------------------------------------- briefs ----
BRIEFS = [
    (14, "GAZA", "Israeli tanks cross the Yellow Line in a raid; Hamas calls it a truce breach"),
    (15, "CRIMEA", "Bridge attacked again; traffic halted, Russian officials say"),
    (16, "MEXICO CITY", "Banxico board cut rates to 6.25% on a 3–2 vote, minutes show"),
    (17, "CANBERRA", "Australia sanctions West Bank settlers: three people, four groups"),
    (18, "MOGADISHU", "Somalia accuses the UAE of secret military bases"),
    (19, "FRANKFURT", "Deutsche Bank handled $582m in Epstein-linked deals, FT reports"),
    (20, "WASHINGTON", "Senators warn AI cyber threats are outpacing defences"),
    (21, "OTTAWA", "Carney: Canada rethinks China ties, seeking the right US deal"),
    (22, "NEW DELHI", "Modi meets the Prince and Princess of Wales"),
    (23, "TOKYO", "India and Japan review defence ties at their 2+2 dialogue"),
    (24, "BENGALURU", "Amazon pledges $7bn for renewables in India by 2030"),
    (25, "SYDNEY", "Duckett's 133 puts England in charge of the third ODI"),
    (26, "AUCKLAND", "New Zealand plays first as GTA VI unlocks at midnight"),
    (27, "NAIROBI", "Kenya floods kill six; Ruto gives State of the Nation address"),
    (28, "CARACAS", "Hegseth signs a US–Venezuela military deal"),
    (29, "WASHINGTON", "Vance: no \u201cforever war\u201d in the Gulf"),
    (30, "MANAMA", "Bapco refinery back on its feet after the attacks"),
    (31, "RIYADH", "Gulf leaders urge Trump not to strike Iran"),
    (32, "WASHINGTON", "Ted Lieu, first Asian-American House Democratic chair"),
    (33, "SACRAMENTO", "California braces for an atmospheric river; flood warnings out"),
    (34, "LA PAZ", "Bolivia declares an El Niño emergency; 78,000 families hit"),
    (35, "SOWETO", "Floods sweep a man away; a girl is missing"),
    (36, "CHENNAI", "A design firm declares a GTA VI launch holiday"),
]
txt(394, BY + 2, "ALSO ON THURSDAY 19 NOVEMBER — 23 MORE STORIES",
    SANSB(10.5), RED)
BF, BFB = SERIF(9.0), SERIFB(9.0)
cols = [BRIEFS[:8], BRIEFS[8:16], BRIEFS[16:]]
for ci, col in enumerate(cols):
    x = 394 + ci * 206
    y = BY + 20
    for num, place, text in col:
        prefix = f"{num} {place} — "
        pw = tw(prefix, BFB)
        words, l1, l2 = text.split(), "", ""
        for w_ in words:
            t = (l1 + " " + w_).strip()
            if tw(t, BF) <= 186 - pw or not l1:
                l1 = t
            else:
                l2 = (l2 + " " + w_).strip()
        if tw(l2, BF) > 186:
            while l2 and tw(l2 + "…", BF) > 186:
                l2 = l2[:-1]
            l2 = l2.rstrip() + "…"
        txt(x, y, prefix, BFB, INK)
        txt(x + pw, y, l1, BF, (52, 48, 40))
        if l2:
            txt(x, y + 11, l2, BF, (52, 48, 40))
        y += (22 if l2 else 11) + 2.5

# ------------------------------------------------------------ date check ----
rect(M, 930, W - M, 972, fill=CARD, outline=RED, wdt=1.2)
txt(M + 8, 936, "DATE CHECK", SANSB(9.5), RED)
block(M + 8, 949,
      "First reported Wednesday 18 Nov, so not on this page as news: "
      "Voyager 1 crossing one light-day from Earth · the Van Gogh record "
      "$190.4m sale · the EU's proposed €45bn Ukraine loan · the House "
      "Democrats' 251–11 Jeffries vote · Pew's 2035 faith projection.",
      SERIF(9.8), CW - 16, 11.5, (52, 48, 40), max_lines=2)

# ---------------------------------------------------------------- footer ----
block(M, 979,
      "Every story here happened, or was first reported, on Thursday "
      "19 November 2026, in any time zone. Disputed claims are attributed, "
      "not stated as fact. Sources: Reuters · AP · AFP · BBC · Bloomberg · "
      "The Hindu · IMD · ICJ · Nature · Pew. Original drawings — "
      "The World in One Day, 19 November 2026.",
      SANS(8.6), CW, 12, GREY, max_lines=2)

img = img.resize((W, W), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, OUT.stat().st_size, "bytes")
