# db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

_client = None
_db = None


def connect_mongo() -> None:
    global _client
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI is missing")
    _client = AsyncIOMotorClient(uri)

def close_mongo() -> None:
    global _client
    if _client:
        _client.close()
        _client = None




def init_db():
    global _client, _db
    if _client is None:
        uri = os.getenv("MONGODB_URI")
        _client = MongoClient(uri)
        _db = _client[os.getenv("MONGODB_DB", "web_crawler_rag")]

def get_db():
    if _db is None:
        init_db()
    return _db
