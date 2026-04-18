"""
GameInsight Crawler
Multi-platform social media crawler using Playwright.
Respects robots.txt and rate limits.
"""

import argparse
import hashlib
import logging
import sys
import time
import sqlite3
from datetime import datetime
from pathlib import Path

from platforms import (
    crawl_bilibili,
    crawl_weibo,
    crawl_xiaohongshu,
    crawl_taptap,
    crawl_douyin,
)

DB_PATH = Path(__file__).parent.parent / "data" / "gameinsight.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def save_feed(platform: str, url: str, content: str, author: str, published_at: str, game_keyword: str):
    author_hash = hashlib.sha256(author.encode()).hexdigest()[:16]
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO feeds (platform, url, content, author_hash, published_at, game_keyword)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (platform, url, content, author_hash, published_at, game_keyword),
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


PLATFORM_MAP = {
    "bilibili": crawl_bilibili,
    "weibo": crawl_weibo,
    "xiaohongshu": crawl_xiaohongshu,
    "taptap": crawl_taptap,
    "douyin": crawl_douyin,
}


def dispatch(platform: str, keyword: str, limit: int = 10):
    """Dispatch crawl to the requested platform module."""
    if platform not in PLATFORM_MAP:
        raise ValueError(f"Unknown platform: {platform}. Supported: {list(PLATFORM_MAP.keys())}")

    logger.info("Dispatching crawler | platform=%s keyword=%s limit=%d", platform, keyword, limit)
    results = PLATFORM_MAP[platform](keyword=keyword, limit=limit)
    logger.info("Crawl complete | platform=%s items=%d", platform, len(results))
    return results


def run_all(keyword: str = "英雄联盟", limit: int = 10, rate_limit_seconds: int = 5):
    """Run crawlers for all platforms sequentially with rate limiting."""
    all_results = {}
    for name in PLATFORM_MAP:
        try:
            results = dispatch(name, keyword, limit)
            all_results[name] = results
        except Exception as exc:
            logger.error("Error crawling %s: %s", name, exc, exc_info=True)
            all_results[name] = []
        time.sleep(rate_limit_seconds)
    return all_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gameinsight-crawler",
        description="GameInsight multi-platform social media crawler",
    )
    parser.add_argument(
        "--platform",
        choices=list(PLATFORM_MAP.keys()) + ["all"],
        default="all",
        help="Platform to crawl (default: all)",
    )
    parser.add_argument(
        "--keyword",
        default="英雄联盟",
        help="Game keyword to search for (default: 英雄联盟)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max items to fetch per platform (default: 10)",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=5,
        help="Seconds to sleep between platform crawls (default: 5)",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.platform == "all":
        run_all(keyword=args.keyword, limit=args.limit, rate_limit_seconds=args.rate_limit)
    else:
        dispatch(args.platform, args.keyword, args.limit)


if __name__ == "__main__":
    main()
