from app.pkg.service import Service
from app.pkg.factory import EmailDTO
from app.pkg.config import Connection
from fastapi import APIRouter, Depends, status
from app.pkg.repository import email_repo, log_repo

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["emails"]
)

conn = Connection()


def get_service(session=conn.get_db) -> Service:
    return Service(email_repo(session), log_repo(session))


@router.post("/v1", status_code=status.HTTP_200_OK)
def post_email_request(payload: EmailDTO, service: Service = Depends(get_service)) -> dict:
    result = service.mailto(payload)
    return {
        "status": result.Outcome,
        "context": None if result.Outcome == "SENT" else result.Error
    }
