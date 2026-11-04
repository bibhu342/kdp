"""Dino Trucks Sudoku for Kids — interior builder (code-made, 0 image credits).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
30 x 4x4 (2x2 boxes), 30 x 6x6 (2x3 boxes), 20 x easy 9x9. Every puzzle has exactly one solution (solver-checked).
Pencil book: double-sided. Pictures reuse the Dino Trucks art in ../../03-dino-trucks-mazes/art/.
"""
import os, random
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, Color

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', '..', '03-dino-trucks-mazes', 'art')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
for n, f in [('Lucky', 'LuckiestGuy'), ('Fred', 'Fredoka-SemiBold'), ('FredR', 'Fredoka-Regular')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, f + '.ttf')))
W, H, M = 612, 792, 43
SHADE = Color(0.9, 0.9, 0.9)
LEVELS = [('EASY', 1, 4, (2, 2), 9, 30), ('MEDIUM', 2, 6, (2, 3), 20, 30), ('HARD', 3, 9, (3, 3), 38, 20)]  # name, stars, n, box(r,c), clues, count


def candidates(g, n, br, bc, r, c):
    used = set(g[r]) | {g[i][c] for i in range(n)}
    r0, c0 = r - r % br, c - c % bc
    used |= {g[i][j] for i in range(r0, r0 + br) for j in range(c0, c0 + bc)}
    return [v for v in range(1, n + 1) if v not in used]


def solve(g, n, br, bc, rng=None, limit=2):
    """Count solutions up to `limit`; if rng is given, fill g with a random full solution."""
    best = None
    for r in range(n):
        for c in range(n):
            if g[r][c] == 0:
                cand = candidates(g, n, br, bc, r, c)
                if best is None or len(cand) < len(best[2]): best = (r, c, cand)
    if best is None: return 1
    r, c, cand = best
    if rng: rng.shuffle(cand)
    total = 0
    for v in cand:
        g[r][c] = v; total += solve(g, n, br, bc, rng, limit)
        if rng and total: return total
        if total >= limit: break
    g[r][c] = 0
    return total


def make(n, br, bc, clues, rng):
    sol = [[0] * n for _ in range(n)]; solve(sol, n, br, bc, rng)
    puz = [row[:] for row in sol]; cells = [(r, c) for r in range(n) for c in range(n)]; rng.shuffle(cells)
    filled = n * n
    for r, c in cells:
        if filled <= clues: break
        keep = puz[r][c]; puz[r][c] = 0
        if solve([row[:] for row in puz], n, br, bc) != 1: puz[r][c] = keep
        else: filled -= 1
    assert solve([row[:] for row in puz], n, br, bc) == 1
    return puz, sol


