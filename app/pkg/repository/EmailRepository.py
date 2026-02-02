from app.pkg.domain import EmailModel
from pymongo.database import Database
from .BaseRepository import BaseRepository


class EmailRepository(BaseRepository[EmailModel]):
    def __init__(self, session: Database):
        super().__init__(session["emails"], EmailModel)
