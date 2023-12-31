from fastapi import FastAPI
from src.routes.users import user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])