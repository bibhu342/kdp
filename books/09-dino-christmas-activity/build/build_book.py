"""Dino Christmas Activity Book — interior builder (code-made, 0 image credits).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf (+ ../work/ cleaned art, cover image)
Reuses: Book 05 Christmas pages (source/raw) + cleaning, Book 03 maze generator, Book 06 word search, Book 07 dot packing.
Activity pages are single-sided (markers/crayons); answers and front matter are not.
"""
import os, sys, random, importlib.util
from collections import deque
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, '..', '..')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
WORK = os.path.join(HERE, '..', 'work'); os.makedirs(os.path.join(WORK, 'clean'), exist_ok=True)


def load(name, rel, patch=None):
    path = os.path.join(BOOKS, rel); src = open(path).read()
    for a, b in (patch or []): src = src.replace(a, b)
    mod = type(sys)(name); mod.__file__ = path; exec(compile(src, path, 'exec'), mod.__dict__); return mod


FONTS = os.path.join(HERE)
ws = load('ws', '06-dino-trucks-word-search/build/build_book.py')
dm = load('dm', '07-dino-dot-marker/build/build_book.py')
xm = load('xm', '05-dino-christmas-trucks/build/build_book.py')
mz = load('mz', '03-dino-trucks-mazes/build/build_book.py', [
    ("'/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'", repr(os.path.join(HERE, 'Fredoka-Regular.ttf'))),
    ("'/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'", repr(os.path.join(HERE, 'Fredoka-SemiBold.ttf')))])
W, H, M = 612, 792, 43

RAW = os.path.join(BOOKS, '05-dino-christmas-trucks', 'source', 'raw')
MANIFEST = os.path.join(BOOKS, '05-dino-christmas-trucks', 'source', 'higgsfield_urls.txt')
NUM2FILE = {int(n): os.path.join(RAW, os.path.basename(u)) for n, u in (l.split() for l in open(MANIFEST))}
COLOR_PAGES = [7, 11, 1, 21, 47, 2, 20, 14, 43, 25, 31, 50]          # full-page coloring
SMALL_ART = [3, 4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37]

_clean = {}
def clean(n):
    if n not in _clean:
        p = os.path.join(WORK, 'clean', f'{n:02d}.png')
        if not os.path.exists(p): xm.clean(NUM2FILE[n])[0].save(p)
        _clean[n] = Image.open(p).convert('L')
    return _clean[n]

def small(n, h=140):
    im = clean(n); return im.resize((int(im.width * h * 3 / im.height), h * 3), Image.LANCZOS)


XMAS_WS = [
 ('Santa\'s Sleigh', 'SANTA SLEIGH REINDEER GIFTS SACK BELLS ROOF CHIMNEY NIGHT FLY STARS SNOW'),
 ('Christmas Tree', 'TREE STAR LIGHTS ORNAMENT TINSEL BALLS PINE GARLAND BOW GIFT ANGEL TOP'),
 ('Snow Day', 'SNOW SLED SNOWMAN MITTENS SCARF BOOTS ICE COLD HAT SKATE FROST FLAKE'),
 ('Holiday Treats', 'COOKIE CANDY CANE COCOA PIE CAKE FUDGE MILK GINGER SUGAR TREAT JAM'),
 ('Toy Workshop', 'ELF TOYS HAMMER PAINT TRAIN DOLL BLOCKS ROBOT BALL KITE DRUM WRAP'),
 ('Dino Christmas', 'TREX DINO ROAR CLAW TAIL EGG HORNS SPIKES STOMP CHOMP HAT JOLLY'),
 ('Holiday Trucks', 'TRUCK PLOW TRAIN BUS CRANE TRACTOR VAN DUMP MIXER WHEELS ROAD SALT'),
 ('Winter Animals', 'OWL FOX BEAR DEER PENGUIN SEAL RABBIT MOOSE ROBIN WOLF HARE ORCA'),
 ('Christmas Eve', 'STOCKING FIRE CHIMNEY BED DREAM MOON WAIT HUSH SLEEP MILK NOTE PAJAMAS'),
 ('Decorations', 'WREATH LIGHTS STAR BOW RIBBON CANDLE HOLLY BELL TINSEL GARLAND LAMP RED'),
 ('Gifts', 'GIFT BOX BOW WRAP TAG RIBBON PAPER SURPRISE SHARE GIVE THANKS OPEN'),
 ('Merry Words', 'MERRY JOLLY HAPPY CHEER JOY PEACE LOVE KIND FAMILY FRIENDS SMILE HUG'),
]
DOT_SHAPES = [('STAR', 'STAR'), ('TREE', 'TRIANGLE'), ('ORNAMENT', 'CIRCLE'), ('HEART', 'HEART'), ('GIFT BOX', 'SQUARE'), ('CANDY', 'DIAMOND')]
MAZE_CAPS = ['Help the dino deliver the presents!', 'Drive the snowplough to the town!', 'Get the train to the North Pole!',
             'Find the way to the Christmas tree!', 'Help the elf reach the workshop!', 'Bring the cocoa truck home!',
             'Guide the sleigh to the chimney!', 'Carry the tree to the house!', 'Skate across the frozen pond!',
             'Deliver the mail before Christmas!', 'Find the lost reindeer!', 'Race to open the presents!']


