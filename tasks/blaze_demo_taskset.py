import traceback

from locust import HttpUser, constant, task, TaskSet
from faker import Faker
from config.config import BLAZEDEMO_BASE_URL
from utilities.helpers import build_headers
from utilities.logger import setup_logger
from utilities.common import log_response

logger = setup_logger()

fake = Faker()

class BlazeDemo(TaskSet):

    @task
    def search_flights(self):
        url = f"{BLAZEDEMO_BASE_URL}/"
        try:
            response = self.client.get(url, headers=build_headers())
            log_response("GET", url, response)
        except Exception as e:
            logger.exception(f"Exception in get_posts:\n{traceback.format_exc()}")

    @task
    def select_flight(self):
        # pick random cities
        from_city = fake.city()
        to_city = fake.city()

        url = f"{BLAZEDEMO_BASE_URL}/reserve.php"
        payload = {
            "fromPort": from_city,
            "toPort": to_city,
        }
        try:
            response = self.client.post(
                url,
                json=payload,
                headers=build_headers(),
                name="Select Flight"
            )
            log_response("POST", url, response, payload=payload)
        except Exception:
            logger.exception(f"Exception in select_flight:\n{traceback.format_exc()}")

class BlazeDemoUserClass(HttpUser):
    host = BLAZEDEMO_BASE_URL
    wait_time = constant(1)
    tasks = [BlazeDemo]
