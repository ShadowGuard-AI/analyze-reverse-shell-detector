#!/usr/bin/env python3
"""analyze-reverse-shell-detector logo: one lobed fin from the flank of a coelacanth, seen from the side
and filling the frame, its fleshy stalk angled down and its fan of rays spread wide, drawn in abyss indigo
with the ray divisions picked out in silt grey. A single anglerfish gold point of light sits at the tip of
the foremost ray, small and round, the sole warm note. The surrounding shape is cut away to bone white.
Beneath it the name is set in BBH Bartle in abyss indigo, heavy enough to survive reduction."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 900, 520
INDIGO = (20, 33, 61); GOLD = (232, 178, 60); SILT = (158, 162, 158); BONE = (238, 234, 222)
img = Image.new("RGB", (W, H), BONE); d = ImageDraw.Draw(img, "RGBA")
# the fin: stalk entering at the upper left, angled down to the fan joint, rays spreading wide to the right
sx, sy = 196, 96
jx, jy = 356, 252  # the joint where stalk meets fan
d.line([(sx, sy), (jx, jy)], fill=INDIGO, width=64)
d.line([(sx, sy), (jx, jy)], fill=(30, 48, 86), width=38)
ray_angles = [-58, -34, -10, 14, 38, 62] if A != "--v1" else [i * 9 - 60 for i in range(15)]  # v1 flaw: fifteen thin rays, a fan coral
ray_len = 252
tips = []
for a in ray_angles:
    r = math.radians(a); tx, ty = jx + math.cos(r) * ray_len, jy + math.sin(r) * ray_len
    tips.append((tx, ty))
    wdt = 4 if A == "--v1" else 21
    d.line([(jx, jy), (tx, ty)], fill=INDIGO, width=wdt)
    d.line([(jx, jy), (tx, ty)], fill=SILT, width=2)  # the ray division picked out in silt grey
d.ellipse([jx - 30, jy - 30, jx + 30, jy + 30], fill=INDIGO)
if A != "--v2":  # v2 flaw: the gold point dropped, and with it the only warm note and the 64 pixel test
    gx, gy = tips[2]  # tip of the foremost ray
    for r, a in [(17, 60), (10, 130), (5.5, 255)]:
        d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(GOLD[0], GOLD[1], GOLD[2], a))
try:
    fb = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BBHBartle.ttf", 40)
    fr = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/AlegreyaSans.ttf", 36)
except Exception:
    fb = fr = ImageFont.load_default()
name = "analyze-reverse-shell-detector"
src = fr if A == "--v2" else fb
size = 40
while size > 12:
    trial = ImageFont.truetype(__file__.rsplit("/", 1)[0] + ("/fonts/AlegreyaSans.ttf" if A == "--v2" else "/fonts/BBHBartle.ttf"), size)
    if d.textlength(name, font=trial) <= 856:
        src = trial; break
    size -= 2
d.text((450, 466), name, font=src, fill=INDIGO, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = {"--v1": "scratch/logo-v1.png", "--v2": "scratch/logo-v2.png"}.get(A, "logo.png")
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if A == "":
    img.resize((64, 37)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
