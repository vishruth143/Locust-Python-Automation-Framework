from locust import HttpUser, constant, between, task, TaskSet

from config.config import JSON_PLACEHOLDER_BASE_URL, DEFAULT_THINK_TIME
from scenarios import  json_placeholder_flows

class JsonPlaceholderUserTaskset(TaskSet):

    @task(2)
    # This will run roughly 3× as often
    def get_posts(self):
        json_placeholder_flows.get_posts(self)

    @task(3)
    # This will run roughly 3× as often
    def get_post_by_id(self):
        json_placeholder_flows.get_post_by_id(self)

    @task(1)
    # This runs with weight = 1
    def create_posts(self):
        json_placeholder_flows.create_posts(self)

class JsonPlaceholderUserTaskSetUserClass(HttpUser):
    host = JSON_PLACEHOLDER_BASE_URL
    wait_time = constant(DEFAULT_THINK_TIME)
    # wait_time = between(1, 3)
    tasks = [JsonPlaceholderUserTaskset]
