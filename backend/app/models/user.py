from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserInDB(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    username: str
    hashed_password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    username: str
    full_name: Optional[str] = None