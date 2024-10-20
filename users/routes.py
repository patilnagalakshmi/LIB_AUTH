from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user, get_db
from .schemas import User
from .usermodel import User as UserModel

users_router = APIRouter()

@users_router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user












#curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYWdhIiwiZXhwIjoxNzI4OTg1NDgxfQ.fABLVoBXeHX5DafHaB3pVROiIP-Yzrec8tU9uAO6LWQ" http://127.0.0.1:8000/users/me
