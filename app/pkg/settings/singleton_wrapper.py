from app.pkg.repository import Repo
from app.pkg.service import Service
from app.pkg.config import Connection

conn = Connection()

def _create_instance(session=None) -> Service:
    if session is None:
        session = conn.get_db()

    return Service(Repo(session))