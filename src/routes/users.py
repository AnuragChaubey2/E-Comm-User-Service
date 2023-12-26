from pydantic import BaseModel, Field, EmailStr, validator
from fastapi import APIRouter, HTTPException
from src.lib.users.index import get_user_by_id, save_user_to_mongo, getAllUsers, removeUser
from passlib.hash import bcrypt
import re
from typing import List
from src.utils import generate_uuid

router = APIRouter(redirect_slashes=False)

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^[6-9]\d{9}$'

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    building_no: str = Field(default="")

class UsersBase(BaseModel):
    user_id: str
    email: str
    full_name: str
    phone_number: str
    date_of_birth: str
    address: Address

class UsersCreate(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: str
    date_of_birth: str
    address: Address
    password: str

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(PHONE_REGEX, value):
            raise ValueError("Invalid phone number format")
        return value

    @validator("email")
    def validate_email(cls, value):
        if not re.match(EMAIL_REGEX, value):
            raise ValueError("Invalid email address format")
        return value

@router.get("/users/{user_id}", response_model=UsersBase)
async def get_user_by_id_endpoint(user_id: str):
    user = await get_user_by_id({"user_id": user_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

user_router = router

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

    result = await save_user_to_mongo(user_data)

    response_data = {"user_id": str(result)}

    return response_data

@router.get("/users", response_model=List[UsersBase])
async def get_all_users():
    users = await getAllUsers()

    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="No users found")
    
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    deleted_user = await removeUser({"user_id": user_id})
    if deleted_user:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")