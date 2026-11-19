#!/usr/bin/env bash
# Google Hotels prices over plain HTTP: one request in, JSON rows out.
# The run-sync endpoint waits for the run (up to 300 s) and returns the dataset items directly.
#
#   APIFY_TOKEN=... ./run-sync.sh
set -euo pipefail

curl -sS -X POST \
  "https://api.apify.com/v2/acts/xpandalabs~google-hotels-rate-monitor/run-sync-get-dataset-items?format=json" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
        "hotels": ["Raffles Singapore"],
        "checkIn": "2026-12-20",
        "checkOut": "2026-12-21",
        "currency": "SGD"
      }'
# Each row has nightlyPrice, every booking site's rate (offers), cheapestSite and the parity check.
# Use format=csv or format=xlsx for spreadsheets.
