"""Dino Trucks Dot Marker Book — interior builder (code-made, 0 image credits).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
Big dot-marker circles are packed inside each shape/number/letter mask so every dot fits.
Pictures to color reuse the Dino Trucks clean art in ../../03-dino-trucks-mazes/art/.
Single-sided pages (dot markers bleed through paper).
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, black, white

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', '..', '03-dino-trucks-mazes', 'art')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
LUCKY = os.path.join(HERE, 'LuckiestGuy.ttf')
for n, f in [('Lucky', 'LuckiestGuy'), ('Fred', 'Fredoka-SemiBold'), ('FredR', 'Fredoka-Regular')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, f + '.ttf')))

W, H = 612, 792
M = 43
PX = 3                       # mask pixels per point
D = 54                       # dot diameter in pt (0.75 in, fits standard dot markers)
BOX = (M + 20, 150, W - M - 20, H - M - 95)   # area for the big shape: x0, y0, x1, y1 (pt)
GREY = Color(0.6, 0.6, 0.6)

SHAPES = ['CIRCLE', 'SQUARE', 'TRIANGLE', 'HEART', 'STAR', 'DIAMOND', 'OVAL', 'RECTANGLE']
WORDS = {'A': 'APPLE', 'B': 'BUS', 'C': 'CAR', 'D': 'DINO', 'E': 'EGG', 'F': 'FIRE TRUCK', 'G': 'GRAPES', 'H': 'HEART',
         'I': 'ICE CREAM', 'J': 'JEEP', 'K': 'KITE', 'L': 'LEAF', 'M': 'MOON', 'N': 'NEST', 'O': 'OCTOPUS', 'P': 'PLANE',
         'Q': 'QUEEN', 'R': 'ROCKET', 'S': 'SUN', 'T': 'T-REX', 'U': 'UMBRELLA', 'V': 'VOLCANO', 'W': 'WHEEL',
         'X': 'XYLOPHONE', 'Y': 'YO-YO', 'Z': 'ZEBRA'}


def shape_polys(name, x0, y0, x1, y1):
    """Return list of polygons (pt coords, y up) or ('ellipse', bbox)."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; s = min(x1 - x0, y1 - y0) / 2 * 0.95
    if name == 'CIRCLE': return ('ellipse', (cx - s, cy - s, cx + s, cy + s))
    if name == 'OVAL': return ('ellipse', (cx - s * 0.72, cy - s, cx + s * 0.72, cy + s))
    if name == 'SQUARE': return [[(cx - s * .85, cy - s * .85), (cx + s * .85, cy - s * .85), (cx + s * .85, cy + s * .85), (cx - s * .85, cy + s * .85)]]
    if name == 'RECTANGLE': return [[(cx - s, cy - s * .62), (cx + s, cy - s * .62), (cx + s, cy + s * .62), (cx - s, cy + s * .62)]]
    if name == 'TRIANGLE': return [[(cx - s, cy - s * .8), (cx + s, cy - s * .8), (cx, cy + s * .95)]]
    if name == 'DIAMOND': return [[(cx, cy - s), (cx + s * .72, cy), (cx, cy + s), (cx - s * .72, cy)]]
    if name == 'STAR':
        return [[(cx + (s if k % 2 == 0 else s * .45) * math.cos(math.pi / 2 + k * math.pi / 5),
                  cy - s * .05 + (s if k % 2 == 0 else s * .45) * math.sin(math.pi / 2 + k * math.pi / 5)) for k in range(10)]]
    if name == 'HEART':
        pts = []
        for k in range(200):
            t = 2 * math.pi * k / 200
            x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((cx + x / 17 * s, cy + y / 17 * s + s * .08))
        return [pts]


def mask_from(draw_fn):
    img = Image.new('L', (W * PX, H * PX), 0); draw_fn(ImageDraw.Draw(img)); return np.array(img) > 127


def to_px(x, y): return (x * PX, (H - y) * PX)


