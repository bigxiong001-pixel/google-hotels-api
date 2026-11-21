"""Cheapest day to fly: the lowest Google Flights fare for each of the next 30 departure dates,
with Google's low / typical / high price level.

    pip install apify-client
    export APIFY_TOKEN=...
    python flights_fare_calendar.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "routes": ["LON-NYC"],
    "outputMode": "cheapest",       # one row per route and date
    "daysAhead": 7,
    "datesToCheck": 30,
    "region": "GB",                 # GBP prices
})

rows = sorted(client.dataset(run["defaultDatasetId"]).iterate_items(), key=lambda r: r["departDate"])
best = min((r for r in rows if r.get("cheapestPrice")), key=lambda r: r["cheapestPrice"])
for r in rows:
    mark = "  <- cheapest" if r is best else ""
    print(f"{r['departDate']}  {r.get('cheapestPrice') or '-':>6} {r['currency']}  "
          f"{(r.get('priceLevel') or ''):8} {r.get('cheapestAirline') or ''}{mark}")
# The run's Output tab also has a colour-coded fare calendar (key-value store record REPORT).
