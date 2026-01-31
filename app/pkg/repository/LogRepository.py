from app.pkg.domain import LogModel
from pymongo.database import Database
from .BaseRepository import BaseRepository


class LogRepository(BaseRepository[LogModel]):
    def __init__(self, db: Database):
        super().__init__(db["logs"], LogModel)
