from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status,Path,Response
from ..models import Todos,Users
from ..database import  SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['user']
)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    


## Depends -> dependency injection
db_dependency = Annotated [Session,Depends(get_db)]

user_dependency = Annotated[dict,Depends(get_current_user)]
bcript_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password:str
    new_password: str = Field(min_length=6)

    
class UserPhoneRequest(BaseModel): 
    new_phone: str = Field(min_length=6)


@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user = db.query(Users).filter(Users.id==user.get('id')).first()
     
    return user

@router.put('/change_password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(response:Response,
                           db: db_dependency,
                            user: user_dependency,
                            user_verification: UserVerification ):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    try:
        user_record = db.query(Users).filter(Users.id==user.get('id')).first()
        if not user_record:
            raise HTTPException(status_code=404, detail='User not found')
        
        if not bcript_context.verify(user_verification.password,user_record.hashed_password):
            raise HTTPException(status_code=401, detail='Error on password change')
        
        user_record.hashed_password=bcript_context.hash(user_verification.new_password)
    
        db.commit()

         # Clear the JWT cookie to logout the user
        response.delete_cookie(key="access_token")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error updating password: {str(e)}')
    

@router.put('/phone_number',status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(response:Response,
                           db: db_dependency,
                            user: user_dependency,
                            user_phone_request: UserPhoneRequest ):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    try:
        user_record = db.query(Users).filter(Users.id==user.get('id')).first()
        if not user_record:
            raise HTTPException(status_code=404, detail='User not found')
        
      
        ## lo encripte sin querer pero bueno puede servir..
        user_record.phone_number=bcript_context.hash(user_phone_request.new_phone)
    
        db.commit()

         # Clear the JWT cookie to logout the user
        response.delete_cookie(key="access_token")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error updating phone: {str(e)}')
     
     
 