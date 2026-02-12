from io import BytesIO
from typing import Optional
from app.pkg.service import Service
from app.pkg.repository import Repo
from app.pkg.config import Connection
from pymongo.database import Database
from app.pkg.factory import Dto as Request
from fastapi import APIRouter, Depends, File, UploadFile, status, Body

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["Emails"],
)

def _get_instance() -> Service:
    return Service(Repo(Connection().get_db()))


@router.post("/v1", status_code=status.HTTP_202_ACCEPTED)
async def post_email_request(payload: Request = Body(...), service: Service = Depends(_get_instance),
                             attachment: Optional[UploadFile] = File(None),
                             ) -> dict:

    if not attachment:
        service.mailto(payload)
    else:
        file_stream = BytesIO(await attachment.read())
        file_stream.seek(0)
        service.mailto_with_attachments(
            payload, str(attachment.filename), file_stream)

    return {"status": "ACCEPTED"}
