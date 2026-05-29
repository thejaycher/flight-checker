import os
import json
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from serpapi import GoogleSearch
from emailer import send_deal_alert
import config

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
DESTINATIONS_PER_RUN = 5


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_index": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


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
        return best[0].get("price")
    except Exception as e:
        print(f"  Error searching {destination_code}: {e}")
        return None


def get_todays_destinations():
    all_destinations = [
        (name, code, "international") for name, code in config.INTERNATIONAL_DESTINATIONS
    ] + [
        (name, code, "domestic") for name, code in config.DOMESTIC_DESTINATIONS
    ]

    state = load_state()
    start = state["last_index"] % len(all_destinations)
    end = start + DESTINATIONS_PER_RUN

    # Wrap around if we hit the end of the list
    if end <= len(all_destinations):
        batch = all_destinations[start:end]
    else:
        batch = all_destinations[start:] + all_destinations[:end - len(all_destinations)]

    state["last_index"] = end % len(all_destinations)
    save_state(state)

    return batch


def find_deals(destinations):
    today = date.today()
    start = today + timedelta(days=config.SEARCH_START_DAYS)

    date_pairs = [
        (start + timedelta(weeks=w), start + timedelta(weeks=w, days=trip_len))
        for w in range(config.SEARCH_WEEKS)
        for trip_len in [config.TRIP_MIN_DAYS, config.TRIP_MAX_DAYS]
    ]

    international_deals = []
    domestic_deals = []
    total = len(destinations) * len(date_pairs)
    checked = 0

    for name, code, kind in destinations:
        best_price = None
        best_dates = None

        for depart, ret in date_pairs:
            checked += 1
            print(f"[{checked}/{total}] Checking {name} ({code}) {depart} -> {ret}   ", end="\r")
            price = search_flights(config.ORIGIN, code, depart, ret)
            if price and (best_price is None or price < best_price):
                best_price = price
                best_dates = (depart, ret)
            time.sleep(0.5)

        if best_price is None:
            continue

        threshold = config.MAX_PRICE_INTERNATIONAL if kind == "international" else config.MAX_PRICE_DOMESTIC
        if best_price <= threshold:
            entry = {
                "name": name,
                "code": code,
                "price": best_price,
                "depart": str(best_dates[0]),
                "return": str(best_dates[1]),
            }
            if kind == "international":
                international_deals.append(entry)
            else:
                domestic_deals.append(entry)

    return international_deals, domestic_deals


def print_deals(international, domestic, destinations_checked):
    names = ", ".join(f"{n} ({c})" for n, c, _ in destinations_checked)
    print(f"\n{'=' * 60}")
    print(f"  FLIGHT DEALS FROM {config.ORIGIN}  --  {date.today()}")
    print(f"  Checked: {names}")
    print("=" * 60)

    if international:
        print(f"\n  INTERNATIONAL (under ${config.MAX_PRICE_INTERNATIONAL})\n")
        for d in sorted(international, key=lambda x: x["price"]):
            print(f"  ${d['price']:>4}  {d['name']} ({d['code']})")
            print(f"         {d['depart']} -> {d['return']}")
    else:
        print("\n  No international deals under threshold today.")

    if domestic:
        print(f"\n  DOMESTIC STEALS (under ${config.MAX_PRICE_DOMESTIC})\n")
        for d in sorted(domestic, key=lambda x: x["price"]):
            print(f"  ${d['price']:>4}  {d['name']} ({d['code']})")
            print(f"         {d['depart']} -> {d['return']}")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    destinations = get_todays_destinations()
    names = [n for n, _, _ in destinations]
    print(f"Today's batch: {', '.join(names)}")

    intl, dom = find_deals(destinations)
    print_deals(intl, dom, destinations)

    all_deals = intl + dom
    if all_deals:
        send_deal_alert(all_deals)
    else:
        print("No deals found today — no email sent.")
