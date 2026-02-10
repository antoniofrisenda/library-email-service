from threading import Thread
from app.pkg.api import router
from app.pkg.worker import consumer
from fastapi import FastAPI, Response, status

app = FastAPI(title="Email Service")
app.include_router(router)


@app.get("/healthz")
def root(response: Response) -> None:
    response.status_code = status.HTTP_200_OK


sqs = consumer()


def start_consuming():
    sqs.consume_queue(None)


# Loop in background
Thread(target=start_consuming, daemon=True).start()
