"""Student Planner for Middle & High School — undated 8.5x11 B&W interior (142 pp) + wraparound cover.
Run: python3 build_book.py  -> ../final/interior.pdf, ../final/cover.pdf
Reuses drawing primitives from kit.py (copied from the ADHD planner build). Fonts embedded (Liberation Sans).
"""
import math
from kit import *   # box, ln, cb, dot, header, footer, lines_in, wrap, star, monthly, wins_wall, notes, W,H,M,cw, colours
import kit
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

AUTHOR = "Leah Marston"
TITLE = "Student Planner for Middle and High School"
WEEKS = 36
MONTH_WEEKS = [5, 4, 5, 4, 5, 4, 5, 4]   # 8 monthly resets, 18 weeks per semester


def bar(c, text, x, y, w, h=16):
    c.setFillColor(GR); c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    c.setFillColor(black); c.setFont("Sans-Bold", 9.5); c.drawString(x + 7, y + 4.5, text)

def labeled_line(c, x, y, label, x2, size=9):
    c.setFont("Sans", size); c.drawString(x, y, label); ln(c, x + c.stringWidth(label, "Sans", size) + 5, y - 1, x2)

def table(c, x, y_top, w, cols, rows, rh, head_size=8.5, tick_cols=()):
    """cols=[(name,frac)]; draws header + grid lines. returns y of bottom."""
    xx = x
    c.setFont("Sans-Bold", head_size)
    for n, f in cols: c.drawString(xx + 3, y_top - 9, n); xx += w * f
    top = y_top - 14
    for i in range(rows + 1): ln(c, x, top - i * rh, x + w)
    xx = x
    for n, f in cols[:-1]:
        xx += w * f; c.setStrokeColor(L); c.setLineWidth(0.6); c.line(xx, y_top + 2, xx, top - rows * rh); c.setStrokeColor(black)
    xx = x
    for k, (n, f) in enumerate(cols):
        if k in tick_cols: cb(c, xx + w * f / 2 - 4.5, top - rh + 5, 9) if False else None
        xx += w * f
    return top - rows * rh


# ---------------- front matter ----------------
def belongs(c):
    c.setFont("Sans-Bold", 30); c.drawCentredString(W / 2, H - 140, "THIS PLANNER")
    c.drawCentredString(W / 2, H - 177, "BELONGS TO")
    c.setLineWidth(1.5); c.roundRect(M + 40, H - 285, cw - 80, 70, 12)
    y = H - 345
    for t in ["School:", "Grade:", "School year:", "Homeroom / advisor:", "If found, please return to:", "Phone / email:"]:
        labeled_line(c, M + 40, y, t, W - M - 40, 11); y -= 34
    c.setFont("Sans-Italic", 9.5); c.setFillColor(G)
    c.drawCentredString(W / 2, M + 60, "Undated: start any week, any year. Two semesters of classes, homework, tests and goals.")
    c.setFillColor(black)

def how_to(c):
    y = header(c, "HOW TO USE THIS PLANNER")
    c.setFont("Sans", 10); c.setFillColor(G)
    c.drawString(M, y - 1, "Ten minutes on Sunday and five minutes a day keeps the whole week under control."); c.setFillColor(black)
    steps = [
        ("1. Set up once", "Fill in My Goals, My Class Schedule and Key Dates at the front. Then do the Semester Kickoff page."),
        ("2. Plan your week", "On Sunday or Monday, fill in the Week page: what's due, your after-school plans, one goal and a to-do list."),
        ("3. Plan each day", "Pick your Top 3 and write homework as you get it: subject, what to do, due date. Tick it when it's done."),
        ("4. Track study time", "Colour in a block for every 30 minutes you study. Seeing the blocks add up feels good."),
        ("5. Study before tests", "Write every test and project in the Tests & Projects tracker, then tick one study day at a time."),
        ("6. Log your grades", "Add each score to the Grade Tracker. Spotting a dip early gives you time to fix it."),
        ("7. Reset monthly", "Use the Monthly Reset to look back at what worked, plan big dates and choose one habit."),
        ("8. Reflect each semester", "At the end of a semester, do the Reflection page. Next semester you start smarter."),
    ]
    y -= 22; gap = (y - M - 6) / len(steps)
    for t, d in steps:
        c.setFillColor(LT); c.roundRect(M, y - gap + 9, cw, gap - 7, 7, fill=1, stroke=0); c.setFillColor(black)
        c.setFont("Sans-Bold", 11.5); c.drawString(M + 12, y - 18, t)
        c.setFont("Sans", 10); wrap(c, d, M + 12, y - 34, cw - 24, "Sans", 10, 13)
        y -= gap
    footer(c, "Messy pages still count. Progress beats perfect.")

