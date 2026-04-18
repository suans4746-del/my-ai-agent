"""
Douyin crawler module.

Searches Douyin video comments for a given game keyword and returns
structured feed items.
"""

import logging
from typing import List

from .base import BaseCrawler, FeedItem, RateLimiter


class DouyinCrawler(BaseCrawler):
    PLATFORM_NAME = "douyin"

    def __init__(
        self,
        rate_limiter: RateLimiter = None,
        logger: logging.Logger = None,
    ):
        super().__init__(rate_limiter=rate_limiter, logger=logger)

    def crawl(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        Placeholder Douyin crawler using Playwright.

        Args:
            keyword: Game name or keyword to search for.
            limit: Maximum number of items to return.

        Returns:
            List of FeedItem instances.
        """
        self.logger.info("[Douyin] Starting crawl for keyword: %s (limit=%d)", keyword, limit)
        results: List[FeedItem] = []

        # TODO: implement Playwright-based scraping for Douyin search
        # 1. Launch browser (headless)
        # 2. Navigate to https://www.douyin.com/search/<keyword>
        # 3. Extract video cards (title, url, author, likes)
        # 4. Open videos and extract top comments
        # 5. Handle infinite scroll pagination
        # 6. Respect rate limits (sleep between scrolls)
        # 7. Close browser

        self.rate_limiter.sleep_jitter(base=0.5, jitter=0.2)
        self.logger.info("[Douyin] Crawl finished. Items collected: %d", len(results))
        return results


def crawl(keyword: str, limit: int = 10) -> List[dict]:
    """Convenience function matching the old API."""
    crawler = DouyinCrawler()
    return crawler.run(keyword=keyword, limit=limit)
