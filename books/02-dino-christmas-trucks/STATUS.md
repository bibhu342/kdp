# Book 2: Dino Christmas Trucks Coloring Book

- **Status (Oct 31, 2026):** 25 of 50 pages received and cleaned (03,04,06,07,11,26-32,34-39,42,44-47,49,50). Interior (52 pp) + cover built, QA passed. Waiting on: Bibhu to resend the other 25 for a 50-page book (recommended), or OK to publish at 25.
- Spec: same as Book 1. 8.5×11, B&W white paper, no bleed, matte, single-sided pages + "This book belongs to" page, $9.99, author **Bibhu Behera**, paperback only.
- Cleaning pipeline (from Book 1): upscale ~2x, blur 1.2, threshold 150, 0.5" margin.
- Cover: auto-coloured best interior page + Christmas title, Dino Doodle series look (Luckiest Guy/Fredoka).
- Raw files: `C:\Users\bibhu\VividFlow-Studio\KDP\Dino-Christmas-Trucks\raw\01.png … 50.png`.

## Build (ready, tested Oct 31)
`python3 build/build_book.py <raw folder> [--skip 07,23] [--cover 12] [--max 45]`
→ clean/NN.png, qa_report.txt (flags low-res/grey/dark/empty pages), contact_sheet.png, interior.pdf (belongs-to + single-sided pages), cover.pdf (auto-coloured page, Luckiest Guy/Fredoka embedded), then the listing in LISTING.md.