def goals(c):
    y = header(c, "MY GOALS THIS YEAR")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Big goals feel doable when you know the first step."); c.setFillColor(black)
    y -= 12; h = 222; box(c, M, y - h, cw, h, "MY 3 BIG GOALS", "school, sports, clubs, friends, anything")
    c.setFont("Sans-Bold", 8); c.setFillColor(G)
    c.drawString(M + 30, y - 33, "Goal"); c.drawString(M + cw * 0.5, y - 33, "Why it matters to me"); c.setFillColor(black)
    for i in range(3):
        yy = y - 64 - i * 52
        c.setFont("Sans-Bold", 14); c.drawString(M + 12, yy, str(i + 1))
        ln(c, M + 30, yy, M + cw * 0.46); ln(c, M + 30, yy - 18, M + cw * 0.46)
        ln(c, M + cw * 0.5, yy, M + cw - 12); ln(c, M + cw * 0.5, yy - 18, M + cw - 12)
        c.setFont("Sans", 8); c.drawString(M + 30, yy - 30, "First step:"); ln(c, M + 72, yy - 31, M + cw * 0.46)
        c.drawString(M + cw * 0.5, yy - 30, "Done by:"); ln(c, M + cw * 0.5 + 40, yy - 31, M + cw - 12)
    y -= h + 7
    h = 168; box(c, M, y - h, cw, h, "GRADES I'M AIMING FOR", "write each class and where you want to land")
    cols = [("Class", 0.30), ("Grade last year", 0.17), ("My target", 0.15), ("One thing I'll do to get there", 0.38)]
    table(c, M + 8, y - 28, cw - 16, cols, 7, 18.5)
    y -= h + 7
    hw = (cw - 8) / 2; x2 = M + hw + 8; h = 92
    box(c, M, y - h, hw, h, "ONE HABIT TO START"); lines_in(c, M, y, hw, 3, 17, 38)
    box(c, x2, y - h, hw, h, "ONE HABIT TO DROP"); lines_in(c, x2, y, hw, 3, 17, 38)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "WHEN I REACH A GOAL, I'LL REWARD MYSELF WITH", "pick something to look forward to")
    for i in range(int((h - 36) / 19)): ln(c, M + 12, M + h - 38 - i * 19, M + cw - 12)
    footer(c, "Small steps, taken often, add up.")

def schedule(c):
    y = header(c, "MY CLASS SCHEDULE")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Write times and classes. Use the A/B column if your school has A and B days."); c.setFillColor(black)
    y -= 12; h = 340; box(c, M, y - h, cw, h, "WEEKLY TIMETABLE", "period, time and class for each day")
    cols = [("Period / time", 0.16), ("Mon", 0.168), ("Tue", 0.168), ("Wed", 0.168), ("Thu", 0.168), ("Fri", 0.172)]
    table(c, M + 8, y - 28, cw - 16, cols, 9, 31)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "MY CLASSES AND TEACHERS", "so you always know who to ask")
    cols = [("Class", 0.22), ("Teacher", 0.22), ("Room", 0.09), ("Email / how to reach them", 0.31), ("Best time to ask", 0.16)]
    rows = int((h - 44) / 21)
    table(c, M + 8, M + h - 28, cw - 16, cols, rows, 21)
    footer(c, "Tip: take a photo of your timetable so it's always on your phone.")

