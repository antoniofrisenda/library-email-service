from pymongo.database import Database
from .BaseRepository import BaseRepository
from app.pkg.model.log import LogCreate, LogRead


class LogRepository(BaseRepository[LogCreate, LogRead]):
    def __init__(self, db: Database):
        super().__init__(db["logs"], LogRead)
