from fastapi import APIRouter,status, Depends, HTTPException
from typing import Annotated

from .utils import verify_token, check_admin
from ..services.db_service import db_dependency
from ..models.auth_model import User
from ..models.chatbot_model import RoomDetails
from ..validations.auth_validation import UserResponse

admin_router = APIRouter()
admin_required = Annotated[str, Depends(check_admin)]

@admin_router.get('/get_user_details/{token}',status_code=status.HTTP_200_OK)
async def get_user_details(token:str, db: db_dependency,limit: int = 50, page: int = 1, search: str = ''):
    current_user= verify_token(token)
    
    if current_user['role'] == 'admin':
        user_details = db.query(User).filter(
        User.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        user_data = [{'id':user.user_id, 'name': user.name, 'email': user.email, 'mobile': user.mobile, 'role':user.role, 
                  'is_active':user.is_active, 'created_at':user.created_at, 'updated_at':user.updated_at} for user in user_details]
        return {
            "status":status.HTTP_200_OK, 
            "success":True, 
            'results': len(user_details),
            'user_details': user_data
        }
    else:
        raise HTTPException(detail='Only admin can access this route')


@admin_router.get('/get_user_details_by_id/{userId}/{token}',status_code=status.HTTP_200_OK)
async def get_user_details_by_id(userId:int, token:str, db: db_dependency, limit: int = 50, page: int = 1, search: str = ''):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        skip = (page - 1) * limit

        get_user_details = db.query(User).filter(
        User.name.contains(search)).filter(User.user_id == userId).first()

        if not get_user_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user details with this id: {userId} found")
        user_data = {
        'id': get_user_details.user_id,
        'name': get_user_details.name,
        'email': get_user_details.email,
        'mobile':get_user_details.mobile,
        'role': get_user_details.role,
        'is_active': get_user_details.is_active,
        'created_at': get_user_details.created_at,
        'updated_at': get_user_details.updated_at
        # Includeing other desired fields, excluding password
        }
        return {
                "status":status.HTTP_200_OK, 
                "success":True,
                'user details': user_data
            }
    else:
        raise HTTPException(detail='Only admin can access this route')



@admin_router.put('/update_activation/{userId}/{token}/{is_active}')
async def update_user_activation(userId:int,token:str, is_active:bool, db: db_dependency):
    current_user= verify_token(token)
    print("======================", current_user['role'])
    
    if current_user['role'] == 'admin':
        db_update_activation= db.query(User).filter(User.user_id==userId).first()
        db_update_activation.is_active=is_active
        db.add(db_update_activation)
        db.commit()

        if not db_update_activation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
        return{
            "status":status.HTTP_200_OK, 
            "success":True,
            "messge": "active Status is updated succesfully"
        }
        

@admin_router.put("/change_user_type/{userId}/{token}/{user_type}", status_code=204)
async def change_user_type(userId: int, token:str, user_type:str, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        user = db.query(User).filter(User.user_id == userId).first()
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")
        user.role = user_type
        db.add(user)
        db.commit()
    else:
        raise HTTPException(detail='Only admin can access this route')
    
@admin_router.delete('/delete_user_details/{userId}/{token}', status_code=status.HTTP_200_OK)
async def delete_user_details(userId: str,token:str, db:db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        user_query = db.query(User).filter(User.user_id == userId)
        userdetails = user_query.first()
        if not userdetails:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user details with this id: {id} found')
        user_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(detail='Only admin can access this route')

    
    
    return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'message': "user details deleted successfully"
        }

@admin_router.get('/get_property_details_for_admin/{token}')
async def get_property_details_for_admin(token:str, db: db_dependency,limit: int = 50, page: int = 1, search: str = ''):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        skip = (page - 1) * limit

        get_room_details = db.query(RoomDetails).filter(
        RoomDetails.locality.contains(search)).limit(limit).offset(skip).all()
    
        return {
            'status':status.HTTP_200_OK, 
            'success':True,
            'results': len(get_room_details), 
            'message':'successfully get all property details',
            'property details': get_room_details
        }
    else:
        raise HTTPException(detail='Only admin can access this route')
 

@admin_router.get('/get_property_details_by_id_for_admin/{roomId}/{token}', status_code=status.HTTP_200_OK)
async def get_property_details_by_id_for_admin(roomId: str, token:str, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        get_room_details_by_id = db.query(RoomDetails).filter(RoomDetails.room_id == roomId).first()

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
        raise HTTPException(detail='Only admin can access this route')

@admin_router.put("/approve_properties/{property_id}/{token}", status_code=204)
async def approve_property(property_id: int,token:str, db:db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        property = db.query(RoomDetails).filter(RoomDetails.room_id == property_id).first()

        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
    
        property.status = "approved"
        db.add(property)
    else:
        raise HTTPException(detail='Only admin can access this route')    
    db.commit()

@admin_router.put("/block_properties/{property_id}/{token}", status_code=204)
async def block_property(property_id: int,token:str, db: db_dependency):
    current_user= verify_token(token)

    if current_user['role'] == 'admin':
        property = db.query(RoomDetails).filter(RoomDetails.room_id == property_id).first()

        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
   
        property.status = "blocked"
        db.add(property)
    else:
        raise HTTPException(detail='Only admin can access this route')   
    db.commit()
