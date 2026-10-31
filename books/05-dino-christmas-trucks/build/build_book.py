"""Dino Christmas Trucks: raw ChatGPT pages -> cleaned pages, interior PDF, wraparound cover.

  python3 build_book.py ../source/raw --cover 07 --max 50   (RAW_DIR: 01.png..50.png, or hf_*.png originals)

RAW_DIR holds 01.png ... 50.png (jpg/webp ok) in prompt order.
Outputs: ../final/interior.pdf + cover.pdf; ../work/ (clean/NN.png, qa_report.txt, contact_sheet.png, cover_page_coloured.png; git-ignored)
Cleaning = Book 1 pipeline: trim, upscale to fit, blur 1.2, threshold 150, 0.5" margin.
"""
import argparse, glob, os, re, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__)); BOOK = os.path.dirname(HERE); OUT = os.path.join(BOOK, "work"); FINAL = os.path.join(BOOK, "final")
for n, f in [("Lucky", "LuckiestGuy"), ("Fred", "Fredoka-SemiBold"), ("FredR", "Fredoka-Regular")]:
    pdfmetrics.registerFont(TTFont(n, f"{HERE}/fonts/{f}.ttf"))

TITLE = "Dino Christmas Trucks"; AUTHOR = "Bibhu Behera"
W, H = 8.5 * 72, 11 * 72; DPI = 300
BOX = (int(7.5 * DPI), int(10 * DPI))  # printable box inside 0.5" margins
RED = HexColor("#C8102E"); GREEN = HexColor("#0B6E4F"); GOLD = HexColor("#FFC93C"); CREAM = HexColor("#FFF8EC"); DARK = HexColor("#7A0A1C")


# ---------- cleaning + QA ----------
def clean(path):
    im = Image.open(path).convert("L"); w0, h0 = im.size
    a = np.array(im)
    grey = float(((a > 70) & (a < 190)).mean())          # shading/grey-fill indicator
    ys, xs = np.where(a < 150)
    if len(xs): im = im.crop((max(xs.min() - 20, 0), max(ys.min() - 20, 0), min(xs.max() + 20, w0), min(ys.max() + 20, h0)))
    s = min(BOX[0] / im.width, BOX[1] / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 150 else 0).convert("1")
    ink = 1 - np.array(im).mean()
    flags = []
    if h0 < 1000: flags.append(f"low-res {w0}x{h0}")
    if grey > 0.06: flags.append(f"grey/shading {grey:.0%}")
    if ink > 0.30: flags.append(f"very dark {ink:.0%} ink")
    if ink < 0.03: flags.append(f"almost empty {ink:.0%} ink")
    return im, flags, (w0, h0)


# ---------- auto-colour a page for the cover ----------
PALETTE = ["#E63946", "#2A9D8F", "#F4A261", "#FFD166", "#06D6A0", "#118AB2", "#EF476F", "#8AC926", "#FF924C", "#C77DFF"]
def autocolour(bw):
    a = np.array(bw.convert("L")) > 128                # True = white
    lab, n = ndimage.label(a)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    sizes = ndimage.sum(a, lab, range(n + 1))
    rgb = np.full(a.shape + (3,), 255, np.uint8); rnd = random.Random(7)
    for i in range(1, n + 1):
        if i in border or sizes[i] < 400: continue
        c = PALETTE[rnd.randrange(len(PALETTE))]; rgb[lab == i] = [int(c[k:k + 2], 16) for k in (1, 3, 5)]
    rgb[~a] = 0
    return Image.fromarray(rgb)


# ---------- interior ----------
def belongs(c):
    c.setFillColor(HexColor("#000000")); c.setFont("Lucky", 40); c.drawCentredString(W / 2, H - 170, "THIS BOOK")
    c.drawCentredString(W / 2, H - 218, "BELONGS TO")
    c.setStrokeColor(HexColor("#000000")); c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    c.setFillColor(HexColor("#000000")); c.setFont("FredR", 13)
    c.drawCentredString(W / 2, 120, "Merry Christmas! Colour your favourite dino trucks.")
    # simple outline snowflakes to colour
    for (x, y, r) in [(130, 260, 30), (W - 130, 300, 26), (W / 2, 200, 20), (200, 370, 18), (W - 200, 400, 22)]:
        for k in range(6):
            import math
            ang = k * math.pi / 3; c.setLineWidth(2.2); c.line(x, y, x + r * math.cos(ang), y + r * math.sin(ang))
    c.setFillColor(HexColor("#000000"))

