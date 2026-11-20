from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB

_client = None


def get_mongo_client() -> MongoClient:
    """Return a MongoDB client instance configured with a 3000ms server selection timeout."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    return _client


def get_database():
    """Return the application MongoDB database instance."""
    client = get_mongo_client()
    return client[MONGO_DB]


def check_mongo_connection() -> bool:
    """Test the MongoDB connection by running a ping command.
    Returns True if MongoDB is up, False if down. Never raises an unhandled exception.
    """
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True
    except Exception:
        return False
