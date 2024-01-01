from pydantic import BaseModel, Field, EmailStr, validator
import re 

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