import os;
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client["finance-dashboard"]
budget_collection = db["budgets"]

def get_budget_collection():
    return budget_collection