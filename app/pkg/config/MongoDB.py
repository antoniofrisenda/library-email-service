import os
from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.client.admin.command("ping")
        self.conn = self.client[str(os.getenv("MONGO_DB_NAME"))]

    def get_db(self):
        return self.conn
