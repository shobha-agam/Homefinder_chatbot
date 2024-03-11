from pydantic import BaseModel,Field, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional

class Roles(str, Enum):
    user = 'user'
    admin = 'admin'
    owner = 'owner'

class CreateUser(BaseModel):
   
    name : str = Field(min_length=4, max_length=50)
    email : EmailStr
    password : str = Field(min_length=5, max_length=20)
    mobile: str = Field(min_length=10, max_length=12) 
    role : Roles 
    is_active : bool = Field(default=True)
    created_at : datetime = Field(default_factory= datetime.now)
    updated_at : datetime = Field(default_factory= datetime.now)

class UserResponse(BaseModel):
    name : str 
    email : EmailStr
    mobile: str  
    role : str 
    is_active : bool 
    created_at : datetime 
    updated_at : datetime 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Update_User(BaseModel):
    name : str = Field(min_length=5, max_length=50)
    email : EmailStr
    role : str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id:int
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None
    expires: datetime
    
class ChangePassword(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
