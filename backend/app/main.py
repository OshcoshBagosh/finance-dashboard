from fastapi import FastAPI
from .api.budget_routes import router as budget_router
from .api.user_routes import router as user_router
from .api.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status":"ok"}

app.include_router(budget_router, prefix="/budgets", tags=["Budgets"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])