import os
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from serpapi import GoogleSearch
import config

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")


def search_flights(origin, destination_code, depart_date, return_date):
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination_code,
        "outbound_date": depart_date.strftime("%Y-%m-%d"),
        "return_date": return_date.strftime("%Y-%m-%d"),
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY,
    }
    try:
        results = GoogleSearch(params).get_dict()
        best = results.get("best_flights") or results.get("other_flights")
        if not best:
            return None
        flight = best[0]
        price = flight.get("price")
        return price
    except Exception as e:
        print(f"  Error searching {destination_code}: {e}")
        return None


def find_deals():
    today = date.today()
    start = today + timedelta(days=config.SEARCH_START_DAYS)

    # Build list of (departure, return) date pairs — one per week
    date_pairs = []
    for week in range(config.SEARCH_WEEKS):
        depart = start + timedelta(weeks=week)
        for trip_len in [config.TRIP_MIN_DAYS, config.TRIP_MAX_DAYS]:
            date_pairs.append((depart, depart + timedelta(days=trip_len)))

    international_deals = []
    domestic_deals = []

    all_destinations = [
        (name, code, "international") for name, code in config.INTERNATIONAL_DESTINATIONS
    ] + [
        (name, code, "domestic") for name, code in config.DOMESTIC_DESTINATIONS
    ]

    total = len(all_destinations) * len(date_pairs)
    checked = 0

    for name, code, kind in all_destinations:
        best_price = None
        best_dates = None

        for depart, ret in date_pairs:
            checked += 1
            print(f"[{checked}/{total}] {name} ({code}) — {depart} to {ret}", end="\r")
            price = search_flights(config.ORIGIN, code, depart, ret)
            if price and (best_price is None or price < best_price):
                best_price = price
                best_dates = (depart, ret)
            time.sleep(0.5)  # stay well within rate limits

        if best_price is None:
            continue

        threshold = config.MAX_PRICE_INTERNATIONAL if kind == "international" else config.MAX_PRICE_DOMESTIC
        if best_price <= threshold:
            entry = {
                "name": name,
                "code": code,
                "price": best_price,
                "depart": best_dates[0],
                "return": best_dates[1],
            }
            if kind == "international":
                international_deals.append(entry)
            else:
                domestic_deals.append(entry)

    return international_deals, domestic_deals


def print_deals(international, domestic):
    print("\n" + "=" * 60)
    print(f"  FLIGHT DEALS FROM {config.ORIGIN}  —  {date.today()}")
    print("=" * 60)

    if international:
        print(f"\n INTERNATIONAL (under ${config.MAX_PRICE_INTERNATIONAL})\n")
        for d in sorted(international, key=lambda x: x["price"]):
            print(f"  ${d['price']:>4}  {d['name']} ({d['code']})")
            print(f"         {d['depart']} -> {d['return']}")
    else:
        print("\n  No international deals found under the threshold today.")

    if domestic:
        print(f"\n DOMESTIC STEALS (under ${config.MAX_PRICE_DOMESTIC})\n")
        for d in sorted(domestic, key=lambda x: x["price"]):
            print(f"  ${d['price']:>4}  {d['name']} ({d['code']})")
            print(f"         {d['depart']} -> {d['return']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print(f"Scanning flights from {config.ORIGIN}...")
    intl, dom = find_deals()
    print_deals(intl, dom)
