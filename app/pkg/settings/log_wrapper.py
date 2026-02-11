import os
import sys
from loguru import logger


def setup_logger() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO")

    logger.remove()

    logger.add(sys.stdout, level=log_level, enqueue=True)

    os.makedirs("logs", exist_ok=True)

    logger.add("logs/service.log",
               level=log_level,
               rotation="10 MB",
               retention="1 days",
               enqueue=True,
            )
