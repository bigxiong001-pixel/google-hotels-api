# Google Hotels API (no API key): hotel prices, OTA rates, rate parity and competitor rate shopping

Google does not offer a public API for Google Hotels results. The Hotel Center and Hotel Prices APIs are for hotel partners **sending** their own rates to Google, not for reading the comparison results out.

This repo shows how to get Google Hotels data as JSON anyway, through the **[Google Hotels Scraper & Rate Monitor](https://apify.com/xpandalabs/google-hotels-rate-monitor)** on Apify. You call it like an API, from Python, JavaScript, cURL, n8n, Make or Zapier: **no Google API key, no partner account**.

## What you get

- **Hotel prices for any destination**: up to 600 hotels per search (`hotels in Paris`, `4-star hotels in Shanghai`) with nightly and total price for your dates, guests and currency, star class, rating, reviews, coordinates and Google's deal labels.
- **Every booking site's rate** for a hotel: the official site, Booking.com, Expedia, Agoda, Trip.com, Hotels.com and the rest Google lists (often 20–30), before and with tax.
- **Rate parity**: the cheapest OTA vs the hotel's own website, with a `parityIssue` flag.
- **Competitor rate shopping**: your hotel vs your competitors across up to 60 check-in dates, with price rank, gap to the competitor average and a rate grid.
- **Price changes between runs**: `up` / `down` / `new` / `unavailable`, with previous price and % change, or only the changed hotels.

## Quick start

1. Create a free [Apify account](https://console.apify.com/sign-up) and copy your API token from **Settings → Integrations**. The free plan includes $5 of monthly credit (about 1,600 hotels).
2. Pick an example:

| Example | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Cheapest hotels in a city |
| [`examples/python/competitor_rate_shop.py`](examples/python/competitor_rate_shop.py) | Your hotel vs competitors for 14 nights: price grid, rank, gap to average |
| [`examples/python/rate_parity_check.py`](examples/python/rate_parity_check.py) | Flags OTAs selling cheaper than the hotel's own website |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Node.js version of the quick start |
| [`examples/curl/run-sync.sh`](examples/curl/run-sync.sh) | One HTTP request in, JSON rows out |
| [`examples/n8n/`](examples/n8n/README.md) | No-code: n8n, Make or Zapier, with daily alerts |

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("xpandalabs/google-hotels-rate-monitor").call(run_input={
    "searches": ["hotels in Paris"],
    "checkIn": "2026-12-20",
    "checkOut": "2026-12-22",
    "currency": "EUR",
    "maxHotels": 18,
})
for hotel in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(hotel["name"], hotel["nightlyPrice"], hotel["currency"])
```

## Output

One JSON row per hotel (and per check-in date when you check several dates). Real rows from the Actor:

- [`sample-output/destination-search-row.json`](sample-output/destination-search-row.json): a hotel from a destination search
- [`sample-output/hotel-with-booking-sites.json`](sample-output/hotel-with-booking-sites.json): a named hotel with every booking site's rate, the parity check and competitor comparison

| Field | Meaning |
|---|---|
| `name`, `stars`, `rating`, `reviewCount`, `latitude`, `longitude` | Hotel details |
| `nightlyPrice`, `totalPrice`, `currency`, `checkIn`, `checkOut` | Price for your stay |
| `offers[]` | Each booking site: `site`, `isOfficialSite`, `nightlyBeforeTax`, `nightlyWithTax`, `bookingLink` |
| `cheapestSite`, `cheapestNightly`, `officialSiteNightly` | Cheapest site and the hotel's own rate |
| `lowestOtaVsOfficialPct`, `parityIssue` | Rate parity |
| `rankByPrice`, `vsCompSetAvgPct`, `vsMyHotelPct` | Competitor rate shopping |
| `changeType`, `previousNightlyPrice`, `priceChangePct` | Change since the previous run |
| `hotelId`, `googleHotelsUrl` | Stable ID and link |

## Main inputs

| Input | Example |
|---|---|
| `searches` | `["hotels in Sydney"]` |
| `hotels` | `["Park Hyatt Sydney"]` or Google Hotels links |
| `myHotel` | `"Crown Towers Melbourne"` (turns on rate shopping) |
| `checkIn` / `checkOut` | `"2026-12-20"` / `"2026-12-21"` |
| `daysAhead` / `nights` | `7` / `1` (rolling dates for schedules) |
| `datesToCheck` / `dateStepDays` | `30` / `1` (many check-in dates in one run) |
| `adults` / `childrenAges` | `2` / `["4", "9"]` |
| `currency` or `region` | `"EUR"` or `"AU"`, `"US"`, `"GB"`, `"JP"`, `"HK"`, ... |
| `minStars`, `minRating`, `minPrice`, `maxPrice`, `sortBy` | Filters and sorting |
| `onlyChanges` | `true`: only hotels whose price moved since the last run |

Full input reference: [Actor input schema](https://apify.com/xpandalabs/google-hotels-rate-monitor/input-schema).

## Pricing

Pay per result, no start fee: **$3 per 1,000 hotels**, plus **$0.006 per hotel** when you get every booking site's rate. Paid Apify plans get up to 30% off. Set a maximum cost per run and the Actor stops at that limit. Details on the [pricing page](https://apify.com/xpandalabs/google-hotels-rate-monitor/pricing).

## AI agents and MCP

AI assistants (Claude, ChatGPT, Cursor and others) can call the Actor as a tool through the [Apify MCP server](https://mcp.apify.com), for example to answer "cheapest 4-star hotel in Shanghai on 20 December" with live prices.

## Ready-made examples on Apify

- [Hotel prices in New York for next week](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/nyc-hotel-prices)
- [Compare your hotel's rates with competitors](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hotel-competitor-rate-shop)
- [Rate parity check: OTAs vs the hotel's own site](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hotel-rate-parity-check)
- [Cheapest 4-star hotels in London](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/cheapest-4-star-london)
- [Tokyo hotel price drop alerts](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/tokyo-hotel-price-alerts)
- [Hong Kong hotel prices in HKD](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hong-kong-hotel-prices-hkd)

## Questions

Open an issue on the [Actor's Issues tab](https://apify.com/xpandalabs/google-hotels-rate-monitor/issues) or in this repo.

The data is the public Google Hotels results any visitor sees. You are responsible for using it in line with applicable laws and Google's terms. The code in this repo is MIT-licensed.
