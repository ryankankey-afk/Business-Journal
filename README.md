# Centerline — Daily Business Journal

A one-page morning business journal that rebuilds itself automatically every day at **7:00 AM Central**, covering U.S. markets, a stock watchlist, Missouri & Kansas City business news, and international headlines.

No paid API keys required — market data comes from Yahoo Finance (via `yfinance`) and news comes from public RSS feeds.

---

## What's in this folder

| File | Purpose |
|---|---|
| `template.html` | The page design (Jinja2 template) |
| `generate_journal.py` | Pulls live data and renders `template.html` → `index.html` |
| `render_sample.py` | Renders the page with sample data (for previewing the design only) |
| `requirements.txt` | Python dependencies |
| `.github/workflows/update-journal.yml` | The schedule that runs `generate_journal.py` every morning |
| `index.html` | The current generated page (this is what gets published) |

---

## Setup — about 10 minutes, one time only

### 1. Create a GitHub account
If you don't already have one: go to [github.com/join](https://github.com/join) and sign up (free).

### 2. Create a new repository
- Click the **+** in the top right → **New repository**
- Name it something like `kc-market-journal`
- Set it to **Public** (required for free GitHub Pages)
- Leave "Add a README" unchecked (we already have one)
- Click **Create repository**

### 3. Upload these files
On your new repo's page:
- Click **Add file → Upload files**
- Drag in every file from this folder, **keeping the folder structure** — the `.github/workflows/update-journal.yml` file needs to stay inside a `.github/workflows/` folder. (If the drag-and-drop flattens folders, instead use the steps in "Uploading via Git" below.)
- Scroll down, click **Commit changes**

**Uploading via Git (alternative, preserves folders reliably):**
```bash
cd path/to/this/folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/kc-market-journal.git
git push -u origin main
```

### 4. Turn on GitHub Pages
- In your repo, go to **Settings → Pages**
- Under "Build and deployment" → Source: select **Deploy from a branch**
- Branch: **main**, folder: **/ (root)** → **Save**
- After a minute, GitHub will show your live URL, something like:
  `https://YOUR-USERNAME.github.io/kc-market-journal/`

### 5. Turn on and test the automation
- Go to the **Actions** tab of your repo
- You may see a banner asking to enable workflows — click **I understand, enable them**
- Click **Update Centerline Journal** in the left sidebar → **Run workflow** (top right) → **Run workflow**
- Wait ~30 seconds, refresh — you should see a green checkmark
- Visit your GitHub Pages URL — you'll see the journal with live data

That's it. From now on, it will automatically regenerate every morning at 7:00 AM Central and publish itself, with zero further action from you.

---

## Bookmark it / put it on your phone

Once it's live at your GitHub Pages URL, you can:
- Bookmark it in your browser
- On iPhone: open it in Safari → Share → **Add to Home Screen** (it'll behave like an app icon)
- On Android: open it in Chrome → ⋮ menu → **Add to Home screen**

---

## Customizing

- **Change the watchlist stocks**: edit the `WATCHLIST` list near the top of `generate_journal.py`
- **Change news sources**: edit `NATIONAL_FEEDS`, `INTERNATIONAL_FEEDS`, or `KC_FEEDS` — any standard RSS feed URL works
- **Change colors/fonts/layout**: edit `template.html` (all styling is in the `<style>` block at the top)
- **Change the update time**: edit the cron lines in `.github/workflows/update-journal.yml`. Note GitHub Actions schedules are in UTC — the workflow already fires twice (to handle both sides of Daylight Saving Time) and `generate_journal.py` itself checks the Central-time hour and only actually rebuilds during the 7am hour.

## If a data source ever changes or breaks

RSS feeds occasionally get renamed or retired. If a section goes empty, the script won't crash — it just skips that source. If you notice a section consistently empty, swap in a replacement feed URL in `generate_journal.py`.
