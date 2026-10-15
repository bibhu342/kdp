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
- Pen names don't sell planners; cover/title/keywords do. Default to Bibhu Behera unless there's a brand reason to separate lines.
