import traceback

from locust import HttpUser, constant, between, task, TaskSet
from config.config import JSON_PLACEHOLDER_BASE_URL, DEFAULT_THINK_TIME
from utilities.helpers import build_headers
from utilities.logger import setup_logger
from utilities.common import log_response


logger = setup_logger()

class JsonPlaceholderUserTaskset(TaskSet):

    @task(2)
    # This will run roughly 3× as often
    def get_posts(self):
        url = f"{JSON_PLACEHOLDER_BASE_URL}/posts"
        try:
            response = self.client.get(url, headers=build_headers(), name="Get Posts")
            log_response("GET", url, response)
        except Exception as e:
            logger.exception(f"Exception in get_posts:\n{traceback.format_exc()}")

    @task(3)
    # This will run roughly 3× as often
    def get_post_by_id(self):
        url = f"{JSON_PLACEHOLDER_BASE_URL}/posts/1"
        try:
            response = self.client.get(url, headers=build_headers(), name="Get Post By ID")
            log_response("GET", url, response)
        except Exception as e:
            logger.exception(f"Exception in get_post_by_id:\n{traceback.format_exc()}")

    @task(1)
    # This runs with weight = 1
    def create_posts(self):
        url = f"{JSON_PLACEHOLDER_BASE_URL}/posts"
        payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        try:
            response = self.client.post(url, json=payload, headers=build_headers(), name="Create Posts")
            self.log_response("POST", url, response, payload=payload)
        except Exception as e:
            logger.exception(f"Exception in create_post:\n{traceback.format_exc()}")

class JsonPlaceholderUserTaskSetUserClass(HttpUser):
    host = JSON_PLACEHOLDER_BASE_URL
    wait_time = constant(DEFAULT_THINK_TIME)
    # wait_time = between(1, 3)
    tasks = [JsonPlaceholderUserTaskset]
