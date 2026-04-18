# Alice Cycle Note

## What was done
- Created `crawler/platforms/` package with skeleton modules:
  - `__init__.py` — exports all platform crawl functions
  - `bilibili.py` — placeholder Bilibili crawler
  - `weibo.py` — placeholder Weibo crawler
  - `xiaohongshu.py` — placeholder Xiaohongshu crawler
  - `taptap.py` — placeholder TapTap crawler
  - `douyin.py` — placeholder Douyin crawler
- Rewrote `crawler/main.py` with:
  - `argparse` CLI entry point (`--platform`, `--keyword`, `--limit`, `--rate-limit`)
  - `PLATFORM_MAP` dispatcher
  - `dispatch()` and `run_all()` functions
  - Logging setup
- Verified syntax and ran quick smoke test (`python main.py --platform bilibili --keyword 原神 --limit 5`)
- Committed and pushed to `origin/main`

## Next steps
- Implement actual Playwright scraping logic per platform
- Add rate-limiting, retry logic, and error recovery
- Integrate data validation and storage via `save_feed()`
