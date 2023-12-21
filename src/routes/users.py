from pydantic import BaseModel,Field
from fastapi import APIRouter, HTTPException
from src.lib.users.index import get_user_by_id

router = APIRouter(redirect_slashes=False)

# Base pydantic models 
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^[789]\d{9}$'

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    building_no: str = Field(default="")

class Users(BaseModel):
    user_id: str
    email: str
    full_name: str
    phone_number: str
    date_of_birth: str
    address: Address

@router.get("/users/{user_id}", response_model=Users)
async def get_user_by_id_endpoint(user_id: str):
    user = await get_user_by_id({"user_id": user_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

user_router = router