from appwrite.client import Client
from appwrite.services.storage import Storage

from config.environments import (
    APPWRITE_ENDPOINT,
    APPWRITE_PROJECT_ID,
    APPWRITE_SECRET_API_KEY,
)


class Appwrite:
    def __init__(self):
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_SECRET_API_KEY)
        self.storage = Storage(client)
