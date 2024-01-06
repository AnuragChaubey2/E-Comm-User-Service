from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
security = HTTPBasic()

def basic_auth_middleware(credentials: HTTPBasicCredentials = Depends(security)):
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if credentials.username == username and credentials.password == password:
        return True
    else:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )