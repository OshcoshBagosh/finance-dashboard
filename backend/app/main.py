from fastapi import FastAPI
from .api.budget_routes import router as budget_router

app = FastAPI()

app.include_router(budget_router, prefix="/budgets", tags=["Budgets"])