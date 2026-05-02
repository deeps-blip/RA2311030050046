import httpx
from typing import List
from app.schemas.task import Task

async def fetch_tasks() -> List[Task]:
    return [
        Task(id="T1", duration=2, importance=10),
        Task(id="T2", duration=3, importance=15),
        Task(id="T3", duration=5, importance=25),
        Task(id="T4", duration=7, importance=35),
        Task(id="T5", duration=1, importance=8),
        Task(id="T6", duration=4, importance=20),
    ]
