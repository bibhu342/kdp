"""Dino Trucks Mazes — interior builder (reportlab, vector mazes, embedded TTF fonts).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
"""
import random, os
from collections import deque
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', 'art')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
pdfmetrics.registerFont(TTFont('Lucky', os.path.join(HERE, 'LuckiestGuy.ttf')))
pdfmetrics.registerFont(TTFont('Pop', '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('PopB', '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'))

W, H = 612, 792
M = 45  # ink margin (0.625 in)
BOOK = 'Dino Trucks Mazes'
GREY = 0.55

CAPTIONS = {
 1: 'Help the digger dino reach the dirt pile!', 2: 'Push the rocks all the way to FINISH!',
 3: 'Drive the dump truck to the building site!', 4: 'Guide the crane to the steel beams!',
 5: 'Roll the new road all the way to FINISH!', 6: 'Carry the crates to the warehouse!',
 7: 'Get the cement mixer to the new house!', 8: 'Help the little digger find the way out!',
 9: 'Help the dino team finish the bridge!', 10: 'Pull the big log back to the farm!',
 11: 'Jump the monster truck to the finish line!', 12: 'Race to the checkered flag!',
 13: 'Zoom the go-kart around the track!', 14: 'Bounce over the sand dunes to FINISH!',
 15: 'Who wins? Race to the finish line!', 16: 'Ride the dirt bike along the trail!',
 17: 'Drive over the ramp and find the way!', 18: 'Get the muddy car to the car wash!',
 19: 'Rush the fire truck to the fire!', 20: 'Drive the ambulance to the hospital!',
 21: 'Help the police car find its way home!', 22: 'Tow the little car to the garage!',
 23: 'Fly the helicopter back to the helipad!', 24: 'Sail the boat across the lake!',
 25: 'Clear a path through the snow!'}

LEVELS = [('EASY', 1, (6, 9), 4.2), ('MEDIUM', 2, (10, 13), 3.2), ('HARD', 3, (14, 17), 2.6)]


def make_maze(cols, rows, rng):
    """Recursive backtracker. walls[r][c] = set of open dirs."""
    opened = [[set() for _ in range(cols)] for _ in range(rows)]
    seen = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]; seen[0][0] = True
    D = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    OPP = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}
    while stack:
        r, c = stack[-1]
        nb = [(d, r + dr, c + dc) for d, (dr, dc) in D.items()
              if 0 <= r + dr < rows and 0 <= c + dc < cols and not seen[r + dr][c + dc]]
        if not nb:
            stack.pop(); continue
        d, nr, nc = rng.choice(nb)
        opened[r][c].add(d); opened[nr][nc].add(OPP[d]); seen[nr][nc] = True
        stack.append((nr, nc))
    return opened


def solve(opened, cols, rows):
    D = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    prev = {(0, 0): None}; q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        if (r, c) == (rows - 1, cols - 1): break
        for d in opened[r][c]:
            n = (r + D[d][0], c + D[d][1])
            if n not in prev: prev[n] = (r, c); q.append(n)
    path, n = [], (rows - 1, cols - 1)
    while n: path.append(n); n = prev[n]
    return path[::-1]


def draw_maze(cv, opened, cols, rows, x0, ytop, cell, lw, sol=None, labels=True):
    """x0,ytop = top-left corner of maze in PDF points."""
    def X(c): return x0 + c * cell
    def Y(r): return ytop - r * cell
    if sol:
        cv.setStrokeGray(0.72); cv.setLineWidth(cell * 0.38); cv.setLineCap(1); cv.setLineJoin(1)
        p = cv.beginPath()
        pts = [(X(c) + cell / 2, Y(r) - cell / 2) for r, c in sol]
        p.moveTo(pts[0][0], pts[0][1] + cell / 2)
        for x, y in pts: p.lineTo(x, y)
        p.lineTo(pts[-1][0], pts[-1][1] - cell / 2)
        cv.drawPath(p, stroke=1, fill=0)
    cv.setStrokeGray(0); cv.setLineWidth(lw); cv.setLineCap(1)
    for r in range(rows):
        for c in range(cols):
            o = opened[r][c]
            if 'E' not in o and c < cols - 1: cv.line(X(c + 1), Y(r), X(c + 1), Y(r + 1))
            if 'S' not in o and r < rows - 1: cv.line(X(c), Y(r + 1), X(c + 1), Y(r + 1))
    # border with entrance (top of 0,0) and exit (bottom of last cell)
    cv.line(X(1), Y(0), X(cols), Y(0)); cv.line(X(0), Y(0), X(0), Y(rows))
    cv.line(X(cols), Y(0), X(cols), Y(rows)); cv.line(X(0), Y(rows), X(cols - 1), Y(rows))
    if labels:
        fs = 13
        cv.setFillGray(0); cv.setFont('PopB', fs)
        cx = X(0) + cell / 2
        cv.drawCentredString(cx, Y(0) + 17, 'START')
        arrow(cv, cx, Y(0) + 14, Y(0) + 3)
        ex = X(cols - 1) + cell / 2
        arrow(cv, ex, Y(rows) - 3, Y(rows) - 14)
        cv.drawCentredString(ex, Y(rows) - 28, 'FINISH')