def header(c, kind, num, title, sub):
    c.setFont('Lucky', 14); c.drawString(M, H - M - 12, f'{kind} {num}')
    c.setFont('Lucky', 32); c.drawCentredString(W / 2, H - M - 52, title.upper())
    if sub: c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 76, sub)


def coloring_page(c, n):
    im = clean(n); iw, ih = im.width / 300 * 72, im.height / 300 * 72
    c.drawImage(ImageReader(im), (W - iw) / 2, (H - ih) / 2, iw, ih)


def maze_page(c, num, rng, art_n, mazes):
    cols = [8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13][num - 1]; rows = int(cols * 1.25)
    opened = mz.make_maze(cols, rows, rng); sol = mz.solve(opened, cols, rows); mazes.append((num, opened, cols, rows, sol))
    header(c, 'MAZE', num, 'Christmas Maze', MAZE_CAPS[num - 1])
    im = small(art_n, 120); c.drawImage(ImageReader(im), W - M - im.width / 3, H - M - 210, im.width / 3, 120)
    cell = min((W - 2 * M - 40) / cols, (H - M - 250 - (M + 40)) / rows)
    x0 = (W - cell * cols) / 2; ytop = H - M - 240
    mz.draw_maze(c, opened, cols, rows, x0, ytop, cell, 3.2)


def ws_page(c, num, rng, art_n, found):
    title, words = XMAS_WS[num - 1]
    lvl = ws.EASY if num <= 6 else ws.MED
    name, st, n, k, maxlen, dirs = lvl
    pool = [w for w in words.split() if 3 <= len(w) <= maxlen]; chosen = []
    for w in pool:
        if len(chosen) < k and not any(w in o or o in w for o in chosen): chosen.append(w)
    g, placed = ws.make_puzzle(chosen, n, dirs, rng)
    ws.puzzle_page(c, num, title, lvl, g, placed, small(art_n, 150).convert('L'))
    found.append((num, title, g, placed))


def dot_page(c, num, label, shape, art_n):
    header(c, 'DOT', num, f'Dot the {label}', 'Press one dot in every circle!')
    m, sp = dm.shape_mask(shape)
    c.setLineWidth(4); c.setStrokeColor(black)
    if sp[0] == 'ellipse':
        x0, y0, x1, y1 = sp[1]; c.ellipse(x0, y0, x1, y1, stroke=1, fill=0)
    else:
        for poly in sp:
            p = c.beginPath(); p.moveTo(*poly[0]); [p.lineTo(*q) for q in poly[1:]]; p.close(); c.drawPath(p, stroke=1, fill=0)
    dm.dots(c, dm.pack(m))
    im = small(art_n, 110); c.drawImage(ImageReader(im), W - M - im.width / 3, M, im.width / 3, 110)


