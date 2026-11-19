"""Rate parity check: is any booking site (OTA) selling your hotel cheaper than your own website?

    pip install apify-client
    export APIFY_TOKEN=...
    python rate_parity_check.py
"""
import os

from apify_client import ApifyClient

HOTELS = ["Park Hyatt Sydney", "Shangri-La Sydney", "Crown Towers Melbourne"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("xpandalabs/google-hotels-rate-monitor").call(run_input={
    "hotels": HOTELS,
    "daysAhead": 14,
    "region": "AU",
})

for h in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"\n{h['name']} ({h['checkIn']}), {len(h.get('offers') or [])} booking sites")
    if h.get("officialSiteNightly") is None:
        print("  no official-site rate listed on Google Hotels")
        continue
    print(f"  official site: {h['officialSiteNightly']} {h['currency']}")
    print(f"  cheapest:      {h['cheapestNightly']} {h['currency']} on {h['cheapestSite']} "
          f"({h['lowestOtaVsOfficialPct']:+.1f}% vs official)")
    if h.get("parityIssue"):
        undercut = [o for o in h["offers"] if not o["isOfficialSite"] and o.get("nightlyBeforeTax")
                    and o["nightlyBeforeTax"] < h["officialSiteNightly"]]
        print("  PARITY ISSUE, cheaper than the official site on: " + ", ".join(o["site"] for o in undercut))
