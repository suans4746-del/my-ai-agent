"""
GameInsight Platform Crawlers

Each platform module exposes a `crawl(keyword: str, limit: int)` function
that returns a list of structured feed items.
"""

from .bilibili import crawl as crawl_bilibili
from .weibo import crawl as crawl_weibo
from .xiaohongshu import crawl as crawl_xiaohongshu
from .taptap import crawl as crawl_taptap
from .douyin import crawl as crawl_douyin

__all__ = [
    "crawl_bilibili",
    "crawl_weibo",
    "crawl_xiaohongshu",
    "crawl_taptap",
    "crawl_douyin",
]
