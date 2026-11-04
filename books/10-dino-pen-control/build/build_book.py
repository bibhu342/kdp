"""Dino Trucks Pen Control — pre-writing tracing workbook (code-made, 0 image credits).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
Reuses the Book 08 path generator; lines are dotted grey to trace from a start dot to a dino truck picture.
Pencil/crayon book: pages are double-sided.
"""
import os, sys, math, random
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, Color

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', '08-dino-scissor-skills', 'build', 'build_book.py')
ss = type(sys)('ss'); ss.__file__ = SRC; exec(compile(open(SRC).read(), SRC, 'exec'), ss.__dict__)
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
W, H, M = 612, 792, 43
TRACE = Color(0.6, 0.6, 0.6)


def dotted(c, pts, w=4):
    c.setStrokeColor(TRACE); c.setLineWidth(w); c.setLineCap(1); c.setDash(0.1, 9)
    p = c.beginPath(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; c.drawPath(p, stroke=1, fill=0)
    c.setDash(); c.setLineCap(0); c.setStrokeColor(black)


def start(c, x, y):
    c.setFillColor(black); c.circle(x, y, 6, stroke=0, fill=1)


def head(c, title, sub):
    c.setFont('Lucky', 32); c.drawCentredString(W / 2, H - M - 40, title)
    c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 64, sub)
    c.setFont('FredR', 10); c.drawString(M, M - 14 + 10, 'Name: ____________________')


def strips(c, kinds, title, sub, a, rng, n=5):
    head(c, title, sub)
    top = H - M - 86; bot = M + 16; band = (top - bot) / n
    for k in range(n):
        yc = top - band * (k + .5)
        img = ss.art(a + k); iw, ih = img.size; s = min(band * .8 / ih, 90 / iw)
        c.drawImage(ImageReader(img), W - M - iw * s, yc - ih * s / 2, iw * s, ih * s, mask='auto')
        x0, x1 = M + 26, W - M - 104
        start(c, x0 - 10, yc if kinds[k % len(kinds)] != 'steps' else yc + band * .26)
        dotted(c, ss.path(kinds[k % len(kinds)], x0, x1, yc, band * .26, rng))


def vertical(c, kind, title, a, rng):
    head(c, title, 'Start at the dot and trace down to the picture!')
    top = H - M - 100; bot = M + 120; n = 4; colw = (W - 2 * M) / n
    for k in range(n):
        xc = M + colw * (k + .5)
        pts = ss.path(kind, bot, top, xc, colw * .22, rng)           # build horizontally, then rotate
        pts = [(xc + (y - xc), x) for x, y in pts][::-1]
        start(c, pts[0][0], pts[0][1] + 10); dotted(c, pts)
        img = ss.art(a + k); iw, ih = img.size; s = min(90 / ih, colw * .9 / iw)
        c.drawImage(ImageReader(img), xc - iw * s / 2, M + 20, iw * s, ih * s, mask='auto')


