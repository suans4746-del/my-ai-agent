"""
Base crawler module for GameInsight.

Provides:
- Abstract base class for all platform crawlers
- Rate limiting utilities
- Structured logging setup
- Feed item validation
"""

import abc
import logging
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure structured logging for the crawler package."""
    logger = logging.getLogger("gameinsight.crawler")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


# ---------------------------------------------------------------------------
# Rate Limiting
# ---------------------------------------------------------------------------

class RateLimiter:
    """Simple token-bucket-like rate limiter with jitter."""

    def __init__(
        self,
        min_delay: float = 5.0,
        max_delay: float = 10.0,
        burst: int = 1,
    ):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.burst = burst
        self._tokens = burst
        self._last_request = 0.0

    def acquire(self) -> None:
        """Block until the next request is allowed."""
        now = time.time()
        elapsed = now - self._last_request
        delay = random.uniform(self.min_delay, self.max_delay)

        if elapsed < delay:
            sleep_time = delay - elapsed
            time.sleep(sleep_time)

        self._last_request = time.time()

    def sleep_jitter(self, base: float = 1.0, jitter: float = 0.5) -> None:
        """Sleep for base +/- jitter seconds."""
        time.sleep(max(0.0, base + random.uniform(-jitter, jitter)))


# ---------------------------------------------------------------------------
# Feed Item
# ---------------------------------------------------------------------------

@dataclass
class FeedItem:
    """Standardised feed item returned by every platform crawler."""

    platform: str
    url: str
    content: str
    author: str
    published_at: Optional[str] = None
    game_keyword: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "url": self.url,
            "content": self.content,
            "author": self.author,
            "published_at": self.published_at,
            "game_keyword": self.game_keyword,
            **self.metadata,
        }


# ---------------------------------------------------------------------------
# Abstract Base Crawler
# ---------------------------------------------------------------------------

class BaseCrawler(abc.ABC):
    """Abstract base class that all platform crawlers must implement."""

    PLATFORM_NAME: str = ""

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.rate_limiter = rate_limiter or RateLimiter()
        self.logger = logger or setup_logging()

    @abc.abstractmethod
    def crawl(self, keyword: str, limit: int = 10) -> List[FeedItem]:
        """
        Crawl the platform for content matching *keyword*.

        Args:
            keyword: Game name or keyword to search for.
            limit: Maximum number of items to return.

        Returns:
            List of FeedItem instances.
        """
        ...

    def validate_items(self, items: List[FeedItem]) -> List[FeedItem]:
        """Remove invalid or empty items."""
        valid: List[FeedItem] = []
        for item in items:
            if not item.platform or not item.content:
                self.logger.warning("Skipping invalid item: missing platform or content")
                continue
            valid.append(item)
        return valid

    def run(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Wrapper around crawl() that applies rate limiting, validation,
        and converts results to plain dicts.
        """
        self.logger.info(
            "[%s] Starting crawl for keyword: %s (limit=%d)",
            self.PLATFORM_NAME,
            keyword,
            limit,
        )
        try:
            items = self.crawl(keyword=keyword, limit=limit)
            items = self.validate_items(items)
        except Exception as exc:
            self.logger.error(
                "[%s] Crawl failed: %s", self.PLATFORM_NAME, exc, exc_info=True
            )
            items = []

        self.logger.info(
            "[%s] Crawl finished. Items collected: %d", self.PLATFORM_NAME, len(items)
        )
        return [item.to_dict() for item in items]