def shape_mask(name):
    sp = shape_polys(name, *BOX)
    def f(d):
        if sp[0] == 'ellipse':
            x0, y0, x1, y1 = sp[1]; d.ellipse([x0 * PX, (H - y1) * PX, x1 * PX, (H - y0) * PX], fill=255)
        else:
            for poly in sp: d.polygon([to_px(*p) for p in poly], fill=255)
    return mask_from(f), sp


def glyph_layout(ch):
    """Font size + baseline so the glyph fills BOX."""
    x0, y0, x1, y1 = BOX; size = 1000
    font = ImageFont.truetype(LUCKY, size); l, t, r, b = font.getbbox(ch)
    sc = min((x1 - x0) / (r - l), (y1 - y0) / (b - t)) * 0.97; size = size * sc
    font = ImageFont.truetype(LUCKY, int(size * PX)); l, t, r, b = font.getbbox(ch)
    gx = ((x0 + x1) / 2) * PX - (l + r) / 2; gy = ((H - (y0 + y1) / 2) * PX) - (t + b) / 2
    return font, gx, gy, size


def glyph_mask(ch):
    font, gx, gy, size = glyph_layout(ch)
    return mask_from(lambda d: d.text((gx, gy), ch, font=font, fill=255)), (font, gx, gy, size)


def pack(mask, d=D):
    """Hex-pack dots fully inside mask; try offsets, keep the densest. Returns centres in pt."""
    dist = ndimage.distance_transform_edt(mask) / PX
    r = d / 2; best = []
    for scale in (1.0, 0.86):                        # shrink dots a little for thin strokes
        rr = r * scale; step = 2 * rr * 1.08
        for ox in np.linspace(0, step, 4, endpoint=False):
            for oy in np.linspace(0, step * .866, 3, endpoint=False):
                pts = []
                y = oy; row = 0
                while y < H:
                    x = ox + (step / 2 if row % 2 else 0)
                    while x < W:
                        px, py = int(x * PX), int((H - y) * PX)
                        if 0 <= px < W * PX and 0 <= py < H * PX and dist[py, px] >= rr * 1.02: pts.append((x, y, rr))
                        x += step
                    y += step * .866; row += 1
                if len(pts) > len(best): best = pts
        if len(best) >= 6: break
    return best


def dots(c, pts):
    c.setStrokeColor(black); c.setLineWidth(1.6)
    for x, y, rr in pts: c.circle(x, y, rr, stroke=1, fill=0)


_art = {}
def art(i):
    if i not in _art: _art[i] = Image.open(os.path.join(ART, f'{(i - 1) % 25 + 1:02d}.png')).convert('L')
    return _art[i]


def picture(c, i, h=118):
    img = art(i); iw, ih = img.size; s = h / ih
    c.drawImage(ImageReader(img), W - M - iw * s, M, iw * s, h, mask='auto')


def header(c, big, small=None):
    c.setFont('Lucky', 44); c.drawCentredString(W / 2, H - M - 52, big)
    if small: c.setFont('Fred', 15); c.drawCentredString(W / 2, H - M - 78, small)


def shape_page(c, name, i):
    header(c, name, 'Dot every circle!')
    m, sp = shape_mask(name)
    c.setLineWidth(4); c.setStrokeColor(black)
    if sp[0] == 'ellipse':
        x0, y0, x1, y1 = sp[1]; c.ellipse(x0, y0, x1, y1, stroke=1, fill=0)
    else:
        for poly in sp:
            p = c.beginPath(); p.moveTo(*poly[0]); [p.lineTo(*q) for q in poly[1:]]; p.close(); c.drawPath(p, stroke=1, fill=0)
    dots(c, pack(m)); picture(c, i)
    c.setFont('FredR', 12); c.drawString(M + 4, M + 40, 'Trace the shape with your finger,'); c.drawString(M + 4, M + 24, 'then color the dino truck picture!')


