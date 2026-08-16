from pymongo import MongoClient
from django.conf import settings

class MongoDBService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            # Connect to MongoDB
            cls._client = MongoClient(settings.MONGO_URI)
        return cls._client

    @classmethod
    def get_db(cls):
        client = cls.get_client()
        return client[settings.MONGO_DB_NAME]

    @classmethod
    def get_collection(cls, collection_name):
        db = cls.get_db()
        return db[collection_name]