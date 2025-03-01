from .utils import *
from ..routers.users import get_db,get_current_user
from fastapi import status
from ..models import Users
 

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None
    assert response.json()['username'] =='admin'
    assert response.json()['email'] =='admin@test.com'
    assert response.json()['first_name'] =='ad'
    assert response.json()['last_name'] =='min'
    assert response.json()['role'] =='admin'
    assert response.json()['phone_number'] =='(111)-111-1111'
 


def test_change_password_succes(test_user):
    response = client.put("/user/password",json={"password":"asdzxc3033",
                                                 "new_password":"test123"})
    response.status_code==status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
        response = client.put("/user/password",json={"password":"asdzxc3133",
                                                 "new_password":"test123"})
        response.status_code==status.HTTP_401_UNAUTHORIZED
        response.json()=={'detail':'Error on password change'}
        
def test_change_phone_number_success(test_user):
        response = client.put("/user/phonenumber/222222222")
        response.status_code==status.HTTP_204_NO_CONTENT
        