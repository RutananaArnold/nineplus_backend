from fastapi import APIRouter, File, UploadFile
from schemas.index import User, Login, Post
from models.index import users, posts
from config.db import conn
import bcrypt
import shutil
from datetime import datetime


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
    
@user.post("/addpost/{id}")
def addpost(post: Post, id:int, file: UploadFile):
    allowedFiles = {"image/jpeg", "image/png", "image/gif", "image/tiff", "image/bmp", "video/webm"}
    if file.content_type in allowedFiles:
        with open(f'uploaded_images/{file.filename}', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            encodeFile = datetime.now(),'.',file.content_type 
                
            result = conn.execute(posts.insert().values(
                caption=post.caption,
                owner_id=id,  
                image_name=encodeFile
            ))
            print(result.lastrowid)
    return {"msg":"Post added succefully", "post_id": result.lastrowid}


@user.get("/fetchpost/{post_id}")
def getParticularPost(post_id: int):
    post = conn.execute(
        posts.select().where(posts.c.id == post_id)).fetchone()
    print(post)
    return post

@user.get("/fetchALLposts/{page_number}/{number_of_rows_per_page}")
def fetchPosts(page_number: int, number_of_rows_per_page: int ):
    query = posts.select().slice((page_number - 1)*number_of_rows_per_page, ((page_number - 1)*number_of_rows_per_page)+number_of_rows_per_page)
    current_pages_rows = conn.execute(query).fetchall()
   
    print(current_pages_rows)
    return current_pages_rows


@user.post("/uploadfile/")
async def pick_upload_file(file: UploadFile):
    allowedFiles = {"image/jpeg", "image/png", "image/gif", "image/tiff", "image/bmp", "video/webm"}
    if file.content_type in allowedFiles:
        with open(f'uploaded_images/{file.filename}', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            encodeFile = datetime.now(),file.content_type
        return {"filename": file.filename, "file-Type": file.content_type, "Given-Name": encodeFile}
    else:
        return {"message": "There was an error uploading the file(s)"}