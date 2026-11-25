#!/usr/bin/env python3
"""Draw the front page for Wednesday, 25 November 2026.

Renders a 1024x1024 newspaper front page with Pillow: a masthead
with the date, one lead story in a dark panel, four more stories
on white cards, and a source line under every story. Only the
standard library and Pillow are used, with the system DejaVu fonts.
No network, no randomness, no timestamps: running this script twice
produces byte-identical PNG output.

Usage:  python3 draw.py        # writes entry.png next to this file
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 36

PAPER = (246, 241, 230)
INK = (26, 26, 24)
NAVY = (29, 53, 87)
NAVY_SOFT = (214, 224, 238)
GOLD = (201, 162, 39)
RED = (158, 32, 32)
CARD = (255, 255, 255)
CARD_EDGE = (198, 188, 168)
MUTED = (96, 90, 78)
TEAL = (14, 116, 144)
CRIMSON = (159, 18, 57)
AMBER = (180, 83, 9)
OLIVE = (54, 83, 20)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    out = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
    return out


def clip_lines(draw, text, fnt, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap_text(draw, text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1] + " ..."
    return lines


def put_lines(draw, lines, fnt, x, y, fill, gap):
    """Draw lines of text; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def tower_icon(draw, cx, cy, size, color):
    """A flat skyscraper: tall slab, lit windows, impact burst."""
    w = size // 3
    h = size * 3 // 4
    x0, y0 = cx - w // 2, cy - h // 2
    draw.rectangle([x0, y0, cx + w // 2, cy + h // 2],
                   outline=color, width=4)
    for row in range(4):
        wy = y0 + 12 + row * (h // 5)
        for col in range(2):
            wx = cx - w // 4 + col * (w // 2)
            draw.rectangle([wx - 4, wy - 3, wx + 4, wy + 3], fill=color)
    # burst at the impact point, upper third
    bx, by = cx + w // 2 + 12, cy - h // 6
    for dx, dy in ((-10, -10), (10, -10), (-12, 0), (12, 0),
                   (-10, 10), (10, 10), (0, -12), (0, 12)):
        draw.line([(bx, by), (bx + dx, by + dy)], fill=color, width=3)
    draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=color)


def medal_icon(draw, cx, cy, size, color):
    """A flat medal: ribbon V and a round medallion with a star."""
    draw.line([(cx - size // 4, cy - size // 2),
               (cx, cy - size // 8)], fill=color, width=5)
    draw.line([(cx + size // 4, cy - size // 2),
               (cx, cy - size // 8)], fill=color, width=5)
    r = size // 4
    my = cy + size // 6
    draw.ellipse([cx - r, my - r, cx + r, my + r], outline=color, width=4)
    draw.ellipse([cx - r // 2, my - r // 2, cx + r // 2, my + r // 2],
                 outline=color, width=2)
    draw.regular_polygon((cx, my, r // 2), 5, rotation=90, fill=color)


def seal_icon(draw, cx, cy, size, color):
    """A flat stamped file: page, text lines, round seal."""
    w, h = size // 2, size * 2 // 3
    draw.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
                   outline=color, width=4)
    for frac in (0.28, 0.45, 0.62):
        y = cy - h // 2 + int(h * frac)
        draw.line([(cx - w // 2 + 8, y), (cx + w // 2 - 8, y)],
                  fill=color, width=3)
    r = size // 6
    sx, sy = cx + w // 2 - r, cy + h // 2 - r
    draw.ellipse([sx - r, sy - r, sx + r, sy + r], outline=color, width=3)
    draw.text((sx - 4, sy - 8), "!", font=load(SANS_BOLD, 16), fill=color)


def burst_icon(draw, cx, cy, size, color):
    """A flat blast star: radiating spikes from a centre dot."""
    for i in range(8):
        angle = i * 45
        long = size // 2
        short = size // 4
        import math
        dx = math.cos(math.radians(angle))
        dy = math.sin(math.radians(angle))
        draw.line([(cx + dx * short, cy + dy * short),
                   (cx + dx * long, cy + dy * long)],
                  fill=color, width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)


def chip_icon(draw, cx, cy, size, color):
    """A flat microchip: square body, pins on four sides, inner die."""
    half = size // 2
    pin = size // 10
    body = size // 2
    draw.rounded_rectangle(
        [cx - body // 2, cy - body // 2, cx + body // 2, cy + body // 2],
        radius=6, outline=color, width=4)
    for i in range(3):
        off = -body // 4 + i * body // 4
        draw.line([(cx + off, cy - body // 2 - pin),
                   (cx + off, cy - body // 2)], fill=color, width=4)
        draw.line([(cx + off, cy + body // 2),
                   (cx + off, cy + body // 2 + pin)], fill=color, width=4)
        draw.line([(cx - body // 2 - pin, cy + off),
                   (cx - body // 2, cy + off)], fill=color, width=4)
        draw.line([(cx + body // 2, cy + off),
                   (cx + body // 2 + pin, cy + off)], fill=color, width=4)
    inner = body // 3
    draw.rectangle([cx - inner, cy - inner, cx + inner, cy + inner],
                   outline=color, width=3)


def main():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)

    masthead = load(SERIF_BOLD, 62)
    date_font = load(SANS_BOLD, 25)
    kicker_font = load(SANS_BOLD, 19)
    lead_head = load(SERIF_BOLD, 46)
    lead_deck = load(SERIF, 24)
    head_font = load(SERIF_BOLD, 28)
    deck_font = load(SERIF, 20)
    source_font = load(SANS, 15)
    foot_font = load(SANS, 16)

    # Masthead.
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=masthead)
    draw.text(((SIZE - tw) / 2, 26), title, font=masthead, fill=INK)
    draw.line([(MARGIN, 104), (SIZE - MARGIN, 104)], fill=INK, width=3)
    date_line = "WEDNESDAY,  25 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=date_font)
    draw.text(((SIZE - dw) / 2, 116), date_line, font=date_font, fill=RED)
    draw.line([(MARGIN, 152), (SIZE - MARGIN, 152)], fill=CARD_EDGE, width=1)

    # Lead story: dark panel.
    lead = (MARGIN, 168, SIZE - MARGIN, 424)
    draw.rounded_rectangle(lead, radius=14, fill=NAVY)
    lx, ly = lead[0] + 28, lead[1] + 22
    draw.text((lx, ly), "MIDDLE EAST  \u00b7  SAUDI ARABIA",
              font=kicker_font, fill=GOLD)
    head = clip_lines(draw, "Riyadh tower struck again", lead_head, 700, 1)
    y = put_lines(draw, head, lead_head, lx, ly + 34, (255, 255, 255), 4)
    deck = clip_lines(
        draw,
        "A Houthi strike hits the PIF Tower, Riyadh's tallest "
        "skyscraper, for the second time in a week, wounding 11 "
        "people.",
        lead_deck, 700, 3)
    y = put_lines(draw, deck, lead_deck, lx, y + 8, NAVY_SOFT, 6)
    draw.text((lx, lead[3] - 34),
              "Sources: Reuters, AFP, The Jerusalem Post",
              font=source_font, fill=(176, 192, 212))
    tower_icon(draw, lead[2] - 110, lead[1] + 128, 130, NAVY_SOFT)

    # Four cards in a 2 x 2 grid.
    cards = [
        dict(kicker="CHINA  \u00b7  POLITICS", color=TEAL,
             headline="Shanghai chief probed for graft",
             deck="Chen Jining, Shanghai's party chief and a Politburo "
                  "member, is put under investigation \u2014 the fourth "
                  "since 2025.",
             sources="Sources: Xinhua, Reuters, SCMP",
             icon=seal_icon),
        dict(kicker="UNITED STATES", color=CRIMSON,
             headline="Trump honours Giuliani",
             deck="The president awards the Medal of Freedom, the top "
                  "civilian honour, to Rudy Giuliani in a private "
                  "ceremony.",
             sources="Sources: Reuters, AP, The New York Times",
             icon=medal_icon),
        dict(kicker="MIDDLE EAST  \u00b7  GAZA", color=AMBER,
             headline="Hamas security chief killed",
             deck="An Israeli strike in Gaza City kills Naim Abu Nahal, "
                  "head of Hamas's internal security, as the ceasefire "
                  "frays.",
             sources="Sources: Reuters, Al Jazeera, Times of Israel",
             icon=burst_icon),
        dict(kicker="TECHNOLOGY", color=OLIVE,
             headline="Huang says sorry, in therapy",
             deck="A day after his return, Nvidia's Jensen Huang "
                  "apologises to staff, says he is in therapy and admits "
                  "\u2018terrible mistakes\u2019.",
             sources="Sources: The New York Times, CNN, SCMP",
             icon=chip_icon),
    ]
    gap = 20
    card_w = (SIZE - 2 * MARGIN - gap) // 2
    card_h = 228
    top = 444
    for index, card in enumerate(cards):
        row, col = divmod(index, 2)
        x0 = MARGIN + col * (card_w + gap)
        y0 = top + row * (card_h + gap)
        x1, y1 = x0 + card_w, y0 + card_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                               fill=CARD, outline=CARD_EDGE, width=1)
        px, py = x0 + 22, y0 + 18
        draw.text((px, py), card["kicker"], font=kicker_font,
                  fill=card["color"])
        icon_cx, icon_cy = x1 - 52, y0 + 52
        card["icon"](draw, icon_cx, icon_cy, 64, card["color"])
        head_w = card_w - 44 - 78
        head = clip_lines(draw, card["headline"], head_font, head_w, 2)
        y = put_lines(draw, head, head_font, px, py + 30, INK, 2)
        deck = clip_lines(draw, card["deck"], deck_font, card_w - 44, 3)
        put_lines(draw, deck, deck_font, px, y + 6, (58, 54, 48), 4)
        draw.text((px, y1 - 30), card["sources"], font=source_font,
                  fill=MUTED)

    # Footer.
    draw.line([(MARGIN, 940), (SIZE - MARGIN, 940)], fill=CARD_EDGE, width=1)
    foot = "All five stories happened, or were first reported, on 25 November 2026."
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((SIZE - fw) / 2, 954), foot, font=foot_font, fill=MUTED)

    image.save("entry.png", format="PNG")
    print("wrote entry.png (%dx%d)" % image.size)


if __name__ == "__main__":
    main()
