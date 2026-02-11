from threading import Thread
from app.pkg.api import router
from app.pkg.service import Consumer
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status

def start_consuming(sqs = Consumer()):
    sqs.consume_queue(None)

@asynccontextmanager
async def lifespan(_: FastAPI):
    Thread(target=start_consuming, daemon=True).start()
    yield 

app = FastAPI(title="Email Service", lifespan=lifespan)
app.include_router(router)

@app.get("/healthz")
def root(response: Response) -> None:
    response.status_code = status.HTTP_200_OK
