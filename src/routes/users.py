from pydantic import BaseModel, validator
from fastapi import APIRouter, HTTPException
from src.lib.users.index import get_user_by_id
import re

router = APIRouter(redirect_slashes=False)

# Base pydantic models 
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^[789]\d{9}$'

class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    building_no: str

class Users(BaseModel):
    name: str
    email: str
    full_name: str
    phone_number: str
    date_of_birth: str
    address: Address

    @validator('email', always=True)
    def check_email_required(cls, value):
        if not value:
            raise ValueError('Email Field is required')
        return value

    @validator('email', always=True)
    def check_valid_email(cls, value):
        if not re.match(EMAIL_REGEX, value):
            raise ValueError('Email is Invalid')
        return value

    @validator('phone_number', always=True)
    def check_phone_required(cls, value):
        if not value:
            raise ValueError('Phone Field is required')
        return value

    @validator('phone_number', always=True)
    def check_valid_phone(cls, value):
        if not re.match(PHONE_REGEX, value):
            raise ValueError('Invalid Phone Number')
        return value

@router.get("/users/{user_id}", response_model=Users)
async def get_user_by_id_endpoint(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

user_router = router