from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.task import Task

class Project:
    def __init__(self, title: str, description: str = "", due_date: str = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self._user = None
        self._tasks = []

    @property
    def user(self) -> 'User':
        return self._user

    @user.setter
    def user(self, value: 'User'):
        self._user = value

    @property
    def tasks(self) -> List['Task']:
        return self._tasks

    def add_task(self, task: 'Task'):
        if task not in self._tasks:
            self._tasks.append(task)
            task.project = self

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user": self.user.name if self.user else None,
            "tasks": [t.title for t in self._tasks]
        }

    def __repr__(self):
        return f"Project(title={self.title}, user={self.user.name if self.user else None})"
