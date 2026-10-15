"""ADHD Homework Planner — full 120-page interior + wraparound cover.
Run: python3 build_book.py  -> ../interior.pdf, ../cover.pdf
Fonts are embedded TrueType (Liberation Sans = Helvetica metrics) so KDP preflight passes.
"""
import math
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/liberation/"
for n, f in [("Sans", "LiberationSans-Regular"), ("Sans-Bold", "LiberationSans-Bold"),
             ("Sans-Italic", "LiberationSans-Italic"), ("Sans-BoldItalic", "LiberationSans-BoldItalic")]:
    pdfmetrics.registerFont(TTFont(n, FD + f + ".ttf"))

AUTHOR = "Leah Marston"  # pen name (Bibhu: do not use real name); clear on web search Oct 15
TITLE = "ADHD Homework Planner for Students"
DAYS, WEEKS = 180, 36
MONTH_WEEKS = [4] * 9  # full school year: 36 weeks over 9 monthly resets

W, H = letter; M = 0.55 * 72; cw = W - 2 * M
GR = HexColor("#D9D9D9"); LT = HexColor("#F0F0F0"); L = HexColor("#AAAAAA"); G = HexColor("#555555")


# ---------- primitives ----------
def box(c, x, y, w, h, title, sub=None):
    c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(white); c.roundRect(x, y, w, h, 7, fill=1)
    c.setFillColor(GR); c.roundRect(x, y + h - 20, w, 20, 7, fill=1, stroke=0); c.rect(x, y + h - 20, w, 8, fill=1, stroke=0)
    c.setStrokeColor(black); c.roundRect(x, y, w, h, 7)
    c.setFillColor(black); c.setFont("Sans-Bold", 10.5); c.drawString(x + 8, y + h - 14, title)
    if sub:
        c.setFont("Sans-Italic", 7.5); c.setFillColor(G); c.drawRightString(x + w - 8, y + h - 14, sub); c.setFillColor(black)

def ln(c, x1, y, x2): c.setStrokeColor(L); c.setLineWidth(0.6); c.line(x1, y, x2, y); c.setStrokeColor(black)
def cb(c, x, y, s=9): c.setLineWidth(0.9); c.rect(x, y, s, s)
def dot(c, x, y, r=6): c.setFillColor(LT); c.setLineWidth(0.9); c.circle(x, y, r, fill=1); c.setFillColor(black)

def header(c, title, right1=None, right2=None, tag=None):
    y = H - M
    c.setFont("Sans-Bold", 21); c.setFillColor(black); c.drawString(M, y - 18, title)
    if tag:
        tw = c.stringWidth(title, "Sans-Bold", 21)
        c.setFont("Sans-Bold", 8); pw = c.stringWidth(tag, "Sans-Bold", 8) + 12
        c.setFillColor(GR); c.roundRect(M + tw + 10, y - 18, pw, 14, 7, fill=1, stroke=0)
        c.setFillColor(black); c.drawCentredString(M + tw + 10 + pw / 2, y - 14, tag)
    c.setFont("Sans", 9.5); c.setFillColor(G)
    if right1: c.drawRightString(W - M, y - 7, right1)
    if right2: c.drawRightString(W - M, y - 21, right2)
    c.setFillColor(black)
    return y - 32

def footer(c, text):
    c.setFont("Sans-Italic", 7); c.setFillColor(G); c.drawCentredString(W / 2, M - 13, text); c.setFillColor(black)

def lines_in(c, x, y_top, w, n, gap, start=34):
    for i in range(n): ln(c, x + 10, y_top - start - i * gap, x + w - 10)


