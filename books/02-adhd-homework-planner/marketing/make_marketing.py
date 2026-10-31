"""A+ Content (970x600) + Pinterest pins (1000x1500) for the ADHD Homework Planner.
Run from this folder: python3 make_marketing.py  (needs src/ page renders, see README)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
NAVY = (27, 42, 74); TEAL = (22, 179, 163); SUN = (255, 201, 60); CORAL = (255, 107, 91)
CREAM = (255, 248, 236); WHITE = (255, 255, 255); INK = (30, 34, 45); MUTE = (90, 98, 115)
PF = "/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf"
IF = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def P(s, w="Bold"): return ImageFont.truetype(PF % w, s)
def I(s, w="Regular"): return ImageFont.truetype(IF % w, s)

def page(n): return Image.open(os.path.join(SRC, f"p{n}.png")).convert("RGB")
def crop(img, y0, y1, x0=0.0, x1=1.0):
    W, H = img.size; return img.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
def fit_w(img, w): return img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)
def fit_h(img, h): return img.resize((int(img.width * h / img.height), h), Image.LANCZOS)

def focus(img, y0, y1, x0, x1, aw, ah):
    """Crop page so the box (fractions) sits near the top, filling an aw x ah area, with a coral highlight."""
    W, H = img.size; cw = int(0.94 * W); ch = min(H, int(cw * ah / aw))
    top = max(0, min(int((y0 - 0.025) * H), H - ch)); left = int(0.03 * W)
    im = img.crop((left, top, left + cw, top + ch)).copy(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((int(x0 * W) - left - 10, int(y0 * H) - top - 10, int(x1 * W) - left + 10, int(y1 * H) - top + 10), 26, outline=CORAL, width=12)
    return im

def paste_card(bg, img, x, y, radius=14, shadow=True, border=None):
    w, h = img.size
    if shadow:
        sh = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((20, 26, w + 20, h + 26), radius, fill=(0, 0, 0, 70))
        sh = sh.filter(ImageFilter.GaussianBlur(9)); bg.paste(sh, (x - 20, y - 20), sh)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    bg.paste(img, (x, y), m)
    if border: ImageDraw.Draw(bg).rounded_rectangle((x, y, x + w - 1, y + h - 1), radius, outline=border, width=2)

def text_block(d, xy, text, font, fill, maxw, lead=1.18):
    x, y = xy; words = text.split(); line = ""
    for wd in words:
        t = (line + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: d.text((x, y), line, font=font, fill=fill); y += int(font.size * lead); line = wd
    if line: d.text((x, y), line, font=font, fill=fill); y += int(font.size * lead)
    return y

def pill(d, x, y, text, bg, fg, font, padx=18, h=None):
    tw = d.textlength(text, font=font); h = h or int(font.size * 1.9)
    d.rounded_rectangle((x, y, x + tw + 2 * padx, y + h), h // 2, fill=bg)
    d.text((x + padx, y + (h - font.size) / 2 - font.size * 0.12), text, font=font, fill=fg)
    return x + tw + 2 * padx

# Daily page regions (fractions of page height/width), verified against the render.
D_RECHARGE = (0.085, 0.140); D_TOP3 = (0.142, 0.252); D_HW = (0.255, 0.482)
D_ROW3 = (0.485, 0.622); D_ROW4 = (0.625, 0.757); WK_STREAK = (0.385, 0.475); L = (0.055, 0.502); R = (0.498, 0.945)

out_ap = os.path.join(HERE, "aplus"); out_pin = os.path.join(HERE, "pins")
os.makedirs(out_ap, exist_ok=True); os.makedirs(out_pin, exist_ok=True)
daily, weekly, monthly, brain, tracker, howto = page(8), page(7), page(6), page(3), page(4), page(2)

# ---------------- A+ CONTENT (970 x 600) ----------------
def aplus1():
    bg = Image.new("RGB", (970, 600), NAVY); d = ImageDraw.Draw(bg)
    d.text((48, 52), "FULL SCHOOL YEAR  •  UNDATED  •  AGES 9-16", font=I(17, "SemiBold"), fill=SUN)
    y = text_block(d, (48, 92), "Homework, one page at a time.", P(44), WHITE, 440, 1.12)
    y = text_block(d, (48, y + 22), "A daily planner designed for ADHD students and anyone who struggles to start, keep track and finish.", I(21), (210, 218, 235), 420, 1.35)
    x = 48; y += 26; f = P(18, "Medium")
    x = pill(d, x, y, "Focus Sprints", CORAL, WHITE, f) + 10; pill(d, x, y, "Time Guessing", SUN, NAVY, f)
    pill(d, 48, y + 50, "Before I Hand It In", TEAL, WHITE, f)
    img = fit_w(crop(daily, 0.02, 0.62, 0.03, 0.97), 440)
    paste_card(bg, img, 492, 48)
    bg.save(os.path.join(out_ap, "aplus-1-hero.png"))

def aplus2():
    bg = Image.new("RGB", (970, 600), CREAM); d = ImageDraw.Draw(bg)
    img = fit_h(daily, 560); paste_card(bg, img, 36, 20, border=(220, 210, 190))
    x0 = 36 + img.width + 40
    d.text((x0, 26), "Every box has one job", font=P(34), fill=NAVY)
    rows = [("Can't get started?", "Top 3 + a tiny 2-minute first step"),
            ("Forget the steps?", "Homework table: write every step"),
            ("Time slips away?", "Guess vs Real minutes"),
            ("Restless after 20 min?", "Focus sprints with move breaks"),
            ("Careless mistakes?", "Before I Hand It In checklist"),
            ("Drained after school?", "Recharge First: snack, water, move")]
    y = 92
    for q, a in rows:
        d.ellipse((x0, y + 8, x0 + 14, y + 22), fill=CORAL)
        d.text((x0 + 26, y), q, font=P(21, "Bold"), fill=INK)
        d.text((x0 + 26, y + 30), a, font=I(19), fill=MUTE)
        y += 80
    bg.save(os.path.join(out_ap, "aplus-2-every-box.png"))

def aplus3():
    bg = Image.new("RGB", (970, 600), WHITE); d = ImageDraw.Draw(bg)
    d.rectangle((0, 0, 970, 600), fill=(236, 250, 248))
    img = fit_w(crop(weekly, 0.02, 0.74, 0.03, 0.97), 470); paste_card(bg, img, 450, 36, border=(200, 230, 226))
    d.text((48, 60), "Plan the week", font=P(40), fill=NAVY)
    d.text((48, 110), "in 5 minutes", font=P(40), fill=TEAL)
    items = ["Big things due, Monday to Friday", "After-school schedule at a glance", "One goal + a reward for hitting it",
             "Homework streak: colour a star each day", "Friendship check-in with ready-to-use phrases"]
    y = 200
    for t in items:
        d.text((48, y), "✓", font=I(24, "Bold"), fill=TEAL); y = text_block(d, (82, y), t, I(21, "Medium"), INK, 340, 1.25) + 14
    bg.save(os.path.join(out_ap, "aplus-3-weekly.png"))

def aplus4():
    bg = Image.new("RGB", (970, 600), NAVY); d = ImageDraw.Draw(bg)
    d.text((48, 40), "Reset every month. Track every test.", font=P(34), fill=WHITE)
    d.text((48, 92), "9 monthly reset pages  •  Tests & projects tracker", font=I(20, "Medium"), fill=SUN)
    a = fit_w(crop(monthly, 0.02, 0.62, 0.03, 0.97), 420); b = fit_w(crop(tracker, 0.02, 0.62, 0.03, 0.97), 420)
    paste_card(bg, a, 48, 150); paste_card(bg, b, 502, 150)
    bg.save(os.path.join(out_ap, "aplus-4-monthly-tracker.png"))

def aplus5():
    bg = Image.new("RGB", (970, 600), CREAM); d = ImageDraw.Draw(bg)
    img = fit_w(crop(brain, 0.02, 0.64, 0.03, 0.97), 440); paste_card(bg, img, 490, 36, border=(220, 210, 190))
    d.text((48, 50), "A card to share", font=P(38), fill=NAVY)
    d.text((48, 98), "with teachers", font=P(38), fill=CORAL)
    y = text_block(d, (48, 168), "\"How My Brain Works Best\" helps your child explain what helps them focus, what makes it harder and the best way to remind them.", I(20), INK, 400, 1.4)
    y += 24
    for t in ["180 daily pages", "36 weekly pages", "9 monthly resets", "Undated: start any day", "Big 8.5 x 11 pages"]:
        d.text((48, y), "•", font=I(22, "Bold"), fill=TEAL); d.text((70, y), t, font=I(20, "SemiBold"), fill=INK); y += 32
    d.text((48, 560), "A planning tool, not a medical or therapeutic product.", font=I(14), fill=MUTE)
    bg.save(os.path.join(out_ap, "aplus-5-teacher-card.png"))

# ---------------- PINTEREST (1000 x 1500) ----------------
FOOT = "ADHD Homework Planner for Students  •  on Amazon"
def pin_base(dark):
    bg = Image.new("RGB", (1000, 1500), NAVY if dark else CREAM); d = ImageDraw.Draw(bg)
    d.rectangle((0, 1400, 1000, 1500), fill=TEAL if dark else NAVY)
    f = I(30, "SemiBold"); d.text(((1000 - d.textlength(FOOT, font=f)) / 2, 1433), FOOT, font=f, fill=WHITE)
    return bg, d

def pin_tip(name, kicker, title, sub, img, dark=False):
    bg, d = pin_base(dark); fg = WHITE if dark else NAVY; sf = (210, 218, 235) if dark else MUTE
    d.text((70, 80), kicker, font=I(32, "Bold"), fill=SUN if dark else CORAL)
    y = text_block(d, (70, 135), title, P(68), fg, 860, 1.12)
    y = text_block(d, (70, y + 18), sub, I(34), sf, 860, 1.35)
    ah = 1360 - y - 50
    if isinstance(img, tuple): src, box = img; img = focus(src, *box, 860, ah)
    img = fit_w(img, 860)
    if img.height > ah: img = fit_h(img, ah)
    paste_card(bg, img, (1000 - img.width) // 2, y + 50, border=None if dark else (220, 210, 190))
    bg.save(os.path.join(out_pin, name))

def pin_list(name, kicker, title, items, dark=True):
    bg, d = pin_base(dark); fg = WHITE if dark else NAVY
    d.text((70, 90), kicker, font=I(32, "Bold"), fill=SUN if dark else CORAL)
    y = text_block(d, (70, 145), title, P(70), fg, 860, 1.12) + 50
    for i, t in enumerate(items, 1):
        d.rounded_rectangle((70, y, 930, y + 150), 24, fill=(39, 58, 98) if dark else WHITE)
        d.ellipse((100, y + 40, 170, y + 110), fill=TEAL); n = str(i); fn = P(40)
        d.text((135 - d.textlength(n, font=fn) / 2, y + 46), n, font=fn, fill=WHITE)
        text_block(d, (200, y + 32 if len(t) > 32 else y + 52), t, I(36, "SemiBold"), fg, 700, 1.25)
        y += 176
    bg.save(os.path.join(out_pin, name))

def pins():
    pin_tip("pin-01-tiny-first-step.png", "HOMEWORK TIP", "Can't start homework? Make step one 2 minutes long.",
            "Write the task, then the tiniest first step. Starting is the hardest part.", (daily, (*D_TOP3, 0.055, 0.945)))
    pin_tip("pin-02-guess-vs-real.png", "TIME BLINDNESS HACK", "Guess the minutes. Then check.",
            "Writing a guess and the real time builds a feel for how long homework takes.", (daily, (*D_HW, 0.055, 0.945)), dark=True)
    pin_list("pin-03-recharge-first.png", "AFTER-SCHOOL ROUTINE", "Recharge first, homework second",
             ["Snack", "Water", "Move for 10 minutes", "A little quiet time", "Then open the planner"])
    pin_tip("pin-04-focus-sprints.png", "FOCUS IDEA", "Work 20 minutes. Move. Repeat.",
            "Fill one circle per sprint and take a short movement break between them.", (daily, (*D_ROW3, *L)))
    pin_list("pin-05-hand-it-in.png", "CATCH SILLY MISTAKES", "Check this before you hand it in",
             ["Name and date on it", "Every question answered", "Read the instructions again", "Checked one more time", "In my folder or sent"], dark=False)
    pin_tip("pin-06-parking-lot.png", "DISTRACTED?", "Park the thought. Get back to work.",
            "A Distraction Parking Lot on every page: write it down now, deal with it later.", (daily, (*D_ROW3, *R)), dark=True)
    pin_tip("pin-07-teacher-card.png", "FOR PARENTS & TEACHERS", "A 'How My Brain Works Best' card",
            "Your child fills it in, then shares it with teachers so they know what helps.", (brain, (0.10, 0.62, 0.055, 0.945)))
    # product pins
    W, H = Image.open(os.path.join(SRC, "cover.png")).size
    front = Image.open(os.path.join(SRC, "cover.png")).convert("RGB").crop((int(W * (1 - 8.625 / 17.777)), int(H * 0.125 / 11.25), int(W * (1 - 0.125 / 17.777)), int(H * (1 - 0.125 / 11.25))))
    bg, d = pin_base(False)
    d.text((70, 80), "UNDATED  •  FULL SCHOOL YEAR", font=I(32, "Bold"), fill=CORAL)
    y = text_block(d, (70, 135), "The homework planner built for ADHD brains", P(64), NAVY, 860, 1.12)
    c = fit_h(front, 1340 - y - 70); paste_card(bg, c, (1000 - c.width) // 2, y + 40, radius=6)
    bg.save(os.path.join(out_pin, "pin-08-cover.png"))
    bg, d = pin_base(True)
    d.text((70, 80), "LOOK INSIDE", font=I(32, "Bold"), fill=SUN)
    y = text_block(d, (70, 135), "180 days, 36 weeks, 9 monthly resets", P(60), WHITE, 860, 1.12) + 40
    tw = 410; gap = 40; cells = [daily, weekly, monthly, brain]
    for i, pg in enumerate(cells):
        t = fit_w(pg, tw); t = t.crop((0, 0, tw, min(t.height, (1360 - y - gap) // 2)))
        paste_card(bg, t, 70 + (i % 2) * (tw + gap), y + (i // 2) * (t.height + gap), radius=10)
    bg.save(os.path.join(out_pin, "pin-09-look-inside.png"))
    pin_tip("pin-10-homework-streak.png", "MOTIVATION", "Colour a star for every homework day",
            "A weekly homework streak makes progress visible, plus one small goal and a reward.", (weekly, (WK_STREAK[0], WK_STREAK[1], 0.50, 0.945)), dark=True)

for f in (aplus1, aplus2, aplus3, aplus4, aplus5, pins): f()
print("done")
