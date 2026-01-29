from app.pkg.model import EmailRead
from pymongo.database import Database
from .BaseRepository import BaseRepository


class EmailRepository(BaseRepository[EmailRead]):
    def __init__(self, db: Database):
        super().__init__(db["emails"], EmailRead)