def arrow(cv, x, y1, y2):
    cv.setLineWidth(2); cv.line(x, y1, x, y2)
    p = cv.beginPath(); p.moveTo(x - 4, y2 + 4); p.lineTo(x + 4, y2 + 4); p.lineTo(x, y2 - 1); p.close()
    cv.drawPath(p, fill=1, stroke=0)


def stars(cv, x, y, n, size=9):
    import math
    for k in range(3):
        cx = x + k * (size * 2.3)
        p = cv.beginPath()
        for i in range(10):
            a = math.pi / 2 + i * math.pi / 5
            rr = size if i % 2 == 0 else size * 0.45
            px, py = cx + rr * math.cos(a), y + rr * math.sin(a)
            (p.moveTo if i == 0 else p.lineTo)(px, py)
        p.close()
        cv.setLineWidth(1.2); cv.setStrokeGray(0)
        cv.setFillGray(0 if k < n else 1)
        cv.drawPath(p, fill=1, stroke=1)
    cv.setFillGray(0)


def footer(cv, pageno):
    cv.setFont('Pop', 8); cv.setFillGray(0.45)
    cv.drawCentredString(W / 2, 30, f'{pageno}')
    cv.setFillGray(0)


def place_art(cv, n, x, y, w, h):
    img = ImageReader(os.path.join(ART, f'{n:02d}.png'))
    iw, ih = img.getSize(); s = min(w / iw, h / ih)
    cv.drawImage(img, x + (w - iw * s) / 2, y + (h - ih * s) / 2, iw * s, ih * s)


