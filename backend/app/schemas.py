from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PlanRequest(BaseModel):
    goal: str = "Build a AI model for Business Data Analysis and Insights Generation"

class Task(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    depends_on: Optional[List[str]] = []
    estimated_days: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class PlanResponse(BaseModel):
    plan_id: int
    goal: str
    tasks: List[Task]
