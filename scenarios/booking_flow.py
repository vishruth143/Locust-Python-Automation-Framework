import traceback

from faker import Faker
from config.config import BLAZEDEMO_BASE_URL
from utilities.common import log_response
from utilities.helpers import build_headers
from utilities.logger import setup_logger

logger = setup_logger()
fake = Faker()

def search_flights(user):
    url = f"{BLAZEDEMO_BASE_URL}/"
    try:
        response=user.client.get(url, headers=build_headers(), name="Search Flights")
        log_response("GET", url, response)
    except Exception as e:
        logger.exception(f"Exception in get_posts:\n{traceback.format_exc()}")

def select_flight(user):
    url = f"{BLAZEDEMO_BASE_URL}/reserve.php"
    # pick random cities
    payload = {
        "fromPort": fake.city(),
        "toPort": fake.city(),
    }
    try:
        response = user.client.post(url, json=payload, headers=build_headers(), name="Select Flight")
        log_response("POST", url, response, payload=payload)
    except Exception:
        logger.exception(f"Exception in select_flight:\n{traceback.format_exc()}")

def book_flight(user):
    url = f"{BLAZEDEMO_BASE_URL}/confirmation.php"
    payload = {
        "inputName": fake.name(),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip": fake.zipcode(),
        "cardType": "Visa",
        "creditCardNumber": fake.credit_card_number(),
        "creditCardMonth": "12",
        "creditCardYear": "2025",
        "nameOnCard": fake.name()
    }
    try:
        response = user.client.post(url, json=payload, headers=build_headers(), name="Book Flight")
        log_response("POST", url, response, payload=payload)
    except Exception:
        logger.exception(f"Exception in select_flight:\n{traceback.format_exc()}")

    # ✅ Finish task sequence so Locust doesn't stop early
    user.interrupt()
