"""Google Trends: is each keyword rising or falling, and which related searches are breaking out?

    pip install apify-client
    export APIFY_TOKEN=...
    python trends_quickstart.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-trends-monitor").call(run_input={
    "keywords": ["ChatGPT", "Claude", "Gemini"],   # any number; compared on one 0-100 scale
    "timeRange": "past_90_days",
    "geo": "",                                     # worldwide; or "US", "GB", "US-CA", ...
    "includeTimeline": False,                      # headline numbers only
})

for r in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{r['keyword']:10} {r['trend']:8} {r['changePct']:+6.1f}%  avg {r['averageInterest']:5}  "
          f"peak {r['peakDate']}  breakout: {', '.join(r.get('breakoutQueries', [])[:3])}")
