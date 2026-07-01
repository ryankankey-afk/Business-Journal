<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Centerline — Tuesday, June 30, 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root{
    --bg:#0B0E14;
    --surface:#12151F;
    --surface-2:#171B27;
    --border:#232838;
    --text:#EDEFF3;
    --text-dim:#8A93A6;
    --text-faint:#565E70;
    --accent:#4F7CFF;
    --accent-soft:rgba(79,124,255,0.12);
    --pos:#1FCB86;
    --pos-soft:rgba(31,203,134,0.12);
    --neg:#FF5C5C;
    --neg-soft:rgba(255,92,92,0.12);
    --kc:#D9A24B;
    --kc-soft:rgba(217,162,75,0.12);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{
    background:var(--bg);
    color:var(--text);
    font-family:'Inter',sans-serif;
    -webkit-font-smoothing:antialiased;
    line-height:1.5;
  }
  .mono{font-family:'JetBrains Mono',monospace;}
  .display{font-family:'Space Grotesk',sans-serif;}

  /* Ticker tape — signature element */
  .ticker-wrap{
    background:#000;
    border-bottom:1px solid var(--border);
    overflow:hidden;
    white-space:nowrap;
    padding:9px 0;
  }
  .ticker{
    display:inline-block;
    animation:scroll 38s linear infinite;
  }
  .ticker-wrap:hover .ticker{ animation-play-state:paused; }
  @keyframes scroll{
    0%{ transform:translateX(0); }
    100%{ transform:translateX(-50%); }
  }
  .ticker-item{
    display:inline-flex; align-items:center; gap:8px;
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px;
    padding:0 22px;
    color:var(--text-dim);
    border-right:1px solid var(--border);
  }
  .ticker-item b{ color:var(--text); font-weight:600; }
  .up{ color:var(--pos); }
  .down{ color:var(--neg); }

  .wrap{ max-width:1040px; margin:0 auto; padding:0 24px; }

  /* Masthead */
  header.masthead{
    padding:38px 0 26px;
    border-bottom:1px solid var(--border);
  }
  .masthead-row{
    display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:16px;
  }
  .brand{
    font-family:'Space Grotesk',sans-serif;
    font-weight:700;
    font-size:34px;
    letter-spacing:-0.5px;
  }
  .brand span{ color:var(--accent); }
  .tagline{
    color:var(--text-dim);
    font-size:14px;
    margin-top:4px;
  }
  .meta{
    text-align:right;
    font-family:'JetBrains Mono',monospace;
    font-size:12px;
    color:var(--text-faint);
    line-height:1.7;
  }
  .meta .liveDot{
    display:inline-block; width:6px; height:6px; border-radius:50%;
    background:var(--pos); margin-right:6px;
    box-shadow:0 0 0 3px var(--pos-soft);
  }

  /* Hero snapshot */
  section.hero{ padding:32px 0 8px; }
  .section-label{
    font-family:'JetBrains Mono',monospace;
    font-size:11px;
    letter-spacing:1.5px;
    color:var(--text-faint);
    text-transform:uppercase;
    margin-bottom:14px;
    display:flex; align-items:center; gap:10px;
  }
  .section-label::after{
    content:''; flex:1; height:1px; background:var(--border);
  }

  .index-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:1px;
    background:var(--border);
    border:1px solid var(--border);
    border-radius:10px;
    overflow:hidden;
  }
  .index-card{
    background:var(--surface);
    padding:18px 18px 16px;
  }
  .index-name{ font-size:12.5px; color:var(--text-dim); margin-bottom:8px; }
  .index-price{
    font-family:'JetBrains Mono',monospace;
    font-size:21px; font-weight:600;
  }
  .index-change{
    font-family:'JetBrains Mono',monospace;
    font-size:12.5px; margin-top:4px;
  }

  /* Chart panel */
  .chart-panel{
    margin-top:20px;
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:10px;
    padding:20px;
  }
  .chart-panel-head{
    display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;
  }
  .chart-title{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:15px; }
  .chart-sub{ font-size:12px; color:var(--text-faint); font-family:'JetBrains Mono',monospace; }
  .chart-box{ height:220px; }

  /* Watchlist */
  .watchlist{
    margin-top:20px;
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:10px;
    overflow:hidden;
  }
  .watchlist-head{
    padding:14px 18px; border-bottom:1px solid var(--border);
    font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:14px;
  }
  table.wl{ width:100%; border-collapse:collapse; }
  table.wl td{ padding:11px 18px; font-size:13px; border-top:1px solid var(--border); }
  table.wl tr:first-child td{ border-top:none; }
  .wl-ticker{ font-family:'JetBrains Mono',monospace; font-weight:600; }
  .wl-name{ color:var(--text-dim); }
  .wl-price{ font-family:'JetBrains Mono',monospace; text-align:right; }
  .wl-change{ font-family:'JetBrains Mono',monospace; text-align:right; width:90px; }

  /* News sections */
  .news-grid{
    margin-top:36px;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
  }
  .news-card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:10px;
    padding:20px;
  }
  .news-card.kc{ grid-column:1 / -1; border-color:#2A2415; }
  .news-card-head{
    display:flex; align-items:center; gap:8px; margin-bottom:14px;
  }
  .badge{
    font-family:'JetBrains Mono',monospace;
    font-size:10.5px; letter-spacing:0.5px;
    padding:3px 8px; border-radius:5px;
    background:var(--accent-soft); color:var(--accent);
  }
  .badge.kc{ background:var(--kc-soft); color:var(--kc); }
  .news-card-title{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:15px; }
  .news-item{
    padding:11px 0; border-top:1px solid var(--border);
  }
  .news-item:first-child{ border-top:none; padding-top:0; }
  .news-item a{
    color:var(--text); text-decoration:none; font-size:13.5px; font-weight:500;
    display:block; margin-bottom:3px;
  }
  .news-item a:hover{ color:var(--accent); }
  .news-source{ font-size:11px; color:var(--text-faint); font-family:'JetBrains Mono',monospace; }

  .kc-flex{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }

  footer{
    margin-top:44px; padding:22px 0 40px;
    border-top:1px solid var(--border);
    font-size:11.5px; color:var(--text-faint);
    display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
    font-family:'JetBrains Mono',monospace;
  }

  @media (max-width:720px){
    .index-grid{ grid-template-columns:repeat(2,1fr); }
    .news-grid{ grid-template-columns:1fr; }
    .kc-flex{ grid-template-columns:1fr; }
    .masthead-row{ flex-direction:column; align-items:flex-start; }
    .meta{ text-align:left; }
  }

  @media (prefers-reduced-motion:reduce){
    .ticker{ animation:none; }
  }
</style>
</head>
<body>

  <div class="ticker-wrap">
    <div class="ticker">
      
      <span class="ticker-item"><b>S&P 500</b> 6,142.18 <span class="up">▲ +0.42%</span></span>
      
      <span class="ticker-item"><b>DOW</b> 43,207.55 <span class="up">▲ +0.28%</span></span>
      
      <span class="ticker-item"><b>NASDAQ</b> 20,118.90 <span class="down">▼ -0.15%</span></span>
      
      <span class="ticker-item"><b>10-YR YIELD</b> 4.31% <span class="down">▼ -0.03%</span></span>
      
      <span class="ticker-item"><b>VIX</b> 13.82 <span class="down">▼ -1.10%</span></span>
      
      <span class="ticker-item"><b>CRUDE OIL</b> 68.44 <span class="up">▲ +0.91%</span></span>
      
      <span class="ticker-item"><b>GOLD</b> 2,614.30 <span class="up">▲ +0.33%</span></span>
      
      
      <span class="ticker-item"><b>S&P 500</b> 6,142.18 <span class="up">▲ +0.42%</span></span>
      
      <span class="ticker-item"><b>DOW</b> 43,207.55 <span class="up">▲ +0.28%</span></span>
      
      <span class="ticker-item"><b>NASDAQ</b> 20,118.90 <span class="down">▼ -0.15%</span></span>
      
      <span class="ticker-item"><b>10-YR YIELD</b> 4.31% <span class="down">▼ -0.03%</span></span>
      
      <span class="ticker-item"><b>VIX</b> 13.82 <span class="down">▼ -1.10%</span></span>
      
      <span class="ticker-item"><b>CRUDE OIL</b> 68.44 <span class="up">▲ +0.91%</span></span>
      
      <span class="ticker-item"><b>GOLD</b> 2,614.30 <span class="up">▲ +0.33%</span></span>
      
    </div>
  </div>

  <div class="wrap">
    <header class="masthead">
      <div class="masthead-row">
        <div>
          <div class="brand">CENTER<span>LINE</span></div>
          <div class="tagline">Markets · Missouri &amp; Kansas City · The World — before your coffee's done.</div>
        </div>
        <div class="meta">
          <div><span class="liveDot"></span>Tuesday, June 30, 2026</div>
          <div>Updated 7:00 AM CT</div>
        </div>
      </div>
    </header>

    <section class="hero">
      <div class="section-label">U.S. Markets</div>
      <div class="index-grid">
        
        <div class="index-card">
          <div class="index-name">S&P 500</div>
          <div class="index-price">6,142.18</div>
          <div class="index-change up">▲ +0.42%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">Dow Jones</div>
          <div class="index-price">43,207.55</div>
          <div class="index-change up">▲ +0.28%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">Nasdaq</div>
          <div class="index-price">20,118.90</div>
          <div class="index-change down">▼ -0.15%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">10-Yr Yield</div>
          <div class="index-price">4.31%</div>
          <div class="index-change down">▼ -0.03%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">VIX</div>
          <div class="index-price">13.82</div>
          <div class="index-change down">▼ -1.10%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">US Dollar Idx</div>
          <div class="index-price">104.12</div>
          <div class="index-change up">▲ +0.08%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">Crude Oil</div>
          <div class="index-price">68.44</div>
          <div class="index-change up">▲ +0.91%</div>
        </div>
        
        <div class="index-card">
          <div class="index-name">Gold</div>
          <div class="index-price">2,614.30</div>
          <div class="index-change up">▲ +0.33%</div>
        </div>
        
      </div>

      <div class="chart-panel">
        <div class="chart-panel-head">
          <div class="chart-title">S&amp;P 500 — 5 Day</div>
          <div class="chart-sub">Mon 9:30am → Fri 3:30pm</div>
        </div>
        <div class="chart-box"><canvas id="spxChart"></canvas></div>
      </div>

      <div class="watchlist">
        <div class="watchlist-head">Stocks to Watch</div>
        <table class="wl">
          
          <tr>
            <td class="wl-ticker">AAPL</td>
            <td class="wl-name">Apple</td>
            <td class="wl-price">231.07</td>
            <td class="wl-change up">▲ +0.61%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">MSFT</td>
            <td class="wl-name">Microsoft</td>
            <td class="wl-price">468.22</td>
            <td class="wl-change up">▲ +0.34%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">NVDA</td>
            <td class="wl-name">NVIDIA</td>
            <td class="wl-price">142.85</td>
            <td class="wl-change down">▼ -0.87%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">AMZN</td>
            <td class="wl-name">Amazon</td>
            <td class="wl-price">224.60</td>
            <td class="wl-change up">▲ +1.02%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">GOOGL</td>
            <td class="wl-name">Alphabet</td>
            <td class="wl-price">192.34</td>
            <td class="wl-change up">▲ +0.19%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">TSLA</td>
            <td class="wl-name">Tesla</td>
            <td class="wl-price">318.77</td>
            <td class="wl-change down">▼ -2.14%</td>
          </tr>
          
          <tr>
            <td class="wl-ticker">JPM</td>
            <td class="wl-name">JPMorgan Chase</td>
            <td class="wl-price">266.91</td>
            <td class="wl-change up">▲ +0.45%</td>
          </tr>
          
        </table>
      </div>
    </section>

    <section class="news-grid">
      <div class="news-card">
        <div class="news-card-head">
          <span class="badge">NATIONAL</span>
          <span class="news-card-title">Business &amp; Economy</span>
        </div>
        
        <div class="news-item">
          <a href="https://www.cnbc.com/" target="_blank" rel="noopener">Fed officials signal a cautious, data-dependent path on rate cuts</a>
          <div class="news-source">CNBC</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.marketwatch.com/" target="_blank" rel="noopener">Retail spending held steady last month, easing recession worries</a>
          <div class="news-source">MarketWatch</div>
        </div>
        
        <div class="news-item">
          <a href="https://apnews.com/hub/business" target="_blank" rel="noopener">Regional banks post stronger-than-expected quarterly earnings</a>
          <div class="news-source">AP Business</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.cnbc.com/" target="_blank" rel="noopener">Homebuilders see permit activity tick up as mortgage rates ease</a>
          <div class="news-source">CNBC</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.marketwatch.com/" target="_blank" rel="noopener">Airlines trim summer capacity as fuel costs climb</a>
          <div class="news-source">MarketWatch</div>
        </div>
        
      </div>

      <div class="news-card">
        <div class="news-card-head">
          <span class="badge">WORLD</span>
          <span class="news-card-title">International</span>
        </div>
        
        <div class="news-item">
          <a href="https://www.bbc.com/news/world" target="_blank" rel="noopener">European Central Bank holds rates, cites steady inflation outlook</a>
          <div class="news-source">BBC World</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.reutersagency.com/" target="_blank" rel="noopener">Asian manufacturing data points to a modest rebound in exports</a>
          <div class="news-source">Reuters World</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.bbc.com/news/world" target="_blank" rel="noopener">UK Parliament debates new trade framework ahead of summer recess</a>
          <div class="news-source">BBC World</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.reutersagency.com/" target="_blank" rel="noopener">Global shipping rates ease as Red Sea traffic slowly normalizes</a>
          <div class="news-source">Reuters World</div>
        </div>
        
        <div class="news-item">
          <a href="https://www.bbc.com/news/world" target="_blank" rel="noopener">China property sector shows early signs of stabilizing</a>
          <div class="news-source">BBC World</div>
        </div>
        
      </div>

      <div class="news-card kc">
        <div class="news-card-head">
          <span class="badge kc">HOME TURF</span>
          <span class="news-card-title">Missouri &amp; Kansas City</span>
        </div>
        <div class="kc-flex">
          <div>
            
            <div class="news-item">
              <a href="https://www.bizjournals.com/kansascity/" target="_blank" rel="noopener">Downtown KC office conversions get new city tax incentive</a>
              <div class="news-source">KC Business Journal</div>
            </div>
            
            <div class="news-item">
              <a href="https://www.bizjournals.com/kansascity/" target="_blank" rel="noopener">Cerner campus redevelopment adds another anchor tenant</a>
              <div class="news-source">KC Business Journal</div>
            </div>
            
            <div class="news-item">
              <a href="https://missouriindependent.com/" target="_blank" rel="noopener">Missouri unemployment holds near historic lows in latest report</a>
              <div class="news-source">Missouri Independent</div>
            </div>
            
          </div>
          <div>
            
            <div class="news-item">
              <a href="https://www.kshb.com/" target="_blank" rel="noopener">KC streetcar Main Street extension nears completion</a>
              <div class="news-source">KSHB 41</div>
            </div>
            
            <div class="news-item">
              <a href="https://kansasreflector.com/" target="_blank" rel="noopener">Kansas lawmakers weigh new incentives for data center projects</a>
              <div class="news-source">Kansas Reflector</div>
            </div>
            
            <div class="news-item">
              <a href="https://kansasreflector.com/" target="_blank" rel="noopener">Panasonic battery plant in De Soto ramps up hiring</a>
              <div class="news-source">Kansas Reflector</div>
            </div>
            
          </div>
        </div>
      </div>
    </section>

    <footer>
      <div>Market data via Yahoo Finance · News via public RSS feeds · Auto-generated, not investment advice.</div>
      <div>Next update tomorrow 7:00 AM CT</div>
    </footer>
  </div>

<script>
  const ctx = document.getElementById('spxChart').getContext('2d');
  const labels = ["Mon 9:30am", "Mon 3:30pm", "Tue 9:30am", "Tue 3:30pm", "Wed 9:30am", "Wed 3:30pm", "Thu 9:30am", "Thu 3:30pm", "Fri 9:30am", "Fri 3:30pm"];
  const data = [6098, 6110, 6105, 6122, 6118, 6130, 6127, 6135, 6139, 6142];
  const isUp = data[data.length-1] >= data[0];
  const lineColor = isUp ? '#1FCB86' : '#FF5C5C';
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        borderColor: lineColor,
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
        fill: true,
        backgroundColor: (ctx) => {
          const g = ctx.chart.ctx.createLinearGradient(0,0,0,220);
          g.addColorStop(0, lineColor + '33');
          g.addColorStop(1, lineColor + '00');
          return g;
        }
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display:false }, tooltip: { mode:'index', intersect:false } },
      scales: {
        x: { grid:{ display:false }, ticks:{ color:'#565E70', font:{ family:'JetBrains Mono', size:10 } } },
        y: { grid:{ color:'#1B2030' }, ticks:{ color:'#565E70', font:{ family:'JetBrains Mono', size:10 } } }
      }
    }
  });
</script>
</body>
</html>