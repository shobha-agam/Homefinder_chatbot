from pydantic import BaseModel,Field
from enum import Enum
from datetime import datetime
from typing import Optional

class Amenities(str, Enum):
    full_furnished = 'Full-Furnished'
    semi_furnished = 'Semi-Furnished'
    unfurnished = 'UnFurnished'

class Services(str, Enum):
    wifi = 'Wi-Fi'
    food = 'Food'
    washing_machine = 'Washing Machine'
    closet = 'Closet'
    parking = 'Parking'
 
class Bhk(str, Enum):
    rk = '1RK'
    one_bhk = '1-BHK'
    two_bhk = '2-BHK'
    three_bhk = '3-BHK'
    four_bhk = '4-BHK' 

class Beds(str, Enum):
    single = 'Single Bed'
    double = 'Double Beds'
    triple = 'Triple Beds'
    four = 'Four Beds'
    five = 'Five Beds'
    six = 'Six Beds'

class Category(str, Enum):
    flat = 'Flat'
    pg = 'PG'
    hostel = 'Hostel'

class CreateProperty(BaseModel):
    user_id: int
    locality: str
    address: str
    bhk: Bhk
    beds: Optional[str] = None
    rent : int
    carpet_area : float
    amenities : Amenities
    services :Services
    category : Category
    owner_name : str
    owner_mobile : str = Field(min_length=10, max_length=12) 
    created_at : datetime = Field(default_factory= datetime.now)
    updated_at : datetime = Field(default_factory= datetime.now)

class PropertyResponse(CreateProperty):
    status: str

class CreateHistory(BaseModel):
    history : str
    user_id: int
