// Google Hotels prices for a city from Node.js.
//
//   npm install apify-client
//   APIFY_TOKEN=... node quickstart.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('xpandalabs/google-hotels-rate-monitor').call({
    searches: ['hotels in Tokyo'],
    checkIn: '2026-12-20',
    checkOut: '2026-12-21',
    currency: 'JPY',
    maxHotels: 18,
    minStars: 4,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const h of items) {
    console.log(`${h.name.slice(0, 45).padEnd(45)} ${h.stars ?? '-'}★ ${h.nightlyPrice ?? 'n/a'} ${h.currency}`);
}
