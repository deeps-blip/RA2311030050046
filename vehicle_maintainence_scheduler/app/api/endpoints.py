from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.depot import Depot
from app.schemas.task import Task, ScheduleResponse
from app.services.storage_service import storage
from app.core.scheduler import schedule_tasks

router = APIRouter()

@router.post("/depots", response_model=Depot)
async def create_depot(depot: Depot):
    storage.add_depot(depot)
    return depot

@router.get("/depots", response_model=List[Depot])
async def list_depots():
    return storage.get_depots()

@router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    storage.add_task(task)
    return task

@router.get("/tasks", response_model=List[Task])
async def list_tasks():
    return storage.get_tasks()

@router.post("/schedule/{depot_id}", response_model=ScheduleResponse)
async def get_schedule(depot_id: str):
    depot = storage.get_depot(depot_id)
    if not depot:
        raise HTTPException(status_code=404, detail="Depot not found")
    
    tasks = storage.get_tasks()
    if not tasks:
        return ScheduleResponse(
            depot_id=depot_id,
            selected_tasks=[],
            total_impact=0,
            total_duration=0,
            available_hours=depot.mechanic_hours
        )
    
    selected, total_impact, total_duration = schedule_tasks(tasks, depot.mechanic_hours)
    
    return ScheduleResponse(
        depot_id=depot_id,
        selected_tasks=selected,
        total_impact=total_impact,
        total_duration=total_duration,
        available_hours=depot.mechanic_hours
    )
