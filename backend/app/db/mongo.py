import os;
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client["finance-dashboard"]
budget_collection = db["budgets"]
user_collection = db["users"]

def get_budget_collection():
    return budget_collection

def get_user_collection():
    return user_collection