from typing import List, Tuple
from app.schemas.task import Task

def schedule_tasks(tasks: List[Task], budget: int) -> Tuple[List[Task], int, int]:
    n = len(tasks)
    dp = [0] * (budget + 1)
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        task = tasks[i-1]
        for w in range(budget, task.duration - 1, -1):
            if dp[w - task.duration] + task.Impact > dp[w]:
                dp[w] = dp[w - task.duration] + task.Impact
                keep[i][w] = True

    selected_tasks = []
    w = budget
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected_tasks.append(tasks[i-1])
            w -= tasks[i-1].duration

    return selected_tasks[::-1], dp[budget], budget - w
