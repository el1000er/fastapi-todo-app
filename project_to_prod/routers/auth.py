from datetime import datetime, timedelta, timezone
from fastapi import APIRouter,Depends,status,HTTPException,Request
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from ..database import  SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


## Parameters for JWT
## the secret can be any long string, for this one, I had to install git with openssl local
## the ran in powershell this command:  & "C:\Program Files\Git\usr\bin\openssl.exe" rand -hex 32
SECRET_KEY ='c9cd027ddf6e1fa93731966569475be3b449b7e0ed3835aef6ee5a91b4ebf6a8'
ALGORITHM ='HS256'

bcript_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str

class Token(BaseModel):
    access_token:str
    token_type:str
     
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Depends -> dependency injection
db_dependency = Annotated [Session,Depends(get_db)]

templates = Jinja2Templates(directory="project_to_prod/templates")


### Pages ###
@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.get('/register-page')
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html',{'request':request})





### Endpoints ###

def authenticate_user(username:str,password:str,db):
    user =db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcript_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int,role:str, expires_delta:timedelta):
    ## information that lives inside jwt
    encode = {'sub':username,'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role:str =payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return{'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,
                      create_user_request:CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcript_context.hash(create_user_request.password),
        is_active=True,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()
 

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:db_dependency):
    user= authenticate_user(form_data.username,form_data.password,db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
    
    token = create_access_token(user.username, user.id,user.role, timedelta(minutes=20))
    return {'access_token':token,'token_type':'bearer'}
 
'''

 ## BEARER

In simple terms, we are telling the application whoever "bears" the valid JWT is authorized.

In long terms:

A bearer token is a type of authentication token. In the context of security, a token is a piece of data that represents a specific set of permissions or claims.
The "bearer" of the token is granted those permissions or claims, hence the name.

Here's a bit more detail on the concept:

Bearer Authentication: When a user or system presents a bearer token to access a resource, they don't need to provide any other form of identification.
 Whoever "bears" the token can access the associated resources, making it crucial to protect the token.

Usage: Bearer tokens are commonly used in web authentication systems. For example, after logging into a website, the server may provide the client with a bearer token.
The client then includes this token with subsequent requests, allowing the server to recognize and authenticate the client without requiring the user to log in again. 
The OAuth 2.0 protocol for authorization also uses bearer tokens.
'''
