from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email:Optional[str]
    phone:Optional[str]
    password:Optional[str]
    