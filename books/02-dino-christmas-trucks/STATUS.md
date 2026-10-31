# Book 2: Dino Christmas Trucks Coloring Book

- **Status (Oct 31, 2026):** all 50 pages in (full-res originals pushed by Bibhu to raw/). Interior 102 pp + cover (17.48×11.25, spine 0.230 in with spine text) BUILT, QA passed (margins, fonts, no flagged pages). Ready to upload; publishing Sat Oct 31 (Oct 25–31 slot).
- Spec: same as Book 1. 8.5×11, B&W white paper, no bleed, matte, single-sided pages + "This book belongs to" page, $9.99, author **Bibhu Behera**, paperback only.
- Cleaning pipeline (from Book 1): upscale ~2x, blur 1.2, threshold 150, 0.5" margin.
- Cover: auto-coloured best interior page + Christmas title, Dino Doodle series look (Luckiest Guy/Fredoka).
- Raw files: `C:\Users\bibhu\VividFlow-Studio\KDP\Dino-Christmas-Trucks\raw\01.png … 50.png`.

## Build (ready, tested Oct 31)
`python3 build/build_book.py <raw folder> [--skip 07,23] [--cover 12] [--max 45]`
→ clean/NN.png, qa_report.txt (flags low-res/grey/dark/empty pages), contact_sheet.png, interior.pdf (belongs-to + single-sided pages), cover.pdf (auto-coloured page, Luckiest Guy/Fredoka embedded), then the listing in LISTING.md.
