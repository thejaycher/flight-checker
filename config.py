ORIGIN = "SLC"

# Max price in USD to consider a deal worth reporting
MAX_PRICE_INTERNATIONAL = 700
MAX_PRICE_DOMESTIC = 200

# How many days from today to start searching
SEARCH_START_DAYS = 14
# How many departure dates to check (one per week)
SEARCH_WEEKS = 12

# Minimum and maximum trip length in days
TRIP_MIN_DAYS = 5
TRIP_MAX_DAYS = 21

# International destinations to scan
INTERNATIONAL_DESTINATIONS = [
    ("Tokyo", "NRT"),
    ("Osaka", "KIX"),
    ("Seoul", "ICN"),
    ("Bangkok", "BKK"),
    ("Bali", "DPS"),
    ("Singapore", "SIN"),
    ("Hong Kong", "HKG"),
    ("London", "LHR"),
    ("Paris", "CDG"),
    ("Rome", "FCO"),
    ("Barcelona", "BCN"),
    ("Amsterdam", "AMS"),
    ("Lisbon", "LIS"),
    ("Dublin", "DUB"),
    ("Reykjavik", "KEF"),
    ("Cancun", "CUN"),
    ("Mexico City", "MEX"),
    ("Bogota", "BOG"),
    ("Lima", "LIM"),
    ("Buenos Aires", "EZE"),
    ("Cape Town", "CPT"),
    ("Nairobi", "NBO"),
    ("Dubai", "DXB"),
    ("Sydney", "SYD"),
    ("Auckland", "AKL"),
]

# Domestic destinations (only reported if under MAX_PRICE_DOMESTIC)
DOMESTIC_DESTINATIONS = [
    ("New York", "JFK"),
    ("Miami", "MIA"),
    ("Chicago", "ORD"),
    ("New Orleans", "MSY"),
    ("Nashville", "BNA"),
    ("Seattle", "SEA"),
    ("Portland", "PDX"),
    ("Honolulu", "HNL"),
]
