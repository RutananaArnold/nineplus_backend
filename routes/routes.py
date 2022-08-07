from fastapi import APIRouter
from schemas.index import User, Login
from models.index import users
from config.db import conn
import bcrypt


user = APIRouter()

@user.post("/register")
def registration(user: User):
    # query to check if there is an existing emails
    existingEmail = conn.execute(
        users.select().where(users.c.email == user.email)).fetchone()
    print(existingEmail)
    
    # if user email exists, return false and exit 
    if existingEmail != None:
        return {"msg" : "This email already exists, please login"}
        
    # user is new   
    password2 = "mypasswordstring"
 
    # Encode password into a readable utf-8 byte code: 
    password = password2.encode('utf-8')  
    # Hash the ecoded password and generate a salt: 
    hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
    print(hashedPassword) 
    result = conn.execute(users.insert().values(
        email=user.email,
        phone=user.phone,
        password=user.password,
    ))
    print(result.lastrowid)
    return {"user_id": result.lastrowid}

@user.post("/login")
def login(login: Login):
    savedEmail = conn.execute(
        users.select().where(users.c.email == login.email)).fetchone()
    print(savedEmail)
    
    if savedEmail['email'].strip() != login.email:
        return {"status": "Wrong Email"}
    
    if savedEmail['password'].strip() != login.password:
        return {"status": "Incorrect password"}
    
    return {'status' : 'logged in','data':savedEmail}

@user.get("/userprofile/{id}")
def getProfile(id: int):
    userProfile = conn.execute(
        users.select().where(users.c.id == id)).fetchone()
    print(userProfile)
    return userProfile
    