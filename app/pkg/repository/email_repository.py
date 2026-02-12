from app.pkg.domain import Email
from pymongo.database import Database
from app.pkg.repository.base_repository import BaseRepository as repo


class EmailRepository(repo[Email]):
    def __init__(self, db: Database) -> None:
        super().__init__(db["emails"], Email)
