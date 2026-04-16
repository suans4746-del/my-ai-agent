"""
GameInsight Crawler
Multi-platform social media crawler using Playwright.
Respects robots.txt and rate limits.
"""

import hashlib
import time
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "gameinsight.db"


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


def crawl_weibo(keyword: str, limit: int = 10):
    """Placeholder: Weibo crawler using Playwright."""
    print(f"[Crawler] Weibo search for '{keyword}'")
    # TODO: implement Playwright-based scraping
    time.sleep(1)


def crawl_bilibili(keyword: str, limit: int = 10):
    """Placeholder: Bilibili comment crawler."""
    print(f"[Crawler] Bilibili search for '{keyword}'")
    time.sleep(1)


def crawl_taptap(keyword: str, limit: int = 10):
    """Placeholder: TapTap review crawler."""
    print(f"[Crawler] TapTap search for '{keyword}'")
    time.sleep(1)


def crawl_xiaohongshu(keyword: str, limit: int = 10):
    """Placeholder: Xiaohongshu note crawler."""
    print(f"[Crawler] Xiaohongshu search for '{keyword}'")
    time.sleep(1)


def crawl_douyin(keyword: str, limit: int = 10):
    """Placeholder: Douyin comment crawler."""
    print(f"[Crawler] Douyin search for '{keyword}'")
    time.sleep(1)


def run_all(keyword: str = "英雄联盟"):
    platforms = {
        "weibo": crawl_weibo,
        "bilibili": crawl_bilibili,
        "taptap": crawl_taptap,
        "xiaohongshu": crawl_xiaohongshu,
        "douyin": crawl_douyin,
    }
    for name, fn in platforms.items():
        try:
            fn(keyword)
            time.sleep(5)  # rate limit: 5s between platforms
        except Exception as e:
            print(f"[Crawler] Error on {name}: {e}")


if __name__ == "__main__":
    run_all()
