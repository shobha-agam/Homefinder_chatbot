from sqlalchemy import Column, String, Integer,Boolean, DateTime,ForeignKey, Float
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from ..config.db_config import Base
from ..validations.chatbot_validation import Bhk, Amenities, Services, Category

class RoomDetails(Base):

    __tablename__ = 'room_details'
    room_id = Column(Integer, primary_key=True)
    locality= Column(String)
    address = Column(String)
    bhk= Column(Enum(Bhk), default=Bhk.rk)
    beds = Column(String, nullable=True)
    rent = Column(Integer)
    carpet_area = Column(Float)
    amenities = Column(Enum(Amenities), default=Amenities.semi_furnished)
    services = Column(Enum(Services), default=Services.wifi)
    category = Column(Enum(Category), default=Category.flat)
    owner_name = Column(String)
    owner_mobile = Column(String)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    users= relationship("User", back_populates="room_detils") 
    historys= relationship("History", back_populates="rooms")

class History(Base):

    __tablename__ = 'history'
    history_id = Column(Integer, primary_key=True)
    history = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, )
    user_id = Column(Integer, ForeignKey("users.user_id"))
    room_id = Column(Integer,ForeignKey("room_details.room_id"))
    users = relationship("User", back_populates="histories")
    rooms = relationship("RoomDetails", back_populates="historys")