def keydates(c):
    y = header(c, "KEY DATES")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Copy dates from the school calendar once. Check them every Sunday."); c.setFillColor(black)
    y -= 12; hw = (cw - 8) / 2; x2 = M + hw + 8; h = (y - M - 7) / 2
    for k, (x, t) in enumerate([(M, "SEMESTER 1"), (x2, "SEMESTER 2")]):
        box(c, x, y - h, hw, h, t, "date  |  what")
        n = int((h - 32) / 19)
        for i in range(n):
            yy = y - 40 - i * 19; ln(c, x + 10, yy, x + 62); ln(c, x + 68, yy, x + hw - 10)
    y -= h + 7
    h2 = y - M; box(c, M, M, hw, h2, "BREAKS, EXAMS + REPORT CARDS", "")
    for i in range(int((h2 - 32) / 19)): ln(c, M + 10, M + h2 - 40 - i * 19, M + hw - 10)
    box(c, x2, M, hw, h2, "PEOPLE WHO CAN HELP", "")
    for i in range(int((h2 - 32) / 19)): ln(c, x2 + 10, M + h2 - 40 - i * 19, x2 + hw - 10)
    footer(c, "Know the dates, skip the surprises.")

def study_guide(c):
    y = header(c, "STUDY SMARTER")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Six study habits many students find helpful. Try one this week."); c.setFillColor(black)
    tips = [("Little and often", "Four 30-minute sessions beat one big cram. Spread study over several days before a test."),
            ("Quiz yourself", "Close the book and write down what you remember. Then check. Trying to remember is how it sticks."),
            ("Teach it back", "Explain a topic out loud to a friend, a pet or a mirror. Where you get stuck is what to study."),
            ("Work in blocks", "Try 25 minutes of work, then a 5 minute break. Put your phone in another room."),
            ("Mix it up", "Switch between subjects or problem types in one session. It feels harder, but it helps."),
            ("Set up tonight", "Pack your bag, charge your laptop and write tomorrow's Top 3 before bed.")]
    y -= 14; hw = (cw - 8) / 2; bh = (y - M - 40 - 2 * 8) / 3
    for i, (t, d) in enumerate(tips):
        x = M + (i % 2) * (hw + 8); yy = y - (i // 2) * (bh + 8)
        box(c, x, yy - bh, hw, bh, f"{i + 1}. {t}")
        c.setFont("Sans", 9.5); wrap(c, d, x + 10, yy - 38, hw - 20, "Sans", 9.5, 13)
        c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(x + 10, yy - 78, "I'll try it for:"); c.setFillColor(black)
        for j in range(int((bh - 100) / 18) + 1): ln(c, x + 10, yy - 96 - j * 18, x + hw - 10)
    labeled_line(c, M, M + 6, "My best study spot:", M + cw * 0.55); labeled_line(c, M + cw * 0.6, M + 6, "Music or quiet?", M + cw)
    footer(c, "Study habits are skills. Skills get better with practice.")


# ---------------- semester pages ----------------
def kickoff(c, s):
    y = header(c, f"SEMESTER {s} KICKOFF", "Starts: ____ / ____ / ______", "Ends: ____ / ____ / ______")
    h = 280; box(c, M, y - h, cw, h, "MY CLASSES THIS SEMESTER", "goal grade + how I'll get there")
    cols = [("Class", 0.22), ("Teacher", 0.18), ("Goal grade", 0.12), ("How I'll get there", 0.48)]
    table(c, M + 8, y - 28, cw - 16, cols, 9, 25)
    y -= h + 7
    hw = (cw - 8) / 2; x2 = M + hw + 8; h = 120
    box(c, M, y - h, hw, h, "BIGGEST CHALLENGE", "and my plan for it"); lines_in(c, M, y, hw, 4, 19, 40)
    box(c, x2, y - h, hw, h, "WHAT WORKED LAST SEMESTER", "keep doing this"); lines_in(c, x2, y, hw, 4, 19, 40)
    y -= h + 7
    h = 96; box(c, M, y - h, cw, h, "MY 3 SEMESTER GOALS")
    for i in range(3):
        yy = y - 40 - i * 19; c.setFont("Sans-Bold", 11); c.drawString(M + 12, yy, str(i + 1)); ln(c, M + 28, yy - 1, M + cw - 12)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "MY STUDY SETUP", "tick what you'll do")
    items = ["A set study spot", "A regular study time", "Phone away while I work", "Bag packed the night before",
             "Ask for help early", "Weekly planner check on Sunday", "Water + snack ready", "Review notes once a week"]
    c.setFont("Sans", 9.5)
    for i, t in enumerate(items):
        x = M + 12 + (i % 2) * (cw / 2); yy = M + h - 40 - (i // 2) * 18; cb(c, x, yy); c.drawString(x + 15, yy + 1, t)
    footer(c, "A good start makes the semester easier.")

def grades(c, s, part):
    y = header(c, "GRADE TRACKER", tag=f"SEMESTER {s}  •  PAGE {part} of 2")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Write every score. Percent = score ÷ out of × 100."); c.setFillColor(black)
    y -= 12; bh = (y - M - 3 * 7) / 4
    for i in range(4):
        yy = y - i * (bh + 7)
        box(c, M, yy - bh, cw, bh, "CLASS", "")
        c.setFont("Sans", 9); c.setFillColor(black)
        ln(c, M + 52, yy - 14, M + cw * 0.45); c.setFont("Sans", 8.5); c.drawString(M + cw * 0.55, yy - 14, "Target %:"); ln(c, M + cw * 0.55 + 42, yy - 15, M + cw * 0.72)
        c.drawString(M + cw * 0.76, yy - 14, "Now:"); ln(c, M + cw * 0.76 + 26, yy - 15, M + cw - 10)
        cols = [("Assignment / test", 0.40), ("Date", 0.15), ("Score", 0.15), ("Out of", 0.15), ("%", 0.15)]
        n = int((bh - 50) / 15)
        table(c, M + 8, yy - 30, cw - 16, cols, n, 15, 8)
    footer(c, "Numbers tell you where to put your effort.")

def tests(c, s):
    y = header(c, "TESTS & PROJECTS", tag=f"SEMESTER {s}")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Write the date, then tick a study day each time you review."); c.setFillColor(black)
    y -= 12; th = y - M; box(c, M, M, cw, th, "MY TRACKER", "start early, finish calm")
    cols = [("Class", 0.13), ("Test / project", 0.22), ("Date", 0.09), ("What to review", 0.26), ("Study days", 0.18), ("Score", 0.12)]
    rows = 11; rh = (th - 44) / rows
    bottom = table(c, M + 8, y - 28, cw - 16, cols, rows, rh)
    tw = cw - 16; x0 = M + 8 + tw * (0.13 + 0.22 + 0.09 + 0.26)
    for i in range(rows):
        yb = y - 42 - (i + 1) * rh + rh / 2 - 4.5
        for k in range(4): cb(c, x0 + 8 + k * (tw * 0.18 - 16) / 3.4, yb, 9)
    footer(c, "Future you will say thank you.")


# ---------------- weekly pages ----------------
def week_overview(c, wk):
    y = header(c, "MY WEEK", "Week of: ____ / ____ / ______", tag=f"WEEK {wk} of {WEEKS}")
    h = 200; box(c, M, y - h, cw, h, "DUE THIS WEEK", "homework, tests, projects, forms")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]; dw = (cw - 16) / 5
    for i, d in enumerate(days):
        x = M + 8 + i * dw
        c.setFont("Sans-Bold", 9); c.drawCentredString(x + dw / 2, y - 34, d)
        if i: c.setStrokeColor(L); c.line(x, y - 26, x, y - h + 8); c.setStrokeColor(black)
        for j in range(7): ln(c, x + 5, y - 55 - j * 20.5, x + dw - 5)
    y -= h + 7
    h = 76; box(c, M, y - h, cw, h, "AFTER SCHOOL + WEEKEND", "practice, clubs, work, family, fun")
    d7 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]; dw = (cw - 16) / 7
    for i, d in enumerate(d7):
        x = M + 8 + i * dw
        c.setFont("Sans-Bold", 8.5); c.drawCentredString(x + dw / 2, y - 34, d)
        if i: c.setStrokeColor(L); c.line(x, y - 26, x, y - h + 8); c.setStrokeColor(black)
        ln(c, x + 5, y - 52, x + dw - 5); ln(c, x + 5, y - 66, x + dw - 5)
    y -= h + 7
    hw = (cw - 8) / 2; x2 = M + hw + 8; h = 150
    box(c, M, y - h, hw, h, "THIS WEEK I NEED TO", "")
    for i in range(8):
        yy = y - 40 - i * 13.5; cb(c, M + 10, yy, 8.5); ln(c, M + 24, yy, M + hw - 10)
    box(c, x2, y - h, hw, h, "STUDY BLOCKS", "colour 1 box per 30 min")
    for i, d in enumerate(d7):
        yy = y - 38 - i * 15; c.setFont("Sans", 8); c.drawString(x2 + 10, yy, d)
        for j in range(8): c.setLineWidth(0.7); c.rect(x2 + 38 + j * 16.5, yy - 2, 12, 10, fill=0)
    y -= h + 7
    h = 88; box(c, M, y - h, hw, h, "MY ONE GOAL THIS WEEK", "small + specific"); lines_in(c, M, y, hw, 2, 17, 38)
    c.setFont("Sans", 8.5); c.drawString(M + 10, y - h + 12, "My reward:"); ln(c, M + 58, y - h + 11, M + hw - 10)
    box(c, x2, y - h, hw, h, "HOMEWORK STREAK", "colour a star each school day")
    for i, d in enumerate(days):
        cx = x2 + 26 + i * (hw - 52) / 4; star(c, cx, y - 52, 13); c.setFont("Sans", 8); c.drawCentredString(cx, y - 78, d)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "LOOKING BACK", "fill this in on Friday or Sunday")
    c.setFont("Sans", 9)
    for i, t in enumerate(["What went well:", "What got in the way:", "Someone who helped me:", "A question to ask a teacher:", "Next week I'll try:"]):
        yy = M + h - 38 - i * 20; c.drawString(M + 12, yy, t); ln(c, M + 150, yy - 1, M + cw - 12)
    footer(c, "Plan the week, then work the plan.")