def build():
    rng = random.Random(2026)
    cv = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='Pop', initialFontSize=12)
    cv.setTitle(BOOK); cv.setAuthor('Bibhu Behera')
    page = 1
    # p1 title
    cv.setFont('Lucky', 54); cv.drawCentredString(W / 2, 640, 'DINO TRUCKS')
    cv.setFont('Lucky', 44); cv.drawCentredString(W / 2, 590, 'MAZES')
    cv.setFont('PopB', 16); cv.drawCentredString(W / 2, 556, '75 Fun Mazes for Kids Ages 4-8')
    place_art(cv, 11, 106, 170, 400, 360)
    cv.setFont('Pop', 12); cv.drawCentredString(W / 2, 120, 'Bibhu Behera  ·  Dino Doodle')
    cv.showPage(); page += 1
    # p2 belongs to
    cv.setFont('Lucky', 40); cv.drawCentredString(W / 2, 640, 'THIS BOOK')
    cv.drawCentredString(W / 2, 596, 'BELONGS TO')
    cv.setLineWidth(2.5); cv.roundRect(96, 470, 420, 90, 18)
    place_art(cv, 13, 146, 110, 320, 320)
    footer(cv, page); cv.showPage(); page += 1
    # p3 how to play
    cv.setFont('Lucky', 40); cv.drawCentredString(W / 2, 690, 'HOW TO PLAY')
    lines = ['1. Put your pencil on START.', '2. Find a path to FINISH without crossing a wall.',
             '3. Stuck? Go back and try another way!', '4. Color the dino truck when you finish.',
             '5. Answers are at the back of the book.']
    cv.setFont('Pop', 15)
    for i, t in enumerate(lines): cv.drawString(90, 630 - i * 30, t)
    y = 440
    for name, n, (a, b), _ in LEVELS:
        stars(cv, 110, y + 5, n, 11)
        cv.setFont('PopB', 16); cv.drawString(190, y, name)
        cv.setFont('Pop', 13)
        rng_txt = {'EASY': 'Mazes 1-25 · big paths for little hands',
                   'MEDIUM': 'Mazes 26-50 · more turns, more fun',
                   'HARD': 'Mazes 51-75 · for maze masters'}[name]
        cv.drawString(290, y, rng_txt); y -= 50
    cv.setFont('PopB', 14); cv.drawCentredString(W / 2, 230, 'Tip: start with a pencil, then trace it in crayon!')
    place_art(cv, 8, 206, 60, 200, 150)
    footer(cv, page); cv.showPage(); page += 1

    solutions = []
    mazeno = 0
    for li, (name, n, (cmin, cmax), lw) in enumerate(LEVELS):
        order = list(range(1, 26)); rng.shuffle(order)
        for k, art in enumerate(order):
            mazeno += 1
            cols = cmin + (k * (cmax - cmin + 1)) // 25
            # header
            cv.setFont('Lucky', 30); cv.drawString(M, H - M - 26, f'MAZE {mazeno}')
            cv.setFont('PopB', 13); cv.drawRightString(W - M - 80, H - M - 20, name)
            stars(cv, W - M - 62, H - M - 15, n, 9)
            cv.setFont('Pop', 14); cv.drawCentredString(W / 2, H - M - 52, CAPTIONS[art])
            # art
            place_art(cv, art, M, 500, W - 2 * M, 175)
            # maze area: x 52..560, y 75..470
            area_w, area_h = W - 2 * 52, 470 - 82
            cell = area_w / cols
            rows = max(cols - 1, int(area_h // cell))
            cell = min(area_w / cols, area_h / rows)
            mw, mh = cols * cell, rows * cell
            x0 = (W - mw) / 2; ytop = 82 + (area_h + mh) / 2
            for _ in range(20):  # prefer long solutions
                opened = make_maze(cols, rows, rng)
                sol = solve(opened, cols, rows)
                if len(sol) >= 0.35 * cols * rows or cols * rows > 150: break
            draw_maze(cv, opened, cols, rows, x0, ytop, cell, lw)
            solutions.append((mazeno, opened, cols, rows, sol))
            footer(cv, page); cv.showPage(); page += 1
    # answers
    cv.setFont('Lucky', 52); cv.drawCentredString(W / 2, 470, 'ANSWERS')
    cv.setFont('Pop', 15); cv.drawCentredString(W / 2, 430, 'No peeking until you have tried your best!')
    place_art(cv, 15, 156, 120, 300, 260)
    footer(cv, page); cv.showPage(); page += 1
    for i in range(0, len(solutions), 6):
        for j, (no, opened, cols, rows, sol) in enumerate(solutions[i:i + 6]):
            col, row = j % 2, j // 2
            bx, by_top = M + col * 265, H - M - 10 - row * 235
            cv.setFont('PopB', 12); cv.drawString(bx, by_top, f'Maze {no}')
            bw, bh = 250, 200
            cell = min(bw / cols, bh / rows)
            draw_maze(cv, opened, cols, rows, bx + (bw - cols * cell) / 2, by_top - 10, cell, 1.0,
                      sol=sol, labels=False)
        footer(cv, page); cv.showPage(); page += 1
    # certificate
    cv.setLineWidth(4); cv.roundRect(60, 120, W - 120, 600, 24)
    cv.setLineWidth(1.5); cv.roundRect(72, 132, W - 144, 576, 18)
    cv.setFont('Lucky', 44); cv.drawCentredString(W / 2, 640, 'MAZE MASTER!')
    cv.setFont('Pop', 15); cv.drawCentredString(W / 2, 600, 'This certificate is awarded to')
    cv.setLineWidth(1.5); cv.line(140, 545, W - 140, 545)
    cv.drawCentredString(W / 2, 510, 'for finishing all 75 Dino Trucks Mazes!')
    place_art(cv, 12, 156, 200, 300, 270)
    cv.setFont('Pop', 12); cv.drawString(140, 165, 'Date: ____________')
    footer(cv, page); cv.showPage(); page += 1
    # draw your own maze
    cv.setFont('Lucky', 34); cv.drawCentredString(W / 2, H - M - 30, 'DRAW YOUR OWN MAZE!')
    cv.setFont('Pop', 13); cv.drawCentredString(W / 2, H - M - 54, 'Join the dots to make walls. Then ask a friend to solve it!')
    for r in range(15):
        for c in range(13):
            cv.circle(78 + c * 38, 630 - r * 38, 2.2, fill=1, stroke=0)
    footer(cv, page); cv.showPage()
    cv.save()
    print('pages', page)


if __name__ == '__main__':
    build()
