from fastapi import APIRouter
from ..models.auth import LoginRequest, TokenResponse, login_user

router = APIRouter()

from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=TokenResponse)
async def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data.username, form_data.password)


from ..models.auth import get_current_user
from ..models.user import UserResponse
from fastapi import Depends

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user