from sqlalchemy import Column, String, Integer,Boolean, DateTime, Float
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from ..config.db_config import Base
from ..validations.auth_validation import Roles

class User(Base):

    __tablename__ = "users"
    user_id  = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email= Column(String)
    mobile = Column(String)    
    password = Column(String)
    role = Column(Enum(Roles), default=Roles.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    room_detils = relationship("RoomDetails", back_populates="users")
    histories = relationship("History", back_populates="users")