# ---------- daily page (v2 APPROVED layout, unchanged) ----------
def daily(c, day=None):
    y = header(c, "TODAY'S PLAN", "Date: ____ / ____ / ______", "Circle:  M   T   W   Th   F   Sa   Su",
               tag=f"DAY {day} of {DAYS}" if day else None)
    h = 36; box(c, M, y - h, cw, h, "RECHARGE FIRST", "after school, before homework")
    c.setFont("Sans", 9.5)
    for i, t in enumerate(["Snack", "Water", "Move 10 min", "Quiet time"]):
        x = M + 12 + i * (cw - 24) / 4; cb(c, x, y - 31); c.drawString(x + 14, y - 30, t)
    y -= h + 7
    h = 82; box(c, M, y - h, cw, h, "MY TOP 3", "+ the tiny 2-minute first step")
    c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(M + 30, y - 31, "Task"); c.drawString(M + cw * 0.55, y - 31, "Tiny first step"); c.setFillColor(black)
    for i in range(3):
        yy = y - 47 - i * 15; cb(c, M + 12, yy); ln(c, M + 30, yy, M + cw * 0.52); ln(c, M + cw * 0.55, yy, M + cw - 12)
    y -= h + 7
    h = 176; box(c, M, y - h, cw, h, "HOMEWORK", "guess the time, then check it")
    tw = cw - 16; cols = [("Subject", 0.17), ("Steps (write them all down)", 0.47), ("Guess", 0.11), ("Real", 0.11), ("Done", 0.14)]
    c.setFont("Sans-Bold", 8.5); xx = M + 8; hy = y - 33
    for n, f in cols: c.drawString(xx + 3, hy, n); xx += tw * f
    rows = 6; rh = 21
    for i in range(rows + 1): ln(c, M + 8, hy - 5 - i * rh, M + cw - 8)
    xx = M + 8
    for n, f in cols[:-1]:
        xx += tw * f; c.setStrokeColor(L); c.line(xx, hy + 11, xx, hy - 5 - rows * rh); c.setStrokeColor(black)
    c.setFont("Sans", 7.5); c.setFillColor(G)
    for i in range(rows):
        yb = hy - 5 - (i + 1) * rh + 6
        c.drawRightString(M + 8 + tw * 0.75 - 4, yb, "min"); c.drawRightString(M + 8 + tw * 0.86 - 4, yb, "min")
        c.setFillColor(black); cb(c, M + 8 + tw * 0.93 - 4, yb - 1); c.setFillColor(G)
    c.setFillColor(black)
    y -= h + 7
    hw = (cw - 8) / 2; h = 104; x2 = M + hw + 8
    box(c, M, y - h, hw, h, "FOCUS SPRINTS", "fill one per 20 min")
    for r in range(2):
        for i in range(4):
            cx = M + 28 + i * ((hw - 40) / 3.3); cy = y - 42 - r * 32; dot(c, cx, cy, 10)
            if i < 3: c.setFont("Sans", 6.5); c.setFillColor(G); c.drawCentredString(cx + (hw - 40) / 6.6, cy - 3, "move!"); c.setFillColor(black)
    c.setFont("Sans", 7.5); c.drawString(M + 10, y - h + 7, "Hyperfocus alarm: stop at ____:____")
    box(c, x2, y - h, hw, h, "DISTRACTION PARKING LOT", "park it, do it later")
    for i in range(4): ln(c, x2 + 10, y - 38 - i * 17, x2 + hw - 10)
    y -= h + 7
    h = 100
    box(c, M, y - h, hw, h, "BEFORE I HAND IT IN")
    c.setFont("Sans", 9)
    for i, t in enumerate(["Name + date on it", "Every question answered", "Read the instructions again", "Checked one more time", "In my folder / sent"]):
        yy = y - 36 - i * 13.5; cb(c, M + 12, yy); c.drawString(M + 26, yy + 1, t)
    box(c, x2, y - h, hw, h, "HOW I FELT TODAY")
    c.setFont("Sans", 8.5)
    for i, t in enumerate(["Focus", "Energy", "Mood"]):
        yy = y - 36 - i * 13; c.drawString(x2 + 10, yy, t)
        for j in range(5): dot(c, x2 + 68 + j * 18, yy + 3, 5)
    c.setFont("Sans-Bold", 8); c.drawString(x2 + 10, y - h + 22, "If a friend had my day, I'd tell them:")
    ln(c, x2 + 10, y - h + 9, x2 + hw - 10)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "WIN OF THE DAY", "+ my reward")
    c.setFont("Sans", 9); c.drawString(M + 12, M + h - 36, "Today I did:"); ln(c, M + 75, M + h - 37, M + cw - 12)
    c.drawString(M + 12, M + h - 54, "My reward:"); ln(c, M + 75, M + h - 55, M + cw - 12)
    footer(c, "Mistakes help my brain grow. Done is better than perfect.")


