from fastapi import APIRouter,status, Depends, HTTPException, Response, Header
from typing import Annotated

from ..validations.chatbot_validation import CreateProperty
from ..models.chatbot_model import RoomDetails
from ..services.db_service import db_dependency
from .utils import check_owner, verify_token

chatbot_router = APIRouter()

owner_required = Annotated[str, Depends(check_owner)]
fake_secret_token = "coneofsilence"

@chatbot_router.post('/add_property_details/{token}', status_code=status.HTTP_201_CREATED)
async def add_property_details(token:str, request: CreateProperty, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'owner':
        new_data= RoomDetails(**request.dict())
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return {
            'status':status.HTTP_201_CREATED, 
            'success':True,
            "message":"Property Details Added Successfully",
            'added property details': new_data
        }
    

@chatbot_router.get('/get_property_details/{userid}/{token}',status_code=status.HTTP_200_OK)
async def get_property_details(userid:int, token:str, db: db_dependency, limit: int = 10, page: int = 1, search: str = ''):
    current_user= verify_token(token)

    if current_user['role'] == 'owner':
        skip = (page - 1) * limit

        get_room_details = db.query(RoomDetails).filter(RoomDetails.user_id==userid).limit(limit).offset(skip).all()
    
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'results': len(get_room_details), 
            'message':'successfully get all property details',
            'property details': get_room_details
        }
    else:
        raise HTTPException(detail='Only Owner can access this route')

@chatbot_router.get('/get_property_details_id/{userid}/{roomId}/{token}', status_code=status.HTTP_200_OK)
async def get_property_details_by_id(userid:int, roomId: str, token:str, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'owner':
        get_room_details_by_id = db.query(RoomDetails).filter(RoomDetails.room_id == roomId, RoomDetails.user_id==userid).first()

        if not get_room_details_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No room details with this id: {roomId} found")
    
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'message':'successfully get property details',
            'Property details by ID': get_room_details_by_id
        }
    else:
        raise HTTPException(detail='Only Owner can access this route')

@chatbot_router.patch('/update_property_details/{userid}/{roomId}/{token}', status_code=status.HTTP_205_RESET_CONTENT)
async def update_property_details(userid:int, roomId: str,token:str, payload:CreateProperty, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'owner':
        room_query = db.query(RoomDetails).filter(RoomDetails.room_id == roomId, RoomDetails.user_id==userid)
        db_room = room_query.first()

        if not db_room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {roomId} found')
        update_data = payload.dict(exclude_unset=True)
        room_query.filter(RoomDetails.room_id == roomId).update(update_data,
                                                       synchronize_session=False)
        db.commit()
        db.refresh(db_room)
        return {
            'status':status.HTTP_205_RESET_CONTENT, 
            'success':True,
            'property details': db_room
        }
    else:
        raise HTTPException(detail='Only Owner can access this route')


@chatbot_router.delete('/delete_property_details/{userid}/{roomId}/{token}', status_code=status.HTTP_200_OK)
async def delete_property_details(userid:int, roomId: str,token:str, db:db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'owner':
        room_query = db.query(RoomDetails).filter(RoomDetails.room_id == roomId, RoomDetails.user_id==userid)
        roomdetails = room_query.first()
        if not roomdetails:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No Room details with this id: {id} found')
        room_query.delete(synchronize_session=False)
        db.commit()
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'message': "Property details deleted successfully"
        }
    else:
        raise HTTPException(detail='Only Owner can access this route')
    