from app.pkg.config import MongoDB
from app.pkg.service import Service
from app.pkg.factory import EmailDTO
from fastapi import APIRouter, Depends, status
from app.pkg.repository import EmailRepository, LogRepository

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["emails"]
)


def get_instance(db=Depends(MongoDB.connect)) -> Service:
    return Service(EmailRepository(db), LogRepository(db))


@router.post("/v1", status_code=status.HTTP_200_OK)
def send_email(payload: EmailDTO, service: Service = Depends(get_instance)) -> dict:
    email = service.send_email(payload)
    return {"status": email.email_type.value, "id": str(email.id)}
