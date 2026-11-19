"""Google Hotels prices for a city, in a few lines of Python.

    pip install apify-client
    export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
    python quickstart.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-hotels-rate-monitor").call(run_input={
    "searches": ["hotels in Paris"],
    "checkIn": "2026-12-20",
    "checkOut": "2026-12-22",
    "currency": "EUR",
    "maxHotels": 18,          # one results page: answers in a few seconds
    "sortBy": "price_low",
})

for hotel in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{hotel['name'][:45]:45}  {hotel.get('stars') or '-'}★  "
          f"{hotel.get('rating') or '-':>4}  {hotel.get('nightlyPrice')} {hotel['currency']}/night")
