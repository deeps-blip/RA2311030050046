import unittest
from app.core.scheduler import schedule_tasks
from app.schemas.task import Task

class TestScheduler(unittest.TestCase):
    def test_schedule_tasks_basic(self):
        tasks = [
            Task(id="1", duration=2, importance=10),
            Task(id="2", duration=3, importance=15),
        ]
        selected, total_imp, total_dur = schedule_tasks(tasks, 4)
        self.assertEqual(total_imp, 15)
        self.assertEqual(total_dur, 3)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].id, "2")

    def test_schedule_tasks_full(self):
        tasks = [
            Task(id="1", duration=2, importance=10),
            Task(id="2", duration=3, importance=15),
        ]
        selected, total_imp, total_dur = schedule_tasks(tasks, 5)
        self.assertEqual(total_imp, 25)
        self.assertEqual(total_dur, 5)
        self.assertEqual(len(selected), 2)

    def test_schedule_tasks_zero_budget(self):
        tasks = [Task(id="1", duration=2, importance=10)]
        selected, total_imp, total_dur = schedule_tasks(tasks, 0)
        self.assertEqual(total_imp, 0)
        self.assertEqual(total_dur, 0)
        self.assertEqual(len(selected), 0)

if __name__ == '__main__':
    unittest.main()