def day_block(c, y_top, hb, name):
    box(c, M, y_top - hb, cw, hb, name, "date ____ / ____")
    lw = cw * 0.34
    # left: top 3
    c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(M + 10, y_top - 34, "MY TOP 3"); c.setFillColor(black)
    for i in range(3):
        yy = y_top - 48 - i * 18; cb(c, M + 10, yy, 9); ln(c, M + 24, yy, M + lw - 8)
    c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(M + 10, y_top - 108, "STUDY TIME"); c.setFillColor(black)
    for j in range(6):
        c.setLineWidth(0.7); c.rect(M + 10 + j * 18, y_top - 124, 14, 11, fill=0)
    c.setFont("Sans", 6.5); c.setFillColor(G); c.drawString(M + 10, y_top - 134, "1 box = 30 min"); c.setFillColor(black)
    c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(M + 10, y_top - 152, "REMEMBER"); c.setFillColor(black)
    ln(c, M + 10, y_top - 168, M + lw - 8); ln(c, M + 10, y_top - 184, M + lw - 8)
    # right: homework table
    tx = M + lw + 4; tw = cw - lw - 12
    cols = [("Class", 0.2), ("Homework", 0.56), ("Due", 0.13), ("Done", 0.11)]
    rows = 7; rh = (hb - 40 - 30) / 7
    c.setFont("Sans-Bold", 8); xx = tx
    for n, f in cols: c.drawString(xx + 3, y_top - 34, n); xx += tw * f
    for i in range(rows + 1): ln(c, tx, y_top - 40 - i * rh, tx + tw)
    xx = tx
    for n, f in cols[:-1]:
        xx += tw * f; c.setStrokeColor(L); c.setLineWidth(0.6); c.line(xx, y_top - 28, xx, y_top - 40 - rows * rh); c.setStrokeColor(black)
    for i in range(rows): cb(c, tx + tw * 0.89 + tw * 0.11 / 2 - 4 - 3, y_top - 40 - (i + 1) * rh + rh / 2 - 4, 8)
    # bottom strip
    yb = y_top - hb + 12
    c.setFont("Sans", 8.5); c.drawString(M + 10, yb, "Mood:")
    for j in range(5): dot(c, M + 48 + j * 17, yb + 3, 5)
    c.drawString(M + 150, yb, "Tomorrow I need:"); ln(c, M + 232, yb - 1, M + cw - 10)

