from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def verify_token(token):
    try: 
        payload = jwt.decode(token, key=SECRET_KEY)
        return payload
    except Exception as e:
        print("Exception occur", e)

def check_active(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    active = payload.get("is_active")
    if not active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please Active your account",
            headers={"www-Authenticate":"Bearer"}
        )
    else:
        return payload
    
def check_owner(payload:dict= Depends(check_active)):
    role = payload.get("role")
    if role != "owner":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This Route Only Access Owner"
        )
    else:
        return payload
    
def check_admin(payload:dict= Depends(check_active)):
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This Route Only Access Admin"
        )
    else:
        return payload

def check_user(payload:dict= Depends(check_active)):
    role = payload.get("role")
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This Route Only Access Admin"
        )
    else:
        return payload
    