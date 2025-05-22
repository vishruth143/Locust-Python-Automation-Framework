import traceback

from faker import Faker
from config.config import JSON_PLACEHOLDER_BASE_URL
from utilities.common import log_response
from utilities.helpers import build_headers
from utilities.logger import setup_logger

logger = setup_logger()
fake = Faker()


def get_posts(user):
    url = f"{JSON_PLACEHOLDER_BASE_URL}/posts"
    try:
        response = user.client.get(url, headers=build_headers(), name="Get Posts")
        log_response("GET", url, response)
    except Exception as e:
        logger.exception(f"Exception in get_posts:\n{traceback.format_exc()}")


def get_post_by_id(user):
    url = f"{JSON_PLACEHOLDER_BASE_URL}/posts/1"
    try:
        response = user.client.get(url, headers=build_headers(), name="Get Post By ID")
        log_response("GET", url, response)
    except Exception as e:
        logger.exception(f"Exception in get_post_by_id:\n{traceback.format_exc()}")


def create_posts(user):
    url = f"{JSON_PLACEHOLDER_BASE_URL}/posts"
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    try:
        response = user.client.post(url, json=payload, headers=build_headers(), name="Create Posts")
        log_response("POST", url, response, payload=payload)
    except Exception as e:
        logger.exception(f"Exception in create_post:\n{traceback.format_exc()}")