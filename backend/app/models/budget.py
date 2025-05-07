from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, confloat
from typing import Optional
import datetime

app = FastAPI()

class Budget(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    category: str = Field(..., example="Food")
    limit: confloat(ge=0)
    month: datetime.datetime
    total_spent: Optional[float] = 0.0

    class Config:
        allow_population_by_field_name = True