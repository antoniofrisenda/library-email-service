from fastapi import FastAPI
from threading import Thread
from app.pkg.api import router
from app.pkg.worker import consume

app = FastAPI()

@app.get("/api/internal/emails/health-check/v1")
def ping() -> dict:
    return {"status":"ok"}

app.include_router(router)

def start_consume():
    consume(None)

#runna in background
thread = Thread(target=start_consume, daemon=True).start()
