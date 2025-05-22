from locust import HttpUser, constant, task, SequentialTaskSet

from config.config import BLAZEDEMO_BASE_URL, DEFAULT_THINK_TIME
from scenarios import blaze_demo_flows

class BlazeDemoUserSequentialTaskSet(SequentialTaskSet):
    @task
    def search_flight(self):
        blaze_demo_flows.search_flights(self)

    @task
    def select_flight(self):
        blaze_demo_flows.select_flight(self)

    @task
    def book_flight(self):
        blaze_demo_flows.book_flight(self)

class BlazeDemoUserSequentialTaskSetUserClass(HttpUser):
    host = BLAZEDEMO_BASE_URL
    wait_time = constant(DEFAULT_THINK_TIME)
    tasks = [BlazeDemoUserSequentialTaskSet]
