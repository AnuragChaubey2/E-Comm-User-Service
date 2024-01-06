from pymongo import MongoClient
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv('MONGO_DB_URL'))
db = mongo_client[os.getenv('MONGO_DB_NAME')]
collection = db[os.getenv('MONGO_COLLECTION_NAME')]


# ---------------------------Create---------------------------
async def save_user_to_mongo(user_data):
    result = collection.insert_one(user_data)
    return result.inserted_id

# ---------------------------GetByID---------------------------
async def get_user_by_id(query):
    user = collection.find_one(query, {'_id': 0})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# ---------------------------GetAll---------------------------    
async def getAllUsers():
    users_cursor = collection.find({})
    users_list = list(users_cursor)
    return users_list

# ---------------------------Delete---------------------------
async def removeUser(query):
    result = collection.delete_one(query)
    return result.deleted_count == 1

# ---------------------------Update---------------------------
async def UpdatedUser(updated_user_data: dict) -> bool:
    result = collection.update_one({"user_id": updated_user_data["user_id"]}, {"$set": updated_user_data})
    return result.modified_count > 0

async def get_user_by_email(email: str):
    user = collection.find_one({"email": email}, {'_id': 0})
    return user

async def get_user_by_phone(phone: str):
    user = collection.find_one({"phone_number": phone}, {'_id': 0})
    return user