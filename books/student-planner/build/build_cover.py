"""Student Planner cover (wraparound, vector, embedded fonts) -> ../final/cover.pdf + cover_preview.png"""
import sys
from build_book import *
from reportlab.lib.colors import HexColor, white
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 142
GREEN = HexColor("#17503F"); DARK = HexColor("#0C2E24"); YEL = HexColor("#FFD23F"); CORAL = HexColor("#FF6B4A"); MINT = HexColor("#7FD6A8"); CREAM = HexColor("#FFF6E3")

def mock(c, x, y_top, w, h, fn, scale, args=()):
    c.setFillColor(DARK); c.roundRect(x + 5, y_top - h - 5, w, h, 10, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(x, y_top - h, w, h, 10, fill=1, stroke=0)
    c.saveState(); p = c.beginPath(); p.roundRect(x, y_top - h, w, h, 10); c.clipPath(p, stroke=0, fill=0)
    c.translate(x + 14 - M * scale, y_top - 14 - (H - M) * scale); c.scale(scale, scale); fn(c, *args); c.restoreState()
    c.setFillColor(black)

def cover(path, n):
    bleed = 9.0; spine = n * 0.002252 * 72
    CW = 2 * bleed + 2 * W + spine; CH = H + 2 * bleed
    c = canvas.Canvas(path, pagesize=(CW, CH), initialFontName="Sans"); c.setTitle(TITLE + " - cover")
    c.setFillColor(GREEN); c.rect(0, 0, CW, CH, fill=1, stroke=0)
    fx = bleed + W + spine; cx = fx + W / 2; top = bleed + H
    # ---- FRONT
    c.setFillColor(YEL); c.setFont("Sans-Bold", 14.5); c.drawCentredString(cx, top - 70, "UNDATED  •  2 SEMESTERS  •  GRADES 6-12")
    c.setFillColor(white); c.setFont("Sans-Bold", 72); c.drawCentredString(cx, top - 142, "STUDENT")
    c.drawCentredString(cx, top - 212, "PLANNER")
    c.setFillColor(CORAL); c.roundRect(cx - 190, top - 262, 380, 36, 18, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Sans-Bold", 19); c.drawCentredString(cx, top - 250, "FOR MIDDLE & HIGH SCHOOL")
    c.setFillColor(CREAM); c.setFont("Sans", 13); c.drawCentredString(cx, top - 290, "Weekly plans, daily pages, grade tracker and study log")
    pills = [("Grade Tracker", YEL, DARK), ("Study Blocks", MINT, DARK), ("Goals", CORAL, white)]
    c.setFont("Sans-Bold", 12.5); gap = 10; pws = [c.stringWidth(t, "Sans-Bold", 12.5) + 26 for t, _, _ in pills]
    x = cx - (sum(pws) + 2 * gap) / 2; py = top - 334
    for (t, bg, fg), pw in zip(pills, pws):
        c.setFillColor(bg); c.roundRect(x, py, pw, 26, 13, fill=1, stroke=0); c.setFillColor(fg); c.drawCentredString(x + pw / 2, py + 8.5, t); x += pw + gap
    s = 0.84; mw = (W - 2 * M) * s + 28; mock(c, cx - mw / 2, py - 18, mw, 330, week_overview, s, (1,))
    c.setFillColor(white); c.setFont("Sans-Bold", 15); c.drawCentredString(cx, bleed + 34, AUTHOR)
    # ---- SPINE
    c.saveState(); c.translate(bleed + W + spine / 2, bleed + H / 2); c.rotate(-90)
    c.setFillColor(YEL); c.setFont("Sans-Bold", 12.5); c.drawCentredString(0, -4.5, "STUDENT PLANNER FOR MIDDLE AND HIGH SCHOOL   •   " + AUTHOR.upper()); c.restoreState()
    # ---- BACK
    bx = bleed; m = 54
    c.setFillColor(YEL); c.setFont("Sans-Bold", 27); c.drawString(bx + m, top - 90, "Plan it. Do it. Check it off.")
    c.setFillColor(CREAM); blurb = ("One planner for the whole school year. Write down classes, homework and tests, plan each week, "
                                     "log your grades and spot problems early. Simple pages, big boxes, room to write.")
    c.setFont("Sans", 12.5); wrap(c, blurb, bx + m, top - 124, W - 2 * m, "Sans", 12.5, 17)
    bullets = ["Weekly overview with due dates, study blocks and a homework streak",
               "Daily pages for 5 school days plus the weekend, 36 weeks",
               "Grade Tracker for every class, both semesters",
               "Tests & Projects tracker with study-day checkboxes",
               "Goals, class schedule, key dates and a study guide",
               "Monthly resets and a reflection page each semester",
               "Reading log, wins wall and notes pages"]
    y = top - 205; c.setFont("Sans", 12)
    for b in bullets:
        c.setFillColor(MINT); c.circle(bx + m + 5, y + 4, 4, fill=1, stroke=0); c.setFillColor(white); c.drawString(bx + m + 18, y, b); y -= 22
    c.setFillColor(YEL); c.setFont("Sans-Bold", 13); c.drawString(bx + m, y - 14, "Undated  •  36 weeks  •  142 pages  •  8.5 x 11 in")
    s2 = 0.58; ww = (W - 2 * M) * s2 + 28
    mock(c, bx + m, bleed + 365, ww, 320, days_a, s2, (1,))
    c.save(); return CW / 72, CH / 72, spine / 72

if __name__ == "__main__":
    a, b, sp = cover("../final/cover.pdf", PAGES); print(f"cover {a:.3f} x {b:.3f} in, spine {sp:.4f} in")
