from fastapi import APIRouter
from schemas.index import User
from config.db import conn


user = APIRouter()

@user.get("/fetch")
def display():
    return {"msg": "hello"}

@user.post("/register")
def registration(user: User):
    result = conn.execute(users.insert().values(
        phone=user.phone,
        email=user.email,
        password=user.password,
    ))
    print(result.lastrowid)
    return {"user_id": result.lastrowid}