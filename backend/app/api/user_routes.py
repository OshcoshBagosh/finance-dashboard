from ..models.user import UserCreate, UserInDB, UserResponse
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from ..db.mongo import get_user_collection
from passlib.context import CryptContext


user_collection = get_user_collection()

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def register_user(user: UserCreate):
    query = {"username": user.username, "email": user.email}
    
    is_unique = await user_collection.find_one(query)
    
    if is_unique is not None:
        raise HTTPException(status_code=401, detail="Username or Email is already taken")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    hashed_password = pwd_context.hash(user.password)
    
    user_db = UserInDB(
        email= user.email,
        username= user.username,
        hashed_password= hashed_password
    )
    
    user_dict = user_db.dict(by_alias=True, exclude_none=True)
    
    result = await user_collection.insert_one(user_dict)
    
    inserted_id = str(result.inserted_id)
    
    return UserResponse(
        user_id= inserted_id,
        username= user.username,
        full_name= user.full_name
    )

from ..models.auth import get_current_user
from ..models.user import UserResponse
from fastapi import Depends

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user