#!/usr/bin/env python3
"""analyze-reverse-shell-detector wordmark banner: inside a volcanic cave off the Comoros, at a depth
where surface light has thinned to a greenish memory far above the entrance. Black basalt walls curve
away on both sides, pitted and hung with pale sediment, and the cave floor drops out of sight into abyss
indigo. At the centre, suspended a little above that floor and angled toward the viewer, hangs a whole
coelacanth, large and still apart from the slowest movement of its paired fins. Its eye catches one
thread of anglerfish gold from a lure drifting at the right hand edge, where a much smaller fish holds
station. Silt grey motes hang in the water. The title belongs to the cave mouth behind the fish: the name
picked out in BBH Bartle in bone white across a pale band of fallen sediment on the rear wall."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(31)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1200, 420
INDIGO = (20, 33, 61); GOLD = (232, 178, 60); SILT = (158, 162, 158); BONE = (238, 234, 222)
img = Image.new("RGB", (W, H), (8, 12, 28)); d = ImageDraw.Draw(img, "RGBA")
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(12 + 6 * t), int(20 + 6 * t), int(40 + 14 * t)))
d.ellipse([900, -130, 1250, 130], fill=(44, 96, 96, 130))  # the entrance, a greenish memory above
# basalt walls curving away on both sides, pitted, hung with pale sediment
d.polygon([(0, 0), (190, 0), (150, 150), (176, 300), (130, 420), (0, 420)], fill=(10, 12, 22))
d.polygon([(1200, 0), (1060, 0), (1030, 130), (1066, 300), (1110, 420), (1200, 420)], fill=(10, 12, 22))
for _ in range(170):
    side = random.choice([0, 1]); x = random.uniform(0, 165) if side == 0 else random.uniform(1045, 1195); y = random.uniform(0, H); r = random.uniform(1.5, 4.6)
    if random.random() < 0.4:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(190, 186, 172, 90))
    else:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(4, 5, 10, 160))
# a pale band of fallen sediment across the rear wall, behind the fish
d.polygon([(262, 78), (938, 66), (954, 158), (278, 172)], fill=(138, 136, 124))
d.polygon([(262, 78), (938, 66), (954, 158), (278, 172)], outline=(150, 146, 132), width=2)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BBHBartle.ttf", 27)
except Exception:
    f = ImageFont.load_default()
name = "analyze-reverse-shell-detector"
if A == "--v1":  # v1 flaw: the name lettered across the fish itself, a label on the animal
    pass  # lettering is drawn after the fish in this variant
elif A == "--v2":  # v2 flaw: the name in gold, huge, floating in the open water at the top
    fbig = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BBHBartle.ttf", 52)
    d.text((600, 66), name, font=fbig, fill=GOLD, anchor="mm")
else:
    d.text((608, 98), "analyze-reverse-", font=f, fill=BONE, anchor="mm")  # bone white lettering across the pale sediment band, two survey lines
    d.text((608, 134), "shell-detector", font=f, fill=BONE, anchor="mm")
# the cave floor drops out of sight into abyss indigo
d.polygon([(0, 420), (240, 342), (960, 342), (1200, 420)], fill=(6, 9, 20))
# the coelacanth at the centre, suspended a little above that floor, still
cx, cy = 600, 238
d.polygon([(330, cy + 2), (398, cy - 42), (522, cy - 52), (664, cy - 44), (782, cy - 22), (842, cy - 30), (872, cy - 6), (892, cy + 2), (872, cy + 12), (842, cy + 34), (782, cy + 26), (664, cy + 44), (522, cy + 50), (398, cy + 38)], fill=(27, 42, 74))
d.polygon([(330, cy + 2), (398, cy - 42), (522, cy - 52), (556, cy), (522, cy + 50), (398, cy + 38)], fill=(33, 50, 86))
for bx in range(452, 776, 42):
    for by in (-26, -4, 16):
        d.arc([bx - 14, cy + by - 8, bx + 14, cy + by + 8], 0, 180, fill=(120, 136, 160, 75), width=2)
def fin(x, y, ang, ln, spread):
    ex, ey = x + math.cos(math.radians(ang)) * ln * 0.45, y + math.sin(math.radians(ang)) * ln * 0.45
    d.line([(x, y), (ex, ey)], fill=(31, 47, 78), width=12)
    for k in range(5):
        a2 = math.radians(ang - spread / 2 + spread * k / 4)
        fx, fy = ex + math.cos(a2) * ln * 0.62, ey + math.sin(a2) * ln * 0.62
        d.line([(ex, ey), (fx, fy)], fill=(36, 54, 88), width=6)
        d.line([(ex, ey), (fx, fy)], fill=(110, 118, 118, 120), width=1)
fin(456, cy + 34, 118, 66, 50); fin(630, cy + 38, 96, 72, 54); fin(556, cy - 46, -78, 56, 46); fin(716, cy - 38, -96, 60, 48); fin(700, cy + 34, 74, 58, 46)
d.ellipse([356, cy - 12, 369, cy + 1], fill=(10, 12, 10))
d.ellipse([360, cy - 9, 364, cy - 5], fill=(210, 190, 120, 210))  # the eye catches one thread of gold
if A == "--v1":
    d.text((600, cy + 2), name, font=f, fill=BONE, anchor="mm")
# a much smaller fish holding station at the right hand edge, its lure drifting ahead of it
ax, ay = 1066, 210
d.ellipse([ax - 26, ay - 9, ax + 26, ay + 9], fill=(16, 20, 34))
d.polygon([(ax + 22, ay), (ax + 40, ay - 10), (ax + 40, ay + 10)], fill=(16, 20, 34))
d.arc([ax - 6, ay - 30, ax + 34, ay + 2], 300, 360, fill=(120, 118, 110), width=2)  # the lure stalk
for r, a in [(16, 40), (9, 90), (4.5, 240)]:
    d.ellipse([ax + 30 - r, ay - 34 - r, ax + 30 + r, ay - 34 + r], fill=(GOLD[0], GOLD[1], GOLD[2], a))
# silt grey motes hanging in the water, neither rising nor settling
for _ in range(110):
    x, y = random.uniform(200, 1040), random.uniform(40, 380); r = random.uniform(0.7, 1.7)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(SILT[0], SILT[1], SILT[2], random.randint(50, 115)))
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = {"--v1": "scratch/banner-v1.png", "--v2": "scratch/banner-v2.png"}.get(A, "banner.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
