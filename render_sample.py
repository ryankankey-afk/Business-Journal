"""Renders template.html with sample/placeholder data — for design preview only.
The real generate_journal.py pulls live data; this just shows the look & feel."""

import json
from datetime import datetime
from zoneinfo import ZoneInfo
from jinja2 import Environment, FileSystemLoader

now_ct = datetime.now(ZoneInfo("America/Chicago"))

ticker_items = [
    {"symbol": "S&P 500", "price": "6,142.18", "change": "▲ +0.42%", "dir": "up"},
    {"symbol": "DOW", "price": "43,207.55", "change": "▲ +0.28%", "dir": "up"},
    {"symbol": "NASDAQ", "price": "20,118.90", "change": "▼ -0.15%", "dir": "down"},
    {"symbol": "10-YR YIELD", "price": "4.31%", "change": "▼ -0.03%", "dir": "down"},
    {"symbol": "VIX", "price": "13.82", "change": "▼ -1.10%", "dir": "down"},
    {"symbol": "CRUDE OIL", "price": "68.44", "change": "▲ +0.91%", "dir": "up"},
    {"symbol": "GOLD", "price": "2,614.30", "change": "▲ +0.33%", "dir": "up"},
]

indices = [
    {"name": "S&P 500", "price": "6,142.18", "change": "▲ +0.42%", "dir": "up"},
    {"name": "Dow Jones", "price": "43,207.55", "change": "▲ +0.28%", "dir": "up"},
    {"name": "Nasdaq", "price": "20,118.90", "change": "▼ -0.15%", "dir": "down"},
    {"name": "10-Yr Yield", "price": "4.31%", "change": "▼ -0.03%", "dir": "down"},
    {"name": "VIX", "price": "13.82", "change": "▼ -1.10%", "dir": "down"},
    {"name": "US Dollar Idx", "price": "104.12", "change": "▲ +0.08%", "dir": "up"},
    {"name": "Crude Oil", "price": "68.44", "change": "▲ +0.91%", "dir": "up"},
    {"name": "Gold", "price": "2,614.30", "change": "▲ +0.33%", "dir": "up"},
]

spx_labels = ["Mon 9:30am", "Mon 3:30pm", "Tue 9:30am", "Tue 3:30pm", "Wed 9:30am",
              "Wed 3:30pm", "Thu 9:30am", "Thu 3:30pm", "Fri 9:30am", "Fri 3:30pm"]
spx_values = [6098, 6110, 6105, 6122, 6118, 6130, 6127, 6135, 6139, 6142]

watchlist = [
    {"symbol": "AAPL", "name": "Apple", "price": "231.07", "change": "▲ +0.61%", "dir": "up"},
    {"symbol": "MSFT", "name": "Microsoft", "price": "468.22", "change": "▲ +0.34%", "dir": "up"},
    {"symbol": "NVDA", "name": "NVIDIA", "price": "142.85", "change": "▼ -0.87%", "dir": "down"},
    {"symbol": "AMZN", "name": "Amazon", "price": "224.60", "change": "▲ +1.02%", "dir": "up"},
    {"symbol": "GOOGL", "name": "Alphabet", "price": "192.34", "change": "▲ +0.19%", "dir": "up"},
    {"symbol": "TSLA", "name": "Tesla", "price": "318.77", "change": "▼ -2.14%", "dir": "down"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "price": "266.91", "change": "▲ +0.45%", "dir": "up"},
]

national_news = [
    {"title": "Fed officials signal a cautious, data-dependent path on rate cuts", "link": "https://www.cnbc.com/", "source": "CNBC"},
    {"title": "Retail spending held steady last month, easing recession worries", "link": "https://www.marketwatch.com/", "source": "MarketWatch"},
    {"title": "Regional banks post stronger-than-expected quarterly earnings", "link": "https://apnews.com/hub/business", "source": "AP Business"},
    {"title": "Homebuilders see permit activity tick up as mortgage rates ease", "link": "https://www.cnbc.com/", "source": "CNBC"},
    {"title": "Airlines trim summer capacity as fuel costs climb", "link": "https://www.marketwatch.com/", "source": "MarketWatch"},
]

international_news = [
    {"title": "European Central Bank holds rates, cites steady inflation outlook", "link": "https://www.bbc.com/news/world", "source": "BBC World"},
    {"title": "Asian manufacturing data points to a modest rebound in exports", "link": "https://www.reutersagency.com/", "source": "Reuters World"},
    {"title": "UK Parliament debates new trade framework ahead of summer recess", "link": "https://www.bbc.com/news/world", "source": "BBC World"},
    {"title": "Global shipping rates ease as Red Sea traffic slowly normalizes", "link": "https://www.reutersagency.com/", "source": "Reuters World"},
    {"title": "China property sector shows early signs of stabilizing", "link": "https://www.bbc.com/news/world", "source": "BBC World"},
]

kc_news = [
    {"title": "Downtown KC office conversions get new city tax incentive", "link": "https://www.bizjournals.com/kansascity/", "source": "KC Business Journal"},
    {"title": "Cerner campus redevelopment adds another anchor tenant", "link": "https://www.bizjournals.com/kansascity/", "source": "KC Business Journal"},
    {"title": "Missouri unemployment holds near historic lows in latest report", "link": "https://missouriindependent.com/", "source": "Missouri Independent"},
    {"title": "KC streetcar Main Street extension nears completion", "link": "https://www.kshb.com/", "source": "KSHB 41"},
    {"title": "Kansas lawmakers weigh new incentives for data center projects", "link": "https://kansasreflector.com/", "source": "Kansas Reflector"},
    {"title": "Panasonic battery plant in De Soto ramps up hiring", "link": "https://kansasreflector.com/", "source": "Kansas Reflector"},
]

env = Environment(loader=FileSystemLoader("."), autoescape=False)
template = env.get_template("template.html")

html = template.render(
    generated_date=now_ct.strftime("%A, %B %-d, %Y"),
    generated_time_ct="7:00 AM",
    ticker_items=ticker_items,
    indices=indices,
    spx_labels=json.dumps(spx_labels),
    spx_values=json.dumps(spx_values),
    spx_range_label="Mon 9:30am → Fri 3:30pm",
    watchlist=watchlist,
    national_news=national_news,
    international_news=international_news,
    kc_news=kc_news,
    kc_half=(len(kc_news) + 1) // 2,
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Sample index.html rendered.")
