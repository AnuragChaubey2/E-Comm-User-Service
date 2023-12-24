from pymongo import MongoClient
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv('MONGO_DB_URL'))
db = mongo_client[os.getenv('MONGO_DB_NAME')]
collection = db[os.getenv('MONGO_COLLECTION_NAME')]


async def save_user_to_mongo(user_data):
    result = collection.insert_one(user_data)
    return result.inserted_id

async def get_user_by_id(query):
    user = collection.find_one(query, {'_id': 0})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")