def shapes(c, name, a):
    head(c, f'TRACE THE {name}S', 'Trace each shape. The first one shows you how!')
    for k in range(6):
        cx = M + 130 + (k % 2) * 270; cy = H - M - 190 - (k // 2) * 205; s = 78
        if name == 'CIRCLE': pts = [(cx + s * math.cos(t), cy + s * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 120)]
        elif name == 'SQUARE': pts = [(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s), (cx - s, cy - s)]
        elif name == 'TRIANGLE': pts = [(cx - s, cy - s * .8), (cx + s, cy - s * .8), (cx, cy + s * .95), (cx - s, cy - s * .8)]
        elif name == 'STAR': pts = [(cx + (s if j % 2 == 0 else s * .45) * math.cos(math.pi / 2 + j * math.pi / 5), cy + (s if j % 2 == 0 else s * .45) * math.sin(math.pi / 2 + j * math.pi / 5)) for j in range(11)]
        elif name == 'HEART':
            pts = [(cx + 16 * math.sin(t) ** 3 / 17 * s, cy + (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 * s + s * .08) for t in np.linspace(0, 2 * math.pi, 160)]
        elif name == 'DIAMOND': pts = [(cx, cy - s), (cx + s * .72, cy), (cx, cy + s), (cx - s * .72, cy), (cx, cy - s)]
        if k == 0:
            c.setLineWidth(4); p = c.beginPath(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; c.drawPath(p, stroke=1, fill=0)
        else:
            dotted(c, pts); start(c, *pts[0])


def spiral(c, a, inward):
    head(c, 'SNAIL SPIRAL' if inward else 'TORNADO SPIRAL', 'Go round and round, slowly!')
    cx, cy = W / 2, H / 2 - 20; turns = 4.5
    th = np.linspace(0, turns * 2 * math.pi, 900); r = 15 + 200 * th / th[-1]
    pts = [(cx + rr * math.cos(t), cy + rr * math.sin(t)) for t, rr in zip(th, r)]
    if not inward: pts = pts[::-1]
    start(c, *pts[0]); dotted(c, pts)
    img = ss.art(a); iw, ih = img.size; s = 100 / ih
    c.drawImage(ImageReader(img), W - M - iw * s, M, iw * s, 100, mask='auto')


def front(c):
    ss.belongs(c); c.showPage()
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 44, 'TIPS FOR GROWN-UPS')
    c.setFont('FredR', 16)
    tips = ['Use a pencil or a chunky crayon.', 'Hold it like a little bird: gently, not squeezing.', 'Start at the big black dot every time.',
            'Go slowly and stay on the dotted line.', 'It is fine to go off the line! Praise trying.', 'Do 2 or 3 pages a day, little and often.',
            'Lines go left to right and top to bottom,', 'the same way kids will learn to write.']
    for k, t in enumerate(tips): c.drawCentredString(W / 2, H - M - 110 - k * 32, t)
    img = ss.art(13); iw, ih = img.size; s = 250 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, M + 20, iw * s, 250, mask='auto'); c.showPage()


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 46); c.drawCentredString(W / 2, H - 215, 'PENCIL'); c.drawCentredString(W / 2, H - 268, 'PRO')
    c.setFont('FredR', 16); c.drawCentredString(W / 2, H - 330, 'This award goes to'); c.line(140, H - 390, W - 140, H - 390)
    c.drawCentredString(W / 2, H - 430, 'for tracing every line, curve and shape!')
    img = ss.art(11); iw, ih = img.size; s = 230 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 130, iw * s, ih * s, mask='auto')


def build():
    rng = random.Random(77)
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Trucks Pen Control'); c.setAuthor('Bibhu Behera')
    front(c); a = 1; pages = 0
    plan = [('LEVEL 1: STRAIGHT LINES', 'Trace from the dot to the dino truck!', ['straight'], 10),
            ('LEVEL 2: WAVES', 'Trace the wavy roads!', ['wavy'], 10),
            ('LEVEL 3: ZIGZAGS', 'Up and down the mountains!', ['zigzag'], 10),
            ('LEVEL 4: BUMPS AND STEPS', 'Bumpy roads and building blocks!', ['spikes', 'steps'], 10),
            ('LEVEL 5: LOOPS', 'Loop-de-loop like a race car!', ['loops'], 8),
            ('LEVEL 6: MIXED PATHS', 'Every road is different!', ['wavy', 'zigzag', 'steps', 'spikes', 'loops'], 10)]
    for title, sub, kinds, n in plan:
        for p in range(n):
            ks = kinds[p % len(kinds):] + kinds[:p % len(kinds)]
            strips(c, ks, title, sub, a, rng); a += 5; c.showPage(); pages += 1
        if title.startswith('LEVEL 3') or title.startswith('LEVEL 5'):
            for kind in ['straight', 'wavy', 'zigzag']:
                vertical(c, kind, 'TOP TO BOTTOM', a, rng); a += 4; c.showPage(); pages += 1
    for s in ['CIRCLE', 'SQUARE', 'TRIANGLE', 'HEART', 'STAR', 'DIAMOND']:
        shapes(c, s, a); c.showPage(); pages += 1
    for k in range(4): spiral(c, a + k, k % 2 == 0); c.showPage(); pages += 1
    certificate(c); c.showPage()
    total = 2 + pages + 1
    if total % 2: c.showPage(); total += 1
    c.save(); print('activity pages', pages, 'total', total)


if __name__ == '__main__':
    build()
