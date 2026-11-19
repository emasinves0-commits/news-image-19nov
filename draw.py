#!/usr/bin/env python3
"""Draws entry.png: a 1024x1024 infographic of 19 November 2026's world news."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=True):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

BG = (14, 22, 44); CARD = (26, 40, 76); WHITE = (245, 247, 252); SUB = (176, 192, 224)
GOLD = (255, 200, 60)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def center(text, font, cx, y, fill):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)

# header
d.rectangle([0, 0, W, 118], fill=(8, 14, 30))
d.rectangle([0, 118, W, 124], fill=GOLD)
center("19 NOVEMBER 2026", F(66), W / 2, 12, WHITE)
center("THURSDAY  •  THE WORLD IN FIVE STORIES", F(24), W / 2, 86, GOLD)

# icons (shapes only), drawn inside an 120x120 box at (x, y)
def icon_game(x, y, c):
    d.rounded_rectangle([x, y + 25, x + 120, y + 95], 22, fill=c)
    d.rectangle([x + 22, y + 52, x + 52, y + 62], fill=CARD)
    d.rectangle([x + 32, y + 42, x + 42, y + 72], fill=CARD)
    d.ellipse([x + 80, y + 36, x + 94, y + 50], fill=CARD)
    d.ellipse([x + 98, y + 46, x + 112, y + 60], fill=CARD)
    center("VI", F(26), x + 82, y + 66, CARD)

def icon_summit(x, y, c):
    for i, col in enumerate([(235, 90, 90), c, (90, 150, 235)]):
        cx = x + 22 + i * 38
        d.ellipse([cx - 16, y + 22, cx + 16, y + 54], fill=col)
        d.pieslice([cx - 24, y + 62, cx + 24, y + 112], 180, 360, fill=col)
    d.rectangle([x, y + 100, x + 120, y + 108], fill=c)

def icon_arctic(x, y, c):  # map pin over iceberg
    d.polygon([(x + 10, y + 110), (x + 40, y + 62), (x + 62, y + 84), (x + 84, y + 50), (x + 112, y + 110)], fill=c)
    d.polygon([(x + 84, y + 50), (x + 96, y + 70), (x + 74, y + 70)], fill=WHITE)
    d.ellipse([x + 30, y + 0, x + 66, y + 36], fill=(235, 90, 90))
    d.polygon([(x + 32, y + 28), (x + 64, y + 28), (x + 48, y + 56)], fill=(235, 90, 90))
    d.ellipse([x + 41, y + 9, x + 55, y + 23], fill=BG)

def icon_ukraine(x, y, c):  # bridge with a flash
    d.rectangle([x, y + 66, x + 120, y + 76], fill=c)
    for px in (x + 14, x + 54, x + 94):
        d.rectangle([px, y + 76, px + 12, y + 112], fill=c)
    d.arc([x + 6, y + 18, x + 114, y + 120], 200, 340, fill=c, width=6)
    for px in (x + 30, x + 60, x + 90):
        d.line([px, y + 66, px, y + 40], fill=c, width=4)
    d.polygon([(x + 70, y + 0), (x + 46, y + 36), (x + 62, y + 36), (x + 50, y + 62), (x + 84, y + 24), (x + 66, y + 24)], fill=GOLD)

def icon_iran(x, y, c):  # radar / missile-defense rings with alert
    for r, w in ((52, 6), (36, 6), (20, 6)):
        d.ellipse([x + 60 - r, y + 60 - r, x + 60 + r, y + 60 + r], outline=c, width=w)
    d.ellipse([x + 52, y + 52, x + 68, y + 68], fill=(235, 90, 90))
    d.line([x + 60, y + 60, x + 108, y + 24], fill=GOLD, width=5)

stories = [
    ((120, 190, 255), icon_game, "GTA VI LAUNCHES TO A 99 METASCORE",
     "Out on PS5 and Xbox; record reviews, launch-day PSN errors", "VIDEO GAMES"),
    ((255, 130, 120), icon_summit, "TRUMP, PUTIN AND XI HOLD SUMMIT",
     "Shenzhen talks end in a 4-point “peace declaration”", "DIPLOMACY"),
    ((130, 230, 200), icon_arctic, "DENMARK BACKS ARCTIC DEAL WITH US",
     "Parliament votes unanimously for Greenland security pact", "GREENLAND"),
    ((255, 190, 90), icon_ukraine, "UKRAINE: BERLIN TALKS, CRIMEA BRIDGE",
     "Allies meet on guarantees as Russia reports a third strike", "UKRAINE"),
    ((190, 150, 255), icon_iran, "TRUMP ON IRAN: “SEE WHAT HAPPENS”",
     "Waits past 1 Jan 2027; apparent Houthi strike on Riyadh", "MIDDLE EAST"),
]

top, ch, gap = 140, 156, 10
for i, (col, ic, head, sub, tag) in enumerate(stories):
    y = top + i * (ch + gap)
    d.rounded_rectangle([20, y, W - 20, y + ch], 18, fill=CARD)
    d.rounded_rectangle([20, y, 34, y + ch], 6, fill=col)
    # number badge
    d.ellipse([50, y + 12, 94, y + 56], fill=col)
    center(str(i + 1), F(30), 72, y + 15, BG)
    ic(66, y + 30, col)  # icon below-left: 120px box
    # text
    d.text((214, y + 14), tag, font=F(25), fill=col)
    fs = 35
    while d.textlength(head, font=F(fs)) > 780:
        fs -= 1
    d.text((214, y + 44 + (35 - fs) // 2), head, font=F(fs), fill=WHITE)
    line, ss = "19 Nov • " + sub, 26
    while d.textlength(line, font=F(ss, False)) > 765:
        ss -= 1
    d.text((214, y + 102), line, font=F(ss, False), fill=SUB)
SRC = "Sources: Forbes, Tom's Guide, Democracy Now, Euronews, Just Security"
fs = 20
while d.textlength(SRC, font=F(fs, False)) > W - 40:
    fs -= 1
d.text((20, H - 30), SRC, font=F(fs, False), fill=SUB)
img.save("entry.png", optimize=True)
print(os.path.getsize("entry.png"), img.size)
