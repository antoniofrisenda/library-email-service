from pymongo.database import Database
from .BaseRepository import BaseRepository
from app.pkg.model import EmailCreate, EmailRead


class EmailRepository(BaseRepository[EmailCreate, EmailRead]):
    def __init__(self, db: Database):
        super().__init__(db["emails"], EmailRead)
