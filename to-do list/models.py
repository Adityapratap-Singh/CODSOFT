from datetime import datetime

class Task:
    def __init__(self, title, description, start_time, deadline, priority, tags, subtasks, recurring=None, completed=False):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.deadline = deadline
        self.priority = priority
        self.tags = tags
        self.subtasks = subtasks
        self.recurring = recurring  # <-- Add this line
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "deadline": self.deadline.isoformat(),
            "priority": self.priority,
            "tags": self.tags,
            "subtasks": self.subtasks,
            "recurring": self.recurring,  # <-- Add this line
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        from datetime import datetime
        return Task(
            data["title"],
            data.get("description", ""),
            datetime.fromisoformat(data["start_time"]),
            datetime.fromisoformat(data["deadline"]),
            data.get("priority", "Low"),
            data.get("tags", []),
            data.get("subtasks", []),
            data.get("recurring", None),  # <-- Add this line
            data.get("completed", False)
        )

