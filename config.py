ORIGIN = "SLC"

# Max price in USD to consider a deal worth reporting
MAX_PRICE_INTERNATIONAL = 700
MAX_PRICE_DOMESTIC = 200

# How many days from today to start searching
SEARCH_START_DAYS = 14
# Check 2 date pairs per destination (6 weeks out, 10 weeks out — both on Tuesdays, cheapest day to fly)
SEARCH_OFFSETS = [42, 70]

# Minimum and maximum trip length in days
TRIP_MIN_DAYS = 7
TRIP_MAX_DAYS = 14

# International destinations — ordered by priority
INTERNATIONAL_DESTINATIONS = [
    ("Seoul", "ICN"),
    ("Bali", "DPS"),
    ("Singapore", "SIN"),
    ("Hong Kong", "HKG"),
    ("London", "LHR"),
    ("Paris", "CDG"),
    ("Rome", "FCO"),
    ("Barcelona", "BCN"),
    ("Lisbon", "LIS"),
    ("Buenos Aires", "EZE"),
    ("Cape Town", "CPT"),
    ("Dubai", "DXB"),
]

# Domestic destinations (only reported if under MAX_PRICE_DOMESTIC)
DOMESTIC_DESTINATIONS = [
    ("Honolulu", "HNL"),
    ("New Orleans", "MSY"),
    ("Miami", "MIA"),
]
