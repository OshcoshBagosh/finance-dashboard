from fastapi import APIRouter
from ..models.auth import LoginRequest, TokenResponse, login_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_route(login_data: LoginRequest):
    return await login_user(login_data.username, login_data.password)

from fastapi import Depends
from ..models.auth import get_current_user

@router.get("/me")
async def read_my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"]
    }