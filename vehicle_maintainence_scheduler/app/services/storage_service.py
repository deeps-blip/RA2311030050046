from typing import List, Dict
from app.schemas.depot import Depot
from app.schemas.task import Task

class Storage:
    def __init__(self):
        self.depots: Dict[str, Depot] = {}
        self.tasks: Dict[str, Task] = {}

    def add_depot(self, depot: Depot):
        self.depots[depot.id] = depot

    def get_depots(self) -> List[Depot]:
        return list(self.depots.values())

    def get_depot(self, depot_id: str) -> Depot:
        return self.depots.get(depot_id)

    def add_task(self, task: Task):
        self.tasks[task.taskID] = task

    def get_tasks(self) -> List[Task]:
        return list(self.tasks.values())

storage = Storage()
