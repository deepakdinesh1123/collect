import logging
import time
from logging import config

import sentry_sdk
from fastapi import FastAPI, Request

from backend.logging_config import LOGGING_CONFIG
from backend.routes import forms, response, sheets

sentry_sdk.init(
    dsn="https://244597001b6040449ae6601863e1f1da@o4504068650106880.ingest.sentry.io/4504068651548672",  # noqa: E501
    traces_sample_rate=1.0,
)

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("Logger")


origins = ["http://localhost:3000"]

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        f"""start request
        path={request.url.path} method={request.method}
        path_params={request.path_params} query_params={request.query_params}"""
    )
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


app.include_router(forms.router)
app.include_router(response.router)
app.include_router(sheets.router)
