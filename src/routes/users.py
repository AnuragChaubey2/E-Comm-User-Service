from fastapi import APIRouter, HTTPException
import logging
from src.lib.users.index import (
    get_user_by_id, 
    save_user_to_mongo,
    getAllUsers, 
    UpdatedUser,
    removeUser,
)
from src.models.users import UsersBase, UsersCreate
from service.user import check_duplicate_email_and_phone
from passlib.hash import bcrypt
from typing import List
from src.utils import generate_uuid

router = APIRouter(redirect_slashes=False)

logging.basicConfig(level=logging.INFO)
    
#-------------------------GetUsersByID-------------------------------------    

@router.get("/users/{user_id}", response_model=UsersBase)
async def get_user_by_id_endpoint(user_id: str):
    user = await get_user_by_id({"user_id": user_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

user_router = router

#-------------------------Create-------------------------------------

@router.post("/users", response_model=dict)
async def create_user(user: UsersCreate):
    hashed_password = bcrypt.hash(user.password)
    
    user_data = {
        "user_id": generate_uuid(),
        "email": user.email,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "date_of_birth": user.date_of_birth,
        "address": user.address.dict(),
        "password": hashed_password,
    }

    await check_duplicate_email_and_phone(user, user_data)

    result = await save_user_to_mongo(user_data)

    response_data = {"user_id": str(result)}

    return response_data

#-------------------------Update-------------------------------------

@router.put("/users/{user_id}", response_model=UsersBase)   
async def update_user(user_id: str, updated_user_data: UsersCreate):
    existing_user = await get_user_by_id({"user_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = bcrypt.hash(updated_user_data.password)

    user_data = {
        "user_id": user_id,
        "email": updated_user_data.email,
        "full_name": updated_user_data.full_name,
        "phone_number": updated_user_data.phone_number,
        "date_of_birth": updated_user_data.date_of_birth,
        "address": updated_user_data.address.dict(),
        "password": hashed_password,
    }

    await check_duplicate_email_and_phone(updated_user_data, user_id)

    result = await UpdatedUser(user_data)

    if result:
        return user_data
    else:
        raise HTTPException(status_code=500, detail="Failed to update user")
    
#-------------------------GetAll-------------------------------------    

@router.get("/users", response_model=List[UsersBase])
async def get_all_users():
    users = await getAllUsers()

    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="No users found")
    
#-------------------------Delete------------------------------------- 
    
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    deleted_user = await removeUser({"user_id": user_id})
    if deleted_user:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found") 