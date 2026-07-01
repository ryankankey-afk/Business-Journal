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
    return f"{arrow} {sign}{pct:.2f}%", direction


def safe_quote(symbol):
    """Fetch last price + % change for a symbol. Returns (price, pct_change) or (None, None)."""
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="5d")
        if hist.empty or len(hist) < 2:
            return None, None
        last = hist["Close"].iloc[-1]
        prev = hist["Close"].iloc[-2]
        pct = ((last - prev) / prev) * 100
        return float(last), float(pct)
    except Exception as e:
        print(f"[warn] quote fetch failed for {symbol}: {e}", file=sys.stderr)
        return None, None


def safe_history_5d(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="5d", interval="30m")
        if hist.empty:
            hist = t.history(period="5d")
        labels = [d.strftime("%a %-I:%M%p") if hasattr(d, "strftime") else str(d) for d in hist.index]
        values = [round(float(v), 2) for v in hist["Close"].tolist()]
        return labels, values
    except Exception as e:
        print(f"[warn] history fetch failed for {symbol}: {e}", file=sys.stderr)
        return [], []


def safe_feed_entries(feeds, limit):
    """Try a list of (source_name, url) feeds in order, collecting entries until `limit` reached."""
    items = []
    for source_name, url in feeds:
        if len(items) >= limit:
            break
        try:
            parsed = feedparser.parse(url)
            if parsed.bozo and not parsed.entries:
                continue
            for entry in parsed.entries[: (limit - len(items))]:
                title = getattr(entry, "title", "").strip()
                link = getattr(entry, "link", "#")
                if not title:
                    continue
                items.append({"title": title, "link": link, "source": source_name})
                if len(items) >= limit:
                    break
        except Exception as e:
            print(f"[warn] feed fetch failed for {source_name}: {e}", file=sys.stderr)
            continue
    return items


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build():
    now_ct = datetime.now(CENTRAL)

    # --- indices ---
    ticker_items = []
    index_cards = []
    for symbol, name in INDICES:
        price, pct = safe_quote(symbol)
        change_str, direction = fmt_change(pct)
        price_str = fmt_price(price, symbol)
        ticker_items.append({"symbol": name, "price": price_str, "change": change_str, "dir": direction})
        index_cards.append({"name": name, "price": price_str, "change": change_str, "dir": direction})

    # --- S&P 500 5-day chart ---
    spx_labels, spx_values = safe_history_5d("^GSPC")
    if not spx_values:
        spx_labels, spx_values = ["—"], [0]
    spx_range_label = f"{spx_labels[0]} → {spx_labels[-1]}" if len(spx_labels) > 1 else ""

    # --- watchlist ---
    watchlist = []
    for symbol, name in WATCHLIST:
        price, pct = safe_quote(symbol)
        change_str, direction = fmt_change(pct)
        watchlist.append({
            "symbol": symbol, "name": name,
            "price": fmt_price(price), "change": change_str, "dir": direction,
        })

    # --- news ---
    national_news = safe_feed_entries(NATIONAL_FEEDS, MAX_PER_SECTION)
    international_news = safe_feed_entries(INTERNATIONAL_FEEDS, MAX_PER_SECTION)
    kc_news = safe_feed_entries(KC_FEEDS, MAX_KC)

    env = Environment(loader=FileSystemLoader("."), autoescape=False)
    template = env.get_template("template.html")

    html = template.render(
        generated_date=now_ct.strftime("%A, %B %-d, %Y"),
        generated_time_ct=now_ct.strftime("%-I:%M %p"),
        ticker_items=ticker_items,
        indices=index_cards,
        spx_labels=json.dumps(spx_labels),
        spx_values=json.dumps(spx_values),
        spx_range_label=spx_range_label,
        watchlist=watchlist,
        national_news=national_news,
        international_news=international_news,
        kc_news=kc_news,
        kc_half=(len(kc_news) + 1) // 2,
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # --- save a dated copy into the archive folder ---
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_filename = now_ct.strftime("%Y-%m-%d") + ".html"
    archive_path = os.path.join(ARCHIVE_DIR, archive_filename)

    # The archived copy's "View Archive" link needs to point to itself correctly
    # since it lives one folder deeper than index.html.
    archived_html = html.replace('href="archive/index.html"', 'href="index.html"')
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(archived_html)

    # --- rebuild the archive listing page ---
    existing = sorted(
        [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".html") and f != "index.html"],
        reverse=True,
    )
    days = []
    for fname in existing:
        date_str = fname.replace(".html", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            display = d.strftime("%A, %B %-d, %Y")
        except ValueError:
            display = date_str
        days.append({"filename": fname, "display": display})

    archive_template = env.get_template("archive_template.html")
    archive_html = archive_template.render(days=days)
    with open(os.path.join(ARCHIVE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(archive_html)

    print(f"[ok] index.html + archive/{archive_filename} + archive/index.html generated at {now_ct.isoformat()}")


if __name__ == "__main__":
    force = "--force" in sys.argv
    hour_ct = datetime.now(CENTRAL).hour

    # The GitHub Actions workflow fires at two UTC times to cover both sides of
    # Daylight Saving Time. Only actually regenerate the page during the 7am
    # Central hour (or any time, if --force is passed for manual/testing runs).
    if not force and hour_ct != 7:
        print(f"[skip] current Central hour is {hour_ct}, not 7. Use --force to override.")
        sys.exit(0)

    build()