def glyph_outline(c, ch, lay):
    font, gx, gy, size = lay
    # reportlab text in stroke mode, positioned to match the PIL mask
    fsize = size; l, t, r, b = ImageFont.truetype(LUCKY, int(size * PX)).getbbox(ch)
    width = pdfmetrics.stringWidth(ch, 'Lucky', fsize)
    asc_px = ImageFont.truetype(LUCKY, int(size * PX)).getmetrics()[0]
    x = gx / PX; y = H - (gy + asc_px) / PX
    t_ = c.beginText(); t_.setTextRenderMode(1); t_.setFont('Lucky', fsize); t_.setTextOrigin(x, y); t_.textOut(ch)
    c.setLineWidth(3.5); c.setStrokeColor(black); c.drawText(t_)


def number_page(c, n, i):
    header(c, f'NUMBER {n}', f'Dot the number {n}, then dot {n} circle{"s" if n > 1 else ""} below!')
    m, lay = glyph_mask(str(n)); glyph_outline(c, str(n), lay); dots(c, pack(m))
    # counting row: up to 5 per row, left of the picture
    rr = 20
    for k in range(n):
        c.setLineWidth(1.6); c.circle(M + 30 + (k % 5) * 54, M + 84 - (k // 5) * 50, rr, stroke=1, fill=0)
    picture(c, i, 100)


def letter_page(c, ch, i):
    header(c, f'{ch} is for {WORDS[ch]}', 'Dot every circle on the letter!')
    m, lay = glyph_mask(ch); glyph_outline(c, ch, lay); dots(c, pack(m)); picture(c, i)
    c.setFont('FredR', 12); c.drawString(M + 4, M + 40, f'Say it: "{ch}... {WORDS[ch].lower()}!"'); c.drawString(M + 4, M + 24, 'Then color the dino truck picture.')


def belongs(c):
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 170, 'THIS BOOK'); c.drawCentredString(W / 2, H - 218, 'BELONGS TO')
    c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    img = art(13); iw, ih = img.size; s = 330 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 110, iw * s, ih * s, mask='auto')


def how_to(c):
    header(c, 'HOW TO USE THIS BOOK')
    c.setFont('FredR', 16)
    tips = ['Use washable dot markers (bingo daubers),', 'or stickers, crayons or finger paint.',
            'Press one dot inside each circle.', 'Say the shape, number or letter out loud.',
            'Every picture page is single-sided,', 'so markers will not ruin the next page.',
            'Grown-ups: put a sheet of card behind the page.']
    for k, t in enumerate(tips): c.drawCentredString(W / 2, H - M - 130 - k * 30, t)
    c.setFont('Lucky', 24); c.drawCentredString(W / 2, 330, 'PRACTICE DOTS')
    for k in range(5): c.setLineWidth(1.6); c.circle(W / 2 - 160 + k * 80, 260, D / 2, stroke=1, fill=0)


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 46); c.drawCentredString(W / 2, H - 215, 'DOT MARKER'); c.drawCentredString(W / 2, H - 268, 'SUPERSTAR')
    c.setFont('FredR', 16); c.drawCentredString(W / 2, H - 330, 'This award goes to'); c.line(140, H - 390, W - 140, H - 390)
    c.drawCentredString(W / 2, H - 430, 'for dotting every shape, number and letter!')
    img = art(11); iw, ih = img.size; s = 230 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 130, iw * s, ih * s, mask='auto')


def build():
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Trucks Dot Marker Book'); c.setAuthor('Bibhu Behera')
    belongs(c); c.showPage(); how_to(c); c.showPage()
    i = 0; counts = []
    def blank(): c.showPage()                       # blank back (single-sided)
    for s in SHAPES: i += 1; shape_page(c, s, i); c.showPage(); blank()
    for n in range(1, 11): i += 1; number_page(c, n, i); c.showPage(); blank()
    for ch in WORDS: i += 1; letter_page(c, ch, i); c.showPage(); blank()
    certificate(c); c.showPage(); blank()
    c.save(); print('activity pages', i, 'total pages', 2 + 2 * i + 2)


if __name__ == '__main__':
    build()
