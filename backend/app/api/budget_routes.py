from ..db.mongo import get_budget_collection
from fastapi import APIRouter, HTTPException
from ..models.budget import Budget
from ..models.summary import BudgetSummary
from typing import List, Optional
from bson import ObjectId
import datetime

budget_collection = get_budget_collection()

router = APIRouter()

@router.post("/", response_model=Budget)
async def create_budget(budget: Budget):
    budget_dict = budget.dict()
    result = await budget_collection.insert_one(budget_dict)
    inserted_id = str(result.inserted_id)
    budget_dict["_id"] = inserted_id
    return Budget(**budget_dict)

@router.get("/", response_model=List[Budget])
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

@router.get("/{budget_id}", response_model=Budget)
async def get_budget(budget_id:str):
    try:
        budget = await budget_collection.find_one({"_id": ObjectId(budget_id)})

        if not ObjectId.is_valid(budget_id):
            raise HTTPException(status_code=404, detail="Budget not found")
        budget["_id"] = str(budget["_id"])
        return Budget(**budget)
    
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@router.put("/{budget_id}", response_model=Budget)
async def update_budget(budget_id:str, budget:Budget):
    if not ObjectId.is_valid(budget_id):
            raise HTTPException(status_code=404, detail="Budget not found")
    update = budget.dict(exclude_unset=True, by_alias=True)
    update.pop("_id", None)

    result = await budget_collection.update_one(
        {"_id": ObjectId(budget_id)},
        {"$set": update}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Budget not found or unchanged")
    
    updated = await budget_collection.find_one({"_id": ObjectId(budget_id)})
    updated["_id"] = str(updated["_id"])
    return Budget(**updated)

@router.delete("/{budget_id}", response_model=Budget)
async def delete_budget(budget_id:str):
    if not ObjectId.is_valid(budget_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await budget_collection.find_one_and_delete({"_id": ObjectId(budget_id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    result["_id"] = str(result["_id"])

    return Budget(**result)

@router.get("/summary", response_model=BudgetSummary)
async def get_budget_summary(user_id):
    query = {"user_id": user_id}
    budgets = budget_collection.find(query).to_list(length=100)

    summary = []

    for budget in budgets:
        month_str = budget["month"].strftime("%Y-%m")
        remaining = budget["limit"] - budget.get("total_spent", 0.0)
        summary.append(BudgetSummary(
            month=month_str,
            category=budget["category"],
            limit=budget["limit"],
            total_spent=budget.get("total_spent", 0.0),
            remaining=remaining
        ))

    return summary

from ..models.auth import get_current_user
from ..models.user import UserResponse
from fastapi import Depends

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user

