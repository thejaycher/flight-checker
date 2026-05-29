from dotenv import load_dotenv
load_dotenv()
from emailer import send_deal_alert

test_deals = [
    {"name": "Tokyo", "code": "NRT", "price": 650, "airline": "Japan Airlines", "depart": "2026-07-15", "return": "2026-07-25"},
    {"name": "Lisbon", "code": "LIS", "price": 480, "airline": "TAP Air Portugal", "depart": "2026-08-01", "return": "2026-08-10"},
]

send_deal_alert(test_deals)
