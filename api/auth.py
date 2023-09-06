from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pymongo import MongoClient
from .models import Token, User
from settings import DATABASE_URL
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from settings import SECRET_KEY, ALGORITHM

router = APIRouter()


client = MongoClient(DATABASE_URL)
db = client.get_database()
users_collection = db['users']


password_hasher = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

from fastapi import Depends

@router.get("/protected-resource")
async def protected_resource(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return {"message": "Access granted", "user": payload["sub"]}


def is_token_expired(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_timestamp = payload.get("exp")
        if expiration_timestamp:
            expiration_datetime = datetime.fromtimestamp(expiration_timestamp)
            return expiration_datetime < datetime.utcnow()
        else:
            return True  
    except JWTError:
        return True  
    
print('entering')

@router.post("/register")
async def register_user(user: User):
    print('inside register')
   
    existing_user = users_collection.find_one({"email": user.email})
    print(existing_user,'existing userrrrrrrrrrrrr')
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
  
    hashed_password = password_hasher.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print("form_data",form_data)
    user = users_collection.find_one({"email": form_data.username})
    print("user", user)
    if not user or not password_hasher.verify(form_data.password, user["password"]):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = datetime.utcnow() + access_token_expires
    
 
    access_token = create_access_token(
        data={"sub": user["email"], "exp": expiration},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/check-token-expiration")
async def check_token_expiration(token: str = Depends(oauth2_scheme)):
    if is_token_expired(token):
        raise HTTPException(status_code=401, detail="Token has expired")
    else:
        return {"message": "Token is valid and not expired"}


