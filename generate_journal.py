"""
generate_journal.py
Pulls U.S. market data, a watchlist, and news (national / international / KC & Missouri),
then renders template.html -> index.html.

Data sources (no paid API keys required):
  - Market data: Yahoo Finance via the `yfinance` package
  - News: public RSS feeds via `feedparser`

Run manually any time with:  python generate_journal.py --force
"""

import os
import sys
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import feedparser
import yfinance as yf
from jinja2 import Environment, FileSystemLoader

CENTRAL = ZoneInfo("America/Chicago")
ARCHIVE_DIR = "archive"

# ---------------------------------------------------------------------------
# Config: tickers, watchlist, and RSS sources
# ---------------------------------------------------------------------------

INDICES = [
    ("^GSPC", "S&P 500"),
    ("^DJI",  "Dow Jones"),
    ("^IXIC", "Nasdaq"),
    ("^TNX",  "10-Yr Yield"),
    ("^VIX",  "VIX"),
    ("DX-Y.NYB", "US Dollar Idx"),
    ("CL=F",  "Crude Oil"),
    ("GC=F",  "Gold"),
]

WATCHLIST = [
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("NVDA", "NVIDIA"),
    ("AMZN", "Amazon"),
    ("GOOGL", "Alphabet"),
    ("TSLA", "Tesla"),
    ("JPM", "JPMorgan Chase"),
]

NATIONAL_FEEDS = [
    ("CNBC", "https://www.cnbc.com/id/10001147/device/rss/rss.html"),
    ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/"),
    ("AP Business", "https://apnews.com/hub/business.rss"),
]

INTERNATIONAL_FEEDS = [
    ("BBC World", "http://feeds.bbci.co.uk/news/world/rss.xml"),
    ("Reuters World", "https://www.reutersagency.com/feed/?best-topics=world&post_type=best"),
]

KC_FEEDS = [
    ("KC Business Journal", "https://www.bizjournals.com/kansascity/news/rss.xml"),
    ("KSHB 41", "https://www.kshb.com/news.rss"),
    ("Missouri Independent", "https://missouriindependent.com/feed/"),
    ("Kansas Reflector", "https://kansasreflector.com/feed/"),
]

MAX_PER_SECTION = 5
MAX_KC = 6


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fmt_price(value, ticker=""):
    if value is None:
        return "—"
    if ticker in ("^TNX",):
        return f"{value:.2f}%"
    if abs(value) >= 1000:
        return f"{value:,.2f}"
    return f"{value:,.2f}"


def fmt_change(pct):
    if pct is None:
        return "—", ""
    sign = "+" if pct >= 0 else ""
    direction = "up" if pct >= 0 else "down"
    arrow = "▲" if pct >= 0 else "▼"
    return
