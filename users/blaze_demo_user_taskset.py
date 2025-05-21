from locust import HttpUser, constant, task, TaskSet

from config.config import BLAZEDEMO_BASE_URL, DEFAULT_THINK_TIME
from scenarios import booking_flow


class BlazeDemoUserTaskSet(TaskSet):
    @task
    def search_flight(self):
        booking_flow.search_flights(self)

    @task
    def select_flight(self):
        booking_flow.select_flight(self)

    @task
    def book_flight(self):
        booking_flow.book_flight(self)

class BlazeDemoUserTaskSetUserClass(HttpUser):
    host = BLAZEDEMO_BASE_URL
    wait_time = constant(DEFAULT_THINK_TIME)
    tasks = [BlazeDemoUserTaskSet]
