from locust import events
from users.blaze_demo_user_taskset import BlazeDemoUserTaskSetUserClass
from users.json_placeholder_user_taskset import JsonPlaceholderUserTaskSetUserClass

# Optionally define a list of user classes
user_classes = [BlazeDemoUserTaskSetUserClass, JsonPlaceholderUserTaskSetUserClass]

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    pass