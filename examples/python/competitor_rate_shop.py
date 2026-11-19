"""Hotel competitor rate shopping: your hotel vs your competitors for the next 14 nights.

Prints a price grid (hotel x check-in date), your price rank and your gap to the competitor average.

    pip install apify-client
    export APIFY_TOKEN=...
    python competitor_rate_shop.py
"""
import os
from collections import defaultdict

from apify_client import ApifyClient

MY_HOTEL = "Crown Towers Melbourne"
COMPETITORS = ["Park Hyatt Melbourne", "The Langham Melbourne", "Grand Hyatt Melbourne"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("xpandalabs/google-hotels-rate-monitor").call(run_input={
    "myHotel": MY_HOTEL,
    "hotels": COMPETITORS,
    "daysAhead": 1,          # start tomorrow; leave dates empty so a daily schedule rolls forward
    "datesToCheck": 14,      # 14 consecutive check-in dates
    "region": "AU",          # AUD prices, Australian market
})

rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
grid, mine = defaultdict(dict), {}
for r in rows:
    grid[r["name"]][r["checkIn"]] = r.get("nightlyPrice")
    if r.get("isMyHotel"):
        mine[r["checkIn"]] = r

dates = sorted({r["checkIn"] for r in rows})
my_name = next((r["name"] for r in rows if r.get("isMyHotel")), None)
print("Hotel".ljust(32) + "".join(d[5:].rjust(8) for d in dates))
for name, prices in sorted(grid.items(), key=lambda kv: (kv[0] != my_name, kv[0])):  # your hotel first
    print(name[:31].ljust(32) + "".join(f"{prices[d]:8.0f}" if prices.get(d) else "       -" for d in dates))

print("\nYour rank (1 = cheapest) and gap to the competitor average:")
for d in dates:
    m = mine.get(d)
    if m and m.get("rankByPrice"):
        print(f"  {d}: rank {m['rankByPrice']}/{m['hotelsCompared']}, {m['vsCompSetAvgPct']:+.1f}% vs average")

# The run's Output tab also has a ready-made, colour-coded rate grid (key-value store record REPORT).
