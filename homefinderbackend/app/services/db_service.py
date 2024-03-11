from ..config.db_config import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

session = SessionLocal()

def get_db():
    db= session
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
