# Publishing on BlackVault Finance and Research

1. Copy `content/_TEMPLATE.md` into the right folder, e.g. `content/economy/kenya-food-prices.md`.
   Predictions use `content/_PREDICTION_TEMPLATE.md` and live in `content/predictions/`.
2. Fill in the front matter (title, date, author, summary, confidence) and write in Markdown.
3. Run `python3 build.py` (Python 3.8+, no packages needed).
4. Commit and push. Generated HTML, sitemap, RSS feed and search index are committed in the repo root.

The homepage counters (publications, predictions recorded, graded, open) update automatically from your content.
Set `draft: true` to keep a piece unpublished. Files starting with `_` are ignored.
To change the research agenda questions, edit the AGENDA block at the top of build.py.

Rules: name sources and access dates, date every conclusion, state confidence, grade every prediction, correct errors openly.
