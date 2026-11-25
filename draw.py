#!/usr/bin/env python3
"""Front page for Wednesday, 25 November 2026, drawn by Pillow.

One 1024x1024 newspaper page: masthead and date, a dark lead
panel, four story cards in a grid, a source line under each story,
and a footer. Pillow plus the standard library only, DejaVu fonts
from the system. Deterministic: no network, no clock, no random
numbers, so two runs produce byte-identical PNG output.

Run:  python3 draw.py    # writes entry.png beside this file
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAD = 36

BG = (246, 241, 230)
FG = (26, 26, 24)
NAVY = (29, 53, 87)
PALE = (214, 224, 238)
GILT = (201, 162, 39)
RUST = (158, 32, 32)
CARD = (255, 255, 255)
EDGE = (198, 188, 168)
GREY = (96, 90, 78)
BODY = (58, 54, 48)
TEAL = (14, 116, 144)
WINE = (159, 18, 57)
OCHRE = (180, 83, 9)
LEAF = (54, 83, 20)

FONTDIR = "/usr/share/fonts/truetype/dejavu"
SERIF = FONTDIR + "/DejaVuSerif.ttf"
SERIFB = FONTDIR + "/DejaVuSerif-Bold.ttf"
SANS = FONTDIR + "/DejaVuSans.ttf"
SANSB = FONTDIR + "/DejaVuSans-Bold.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, fnt, width, limit):
    """Wrap text to width, keeping at most limit lines (ellipsis if cut)."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        nxt = word if cur == "" else cur + " " + word
        if d.textlength(nxt, font=fnt) <= width:
            cur = nxt
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > limit:
        lines = lines[:limit]
        while d.textlength(lines[-1] + " ...", font=fnt) > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " ..."
    return lines


def block(d, lines, fnt, x, y, color, leading):
    """Draw stacked lines; return the y below the last one."""
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += fnt.size + leading
    return y


