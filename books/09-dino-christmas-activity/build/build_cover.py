"""Dino Christmas Activity Book — full wraparound cover (series layout, coloured Christmas page as hero) (series look from the Maze Book) (300 DPI) -> ../final/cover.pdf + cover_preview.png
Needs: ../../03-dino-trucks-mazes/art/front-color-13.png (mascot, mirrored), thumbnails thN.png in THUMBS dir.
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
THUMBS = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0'
PAGES = 92
DPI = 300
BLEED = 0.125
spine = PAGES * 0.002252
Win = BLEED * 2 + 8.5 * 2 + spine
Hin = 11 + BLEED * 2
W, H = round(Win * DPI), round(Hin * DPI)
X_SPINE0 = round((BLEED + 8.5) * DPI)
X_FRONT = round((BLEED + 8.5 + spine) * DPI)
FW = W - X_FRONT
LUCKY = os.path.join(HERE, 'LuckiestGuy.ttf')
FRED = os.path.join(HERE, 'Fredoka.ttf')
SKY1, SKY2 = (190, 20, 40), (235, 70, 80)
RED, YEL, ORG, PUR, CREAM, GRN = (229, 57, 53), (255, 214, 64), (255, 140, 26), (123, 77, 220), (255, 244, 214), (124, 179, 66)


def fred(sz, w='Bold'):
    f = ImageFont.truetype(FRED, sz); f.set_variation_by_name(w); return f


def outlined(d, xy, text, font, fill, stroke=(40, 30, 30), sw=14, anchor='mm', shadow=True):
    x, y = xy
    if shadow:
        d.text((x + 10, y + 12), text, font=font, fill=(30, 30, 60), anchor=anchor, stroke_width=sw, stroke_fill=(30, 30, 60))
    d.text((x, y), text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)


def maze_pattern(w, h, cell, rng):
    cols, rows = w // cell + 1, h // cell + 1
    opened = [[set() for _ in range(cols)] for _ in range(rows)]
    seen = [[False] * cols for _ in range(rows)]
    st = [(0, 0)]; seen[0][0] = True
    D = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}; O = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}
    while st:
        r, c = st[-1]
        nb = [(k, r + a, c + b) for k, (a, b) in D.items() if 0 <= r + a < rows and 0 <= c + b < cols and not seen[r + a][c + b]]
        if not nb: st.pop(); continue
        k, nr, nc = rng.choice(nb); opened[r][c].add(k); opened[nr][nc].add(O[k]); seen[nr][nc] = True; st.append((nr, nc))
    img = Image.new('L', (w, h), 0); d = ImageDraw.Draw(img)
    for r in range(rows):
        for c in range(cols):
            x, y = c * cell, r * cell
            if 'E' not in opened[r][c]: d.line([(x + cell, y), (x + cell, y + cell)], fill=255, width=16)
            if 'S' not in opened[r][c]: d.line([(x, y + cell), (x + cell, y + cell)], fill=255, width=16)
    return img


def build():
    rng = random.Random(7)
    cov = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(cov)
    # ---------- FRONT ----------
    front = Image.new('RGB', (FW, H), SKY1)
    fd = ImageDraw.Draw(front)
    for y in range(H):
        t = y / H; fd.line([(0, y), (FW, y)], fill=tuple(int(SKY1[i] + (SKY2[i] - SKY1[i]) * t) for i in range(3)))
    # sunburst
    cx, cy = FW // 2, int(H * 0.55)
    rays = Image.new('L', (FW, H), 0); rd = ImageDraw.Draw(rays)
    for k in range(24):
        a0 = k * 2 * math.pi / 24; a1 = a0 + math.pi / 24
        rd.polygon([(cx, cy), (cx + 6000 * math.cos(a0), cy + 6000 * math.sin(a0)), (cx + 6000 * math.cos(a1), cy + 6000 * math.sin(a1))], fill=40)
    front.paste((255, 255, 255), (0, 0), rays)
    # snow
    lg = Image.new('L', (FW, H), 0); ld = ImageDraw.Draw(lg)
    for _ in range(420):
        x, y, r_ = rng.randrange(FW), rng.randrange(H - 330), rng.randrange(8, 26); ld.ellipse([x - r_, y - r_, x + r_, y + r_], fill=rng.randrange(90, 200))
    front.paste((255, 255, 255), (0, 0), lg)
    # ground
    fd.rectangle([0, H - 330, FW, H], fill=(250, 250, 255))
    fd.rectangle([0, H - 330, FW, H - 310], fill=(215, 225, 240))
    # hero: auto-coloured Christmas page on a white card
    art = Image.open(os.path.join(HERE, '..', 'work', 'cover_page_coloured.png')).convert('RGB')
    s_ = 1330 / art.height; art = art.resize((int(art.width * s_), 1330), Image.LANCZOS)
    cx_, top_ = FW // 2, 1600
    card = [cx_ - art.width // 2 - 50, top_ - 50, cx_ + art.width // 2 + 50, top_ + art.height + 50]
    fd.rounded_rectangle([card[0] + 24, card[1] + 30, card[2] + 24, card[3] + 30], 60, fill=(110, 10, 25))
    fd.rounded_rectangle(card, 60, fill=(255, 255, 255), outline=(40, 30, 30), width=12)
    front.paste(art, (cx_ - art.width // 2, top_))
    # title
    fd = ImageDraw.Draw(front)
    outlined(fd, (FW // 2, 470), 'DINO TRUCKS', ImageFont.truetype(LUCKY, 410), YEL, sw=18)
    # ribbon
    rb = [FW // 2 - 1250, 690, FW // 2 + 1250, 960]
    fd.rounded_rectangle([rb[0] + 14, rb[1] + 16, rb[2] + 14, rb[3] + 16], 40, fill=(30, 30, 60))
    fd.rounded_rectangle(rb, 40, fill=(0, 140, 80), outline=(40, 30, 30), width=14)
    outlined(fd, (FW // 2, 828), 'CHRISTMAS ACTIVITY BOOK', ImageFont.truetype(LUCKY, 135), (255, 255, 255), sw=10, shadow=False)
    # badges
    def badge(c, col, l1, l2):
        r = 260
        fd.ellipse([c[0] - r + 12, c[1] - r + 14, c[0] + r + 12, c[1] + r + 14], fill=(30, 30, 60))
        fd.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=col, outline=(40, 30, 30), width=12)
        outlined(fd, (c[0], c[1] - 70), l1, ImageFont.truetype(LUCKY, 120), (255, 255, 255), sw=8, shadow=False)
        outlined(fd, (c[0], c[1] + 75), l2, ImageFont.truetype(LUCKY, 170), (255, 255, 255), sw=8, shadow=False)
    badge((420, 1250), (0, 140, 80), 'AGES', '4-8')
    badge((FW - 420, 1250), (255, 170, 0), '42', 'IN 1')
    fd.text((FW // 2, H - 170), 'Bibhu Behera', font=fred(120, 'SemiBold'), fill=(190, 20, 40), anchor='mm',
            stroke_width=4, stroke_fill=(255, 255, 255))
    cov.paste(front, (X_FRONT, 0))
    # ---------- SPINE ----------
    d.rectangle([X_SPINE0, 0, X_FRONT, H], fill=(190, 20, 40))
    # ---------- BACK ----------
    BX0 = round(BLEED * DPI) + 120; BW = X_SPINE0 - BX0 - 160
    bc = BX0 + BW // 2
    outlined(d, (bc, 380), 'HO HO HONK!', ImageFont.truetype(LUCKY, 190), RED, sw=12)
    blurb = ['A whole Christmas of dino fun: coloring pages,',
             'mazes, word searches and dot marker pages starring',
             'dinosaurs, trucks, Santa\'s sleigh and the toy workshop.']
    for i, t in enumerate(blurb):
        d.text((bc, 640 + i * 95), t, font=fred(76, 'Medium'), fill=(60, 50, 50), anchor='mm')
    # thumbnails
    tw = 700
    for i, p in enumerate([5, 7, 9]):
        t = Image.open(os.path.join(THUMBS, f'th{p}.png')).convert('RGB')
        t = t.resize((tw, int(t.height * tw / t.width)), Image.LANCZOS)
        fr = Image.new('RGB', (t.width + 24, t.height + 24), (60, 50, 50)); fr.paste(t, (12, 12))
        x = bc - (3 * fr.width + 2 * 70) // 2 + i * (fr.width + 70); y = 920
        d.rectangle([x + 18, y + 22, x + fr.width + 18, y + fr.height + 22], fill=(200, 185, 150))
        cov.paste(fr, (x, y))
    bullets = ['42 activities: coloring, mazes, word search, dots',
               'Answers at the back, plus a champion certificate',
               'Single-sided activity pages: no bleed-through',
               'Large 8.5 x 11 inch pages, ages 4-8']
    by = 2140
    for i, t in enumerate(bullets):
        d.ellipse([BX0 + 40, by + i * 110 - 18, BX0 + 76, by + i * 110 + 18], fill=ORG)
        d.text((BX0 + 110, by + i * 110), t, font=fred(74, 'SemiBold'), fill=(60, 50, 50), anchor='lm')
    d.text((BX0 + 40, H - 300), 'Dino Doodle Press', font=fred(84, 'Bold'), fill=RED, anchor='lm')
    out = os.path.join(HERE, '..', 'final')
    cov.save(os.path.join(out, 'cover.pdf'), resolution=DPI)
    cov.resize((W // 5, H // 5), Image.LANCZOS).save(os.path.join(out, 'cover_preview.png'))
    print('cover', W, H, 'spine in', round(spine, 4))


if __name__ == '__main__':
    build()
