"""
GameInsight Platform Crawlers

Each platform module exposes a `crawl(keyword: str, limit: int)` function
that returns a list of structured feed dicts.
"""

from .bilibili import BilibiliCrawler, crawl as crawl_bilibili
from .weibo import WeiboCrawler, crawl as crawl_weibo
from .xiaohongshu import XiaohongshuCrawler, crawl as crawl_xiaohongshu
from .taptap import TapTapCrawler, crawl as crawl_taptap
from .douyin import DouyinCrawler, crawl as crawl_douyin

__all__ = [
    "BilibiliCrawler",
    "crawl_bilibili",
    "WeiboCrawler",
    "crawl_weibo",
    "XiaohongshuCrawler",
    "crawl_xiaohongshu",
    "TapTapCrawler",
    "crawl_taptap",
    "DouyinCrawler",
    "crawl_douyin",
]
