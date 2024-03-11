from fastapi import APIRouter,Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import Optional, Annotated
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,words
from nltk.stem import PorterStemmer

from ..services.db_service import db_dependency
from ..models.chatbot_model import RoomDetails, History
from .utils import check_user,verify_token

user_router = APIRouter()

user_required = Annotated[str, Depends(check_user)]
MAX_HISTORY_ITEMS = 10

def store_search_history(query: str,userid: int, roomid: int, db:db_dependency):
    existing_history_count = db.query(History).filter(History.user_id == userid).count()
    if existing_history_count >= MAX_HISTORY_ITEMS:
        # Delete the oldest history item
        db.query(History).filter(History.history_id == (
            db.query(History.history_id).filter(History.user_id == userid).order_by(History.history_id).limit(1).subquery())).delete()
        db.commit()
    new_history = History(user_id=userid, room_id=roomid, history=query)
    db.add(new_history)
    db.commit()

def process_query(query):
    tokens = word_tokenize(query)
 
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
 
    # Join the processed tokens back into a string
    processed_query = ' '.join(stemmed_tokens)
 
    return processed_query


@user_router.get('/search/{userid}/{token}')
async def search_property_details(userid:int, token:str,request:Request, query: Optional[str], db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'user':
        processed_query = process_query(query)
    
        history=store_search_history(processed_query, userid, None, db)

        get_room = db.query(RoomDetails).filter(RoomDetails.locality == processed_query.title() , RoomDetails.status == "approved").all()
        if not get_room:
         raise HTTPException(status_code=404, detail="No rooms found at {query} city")
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'details': get_room
        }
    else:
        raise HTTPException(detail='Only User can access this route')

@user_router.get('/get_history/{userid}/{token}')
async def get_history(userid:int, token:str, db: db_dependency, limit: int = 10, page: int = 1, search: str = ''):
    current_user= verify_token(token)

    if current_user['role'] == 'user':
        skip = (page - 1) * limit

        get_history = db.query(History).filter(
        History.history.contains(search),History.user_id==userid).limit(limit).offset(skip).all()
        if not get_history:
            raise HTTPException(status_code=404, detail="No history found")
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'results': len(get_history),
            'property details': get_history
        }
    else:
        raise HTTPException(detail='Only User can access this route')

@user_router.get('/get_all_property_details/{token}',status_code=status.HTTP_200_OK)
async def get_all_property_details(token:str, db: db_dependency,limit: int = 50, page: int = 1):
    current_user= verify_token(token)

    if current_user['role'] == 'user':
        skip = (page - 1) * limit
        approved_items = db.query(RoomDetails).filter(RoomDetails.status == "approved").limit(limit).offset(skip).all()

        return {
            'status':status.HTTP_200_OK, 
            'success':True, 
            'property details': approved_items
        }
    else:
        raise HTTPException(detail='Only User can access this route')

@user_router.get('/get_all_property_details_by_id/{roomId}/{token}',status_code=status.HTTP_200_OK)
async def get_all_property_details_by_id(roomId:int,token:str, db: db_dependency,limit: int = 50, page: int = 1):
    current_user= verify_token(token)

    if current_user['role'] == 'user':
        skip = (page - 1) * limit
        approved_items = db.query(RoomDetails).filter(RoomDetails.room_id==roomId, RoomDetails.status == "approved").first()
        print("+++++++++++++++++", approved_items)
        return {
            'status':status.HTTP_200_OK, 
            'success':True, 
            'property details': approved_items
        }
    else:
        raise HTTPException(detail='Only User can access this route')
    