from app.pkg.domain import Email
from pymongo.database import Database
from app.pkg.repository.base_db_repository import BaseRepository as repo


class EmailRepository(repo[Email]):
    def __init__(self, session: Database):
        super().__init__(session["emails"], Email)
