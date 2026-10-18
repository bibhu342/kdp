# KDP Learnings Log — read before every book, add 3 lines after every book

## Book 1 — Dino Trucks Coloring Book (Oct 6, 2026)
What worked
- One fixed prompt template → all 50 pages matched in style; zero rejects.
- Cleaning pipeline (upscale ~2x, blur 1.2, threshold 150, 0.5" margin) → KDP flagged no issues.
- Cover from a coloured interior page = free, matches inside, strong thumbnail.
- Single-sided pages + "This book belongs to" page = 102 pages.
Lessons / fix next time
- Ask Bibhu to name files 01–50 in prompt order (Book 1 needed manual mapping).
- ChatGPT output ~1100×1425 px — ask for largest size/upscale; aim ≥2000 px tall.
- Real print cost is $2.84 for 102 pp (not $2.25) → royalty $3.15 at $9.99. Consider 80–90 pp to cut cost.
- KDP Previewer can stall on "Checking cover" → reload the content page and relaunch; files stay saved.
- AI-disclosure answers reset after file uploads → re-check them + tick "I confirm" before Save and Continue.
- Complete KDP account (tax/bank) BEFORE the first book.
Results (fill in later)
- Live date: — | Sales wk1: — | wk4: — | BSR: — | Reviews: —

## Oct 9, 2026 — KDP "Alert from Amazon": contributor name may confuse customers
- Cause: author "Dino Doodle Press" reads like a publisher, not a person. 5-day deadline or book is unpublished.
- Fix: author = **Bibhu Behera** (real name) for all books; cover front/back updated to match; "Dino Doodle" stays as brand/series.
- Rule: author must be a person-style name. Never use "Press/Publishing/Studio" as author. Before any pen name, search Amazon/Goodreads — "Riley Brooks" was a real children's author (caught before publishing).

## Oct 15, 2026 — Planner design decisions (ADHD Homework Planner)
- Spiral/tabbed/tear-off planners (Blue Sky, Taja) can't be made on KDP — sell the same job as an undated glued paperback.
- Keep planner interiors **black & white + grey tints**. Colour interior ≈ $5.30 print vs ~$2.45 B&W at 120 pp → royalty halves. Colour lives on the cover only.
- Design each box to solve one named user problem — makes the listing write itself.
- Never claim a planner treats/fixes/improves ADHD. Say "designed for ADHD students / executive function".

## Oct 15, 2026 — ADHD Homework Planner build (code-made, 0 image credits)
- Whole 120-pp interior + wraparound cover built from one reportlab script (`build_book.py`) in a single session. Cover reuses the real daily page as a vector mockup, so it's always in sync with the inside.
- reportlab's built-in Helvetica is NOT embedded, and KDP can reject that → register TTF fonts (Liberation Sans) and pass `initialFontName`. Check with `pdffonts` (the "emb" column must say yes on every row).
- Cover maths: spine = pages × 0.002252 in (white paper). 120 pp → 0.270 in, so the full cover is 17.52 × 11.25 in. Keep the back-panel bottom-right 2×1.2 in clear for the barcode.
- Planner page plan: 90 daily + 18 weekly + 4 monthly + 8 front/back = 120. Number the pages "DAY n of 90" to build progress motivation without dating them.
- Final QA script: render every page, assert ink ≥0.375 in from the sides and ≥0.25 in from top/bottom, assert no blank pages, `pdffonts` shows no unembedded fonts. Passed on all 120 pages (min margins 0.54/0.54/0.55/0.35 in).
- Pen names don't change planner sales (cover/title/keywords do), but Bibhu keeps his real name off non-Dino lines → ADHD planner uses pen name Leah Marston.
- Expanded to a full school year (180 daily / 36 weekly / 9 monthly = 234 pp). B&W print = $1.00 + $0.012 × pages → $3.81, so price $14.99 to keep the royalty around $5. Stay undated: a "2027" dated planner sells for about 3 months and then dies, while undated sells every year.
- Cover mockup: never rotate the page preview. The tilt plus offset shadow looked skewed (Bibhu: "distorted"). Use a straight page, a small drop shadow, and stickers kept outside the page.
- Cover previews must be readable: show a zoomed crop (scale ≥0.6, ending cleanly under a box row) instead of a whole page shrunk to 0.3–0.5×, which makes the text 4–5 pt.

## Oct 16, 2026 — ADHD Homework Planner published
- Real KDP print cost for 234 pp B&W 8.5×11 = **$4.98** (not $3.81 from the old formula) → royalty $4.02 at $14.99. Always read the printing cost in KDP's pricing table before picking a price.
- KDP has no Self-Help › Time Management category any more; used Children's/Teen Study Aids + School & Education.
- Previewer passed first try with 234 pp and embedded Liberation Sans; AI disclosure stayed set after upload (fill it AFTER uploading files, then re-check).
- Chrome file upload works from the staged container copy, not the Windows path.
- KDP alert same day: long keyword-stuffed subtitle flagged as misleading. Keep subtitles short, no repeated words, no outcome promises.
Results (fill in later): Live date: — | Sales wk1: — | wk4: — | BSR: — | Reviews: —

## Oct 19, 2026 — Book 3: Dino Trucks Maze Book (built + published in one night, 0 image credits)
- Reusing Book 1 clean art as the maze-page picture + a new flood-filled cover dino = series look for free. Mazes: recursive backtracker, vector lines in reportlab; 3 levels by grid size (6–9 / 10–13 / 14–17 cols).
- Gotcha: drawing an empty (white-filled) star left the fill colour white, so following text vanished. Reset setFillGray(0) after any white fill.
- Gotcha: reportlab Canvas defaults to unembedded Helvetica even if never used. Always pass initialFontName.
- Print cost 94 pp B&W 8.5x11 = $2.84 → $3.15 royalty at $9.99. Previewer passed first try.
- Assigning a free ISBN is blocked for Claude's browser automation even with Bibhu's yes. Bibhu clicks "Assign ISBN" himself (one click), then Claude continues.
- KDP AI disclosure now asks which tool(s): enter Claude (texts) and ChatGPT (images).
- Title kept short with no repeated words (lesson from the Oct 16 planner alert).
Results (fill in later): Live date: — | Sales wk1: — | wk4: — | BSR: — | Reviews: —
