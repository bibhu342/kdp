"""Dino Trucks Scissor Skills — interior builder (code-made, 0 image credits).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
Levels: straight, zigzag, wavy, mixed paths, shapes, dino-truck cut-outs (dashed outline traced from the art).
Pictures reuse the Dino Trucks clean art in ../../03-dino-trucks-mazes/art/. Single-sided pages (for cutting).
"""
import os, math, random
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', '..', '03-dino-trucks-mazes', 'art')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
for n, f in [('Lucky', 'LuckiestGuy'), ('Fred', 'Fredoka-SemiBold'), ('FredR', 'Fredoka-Regular')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, f + '.ttf')))
W, H = 612, 792
M = 43
DASH = (9, 6)

_art = {}
def art(i):
    i = (i - 1) % 25 + 1
    if i not in _art: _art[i] = Image.open(os.path.join(ART, f'{i:02d}.png')).convert('L')
    return _art[i]


def dashed(c, pts, w=2.2):
    c.setDash(*DASH); c.setLineWidth(w); c.setStrokeColor(black)
    p = c.beginPath(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; c.drawPath(p, stroke=1, fill=0); c.setDash()


def scissors(c, x, y, s=16):
    """Simple scissors icon pointing right at (x, y)."""
    c.setLineWidth(1.6); c.circle(x - s * .55, y + s * .32, s * .26); c.circle(x - s * .55, y - s * .32, s * .26)
    c.line(x - s * .35, y + s * .2, x + s * .55, y - s * .12); c.line(x - s * .35, y - s * .2, x + s * .55, y + s * .12)


def path(kind, x0, x1, y, amp, rng):
    n = 220; xs = np.linspace(x0, x1, n); L = x1 - x0
    if kind == 'straight': ys = np.full(n, y)
    elif kind == 'zigzag':
        per = L / rng.choice([6, 7, 8]); t = (xs - x0) / per; ys = y + amp * (2 * np.abs(2 * (t - np.floor(t + .5))) - 1)
    elif kind == 'wavy':
        per = L / rng.choice([3, 4, 5]); ys = y + amp * np.sin(2 * math.pi * (xs - x0) / per)
    elif kind == 'steps':
        per = L / 6; ys = y + amp * np.where(np.floor((xs - x0) / per) % 2 == 0, 1, -1)
        pts = []
        k = 0
        while x0 + k * per < x1:
            yy = y + (amp if k % 2 == 0 else -amp); pts += [(x0 + k * per, yy), (min(x0 + (k + 1) * per, x1), yy)]; k += 1
        return pts
    elif kind == 'spikes':
        per = L / 9; t = (xs - x0) / per; ys = y + amp * (np.abs(np.sin(math.pi * t)) * 2 - 1)
    elif kind == 'loops':
        per = L / 5; th = np.linspace(0, 5 * 2 * math.pi, 600)
        return [(x0 + per * tt / (2 * math.pi) + per * .32 * math.sin(tt), y + amp * math.cos(tt)) for tt in th]
    return list(zip(xs, ys))


def strips_page(c, kinds, title, sub, art_i, rng, n=5):
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 40, title)
    c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 64, sub)
    top = H - M - 90; bot = M + 20; band = (top - bot) / n
    for k in range(n):
        yc = top - band * (k + .5)
        if k: c.setLineWidth(.6); c.setStrokeGray(.75); c.line(M, top - band * k, W - M, top - band * k); c.setStrokeGray(0)
        img = art(art_i + k); iw, ih = img.size; s = min(band * .78 / ih, 95 / iw)
        c.drawImage(ImageReader(img), W - M - iw * s, yc - ih * s / 2, iw * s, ih * s, mask='auto')
        kind = kinds[k % len(kinds)]
        x0 = M + 34; x1 = W - M - 110
        scissors(c, M + 14, yc)
        dashed(c, path(kind, x0, x1, yc, band * .26, rng))


