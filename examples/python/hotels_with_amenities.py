"""Hotels that have the amenities you need, cheapest first.

Example: Bali hotels with free breakfast, a pool and a spa for a stay two weeks out.

    pip install apify-client
    export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
    python hotels_with_amenities.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("xpandalabs/google-hotels-rate-monitor").call(run_input={
    "searches": ["hotels in Bali"],
    "daysAhead": 14,
    "nights": 3,
    "requiredAmenities": ["free_breakfast", "pool", "spa"],  # only hotels that have all three
    "minRating": 4.3,
    "onlyWithPrice": True,
    "sortBy": "price_low",
    "maxHotels": 30,
})

for h in client.dataset(run["defaultDatasetId"]).iterate_items():
    extras = [a for a in h["amenities"] if a in ("Beach access", "Airport shuttle", "Kid-friendly", "All inclusive available")]
    print(f"{h['name'][:42]:42}  {h.get('rating') or '-':>4}  "
          f"{h['nightlyPrice']:>7} {h['currency']}/night  {h['totalPrice']:>7} total  {', '.join(extras)}")

# Other filter keys: free_wifi, free_parking, indoor_pool, outdoor_pool, hot_tub, fitness_center, pet_friendly,
# airport_shuttle, beach_access, all_inclusive, restaurant, bar, kid_friendly, kitchen, air_conditioning,
# accessible, room_service, golf
