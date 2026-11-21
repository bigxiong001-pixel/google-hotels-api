"""New-search-term radar: run daily (cron, GitHub Actions, or an Apify schedule) and print only
related searches that started rising since the previous run.

    pip install apify-client
    export APIFY_TOKEN=...
    python trends_rising_alert.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-trends-monitor").call(run_input={
    "keywords": ["AI agent", "vibe coding", "AI video generator"],
    "compareMode": "separate",
    "timeRange": "past_7_days",
    "onlyChanges": True,          # first run = baseline; later runs return (and charge) only changes
    "trendingNow": ["US"],        # also: what is trending in the US right now, new ones only
    "maxTrendingPerCountry": 20,
})

for r in client.dataset(run["defaultDatasetId"]).iterate_items():
    if r["type"] == "keyword":
        new = r.get("newRisingQueries") or [q["query"] for q in r.get("risingQueries", [])]
        print(f"[{r['keyword']}] {r['changeType']}: {', '.join(new[:8])}")
    else:
        print(f"[trending {r['geo']}] {r['title']} ({r.get('approxTraffic')})")