def days_a(c, wk):
    y = header(c, "DAILY PLAN", "Mon  •  Tue  •  Wed", tag=f"WEEK {wk}")
    hb = (y - M - 2 * 7) / 3
    for i, d in enumerate(["MONDAY", "TUESDAY", "WEDNESDAY"]): day_block(c, y - i * (hb + 7), hb, d)
    footer(c, "Do the hard thing first.")

def days_b(c, wk):
    y = header(c, "DAILY PLAN", "Thu  •  Fri  •  Weekend", tag=f"WEEK {wk}")
    hb = (y - M - 2 * 7) / 3
    for i, d in enumerate(["THURSDAY", "FRIDAY"]): day_block(c, y - i * (hb + 7), hb, d)
    yt = y - 2 * (hb + 7); box(c, M, yt - hb, cw, hb, "WEEKEND", "catch up, get ahead, recharge")
    hw = (cw - 24) / 2
    for k, nm in enumerate(["SATURDAY", "SUNDAY"]):
        x = M + 10 + k * (hw + 4)
        c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(x, yt - 34, nm + " TOP 3"); c.setFillColor(black)
        for i in range(3):
            yy = yt - 48 - i * 17; cb(c, x, yy, 9); ln(c, x + 14, yy, x + hw - 4)
    c.setFont("Sans-Bold", 8); c.setFillColor(G); c.drawString(M + 10, yt - 104, "NEXT WEEK PREP"); c.setFillColor(black)
    preps = ["Bag packed", "Laptop charged", "Forms signed", "Supplies ready", "Plan checked"]
    c.setFont("Sans", 8.5)
    for i, t in enumerate(preps):
        x = M + 10 + i * (cw - 20) / 5; cb(c, x, yt - 120, 9); c.drawString(x + 13, yt - 119, t)
    labeled_line(c, M + 10, yt - 142, "Something fun I'm doing:", M + cw - 10, 8.5)
    labeled_line(c, M + 10, yt - 164, "Catch up on:", M + cw - 10, 8.5)
    labeled_line(c, M + 10, yt - 186, "Get ahead on:", M + cw - 10, 8.5)
    footer(c, "Rest is part of the plan.")


