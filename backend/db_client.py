import logging
import os

import pymongo
from pymongo import errors

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)

logger = logging.getLogger("Logger")

try:
    client = pymongo.MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))
except errors.InvalidURI:
    logger.error("Given Mongo URI is invalid")
except errors.ConnectionFailure:
    logger.error("Not able to connect to Mongo DB")
