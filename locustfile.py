import os
from locust import events

from users.blaze_demo_user_taskset import BlazeDemoUserTaskSetUserClass
from users.json_placeholder_user_taskset import JsonPlaceholderUserTaskSetUserClass

# Optionally define a list of user classes
user_classes = [BlazeDemoUserTaskSetUserClass, JsonPlaceholderUserTaskSetUserClass]

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    # Ensure output directories exist
    os.makedirs("output/reports", exist_ok=True)
    os.makedirs("output/logs", exist_ok=True)
