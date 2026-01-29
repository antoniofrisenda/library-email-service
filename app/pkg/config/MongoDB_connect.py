import os
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.conn = self.client[str(os.getenv("DB_NAME"))]

    def connect(self):
        return self.conn
