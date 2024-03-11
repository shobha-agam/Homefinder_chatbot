from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from ..models.auth_model import User
from ..validations.auth_validation import CreateUser, ChangePassword, UserLogin
from ..services.db_service import db_dependency
from ..services.auth_service import create_access_token, verify_password, get_password_hash
from .utils import verify_token

auth_router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@auth_router.post('/create-user')
async def create_user(db: db_dependency,user_request: CreateUser):
    user_data = User(
        name = user_request.name,
        email= user_request.email,
        mobile = user_request.mobile,
        password = password_context.hash(user_request.password),
        role = user_request.role,
        is_active =user_request.is_active,
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    user_data_dict = {
        
        'name': user_data.name,
        'email': user_data.email,
        'mobile':user_data.mobile,
        'role': user_data.role,
        'is_active': user_data.is_active,
        'created_at': user_data.created_at,
        'updated_at': user_data.updated_at
        # Include other desired fields, excluding password
    }
    
    return{
        "status":status.HTTP_200_OK,
        "success":True,
        "message":"user created sucessfully",
        "user": user_data_dict
    }

@auth_router.post("/login")
def login_user(db: db_dependency,
            form_data: UserLogin):
    user = db.query(User).filter(User.email == form_data.email).first()
    print("user loged in data----===", user.role)

    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_active == False:
       raise HTTPException(
            status_code=401,
            detail="user is deactivated please connect with admin"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token( 
        data={"id":user.user_id,"sub": user.name, "is_active":user.is_active, "role":user.role}, expires_delta=access_token_expires
    )
    
    return {
            "status":status.HTTP_200_OK, 
            "success":True,
            "message":"user logged in sucessfully",
            "user_id": user.user_id,
            "user_role":user.role,
            "access_token": access_token, 
            "token_type": "bearer",
            
        }

@auth_router.post('/change_password')
def change_password(request: ChangePassword, db: db_dependency):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
   
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
   
    encrypted_password = get_password_hash(request.new_password)
    user.password = encrypted_password
    db.commit()
   
    return {
            "status":status.HTTP_200_OK, 
            "success":True,
            "message": "password changed successfully"
        }


@auth_router.get("/get_profile/{token}")
def get_user_profile(token:str, db:db_dependency):
    print("token", token)
    current_user= verify_token(token)
    # print("cureent user=", current_user['role'])
    return {"role":current_user}
