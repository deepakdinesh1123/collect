import logging
import os

from redis import Redis
from rq import Queue
from rq.connections import NoRedisConnectionException

logger = logging.getLogger("Logger")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

redis_connection = Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
try:
    sms_task_queue = Queue(connection=redis_connection)
    sheets_task_queue = Queue(connection=redis_connection)
except NoRedisConnectionException:
    logger.error("Not able to connect to redis")
