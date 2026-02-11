import os
from pymongo import MongoClient
from pymongo.database import Database

class MongoConnection:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.mongo_client.admin.command("ping")
        self.db = self.mongo_client[str(os.getenv("MONGO_DB_NAME"))]

    def get_db(self) -> Database:
        return self.db
