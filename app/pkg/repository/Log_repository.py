from app.pkg.domain import LogModel
from pymongo.database import Database
from .Base_repository import BaseRepository


class LogRepository(BaseRepository[LogModel]):
    def __init__(self, session: Database):
        super().__init__(session["logs"], LogModel)
