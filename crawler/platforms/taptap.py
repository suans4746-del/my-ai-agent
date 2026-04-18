"""
TapTap crawler module.

Searches TapTap reviews/forum posts for a given game keyword and returns
structured feed items.
"""

import logging
from typing import List

from .base import BaseCrawler, FeedItem, RateLimiter


class TapTapCrawler(BaseCrawler):
    PLATFORM_NAME = "taptap"

    def __init__(
        self,
        rate_limiter: RateLimiter = None,
        logger: logging.Logger = None,
    ):
        super().__init__(rate_limiter=rate_limiter, logger=logger)

    def crawl(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        Placeholder TapTap crawler using Playwright.

        Args:
            keyword: Game name or keyword to search for.
            limit: Maximum number of items to return.

        Returns:
            List of FeedItem instances.
        """
        self.logger.info("[TapTap] Starting crawl for keyword: %s (limit=%d)", keyword, limit)
        results: List[FeedItem] = []

        # TODO: implement Playwright-based scraping for TapTap search
        # 1. Launch browser (headless)
        # 2. Navigate to https://www.taptap.cn/search?q=<keyword>
        # 3. Select game result and open reviews tab
        # 4. Extract review cards (content, author, rating, version, timestamp)
        # 5. Handle pagination (click load-more or page numbers)
        # 6. Respect rate limits (sleep between requests)
        # 7. Close browser

        self.rate_limiter.sleep_jitter(base=0.5, jitter=0.2)
        self.logger.info("[TapTap] Crawl finished. Items collected: %d", len(results))
        return results


def crawl(keyword: str, limit: int = 10) -> List[dict]:
    """Convenience function matching the old API."""
    crawler = TapTapCrawler()
    return crawler.run(keyword=keyword, limit=limit)