def maze_answers(c, mazes):
    for p in range(0, len(mazes), 6):
        c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - M - 30, 'MAZE ANSWERS')
        for i, (num, opened, cols, rows, sol) in enumerate(mazes[p:p + 6]):
            bw = (W - 2 * M - 30) / 2; bh = (H - 2 * M - 70) / 3
            x = M + (i % 2) * (bw + 30); ytop = H - M - 70 - (i // 2) * bh
            c.setFont('Fred', 11); c.drawString(x, ytop, f'Maze {num}')
            cell = min((bw - 10) / cols, (bh - 30) / rows)
            mz.draw_maze(c, opened, cols, rows, x + (bw - cell * cols) / 2, ytop - 10, cell, 1.2, sol=sol, labels=False)
        c.showPage()


def belongs(c):
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 170, 'THIS BOOK'); c.drawCentredString(W / 2, H - 218, 'BELONGS TO')
    c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    im = small(3, 300); c.drawImage(ImageReader(im), (W - im.width / 3) / 2, 100, im.width / 3, 300)


def contents(c):
    c.setFont('Lucky', 36); c.drawCentredString(W / 2, H - M - 40, "WHAT'S INSIDE")
    c.setFont('FredR', 16)
    rows = ['12 Christmas coloring pages', '12 mazes (easy to tricky)', '12 Christmas word searches',
            '6 dot marker pages', 'Answers at the back', 'A Christmas Activity Champion certificate']
    for i, t in enumerate(rows): c.circle(170, H - M - 110 - i * 34 + 5, 4, fill=1); c.drawString(185, H - M - 110 - i * 34, t)
    c.setFont('FredR', 13); c.drawCentredString(W / 2, H - M - 340, 'Every activity page is single-sided, so markers will not bleed through.')
    c.drawCentredString(W / 2, H - M - 362, 'The coloring pages also appear in our Dino Christmas Trucks Coloring Book.')
    im = small(9, 240); c.drawImage(ImageReader(im), (W - im.width / 3) / 2, M + 30, im.width / 3, 240)


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 210, 'CHRISTMAS ACTIVITY'); c.drawCentredString(W / 2, H - 258, 'CHAMPION')
    c.setFont('FredR', 16); c.drawCentredString(W / 2, H - 320, 'This award goes to'); c.line(140, H - 380, W - 140, H - 380)
    c.drawCentredString(W / 2, H - 420, 'for finishing every activity. Merry Christmas!')
    im = small(47, 240); c.drawImage(ImageReader(im), (W - im.width / 3) / 2, 120, im.width / 3, 240)


def build():
    rng = random.Random(1225)
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Christmas Activity Book'); c.setAuthor('Bibhu Behera')
    belongs(c); c.showPage(); contents(c); c.showPage()
    mazes, found = [], []; art = iter(SMALL_ART * 3); acts = 0
    for i in range(12):
        coloring_page(c, COLOR_PAGES[i]); c.showPage(); c.showPage(); acts += 1
        maze_page(c, i + 1, rng, next(art), mazes); c.showPage(); c.showPage(); acts += 1
        ws_page(c, i + 1, rng, next(art), found); c.showPage(); c.showPage(); acts += 1
        if i < 6:
            dot_page(c, i + 1, *DOT_SHAPES[i], next(art)); c.showPage(); c.showPage(); acts += 1
    maze_answers(c, mazes)
    for p in range(0, 12, 4): ws.answers_page(c, found[p:p + 4], p + 1); c.showPage()
    certificate(c); c.showPage()
    c.save()
    # coloured sleigh page for the front cover (same auto-colour as Book 05)
    sm = clean(7).resize((clean(7).width // 3, clean(7).height // 3), Image.LANCZOS).point(lambda v: 255 if v > 128 else 0)
    xm.autocolour(sm).save(os.path.join(WORK, 'cover_page_coloured.png'))
    print('activities', acts)


if __name__ == '__main__':
    build()
