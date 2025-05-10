from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from ..db.mongo import get_user_collection

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

user_collection = get_user_collection()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
async def login_user(username: str, password: str) -> TokenResponse:
    query = {"username": username}
    user = await user_collection.find_one(query)
    
    if user is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    authenticated = pwd_context.verify(password, user["hashed_password"])
    
    if not authenticated:
        raise HTTPException(status_code=401)
    
    else:
        token = create_access_token(data={"user_id": str(user["_id"])})
        return TokenResponse(
            access_token= token,
            token_type= "bearer"
        )
        

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from ..models.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception

    return UserResponse(
        user_id=str(user["_id"]),
        username=user["username"],
        full_name=user.get("full_name")
    )