def icon_tower(d, cx, cy, s, color):
    """Skyscraper slab with lit windows and a burst at the top."""
    w, h = s // 3, s * 3 // 4
    d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
                outline=color, width=4)
    for row in range(4):
        wy = cy - h // 2 + 14 + row * (h // 5)
        d.rectangle([cx - w // 4 - 4, wy - 3, cx - w // 4 + 4, wy + 3],
                    fill=color)
        d.rectangle([cx + w // 4 - 4, wy - 3, cx + w // 4 + 4, wy + 3],
                    fill=color)
    bx, by = cx + w // 2 + 12, cy - h // 6
    for dx, dy in ((-9, -9), (9, -9), (-11, 0), (11, 0),
                   (-9, 9), (9, 9), (0, -11), (0, 11)):
        d.line([(bx, by), (bx + dx, by + dy)], fill=color, width=3)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=color)


def icon_medal(d, cx, cy, s, color):
    """Medal on a ribbon: V straps and a ringed disc with a star."""
    d.line([(cx - s // 4, cy - s // 2), (cx, cy - s // 8)],
           fill=color, width=5)
    d.line([(cx + s // 4, cy - s // 2), (cx, cy - s // 8)],
           fill=color, width=5)
    r, my = s // 4, cy + s // 6
    d.ellipse([cx - r, my - r, cx + r, my + r], outline=color, width=4)
    d.ellipse([cx - r // 2, my - r // 2, cx + r // 2, my + r // 2],
              outline=color, width=2)
    d.regular_polygon((cx, my, r // 2), 5, rotation=90, fill=color)


def icon_seal(d, cx, cy, s, color):
    """Stamped file: page with rulings and a round seal at the corner."""
    w, h = s // 2, s * 2 // 3
    d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
                outline=color, width=4)
    for frac in (0.28, 0.45, 0.62):
        yy = cy - h // 2 + int(h * frac)
        d.line([(cx - w // 2 + 8, yy), (cx + w // 2 - 8, yy)],
               fill=color, width=3)
    r = s // 6
    sx, sy = cx + w // 2 - r, cy + h // 2 - r
    d.ellipse([sx - r, sy - r, sx + r, sy + r], outline=color, width=3)
    d.ellipse([sx - r // 2, sy - r // 2, sx + r // 2, sy + r // 2],
              fill=color)


def icon_burst(d, cx, cy, s, color):
    """Blast star: eight spikes around a centre dot."""
    import math
    for i in range(8):
        ang = math.radians(i * 45)
        dx, dy = math.cos(ang), math.sin(ang)
        d.line([(cx + dx * s // 4, cy + dy * s // 4),
                (cx + dx * s // 2, cy + dy * s // 2)],
               fill=color, width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)


def icon_chip(d, cx, cy, s, color):
    """Microchip: square body, pins on four sides, inner die."""
    half = s // 2
    pin = s // 10
    body = s // 2
    d.rounded_rectangle(
        [cx - body // 2, cy - body // 2, cx + body // 2, cy + body // 2],
        radius=6, outline=color, width=4)
    for i in range(3):
        off = -body // 4 + i * body // 4
        d.line([(cx + off, cy - body // 2 - pin),
                (cx + off, cy - body // 2)], fill=color, width=4)
        d.line([(cx + off, cy + body // 2),
                (cx + off, cy + body // 2 + pin)], fill=color, width=4)
        d.line([(cx - body // 2 - pin, cy + off),
                (cx - body // 2, cy + off)], fill=color, width=4)
        d.line([(cx + body // 2, cy + off),
                (cx + body // 2 + pin, cy + off)], fill=color, width=4)
    inner = body // 3
    d.rectangle([cx - inner, cy - inner, cx + inner, cy + inner],
                outline=color, width=3)


LEAD = {
    "kicker": "MIDDLE EAST  \u00b7  SAUDI ARABIA",
    "head": "Riyadh tower struck again",
    "deck": ("A Houthi strike hits the PIF Tower, Riyadh's tallest "
             "skyscraper, for the second time in a week, wounding 11 "
             "people."),
    "sources": "Sources: Reuters, AFP, The Jerusalem Post",
    "icon": icon_tower,
}

CARDS = [
    {
        "kicker": "CHINA  \u00b7  POLITICS",
        "color": TEAL,
        "head": "Shanghai chief probed for graft",
        "deck": ("Chen Jining, Shanghai's party chief and a Politburo "
                 "member, is put under investigation \u2014 the fourth "
                 "since 2025."),
        "sources": "Sources: Xinhua, Reuters, SCMP",
        "icon": icon_seal,
    },
    {
        "kicker": "UNITED STATES",
        "color": WINE,
        "head": "Trump honours Giuliani",
        "deck": ("The president awards the Medal of Freedom, the top "
                 "civilian honour, to Rudy Giuliani in a private "
                 "ceremony."),
        "sources": "Sources: Reuters, AP, The New York Times",
        "icon": icon_medal,
    },
    {
        "kicker": "MIDDLE EAST  \u00b7  GAZA",
        "color": OCHRE,
        "head": "Hamas security chief killed",
        "deck": ("An Israeli strike in Gaza City kills Naim Abu Nahal, "
                 "head of Hamas's internal security, as the ceasefire "
                 "frays."),
        "sources": "Sources: Reuters, Al Jazeera, Times of Israel",
        "icon": icon_burst,
    },
    {
        "kicker": "TECHNOLOGY",
        "color": LEAF,
        "head": "Huang says sorry, in therapy",
        "deck": ("A day after his return, Nvidia's Jensen Huang "
                 "apologises to staff, says he is in therapy and admits "
                 "\u2018terrible mistakes\u2019."),
        "sources": "Sources: The New York Times, CNN, SCMP",
        "icon": icon_chip,
    },
]


def page():
    img = Image.new("RGB", (W, W), BG)
    d = ImageDraw.Draw(img)

    mast = face(SERIFB, 62)
    datef = face(SANSB, 25)
    kickf = face(SANSB, 19)
    leadh = face(SERIFB, 46)
    leadd = face(SERIF, 24)
    headf = face(SERIFB, 28)
    deckf = face(SERIF, 20)
    srcf = face(SANS, 15)
    footf = face(SANS, 16)

    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 26), title, font=mast, fill=FG)
    d.line([(PAD, 104), (W - PAD, 104)], fill=FG, width=3)
    dateline = "WEDNESDAY,  25 NOVEMBER 2026"
    dw = d.textlength(dateline, font=datef)
    d.text(((W - dw) / 2, 116), dateline, font=datef, fill=RUST)
    d.line([(PAD, 152), (W - PAD, 152)], fill=EDGE, width=1)

    # Lead story on a dark panel.
    x0, y0, x1, y1 = PAD, 168, W - PAD, 424
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=NAVY)
    lx, ly = x0 + 28, y0 + 22
    d.text((lx, ly), LEAD["kicker"], font=kickf, fill=GILT)
    y = block(d, fit(d, LEAD["head"], leadh, 700, 1), leadh,
              lx, ly + 34, (255, 255, 255), 4)
    y = block(d, fit(d, LEAD["deck"], leadd, 700, 3), leadd,
              lx, y + 8, PALE, 6)
    d.text((lx, y1 - 34), LEAD["sources"], font=srcf, fill=(176, 192, 212))
    LEAD["icon"](d, x1 - 116, y0 + 132, 148, PALE)

    # Four cards, two by two.
    gap = 20
    cw = (W - 2 * PAD - gap) // 2
    ch = 228
    top = 444
    for n, card in enumerate(CARDS):
        row, col = divmod(n, 2)
        cx0 = PAD + col * (cw + gap)
        cy0 = top + row * (ch + gap)
        cx1, cy1 = cx0 + cw, cy0 + ch
        d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=10,
                            fill=CARD, outline=EDGE, width=1)
        px, py = cx0 + 22, cy0 + 18
        d.text((px, py), card["kicker"], font=kickf, fill=card["color"])
        card["icon"](d, cx1 - 52, cy0 + 52, 72, card["color"])
        y = block(d, fit(d, card["head"], headf, cw - 44 - 78, 2), headf,
                  px, py + 30, FG, 2)
        block(d, fit(d, card["deck"], deckf, cw - 44, 3), deckf,
              px, y + 6, BODY, 4)
        d.text((px, cy1 - 30), card["sources"], font=srcf, fill=GREY)

    # Footer.
    d.line([(PAD, 940), (W - PAD, 940)], fill=EDGE, width=1)
    foot = ("All five stories happened, or were first reported, "
            "on 25 November 2026.")
    fw = d.textlength(foot, font=footf)
    d.text(((W - fw) / 2, 954), foot, font=footf, fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png (%dx%d)" % img.size)


if __name__ == "__main__":
    page()
