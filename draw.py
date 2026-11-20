#!/usr/bin/env python3
"""Draw entry.png for news-image-20261119, agent 3, 2/3 ("The Ledger").

Flat-vector front page, 1024x1024, drawn entirely in code with PIL + DejaVu.
Deterministic: no timestamps, no randomness, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 220)
PAPER = (250, 244, 228)
INK = (26, 26, 26)
BRICK = (176, 58, 46)
NAVY = (31, 56, 100)
GOLD = (201, 162, 39)
GOLD_D = (168, 130, 24)
GREY = (90, 86, 76)
LIGHT_LINE = (200, 190, 165)
SKIN = (242, 200, 155)
SKIN2 = (232, 184, 138)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSC_B = lambda s: F("DejaVuSansCondensed-Bold.ttf", s)
SANSC = lambda s: F("DejaVuSansCondensed.ttf", s)


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text(d, xy, text, font, fill=INK, anchor="la"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor)


def fit_lines(d, x, y, lines, font, fill, leading, max_w=None):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def num_badge(d, cx, cy, n, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRICK, outline=INK, width=1)
    f = SANS_B(13 if len(str(n)) < 2 else 11)
    d.text((cx, cy), str(n), font=f, fill=(255, 255, 255), anchor="mm")


def kicker(d, x, y, place, topic, font=None):
    font = font or SANS_B(11)
    d.text((x, y), place, font=font, fill=BRICK)
    w = font.getlength(place + " ")
    d.text((x + w, y), "· " + topic, font=font, fill=INK)


# ---------------------------------------------------------------- world map
# Rough continent polygons in (lon, lat). Pins use the same projection, so a
# pin computed from lon/lat always lands on the polygon that covers it.
NA = [(-168, 66), (-160, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
      (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
      (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-79, 9),
      (-81, 13), (-87, 15), (-91, 16), (-92, 15), (-97, 16), (-97, 21),
      (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
      (-76, 35), (-74, 40), (-70, 42), (-66, 45), (-60, 47), (-65, 50),
      (-60, 52), (-64, 58), (-68, 58), (-72, 62), (-78, 62), (-80, 66),
      (-85, 66), (-90, 69), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
      (-155, 71), (-165, 68), (-168, 66)]
SA = [(-79, 9), (-77, 7), (-77, 4), (-80, -3), (-81, -5), (-77, -12),
      (-75, -15), (-70, -18), (-70, -23), (-70, -30), (-71, -33), (-73, -37),
      (-73, -44), (-74, -50), (-68, -52), (-66, -55), (-65, -50), (-62, -45),
      (-58, -40), (-57, -34), (-52, -32), (-48, -28), (-41, -23), (-39, -15),
      (-35, -8), (-35, -6), (-40, -3), (-43, -2), (-50, 0), (-52, 4),
      (-58, 6), (-62, 9), (-66, 10), (-71, 11), (-75, 10), (-79, 9)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 12),
          (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, -1),
          (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34),
          (26, -34), (32, -28), (35, -24), (40, -16), (40, -10), (42, -4),
          (46, 0), (51, 2), (51, 11), (48, 11), (44, 11), (40, 15), (38, 18),
          (37, 22), (34, 27), (32, 31), (30, 32), (25, 32), (20, 32),
          (15, 32), (11, 34), (10, 37), (5, 37), (-1, 35), (-6, 35)]
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (0, 51),
           (3, 53), (7, 54), (8, 57), (10, 59), (6, 60), (5, 62), (8, 64),
           (12, 66), (16, 69), (22, 70), (28, 71), (32, 70), (38, 68),
           (44, 68), (50, 69), (56, 68), (62, 69), (68, 72), (72, 73),
           (78, 73), (85, 75), (92, 75), (100, 77), (108, 76), (115, 73),
           (122, 73), (128, 71), (135, 71), (142, 72), (150, 70), (158, 70),
           (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 60),
           (158, 52), (156, 51), (150, 59), (142, 59), (141, 52), (140, 47),
           (138, 45), (135, 43), (132, 42), (130, 42), (127, 40), (126, 38),
           (122, 38), (120, 34), (119, 30), (121, 28), (118, 25), (113, 21),
           (110, 20), (108, 18), (106, 10), (104, 9), (101, 7), (99, 9),
           (98, 12), (97, 16), (94, 17), (91, 22), (89, 22), (86, 20),
           (84, 18), (82, 16), (80, 13), (78, 8), (76, 10), (74, 14),
           (72, 20), (70, 21), (67, 24), (64, 25), (61, 25), (58, 26),
           (56, 24), (55, 20), (54, 17), (51, 15), (48, 14), (45, 13),
           (43, 12), (41, 14), (39, 17), (38, 20), (37, 23), (35, 27),
           (34, 29), (33, 31), (35, 33), (36, 36), (33, 36), (30, 36),
           (27, 37), (26, 38), (23, 36), (22, 37), (21, 38), (19, 40),
           (16, 40), (14, 38), (12, 44), (10, 44), (8, 44), (6, 43),
           (3, 43), (0, 39), (-1, 37), (-5, 36), (-9, 37)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-25, 70),
             (-20, 70), (-22, 74), (-30, 76), (-45, 76), (-58, 74), (-60, 70),
             (-58, 64)]
AUSTRALIA = [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20), (114, -21), (113, -22)]
UK = [(-5.7, 50.0), (-3.5, 50.7), (-1.8, 50.8), (0.5, 51.3), (1.7, 52.6),
      (0.8, 53.5), (-0.5, 53.8), (-2.2, 54.8), (-3.2, 55.8), (-5.0, 56.5),
      (-6.0, 57.5), (-5.2, 58.5), (-3.5, 58.6), (-2.0, 57.7), (-1.0, 57.5),
      (-2.5, 56.0), (-4.0, 55.0), (-5.5, 54.0), (-5.7, 50.0)]
CONTINENTS = [NA, SA, AFRICA, EURASIA, GREENLAND, AUSTRALIA, UK]

# Numbered pins (lon, lat) — stories 1-13. Brief dots (lon, lat) — briefs 14-32.
PINS = {1: (114.1, 22.4), 2: (4.3, 52.0), 3: (30.7, 36.9), 4: (36.4, 45.4),
        5: (46.7, 24.6), 6: (85.8, 20.3), 7: (127.0, 37.5), 8: (-42.0, 72.0),
        9: (-74.0, 40.7), 10: (-0.1, 51.5), 11: (-74.0, 4.6), 12: (36.8, -1.3),
        13: (149.1, -35.3)}
DOTS = [(114.1, 22.4), (127.0, 37.5), (112.7, -7.2), (55.3, 26.0),
        (34.4, 31.4), (36.4, 45.4), (4.3, 50.8), (-0.1, 51.5), (10.5, 47.4),
        (12.5, 41.9), (45.3, 2.0), (32.6, 15.6), (28.2, -25.7), (-15.4, 28.3),
        (-80.2, 26.1), (0.1, 51.5), (174.8, -41.3), (175.0, -21.1),
        (-159.8, -21.2)]


def project(lon, lat, x0, y0, w, h, lat_top=84.0, lat_bot=-58.0):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
    return (x, y)


# Display offsets in pixels for pins that would otherwise collide on the
# small map (2 The Hague and 10 London are ~5px apart at this scale).
# A thin leader line joins the offset circle to its true position.
PIN_OFFSETS = {2: (12, 0)}


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 224, 196),
                outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, x0, y0, w, h) for lon, lat in poly]
        d.polygon(pts, fill=(214, 196, 150), outline=(120, 105, 70))
    for lon, lat in DOTS:
        x, y = project(lon, lat, x0, y0, w, h)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=GREY)
    for n, (lon, lat) in PINS.items():
        x, y = project(lon, lat, x0, y0, w, h)
        dx, dy = PIN_OFFSETS.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([x, y, x + dx, y + dy], fill=INK, width=1)
            x, y = x + dx, y + dy
        r = 8
        d.ellipse([x - r, y - r, x + r, y + r], fill=BRICK, outline=INK,
                  width=1)
        d.text((x, y), str(n), font=SANS_B(9), fill=(255, 255, 255),
               anchor="mm")

# ---------------------------------------------------------------- scenes
def scene_frame(d, x, y, w, h, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=1)


def face(d, cx, cy, r, skin, hair, hair_style):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin, outline=INK,
              width=1)
    if hair_style == "blond":
        d.pieslice([cx - r, cy - r - 4, cx + r, cy + r - 6], 180, 360,
                   fill=(240, 210, 90), outline=INK, width=1)
        d.rectangle([cx - r, cy - r + 2, cx + r, cy - r + 7],
                    fill=(240, 210, 90))
    elif hair_style == "black":
        d.pieslice([cx - r, cy - r - 3, cx + r, cy + r - 8], 180, 360,
                   fill=(20, 20, 20), outline=INK, width=1)
    elif hair_style == "grey":
        d.pieslice([cx - r, cy - r - 3, cx + r, cy + r - 8], 180, 360,
                   fill=(200, 200, 200), outline=INK, width=1)
    d.ellipse([cx - r - 3, cy - 2, cx - r + 3, cy + 4], fill=skin,
              outline=INK, width=1)
    d.ellipse([cx + r - 3, cy - 2, cx + r + 3, cy + 4], fill=skin,
              outline=INK, width=1)
    d.ellipse([cx - 8, cy - 3, cx - 5, cy + 0], fill=INK)
    d.ellipse([cx + 5, cy - 3, cx + 8, cy + 0], fill=INK)
    d.arc([cx - 6, cy + 2, cx + 6, cy + 10], 10, 170, fill=INK, width=2)


def figure(d, cx, base_y, suit, tie, skin, hair, hs):
    # torso
    d.polygon([(cx - 26, base_y), (cx - 20, base_y - 42), (cx + 20, base_y - 42),
               (cx + 26, base_y)], fill=suit, outline=INK, width=1)
    # shirt + tie
    d.polygon([(cx - 7, base_y - 42), (cx + 7, base_y - 42), (cx, base_y - 26)],
              fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(cx - 3, base_y - 38), (cx + 3, base_y - 38), (cx + 4, base_y - 22),
               (cx, base_y - 18), (cx - 4, base_y - 22)], fill=tie)
    face(d, cx, base_y - 58, 15, skin, hair, hs)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK,
                width=1)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=BRICK)
    d.rectangle([x, y, x + w * 0.45, y + h * 4 / 7], fill=NAVY)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK,
                width=1)
    for sx, sy in [(0.2, 0.25), (0.45, 0.15), (0.5, 0.35), (0.45, 0.55),
                   (0.2, 0.5)]:
        d.text((x + w * sx, y + h * sy), "★", font=SANS_B(8),
               fill=(255, 220, 0), anchor="mm")


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK,
                width=1)
    d.rectangle([x, y, x + w, y + h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def burst(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=INK, width=1)


def scene_apec(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (188, 211, 232))
    d.rectangle([x, y, x + w, y + 20], fill=GOLD)
    d.text((x + w / 2, y + 10), "FIRST US–CHINA–RUSSIA SUMMIT",
           font=SANS_B(10), fill=INK, anchor="mm")
    # flags on poles behind the three leaders
    flag_us(d, x + 28, y + 30, 34, 22)
    flag_cn(d, x + w / 2 - 17, y + 30, 34, 22)
    flag_ru(d, x + w - 62, y + 30, 34, 22)
    base = y + h - 26
    figure(d, x + 52, base, NAVY, BRICK, SKIN, None, "blond")
    figure(d, x + w / 2, base, (20, 20, 20), BRICK, SKIN2, None, "black")
    figure(d, x + w - 52, base, (60, 60, 70), (40, 90, 160), SKIN, None,
           "grey")
    # table + nameplates
    d.rectangle([x + 8, base + 2, x + w - 8, base + 22], fill=(240, 236, 222),
                outline=INK, width=1)
    for cx, name in [(x + 52, "TRUMP"), (x + w / 2, "XI"),
                     (x + w - 52, "PUTIN")]:
        d.rectangle([cx - 26, base + 5, cx + 26, base + 19], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.text((cx, base + 12), name, font=SANS_B(9), fill=INK, anchor="mm")


def scene_icj(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (223, 232, 216))
    bx, by, bw, bh = x + 12, y + 30, 150, 72
    d.polygon([(bx - 6, by), (bx + bw / 2, by - 18), (bx + bw + 6, by)],
              fill=(176, 58, 46), outline=INK, width=1)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(196, 120, 80),
                outline=INK, width=1)
    for i in range(4):
        cx = bx + 18 + i * 40
        d.rectangle([cx - 6, by + 8, cx + 6, by + bh - 8], fill=(250, 244, 228),
                    outline=INK, width=1)
    d.rectangle([bx - 4, by + bh, bx + bw + 4, by + bh + 8], fill=(120, 90, 70),
                outline=INK, width=1)
    # scales
    sx = x + w - 78
    d.line([sx, y + 30, sx, y + 96], fill=INK, width=3)
    d.line([sx - 34, y + 38, sx + 34, y + 38], fill=INK, width=3)
    for dx in (-34, 34):
        d.line([sx + dx, y + 38, sx + dx - 10, y + 62], fill=INK, width=2)
        d.line([sx + dx, y + 38, sx + dx + 10, y + 62], fill=INK, width=2)
        d.arc([sx + dx - 12, y + 56, sx + dx + 12, y + 70], 0, 180,
              fill=GOLD, width=3)
    d.ellipse([sx - 5, y + 24, sx + 5, y + 34], fill=GOLD, outline=INK,
              width=1)
    # badge 9-6
    d.rectangle([x + w - 66, y + 6, x + w - 8, y + 28], fill=BRICK,
                outline=INK, width=1)
    d.text((x + w - 37, y + 17), "9–6", font=SANS_B(13),
           fill=(255, 255, 255), anchor="mm")
    d.text((x + w - 8, y + h - 10), "GENOCIDE RULING", font=SANS_B(9),
           fill=BRICK, anchor="ra")


def scene_cop31(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (207, 227, 221))
    # globe
    gx, gy, gr = x + 52, y + 58, 38
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 180),
              outline=INK, width=2)
    d.ellipse([gx - 18, gy - 26, gx + 2, gy - 2], fill=(90, 170, 90),
              outline=INK, width=1)
    d.ellipse([gx - 4, gy + 6, gx + 22, gy + 28], fill=(90, 170, 90),
              outline=INK, width=1)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=INK, width=1)
    # thermometer
    tx = x + 108
    d.rounded_rectangle([tx - 6, y + 18, tx + 6, y + 84], radius=3,
                        fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([tx - 13, y + 78, tx + 13, y + 104], fill=BRICK, outline=INK,
              width=1)
    d.rectangle([tx - 2, y + 40, tx + 2, y + 84], fill=BRICK)
    # draft document with FOSSIL FUELS struck through
    dx, dy, dw, dh = x + 150, y + 14, 158, 76
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((dx + 8, dy + 6), "DRAFT DEAL · 19 NOV", font=SANS_B(9), fill=INK)
    d.text((dx + 8, dy + 24), "FOSSIL FUELS", font=SANS_B(13), fill=INK)
    d.line([dx + 6, dy + 31, dx + 118, dy + 31], fill=BRICK, width=3)
    d.text((dx + 8, dy + 42), "$120BN ADAPTATION AID", font=SANS_B(10),
           fill=INK)
    d.line([dx + 6, dy + 62, dx + 150, dy + 62], fill=BRICK, width=2)
    # stamp CUT
    d.rectangle([x + w - 74, y + h - 26, x + w - 10, y + h - 6], fill=BRICK,
                outline=INK, width=1)
    d.text((x + w - 42, y + h - 16), "CUT", font=SANS_B(12),
           fill=(255, 255, 255), anchor="mm")
    d.text((x + 52, y + h - 10), "TALKS END FRIDAY", font=SANS_B(9),
           fill=INK, anchor="mm")


def scene_kerch(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (206, 220, 228))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 150, 175),
                outline=INK, width=1)
    # bridge deck + arch
    d.line([x + 8, y + h - 34, x + w - 8, y + h - 34], fill=INK, width=4)
    d.arc([x + 20, y + 12, x + w - 20, y + h - 20], 180, 360, fill=INK,
          width=3)
    for px in (x + 40, x + w - 40):
        d.line([px, y + h - 34, px, y + h - 26], fill=INK, width=3)
    burst(d, x + w / 2 + 30, y + 22, 15, (245, 180, 40))
    burst(d, x + w / 2 + 30, y + 22, 8, BRICK)


def scene_riyadh(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (28, 38, 66))
    for i, (bx, bw, bh) in enumerate([(8, 22, 26), (36, 16, 38), (58, 26, 30),
                                      (90, 18, 44), (114, 24, 24),
                                      (144, 20, 34)]):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(10, 14, 26),
                    outline=(60, 70, 100), width=1)
        for wy in range(y + h - bh + 4, y + h - 4, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 4], fill=GOLD)
    d.arc([x + 30, y - 30, x + 150, y + 60], 300, 30, fill=(255, 255, 255),
          width=2)
    burst(d, x + 150, y + 14, 9, (255, 220, 100))


def scene_cyclone(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (200, 222, 235))
    cx, cy = x + w / 2, y + h / 2 - 4
    rmax = min(34, h // 2 - 4)
    for r in (rmax, int(rmax * 0.76), int(rmax * 0.53), int(rmax * 0.3)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=NAVY, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(232, 214, 170),
                outline=INK, width=1)
    d.text((x + 6, y + 4), "ODISHA", font=SANS_B(9), fill=BRICK)


def scene_seoul(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (238, 232, 210))
    # gavel diagonal
    d.line([x + 30, y + h - 12, x + 110, y + 18], fill=(120, 72, 20),
           width=7)
    d.rectangle([x + 96, y + 6, x + 140, y + 26], fill=(90, 55, 15),
                outline=INK, width=1)
    d.rectangle([x + 130, y + 2, x + 138, y + 30], fill=(90, 55, 15),
                outline=INK, width=1)
    d.rectangle([x + 118, y + h - 22, x + w - 8, y + h - 8], fill=BRICK,
                outline=INK, width=1)
    d.text((x + (118 + w - 8) / 2, y + h - 15), "OVERTURNED",
           font=SANS_B(9), fill=(255, 255, 255), anchor="mm")
    # taegeuk
    d.ellipse([x + 14, y + 8, x + 40, y + 34], fill=(255, 255, 255),
              outline=INK, width=1)
    d.pieslice([x + 14, y + 8, x + 40, y + 34], 180, 360, fill=BRICK)
    d.pieslice([x + 14, y + 8, x + 40, y + 34], 0, 180, fill=NAVY)


def scene_greenland(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (210, 226, 238))
    d.polygon([(x + 6, y + h), (x + 60, y + 14), (x + 118, y + h)],
              fill=(240, 244, 250), outline=INK, width=1)
    d.polygon([(x + 70, y + h), (x + 130, y + 22), (x + 190, y + h)],
              fill=(200, 216, 230), outline=INK, width=1)
    # Denmark flag
    d.rectangle([x + 12, y + 8, x + 44, y + 24], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x + 12, y + 14, x + 44, y + 18], fill=BRICK)
    d.rectangle([x + 24, y + 8, x + 28, y + 24], fill=BRICK)
    # US flag mini
    flag_us(d, x + 50, y + 8, 32, 16)
    d.rectangle([x + w - 52, y + 6, x + w - 6, y + 24], fill=BRICK,
                outline=INK, width=1)
    d.text((x + w - 29, y + 15), "109–0", font=SANS_B(10),
           fill=(255, 255, 255), anchor="mm")


def scene_anthropic(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (24, 60, 44))
    d.text((x + 10, y + 6), "ANT", font=SANS_B(20), fill=(255, 255, 255))
    pts = [(x + 12, y + h - 12), (x + 50, y + h - 22), (x + 80, y + h - 18),
           (x + 115, y + h - 28), (x + 150, y + h - 34), (x + 182, y + h - 42)]
    d.line(pts, fill=(120, 220, 140), width=3)
    d.polygon(pts + [(x + 182, y + h), (x + 12, y + h)],
              fill=(60, 140, 80))
    d.line(pts, fill=(120, 220, 140), width=3)
    d.polygon([(x + 182, y + h - 42), (x + 182, y + h - 32),
               (x + 168, y + h - 42)], fill=(120, 220, 140))
    d.rectangle([x + w - 74, y + h - 24, x + w - 8, y + h - 8], fill=GOLD,
                outline=INK, width=1)
    d.text((x + w - 41, y + h - 16), "IPO $83", font=SANS_B(10), fill=INK,
           anchor="mm")


def scene_gta(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (88, 52, 130))
    d.text((x + w / 2, y + 2), "VI", font=SERIF_B(22),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + w - 6, y + 6), "13 YEARS ON", font=SANS_B(8),
           fill=GOLD, anchor="ra")
    # controller
    cx, cy = x + w / 2, y + h - 16
    d.rounded_rectangle([cx - 52, cy - 14, cx + 52, cy + 14], radius=12,
                        fill=(30, 30, 40), outline=INK, width=1)
    d.ellipse([cx - 38, cy - 5, cx - 28, cy + 5], fill=(200, 200, 210),
              outline=INK, width=1)
    d.ellipse([cx + 28, cy - 5, cx + 38, cy + 5], fill=(200, 200, 210),
              outline=INK, width=1)
    for dx, dy, c in [(-14, -6, (255, 220, 0)), (-6, -6, (255, 80, 80)),
                      (-14, 2, (80, 200, 255)), (-6, 2, (120, 220, 120))]:
        d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                  fill=c, outline=INK, width=1)


def scene_bogota(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (238, 226, 200))
    # Colombia flag
    d.rectangle([x + 10, y + 6, x + 54, y + 22], fill=(255, 220, 0),
                outline=INK, width=1)
    d.rectangle([x + 10, y + 17, x + 54, y + 22], fill=(0, 60, 160))
    d.rectangle([x + 10, y + 20, x + 54, y + 22], fill=BRICK)
    # crowd
    cols = [BRICK, NAVY, (40, 120, 60), (200, 140, 40), (110, 60, 140)]
    for i in range(7):
        cx = x + 18 + i * 24
        d.ellipse([cx - 6, y + 30, cx + 6, y + 42], fill=SKIN, outline=INK,
                  width=1)
        d.polygon([(cx - 10, y + h - 4), (cx - 8, y + 44), (cx + 8, y + 44),
                   (cx + 10, y + h - 4)], fill=cols[i % 5], outline=INK,
                  width=1)
    d.rectangle([x + 120, y + 8, x + 186, y + 24], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((x + 153, y + 16), "PARO NACIONAL", font=SANS_B(8), fill=INK,
           anchor="mm")


def scene_nairobi(d, x, y, w, h):
    scene_frame(d, x, y, w, h, (240, 224, 200))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(176, 96, 60),
                outline=INK, width=1)
    d.line([x, y + h - 12, x + w, y + h - 12], fill=(255, 255, 255), width=1)
    # runner stick figure
    cx, cy = x + 70, y + 22
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=SKIN, outline=INK,
              width=1)
    d.line([cx, cy + 7, cx - 4, cy + 26], fill=INK, width=3)
    d.line([cx - 4, cy + 26, cx - 18, cy + 34], fill=INK, width=3)
    d.line([cx - 4, cy + 26, cx + 12, cy + 30], fill=INK, width=3)
    d.line([cx, cy + 12, cx - 16, cy + 6], fill=INK, width=3)
    d.line([cx, cy + 12, cx + 16, cy + 20], fill=INK, width=3)
    d.rectangle([x + w - 72, y + 6, x + w - 8, y + 24], fill=BRICK,
                outline=INK, width=1)
    d.text((x + w - 40, y + 15), "BANNED", font=SANS_B(10),
           fill=(255, 255, 255), anchor="mm")


def scene_canberra(d, x, y, w, h):
    scene_frame(d, x, y, w, h, NAVY)
    d.text((x + w / 2, y + 6), "4.9%", font=SANS_B(26),
           fill=(255, 255, 255), anchor="ma")
    # falling arrow
    d.line([x + 16, y + 10, x + 52, y + 30], fill=BRICK, width=4)
    d.polygon([(x + 52, y + 30), (x + 40, y + 28), (x + 50, y + 40)],
              fill=BRICK)
    for i, cx in enumerate([x + 120, x + 145, x + 170]):
        d.ellipse([cx - 6, y + 34, cx + 6, y + 46], fill=SKIN, outline=INK,
                  width=1)
        d.polygon([(cx - 8, y + h - 4), (cx - 6, y + 48), (cx + 6, y + 48),
                   (cx + 8, y + h - 4)], fill=[(200, 200, 200), BRICK,
                   (40, 120, 60)][i], outline=INK, width=1)

# ---------------------------------------------------------------- content
HEROES = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT",
         head="Trump, Xi and Putin meet in first three-way summit",
         deck=("Ninety minutes at Kylin Villa produce a four-point "
               "\u201cDeclaration Towards Peace\u201d on nuclear war \u2014 yet "
               "Ukraine goes unmentioned, with no timeline, no mechanism."),
         src="Reuters \u00b7 AP \u00b7 Xinhua", tag="REPORTED",
         scene=scene_apec),
    dict(n=2, place="THE HAGUE", topic="JUSTICE",
         head="World Court finds Myanmar guilty of genocide",
         deck=("Nine judges to six, the ICJ rules Myanmar committed "
               "genocide against the Rohingya \u2014 the first state ever "
               "found guilty in the court\u2019s 80-year history \u2014 and "
               "orders reparations."),
         src="Al Jazeera \u00b7 UN News", tag="REPORTED",
         scene=scene_icj),
    dict(n=3, place="ANTALYA", topic="CLIMATE",
         head="COP31 draft drops fossil-fuel text and $120bn aid goal",
         deck=("The slimmed-down draft sets no figure for adaptation aid; "
               "talks are due to end on Friday."),
         src="Reuters \u00b7 AFP", tag="REPORTED", scene=scene_cop31),
]

CARDS = [
    dict(n=4, place="CRIMEA", topic="WAR",
         head="Ukraine strikes Crimea bridge again",
         deck="A third strike in a week stops trains to Russia.",
         src="Euronews", tag="REPORTED", scene=scene_kerch),
    dict(n=5, place="RIYADH", topic="WAR",
         head="Saudis shoot down Houthi missiles",
         deck="Debris fell on the capital; no casualties reported.",
         src="Reuters", tag="REPORTED", scene=scene_riyadh),
    dict(n=6, place="ODISHA", topic="STORM",
         head="Cyclone Akvan nears India\u2019s coast",
         deck="Over 100,000 in shelters before Friday\u2019s landfall.",
         src="IMD", tag="REPORTED", scene=scene_cyclone),
    dict(n=7, place="SEOUL", topic="JUSTICE",
         head="Korea\u2019s top court clears ex-PM Han",
         deck="Han Duck-soo\u2019s martial law conviction is overturned.",
         src="AP", tag="REPORTED", scene=scene_seoul),
    dict(n=8, place="GREENLAND", topic="SECURITY",
         head="Denmark backs Arctic pact with US",
         deck="Parliament approves the Greenland security deal 109\u20130.",
         src="AP", tag="REPORTED", scene=scene_greenland),
    dict(n=9, place="NEW YORK", topic="MARKETS",
         head="Anthropic starts trading on Nasdaq",
         deck=("Its record $81.3bn share sale was priced at $83; shares "
               "rose 17% on day one."),
         src="AP", tag="REPORTED", scene=scene_anthropic),
    dict(n=10, place="WORLDWIDE", topic="GAMES",
         head="GTA VI goes on sale after 13 years",
         deck="The midnight launch draws rave reviews.",
         src="ABC", tag="REPORTED", scene=scene_gta),
    dict(n=11, place="BOGOT\u00c1", topic="LABOUR",
         head="Colombia\u2019s unions hold national strike",
         deck="Marches in three cities against an economic law.",
         src="Infobae", tag="REPORTED", scene=scene_bogota),
    dict(n=12, place="NAIROBI", topic="SPORT",
         head="Marathon champion banned for doping",
         deck="Kenya\u2019s Peres Jepchirchir gets three years.",
         src="ABC", tag="REPORTED", scene=scene_nairobi),
    dict(n=13, place="CANBERRA", topic="ECONOMY",
         head="Australia\u2019s jobless rate hits 4.9%",
         deck="Highest since 2024; shares and the dollar slide.",
         src="ABC", tag="REPORTED", scene=scene_canberra),
]

BRIEFS = [
    (14, "Shenzhen", "Xi urges ban on all nuclear arms.", "Al Jazeera"),
    (15, "APEC", "Albanese to Putin: \u201cEnd your war, end it now.\u201d",
     "ABC"),
    (16, "Seoul", "Half a million sit college entrance exam.", "Sedaily"),
    (17, "Jakarta", "Asset-seizure law passes after 18 years.", "Kompas"),
    (18, "Hormuz", "Iran says mines set 5 tankers ablaze.", "Al Jazeera"),
    (19, "Gaza", "Israel ends tank raid past truce line.", "BBC"),
    (20, "Krasnodar", "Kyiv says it hit two oil refineries.", "Euronews"),
    (21, "Brussels", "EU delays methane rules two years.", "Euronews"),
    (22, "UK", "Inquiry: yacht Bayesian was vulnerable to wind.", "RNZ"),
    (23, "Zurich", "Two rivals to challenge FIFA\u2019s Infantino.", "ABC"),
    (24, "Rome", "Author Corrado Augias dies at 91.", "Euronews"),
    (25, "Mogadishu", "Somalia expels UAE ambassador.", "Al Jazeera"),
    (26, "Sudan", "Court sentences absent RSF chief to death.", "AP"),
    (27, "Pretoria", "Central bank holds rate at 7.25%.", "SABC"),
    (28, "Canaries", "Record 11,000 migrants in 15 days.", "Africanews"),
    (29, "Florida", "Floods shut Broward, Miami schools again.", "CBS"),
    (30, "Wellington", "Court: pay equity cuts broke rights law.", "RNZ"),
    (31, "Tonga", "Drought emergency takes effect.", "RNZ"),
    (32, "Cook Islands", "Cyclone Xavier weakens to category 4.", "RNZ"),
    (33, "Space", "Red giant seen eating a Sun-sized star.", "Nature"),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court genocide vote"),
    ("$120bn", "aid goal cut at COP31"),
    ("$81.3bn", "Anthropic\u2019s record IPO"),
    ("109\u20130", "Danish vote on Arctic pact"),
    ("4.9%", "Australian jobless rate"),
]

REGIONS = [
    ("ASIA 7", (176, 58, 46)), ("MIDDLE EAST 3", (140, 40, 40)),
    ("EUROPE 7", (31, 56, 100)), ("AFRICA 5", (46, 107, 52)),
    ("AMERICAS 4", (107, 79, 161)), ("OCEANIA 4", (42, 127, 111)),
    ("GLOBAL 3", (90, 86, 76)),
]

LEFT_OUT = ("EU\u2019s \u20ac45bn Ukraine loan plan \u00b7 Iran fires on "
            "Kuwait and Bahrain \u00b7 Nvidia results \u00b7 Jeffries named "
            "for US speaker \u00b7 Carney on China ties \u00b7 Van Gogh "
            "$190.4m sale \u00b7 Voyager 1 one light-day \u00b7 Pew 2035 \u00b7 "
            "Anthropic IPO pricing ($83) \u00b7 Gaza push began")
NOT_YET = "COP31\u2019s scheduled close \u00b7 Cyclone Akvan\u2019s landfall"

SUBHEAD = ("Trump, Xi and Putin share one table \u00b7 The World Court "
           "finds genocide in Myanmar \u00b7 COP31\u2019s draft drops fossil "
           "fuels")

FOOTER = ("Claims are attributed, not stated as fact \u00b7 Pictures and "
          "map: original, drawn in code \u00b7 Sources: Reuters, AP, AFP, "
          "BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature, "
          "Kompas, SABC, CBS, Africanews, Infobae, Sedaily, IMD \u00b7 "
          "2026-11-19")


def hero_panel(d, x, y, w, h, item):
    scene_h = 118
    item["scene"](d, x, y, w, scene_h)
    ty = y + scene_h + 6
    num_badge(d, x + 11, ty + 6, item["n"], r=11)
    kicker(d, x + 26, ty, item["place"], item["topic"])
    ty += 20
    lines = wrap(item["head"], SERIF_B(19), w - 4)
    ty = fit_lines(d, x + 2, ty, lines[:2], SERIF_B(19), INK, 22)
    ty += 2
    lines = wrap(item["deck"], SANS(10), w - 4)
    fit_lines(d, x + 2, ty, lines[:3], SANS(10), INK, 13)
    d.text((x + 2, y + h - 12), "\u2014 " + item["src"], font=SANS(10),
           fill=GREY)
    tw = SANS_B(10).getlength(item["tag"])
    d.text((x + w - 2 - tw, y + h - 12), item["tag"], font=SANS_B(10),
           fill=BRICK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def card_panel(d, x, y, w, h, item):
    scene_h = 50
    item["scene"](d, x, y, w, scene_h)
    ty = y + scene_h + 4
    num_badge(d, x + 9, ty + 5, item["n"], r=9)
    kicker(d, x + 20, ty - 1, item["place"], item["topic"],
           font=SANS_B(9))
    ty += 15
    lines = wrap(item["head"], SERIF_B(13), w - 4)
    ty = fit_lines(d, x + 2, ty, lines[:2], SERIF_B(13), INK, 14)
    lines = wrap(item["deck"], SANS(9), w - 4)
    fit_lines(d, x + 2, ty, lines[:2], SANS(9), INK, 10)
    d.text((x + 2, y + h - 11), "\u2014 " + item["src"], font=SANS(8),
           fill=GREY)
    tw = SANS_B(8).getlength(item["tag"])
    d.text((x + w - 2 - tw, y + h - 11), item["tag"], font=SANS_B(8),
           fill=BRICK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=2)
    x0, x1 = 16, W - 16
    cw = x1 - x0

    # kicker row
    d.text((x0, 14), "THE DAY IN WORLD NEWS", font=SANS_B(14), fill=INK)
    rt = "33 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    d.text((x1, 14), rt, font=SANS_B(13), fill=BRICK, anchor="ra")

    # masthead
    f = SERIF_B(52)
    while f.getlength("Thursday 19 November 2026") > cw:
        f = SERIF_B(f.size - 1)
    d.text((x0, 30), "Thursday 19 November 2026", font=f, fill=INK)
    # subhead (auto-fit italic serif)
    fs = 16
    while SERIF_I(fs).getlength(SUBHEAD) > cw:
        fs -= 1
    d.text((x0, 86), SUBHEAD, font=SERIF_I(fs), fill=BRICK)
    d.line([x0, 106, x1, 106], fill=INK, width=2)

    # number strip: 6 navy blocks
    y = 112
    bw, gap = 164, 4
    for i, (num, label) in enumerate(NUMBERS):
        bx = x0 + i * (bw + gap)
        d.rectangle([bx, y, bx + bw, y + 52], fill=NAVY, outline=INK,
                    width=1)
        nf = SANS_B(26)
        while nf.getlength(num) > bw - 10:
            nf = SANS_B(nf.size - 1)
        d.text((bx + bw / 2, y + 6), num, font=nf, fill=(255, 255, 255),
               anchor="ma")
        lf = SANS(10)
        lines = wrap(label, lf, bw - 8)
        ly = y + 36
        for ln in lines[:2]:
            d.text((bx + bw / 2, ly), ln, font=lf, fill=(255, 255, 255),
                   anchor="ma")
            ly += 11

    # region strip: 7 chips
    y = 170
    cx = x0
    for label, col in REGIONS:
        fnt = SANS_B(11)
        wch = fnt.getlength(label) + 16
        d.rectangle([cx, y, cx + wch, y + 20], fill=col, outline=INK,
                    width=1)
        d.text((cx + wch / 2, y + 10), label, font=fnt,
               fill=(255, 255, 255), anchor="mm")
        cx += wch + 5

    # hero: 3 panels
    y = 196
    hw, hgap = 330, 7
    for i, item in enumerate(HEROES):
        hero_panel(d, x0 + i * (hw + hgap), y, hw, 244, item)

    # tag legend
    y = 444
    legend = ("HOW SURE ARE WE? \u2014 REPORTED: confirmed by multiple "
              "sources \u00b7 CLAIM: as claimed by one side \u00b7 FORECAST: "
              "projection, not yet fact")
    d.text((x0, y), legend, font=SANS(10), fill=GREY)

    # secondary grid: 2 rows x 5
    y = 460
    kw, kgap = 196, 6
    kh = 130
    for r in range(2):
        for c in range(5):
            item = CARDS[r * 5 + c]
            card_panel(d, x0 + c * (kw + kgap), y + r * (kh + 6), kw, kh,
                       item)

    # bottom band: briefs left, map right
    y = 730
    d.text((x0, y), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=SANS_B(12),
           fill=INK)
    d.text((x1, y), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK,
           anchor="ra")
    d.line([x0, y + 16, x1, y + 16], fill=INK, width=1)
    by = y + 22
    # briefs: 2 columns x 10 rows
    col_w = 300
    for i, (n, place, text, src) in enumerate(BRIEFS):
        col = i // 10
        row = i % 10
        bx = x0 + col * (col_w + 4)
        ry = by + row * 16
        d.text((bx, ry), str(n), font=SANS_B(10), fill=BRICK)
        nw = SANS_B(10).getlength(str(n)) + 3
        full = place + " \u2014 " + text + " " + src + "."
        fnt = SANSC(10)
        # place bold: draw place in bold condensed, rest regular
        d.text((bx + nw, ry), place, font=SANSC_B(10), fill=INK)
        pw = SANSC_B(10).getlength(place)
        rest = " \u2014 " + text + " " + src + "."
        while fnt.getlength(rest) > col_w - nw - pw - 2 and fnt.size > 8:
            fnt = SANSC(fnt.size - 1)
        d.text((bx + nw + pw, ry), rest, font=fnt, fill=INK)
    # map right
    mx = x0 + 2 * (col_w + 4) + 6
    mw = x1 - mx
    draw_map(d, mx, by, mw, 148)
    d.text((mx, by + 152), "numbers match the stories \u00b7 dots: briefs",
           font=SANS(8), fill=GREY)

    # DATE CHECK box (2 columns)
    y = 916
    d.rectangle([x0, y, x1, y + 70], outline=INK, width=2)
    d.text((x0 + 8, y + 5),
           "DATE CHECK \u2713  Every story on this page happened, or was "
           "first reported, on Thursday 19 November 2026.",
           font=SANS_B(11), fill=INK)
    d.line([x0, y + 24, x1, y + 24], fill=LIGHT_LINE, width=1)
    colw = (cw - 16) // 2
    d.text((x0 + 8, y + 28), "LEFT OUT \u2014 18 NOV:",
           font=SANS_B(10), fill=BRICK)
    lines = wrap(LEFT_OUT, SANS(9), colw - 8)
    ly = y + 40
    for ln in lines[:3]:
        d.text((x0 + 8, ly), ln, font=SANS(9), fill=INK)
        ly += 10
    d.line([x0 + colw + 4, y + 26, x0 + colw + 4, y + 68], fill=LIGHT_LINE,
           width=1)
    d.text((x0 + colw + 12, y + 28), "NOT YET \u2014 20 NOV:",
           font=SANS_B(10), fill=BRICK)
    lines = wrap(NOT_YET, SANS(9), colw - 12)
    ly = y + 40
    for ln in lines[:2]:
        d.text((x0 + colw + 12, ly), ln, font=SANS(9), fill=INK)
        ly += 10

    # footer sources
    y = 990
    fnt = SANSC(9)
    while fnt.getlength(FOOTER) > cw:
        fnt = SANSC(fnt.size - 1)
    d.text((x0, y), FOOTER, font=fnt, fill=GREY)
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    img = draw()
    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out))
