from locust import HttpUser, constant, task, TaskSet

from config.config import BLAZEDEMO_BASE_URL, DEFAULT_THINK_TIME
from scenarios import blaze_demo_flows


class BlazeDemoUserTaskSet(TaskSet):
    @task
    def search_flight(self):
        blaze_demo_flows.search_flights(self)

    @task
    def select_flight(self):
        blaze_demo_flows.select_flight(self)

    @task
    def book_flight(self):
        blaze_demo_flows.book_flight(self)

class BlazeDemoUserTaskSetUserClass(HttpUser):
    host = BLAZEDEMO_BASE_URL
    wait_time = constant(DEFAULT_THINK_TIME)
    tasks = [BlazeDemoUserTaskSet]