# ---------- weekly overview ----------
def weekly(c, wk):
    y = header(c, "MY WEEK", "Week of: ____ / ____ / ______", tag=f"WEEK {wk} of {WEEKS}")
    h = 170; box(c, M, y - h, cw, h, "BIG THINGS DUE THIS WEEK", "tests, projects, forms, library books")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]; dw = (cw - 16) / 5
    for i, d in enumerate(days):
        x = M + 8 + i * dw
        c.setFont("Sans-Bold", 9); c.drawCentredString(x + dw / 2, y - 34, d)
        if i: c.setStrokeColor(L); c.line(x, y - 26, x, y - h + 8); c.setStrokeColor(black)
        for j in range(6): ln(c, x + 5, y - 56 - j * 19, x + dw - 5)
    y -= h + 7
    h = 74; box(c, M, y - h, cw, h, "AFTER-SCHOOL SCHEDULE", "sports, clubs, appointments")
    days7 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]; dw = (cw - 16) / 7
    for i, d in enumerate(days7):
        x = M + 8 + i * dw
        c.setFont("Sans-Bold", 8.5); c.drawCentredString(x + dw / 2, y - 34, d)
        if i: c.setStrokeColor(L); c.line(x, y - 26, x, y - h + 8); c.setStrokeColor(black)
        ln(c, x + 5, y - 52, x + dw - 5); ln(c, x + 5, y - 66, x + dw - 5)
    y -= h + 7
    hw = (cw - 8) / 2; x2 = M + hw + 8; h = 88
    box(c, M, y - h, hw, h, "ONE GOAL THIS WEEK", "small + specific")
    lines_in(c, M, y, hw, 2, 17, 38)
    c.setFont("Sans", 8.5); c.drawString(M + 10, y - h + 12, "If I hit it, my reward:"); ln(c, M + 108, y - h + 11, M + hw - 10)
    box(c, x2, y - h, hw, h, "HOMEWORK STREAK", "colour a star each day")
    for i, d in enumerate(days):
        cx = x2 + 26 + i * (hw - 52) / 4; star(c, cx, y - 52, 13)
        c.setFont("Sans", 8); c.drawCentredString(cx, y - 78, d)
    y -= h + 7
    h = 150; box(c, M, y - h, cw, h, "FRIENDSHIP CHECK-IN", "people matter too")
    c.setFont("Sans", 9)
    q = ["Someone I enjoyed being with:", "One kind thing I did for someone:", "Something with friends that felt hard:"]
    for i, t in enumerate(q):
        yy = y - 40 - i * 22; c.drawString(M + 12, yy, t); ln(c, M + 12 + c.stringWidth(t, "Sans", 9) + 6, yy - 1, M + cw - 12)
    c.setFont("Sans-Bold", 8.5); c.drawString(M + 12, y - 110, "Words I can use:")
    scripts = ["“Can I join you?”", "“Sorry I interrupted - you go first.”", "“I need a minute. I'll be right back.”"]
    sw = (cw - 24) / 3
    for i, s in enumerate(scripts):
        x = M + 12 + i * sw
        c.setFillColor(LT); c.roundRect(x, y - h + 10, sw - 8, 24, 6, fill=1, stroke=0); c.setFillColor(black)
        c.setFont("Sans-Italic", 8); c.drawCentredString(x + (sw - 8) / 2, y - h + 19, s)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "LOOKING BACK", "fill this in on Friday or Sunday")
    c.setFont("Sans", 9)
    for i, t in enumerate(["What went well:", "What got in the way:", "Next week I'll try:"]):
        yy = M + h - 38 - i * 20; c.drawString(M + 12, yy, t); ln(c, M + 112, yy - 1, M + cw - 12)
    footer(c, "Progress, not perfection.")

def star(c, cx, cy, r):
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close(); c.setFillColor(LT); c.setLineWidth(0.9); c.drawPath(p, fill=1, stroke=1); c.setFillColor(black)


