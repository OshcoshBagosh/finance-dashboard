from ..db.mongo import get_budget_collection
from fastapi import APIRouter
from ..models.budget import Budget
from typing import List, Optional
import datetime

budget_collection = get_budget_collection()

router = APIRouter()

@router.post("/budgets/", response_model=Budget)
async def create_budget(budget: Budget):
    budget_dict = budget.dict()
    result = await budget_collection.insert_one(budget_dict)
    inserted_id = str(result.inserted_id)
    budget_dict["_id"] = inserted_id
    return Budget(**budget_dict)

@router.get("/budgets/", response_model=List[Budget])
async def get_budgets(user_id:str, month:Optional[datetime.datetime] = None):
    query = {"user_id": user_id}
    if month:
        query["month"] = month
    
    budgets = await budget_collection.find(query).to_list(length=100)
    results = []
    for budget in budgets:
        budget["_id"] = str(budget["_id"])
        results.append(Budget(**budget))

    return results