def shape_page(c, name, i):
    c.setFont('Lucky', 38); c.drawCentredString(W / 2, H - M - 44, f'CUT THE {name}')
    c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 70, 'Cut along the dashed line. Go slowly!')
    cx, cy, s = W / 2, H / 2 - 10, 205
    if name == 'CIRCLE': pts = [(cx + s * math.cos(t), cy + s * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 300)]
    elif name == 'SQUARE': pts = [(cx - s * .85, cy - s * .85), (cx + s * .85, cy - s * .85), (cx + s * .85, cy + s * .85), (cx - s * .85, cy + s * .85), (cx - s * .85, cy - s * .85)]
    elif name == 'TRIANGLE': pts = [(cx - s, cy - s * .8), (cx + s, cy - s * .8), (cx, cy + s * .95), (cx - s, cy - s * .8)]
    elif name == 'STAR': pts = [(cx + (s if k % 2 == 0 else s * .45) * math.cos(math.pi / 2 + k * math.pi / 5), cy + (s if k % 2 == 0 else s * .45) * math.sin(math.pi / 2 + k * math.pi / 5)) for k in range(11)]
    elif name == 'HEART':
        pts = []
        for t in np.linspace(0, 2 * math.pi, 300):
            x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((cx + x / 17 * s, cy + y / 17 * s + s * .08))
    elif name == 'DIAMOND': pts = [(cx, cy - s), (cx + s * .72, cy), (cx, cy + s), (cx - s * .72, cy), (cx, cy - s)]
    elif name == 'OVAL': pts = [(cx + s * .72 * math.cos(t), cy + s * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 300)]
    elif name == 'HEXAGON': pts = [(cx + s * math.cos(math.pi / 6 + k * math.pi / 3), cy + s * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(7)]
    dashed(c, pts, 2.6); scissors(c, pts[0][0] - 18, pts[0][1] + 4)
    img = art(i); iw, ih = img.size; sc = 105 / ih
    c.drawImage(ImageReader(img), W - M - iw * sc, M, iw * sc, 105, mask='auto')


def cutout_page(c, i):
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 40, 'CUT OUT THE DINO TRUCK')
    c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 64, 'Color it first, then cut along the dashed line!')
    img = art(i); a = np.array(img) < 140
    # silhouette: close gaps, fill holes, then pad outward ~0.18 in
    sil = ndimage.binary_closing(a, iterations=6); sil = ndimage.binary_fill_holes(sil)
    lab, n = ndimage.label(sil)
    if n > 1: sil = lab == (np.argmax(ndimage.sum(sil, lab, range(1, n + 1))) + 1)
    sil = ndimage.binary_fill_holes(sil)
    box_w, box_h = W - 2 * M - 110, H - 2 * M - 190
    s = min(box_w / img.width, box_h / img.height)       # pt per px
    pad = int(0.18 * 72 / s)
    sil = ndimage.binary_dilation(sil, iterations=pad)
    sil = ndimage.binary_opening(sil, iterations=pad // 2)  # smooth spiky bits for little hands
    big = np.pad(sil, 2)
    cont = max(measure.find_contours(big.astype(float), .5), key=len)
    iw, ih = img.width * s, img.height * s
    ox, oy = (W - iw) / 2, M + 60 + (box_h - ih) / 2
    pts = [(ox + (x - 2) * s, oy + ih - (y - 2) * s) for y, x in cont[::3]]
    # keep cut line inside the page
    pts = [(min(max(x, M + 4), W - M - 4), min(max(y, M + 4), H - M - 90)) for x, y in pts]
    pts.append(pts[0])
    clean = Image.fromarray(np.where(sil, np.array(img), 255).astype(np.uint8))  # hide background outside the cut line
    c.drawImage(ImageReader(clean), ox, oy, iw, ih, mask='auto')
    dashed(c, pts, 2.4); scissors(c, pts[0][0] - 16, pts[0][1])


def belongs(c):
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 170, 'THIS BOOK'); c.drawCentredString(W / 2, H - 218, 'BELONGS TO')
    c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    img = art(13); iw, ih = img.size; s = 330 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 110, iw * s, ih * s, mask='auto')


def safety(c):
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 44, 'SCISSOR SAFETY')
    c.setFont('FredR', 16)
    tips = ['Use child-safe scissors with a grown-up nearby.', 'Sit down at a table to cut.', 'Hold the scissors with your thumb on top.',
            'Turn the paper, not the scissors.', 'Walk with scissors closed, pointing down.', 'Cut slowly along the dashed line.',
            'Each page is printed on one side only,', 'so you can cut it out without losing the next page.']
    for k, t in enumerate(tips): c.drawCentredString(W / 2, H - M - 110 - k * 32, t)
    c.setFont('Lucky', 22); c.drawCentredString(W / 2, 260, 'PRACTICE: SNIP THE LITTLE LINES')
    for k in range(6):
        x = M + 50 + k * 85; c.setLineWidth(.8); c.rect(x - 22, 120, 44, 110); dashed(c, [(x, 120), (x, 230)])


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 46); c.drawCentredString(W / 2, H - 215, 'SUPER'); c.drawCentredString(W / 2, H - 268, 'SCISSOR STAR')
    c.setFont('FredR', 16); c.drawCentredString(W / 2, H - 330, 'This award goes to'); c.line(140, H - 390, W - 140, H - 390)
    c.drawCentredString(W / 2, H - 430, 'for cutting every line, shape and dino truck!')
    img = art(11); iw, ih = img.size; s = 230 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 130, iw * s, ih * s, mask='auto')


def build():
    rng = random.Random(42)
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Trucks Scissor Skills'); c.setAuthor('Bibhu Behera')
    belongs(c); c.showPage(); safety(c); c.showPage()
    acts = 0; a = 1
    def page_done():
        nonlocal acts; acts += 1; c.showPage(); c.showPage()   # single-sided: blank back
    levels = [('LEVEL 1: STRAIGHT LINES', 'Cut along the dashed lines to help the dino trucks!', ['straight'], 6),
              ('LEVEL 2: ZIGZAGS', 'Cut the zigzag roads!', ['zigzag'], 6),
              ('LEVEL 3: WAVY LINES', 'Cut along the wavy paths!', ['wavy'], 6),
              ('LEVEL 4: TRICKY PATHS', 'Steps, spikes and curves: go slowly!', ['steps', 'spikes', 'wavy', 'zigzag', 'steps'], 6)]
    for title, sub, kinds, npages in levels:
        for p in range(npages):
            ks = kinds[p % len(kinds):] + kinds[:p % len(kinds)]
            strips_page(c, ks, title, sub, a, rng, n=5 if 'loops' not in ks[:5] else 5); a += 5; page_done()
    for s in ['CIRCLE', 'SQUARE', 'TRIANGLE', 'HEART', 'STAR', 'DIAMOND', 'OVAL', 'HEXAGON']:
        shape_page(c, s, a); a += 1; page_done()
    for i in range(1, 13):
        cutout_page(c, i * 2 - 1); page_done()
    certificate(c); c.showPage(); c.showPage()
    c.save(); print('activities', acts, 'pages', 2 + 2 * acts + 2)


if __name__ == '__main__':
    build()
