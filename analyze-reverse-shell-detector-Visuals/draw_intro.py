#!/usr/bin/env python3
"""analyze-reverse-shell-detector intro: the cave and its tenant before any survey lettering, nothing
readable anywhere. Foreground: a basalt ledge entering from the lower left, its top dusted with pale
sediment, a few empty shells resting on it out of focus, silt hanging in the water beyond the ledge edge.
Midground: the coelacanth itself, full length, hanging head slightly down in open water between the walls,
fins spread, scales catching what little light reaches this far, its shadow lost against darker water
below. Background: the cave narrowing into blackness behind the fish, the entrance a dim blue green arch
high at the upper right, and one tiny gold lure glowing far back on the right."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(53)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1200, 520
INDIGO = (14, 22, 48); GOLD = (232, 178, 60); SILT = (158, 162, 158); BONE = (238, 234, 222)
img = Image.new("RGB", (W, H), (8, 12, 28)); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):  # water deepening downward into abyss indigo
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(12 + 6 * t), int(20 + 6 * t), int(40 + 14 * t)))
# cave entrance: a dim blue green arch high at the upper right
d.ellipse([930, -150, 1210, 120], fill=(38, 84, 86, 110))
d.ellipse([958, -128, 1184, 92], fill=(52, 108, 106, 85))
shaft = Image.new("RGB", (W, H), (0, 0, 0)); sd = ImageDraw.Draw(shaft)
sd.polygon([(960, 0), (1120, 0), (900, 300), (760, 300)], fill=(34, 60, 58))
shaft = shaft.filter(ImageFilter.GaussianBlur(30))
img.paste(Image.new("RGB", (W, H), (70, 130, 122)), (0, 0), shaft.convert("L").point(lambda v: int(v * 0.5)))
d = ImageDraw.Draw(img, "RGBA")
# black basalt walls curving away on both sides, pitted, hung with pale sediment
d.polygon([(0, 0), (210, 0), (168, 170), (196, 340), (150, 520), (0, 520)], fill=(10, 12, 22))
d.polygon([(1200, 210), (1060, 260), (1090, 420), (1140, 520), (1200, 520)], fill=(9, 11, 20))
d.polygon([(0, 0), (210, 0), (196, 60), (60, 44), (0, 70)], fill=(16, 18, 30))
for _ in range(210):  # pitting and sediment flecks on the walls
    side = random.choice([0, 1])
    x = random.uniform(0, 185) if side == 0 else random.uniform(1065, 1195)
    y = random.uniform(0, H)
    r = random.uniform(1.5, 5)
    if random.random() < 0.4:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(190, 186, 172, 90))  # pale sediment
    else:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(4, 5, 10, 160))  # a pit
# the cave narrowing into blackness behind the fish: the water simply darkens past the fish, no plate behind it
# one tiny gold lure glowing far back on the right, no fish clearly attached at this distance
lx, ly = (1036, 268) if A != "--v1" else (300, 420)  # v1 flaw: the lure dragged big and near into the foreground
lr = 4 if A != "--v1" else 17
for r, a in [(lr * 3.4, 36), (lr * 2, 70), (lr, 235)]:
    d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(GOLD[0], GOLD[1], GOLD[2], a))
# the coelacanth, full length in profile, head slightly down at the left, hanging in open water
cx, cy = 600, 268
tilt = 7
def P(points):
    out = []
    for (x, y) in points:
        yy = y + (x - cx) * math.tan(math.radians(tilt)) * 0.4
        out.append((x, yy))
    return out
if A == "--v2":  # v2 flaw: a generic shark silhouette, pointed tail, no lobed fins at all
    d.polygon(P([(330, cy - 6), (430, cy - 52), (700, cy - 40), (856, cy - 76), (812, cy), (856, cy + 62), (700, cy + 40), (430, cy + 48)]), fill=(24, 36, 66))
    d.polygon(P([(520, cy - 46), (590, cy - 104), (640, cy - 42)]), fill=(24, 36, 66))
else:
    # body: deep, armoured, tapered to a rounded tail with the small middle lobe coelacanths carry
    d.polygon(P([(322, cy + 2), (392, cy - 46), (520, cy - 58), (668, cy - 50), (790, cy - 26), (852, cy - 34), (884, cy - 8), (906, cy + 2), (884, cy + 14), (852, cy + 38), (790, cy + 30), (668, cy + 50), (520, cy + 56), (392, cy + 44)]), fill=(26, 40, 72))
    d.polygon(P([(322, cy + 2), (392, cy - 46), (520, cy - 58), (560, cy), (520, cy + 56), (392, cy + 44)]), fill=(31, 47, 82))  # head and gill shading
    for bx in range(448, 792, 42):  # scale arcs catching what little light reaches this far
        for by in (-30, -6, 18):
            d.arc([bx - 15, cy + by - 9, bx + 15, cy + by + 9], 0, 180, fill=(120, 136, 160, 80), width=2)
    # lobed fins: a fleshy stalk and a fan of rays, paired fins spread
    def fin(x, y, ang, ln, spread):
        ex, ey = x + math.cos(math.radians(ang)) * ln * 0.45, y + math.sin(math.radians(ang)) * ln * 0.45
        d.line([(x, y), (ex, ey)], fill=(30, 45, 76), width=13)  # the stalk
        for k in range(5):
            a2 = math.radians(ang - spread / 2 + spread * k / 4)
            fx, fy = ex + math.cos(a2) * ln * 0.62, ey + math.sin(a2) * ln * 0.62
            d.line([(ex, ey), (fx, fy)], fill=(34, 51, 84), width=7)
            d.line([(ex, ey), (fx, fy)], fill=(110, 118, 118, 120), width=1)  # ray division in silt grey
    fin(452, cy + 40, 118, 74, 52)   # pectoral fin, low
    fin(636, cy + 44, 96, 80, 56)    # pelvic fin, low
    fin(560, cy - 52, -78, 62, 48)   # first dorsal area fin, above
    fin(724, cy - 44, -96, 66, 50)   # second dorsal, above
    fin(706, cy + 40, 74, 64, 48)    # anal fin, below behind
    d.ellipse([352, cy - 14, 366, cy], fill=(10, 12, 10))  # the eye
    d.ellipse([356, cy - 11, 360, cy - 7], fill=(210, 190, 120, 200))  # one thread of gold caught in it
# silt grey motes hanging in the water between viewer and animal, neither rising nor settling
for _ in range(130):
    x, y = random.uniform(200, 1080), random.uniform(60, 470)
    r = random.uniform(0.7, 1.8)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(SILT[0], SILT[1], SILT[2], random.randint(50, 120)))
# foreground ledge from the lower left, top dusted with pale sediment, empty shells out of focus
ledge = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(ledge)
ld.polygon([(0, 520), (0, 420), (150, 398), (330, 428), (430, 478), (470, 520)], fill=(12, 14, 24, 255))
ld.polygon([(0, 420), (150, 398), (330, 428), (322, 436), (144, 410), (0, 428)], fill=(168, 164, 150, 110))  # sediment dusting
for (sx, sy, sr) in [(70, 424, 15), (128, 416, 11), (206, 424, 13)]:
    ld.arc([sx - sr, sy - sr * 0.7, sx + sr, sy + sr * 0.7], 20, 330, fill=(206, 200, 182, 220), width=3)
    ld.arc([sx - sr * 0.55, sy - sr * 0.4, sx + sr * 0.55, sy + sr * 0.4], 20, 330, fill=(206, 200, 182, 170), width=2)
ledge = ledge.filter(ImageFilter.GaussianBlur(2.2))  # out of focus, as the prose puts it
img.paste(Image.alpha_composite(img.convert("RGBA"), ledge).convert("RGB"), (0, 0))
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = {"--v1": "scratch/intro-v1.png", "--v2": "scratch/intro-v2.png"}.get(A, "intro-banner.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
