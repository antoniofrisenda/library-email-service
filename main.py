from fastapi import FastAPI
from threading import Thread
from app.pkg.api import router
from app.pkg.worker import consumer

app = FastAPI(title="Email Service")


@app.get("/api/internal/emails/health-check/v1")
def WeGood() -> dict:
    return {"status": "ok"}


app.include_router(router)

sqs = consumer()
def start_consuming():
    sqs.consume_queue(None)


# Loop in background
Thread(target=start_consuming, daemon=True).start()
