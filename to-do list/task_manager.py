# task_manager.py

import json
import os
from datetime import datetime
from models import Task
from export_utils import export_to_csv, export_to_pdf

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True

            # 🔁 If recurring, add the next instance
            if self.tasks[index].recurring:
                new_task = self.tasks[index].apply_recurring()
                if new_task:
                    self.tasks.append(new_task)

            self.save_tasks()

    def get_pending_tasks(self):
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self):
        return [t for t in self.tasks if t.completed]

    def get_all_tasks(self):
        return self.tasks

    def save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        with open(TASKS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            self.tasks = []
            return

        with open(TASKS_FILE, "r") as f:
            try:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
            except json.JSONDecodeError:
                self.tasks = []

    def export_as_json(self, filename="tasks_export.json"):
        data = [t.to_dict() for t in self.tasks]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def export_as_csv(self, filename="tasks_export.csv"):
        export_to_csv(self.tasks, filename)

    def export_as_pdf(self, filename="tasks_export.pdf"):
        export_to_pdf(self.tasks, filename)
