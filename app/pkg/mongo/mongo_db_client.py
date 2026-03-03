from dataclasses import dataclass
from pymongo import MongoClient
from pymongo.database import Database

@dataclass
class MongoConnection:
    client: MongoClient
    database: Database
    

def get_mongoDb(mongo_url: str, db_name: str) -> MongoConnection:
        client = MongoClient(mongo_url)
        client.admin.command("ping")
        return MongoConnection(client=client, database=client[db_name])