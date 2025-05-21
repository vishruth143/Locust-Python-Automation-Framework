from locust import HttpUser, task, between
from config.config import BASE_URL
from utils.helpers import build_headers
from utils.logger import setup_logger
import json
import traceback

logger = setup_logger()

class UserBehavior(HttpUser):
    host = BASE_URL
    wait_time = between(1, 3)

    def log_response(self, method, url, response, payload=None):
        log_message = (
            f"{method} {url} | Status: {response.status_code} | "
            f"Request: {json.dumps(payload) if payload else 'N/A'} | "
            f"Response: {response.text[:200]}..."  # Trim long responses
        )
        if response.status_code >= 400:
            logger.error(log_message)
        else:
            logger.info(log_message)

    @task
    def get_posts(self):
        try:
            url = f"{BASE_URL}/posts"
            response = self.client.get(url, headers=build_headers())
            self.log_response("GET", url, response)
        except Exception as e:
            logger.exception(f"Exception in get_posts:\n{traceback.format_exc()}")

    @task
    def get_post_by_id(self):
        try:
            url = f"{BASE_URL}/posts/1"
            response = self.client.get(url, headers=build_headers())
            self.log_response("GET", url, response)
        except Exception as e:
            logger.exception(f"Exception in get_post_by_id:\n{traceback.format_exc()}")

    @task
    def create_post(self):
        url = f"{BASE_URL}/posts"
        payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        try:
            response = self.client.post(url, json=payload, headers=build_headers())
            self.log_response("POST", url, response, payload=payload)
        except Exception as e:
            logger.exception(f"Exception in create_post:\n{traceback.format_exc()}")