def grid(c, g, n, br, bc, x0, ytop, size, fs, sol=None):
    cell = size / n
    for r in range(n):                           # shade alternate boxes for little eyes
        for k in range(n):
            if ((r // br) + (k // bc)) % 2 == 0: c.setFillColor(SHADE); c.rect(x0 + k * cell, ytop - (r + 1) * cell, cell, cell, stroke=0, fill=1)
    c.setFillColor(black)
    for i in range(n + 1):
        c.setLineWidth(3.2 if i % bc == 0 or i in (0, n) else 0.9); c.line(x0 + i * cell, ytop, x0 + i * cell, ytop - size)
        c.setLineWidth(3.2 if i % br == 0 or i in (0, n) else 0.9); c.line(x0, ytop - i * cell, x0 + size, ytop - i * cell)
    for r in range(n):
        for k in range(n):
            v = g[r][k] or (sol[r][k] if sol else 0)
            if v:
                c.setFont('Fred' if g[r][k] else 'FredR', fs); c.setFillColor(black if g[r][k] else Color(.45, .45, .45))
                c.drawCentredString(x0 + (k + .5) * cell, ytop - (r + .5) * cell - fs * .35, str(v))
    c.setFillColor(black)


def stars(c, x, y, k, size=8):
    import math
    for i in range(3):
        cx = x + i * size * 2.4; p = c.beginPath()
        for j in range(10):
            a = math.pi / 2 + j * math.pi / 5; rr = size if j % 2 == 0 else size * .45
            px, py = cx + rr * math.cos(a), y + rr * math.sin(a); p.moveTo(px, py) if j == 0 else p.lineTo(px, py)
        p.close(); c.setLineWidth(1); c.setFillColor(black if i < k else Color(1, 1, 1)); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(black)


_art = {}
def art(i):
    i = (i - 1) % 25 + 1
    if i not in _art: _art[i] = Image.open(os.path.join(ART, f'{i:02d}.png')).convert('L')
    return _art[i]


def puzzle_page(c, num, lvl, puz):
    name, st, n, (br, bc), _, _ = lvl
    c.setFont('Lucky', 15); c.drawString(M, H - M - 12, f'SUDOKU {num}')
    c.setFont('Fred', 10); c.drawRightString(W - M - 58, H - M - 11, name); stars(c, W - M - 44, H - M - 7, st)
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 56, f'{n} x {n} SUDOKU')
    c.setFont('Fred', 14); c.drawCentredString(W / 2, H - M - 82, f'Write 1 to {n} so every row, column and box has each number once.')
    size = {4: 360, 6: 420, 9: 470}[n]; fs = {4: 54, 6: 40, 9: 26}[n]
    grid(c, puz, n, br, bc, (W - size) / 2, H - M - 110, size, fs)
    gb = H - M - 110 - size                       # grid bottom: keep the picture below it
    img = art(num); iw, ih = img.size; s = min(min(130, gb - M - 8) / ih, 160 / iw)
    c.drawImage(ImageReader(img), W - M - iw * s, M, iw * s, ih * s, mask='auto')
    c.setFont('FredR', 10); c.drawString(M, M + 4, 'Tip: use a pencil so you can rub out. Then color the picture!')


def how_to(c):
    c.setFont('Lucky', 36); c.drawCentredString(W / 2, H - M - 40, 'HOW TO PLAY SUDOKU')
    c.setFont('FredR', 16)
    for k, t in enumerate(['Each row (across) uses every number once.', 'Each column (down) uses every number once.',
                           'Each thick-lined box uses every number once.', 'Look for a row, column or box with just one gap',
                           'and work out the missing number.', 'Start with EASY 4x4, then MEDIUM 6x6, then HARD 9x9.',
                           'Stuck? The answers are at the back.']):
        c.drawCentredString(W / 2, H - M - 100 - k * 30, t)
    rng = random.Random(5); puz, sol = make(4, 2, 2, 11, rng)
    c.setFont('Fred', 14); c.drawCentredString(W / 2, 360, 'Try this one: which number is missing?')
    grid(c, puz, 4, 2, 2, (W - 240) / 2, 340, 240, 40)


def answers(c, items, per):
    cols = 3 if per == 9 else 2; rows = per // cols
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - M - 30, 'ANSWERS')
    bw = (W - 2 * M - (cols - 1) * 24) / cols; bh = (H - 2 * M - 60) / rows
    for i, (num, lvl, puz, sol) in enumerate(items):
        n, (br, bc) = lvl[2], lvl[3]
        x = M + (i % cols) * (bw + 24); ytop = H - M - 56 - (i // cols) * bh
        c.setFont('Fred', 11); c.drawString(x, ytop - 2, f'Sudoku {num}')
        size = min(bw, bh - 28); grid(c, puz, n, br, bc, x + (bw - size) / 2, ytop - 12, size, size / n * .55, sol)


def belongs(c):
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 170, 'THIS BOOK'); c.drawCentredString(W / 2, H - 218, 'BELONGS TO')
    c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    img = art(13); iw, ih = img.size; s = 330 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 110, iw * s, ih * s, mask='auto')


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 46); c.drawCentredString(W / 2, H - 215, 'SUDOKU'); c.drawCentredString(W / 2, H - 268, 'SUPERSTAR')
    c.setFont('FredR', 16); c.drawCentredString(W / 2, H - 330, 'This award goes to'); c.line(140, H - 390, W - 140, H - 390)
    c.drawCentredString(W / 2, H - 430, 'for solving all 80 sudoku puzzles!')
    img = art(11); iw, ih = img.size; s = 230 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 130, iw * s, ih * s, mask='auto')


def build():
    rng = random.Random(2027)
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Trucks Sudoku for Kids'); c.setAuthor('Bibhu Behera')
    belongs(c); c.showPage(); how_to(c); c.showPage(); pages = 2
    done = []; num = 0
    for lvl in LEVELS:
        _, _, n, (br, bc), clues, count = lvl
        for _ in range(count):
            num += 1; puz, sol = make(n, br, bc, clues, rng)
            puzzle_page(c, num, lvl, puz); c.showPage(); pages += 1; done.append((num, lvl, puz, sol))
    for lvl, per in zip(LEVELS, (9, 6, 4)):
        items = [d for d in done if d[1] is lvl]
        for p in range(0, len(items), per): answers(c, items[p:p + per], per); c.showPage(); pages += 1
    certificate(c); c.showPage(); pages += 1
    if pages % 2: c.showPage(); pages += 1
    c.save(); print('puzzles', num, 'pages', pages)


if __name__ == '__main__':
    build()
