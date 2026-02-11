from io import BytesIO
from typing import Optional
from app.pkg.service import Service
from app.pkg.config import Connection
from pymongo.database import Database
from app.pkg.factory import email_dto as Request
from app.pkg.repository import email_repo, log_repo
from fastapi import APIRouter, Depends, File, UploadFile, status

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["Emails"]
)

conn = Connection()


def _get_service(session: Database = Depends(conn.get_db)) -> Service:
    return Service(email_repo(session), log_repo(session))


@router.post("/v1", status_code=status.HTTP_200_OK)
async def post_email_request(payload: Request, 
                             attachment: Optional[UploadFile] = File(None), 
                             service: Service = Depends(_get_service)
                            ) -> dict:
    
    if attachment is not None:
        file_stream = BytesIO(await attachment.read())
        result = service.mailto_with_attachments(
            payload, str(attachment.filename), file_stream)
    else:
        result = service.mailto(payload)
        
    return {
        "status": result.Outcome,
        "context": None if result.Outcome == "SENT" else result.Error
    }
