from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email:Optional[str]
    phone:Optional[str]
    password:Optional[str]
    
class Login(BaseModel):
    email:Optional[str]
    password:Optional[str]   
    
class Post(BaseModel):
    caption:Optional[str]
    owner_id:int 
    image_name:Optional[str]
    