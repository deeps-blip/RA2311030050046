from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    taskID: str
    Impact: int
    duration: int

class ScheduleResponse(BaseModel):
    depot_id: str
    selected_tasks: List[Task]
    total_impact: int
    total_duration: int
    available_hours: int
