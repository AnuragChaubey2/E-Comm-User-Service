from fastapi import HTTPException
from src.lib.users.index import get_user_by_email, get_user_by_phone


async def check_duplicate_email_and_phone(updated_user_data, user_id):
    existing_email_user = await get_user_by_email(updated_user_data.email)
    if existing_email_user and existing_email_user["user_id"] != user_id:
        raise HTTPException(status_code=422, detail="Email already exists")

    existing_phone_user = await get_user_by_phone(updated_user_data.phone_number)
    if existing_phone_user and existing_phone_user["user_id"] != user_id:
        raise HTTPException(status_code=422, detail="Phone number already exists")   