# ---------- monthly reset ----------
def monthly(c, n):
    y = header(c, "MONTHLY RESET", "Month: ______________", tag=f"MONTH {n}")
    h = 260; box(c, M, y - h, cw, h, "BIG DATES", "write the day numbers in, then tests, trips, birthdays")
    gx, gy = M + 8, y - 26; gw = (cw - 16) / 7
    for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        c.setFont("Sans-Bold", 8.5); c.drawCentredString(gx + i * gw + gw / 2, gy - 10, d)
    rh = (h - 26 - 18 - 8) / 5; top = gy - 16
    c.setStrokeColor(L); c.setLineWidth(0.6)
    for r in range(6): c.line(gx, top - r * rh, gx + 7 * gw, top - r * rh)
    for i in range(8): c.line(gx + i * gw, top, gx + i * gw, top - 5 * rh)
    c.setStrokeColor(black)
    for r in range(5):
        for i in range(7): c.setLineWidth(0.6); c.rect(gx + i * gw + 3, top - r * rh - 15, 12, 12)
    y -= h + 7
    hw = (cw - 8) / 2; x2 = M + hw + 8; h = 108
    box(c, M, y - h, hw, h, "LAST MONTH'S WINS"); lines_in(c, M, y, hw, 4, 18, 38)
    box(c, x2, y - h, hw, h, "WHAT GOT IN THE WAY"); lines_in(c, x2, y, hw, 4, 18, 38)
    y -= h + 7
    h = 84; box(c, M, y - h, cw, h, "ONE HABIT TO BUILD", "colour a dot each day you do it")
    c.setFont("Sans", 9); c.drawString(M + 12, y - 38, "My habit:"); ln(c, M + 62, y - 39, M + cw - 12)
    for i in range(31):
        cx = M + 18 + i * (cw - 36) / 30; dot(c, cx, y - 62, 6)
        c.setFont("Sans", 5.5); c.setFillColor(G); c.drawCentredString(cx, y - 76, str(i + 1)); c.setFillColor(black)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "THIS MONTH", "one thing to try + a reward to work toward")
    c.setFont("Sans", 9)
    for i, t in enumerate(["One new thing I'll try:", "Who can help me:", "Reward when I finish the month:"]):
        yy = M + h - 40 - i * 22; c.drawString(M + 12, yy, t); ln(c, M + 12 + c.stringWidth(t, "Sans", 9) + 6, yy - 1, M + cw - 12)
    footer(c, "New month, fresh start.")


# ---------- front & back matter ----------
def belongs(c):
    c.setFont("Sans-Bold", 28); c.drawCentredString(W / 2, H - 150, "THIS PLANNER")
    c.drawCentredString(W / 2, H - 185, "BELONGS TO")
    c.setLineWidth(1.5); c.roundRect(M + 40, H - 290, cw - 80, 70, 12)
    c.setFont("Sans", 11)
    y = H - 350
    for t in ["Grade:", "School:", "Teacher(s):", "Started on:", "If found, please return to:", "Phone / email:"]:
        c.drawString(M + 40, y, t); ln(c, M + 48 + c.stringWidth(t, "Sans", 11), y - 1, W - M - 40); y -= 34
    c.setFont("Sans-Italic", 9); c.setFillColor(G)
    c.drawCentredString(W / 2, M + 60, "Undated - start any day, any year. A full school year of homework, one page at a time.")
    c.setFillColor(black)

def how_to(c):
    y = header(c, "HOW TO USE THIS PLANNER")
    c.setFont("Sans", 10); c.setFillColor(G)
    c.drawString(M, y - 1, "Takes about 5 minutes a day. You don't have to fill in every box - use what helps."); c.setFillColor(black)
    steps = [
        ("1. Recharge first", "Tick snack, water, move and quiet time before starting. A tired brain can't focus."),
        ("2. Pick your Top 3", "Choose the three most important tasks, then write a tiny first step (2 minutes or less) so starting is easy."),
        ("3. Write every step", "In Homework, break each subject into steps. Your planner remembers so your brain doesn't have to."),
        ("4. Guess the time", "Before you start, guess how many minutes it will take. After, write the real time. You'll get better at guessing."),
        ("5. Work in sprints", "Fill one circle for each 20 minutes of work, then move for a minute. Set a hyperfocus alarm so you remember to stop."),
        ("6. Park distractions", "A random thought pops up? Write it in the Parking Lot and get back to work. Do it later."),
        ("7. Check before handing in", "Use the checklist so silly mistakes don't cost you points."),
        ("8. Notice your win", "Write one win - even a small one - and give yourself the reward you picked."),
        ("Every week", "Fill in the My Week page: big due dates, one goal, your streak and a friendship check-in."),
        ("Every month", "Use the Monthly Reset page to look back, plan big dates and pick one habit."),
    ]
    y -= 22; gap = (y - M - 6) / len(steps)
    for t, d in steps:
        c.setFillColor(LT); c.roundRect(M, y - gap + 9, cw, gap - 7, 7, fill=1, stroke=0); c.setFillColor(black)
        c.setFont("Sans-Bold", 11); c.drawString(M + 12, y - 16, t)
        c.setFont("Sans", 9.5); wrap(c, d, M + 12, y - 31, cw - 24, "Sans", 9.5, 12)
        y -= gap
    footer(c, "This planner is a tool, not a test. Messy pages still count.")

