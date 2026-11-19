# Google Hotels prices in n8n (or Make / Zapier)

No custom node needed: one **HTTP Request** node calls the Actor and returns the hotel rows.

| Setting | Value |
|---|---|
| Method | `POST` |
| URL | `https://api.apify.com/v2/acts/xpandalabs~google-hotels-rate-monitor/run-sync-get-dataset-items` |
| Authentication | Header `Authorization: Bearer <your Apify token>` |
| Body (JSON) | see below |
| Timeout | 300000 ms (the request waits for the run) |

```json
{
  "myHotel": "Crown Towers Melbourne",
  "hotels": ["Park Hyatt Melbourne", "The Langham Melbourne"],
  "daysAhead": 1,
  "datesToCheck": 7,
  "region": "AU",
  "onlyChanges": true
}
```

Each item that comes back is one hotel and check-in date. Typical next steps:

- **Daily competitor alert**: put a *Schedule Trigger* in front, keep `onlyChanges: true`, and send the items to Slack or email. Only hotels whose price moved come through (your own hotel's rows are always kept).
- **Parity alert**: an *IF* node on `parityIssue = true` to flag days when a booking site undercuts your website.
- **Google Sheets log**: append `checkIn`, `name`, `nightlyPrice`, `rankByPrice`, `vsCompSetAvgPct` to a sheet.

Runs longer than 300 s (big rate shops) are better started with `POST .../runs` and collected with Apify's *Actor run finished* webhook, or with Apify's official n8n / Make / Zapier integrations.