# ---------------- back matter ----------------
def reflection(c, s):
    y = header(c, f"SEMESTER {s} REFLECTION")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "Look back before you move on. Be kind and be honest."); c.setFillColor(black)
    y -= 12; hw = (cw - 8) / 2; x2 = M + hw + 8; h = 136
    box(c, M, y - h, hw, h, "I'M PROUD OF"); lines_in(c, M, y, hw, 5, 19, 40)
    box(c, x2, y - h, hw, h, "MY BEST CLASS WAS... BECAUSE"); lines_in(c, x2, y, hw, 5, 19, 40)
    y -= h + 7
    box(c, M, y - h, hw, h, "WHAT WAS HARD"); lines_in(c, M, y, hw, 5, 19, 40)
    box(c, x2, y - h, hw, h, "WHAT HELPED ME MOST"); lines_in(c, x2, y, hw, 5, 19, 40)
    y -= h + 7
    h = 124; box(c, M, y - h, cw, h, "MY GRADES: BEFORE AND AFTER", "")
    cols = [("Class", 0.34), ("Goal", 0.14), ("Final grade", 0.18), ("Hit it?", 0.12), ("Note to self", 0.22)]
    table(c, M + 8, y - 28, cw - 16, cols, 5, 17)
    y -= h + 7
    h = y - M; box(c, M, M, cw, h, "NEXT SEMESTER I WILL", "three changes")
    for i in range(3):
        yy = M + h - 40 - i * 20; c.setFont("Sans-Bold", 11); c.drawString(M + 12, yy, str(i + 1)); ln(c, M + 28, yy - 1, M + cw - 12)
    footer(c, "Every semester teaches you something.")

