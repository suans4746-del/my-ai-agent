# Alice Cycle Note

## What was done
- Created `crawler/platforms/base.py` with:
  - `BaseCrawler` abstract base class (ABC) with `crawl()`, `validate_items()`, and `run()`
  - `RateLimiter` with jitter and token-bucket-like `acquire()`
  - `FeedItem` dataclass for standardised feed items
  - `setup_logging()` for structured logging
- Refactored all 5 platform modules to inherit from `BaseCrawler`:
  - `bilibili.py`, `weibo.py`, `taptap.py`, `xiaohongshu.py`, `douyin.py`
  - Each exposes a top-level `crawl()` convenience function preserving old API
- Updated `crawler/platforms/__init__.py` to export both Crawler classes and convenience functions
- Enhanced `crawler/main.py`:
  - Uses `setup_logging()` and `RateLimiter` from `base.py`
  - Added `--init-db` CLI flag to create the SQLite `feeds` table
  - `run_all()` now uses `RateLimiter.acquire()` between platforms
- Verified syntax (`py_compile`), imports, and ran smoke tests:
  - `python main.py --init-db` ✅
  - `python main.py --platform bilibili --keyword "原神" --limit 3` ✅
- Committed and pushed to branch `alice/crawler-scaffold`

## Next steps
- Implement actual Playwright scraping logic per platform
- Add retry logic with exponential backoff in `BaseCrawler`
- Integrate data validation and storage via `save_feed()`
- Wire crawler to backend API or scheduler (APScheduler)
