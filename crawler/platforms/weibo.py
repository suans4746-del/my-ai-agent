"""
Weibo crawler module.

Searches Weibo posts/comments for a given game keyword and returns
structured feed items.
"""

import logging
from typing import List

from .base import BaseCrawler, FeedItem, RateLimiter


class WeiboCrawler(BaseCrawler):
    PLATFORM_NAME = "weibo"

    def __init__(
        self,
        rate_limiter: RateLimiter = None,
        logger: logging.Logger = None,
    ):
        super().__init__(rate_limiter=rate_limiter, logger=logger)

    def crawl(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        Placeholder Weibo crawler using Playwright.

        Args:
            keyword: Game name or keyword to search for.
            limit: Maximum number of items to return.

        Returns:
            List of FeedItem instances.
        """
        self.logger.info("[Weibo] Starting crawl for keyword: %s (limit=%d)", keyword, limit)
        results: List[FeedItem] = []

        # TODO: implement Playwright-based scraping for Weibo search
        # 1. Launch browser (headless)
        # 2. Navigate to https://s.weibo.com/weibo?q=<keyword>
        # 3. Extract post cards (content, author, timestamp, engagement)
        # 4. Handle pagination (scroll or click next)
        # 5. Respect rate limits (sleep between pages)
        # 6. Close browser

        self.rate_limiter.sleep_jitter(base=0.5, jitter=0.2)
        self.logger.info("[Weibo] Crawl finished. Items collected: %d", len(results))
        return results


def crawl(keyword: str, limit: int = 10) -> List[dict]:
    """Convenience function matching the old API."""
    crawler = WeiboCrawler()
    return crawler.run(keyword=keyword, limit=limit)