def reading_log(c, part):
    y = header(c, "BOOKS I'VE READ", tag=f"PAGE {part} of 2")
    c.setFont("Sans", 10); c.setFillColor(G); c.drawString(M, y - 1, "School reading, free reading, audiobooks. All of it counts."); c.setFillColor(black)
    y -= 12; th = y - M; box(c, M, M, cw, th, "MY READING LOG", "colour the stars to rate each book")
    cols = [("Title", 0.34), ("Author", 0.22), ("Started", 0.10), ("Finished", 0.10), ("Rating", 0.24)]
    rows = 16; rh = (th - 44) / rows
    table(c, M + 8, y - 28, cw - 16, cols, rows, rh)
    tw = cw - 16; x0 = M + 8 + tw * 0.76
    for i in range(rows):
        yb = y - 42 - (i + 1) * rh + rh / 2
        for j in range(5): star(c, x0 + 14 + j * (tw * 0.24 - 20) / 4, yb, 6)
    footer(c, "A reader today, a leader tomorrow.")


# ---------------- assemble ----------------
def page_list():
    P = [belongs, how_to, goals, schedule, keydates, study_guide]
    wk = 0
    for s in (1, 2):
        P += [lambda c, s=s: kickoff(c, s), lambda c, s=s: grades(c, s, 1), lambda c, s=s: grades(c, s, 2), lambda c, s=s: tests(c, s)]
        sem_months = MONTH_WEEKS[:4] if s == 1 else MONTH_WEEKS[4:]
        for mi, nw in enumerate(sem_months, 1 if s == 1 else 5):
            P.append(lambda c, mi=mi: monthly(c, mi))
            for _ in range(nw):
                wk += 1
                P += [lambda c, w=wk: week_overview(c, w), lambda c, w=wk: days_a(c, w), lambda c, w=wk: days_b(c, w)]
        P.append(lambda c, s=s: reflection(c, s))
    P += [lambda c: reading_log(c, 1), lambda c: reading_log(c, 2), wins_wall] + [notes] * 7
    return P

def build_interior(path):
    c = canvas.Canvas(path, pagesize=letter, initialFontName="Sans")
    c.setTitle(TITLE); c.setAuthor(AUTHOR)
    P = page_list()
    for p in P: p(c); c.showPage()
    c.save(); return len(P)

if __name__ == "__main__":
    n = build_interior("../final/interior.pdf")
    print("interior pages:", n)
