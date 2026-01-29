from app.pkg.config import MongoDB
from app.pkg.service import Service
from app.pkg.model import EmailCreate
from app.pkg.repository import EmailRepository, LogRepository
from fastapi import APIRouter, status, HTTPException, Depends

router = APIRouter(
    prefix="/api/internal/emails",
    tags=["emails"]
)

def get_instance (db=Depends(MongoDB.connect)) -> Service:
    return Service(EmailRepository(db), LogRepository(db))

#endpoint di test del servizio
@router.post("/v1", status_code=status.HTTP_200_OK)
def send_email(payload: EmailCreate, service : Service = Depends(get_instance)) -> dict:
    try:
        service = service.send_email(payload)
        return {"status": service.email_type.value, "id": str(service.id)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
