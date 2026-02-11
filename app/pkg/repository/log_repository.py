from app.pkg.domain import Log
from pymongo.database import Database
from app.pkg.repository.base_repository import BaseRepository as repo


class LogRepository(repo[Log]):
    def __init__(self, session: Database):
        super().__init__(session["logs"], Log)
