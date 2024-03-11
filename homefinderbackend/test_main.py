# from fastapi.testclient import TestClient
# import pytest
# from httpx import AsyncClient
# from main import app

# client = TestClient(app)

# @pytest.fixture
# def test_client():
#     return TestClient(app)

# def test_home():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Welcome to HomeFinder"}

# =================================================================
# ================ test cases for auth_routes =====================
# =================================================================

# def test_create_user(test_client):
#     user_data = {
#         "name": "Shan",
#         "email": "shanxxx@gmail.com",
#         "mobile": "1234567890",
#         "password": "Abc1abc2",
#         "role": "user",
#         "is_active": "True"
#     }
#     response = test_client.post('/create-user', json=user_data)
#     assert response.status_code == 200
#     assert response.json() == {
#         "status": status.HTTP_200_OK,
#         "success": True,
#         "message": "user created sucessfully"
#     }

# @pytest.fixture(scope="module")
# def test_user():
#     return {"email": "shobha@gmail.com", "password": "shobha@12345"}

# def test_login(test_client, test_user):
    
#     login_response = test_client.post("/login", json=test_user)

#     assert login_response.status_code == 200
#     # token = login_response.json()["access_token"]

#     # print("========================================",login_response.json())
#     assert login_response.json() == {
#             "access_token": login_response.json()["access_token"], 
#             "token_type": "bearer"
#         }
    
# def test_change_password(test_client,test_user):
#     # token={'Authorization': f"Bearer {create_access_token}"}
#     token = test_login(test_client, test_user)
#     data= {"email":"rahul@gmail.com", "old_password":"rahul@123","new_password":"rahul@12345"}
#     response = test_client.post("/change-password", json=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200

#     assert response.json() == {
#         "message": "password changed successfully"
#     }


# =================================================================
# ================ test cases for owner_routes =====================
# =================================================================
    
# def test_create_item(test_client,test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     print("=================================",login_response)
#     token = login_response.json()["access_token"] 
#     print("++++_====================================", token)
#     sample_data={
#         "user_id": "8", "locality": "Magarpatta", "address": "Pune-Magarpatta",
#         "bhk":"2-BHK","beds":"Double","rent":"22000",
#         "carpet_area":"780","amenities":"Semi-Furnished",
#         "services":"Parking","category":"Flat",
#         "owner_name":"Prakash jadhav","owner_mobile":"1234567890"
#     } 
    
#     response = test_client.post('/add_property_details', 
#                                 json=sample_data, 
#                                 headers={"Authorization": f"Bearer {token}"}
#                 )
    
#     assert response.status_code == 201
#     assert response.json() == {
#             "message":"property details added successfully",
            # 'added property details':sample_data 
#         }


# def test_get_property_details(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"] 

#     data={"userid":8}
#     response = test_client.get("/get_property_details", params=data, headers={'Authorization': f'Bearer {token}'} )
#     assert response.status_code == 200

#     missingID_response = test_client.get("/get_property_details",  headers={'Authorization': f'Bearer {token}'} )
#     assert missingID_response.status_code == 422

# def test_get_property_details_by_id(test_client,test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"] 
#     data={"userid":8,"roomId":17}
#     response = test_client.get("/get_property_details_by_id/17", params=data, headers={"Authorization": f"Bearer {token}", "user_id":"8"} )
#     print("=============================",response.json())
#     assert response.status_code == 200
    
# def test_update_property_details(test_client,test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"] 
#     data={"userid":8,"roomId":19}
#     updated_data={
#         "user_id": "8", "locality": "Magarpatta", "address": "Pune-Magarpatta",
#         "bhk":"2-BHK","beds":"Double","rent":"22000",
#         "carpet_area":"880","amenities":"Semi-Furnished",
#         "services":"Parking","category":"Flat",
#         "owner_name":"Prakash jadhav","owner_mobile":"1234567890"
#     }
#     response = test_client.patch("/update_property_details/19", 
#                                  params=data,
#                                  json=updated_data, 
#                                  headers={"Authorization": f"Bearer {token}", "user_id":"8"} )
#     print("=============================",response.json())
#     assert response.status_code == 205


# def test_delete_property_details(test_client,test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"] 
#     data={"userid":8,"roomId":23}
   
#     response = test_client.delete("/delete_property_details/23", 
#                                  params=data,
#                                  headers={"Authorization": f"Bearer {token}", "user_id":"8"} )
#     print("=============================",response.json())
#     assert response.status_code == 200

# =================================================================
# ================ test cases for admin_routes =====================
# =================================================================
    
# def test_get_user_details(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     response = test_client.get('/get_user_details',headers={"Authorization": f"Bearer {token}"} )
#     # print("==============*********************",response.json())
#     assert response.status_code == 200

# def test_get_user_details_by_id(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data={"userId":8}
#     response = test_client.get('/get_user_details_by_id/8', params=data , headers={"Authorization": f"Bearer {token}"} )
#     # print("==============*********************",response.json())
#     assert response.status_code == 200

# def test_update_user_activation(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data={"userId":24,"is_active":"False"}
#     response = test_client.put("/update_activation", params=data, headers={"Authorization": f"Bearer {token}"} )
#     print("==============*********************",response.json())

#     assert response.status_code == 200

# def test_approve_property(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data = {"property_id": 14}
#     response = test_client.put("/approve_properties/14", params=data, headers={"Authorization": f"Bearer {token}"})
#     # print("==============*********************",response.json())

#     assert response.status_code == 204

# def test_block_property(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data = {"property_id": 14}
#     response = test_client.put("/block_properties/14", params=data, headers={"Authorization": f"Bearer {token}"})
#     # print("==============*********************",response.json())

#     assert response.status_code == 204  

# def test_change_user_type(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data={"userId":45, "user_type":"admin"}
#     response = test_client.put("/change_user_type/45", params=data, headers={"Authorization": f"Bearer {token}"} )
#     assert response.status_code == 204  

# def test_delete_user_details(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data={"userId":24}
#     response = test_client.delete("/delete_user_details/24", params=data, headers={"Authorization": f"Bearer {token}"} )
#     assert response.status_code == 200

# =================================================================
# ================ test cases for user_routes =====================
# =================================================================
    
# def test_get_all_property_details(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     response = test_client.get("/get_all_property_details",headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200

# def test_get_history(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data={"userId":6}
#     response = test_client.get("/get_history/6", params=data, headers={"Authorization": f"Bearer {token}"} )
#     assert response.status_code == 200

# def test_search_property_details(test_client, test_user):
#     login_response = test_client.post("/login", json=test_user) 
#     token = login_response.json()["access_token"]
#     data = {"userid":6, "query": "wakad"}
#     response = test_client.get("/search", params=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
    