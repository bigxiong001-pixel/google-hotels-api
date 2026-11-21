"""Google Flights: every flight on a route and date, cheapest first.

    pip install apify-client
    export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
    python flights_quickstart.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "routes": ["JFK-LAX"],          # airport codes, city codes (NYC-LON) or names ("New York to London")
    "daysAhead": 14,                # or "departDate": "2026-12-20"
    "maxStops": "nonstop",
    "sortBy": "price",
    "maxFlightsPerSearch": 10,
})

for f in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{f['departDate']}  {f['departureTime']}-{f['arrivalTime']}  {'/'.join(f['flightNumbers']):18}"
          f"{f['airline'][:22]:22}  {f['durationMinutes']:>4} min  {f['price']} {f['currency']}")
