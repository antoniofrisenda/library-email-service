import logging
from threading import Thread
from app.pkg.api import router
from app.pkg.aws import Receiver
from app.pkg.util import LOG_SETUP
from app.pkg.service import Consumer
from logging.config import dictConfig
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status

dictConfig(LOG_SETUP)

logger = logging.getLogger("app")

def _get_queue() -> Receiver:
    return Receiver()

def start_consuming():
    try:
        Consumer(_get_queue()).consume_queue()
    except Exception:
        logger.exception("Consumer crashed")


@asynccontextmanager
async def _on_launch(_: FastAPI):
    Thread(target=start_consuming, daemon=True).start()
    yield

app = FastAPI(title="Email Service", lifespan=_on_launch)


@app.get("/healthz")
async def ping(response: Response) -> None:
    response.status_code = status.HTTP_200_OK

app.include_router(router)
