from pydantic import BaseModel
from typing import List

class CrashInput(BaseModel):
    revenue: List[float]
    expenses: List[float]
    cash_in_hand: float
    churn_rate: List[float]
    customers: List[int]