# Google Hotels, Google Flights & Google Trends API (no API key)

Google has no public API for reading Google Hotels or Google Flights results, and the Google Trends API is a closed alpha. This repo shows how to get all three as JSON anyway, through three Actors on Apify that you call like an API from Python, JavaScript, cURL, n8n, Make or Zapier: **no Google API key, no partner account**.

| | Actor | Price | What you get |
|---|---|---|---|
| 🏨 | [Google Hotels Scraper & Rate Monitor](https://apify.com/xpandalabs/google-hotels-rate-monitor) | $3 / 1,000 hotels | Hotel prices for any destination, every booking site's rate, rate parity, competitor rate shopping |
| ✈️ | [Google Flights Scraper & Fare Monitor](https://apify.com/xpandalabs/google-flights-fare-monitor) | $1 / 1,000 flights | Every flight on a route and date, or a cheapest-day fare calendar with Google's low/typical/high price level |
| 📈 | [Google Trends Scraper & Monitor](https://apify.com/xpandalabs/google-trends-monitor) | $1.50 / 1,000 keywords, no start fee | Rising/falling verdict, interest over time, regions, rising and breakout searches, trending now |

All three track changes between runs (price drops, new rising searches) and can return only what changed, so a daily schedule costs almost nothing when nothing moves.

## Quick start

1. Create a free [Apify account](https://console.apify.com/sign-up) and copy your API token from **Settings → Integrations**. The free plan includes $5 of monthly credit.
2. `pip install apify-client` and `export APIFY_TOKEN=...`
3. Run an example:

| Example | What it does |
|---|---|
| **Hotels** | |
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Cheapest hotels in a city |
| [`examples/python/competitor_rate_shop.py`](examples/python/competitor_rate_shop.py) | Your hotel vs competitors for 14 nights: price grid, rank, gap to average |
| [`examples/python/rate_parity_check.py`](examples/python/rate_parity_check.py) | Flags OTAs selling cheaper than the hotel's own website |
| **Flights** | |
| [`examples/python/flights_quickstart.py`](examples/python/flights_quickstart.py) | Nonstop flights JFK → LAX, cheapest first |
| [`examples/python/flights_fare_calendar.py`](examples/python/flights_fare_calendar.py) | Cheapest day to fly London → New York in the next 30 days |
| **Trends** | |
| [`examples/python/trends_quickstart.py`](examples/python/trends_quickstart.py) | ChatGPT vs Claude vs Gemini: rising or falling, peak, breakout searches |
| [`examples/python/trends_rising_alert.py`](examples/python/trends_rising_alert.py) | Daily radar for newly rising searches and what is trending now |
| **Other languages and no-code** | |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Node.js (hotels) |
| [`examples/curl/run-sync.sh`](examples/curl/run-sync.sh) | One HTTP request in, JSON rows out |
| [`examples/n8n/`](examples/n8n/README.md) | n8n, Make or Zapier, with daily alerts |

The JavaScript, cURL and n8n examples call the hotels Actor; swap the Actor name and input to use flights or trends.

---

## 🏨 Google Hotels

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
    print(hotel["name"], hotel["nightlyPrice"], hotel["totalPrice"], hotel["currency"])
```

- **Hotel prices for any destination**: up to 600 hotels per search with nightly and whole-stay price, star class, rating, reviews and coordinates.
- **Every booking site's rate** for a hotel (official site, Booking.com, Expedia, Agoda, Trip.com and the rest, often 20–30), before and with tax.
- **Rate parity**: cheapest OTA vs the hotel's own website, with a `parityIssue` flag.
- **Competitor rate shopping**: your hotel vs competitors across up to 60 check-in dates, with price rank and gap to the average.

| Field | Meaning |
|---|---|
| `nightlyPrice`, `nightlyPriceWithTax`, `totalPrice` | Nightly before tax, nightly with taxes and fees, whole stay with taxes and fees |
| `offers[]` | Each booking site: `site`, `isOfficialSite`, `nightlyBeforeTax`, `nightlyWithTax`, `bookingLink` |
| `cheapestSite`, `cheapestNightly`, `officialSiteNightly`, `parityIssue` | Rate parity |
| `rankByPrice`, `vsCompSetAvgPct`, `vsMyHotelPct` | Competitor rate shopping |
| `changeType`, `previousNightlyPrice`, `priceChangePct` | Change since the previous run |

Samples: [`destination-search-row.json`](sample-output/destination-search-row.json), [`hotel-with-booking-sites.json`](sample-output/hotel-with-booking-sites.json). Ready-made examples on Apify: [NYC hotel prices](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/nyc-hotel-prices), [competitor rate shop](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hotel-competitor-rate-shop), [rate parity check](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hotel-rate-parity-check), [cheapest 4-star London](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/cheapest-4-star-london), [Tokyo price alerts](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/tokyo-hotel-price-alerts), [Hong Kong in HKD](https://apify.com/xpandalabs/google-hotels-rate-monitor/examples/hong-kong-hotel-prices-hkd).

---

## ✈️ Google Flights

```python
run = client.actor("xpandalabs/google-flights-fare-monitor").call(run_input={
    "routes": ["JFK-LAX"],          # airport codes, city codes (NYC-LON) or names ("New York to London")
    "departDate": "2026-12-20",
    "maxStops": "nonstop",
    "sortBy": "price",
})
for f in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f["airline"], f["flightNumbers"], f["departureTime"], f["price"], f["currency"])
```

- **Every flight**: airline, flight numbers, times, duration, stops, layovers, aircraft, legroom, CO₂ and the total price for your passengers.
- **Fare calendar** (`"outputMode": "cheapest"`): cheapest fare per route and departure date, Google's `priceLevel` (low / typical / high), typical price range and 60-day price history.
- One-way and round trips, adults and children, economy to first, stop and airline filters, 15 currency presets, target-price alerts.

| Field | Meaning |
|---|---|
| `price`, `pricePerPassenger`, `currency` | Total for all passengers (round trips: the whole trip) |
| `flightPriceLevel`, `typicalPriceLow`, `typicalPriceHigh` | Where the price falls in Google's typical range |
| `cheapestPrice`, `priceLevel`, `priceHistory` | Fare calendar rows |
| `changeType`, `previousPrice`, `priceChangePct`, `belowTargetPrice` | Change since the previous run and target-price alert |

Samples: [`flight-row.json`](sample-output/flight-row.json), [`fare-calendar-row.json`](sample-output/fare-calendar-row.json). Ready-made examples on Apify: [cheapest day New York → London](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/cheapest-day-to-fly-new-york-london), [price drop alert](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/flight-price-drop-alert), [nonstop JFK → LAX](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/nonstop-flights-jfk-lax), [family round trip HKG → BKK](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/family-round-trip-hong-kong-bangkok), [business class SIN → LON](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/business-class-singapore-london), [Shanghai → Tokyo in CNY](https://apify.com/xpandalabs/google-flights-fare-monitor/examples/shanghai-tokyo-flight-prices-cny).

---

## 📈 Google Trends

```python
run = client.actor("xpandalabs/google-trends-monitor").call(run_input={
    "keywords": ["ChatGPT", "Claude", "Gemini"],   # any number, compared on one 0-100 scale
    "timeRange": "past_90_days",
    "geo": "US",
})
for r in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(r["keyword"], r["trend"], r["changePct"], r["breakoutQueries"][:3])
```

- **The answer, not just a series**: `trend` (rising / falling / stable) with `changePct`, current, average and peak interest, peak date, plus the full timeline.
- **Compare any number of keywords** on one 0–100 scale (Google's own limit is 5).
- **Top regions** down to city or US metro level, **top and rising related searches** with breakout flags.
- **Trending now** in any country, with approximate searches and the news behind each trend.
- **Alerts**: `newRisingQueries` lists rising searches that were not there on the previous run.

| Field | Meaning |
|---|---|
| `trend`, `changePct` | Latest sixth of the period vs the sixth before it; ±15% counts as rising or falling |
| `currentInterest`, `averageInterest`, `peakInterest`, `peakDate`, `timeline` | Google's 0–100 interest |
| `topRegions`, `topQueries`, `risingQueries`, `breakoutQueries` | Where and what people search |
| `newRisingQueries`, `changeType` | New rising searches since the previous run |

Samples: [`trends-keyword-row.json`](sample-output/trends-keyword-row.json), [`trending-now-row.json`](sample-output/trending-now-row.json). Ready-made examples on Apify: [ChatGPT vs Claude vs Gemini](https://apify.com/xpandalabs/google-trends-monitor/examples/ai-chatbots-google-trends), [new rising searches alert](https://apify.com/xpandalabs/google-trends-monitor/examples/new-rising-searches-alert), [trending now US, UK, Japan](https://apify.com/xpandalabs/google-trends-monitor/examples/trending-now-us-uk-japan), [EV brands in the US](https://apify.com/xpandalabs/google-trends-monitor/examples/ev-brands-google-trends-us), [travel seasonality](https://apify.com/xpandalabs/google-trends-monitor/examples/travel-seasonality-google-trends), [YouTube search trends](https://apify.com/xpandalabs/google-trends-monitor/examples/youtube-search-trends-games).

---

## Pricing

Pay per result, no subscription: hotels $3 per 1,000 (plus $0.006 per hotel for every booking site's rate), flights $1 per 1,000 flights or $2 per 1,000 fare-calendar rows, trends $1.50 per 1,000 results with no start fee. Paid Apify plans get up to 30% off. Set a maximum cost per run and the Actor stops at that limit.

## AI agents and MCP

AI assistants (Claude, ChatGPT, Cursor and others) can call all three Actors as tools through the [Apify MCP server](https://mcp.apify.com): "cheapest 4-star hotel in Shanghai on 20 December", "cheapest day to fly London to New York in January", "is Claude getting more popular than Gemini?"

## Questions

Open an issue on the relevant Actor's Issues tab on Apify, or in this repo.

The data is the public Google Hotels, Google Flights and Google Trends pages any visitor sees. You are responsible for using it in line with applicable laws and Google's terms. The code in this repo is MIT-licensed.
