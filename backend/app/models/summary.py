from pydantic import BaseModel
from typing import Optional

class BudgetSummary(BaseModel):
    month: str
    category: str
    limit: float
    total_spent: Optional[float] = 0.0
    remaining: Optional[float] = 0.0