def wrap(c, text, x, y, w, font, size, lead):
    words = text.split(); line = ""
    for wd in words:
        t = (line + " " + wd).strip()
        if c.stringWidth(t, font, size) > w: c.drawString(x, y, line); y -= lead; line = wd
        else: line = t
    if line: c.drawString(x, y, line)

def brain_card(c):
    y = header(c, "HOW MY BRAIN WORKS BEST")
    c.setFont("Sans", 10); c.setFillColor(G)
    c.drawString(M, y - 1, "Fill this in with a parent, then show it to your teachers. It helps them help you."); c.setFillColor(black)
    y -= 14
    items = [("I focus best when...", "e.g. I sit near the front, I have quiet, I can fidget"),
             ("Things that help me", "e.g. written instructions, a timer, movement breaks"),
             ("Things that make it harder", "e.g. lots of noise, long lists said out loud"),
             ("When I'm stuck, please...", "e.g. check in quietly, show me the first step"),
             ("The best way to remind me", "e.g. a note on my desk, a quiet tap"),
             ("My strengths", "e.g. creative ideas, kind, great at building things")]
    hw = (cw - 8) / 2; bh = (y - M - 34 - 16) / 3
    for i, (t, s) in enumerate(items):
        x = M + (i % 2) * (hw + 8); yy = y - (i // 2) * (bh + 8)
        box(c, x, yy - bh, hw, bh, t)
        c.setFont("Sans-Italic", 7.5); c.setFillColor(G); c.drawString(x + 10, yy - 34, s); c.setFillColor(black)
        for j in range(int((bh - 62) / 19) + 1): ln(c, x + 10, yy - 54 - j * 19, x + hw - 10)
    y -= 3 * (bh + 8)
    c.setFont("Sans", 9.5)
    c.drawString(M, y - 14, "Name: ____________________________     Parent signature: ____________________________")
    footer(c, "Everyone's brain is different. Knowing yours is a superpower.")

def tracker(c, part):
    y = header(c, "TESTS & PROJECTS", tag=f"PAGE {part} of 2")
    c.setFont("Sans", 10); c.setFillColor(G)
    c.drawString(M, y - 1, "Big jobs feel smaller in pieces. Write the date you'll do each step."); c.setFillColor(black)
    y -= 12
    cols = [("Subject", 0.14), ("Test / project", 0.24), ("Due", 0.09), ("Steps + the day I'll do them", 0.37), ("Started", 0.08), ("Done", 0.08)]
    th = y - M; box(c, M, M, cw, th, "MY TRACKER", "start early, finish calm")
    tw = cw - 16; hy = y - 36; c.setFont("Sans-Bold", 8.5); xx = M + 8
    for n, f in cols: c.drawString(xx + 3, hy, n); xx += tw * f
    rows = 12; rh = (hy - 6 - (M + 8)) / rows
    for i in range(rows + 1): ln(c, M + 8, hy - 6 - i * rh, M + cw - 8)
    xx = M + 8
    for n, f in cols[:-1]:
        xx += tw * f; c.setStrokeColor(L); c.line(xx, hy + 12, xx, hy - 6 - rows * rh); c.setStrokeColor(black)
    for i in range(rows):
        yb = hy - 6 - (i + 1) * rh
        ln(c, M + 8 + tw * 0.47 + 4, yb + rh / 2, M + 8 + tw * 0.84 - 4)
        for k, f in [(0.84, 0.08), (0.92, 0.08)]: cb(c, M + 8 + tw * k + tw * f / 2 - 5, yb + rh / 2 - 5, 10)
    footer(c, "Future me will say thank you.")

def wins_wall(c):
    y = header(c, "MY WINS WALL")
    c.setFont("Sans", 10); c.setFillColor(G)
    c.drawString(M, y - 1, "Copy your best wins here. Read them on hard days."); c.setFillColor(black)
    y -= 12; cols, rows = 3, 8; gw = (cw - 2 * 8) / 3; gh = (y - M - 7 * 8) / rows
    for r in range(rows):
        for k in range(cols):
            x = M + k * (gw + 8); yy = y - (r + 1) * gh - r * 8
            c.setLineWidth(1); c.roundRect(x, yy, gw, gh, 7); star(c, x + 14, yy + gh - 14, 7)
            ln(c, x + 26, yy + gh - 18, x + gw - 8); ln(c, x + 8, yy + gh - 36, x + gw - 8); ln(c, x + 8, yy + gh - 54, x + gw - 8)
    footer(c, "Look how far you've come.")

def notes(c):
    y = header(c, "NOTES")
    n = int((y - M - 10) / 24)
    for i in range(n): ln(c, M, y - 18 - i * 24, W - M)


# ---------- assemble interior ----------
def build_interior(path):
    c = canvas.Canvas(path, pagesize=letter, initialFontName="Sans")
    c.setTitle(TITLE); c.setAuthor(AUTHOR)
    pages = [belongs, how_to, brain_card, lambda c: tracker(c, 1), lambda c: tracker(c, 2)]
    d = w = 0
    for mi, nw in enumerate(MONTH_WEEKS, 1):
        pages.append(lambda c, mi=mi: monthly(c, mi))
        for _ in range(nw):
            w += 1; pages.append(lambda c, w=w: weekly(c, w))
            for _ in range(5):
                d += 1; pages.append(lambda c, d=d: daily(c, d))
    pages += [wins_wall, notes, notes, notes]
    for p in pages: p(c); c.showPage()
    c.save(); return len(pages)


# ---------- cover ----------
NAVY = HexColor("#1B2A4A"); TEAL = HexColor("#16B3A3"); SUN = HexColor("#FFC93C"); CORAL = HexColor("#FF6B5B"); CREAM = HexColor("#FFF8EC")

def build_cover(path, n_pages):
    bleed = 0.125 * 72; spine = n_pages * 0.002252 * 72
    CW = 2 * bleed + 2 * W + spine; CH = H + 2 * bleed
    c = canvas.Canvas(path, pagesize=(CW, CH), initialFontName="Sans"); c.setTitle(TITLE + " - cover")
    fx = bleed + W + spine  # front panel left edge (trim)
    c.setFillColor(NAVY); c.rect(0, 0, CW, CH, fill=1, stroke=0)
    # confetti shapes (front only, away from text)
    for (x, y, r, col) in [(0.94, 0.975, 18, SUN), (0.06, 0.04, 26, CORAL), (0.95, 0.06, 12, TEAL)]:
        c.setFillColor(col); c.circle(fx + x * W, bleed + y * H, r, fill=1, stroke=0)
    # FRONT: title
    c.setFillColor(SUN); c.setFont("Sans-Bold", 15); c.drawCentredString(fx + W / 2, bleed + H - 78, "FULL SCHOOL YEAR  •  UNDATED  •  AGES 9-16")
    c.setFillColor(white); c.setFont("Sans-Bold", 62)
    c.drawCentredString(fx + W / 2, bleed + H - 150, "ADHD")
    c.setFont("Sans-Bold", 44); c.drawCentredString(fx + W / 2, bleed + H - 198, "HOMEWORK PLANNER")
    c.setFillColor(TEAL); c.roundRect(fx + W / 2 - 110, bleed + H - 240, 220, 30, 15, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Sans-Bold", 17); c.drawCentredString(fx + W / 2, bleed + H - 230, "FOR STUDENTS")
    c.setFillColor(CREAM); c.setFont("Sans", 13)
    c.drawCentredString(fx + W / 2, bleed + H - 266, "Beat procrastination, focus in sprints & finish homework")
    # straight daily-page mockup (no rotation = no skew)
    s = 0.54; pw, ph = W * s, H * s; px, py = fx + (W - pw) / 2, bleed + 54
    c.setFillColor(HexColor("#0E1830")); c.roundRect(px + 5, py - 5, pw, ph, 6, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(px, py, pw, ph, 6, fill=1, stroke=0)
    c.saveState(); c.translate(px, py); c.scale(s, s); daily(c, 1); c.restoreState()
    # callout stickers, outside the page mockup
    for (x, y, txt, col) in [(fx + 74, bleed + 400, "Focus\nSprints", CORAL), (fx + W - 74, bleed + 270, "Time\nGuessing", SUN), (fx + 74, bleed + 140, "Before I\nHand It In", TEAL)]:
        c.setFillColor(col); c.circle(x, y, 40, fill=1, stroke=0)
        c.setFillColor(NAVY if col == SUN else white); c.setFont("Sans-Bold", 11.5)
        ls = txt.split("\n"); [c.drawCentredString(x, y + 2 - i * 13 + (len(ls) - 2) * 6.5, t) for i, t in enumerate(ls)]
    c.setFillColor(white); c.setFont("Sans-Bold", 14); c.drawCentredString(fx + W / 2, bleed + 30, AUTHOR)
    # SPINE
    if n_pages >= 100:
        c.saveState(); c.translate(bleed + W + spine / 2, bleed + H / 2); c.rotate(-90)
        fs = min(14, spine * 0.5); c.setFillColor(white); c.setFont("Sans-Bold", fs); c.drawCentredString(0, -fs * 0.36, "ADHD HOMEWORK PLANNER FOR STUDENTS   \u2022   " + AUTHOR.upper())
        c.restoreState()
    # BACK
    bx = bleed; m = 54
    c.setFillColor(SUN); c.setFont("Sans-Bold", 26); c.drawString(bx + m, bleed + H - 90, "Homework, one page at a time.")
    c.setFillColor(CREAM); c.setFont("Sans", 12.5)
    blurb = ("Built for students whose brains move fast. Every box on the daily page was designed around a real "
             "executive-function struggle - getting started, losing track of steps, time slipping away, "
             "and silly mistakes at the finish line.")
    wrap(c, blurb, bx + m, bleed + H - 125, W - 2 * m, "Sans", 12.5, 17)
    bullets = ["Recharge First - snack, water, move before homework",
               "Top 3 + a tiny 2-minute first step to beat procrastination",
               "Write-every-step homework table with Guess vs Real minutes",
               "Focus Sprints with movement breaks + a hyperfocus alarm",
               "Distraction Parking Lot and a Before-I-Hand-It-In checklist",
               "Win of the Day, weekly friendship check-in, monthly reset",
               "“How My Brain Works Best” card to share with teachers"]
    y = bleed + H - 215; c.setFont("Sans", 12)
    for b in bullets:
        c.setFillColor(TEAL); c.circle(bx + m + 5, y + 4, 4, fill=1, stroke=0)
        c.setFillColor(white); c.drawString(bx + m + 18, y, b); y -= 22
    c.setFillColor(SUN); c.setFont("Sans-Bold", 13)
    c.drawString(bx + m, y - 14, "Undated  •  180 daily  •  36 weekly  •  9 monthly pages  •  8.5 x 11 in")
    # weekly page mini-preview
    s2 = 0.30; c.saveState(); c.translate(bx + m, bleed + 60); c.rotate(3)
    c.setFillColor(white); c.roundRect(0, 0, W * s2, H * s2, 4, fill=1, stroke=0); c.scale(s2, s2); weekly(c, 1); c.restoreState()
    c.setFillColor(CREAM); c.setFont("Sans-Italic", 9)
    c.drawString(bx + m + W * 0.30 + 24, bleed + 160, "A planner, not a treatment. Designed for")
    c.drawString(bx + m + W * 0.30 + 24, bleed + 147, "ADHD students and anyone who struggles")
    c.drawString(bx + m + W * 0.30 + 24, bleed + 134, "with focus, time and getting started.")
    # barcode zone left clear: KDP places 2" x 1.2" barcode bottom-right of back panel
    c.save(); return CW / 72, CH / 72, spine / 72


if __name__ == "__main__":
    n = build_interior("../interior.pdf")
    cw_in, ch_in, sp = build_cover("../cover.pdf", n)
    print(f"interior: {n} pages | cover: {cw_in:.3f} x {ch_in:.3f} in, spine {sp:.3f} in")
