import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_mongo_uri() -> str:
    return os.getenv("MONGO_URI", "mongodb://localhost:27017")


def get_database_name() -> str:
    return os.getenv("MONGO_DATABASE", "WebAPIDemoDb")


def get_collection_name() -> str:
    return os.getenv("MONGO_COLLECTION", "SensorData")


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(get_mongo_uri(), serverSelectionTimeoutMS=2000)


def get_sensor_collection():
    database = get_client()[get_database_name()]
    return database[get_collection_name()]
