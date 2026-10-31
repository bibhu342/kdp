# Book 05: Dino Christmas Trucks Coloring Book

**PUBLISHED Oct 31, 2026 (in review).** $9.99 · 102 pp · free KDP ISBN · series Dino Trucks Activity Books. ISBN/ASIN: _fill in when live_.

- **Status:** all 50 pages in (full-res originals pushed by Bibhu to raw/). Interior 102 pp + cover (17.48×11.25, spine 0.230 in with spine text) BUILT, QA passed (margins, fonts, no flagged pages). Ready to upload; publishing Sat Oct 31 (Oct 25–31 slot).
- Spec: same as Book 1. 8.5×11, B&W white paper, no bleed, matte, single-sided pages + "This book belongs to" page, $9.99, author **Bibhu Behera**, paperback only.
- Cleaning pipeline (from Book 1): upscale ~2x, blur 1.2, threshold 150, 0.5" margin.
- Cover: auto-coloured best interior page + Christmas title, Dino Doodle series look (Luckiest Guy/Fredoka).
- Raw files: `source/raw/` (Higgsfield originals, mapped to prompt numbers by `source/higgsfield_urls.txt`). Prompts: `source/PROMPTS.md`.

## Build (ready, tested Oct 31)
`cd build && python3 build_book.py ../source/raw --cover 07 --max 50`
→ `final/interior.pdf` + `final/cover.pdf`; working files (clean pages, QA report, contact sheet) in `work/` (git-ignored).
