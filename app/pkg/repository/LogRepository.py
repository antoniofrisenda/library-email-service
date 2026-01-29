from app.pkg.model import LogRead
from pymongo.database import Database
from .BaseRepository import BaseRepository


class LogRepository(BaseRepository[LogRead]):
    def __init__(self, db: Database):
        super().__init__(db["logs"], LogRead)

