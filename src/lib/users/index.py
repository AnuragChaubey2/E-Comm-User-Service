from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException

MONGO_DB_URL = "mongodb://localhost:27017"
MONGO_DB_NAME = "e-commerce"
MONGO_COLLECTION_NAME = "users"

mongo_client = MongoClient(MONGO_DB_URL)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

async def get_user_by_id(user_id: str):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")