def build_interior(pages, path):
    c = canvas.Canvas(path, pagesize=(W, H), initialFontName="FredR"); c.setTitle(TITLE + " Coloring Book"); c.setAuthor(AUTHOR)
    belongs(c); c.showPage(); c.showPage()          # title page + blank back
    for im in pages:
        iw, ih = im.width / DPI * 72, im.height / DPI * 72
        c.drawImage(ImageReader(im.convert("L")), (W - iw) / 2, (H - ih) / 2, iw, ih); c.showPage()
        c.showPage()                                   # single-sided: blank back (no bleed-through)
    c.save(); return 2 + 2 * len(pages)


# ---------- cover ----------
def snow(c, x0, y0, w, h, n, seed):
    rnd = random.Random(seed); c.setFillColor(white)
    for _ in range(n):
        c.setFillAlpha(rnd.uniform(0.25, 0.7)); c.circle(x0 + rnd.random() * w, y0 + rnd.random() * h, rnd.uniform(1.5, 4.5), fill=1, stroke=0)
    c.setFillAlpha(1)

def build_cover(cover_img, thumbs, n_imgs, n_pages, path):
    bleed = 9; spine = n_pages * 0.002252 * 72
    CW = 2 * bleed + 2 * W + spine; CH = H + 2 * bleed
    c = canvas.Canvas(path, pagesize=(CW, CH), initialFontName="FredR"); c.setTitle(TITLE + " cover")
    fx = bleed + W + spine
    c.setFillColor(RED); c.rect(0, 0, CW, CH, fill=1, stroke=0)
    snow(c, 0, 0, CW, CH, 260, 3)
    # snowy ground
    c.setFillColor(white); p = c.beginPath(); p.moveTo(0, 0); p.lineTo(0, 70)
    for i in range(0, int(CW) + 40, 40): p.curveTo(i + 10, 86, i + 30, 86, i + 40, 70)
    p.lineTo(CW, 0); p.close(); c.drawPath(p, fill=1, stroke=0)
    # FRONT title
    c.setFillColor(GOLD); c.setFont("Lucky", 66); c.drawCentredString(fx + W / 2, bleed + H - 110, "DINO")
    c.setFillColor(white); c.setFont("Lucky", 58); c.drawCentredString(fx + W / 2, bleed + H - 170, "CHRISTMAS")
    c.drawCentredString(fx + W / 2, bleed + H - 228, "TRUCKS")
    c.setFillColor(GREEN); c.roundRect(fx + W / 2 - 175, bleed + H - 276, 350, 34, 17, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Fred", 18); c.drawCentredString(fx + W / 2, bleed + H - 265, "Coloring Book for Kids Ages 4-8")
    # coloured page card
    cw_, ch_ = 360, 360 * cover_img.height / cover_img.width
    if ch_ > 400: ch_ = 400; cw_ = 400 * cover_img.width / cover_img.height
    px, py = fx + (W - cw_) / 2, bleed + 96
    c.setFillColor(DARK); c.roundRect(px - 14 + 6, py - 14 - 6, cw_ + 28, ch_ + 28, 18, fill=1, stroke=0)
    c.setFillColor(white); c.roundRect(px - 14, py - 14, cw_ + 28, ch_ + 28, 18, fill=1, stroke=0)
    c.drawImage(ImageReader(cover_img), px, py, cw_, ch_)
    # badge
    bx, by = fx + W - 92, bleed + H - 345
    c.setFillColor(GOLD); c.circle(bx, by, 50, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont("Lucky", 30); c.drawCentredString(bx, by + 2, str(n_imgs))
    c.setFont("Fred", 11); c.drawCentredString(bx, by - 16, "BIG & EASY"); c.drawCentredString(bx, by - 29, "PAGES")
    c.setFillColor(DARK); c.setFont("Fred", 15); c.drawCentredString(fx + W / 2, bleed + 30, AUTHOR)
    # SPINE (KDP: text only if > 79 pages; skip if too thin to stay 0.0625" clear)
    if n_pages > 79 and spine >= 0.2 * 72:
        fs = min(12, spine - 9); c.saveState(); c.translate(bleed + W + spine / 2, bleed + H / 2); c.rotate(-90)
        c.setFillColor(white); c.setFont("Fred", fs); c.drawCentredString(0, -fs * 0.35, f"DINO CHRISTMAS TRUCKS  •  {AUTHOR.upper()}"); c.restoreState()
    # BACK
    bx0, m = bleed, 54
    c.setFillColor(GOLD); c.setFont("Lucky", 34); c.drawString(bx0 + m, bleed + H - 96, "HO HO HONK!")
    c.setFillColor(white); c.setFont("FredR", 14)
    lines = ["Dinosaurs + trucks + Christmas = the perfect gift!",
             f"{n_imgs} big, bold pages of friendly dinosaurs driving",
             "delivery trucks, snowploughs, trains and Santa's sleigh,",
             "decorating trees and building toys in the workshop."]
    for i, t in enumerate(lines): c.drawString(bx0 + m, bleed + H - 134 - i * 20, t)
    bullets = ["Thick, simple lines - easy for ages 4-8", "Single-sided pages - no bleed-through",
               "Big 8.5 x 11 in pages", "Great stocking stuffer and holiday activity"]
    c.setFont("Fred", 14)
    for i, t in enumerate(bullets):
        y = bleed + H - 240 - i * 26; c.setFillColor(GOLD); c.circle(bx0 + m + 6, y + 5, 5, fill=1, stroke=0)
        c.setFillColor(white); c.drawString(bx0 + m + 20, y, t)
    tw = 150; th = tw * 11 / 8.5
    for i, t in enumerate(thumbs[:3]):
        x = bx0 + m + i * (tw + 22); y = bleed + 120
        c.setFillColor(white); c.roundRect(x - 6, y - 6, tw + 12, th + 12, 8, fill=1, stroke=0)
        c.drawImage(ImageReader(t.convert("L")), x, y, tw, th, preserveAspectRatio=True)
    # barcode zone (bottom-right of back, 2 x 1.2 in) left clear: thumbnails end before x = W - 0.25in - 2in
    c.save(); return CW / 72, CH / 72, spine / 72


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("raw"); ap.add_argument("--skip", default="")
    ap.add_argument("--cover", default=""); ap.add_argument("--max", type=int, default=45)
    a = ap.parse_args(); skip = {int(s) for s in a.skip.split(",") if s}
    files = sorted([f for f in glob.glob(os.path.join(a.raw, "*")) if re.match(r"^\d+\.(png|jpe?g|webp)$", os.path.basename(f), re.I)],
                   key=lambda f: int(re.match(r"\d+", os.path.basename(f)).group()))
    if not files:  # Higgsfield originals (hf_*.png): map to prompt numbers via ../source/higgsfield_urls.txt
        man = os.path.join(BOOK, "source", "higgsfield_urls.txt"); tmp = os.path.join(OUT, "numbered"); os.makedirs(tmp, exist_ok=True)
        for line in open(man):
            n, u = line.split(); src = os.path.join(a.raw, os.path.basename(u))
            if os.path.exists(src): Image.open(src).save(os.path.join(tmp, f"{n}.png"))
        files = sorted(glob.glob(os.path.join(tmp, "*.png")), key=lambda f: int(re.match(r"\d+", os.path.basename(f)).group()))
    os.makedirs(f"{OUT}/clean", exist_ok=True); os.makedirs(FINAL, exist_ok=True)
    kept, report = [], []
    for f in files:
        num = int(re.match(r"\d+", os.path.basename(f)).group())
        im, flags, size = clean(f); im.save(f"{OUT}/clean/{num:02d}.png")
        report.append(f"{num:02d}  {size[0]}x{size[1]}  {'OK' if not flags else 'CHECK: ' + '; '.join(flags)}")
        if num not in skip: kept.append((num, im))
    kept = kept[:a.max]
    open(f"{OUT}/qa_report.txt", "w").write("\n".join(report) + "\n")
    # contact sheet for review
    tw, th = 170, 220; cols = 10; rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), "white"); d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files):
        num = int(re.match(r"\d+", os.path.basename(f)).group()); t = Image.open(f"{OUT}/clean/{num:02d}.png").convert("L"); t.thumbnail((tw - 8, th - 8))
        x, y = (k % cols) * tw, (k // cols) * (th + 18); sheet.paste(t, (x + 4, y + 4)); d.text((x + 6, y + th), f"{num:02d}" + (" SKIP" if num in skip else ""), fill="red")
    sheet.save(f"{OUT}/contact_sheet.png")
    n_pages = build_interior([im for _, im in kept], f"{FINAL}/interior.pdf")
    cnum = int(a.cover) if a.cover else kept[0][0]
    cover_bw = dict(kept).get(cnum) or kept[0][1]
    small = cover_bw.resize((cover_bw.width // 3, cover_bw.height // 3), Image.LANCZOS).point(lambda v: 255 if v > 128 else 0)
    col = autocolour(small); col.save(f"{OUT}/cover_page_coloured.png")
    thumbs = [im for n, im in kept if n != cnum][1:4]
    cw, ch, sp = build_cover(col, thumbs, len(kept), n_pages, f"{FINAL}/cover.pdf")
    print(f"{len(files)} raw -> {len(kept)} used | interior {n_pages} pp | cover {cw:.3f} x {ch:.3f} in, spine {sp:.3f} in")
    print("\n".join(r for r in report if "CHECK" in r) or "QA: all pages OK")

if __name__ == "__main__":
    main()
