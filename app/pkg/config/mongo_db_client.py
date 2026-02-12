from pymongo import MongoClient
from app.pkg.util import get_env
from pymongo.database import Database

class MongoConnection:
    def __init__(self) -> None:
        self.mongo_client = MongoClient(get_env("MONGO_URI"))
        self.mongo_client.admin.command("ping")
        self.db = self.mongo_client[str(get_env("MONGO_DB_NAME"))]

    def get_db(self) -> Database:
        return self.db
