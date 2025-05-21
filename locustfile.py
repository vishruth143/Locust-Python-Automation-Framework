from locust import events
from users.blaze_demo_user_taskset import BlazeDemoTaskSetUserClass
from users.json_placeholder_user_taskset import JsonPlaceholderTaskSetUserClass

# Optionally define a list of user classes
user_classes = [BlazeDemoTaskSetUserClass, JsonPlaceholderTaskSetUserClass]

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    pass