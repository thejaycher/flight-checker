import os
from datetime import date, timedelta
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

params = {
    "engine": "google_flights",
    "departure_id": "SLC",
    "arrival_id": "NRT",
    "outbound_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
    "return_date": (date.today() + timedelta(days=40)).strftime("%Y-%m-%d"),
    "currency": "USD",
    "hl": "en",
    "api_key": API_KEY,
}

results = GoogleSearch(params).get_dict()
best = results.get("best_flights") or results.get("other_flights")
if best:
    print(f"SLC -> Tokyo (NRT): ${best[0]['price']}")
    print(f"Airline: {best[0]['flights'][0]['airline']}")
else:
    print("No results found")
    print(results.get("error", "Unknown error"))
