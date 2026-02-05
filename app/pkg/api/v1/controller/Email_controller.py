from pkg.service import Service
from pkg.factory import EmailDTO
from pkg.config import Connection
from fastapi import APIRouter, Depends, status
from pkg.repository import email_repo, log_repo

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["emails"]
)


def get_service(session=Depends(Connection.get_db)) -> Service:
    return Service(email_repo(session), log_repo(session))


@router.post("/v1", status_code=status.HTTP_200_OK)
def post_email_request(payload: EmailDTO, service: Service = Depends(get_service)) -> dict:
    result = service.mailto(payload)
    return {
        "status": result.outcome,
        "context": None if result.outcome == "SENT" else result.error
    }
