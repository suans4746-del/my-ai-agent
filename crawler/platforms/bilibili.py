"""
Bilibili crawler module.

Searches Bilibili videos/comments for a given game keyword and returns
structured feed items.
"""

import logging
from typing import List

from playwright.sync_api import sync_playwright

from .base import BaseCrawler, FeedItem, RateLimiter


class BilibiliCrawler(BaseCrawler):
    PLATFORM_NAME = "bilibili"

    def __init__(
        self,
        rate_limiter: RateLimiter = None,
        logger: logging.Logger = None,
    ):
        super().__init__(rate_limiter=rate_limiter, logger=logger)

    def crawl(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        Placeholder Bilibili crawler using Playwright.

        Args:
            keyword: Game name or keyword to search for.
            limit: Maximum number of items to return.

        Returns:
            List of FeedItem instances.
        """
        self.logger.info("[Bilibili] Starting crawl for keyword: %s (limit=%d)", keyword, limit)
        results: List[FeedItem] = []

        # TODO: implement Playwright-based scraping for Bilibili search + comments
        # 1. Launch browser (headless)
        # 2. Navigate to https://search.bilibili.com/all?keyword=<keyword>
        # 3. Extract video metadata (title, url, author, pubdate)
        # 4. For each video, open comment page and extract top comments
        # 5. Respect rate limits (sleep between requests)
        # 6. Close browser

        self.rate_limiter.sleep_jitter(base=0.5, jitter=0.2)
        self.logger.info("[Bilibili] Crawl finished. Items collected: %d", len(results))
        return results


def crawl(keyword: str, limit: int = 10) -> List[dict]:
    """Convenience function matching the old API."""
    crawler = BilibiliCrawler()
    return crawler.run(keyword=keyword, limit=limit)
